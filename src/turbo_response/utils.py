# Django
from django.template.loader import render_to_string

# Local
from .exceptions import InvalidTurboFrame, InvalidTurboStream

STREAM_ACTIONS = ("append", "prepend", "replace", "update", "remove")


def validate_turbo_frame(dom_id):
    if not dom_id:
        raise InvalidTurboFrame("DOM ID must be provided")


def validate_turbo_stream(action, target):
    if not action:
        raise InvalidTurboStream("action must be provided")

    if action not in STREAM_ACTIONS:
        raise InvalidTurboStream(f"action must be one of {', '.join(STREAM_ACTIONS)}")

    if not target:
        raise InvalidTurboStream("target to DOM ID must be provided")


def render_turbo_stream(action, target, content=""):
    validate_turbo_stream(action, target)
    return f'<turbo-stream target="{target}" action="{action}"><template>{content}</template></turbo-stream>'


def render_turbo_frame(dom_id, content):
    validate_turbo_frame(dom_id)
    return f'<turbo-frame id="{dom_id}">{content}</turbo-frame>'


def render_turbo_stream_template(template, context, *, action, target, **kwargs):
    return render_turbo_stream(
        action,
        target,
        render_to_string(
            template,
            context
            | {
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
            context | {"turbo_frame_dom_id": dom_id, "is_turbo_frame": True},
            **kwargs,
        ),
    )
