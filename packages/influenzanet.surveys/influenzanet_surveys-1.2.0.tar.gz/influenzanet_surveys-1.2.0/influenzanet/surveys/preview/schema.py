
from typing import Dict, Optional, List
from . import models as preview
from .models import SurveyPreviewOption, SurveyPreviewQuestion, SurveyPreviewResponseGroup, SurveyPreview
from collections import OrderedDict

class SurveyRef:
    """
        SurveyRef keeps reference of the survey element providing a given column
    """
    def __init__(self, question, group_index=None, group_key=None, option=None, version=None):
        self.question = question
        self.group_index = group_index
        self.group_key = group_key
        self.option = option
        self.version = version

    def signature(self):
        """
        Return a function signature uniquely identifying reference in a survey
        The version is not part of a signature, since the same ref can exists in several surveys
        """
        s = self.question
        if self.group_key is not None:
            s += "|%s" % (self.group_key)

        if self.option is not None:
            s += "/" + self.option
        return s
    
    def to_dict(self):
        return {'question': self.question, 'group': [self.group_index, self.group_key], 'option': self.option, 'version': self.version}
    
class SurveyExportColumn:
    """
        SurveyExportColumn holds information about an exported column
    """

    def __init__(self, column_name:str, value_type:str, ref: SurveyRef):
        self.name = column_name
        self.value_type = value_type
        self.ref = ref
        self.seen_at = []

    def visit(self, version: str):
        self.seen_at.append(version)

    def to_dict(self):
        return {"name": self.name, "type": self.value_type, "ref": self.ref.to_dict(), "seen": self.seen_at}

class SchemaProblem:

    def __init__(self, ref:SurveyRef, context=None):
        self.ref = ref
        self.context = context

    def to_dict(self):
        return {"ref": self.ref.to_dict(), "context": self.context}

class SurveyExportSchema:
    """
        SurveyExportSchema holds the description of all exportable columns inferred from the survey preview
        A schema can be specific to a version, or be merge with several versions
        It also embeds list of eventual problems reported during the mapping process
    """
    def __init__(self, version=None):
        self.columns: Dict[str, SurveyExportColumn] = {}
        self.problems: Dict[str, List[SchemaProblem]] = {}
        self.version = version

    def register(self, column_name:str, value_type:str, ref: SurveyRef):
        if column_name in self.columns:
            prev = self.columns[column_name]
            problem_id = "duplicate:%s" % (column_name)
            self.report(problem_id, ref, {"prev":prev.ref})
            return
        self.columns[column_name] = SurveyExportColumn(column_name, value_type=value_type, ref=ref)

    def report(self, problem:str, ref: SurveyRef, context=None):
        if ref.version is None and self.version is not None:
            ref.version = self.version
        if problem not in self.problems:
            self.problems[problem] = []
        self.problems[problem].append(SchemaProblem(ref, context))

    def merge_problems(self, problems: Dict[str, List[SchemaProblem]]):
        for (id, pp) in problems.items():
            if id in self.problems:
                self.problems[id].extend(pp)
            else:
                self.problems[id] = pp

    def to_dict(self):
        cols = {}
        for name, column in self.columns.items():
            cols[name] = column.to_dict()
        problems = {}
        for name, probs in self.problems.items():
            pp = [ x.to_dict() for x in probs]
            problems[name] = pp
        return {"columns": cols, "problems": problems}
    
    def get_column_types(self):
        d = OrderedDict()
        for name, col in self.columns.items():
            d[name] = col.value_type
        return d
        
    
QUESTION_TYPES_SINGLE_GROUP = ['single_choice', 'multiple_choice']
OPTION_OPEN_TYPES = ['text']

