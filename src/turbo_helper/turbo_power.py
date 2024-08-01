"""
https://github.com/marcoroth/turbo_power-rails

Bring turbo_power to Django
"""
import json

from django.utils.safestring import mark_safe

from turbo_helper import register_turbo_stream_action, turbo_stream


def transform_attributes(attributes):
    transformed_attributes = {}
    for key, value in attributes.items():
        transformed_key = transform_key(key)
        transformed_value = transform_value(value)
        transformed_attributes[transformed_key] = transformed_value
    return transformed_attributes


def transform_key(key):
    return str(key).replace("_", "-")


def transform_value(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, (int, float, bool)):
        return str(value).lower()
    elif value is None:
        return None
    else:
        return json.dumps(value)


################################################################################


def custom_action(action, target=None, content=None, **kwargs):
    return turbo_stream.action(
        action, target=target, content=content, **transform_attributes(kwargs)
    )


def custom_action_all(action, targets=None, content=None, **kwargs):
    return turbo_stream.action_all(
        action, targets=targets, content=content, **transform_attributes(kwargs)
    )


################################################################################

"""
When defining custom action, `target` or `targets` are both supported

def example_action(targets=None, **attributes):
    pass

This action by default will use `targets` as the target selector

turbo_stream.example_action("A")
Generate: <turbo-stream targets="A"

if you want to use `target` as the target selector, should explicitly pass the target

turbo_stream.example_action(target="A")
Generate: <turbo-stream target="A"
"""

# DOM Actions


@register_turbo_stream_action("graft")
def graft(targets=None, parent=None, **attributes):
    return custom_action_all(
        "graft",
        targets=targets,
        parent=parent,
        **attributes,
    )


# Attribute Actions


@register_turbo_stream_action("add_css_class")
def add_css_class(targets=None, classes="", **attributes):
    classes = attributes.get("classes", classes)
    if isinstance(classes, list):
        classes = " ".join(classes)

    return custom_action_all(
        "add_css_class",
        targets=targets,
        classes=classes,
        **attributes,
    )


# Event Actions


@register_turbo_stream_action("dispatch_event")
def dispatch_event(targets=None, name=None, detail=None, **attributes):
    detail = detail or {}
    return custom_action_all(
        "dispatch_event",
        targets=targets,
        name=name,
        content=mark_safe(json.dumps(detail, separators=(",", ":"))),
        **attributes,
    )


# Notification Actions


@register_turbo_stream_action("notification")
def notification(title=None, **attributes):
    return custom_action(
        "notification",
        title=title,
        **attributes,
    )


# Turbo Actions


@register_turbo_stream_action("redirect_to")
def redirect_to(url=None, turbo_action="advance", turbo_frame=None, **attributes):
    return custom_action(
        "redirect_to",
        url=url,
        turbo_action=turbo_action,
        turbo_frame=turbo_frame,
        **attributes,
    )


# Turbo Frame Actions


@register_turbo_stream_action("turbo_frame_reload")
def turbo_frame_reload(target=None, **attributes):
    return custom_action(
        "turbo_frame_reload",
        target=target,
        **attributes,
    )


@register_turbo_stream_action("turbo_frame_set_src")
def turbo_frame_set_src(target=None, src=None, **attributes):
    return custom_action(
        "turbo_frame_set_src",
        target=target,
        src=src,
        **attributes,
    )
