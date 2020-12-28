# Django
from django.template.loader import render_to_string


def render_turbo_stream(action, target, content=""):
    return f'<turbo-stream target="{target}" action="{action}"><template>{content}</template></turbo-stream>'


def render_turbo_frame(dom_id, content):
    return f'<turbo-frame id="{dom_id}">{content}</turbo-frame>'


def render_turbo_stream_template_to_string(template, context, action, target, **kwargs):
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


def render_turbo_frame_template_to_string(template, context, dom_id, **kwargs):
    return render_turbo_frame(
        dom_id,
        render_to_string(
            template,
            context | {"turbo_frame_dom_id": dom_id, "is_turbo_frame": True},
            **kwargs,
        ),
    )
