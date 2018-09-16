# coding: utf-8
from bernard import (
    layers as lyr,
)
from bernard.analytics import (
    page_view,
)
from bernard.engine import (
    BaseState,
)
from bernard.i18n import (
    intents as its,
    translate as t,
)
from bernard.layers import stack
from bernard.platforms.telegram import layers as tgr

from .store import (
    cs,
)

class {{cookiecutter.project_class}}(BaseState):
    """
    Root class for Bot
    """

    async def error(self) -> None:
        """
        This happens when something goes wrong (it's the equivalent of the
        HTTP error 500).
        """

        self.send(lyr.Text(t.ERROR))

    async def confused(self) -> None:
        """
        This is called when the user sends a message that triggers no
        transitions.
        """

        self.send(lyr.Text(t.CONFUSED))

    async def handle(self) -> None:
        raise NotImplementedError

{% for class_name, value in cookiecutter.states|dictsort %}
class {{class_name}}({{cookiecutter.project_class}}):

    async def handle(self) -> None:
        self.send(
            lyr.Text(t.{{value.text}}),
            {% if 'inline_keyboards' in value -%}
            tgr.InlineKeyboard([
                {% for line in value.inline_keyboards -%}
                [
                {% for kb in line -%}
                    tgr.InlineKeyboardCallbackButton(
                        text=t.{{kb['text']}},
                        payload={'action': "{{kb['action']}}"}
                    ),
                {% endfor -%}
                ],
                {% endfor -%}
            ], resize_keyboard=True),
            {% endif -%}
            {% if value.reply_keyboards -%}
            tgr.ReplyKeyboard([
                {% for line in value.reply_keyboards -%}
                [
                {% for kb in line -%}
                    tgr.KeyboardButton(
                        text=t.{{kb}}
                    ),
                {% endfor -%}
                ],
                {% endfor -%}
            ], resize_keyboard=True),
            {% endif -%}
        )
{% endfor %}