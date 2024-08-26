from django import template
from django.template import Node, TemplateSyntaxError
from django.template.base import token_kwargs
from template_simplify.templatetags.template_simplify import class_names, dom_id

from turbo_helper.renderers import render_turbo_frame, render_turbo_stream_from
from turbo_helper.stream import action_proxy

register = template.Library()

register.simple_tag(dom_id, name="dom_id")
register.tag(class_names)


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
