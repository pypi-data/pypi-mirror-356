from typing import Dict,List, Optional

EMBEDDED_CLOZE_PREFIX = 'embedded_cloze_'

QUESTION_TYPE_CONSENT                         = "consent"
QUESTION_TYPE_SINGLE_CHOICE                   = "single_choice"
QUESTION_TYPE_MULTIPLE_CHOICE                 = "multiple_choice"
QUESTION_TYPE_TEXT_INPUT                      = "text"
QUESTION_TYPE_NUMBER_INPUT                    = "number"
QUESTION_TYPE_DATE_INPUT                      = "date"
QUESTION_TYPE_DROPDOWN                        = "dropdown"
QUESTION_TYPE_LIKERT                          = "likert"
QUESTION_TYPE_LIKERT_GROUP                    = "likert_group"
QUESTION_TYPE_EQ5D_SLIDER                     = "eq5d_slider"
QUESTION_TYPE_NUMERIC_SLIDER                  = "slider"
QUESTION_TYPE_RESPONSIVE_TABLE                = "responsive_table"
QUESTION_TYPE_MATRIX                          = "matrix"
QUESTION_TYPE_MATRIX_RADIO_ROW                = "matrix_radio_row"
QUESTION_TYPE_MATRIX_DROPDOWN                 = "matrix_dropdown"
QUESTION_TYPE_MATRIX_INPUT                    = "matrix_input"
QUESTION_TYPE_MATRIX_NUMBER_INPUT             = "matrix_number_input"
QUESTION_TYPE_MATRIX_CHECKBOX                 = "matrix_checkbox"
QUESTION_TYPE_RESPONSIVE_SINGLE_CHOICE_ARRAY  = "responsive_single_choice_array"
QUESTION_TYPE_RESPONSIVE_BIPOLAR_LIKERT_ARRAY = "responsive_bipolar_likert_array"
QUESTION_TYPE_CLOZE                           = "cloze"
QUESTION_TYPE_UNKNOWN                         = "unknown"
QUESTION_TYPE_EMPTY                           = "empty"


QUESTION_TYPE_INPUTS = [QUESTION_TYPE_TEXT_INPUT, QUESTION_TYPE_DATE_INPUT, QUESTION_TYPE_NUMBER_INPUT]

OPTION_TYPE_DROPDOWN_OPTION             = "option"
OPTION_TYPE_RADIO                       = "radio"
OPTION_TYPE_CHECKBOX                    = "checkbox"
OPTION_TYPE_TEXT_INPUT                  = "text"
OPTION_TYPE_DATE_INPUT                  = "date"
OPTION_TYPE_NUMBER_INPUT                = "number"
OPTION_TYPE_CLOZE                       = "cloze"
OPTION_TYPE_DROPDOWN                    = "dropdown"
OPTION_TYPE_EMBEDDED_CLOZE_TEXT_INPUT   = "embedded_cloze_text"
OPTION_TYPE_EMBEDDED_CLOZE_DATE_INPUT   = "embedded_cloze_date"
OPTION_TYPE_EMBEDDED_CLOZE_NUMBER_INPUT = "embedded_cloze_number"
OPTION_TYPE_EMBEDDED_CLOZE_DROPDOWN     = "embedded_cloze_dropdown"

OPEN_FIELD_COL_SUFFIX = "open"

class SurveyPreviewOption:

    def __init__(self, key:str, option_type:str, label:Optional[str]):
        self.key = key
        self.option_type = option_type
        self.label = label
        self.element_index = None

    def is_embedded_cloze(self):
        return self.option_type.startswith(EMBEDDED_CLOZE_PREFIX)

    def option_value_type(self):
        opt_type = self.option_type
        if self.is_embedded_cloze():
            opt_type = opt_type.removeprefix(EMBEDDED_CLOZE_PREFIX)
        if opt_type == "date":
            return "date"
        if opt_type == "number":
            return "number"
        return 'text'

    def readable(self, o: List = None):
        if o is None:
            o = []
        if self.label is not None:
            label = self.label
        else:
            label = ""
        o.append("      - %s : %s %s" % (self.key, self.option_type, label))
    
