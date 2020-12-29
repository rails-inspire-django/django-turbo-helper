# Standard Library
import enum

# Django
from django.template.loader import render_to_string


class Action(enum.Enum):
    """Turbo-Stream action parameter"""

    APPEND = "append"
    PREPEND = "prepend"
    REMOVE = "remove"
    REPLACE = "replace"
    UPDATE = "update"


def render_turbo_stream(action, target, content=""):
    """Wraps content in correct <turbo-stream> tags.

    :param action: action type
    :param target: the DOM ID target of the stream
    :param content: content to be wrapped. Can be empty.

    :type action: turbo_response.Action
    :type target: str
    :type content: str

    :return: *<turbo-stream>* string
    :rtype: str

    """
    return f'<turbo-stream action="{action.value}" target="{target}"><template>{content.strip()}</template></turbo-stream>'


def render_turbo_frame(dom_id, content=""):
    """Wraps a response in correct *<turbo-frame>* tags.


    :param dom_id: a DOM ID present in the content
    :param content: content of the turbo-frame
    :type dom_id: str
    :type content: str

    :rtype: str
    """
    return f'<turbo-frame id="{dom_id}">{content.strip()}</turbo-frame>'


def render_turbo_stream_template(
    template, context, *, action, target, **template_kwargs
):
    """Renders a *<turbo-stream>* template.

    :param template: template name or names
    :param context: template context
    :param action: turbo-stream action
    :param target: turbo-stream target
    :type template: list or str
    :type context: dict
    :type action: turbo_response.Action
    :type target: str

    :rtype: str
    """
    return render_turbo_stream(
        action,
        target,
        render_to_string(
            template,
            {
                **context,
                "turbo_stream_target": target,
                "turbo_stream_action": action.value,
                "is_turbo_stream": True,
            },
            **template_kwargs,
        ),
    )


def render_turbo_frame_template(template, context, *, dom_id, **kwargs):
    """Renders a *<turbo-frame>* template.

    :param template: template name or names
    :param context: template context
    :param dom: turbo-frame DOM ID
    :type template: list or str
    :type context: dict
    :type dom_id: str

    :rtype: str
    """

    return render_turbo_frame(
        dom_id,
        render_to_string(
            template,
            {**context, "turbo_frame_dom_id": dom_id, "is_turbo_frame": True},
            **kwargs,
        ),
    )
