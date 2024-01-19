from actioncable import cable_broadcast
from django.template.loader import render_to_string

from turbo_helper.renderers import render_turbo_stream_refresh
from turbo_helper.stream import action_proxy

from .stream_name import stream_name_from


def broadcast_render_to(*streamables, **kwargs):
    """
    Rails: Turbo::Streams::Broadcasts#broadcast_render_to

    Help render Django template to Turbo Stream Channel

    for example, in Django template, we subscribe to a Turbo stream Channel

    {% turbo_stream_from 'chat' view.kwargs.chat_pk %}

    Then in Python code

    broadcast_render_to(
        "chat",
        instance.chat_id,
        template="message_append.turbo_stream.html",
        context={
            "instance": instance,
        },
    )
    """
    template = kwargs.pop("template", None)
    broadcast_stream_to(
        *streamables, content=render_to_string(template_name=template, **kwargs)
    )


def broadcast_action_to(*streamables, action, target=None, targets=None, **kwargs):
    """
    For now, we do not support:

    broadcast_remove_to
    broadcast_replace_to
    broadcast_update_to
    ...

    But we can use to do the same work

    For example:

    # remove DOM which has id="new_task"
    broadcast_action_to("tasks", action="remove", target="new_task")
    """
    content = action_proxy(
        action,
        target=target,
        targets=targets,
        **kwargs,
    )
    broadcast_stream_to(*streamables, content=content)


def broadcast_refresh_to(*streamables, request, **kwargs):
    content = render_turbo_stream_refresh(request_id=request.turbo.request_id, **kwargs)
    broadcast_stream_to(*streamables, content=content)


def broadcast_stream_to(*streamables, content):
    stream_name = stream_name_from(*streamables)
    cable_broadcast(
        group_name=stream_name,
        message=content,
    )
