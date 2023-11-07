from typing import Any, Optional

from django import template
from django.db.models.base import Model
from django.template import Node, TemplateSyntaxError, engines
from django.template.base import token_kwargs
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def dom_id(instance: Any, prefix: Optional[str] = "") -> str:
    if not isinstance(instance, type) and isinstance(instance, Model):
        # instance
        identifier = f"{instance.__class__.__name__.lower()}_{instance.id}"
    elif isinstance(instance, type) and issubclass(instance, Model):
        # model class
        identifier = f"new_{instance.__name__.lower()}"
    else:
        identifier = str(instance)

    if prefix:
        identifier = f"{prefix}_{identifier}"

    return identifier


class TurboFrameTagNode(Node):
    def __init__(self, frame_id, nodelist, extra_context=None):
        self.frame_id = frame_id
        self.nodelist = nodelist
        self.extra_context = extra_context or {}

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def render(self, context):
        children = self.nodelist.render(context)

        attributes = {
            key: str(value.resolve(context))
            for key, value in self.extra_context.items()
        }
        element_attributes = {}
        for key, value in attributes.items():
            # convert data_xxx to data-xxx
            if key.startswith("data"):
                element_attributes[key.replace("_", "-")] = value
            else:
                element_attributes[key] = value

        element_attributes_array = []
        for key, value in element_attributes.items():
            element_attributes_array.append(f'{key}="{value}"')

        attribute_string = mark_safe(" ".join(element_attributes_array))

        django_engine = engines["django"]
        template_string = """<turbo-frame id="{{ frame_id }}"{% if attribute_string %} {{ attribute_string }}{% endif %}>{{ children }}</turbo-frame>"""
        context = {
            "children": children,
            "frame_id": self.frame_id.resolve(context),
            "attribute_string": attribute_string,
        }
        return django_engine.from_string(template_string).render(context)


class TurboStreamTagNode(Node):
    def __init__(self, action, target, nodelist, extra_context=None):
        self.action = action
        self.target = target
        self.nodelist = nodelist
        self.extra_context = extra_context or {}

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def render(self, context):
        children = self.nodelist.render(context)

        attributes = {
            key: str(value.resolve(context))
            for key, value in self.extra_context.items()
        }
        element_attributes = {}
        for key, value in attributes.items():
            # convert data_xxx to data-xxx
            if key.startswith("data"):
                element_attributes[key.replace("_", "-")] = value
            else:
                element_attributes[key] = value

        element_attributes_array = []
        for key, value in element_attributes.items():
            element_attributes_array.append(f'{key}="{value}"')

        attribute_string = mark_safe(" ".join(element_attributes_array))

        django_engine = engines["django"]
        template_string = """<turbo-stream action="{{ action }}" target="{{ target }}"{% if attribute_string %} {{ attribute_string }}{% endif %}><template>{{ children }}</template></turbo-stream>"""
        context = {
            "children": children,
            "action": self.action.resolve(context),
            "target": self.target.resolve(context),
            "attribute_string": attribute_string,
        }
        return django_engine.from_string(template_string).render(context)


@register.tag("turbo_frame")
def turbo_frame_tag(parser, token):
    args = token.split_contents()

    if len(args) < 2:
        raise TemplateSyntaxError(
            "'turbo_frame' tag requires at least one argument to set the id"
        )

    frame_id = parser.compile_filter(args[1])

    # Get all elements of the list except the first one
    remaining_bits = args[2:]

    # Parse the remaining bits as keyword arguments
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)

    # If there are still remaining bits after parsing the keyword arguments,
    # raise an exception indicating that an invalid token was received
    if remaining_bits:
        raise TemplateSyntaxError(
            "%r received an invalid token: %r" % (args[0], remaining_bits[0])
        )

    # Parse the content between the start and end tags
    nodelist = parser.parse(("endturbo_frame",))

    # Delete the token that triggered this function from the parser's token stream
    parser.delete_first_token()

    return TurboFrameTagNode(frame_id, nodelist, extra_context=extra_context)


@register.tag("turbo_stream")
def turbo_stream_tag(parser, token):
    args = token.split_contents()

    if len(args) < 3:
        raise TemplateSyntaxError(
            "'turbo_stream' tag requires two arguments, first is action, second is the target_id"
        )

    action = parser.compile_filter(args[1])
    target = parser.compile_filter(args[2])

    # Get all elements of the list except the first one
    remaining_bits = args[3:]

    # Parse the remaining bits as keyword arguments
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)

    # If there are still remaining bits after parsing the keyword arguments,
    # raise an exception indicating that an invalid token was received
    if remaining_bits:
        raise TemplateSyntaxError(
            "%r received an invalid token: %r" % (args[0], remaining_bits[0])
        )

    # Parse the content between the start and end tags
    nodelist = parser.parse(("endturbo_stream",))

    # Delete the token that triggered this function from the parser's token stream
    parser.delete_first_token()

    return TurboStreamTagNode(action, target, nodelist, extra_context=extra_context)
