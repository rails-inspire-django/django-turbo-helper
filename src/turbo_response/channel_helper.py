from typing import List, Tuple, Union

from django.core import signing
from django.core.signing import Signer
from django.template.loader import render_to_string

from .templatetags.turbo_helper import dom_id

try:
    from actioncable import cable_broadcast
except ImportError as err:
    raise Exception("Please make sure django-channels is installed") from err


signer = Signer()


def stream_name_from(streamables: Union[List, object]) -> str:
    """
    Generate stream_name from a list of objects or a single object.
    """
    if isinstance(streamables, list):
        return "_".join(stream_name_from(streamable) for streamable in streamables)
    else:
        return dom_id(streamables)


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


def broadcast_render_to(streamables: Union[List, object], template: str, context=None):
    """
    This function help render HTML to Turbo Stream Channel

    for example, in Django template, we subscribe to a Turbo stream Channel

    {% turbo_stream_from 'chat' view.kwargs.chat_pk %}

    Then in Python code

    broadcast_render_to(
        ["chat", instance.chat_id],
        template="message_append.turbo_stream.html",
        context={
            "instance": instance,
        },
    )
    """
    if context is None:
        context = {}

    html = render_to_string(template, context=context)
    stream_name = stream_name_from(streamables)
    cable_broadcast(
        stream_name,
        {
            "message": html,
        },
    )
