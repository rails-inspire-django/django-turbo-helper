# Standard Library
from functools import lru_cache

# Django
from django.template import Context, Template
from django.template.engine import Engine
from django.utils.safestring import mark_safe

# Local
from .constants import Action


def render_turbo_stream(
    action: Action, target: str, content: str = "", is_safe: bool = False
) -> str:
    """Wraps content in correct <turbo-stream> tags.

    :param action: action type
    :param target: the DOM ID target of the stream
    :param content: content to be wrapped. Can be empty.
    :param is_safe: mark content safe for HTML escaping.

    :return: *<turbo-stream>* string
    """
    if is_safe:
        content = mark_safe(content)

    return get_turbo_stream_template().render(
        Context({"action": action.value, "target": target, "content": content})
    )


def render_turbo_frame(dom_id: str, content: str = "", is_safe: bool = False) -> str:
    """

    Wraps a response in correct *<turbo-frame>* tags.

    :param dom_id: a DOM ID present in the content
    :param content: content of the turbo-frame
    :param is_safe: mark content safe for HTML escaping.

    :return: *<turbo-frame>* string
    """
    if is_safe:
        content = mark_safe(content)

    return get_turbo_frame_template().render(
        Context({"dom_id": dom_id, "content": content})
    )


@lru_cache()
def get_turbo_stream_template() -> Template:
    return Engine.get_default().from_string(
        '<turbo-stream action="{{ action }}" target="{{ target }}"><template>{{ content }}</template></turbo-stream>',
    )


@lru_cache()
def get_turbo_frame_template() -> Template:
    return Engine.get_default().from_string(
        '<turbo-frame id="{{ dom_id }}">{{ content }}</turbo-frame>'
    )
