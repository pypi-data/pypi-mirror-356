from typing import Dict
from .translatable import to_translatable,parse_translatable
from .time import Timestamp
from .survey import Study, Survey, SurveyGroupItem, SurveyItemValidation, SurveySingleItem, SurveyItemGroupComponent, SurveyItemResponseComponent, SurveyItemComponent
from .expression import expression_arg_parser, expression_parser, Scalar

def component_parser(obj):
    role = obj['role']
    key =  obj.get('key')

    comp = None
    if 'items' in obj:
        # ItemGroupComponent
        ii = []
        for it in obj['items']:
            ii.append(component_parser(it))
        
        if 'order' in obj:
           order = expression_parser(obj['order'])
        else:
            order = None
        comp = SurveyItemGroupComponent(key=key, role=role, items=ii, order=order)

    if 'dtype' in obj:
        # ResponseComponent
        if comp is not None:
            raise Exception("Component cannot be group and response type")
        comp = SurveyItemResponseComponent(key=key, role=role, dtype=obj['dtype'])

    if comp is None:
        # ItemComponent base (Display ?)
        comp = SurveyItemComponent(key=key, role=role)

    if 'content' in obj:
        comp.content = parse_translatable(obj['content'])
    
    if 'properties' in obj:
            def parse_comp(value):
                if isinstance(value, str):
                    return Scalar("str", value)
                if isinstance(value, (int, float)):
                    return Scalar("num", value)
                return expression_arg_parser(value)
            pp = {}

            for k, p in obj['properties'].items():
                pp[k] = parse_comp(p)
            comp.properties = pp

    if 'description' in obj:
        comp.description = parse_translatable(obj['description'])

    if 'displayCondition' in obj:
        comp.displayCondition = expression_parser(obj['displayCondition'])

    if 'disabled' in obj:
        comp.disabled = expression_parser(obj['disabled'])

    if 'style' in obj:
        ss = {}
        for s in obj['style']:
            ss[s['key']] = s['value']
        comp.style = ss

    return comp

def survey_item_parser(obj):
    _id = obj.get('id')
    key = obj['key']
    if 'items' in obj:

        ii = []
        for i in obj['items']:
            ip = survey_item_parser(i)
            ii.append(ip)
        if 'selectionMethod' in obj:
            selection = expression_parser(obj['selectionMethod'])
        else:
            selection = None
        item = SurveyGroupItem(key,  id=_id, items=ii, selection=selection)

    else:
        comp = None
        if 'components' in obj:
            comp = component_parser(obj['components'])
        _type = obj.get('type')
        if 'validations' in obj:
            vv = []
            for v in  obj['validations']:
                rule = expression_parser(v['rule'])
                validation = SurveyItemValidation(v['key'], v['type'], rule) 
                vv.append(validation)
            validations = vv
        else:
            validations = None
        item = SurveySingleItem(key, id=_id, type=_type, components=comp, validations=validations)

    if 'condition' in obj:
        condition = expression_parser(obj['condition'])
        item.condition = condition
    if 'follows' in obj:
        item.follows = obj['follows']
    
    if 'priority' in obj:
        item.priority = obj['priority']

    if 'metadata' in obj:
        item.setMetadata(obj['metadata'])

    return item

def context_rules_parser(ctx: Dict):
    if 'mode' in ctx:
        ctx['mode'] = expression_arg_parser(ctx['mode'])
    if 'previousResponses' in ctx:
        rr = []
        for r in ctx['previousResponses']:
            exp = expression_parser(r)
            rr.append(exp)
        ctx['previousResponses'] = rr
    return ctx


def survey_parser(survey:Dict):
    """
    Parse a dictionary based survey (loaded from a json definition file) model into a python object model
    
    Returns: Survey

    """
    pp =  survey['props']
    pp = to_translatable(pp, ['name','description', 'typicalDuration'])
    survey['props'] = pp
    if 'published' in survey:
        # published is not present when survey is only a draft from editor
        survey['published'] = Timestamp(survey['published'])
    if 'unpublished' in survey:
        survey['unpublished'] = Timestamp(survey['unpublished'])
    survey['surveyDefinition'] = survey_item_parser(survey['surveyDefinition'])

    if 'prefillRules' in survey:
        rr = []
        for r in survey['prefillRules']:
            exp = expression_parser(r)
            rr.append(exp)
        survey['prefillRules'] = rr

    if 'contextRules' in survey:
        survey['contextRules'] = context_rules_parser(survey['contextRules'])

    return Survey(survey)

def study_parser(study):
    """"
     Parse study to have some elements easier to represents (like expression)
    """
    if 'rules' in study:
        # Replace
        rr = []
        for rule in study['rules']:
            r = expression_parser(rule)
            rr.append(r)
        study['rules'] = rr
    if 'props' in study:
        pp = study['props']
        pp = to_translatable(pp, ['name','description'])
        if 'tags' in pp:
            tt = []
            for tag in pp['tags']:
                if 'label' in tag:
                    tag['label'] = parse_translatable(tag['label'])
                tt.append(tag)
            pp['tags'] = tt
        study['props'] = pp
    return Study(study)
