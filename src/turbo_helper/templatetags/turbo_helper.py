import re
from typing import Any, Optional

from django import template
from django.db.models.base import Model
from django.template import Node, TemplateSyntaxError
from django.template.base import token_kwargs

from turbo_helper.renderers import render_turbo_frame, render_turbo_stream_from
from turbo_helper.stream import action_proxy

register = template.Library()


@register.simple_tag
def dom_id(instance: Any, prefix: Optional[str] = "") -> str:
    """
    Generate a unique identifier for a Django model instance, class, or even Python object.

    Args:
        instance (Any): The instance or class for which the identifier is generated.
        prefix (Optional[str]): An optional prefix to prepend to the identifier. Defaults to an empty string.

    Returns:
        str: The generated identifier.

    Raises:
        Exception: If the model instance does not have either the `to_key` or `pk` attribute.

    Note:
        - If `instance` is a Django model instance, the identifier is generated based on the `to_key` or `pk` attribute.
        - If `instance` is a Django model class, the identifier is generated as `new_<class_name>`.
        - If `instance` is neither a model instance nor a model class, the identifier is generated based on the `to_key`
          attribute if available, otherwise it uses the string representation of the instance.
        - The `prefix` argument can be used to prepend a prefix to the generated identifier.
    """
    if not isinstance(instance, type) and isinstance(instance, Model):
        # Django model instance
        if hasattr(instance, "to_key") and getattr(instance, "to_key"):  # noqa: B009
            identifier = f"{instance.__class__.__name__.lower()}_{instance.to_key}"
        elif hasattr(instance, "pk") and getattr(instance, "pk"):  # noqa: B009
            identifier = f"{instance.__class__.__name__.lower()}_{instance.pk}"
        else:
            raise Exception(
                f"Model instance must have either to_key or pk attribute {instance}"
            )
    elif isinstance(instance, type) and issubclass(instance, Model):
        # Django model class
        identifier = f"new_{instance.__name__.lower()}"
    else:
        if hasattr(instance, "to_key") and getattr(instance, "to_key"):  # noqa: B009
            # Developer can still use to_key property to generate the identifier
            identifier = f"{instance.to_key}"
        else:
            # Use the string representation
            identifier = str(instance)

    if prefix:
        identifier = f"{prefix}_{identifier}"

    return identifier


ATTRIBUTE_RE = re.compile(
    r"""
    (?P<attr>
        [@\w:_\.\/-]+
    )
    (?P<sign>
        \+?=
    )
    (?P<value>
    ['"]? # start quote
        [^"']*
    ['"]? # end quote
    )
""",
    re.VERBOSE | re.UNICODE,
)


VALUE_RE = re.compile(
    r"""
    ['"]            # start quote (required)
    (?P<value>
        [^"']*      # match any character except quotes
    )
    ['"]            # end quote (required)
    """,
    re.VERBOSE | re.UNICODE,
)


@register.tag
def class_names(parser, token):
    error_msg = f"{token.split_contents()[0]!r} tag requires " "a list of css classes"
    try:
        bits = token.split_contents()
        tag_name = bits[0]  # noqa
        attr_list = bits[1:]
    except ValueError as exc:
        raise TemplateSyntaxError(error_msg) from exc

    css_ls = []
    css_dict = {}
    for pair in attr_list:
        attribute_match = ATTRIBUTE_RE.match(pair) or VALUE_RE.match(pair)

        if attribute_match:
            dct = attribute_match.groupdict()
            attr = dct.get("attr", None)
            # sign = dct.get("sign", None)
            value = parser.compile_filter(dct["value"])
            if attr:
                css_dict[attr] = value
            else:
                css_ls.append(value)
        else:
            raise TemplateSyntaxError("class_names found supported token: " + f"{pair}")

    return ClassNamesNode(css_ls=css_ls, css_dict=css_dict)


class ClassNamesNode(Node):
    def __init__(self, css_ls, css_dict):
        self.css_ls = css_ls
        self.css_dict = css_dict

    def render(self, context):
        final_css = []

        # for common css classes
        for value in self.css_ls:
            final_css.append(value.token)

        # for conditionals
        for attr, expression in self.css_dict.items():
            real_value = expression.resolve(context)
            if real_value:
                final_css.append(attr)

        return " ".join(final_css)


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

        return render_turbo_frame(
            frame_id=self.frame_id.resolve(context),
            attributes=attributes,
            content=children,
        )


class TurboStreamTagNode(Node):
    def __init__(self, action, target, targets, nodelist, extra_context=None):
        self.action = action
        self.target = target
        self.targets = targets
        self.nodelist = nodelist
        self.extra_context = extra_context or {}

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def render(self, context):
        action = self.action.resolve(context)
        children = self.nodelist.render(context)

        attributes = {
            key: str(value.resolve(context))
            for key, value in self.extra_context.items()
        }

        target = self.target.resolve(context) if self.target else None
        targets = self.targets.resolve(context) if self.targets else None

        return action_proxy(
            action=action,
            target=target,
            targets=targets,
            content=children,
            **attributes,
        )


class TurboStreamFromTagNode(Node):
    def __init__(self, stream_name_array):
        """
        TODO: Support override channel
        """
        self.stream_name_array = stream_name_array

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def render(self, context):
        stream_name_array = [
            stream_name.resolve(context) for stream_name in self.stream_name_array
        ]

        return render_turbo_stream_from(stream_name_array)


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

    return TurboStreamTagNode(
        action,
        target=target,
        targets=None,
        nodelist=nodelist,
        extra_context=extra_context,
    )


@register.tag("turbo_stream_all")
def turbo_stream_all_tag(parser, token):
    args = token.split_contents()

    if len(args) < 3:
        raise TemplateSyntaxError(
            "'turbo_stream_all' tag requires two arguments, first is action, second is the target_id"
        )

    action = parser.compile_filter(args[1])
    targets = parser.compile_filter(args[2])

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
    nodelist = parser.parse(("endturbo_stream_all",))

    # Delete the token that triggered this function from the parser's token stream
    parser.delete_first_token()

    return TurboStreamTagNode(
        action,
        target=None,
        targets=targets,
        nodelist=nodelist,
        extra_context=extra_context,
    )


@register.tag("turbo_stream_from")
def turbo_stream_from_tag(parser, token):
    args = token.split_contents()

    if len(args) < 1:
        raise TemplateSyntaxError(
            "'turbo_stream_from' tag requires at least one arguments"
        )

    remaining_bits = args[1:]
    stream_name_array = [parser.compile_filter(bit) for bit in remaining_bits]

    return TurboStreamFromTagNode(stream_name_array)
