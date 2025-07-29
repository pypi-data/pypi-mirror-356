Influenzanet Survey Management
=====

influenzanet.surveys is a python library to work with influenzanet surveys, mainly validation and transformation

The purpose of this library is to work with existing surveys in json, it's not designed to create new survey json from scratch (for this use the typescript libraries).

## Installation

```python
pip install influenzanet.surveys

# To use validation
pip install influenzanet.surveys[validator]
```

## Features

- Parse json Survey definition into python object
- Parse [standards survey definition](https://github.com/influenzanet/surveys-standards), standards define the common questions/responses encoding for Influenzanet 
- Export survey in several format : html document, readable yaml (see formats) 
- Check survey internal consistency (reference for keys) and compliance to a standard definition

## Format

- html : view of a survey definition in a static html document (this is survey definition for humans)
- readable : a simplified view of a survey to see survey structure. Expression are transformed into function call-like text to be more readable. 

Each format accepts a "context" for the transformation, allowing, for example, to select the languages to be used in the output.

An helper is provided to build html for all json in a directory :

```python

from influenzanet.surveys.html import build_html_from_dir

## Accept glob patterns and transform all surveys json into html (if a json is not a survey it will be ignored)
## Creates an html file in the same directory for each json, replacing existing html if already exists
build_html_from_dir("output/**/surveys", languages=["en","fr"])
```

## Validation and Survey check

TBD