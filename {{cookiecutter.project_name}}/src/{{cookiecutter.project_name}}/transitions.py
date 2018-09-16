# coding: utf-8

from bernard.engine import (
    Tr,
    triggers as trg,
)
from bernard.i18n import (
    intents as its,
)

from .states import *
from .triggers import *

transitions = [
    (
        dest={{(cookiecutter.states|dictsort)[0][0]}}
        factory=triggers.Equal.builder(tgr.BotCommand('/start')),
    ),
    {% for class_name, value in cookiecutter.states|dictsort -%}
    {% for class_name_dest, dest in value['dest'].items() -%}
    Tr(
        origin={{class_name}},
        dest={{class_name_dest}},
        {% if dest.type == 'nlu' -%}
        factory=triggers.Text.builder(intents.{{dest.value}}),
        {% endif -%}
        {% if dest.type == 'button' -%}
        factory=triggers.Action.builder('{{dest.value}}'),
        {% endif -%}
    )
    {% endfor -%}
    {% endfor -%}
]
