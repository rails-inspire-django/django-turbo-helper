# Standard Library
from typing import Any, Dict

# Django
from django.template.loader import render_to_string

# Local
from .constants import Action
from .renderers import render_turbo_frame, render_turbo_stream


def render_turbo_stream_template(
    template: str,
    context: Dict[str, Any],
    *,
    action: Action,
    target: str,
    **template_kwargs
) -> str:
    """Renders a *<turbo-stream>* template.

    :param template: template name or names
    :param context: template context
    :param action: turbo-stream action
    :param target: turbo-stream target
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


def render_turbo_frame_template(
    template: str, context: Dict[str, Any], *, dom_id: str, **kwargs
) -> str:
    """Renders a *<turbo-frame>* template.

    :param template: template name or names
    :param context: template context
    :param dom_id: turbo-frame DOM ID
    """

    return render_turbo_frame(
        dom_id,
        render_to_string(
            template,
            {**context, "turbo_frame_dom_id": dom_id, "is_turbo_frame": True},
            **kwargs,
        ),
    )
