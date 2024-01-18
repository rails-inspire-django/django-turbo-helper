from typing import Tuple

from actioncable import cable_broadcast
from django.core import signing
from django.core.signing import Signer
from django.template.loader import render_to_string

from .templatetags.turbo_helper import dom_id

signer = Signer()


def stream_name_from(*streamables) -> str:
    """
    Generate stream_name from a list of objects or a single object.
    """
    if len(streamables) == 1:
        return dom_id(streamables[0])
    else:
        return "_".join(stream_name_from(streamable) for streamable in streamables)


def generate_signed_stream_key(stream_name: str) -> str:
    """
    Generate signed stream key from stream_name
    """
    return signer.sign(stream_name)


def verify_signed_stream_key(signed_stream_key: str) -> Tuple[bool, str]:
    """
    Verify signed stream key
    """
    try:
        unsigned_data = signer.unsign(signed_stream_key)
        return True, unsigned_data

    except signing.BadSignature:
        pass

    return False, ""


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
