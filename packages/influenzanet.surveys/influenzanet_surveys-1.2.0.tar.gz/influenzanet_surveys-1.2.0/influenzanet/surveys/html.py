from typing import Dict, Union

from influenzanet.surveys.influenzanet.survey import Survey
from .influenzanet import survey_parser
from jinja2 import Template, FileSystemLoader, Environment
from .context import Context, create_context
from .templates.html import get_html_path
import os
import json
import glob
import traceback

known_styles = {
  'item': 'card',
  'translate-list': 'list-unstyled',
  'trans-code': 'badge badge-light',
  'components': 'card',
  'item-version': 'badge badge-success',
  'role': 'badge badge-warning',
}

def styles(name):
    if name in known_styles:
        return known_styles[name] + ' '+ name
    return name

def survey_to_html(survey:Union[Dict, Survey], context: Context):
    """
        Build an HTML document from a survey json
    """

    if not isinstance(survey, Survey):
        survey = survey_parser(survey)

    path = get_html_path()

    env = Environment(loader=FileSystemLoader(path), autoescape='html',)
    env.globals['language'] = context.get_language()
    env.globals['context'] = context
    env.globals['styles'] = styles
    
    template = env.get_template('survey.html')
    
    with open(path + '/survey.css') as f:
        theme = f.read()

    ctx = {
        'survey': survey,
        'theme_css': theme
    }
    return template.render(ctx)

def build_html_from_dir(path, languages):
    """"
        Helper function to build html files of all json files in a directory (recursively)
    """

    for f in glob.glob(path + "/*.json", recursive=True):
        print(f)
        survey = json.load(open(f, 'r', encoding='UTF-8'))

        if "studyKey" in survey:
            # A study entry
            survey = survey['survey']

        if not "props" in survey or not "surveyDefinition" in survey:
            print("%s is not a survey json" % f)
            continue
        try:
            h = survey_to_html(survey, context=create_context(language=languages))

            fn, ext = os.path.splitext(f)
            with open(fn + '.html', 'w') as o:
                o.write(h)
        except Exception as e:
            print("Unable to process '%s'" % (f))
            traceback.print_exception(e)


