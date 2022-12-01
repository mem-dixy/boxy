"""Application for translating text to other languages."""
from celestine.application.translator.file import save
from celestine.application.translator.string import LANGUAGE
from celestine.application.translator.parser import dictionary_to_file
from .report import main as train
from .string import LANGUAGE

import uuid
import os.path
import shutil
import requests

from celestine.session import load
from celestine.application.translator.translator import Translator


from .string import WRITE
from .string import UTF_8

from celestine.application.translator.parser import word_wrap_dictionary


TRANSLATION = "translation"


SESSION = "session"
TRANSLATIONS = "translations"
TEXT = "text"
TO = "to"


def parser_magic(session):
    """Do all parser stuff here."""
    dictionary = {}
    azure_to_iso = {}
    override = {}
    code = []

    dir_translation = load.argument(TRANSLATION)
    for translation in dir_translation:
        module = load.module(TRANSLATION, translation)
        wow = load.dictionary(module)

        key = wow["LANGUAGE_TAG_AZURE"]
        value = wow["LANGUAGE_TAG_ISO"]
        azure_to_iso[key] = value
        code.append(key)

        override[translation] = wow
        dictionary[translation] = {}

    module = load.module("default", "language")
    thelist = load.dictionary(module)
    for name, value in thelist.items():

        items = post(session, code, value)
        for item in items:
            translations = item[TRANSLATIONS]
            for translation in translations:
                text = translation[TEXT]
                key = azure_to_iso[translation[TO]]
                dictionary[key][name] = text

    for translation in dir_translation:
        dictionary[translation] |= override[translation]

    return dictionary


def reset():
    """Remove the directory and rebuild it."""
    path = load.pathway(LANGUAGE)
    if os.path.islink(path):
        raise RuntimeError

    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=False, onerror=None)

    os.mkdir(path)


def header():
    """Write the header."""
    path = load.python(LANGUAGE, "__init__")
    with open(path, WRITE, encoding=UTF_8) as file:
        file.write('"""Lookup table for languages."""\n')


def save_item(dictionarys):
    """Save the items."""
    translations = load.argument(TRANSLATION)
    for translation in translations:
        dictionary = dictionarys[translation]
        path = load.python(LANGUAGE, translation)
        string = dictionary_to_file(dictionary)
        save(path, string)


def post(session, code, text):
    """Generate a post request."""
    translator = Translator(session.attribute)
    url = translator.endpoint()
    data = None
    json = [{TEXT: text}]
    headers = translator.header(str(uuid.uuid4()))
    params = translator.parameter(code)
    request = requests.post(url, data, json, headers=headers, params=params)
    return request.json()


def report(page):
    with page.line("head") as line:
        line.label("title", "Page 0")
    with page.line("body") as line:
        line.button("past", "Do Work", "reporter")


def one(page):
    with page.line("head") as line:
        line.label("title", "Page 1")
    with page.line("body") as line:
        line.button("past", "Page 0", 0)
        line.button("next", "Page 2", 2)


def two(page):
    with page.line("head") as line:
        line.label("title", "Page 2")
    with page.line("body") as line:
        line.button("past", "Page 1", 1)
        line.button("next", "Page 0", 0)


def main(session):
    """def main"""

    dictionary = parser_magic(session)

    # directory stuff
    # reset()
    # header()

    save_item(dictionary)

    print(dictionary)
    print("done")
    return [
        report,
        one,
        two,
    ]
