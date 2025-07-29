
from typing import Dict, List, OrderedDict
from ..utils import read_json

# Survey version here is related to the survey-engine.ts version
# 1.1 = Survey with old history model (current and history fields, and SurveyItem with version,versionTags field) 
# 1.2 = Survey with only current (Survey doesnt embeds history anymore)

def read_survey_json(file):
    """
        Load a json survey and transform it to new format if needed
    """
    json = read_json(file)
    if 'studyKey' in json and 'survey' in json:
        return survey_transform_to_12(json)

    if 'surveyDefinition' in json and 'props' in json:
        return json
    else:
        raise Exception("The file '%s' doesnt seem to be a survey definition" % file)

def require_fields(json, fields):
    for field in fields:
        if not field in json:
            raise Exception("Missing field '%s'" % field)

def survey_transform_to_12(json, preserve_item_version=False):

    try:
        require_fields(json, ['survey', 'studyKey'])
    except Exception as e:
        raise Exception("Doest seems to be a survey version 1.1 %s " % str(e))

    def transform_item(item):
        if 'version' in item:
            if preserve_item_version:
                item["metadata"] = {'version': str(item['version'])}
            del item['version']
        if 'versionTags' in item:
            del item['versionTags']
        if 'items' in item:
            item['items'] = list(map(transform_item, item['items']))
        return item

    survey = json['survey'] # First level not used any more
    surveyVersion = survey['current']
    del survey['current']
    survey['surveyDefinition'] = transform_item(surveyVersion['surveyDefinition'])
    survey['versionId'] = surveyVersion['versionId']

    return survey

def survey_transform_to_11(json, study_key):
    """
        Take a survey dictionary from a Survey version 1.1 
    
    """
    try:
        require_fields(json, ['surveyDefinition', 'versionId'])
    except Exception as e:
        raise Exception("Doest seems to be a survey version 1.2 %s " % str(e))
    
    def transform_item(item):
        item['version'] = 1
        if 'items' in item:
            item['items'] = list(map(transform_item, item['items']))
        return reorder_dict(item, ['key','version', 'items'])
    
    survey_version = {
        'versionId': json['versionId'],
        'surveyDefinition': transform_item(json['surveyDefinition']),
    }
    del json['surveyDefinition']
    del json['versionId']
    
    if 'unpublished' in json:
        survey_version['unpublished'] = json['unpublished']
        del json['unpublished']
    
    if 'published' in json:
        survey_version['published'] = json['published']
        del json['published']
    
    json['current'] = survey_version

    json = reorder_dict(json, ['id','props', 'current','history','prefillRules','contextRules', 'maxItemsPerPage', 'availableFor','requireLoginBeforeSubmission'])
    return {
         "studyKey": study_key,
         "survey": json
    }


def reorder_dict(data: Dict, fields:List[str]):
    """
    Reorder a dictionnary fields with a list of field to put as first fields
    Fields in data not in field list are placed at the end
    """
    old_keys = list(data.keys())
    new_keys = []
    for field in fields:
        if field in old_keys:
           new_keys.append(field)
           old_keys.remove(field)
    new_keys += old_keys # Add old keys remaining at the end
    d = OrderedDict()
    for field in new_keys:
        d[field] = data[field]
    return d