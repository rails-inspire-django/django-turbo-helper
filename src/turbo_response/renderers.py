# Local
from .constants import Action


def render_turbo_stream(action: Action, target: str, content: str = "") -> str:
    """Wraps content in correct <turbo-stream> tags.

    :param action: action type
    :param target: the DOM ID target of the stream
    :param content: content to be wrapped. Can be empty.

    :return: *<turbo-stream>* string
    """
    return f'<turbo-stream action="{action.value}" target="{target}"><template>{content.strip()}</template></turbo-stream>'


def render_turbo_frame(dom_id: str, content: str = "") -> str:
    """

    Wraps a response in correct *<turbo-frame>* tags.

    :param dom_id: a DOM ID present in the content
    :param content: content of the turbo-frame

    :return: *<turbo-frame>* string
    """
    return f'<turbo-frame id="{dom_id}">{content.strip()}</turbo-frame>'
