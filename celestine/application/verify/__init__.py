"""Package unittest."""

import os
import unittest
import pathlib

from celestine import load
from celestine.load.directory import find


from .text import MODULE
from .text import ERROR
from .text import CELESTINE

from celestine.application.verify.parser.test_operator import test_digit
from celestine.application.verify.parser.test_operator import test_unary
from celestine.application.verify.parser.test_operator import test_comparison

from celestine.application.verify.parser.test_translator import test_translator


from celestine.session.session import SuperSession

from celestine.typed import N

from celestine.window.page import Page


class Session(SuperSession):
    """"""


def main(_):
    """def main"""
    module = load.module("application", "verify", "hold")
    cats = find("test")
    for cat in cats:
        dog = pathlib.PurePath(cat)
        car = load.dictionary(*dog.parts)
        for (item, value) in car.items():
            setattr(module, item, value)

#    module = "celestine.application.viewer.verify"
#    module = MODULE
    unittest.main(
        module,
        None,
        [CELESTINE],
        None,
        unittest.defaultTestLoader,
        False,
        2,
        False,
        True,
        True,
        ERROR,
    )
