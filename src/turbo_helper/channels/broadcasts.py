from actioncable import cable_broadcast
from django.template.loader import render_to_string

from .stream_name import stream_name_from


def broadcast_render_to(*args, **kwargs):
    """
    Rails: Turbo::Streams::Broadcasts#broadcast_render_to

    This function help render HTML to Turbo Stream Channel

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
        *args, content=render_to_string(template_name=template, **kwargs)
    )


def broadcast_stream_to(*args, content):
    stream_name = stream_name_from(*args)
    cable_broadcast(
        group_name=stream_name,
        message=content,
    )
