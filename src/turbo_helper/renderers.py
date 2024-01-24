from typing import Any, Dict, List, Optional

from django.template import engines
from django.utils.html import escape
from django.utils.safestring import mark_safe


def render_turbo_stream(
    action: str,
    content: Optional[str],
    attributes: Dict[str, Any],
    target: Optional[str] = None,
    targets: Optional[str] = None,
) -> str:
    element_attributes = {}
    for key, value in attributes.items():
        # convert data_xxx to data-xxx
        if key.startswith("data"):
            element_attributes[key.replace("_", "-")] = value
        else:
            element_attributes[key] = value

    element_attributes_array = []
    for key, value in element_attributes.items():
        if value is None:
            continue
        # TODO: bool type django/forms/widgets/attrs.html
        element_attributes_array.append(f'{key}="{escape(value)}"')

    attribute_string = mark_safe(" ".join(element_attributes_array))

    django_engine = engines["django"]
    template_string = """<turbo-stream action="{{ action }}"{% if target %} target="{{ target }}"{% elif targets %} targets="{{ targets }}"{% endif %}{% if attribute_string %} {{ attribute_string }}{% endif %}><template>{{ content|default:'' }}</template></turbo-stream>"""
    context = {
        "content": content,
        "action": action,
        "target": target,
        "targets": targets,
        "attribute_string": attribute_string,
    }
    return django_engine.from_string(template_string).render(context)


def render_turbo_frame(frame_id: str, content: str, attributes: Dict[str, Any]) -> str:
    # convert data_xxx to data-xxx
    element_attributes = {}
    for key, value in attributes.items():
        # convert data_xxx to data-xxx
        if key.startswith("data"):
            element_attributes[key.replace("_", "-")] = value
        else:
            element_attributes[key] = value

    element_attributes_array = []
    for key, value in element_attributes.items():
        if value is None:
            continue
        # TODO: bool type django/forms/widgets/attrs.html
        element_attributes_array.append(f'{key}="{escape(value)}"')

    attribute_string = mark_safe(" ".join(element_attributes_array))

    django_engine = engines["django"]
    template_string = """<turbo-frame id="{{ frame_id }}"{% if attribute_string %} {{ attribute_string }}{% endif %}>{{ content }}</turbo-frame>"""  # noqa
    context = {
        "frame_id": frame_id,
        "content": content,
        "attribute_string": attribute_string,
    }
    return django_engine.from_string(template_string).render(context)


def render_turbo_stream_from(stream_name_array: List[Any]):
    from turbo_helper.channels.stream_name import (
        generate_signed_stream_key,
        stream_name_from,
    )
    from turbo_helper.channels.streams_channel import TurboStreamCableChannel

    stream_name_string = stream_name_from(*stream_name_array)

    django_engine = engines["django"]
    template_string = """<turbo-cable-stream-source channel="{{ channel }}" signed-stream-name="{{ signed_stream_name }}"></turbo-cable-stream-source>"""  # noqa
    context = {
        "signed_stream_name": generate_signed_stream_key(stream_name_string),
        "channel": TurboStreamCableChannel.__name__,
    }
    return django_engine.from_string(template_string).render(context)


def render_turbo_stream_refresh(request_id, **attributes):
    attributes["request-id"] = request_id
    return render_turbo_stream(
        action="refresh",
        content=None,
        target=None,
        targets=None,
        attributes=attributes,
    )
