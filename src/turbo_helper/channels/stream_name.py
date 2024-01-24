from typing import Tuple

from django.core import signing
from django.core.signing import Signer

from turbo_helper.templatetags.turbo_helper import dom_id

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