class SurveyPreviewResponseGroup:
    def __init__(self, key:str, response_type:str):
        self.key = key
        self.response_type = response_type
        self.element_index = None
        self.options : List[SurveyPreviewOption] = []

    def add_option(self, option: SurveyPreviewOption):
        self.options.append(option)

    def readable(self, o: List = None):
        if o is None:
            o = []
        o.append("   - RespGroup '%s' (%s)" % (self.key, self.response_type))
        for option in self.options:
            option.readable(o)
   
class SurveyPreviewQuestion:
    
    def __init__(self, key:str, title:str, question_type:str):
        self.key = key
        self.element_index = None
        self.title = title
        self.question_type = question_type
        self.responses: List[SurveyPreviewResponseGroup] = []

    def add_response(self, response: SurveyPreviewResponseGroup):
        self.responses.append(response)

    def readable(self, o: List = None):
        if o is None:
            o = []
        o.append(" - Question '%s' (%s)" % (self.key, self.question_type))
        for r in self.responses:
            r.readable(o)
    
class SurveyPreview:
    def __init__(self, version:str, published:int, unpublished=None) -> None:
        self.version = version
        self.published = published
        self.unpublished = unpublished
        self.questions: List[SurveyPreviewQuestion] = []

    def add_question(self, question:SurveyPreviewQuestion):
        self.questions.append(question)
    
    def readable(self, o: List = None):
        if o is None:
            o = []
        o.append("Survey version '%s'" % self.version )
        for q in self.questions:
            q.readable(o)
        return o
     
def _extract(data:Dict, name:str, cls, alt=None):
    """
        Helper to extract value from a dictionnary with an optional alternate name
    
    """
    v = None
    if name in data:
        v = data[name]
    else:
        if alt is not None and alt in data:
            v = data[alt]
        else:
            raise ValueError("Expecting field : '%s'" % (name) )
    if not isinstance(v, cls):
        raise ValueError("Field '%s' must of class '%s'" % (name, cls)) 
    return v     

def preview_question_from_json(d:dict):
    key = _extract(d, 'key', str, 'id')
    question_type = _extract(d, 'questionType', str)
    title = _extract(d,'title', str)
    question = SurveyPreviewQuestion(key, title, question_type)
    rr = _extract(d, 'responses', list)
    for index, r in enumerate(rr):
        response = preview_response_from_json(r)
        response.element_index = index
        question.add_response(response)
    return question

def preview_response_from_json(d:dict):
    key = _extract(d, 'key', str, 'id') # Some fields have been renamed in new backend version
    response_type = _extract(d, 'responseTypes', str, alt="responseType")
    response = SurveyPreviewResponseGroup(key, response_type)
    if 'options' in d:
        rr = _extract(d, 'options', list)
        for index, r in enumerate(rr):
            option = preview_option_from_json(r)
            option.element_index = IndexError
            response.add_option(option)
    return response

def preview_option_from_json(d:dict):
    key = _extract(d, 'key', str, 'id')
    if 'label' in d:
        label = _extract(d, 'label', str)
    else:
        label = None
    option_type = _extract(d, 'optionType', str)
    option = SurveyPreviewOption(key, option_type, label)
    return option

def preview_from_json(d):
    """
        Build SurveyPreview model from json
        If dictionnary is provided, it's handled as a single survey preview
    
    """
    if isinstance(d, dict):
        version = _extract(d, 'versionId', str)
        unpublished = None
        published = None
        if 'published' in d:
            published = int(d['published'])
        if 'unpublished' in d:
            unpublished = int(d['unpublished'])
        survey = SurveyPreview(version, published, unpublished)
        qq = _extract(d, 'questions', list)
        for index, q in enumerate(qq):
            question = preview_question_from_json(q)
            question.element_index = index
            survey.add_question(question)
        return survey
    if isinstance(d, list):
        versions = []
        for item in d:
            version = preview_from_json(item)
            versions.append(version)
        return versions