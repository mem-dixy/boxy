""""""

import argparse
from argparse import ArgumentParser as AP
from typing import TypeAlias as TA

from celestine import load
from celestine.session import word
from celestine.session.argument import (
    Application,
    Customization,
    InformationConfiguration,
    InformationHelp,
    InformationVersion,
    Optional,
    Positional,
)
from celestine.text import CELESTINE
from celestine.text.directory import (
    APPLICATION,
    INTERFACE,
    LANGUAGE,
)
from celestine.typed import (
    MT,
    TY,
    A,
    B,
    D,
    L,
    N,
    S,
)
from celestine.unicode import NONE

from .configuration import Configuration
from .session import (
    Dictionary,
    Session,
)
from .text import CONFIGURATION

INIT = "__init__"


# ADI: typing.TypeAlias = typing.Iterable[typing.Tuple[str, Argument]]

# APD: TA = D[U[Argument, T[Argument]], U[AP, AG]]
APD: TA = D[A, A]


def make_parser(language: MT, exit_on_error: B) -> AP:
    """"""

    class Error(argparse.ArgumentError):
        """Intercept help formating so translation can happen."""

        def __str__(self):
            value = word.parser_error(
                language.ARGUMENT_PARSER_ARGUMENT,
                self.argument_name,
                self.message,
            )
            return value

    class Formatter(argparse.HelpFormatter):
        """Intercept help formating so translation can happen."""

        def add_usage(self, usage, actions, groups, prefix=None):
            prefix = word.parser_formatter(
                language.ARGUMENT_PARSER_USAGE,
            )
            super().add_usage(usage, actions, groups, prefix)

    class Parser(argparse.ArgumentParser):
        """Intercept help formating so translation can happen."""

        def _check_value(self, action, value):
            try:
                super()._check_value(action, value)
            except argparse.ArgumentError as error:
                value = word.parser_value(
                    language.ARGUMENT_PARSER_CHOICE,
                    value,
                    language.ARGUMENT_PARSER_CHOOSE,
                    action.choices,
                )
                raise Error(action, value) from error

        def error(self, message):
            value = word.parser_parser_error(
                self.prog,
                language.ARGUMENT_PARSER_ERROR,
                message,
            )
            self.exit(2, value)
            # TODO: Seems to not be called in blender.
            # But do we even need this function?

    parser = Parser(
        add_help=False,
        # description="(cow)",
        # epilog="<moo>",
        formatter_class=Formatter,
        prog=CELESTINE,
        exit_on_error=exit_on_error,
    )

    return parser


def make_arguments(language: MT, parser: AP) -> APD:
    """"""

    application = parser.add_argument_group(
        title=language.ARGUMENT_APPLICATION_TITLE,
        description=language.ARGUMENT_APPLICATION_DESCRIPTION,
    )
    """your program stuff goes here. usefull, noone"""

    customization = parser.add_argument_group(
        title=language.ARGUMENT_CUSTOMIZATION_TITLE,
        description=language.ARGUMENT_CUSTOMIZATION_DESCRIPTION,
    )
    """all applications use these. usefull, everone"""

    information = parser.add_argument_group(
        title=language.ARGUMENT_INFORMATION_TITLE,
        description=language.ARGUMENT_INFORMATION_DESCRIPTION,
    )
    """displays information then exits. useless, noone"""

    modification = parser.add_argument_group(
        title=language.ARGUMENT_MODIFICATION_TITLE,
        description=language.ARGUMENT_MODIFICATION_DESCRIPTION,
    )
    """all applications use these. useless, everyone"""

    arguments: APD = {}
    arguments[Application] = application
    arguments[Customization] = customization

    arguments[InformationConfiguration] = modification
    arguments[InformationHelp] = information
    arguments[InformationVersion] = information

    arguments[Positional] = application
    arguments[Optional] = application

    return arguments


def add_argument(sessions: list[Session], arguments: APD) -> N:
    """"""
    for session in sessions:
        for name, argument in session.items():
            if not argument.argument:
                continue
            parser = arguments[argument]
            args = argument.key(name)
            star = argument.dictionary()
            parser.add_argument(*args, **star)


def add_attribute(
    sessions: list[Session],
    configuration: Configuration,
    args: argparse.Namespace,
) -> N:
    """"""
    save = bool(getattr(args, CONFIGURATION, NONE))
    for session in sessions:
        for option, argument in session.items():
            if not argument.attribute:
                continue
            override = getattr(args, option, NONE)
            section = load.module_to_name(session._application)

            database = configuration.get(section, option)
            value = override or database or argument.fallback
            setattr(session, option, value)
            if save and override:
                configuration.set(section, option, override)


def get_parser(
    argv: L[S],
    exit_on_error: B,
    application: MT,
    language: MT,
    attributes: L[Session],
    fast: B,
    configuration: Configuration,
) -> L[Dictionary]:
    """"""
    parser = make_parser(language, exit_on_error)

    arguments = make_arguments(language, parser)

    add_argument(attributes, arguments)

    parse_known_args = parser.parse_known_args
    parse_args = parser.parse_args
    args = parse_known_args(argv)[0] if fast else parse_args(argv)

    add_attribute(attributes, configuration, args)

    return attributes


def session_loader(name: S, *path: S) -> TY[Session]:
    """"""
    module = load.module(*path)
    session = getattr(module, name)
    return session


def start_session(argv: L[S], exit_on_error: B = True) -> Session:
    """"""
    configuration = Configuration()
    configuration.load()

    def load_the_fish(name, value) -> MT:
        session = session_loader(
            name.capitalize(), "session", "session"
        )
        hippo = [
            session(application, interface, language),
        ]
        parser = get_parser(
            argv,
            exit_on_error,
            application,
            language,
            hippo,
            True,
            configuration,
        )[0]
        thing = getattr(parser, name, value)
        return thing

    try:
        language = load.module(LANGUAGE)
        interface = load.module(INTERFACE)
        application = load.module(APPLICATION)

        language = load_the_fish(LANGUAGE, language)
        interface = load_the_fish(INTERFACE, interface)
        application = load_the_fish(APPLICATION, application)

    except ModuleNotFoundError as error:
        raise RuntimeError("Missing __init__ file.") from error

    session1 = session_loader("Session", "session", "session")

    get_name = load.module_to_name(application)
    if get_name == APPLICATION:
        get_name = INIT
    session2 = session_loader("Session", APPLICATION, get_name)
    session3 = session_loader("Information", "session", "session")

    hippos = [
        session1(application, interface, language),
        session2(application, interface, language),
        session3(application, interface, language),
    ]
    attribute = get_parser(
        argv,
        exit_on_error,
        application,
        language,
        hippos,
        True,
        configuration,
    )

    session = attribute[0]
    session.attribute = attribute[1]

    # hacky addon of new data
    session.call = load.module(APPLICATION, get_name, "call")
    session.view = load.module(APPLICATION, get_name, "view")

    configuration.save()

    return session


"""
importer notes.

language.py is all you need for 1 language.
language/__init__.py can be used instead.

Not recomended to use both. However, note that
language/__init__.py takes priority over language.py

Must have at least one of these.
Recomend using directory version so you can add more languages.
Error messages will assume this version.

if you have more then 1 language you must use language/__init__.py
"""


"""
configuration information will show your saved stuff
"""