class HandlerResponse:
    """
        Build list of known columns for a given response of a question
    """

    def __init__(self, separator: str, question: SurveyPreviewQuestion, single_slot: bool, value_type:Optional[str]=None):
        """
            value_type: optional type for the value (type of response)
            separator: question/option separator (given to response exporter)
            question: the question to handle
        """
        self.value_type = value_type
        self.separator = separator
        self.question = question
        single_rg = len(question.responses) == 1
        # If true, the response group key will be omited in the column name if there is only one response group (RG) for a question
        # It's the case for common question types, expecting usually only one RG, like single choice
        if single_slot and single_rg:
            self.use_rg_key = False
        else:
            self.use_rg_key = True
        
    def as_ref(self, rg: SurveyPreviewResponseGroup, option: Optional[SurveyPreviewOption]=None):
        """
            Creates a reference to the currently handled element of the survey
        """
        o_key = None
        if option is not None:
            o_key = option.key
        return SurveyRef(question=self.question.key, group_index=rg.element_index, group_key=rg.key, option=o_key)

    def build_response(self, rg: SurveyPreviewResponseGroup, schema: SurveyExportSchema):
        """
            Build response columns
        """
        pass

    def value_column(self, rg:SurveyPreviewResponseGroup):
        """
            Value column builds a name when a single value is expected for a question response
            The name of the column depends on the context if the question type handle the response group key or not
        """
        if self.use_rg_key:
            return self.question.key + self.separator + rg.key
        return self.question.key
        
    def option_column(self, rg:SurveyPreviewResponseGroup, id):
        """
             builds a column name for an option of a response group
        """
        if self.use_rg_key:
            prefix = self.question.key + self.separator + rg.key + '.'
        else:   
            prefix = self.question.key + self.separator
        return prefix + id


class HandlerSingleChoice(HandlerResponse):

    def build_response(self, rg: SurveyPreviewResponseGroup, schema: SurveyExportSchema):
        schema.register(self.value_column(rg), 'str', self.as_ref(rg))
        if len(rg.options) == 0:
            return
        for option in rg.options:
            if option.option_type not in ['radio', 'dropdown']:
                o_ref = self.as_ref(rg, option)
                # Other like input have extra columns
                # Option key can be composite (option key + '.' + sub cloze key )
                name = self.option_column(rg, option.key)
                schema.register(name, 'str', o_ref)

class HandlerValue(HandlerResponse):

    def build_response(self, rg: SurveyPreviewResponseGroup, schema: SurveyExportSchema):
        schema.register(self.value_column(rg), self.value_type, self.as_ref(rg))

class HandlerMultipleChoice(HandlerResponse):
    
    def build_response(self, rg: SurveyPreviewResponseGroup, schema: SurveyExportSchema):
        for option in rg.options:
            o_ref = self.as_ref(rg, option)
            name = self.option_column(rg, option.key)
            is_embedded = option.is_embedded_cloze()
            column_type = 'bool'
            if is_embedded:
                column_type = option.option_value_type()
            schema.register(name, column_type, o_ref)
            # If it's not a checkbox, and not embedded, then it's an open option
            # create the associated column
            if option.option_type not in [preview.OPTION_TYPE_CHECKBOX] and not is_embedded:
                if option.option_type == preview.OPTION_TYPE_CLOZE:
                    open_name = self.option_column(rg, option.key)
                else:
                    open_name = name + self.separator + preview.OPEN_FIELD_COL_SUFFIX
                schema.register(open_name, 'str', o_ref)

class HandlerCloze(HandlerResponse):
    def build_response(self, rg: SurveyPreviewResponseGroup, schema: SurveyExportSchema):
        for option in rg.options:
            if option.option_type not in ['radio', 'dropdown']:
                o_ref = self.as_ref(rg, option)
                # Other like input have extra columns
                # Option key can be composite (option key + '.' + sub cloze key )
                name = self.option_column(rg, option.key)
                schema.register(name, 'str', o_ref)

class HandlerUnknown(HandlerResponse):
    def build_response(self, rg: SurveyPreviewResponseGroup, schema: SurveyExportSchema):
        schema.register(self.value_column(rg), 'json', self.as_ref(rg))

class HandlerEmpty(HandlerResponse):
    def build_response(self, rg: SurveyPreviewResponseGroup, schema: SurveyExportSchema):
        # Nothing to do
        pass

class HandlerQuestion:
    """
        Define a handler for a question
    """
    def __init__(self, handler:type[HandlerResponse], single_slot:bool, value_type:Optional[str]=None):
        self.handler = handler
        self.single_slot = single_slot
        self.value_type = value_type

    def build(self, question: SurveyPreviewQuestion, separator: str, schema: SurveyExportSchema):
        h = self.handler(separator=separator, question=question, single_slot=self.single_slot, value_type=self.value_type)
        for rg in question.responses:
            h.build_response(rg, schema) 

