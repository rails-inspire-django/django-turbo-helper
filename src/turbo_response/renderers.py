# Local
# Django
from django.template import Context, Template

from .constants import Action


def render_turbo_stream(action: Action, target: str, content: str = "") -> str:
    """Wraps content in correct <turbo-stream> tags.

    :param action: action type
    :param target: the DOM ID target of the stream
    :param content: content to be wrapped. Can be empty.

    :return: *<turbo-stream>* string
    """
    return Template(
        '<turbo-stream action="{{ action }}" target="{{ target }}"><template>{{ content }}</template></turbo-stream>'
    ).render(Context({"action": action.value, "target": target, "content": content}))


def render_turbo_frame(dom_id: str, content: str = "") -> str:
    """

    Wraps a response in correct *<turbo-frame>* tags.

    :param dom_id: a DOM ID present in the content
    :param content: content of the turbo-frame

    :return: *<turbo-frame>* string
    """
    return Template(
        '<turbo-frame id="{{ dom_id }}">{{ content }}</turbo-frame>'
    ).render(Context({"dom_id": dom_id, "content": content}))
