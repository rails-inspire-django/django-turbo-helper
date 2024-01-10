from typing import Optional

from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .constants import Action


def render_turbo_stream(
    action: Action,
    target: Optional[str] = None,
    content: str = "",
    is_safe: bool = False,
    is_multiple: bool = False,
) -> str:
    """Wraps content in correct <turbo-stream> tags.

    :param action: action type
    :param target: the DOM ID target of the stream or CSS selector for multiple targetss
    :param content: content to be wrapped. Can be empty.
    :param is_safe: mark content safe for HTML escaping.
    :param is_multiple: multiple targets

    :return: *<turbo-stream>* string
    """

    if is_safe:
        content = mark_safe(content)

    return format_html(
        '<turbo-stream action="{}" {}="{}">' "<template>{}</template></turbo-stream>",
        action.value,
        "targets" if is_multiple else "target",
        target,
        content,
    )


def render_turbo_frame(
    dom_id: str,
    content: str = "",
    is_safe: bool = False,
) -> str:
    """

    Wraps a response in correct *<turbo-frame>* tags.

    :param dom_id: a DOM ID present in the content
    :param content: content of the turbo-frame
    :param is_safe: mark content safe for HTML escaping.

    :return: *<turbo-frame>* string
    """
    if is_safe:
        content = mark_safe(content)

    return format_html('<turbo-frame id="{}">{}</turbo-frame>', dom_id, content)