HANDLERS: Dict[str, HandlerQuestion] = {}

def handler_def(question_type:str, handler:type[HandlerResponse], single_slot:bool, value_type:Optional[str]=None):
    if question_type in HANDLERS:
        raise KeyError("Duplicate handler for %s" % question_type)
    HANDLERS[question_type] = HandlerQuestion(handler=handler, single_slot=single_slot, value_type=value_type)

def register_handlers():
    
    if len(HANDLERS) > 0:
        return

    # Single Choice and single choice like
    handler_def(preview.QUESTION_TYPE_SINGLE_CHOICE, HandlerSingleChoice, single_slot=True   ) 
    handler_def(preview.QUESTION_TYPE_DROPDOWN, HandlerSingleChoice, single_slot=True  )
    handler_def(preview.QUESTION_TYPE_LIKERT, HandlerSingleChoice, single_slot=True )
    handler_def(preview.QUESTION_TYPE_LIKERT_GROUP, HandlerSingleChoice, single_slot=True  )
    handler_def(preview.QUESTION_TYPE_RESPONSIVE_SINGLE_CHOICE_ARRAY, HandlerSingleChoice, single_slot=True  )
    handler_def(preview.QUESTION_TYPE_RESPONSIVE_BIPOLAR_LIKERT_ARRAY, HandlerSingleChoice, single_slot=True  )

    # Inputs
    handler_def(preview.QUESTION_TYPE_TEXT_INPUT, HandlerValue, single_slot=True, value_type='str')
    handler_def(preview.QUESTION_TYPE_NUMBER_INPUT, HandlerValue, single_slot=True, value_type='number')
    handler_def(preview.QUESTION_TYPE_NUMERIC_SLIDER, HandlerValue, single_slot=True, value_type='number')
    handler_def(preview.QUESTION_TYPE_DATE_INPUT, HandlerValue, single_slot=True, value_type='date')
    handler_def(preview.QUESTION_TYPE_EQ5D_SLIDER, HandlerValue, single_slot=True)
    handler_def(preview.QUESTION_TYPE_CONSENT, HandlerValue, single_slot=True, value_type='bool')
    
    # Multiple Choice
    handler_def(preview.QUESTION_TYPE_MULTIPLE_CHOICE, HandlerMultipleChoice, single_slot=True)
    
    # Responsive Table
    handler_def(preview.QUESTION_TYPE_RESPONSIVE_TABLE, HandlerValue, single_slot=False)
    
    # Matrix
    handler_def(preview.QUESTION_TYPE_MATRIX, HandlerValue, single_slot=False)
    handler_def(preview.QUESTION_TYPE_MATRIX_RADIO_ROW, HandlerValue, single_slot=False)
    handler_def(preview.QUESTION_TYPE_MATRIX_DROPDOWN, HandlerValue, single_slot=False)
    handler_def(preview.QUESTION_TYPE_MATRIX_INPUT, HandlerValue, single_slot=False)
    handler_def(preview.QUESTION_TYPE_MATRIX_NUMBER_INPUT, HandlerValue, single_slot=False, value_type='number')
    handler_def(preview.QUESTION_TYPE_MATRIX_CHECKBOX, HandlerValue, single_slot=False)

    # Cloze
    handler_def(preview.QUESTION_TYPE_CLOZE, HandlerMultipleChoice, single_slot=True)
    
    handler_def(preview.QUESTION_TYPE_UNKNOWN, HandlerUnknown, single_slot=False)
    
    handler_def(preview.QUESTION_TYPE_EMPTY, HandlerEmpty, single_slot=False)

    # case QUESTION_TYPE_SINGLE_CHOICE:
	# 	return processResponseForSingleChoice(question, response, questionOptionSep)
	# case QUESTION_TYPE_CONSENT:
	# 	return processResponseForConsent(question, response, questionOptionSep)
	# case QUESTION_TYPE_DROPDOWN:
	# 	return processResponseForSingleChoice(question, response, questionOptionSep)
	# case QUESTION_TYPE_LIKERT:
	# 	return processResponseForSingleChoice(question, response, questionOptionSep)
	# case QUESTION_TYPE_LIKERT_GROUP:
	# 	return handleSingleChoiceGroupList(question.ID, question.Responses, response, questionOptionSep)
	# case QUESTION_TYPE_RESPONSIVE_SINGLE_CHOICE_ARRAY:
	# 	return processResponseForSingleChoice(question, response, questionOptionSep)
	# case QUESTION_TYPE_RESPONSIVE_BIPOLAR_LIKERT_ARRAY:
	# 	return processResponseForSingleChoice(question, response, questionOptionSep)
	# case QUESTION_TYPE_MULTIPLE_CHOICE:
	# 	return processResponseForMultipleChoice(question, response, questionOptionSep)
	# case QUESTION_TYPE_TEXT_INPUT:
	# 	return processResponseForInputs(question, response, questionOptionSep)
	# case QUESTION_TYPE_DATE_INPUT:
	# 	return processResponseForInputs(question, response, questionOptionSep)
	# case QUESTION_TYPE_NUMBER_INPUT:
	# 	return processResponseForInputs(question, response, questionOptionSep)
	# case QUESTION_TYPE_NUMERIC_SLIDER:
	# 	return processResponseForInputs(question, response, questionOptionSep)
	# case QUESTION_TYPE_EQ5D_SLIDER:
	# 	return processResponseForInputs(question, response, questionOptionSep)
	# case QUESTION_TYPE_RESPONSIVE_TABLE:
	# 	return processResponseForResponsiveTable(question, response, questionOptionSep)
	# case QUESTION_TYPE_MATRIX:
	# 	return processResponseForMatrix(question, response, questionOptionSep)
	# case QUESTION_TYPE_CLOZE:
	# 	return processResponseForCloze(question, response, questionOptionSep)
	# case QUESTION_TYPE_UNKNOWN:
	# 	return processResponseForUnknown(question, response, questionOptionSep)

