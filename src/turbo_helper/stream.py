from django.template.loader import render_to_string

from turbo_helper.renderers import render_turbo_stream
from turbo_helper.response import TurboStreamResponse


class TurboStream:
    """
    https://github.com/hotwired/turbo-rails/blob/066396c67d4cee740c0348089955d7e8cdaa2cb0/app/models/turbo/streams/tag_builder.rb
    """

    def __init__(self):
        self.registered_actions = []

    def is_registered(self, name):
        return name in self.registered_actions

    def render_action(self, action, target, content=None, **kwargs):
        if not content and kwargs.get("template", None):
            # render template content
            template = kwargs.pop("template")
            context = kwargs.pop("context", {})
            request = kwargs.pop("request", None)

            content = render_to_string(template, context=context, request=request)

        return render_turbo_stream(
            action=action, content=content, target=target, attributes=kwargs
        )

    def render_action_all(self, action, targets, content=None, **kwargs):
        if not content and kwargs.get("template", None):
            # render template content
            template = kwargs.pop("template")
            context = kwargs.pop("context", {})
            request = kwargs.pop("request", None)

            content = render_to_string(template, context=context, request=request)

        return render_turbo_stream(
            action=action, content=content, targets=targets, attributes=kwargs
        )

    def response(self, *args, **kwargs):
        """
        Shortcut for TurboStreamResponse
        """
        return TurboStreamResponse(*args, **kwargs)


turbo_stream = TurboStream()


def register_turbo_stream_action(name):
    def decorator(func):
        if hasattr(turbo_stream, name):
            raise AttributeError(
                f"TurboStream action '{name}' already exists in turbo_stream"
            )
        setattr(turbo_stream, name, func)
        turbo_stream.registered_actions.append(name)
        return func

    return decorator


################################################################################


@register_turbo_stream_action("append")
def append(target, content=None, **kwargs):
    return turbo_stream.render_action("append", target, content, **kwargs)


@register_turbo_stream_action("after")
def after(target, content=None, **kwargs):
    return turbo_stream.render_action("after", target, content, **kwargs)


@register_turbo_stream_action("before")
def before(target, content=None, **kwargs):
    return turbo_stream.render_action("before", target, content, **kwargs)


@register_turbo_stream_action("prepend")
def prepend(target, content=None, **kwargs):
    return turbo_stream.render_action("prepend", target, content, **kwargs)


@register_turbo_stream_action("remove")
def remove(target, **kwargs):
    return turbo_stream.render_action("remove", target, **kwargs)


@register_turbo_stream_action("replace")
def replace(target, content=None, **kwargs):
    return turbo_stream.render_action("replace", target, content, **kwargs)


@register_turbo_stream_action("update")
def update(target, content=None, **kwargs):
    return turbo_stream.render_action("update", target, content, **kwargs)


################################################################################


@register_turbo_stream_action("append_all")
def append_all(targets, content=None, **kwargs):
    return turbo_stream.render_action_all("append", targets, content, **kwargs)


@register_turbo_stream_action("after_all")
def after_all(targets, content=None, **kwargs):
    return turbo_stream.render_action_all("after", targets, content, **kwargs)


@register_turbo_stream_action("before_all")
def before_all(targets, content=None, **kwargs):
    return turbo_stream.render_action_all("before", targets, content, **kwargs)


@register_turbo_stream_action("prepend_all")
def prepend_all(targets, content=None, **kwargs):
    return turbo_stream.render_action_all("prepend", targets, content, **kwargs)


@register_turbo_stream_action("remove_all")
def remove_all(targets, **kwargs):
    return turbo_stream.render_action_all("remove", targets, **kwargs)


@register_turbo_stream_action("replace_all")
def replace_all(targets, content=None, **kwargs):
    return turbo_stream.render_action_all("replace", targets, content, **kwargs)


@register_turbo_stream_action("update_all")
def update_all(targets, content=None, **kwargs):
    return turbo_stream.render_action_all("update", targets, content, **kwargs)
