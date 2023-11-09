import json
from typing import List, Tuple, Union

from django.core import signing
from django.core.signing import Signer
from django.template.loader import render_to_string

from .templatetags.turbo_helper import dom_id

try:
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
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


def generate_channel_group_name(channel: str, stream_name: str):
    """
    Generate Django Channel group name from channel and stream_name
    """
    return f"{channel}_{stream_name}"


def broadcast_render_to(streamables: Union[List, object], template: str, context=None):
    if context is None:
        context = {}

    html = render_to_string(template, context=context)

    stream_name = stream_name_from(streamables)
    channel_group_name = generate_channel_group_name("TurboStreamsChannel", stream_name)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        channel_group_name,
        {
            "type": "turbo_stream_message",
            "data": {
                "identifier": json.dumps(
                    {
                        "channel": "TurboStreamsChannel",
                        "signed_stream_name": generate_signed_stream_key(stream_name),
                    },
                    separators=(",", ":"),
                ),
                "message": html,
            },
        },
    )