class SurveySchemaBuilder:

    def __init__(self, separator:str, prefix: str):
        self.separator = separator
        self.prefix = prefix
        # Global schema intented to hold a merge of all versions
        self.schema = SurveyExportSchema()
        register_handlers()

    def build_survey(self, survey: SurveyPreview, merge_schema:bool=True):
        """
            Build an export schema from a survey preview
            if merge_schema is True, merge with global schema
        """
        version_schema = SurveyExportSchema(version=survey.version)
        for question in survey.questions:
            handler = HANDLERS.get(question.question_type, None)
            if handler is None:
                version_schema.report("unknown_handle:%s" % (question.question_type), SurveyRef(question=question.key))
                continue
            handler.build(separator=self.separator, question=question, schema=version_schema)
        if merge_schema:
            self.merge_schema(version_schema)
        return version_schema
        
    def merge_schema(self, schema: SurveyExportSchema):
        for (name, column) in schema.columns.items():
            if name in self.schema.columns:
                prev = self.schema.columns[name]
                if column.ref.signature() != prev.ref.signature():
                    self.schema.report("ref_changed:%s" % name, column.ref, {"message": "'%s' vs '%s'" % (column.ref.signature(), prev.ref.signature())})
                else:
                    prev.visit(schema.version)
            else:
                self.schema.columns[name] = column
                column.visit(schema.version)

        self.schema.merge_problems(schema.problems)

class ReadableSchema:
    """
        Build a readable represnetation of schema content as a dictionnary
        This aims at show a readable (with short content) view once serialized in json/yaml
        It's not intented to produce data to be stored, but mostly printed on console
    """
    def __init__(self):
        pass

    def build(self, schema: SurveyExportSchema):
        cols = {}
        for (name, column) in schema.columns.items():
            cols[name] = self.readable_column(column)
        problems = {}
        for (name, pp) in schema.problems.items():
            problems[name] = [ self.readable_problem(x) for x in pp ]
        return {"columns": cols, "problems": problems}
        
    def readable_column(self, column:SurveyExportColumn):
        return "[%s] from %s (%s)" % (column.value_type, self.readable_ref(column.ref), ','.join( column.seen_at))
    
    def readable_ref(self, ref: SurveyRef):
        if ref.version is not None:
            v = '@' + str(ref.version)
        else: 
            v = ''
        return ref.signature() + v
    
    def readable_problem(self, problem: SchemaProblem):
        return 'from ' + self.readable_ref(problem.ref)