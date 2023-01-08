"""Application for translating text to other languages."""


from celestine.window.page import Page

from celestine.session.session import SuperSession
from celestine.session.session import AD

from celestine.unicode import NONE


from .text import KEY
from .text import REGION
from .text import URL

from .report import _train
from .main import _translate


class Session(SuperSession):
    """"""

    @staticmethod
    def dictionary() -> AD:
        """"""
        return {
            KEY: Optional(
                NONE,
                "pick your nose",
            ),
            REGION: Optional(
                NONE,
                "pick your toes",
            ),
            URL: Optional(
                NONE,
                "pick your hoes",
            ),
        }


def main(page: Page):
    """"""
    with page.line("head") as line:
        line.label("title", "fish eat friends for food")
    _translate(page.session)


# TODO:figure out how to make actions not trigger on function load
def _report(page: Page):
    """"""
    with page.line("head") as line:
        line.label("title", "Page main")
    train = _train()
    for (tag, text) in train.items():
        with page.line("body") as line:
            line.label(tag, text)
