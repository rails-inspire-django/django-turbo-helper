# Standard Library
import enum

# Django
from django.template.loader import render_to_string


class Action(enum.Enum):
    APPEND = "append"
    PREPEND = "prepend"
    REMOVE = "remove"
    REPLACE = "replace"
    UPDATE = "update"


def render_turbo_stream(action, target, content=""):
    return f'<turbo-stream action="{action.value}" target="{target}"><template>{content.strip()}</template></turbo-stream>'


def render_turbo_frame(dom_id, content=""):
    return f'<turbo-frame id="{dom_id}">{content.strip()}</turbo-frame>'


def render_turbo_stream_template(template, context, *, action, target, **kwargs):
    return render_turbo_stream(
        action,
        target,
        render_to_string(
            template,
            {
                **context,
                "turbo_stream_target": target,
                "turbo_stream_action": action,
                "is_turbo_stream": True,
            },
            **kwargs,
        ),
    )


def render_turbo_frame_template(template, context, *, dom_id, **kwargs):
    return render_turbo_frame(
        dom_id,
        render_to_string(
            template,
            {**context, "turbo_frame_dom_id": dom_id, "is_turbo_frame": True},
            **kwargs,
        ),
    )
