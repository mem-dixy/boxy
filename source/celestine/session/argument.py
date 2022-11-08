from argparse import ArgumentParser
import argparse
import dataclasses


from celestine.keyword.all import APPLICATION
from celestine.keyword.all import CELESTINE
from celestine.keyword.all import TASK
from celestine.keyword.all import application

from celestine.keyword.language import LANGUAGE
from celestine.keyword.language import language
from celestine.keyword.language import EN

from celestine.keyword.unicode import HYPHEN_MINUS


from celestine.keyword.language import code

APPLICATION = "application"
# help
INTERFACE = "interface"
# language
PYTHON = "python"
VERSION = "version"


@dataclasses.dataclass
class Argument():
    def flag(self, name):
        iterable = (HYPHEN_MINUS, name[:1])
        return str().join(iterable)

    def name(self, name):
        iterable = (HYPHEN_MINUS, HYPHEN_MINUS, name)
        return str().join(iterable)

    def meta(self, name):
        return name.upper()

    def __init__(self, exit_on_error, translate):
        self.parser = argparse.ArgumentParser(
            prog=CELESTINE,
            exit_on_error=exit_on_error,
        )

        self.parser.add_argument(
            self.flag(APPLICATION),
            self.name(APPLICATION),
        )

        self.parser.add_argument(
            self.flag(INTERFACE),
            self.name(INTERFACE),
            metavar=self.meta(INTERFACE),
        )

        self.parser.add_argument(
            flag(LANGUAGE),
            name(LANGUAGE),
            choices=code,
            default=EN,
            help=translate.LANGUAGE,
        )

        self.parser.add_argument(
            self.flag(PYTHON),
            self.name(PYTHON),
            choices=["3.7", "3.8"],
            metavar="cow",
        )

        self.parser.add_argument(
            self.flag(VERSION),
            self.name(VERSION),
            action=VERSION,
            version="0.4.0",
        )

        self.subparser = self.parser.add_subparsers(
            dest=TASK,
            required=False,
        )

        self.main = self.subparser.add_parser(
            "main",
            help="The default main application.",
        )


def flag(name):
    iterable = (HYPHEN_MINUS, name[:1])
    return str().join(iterable)


def name(name):
    iterable = (HYPHEN_MINUS, HYPHEN_MINUS, name)
    return str().join(iterable)


def meta(name):
    return name.upper()


def language(args, exit_on_error):
    parser = ArgumentParser(prog=CELESTINE, exit_on_error=exit_on_error)
    parser.add_argument(
        flag(LANGUAGE),
        name(LANGUAGE),
        choices=code,
        default=EN,
    )
    car = parser.parse_known_args(args)
    argument = parser.parse_known_args(args)[0]
    return argument.language
