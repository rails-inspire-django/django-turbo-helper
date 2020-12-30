# Local
from .renderers import Action, render_turbo_frame, render_turbo_stream
from .response import (
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)
from .template import render_turbo_frame_template, render_turbo_stream_template


class TurboStream:
    def __init__(self, target):
        self.target = target

    @property
    def append(self):
        return TurboStreamAction(self.target, Action.APPEND)

    @property
    def prepend(self):
        return TurboStreamAction(self.target, Action.PREPEND)

    @property
    def remove(self):
        return TurboStreamAction(self.target, Action.REMOVE)

    @property
    def replace(self):
        return TurboStreamAction(self.target, Action.REPLACE)

    @property
    def update(self):
        return TurboStreamAction(self.target, Action.UPDATE)


class TurboStreamAction:
    def __init__(self, target, action):
        self.action = action
        self.target = target

    def __str__(self):
        return self.render()

    def render(self, content=""):
        return render_turbo_stream(
            action=self.action, target=self.target, content=content
        )

    def response(self, content="", **response_kwargs):
        return TurboStreamResponse(
            action=self.action, target=self.target, content=content, **response_kwargs
        )

    def template(self, template_name, context=None, **template_kwargs):
        return TurboStreamTemplateProxy(
            template_name,
            context,
            action=self.action,
            target=self.target,
            **template_kwargs
        )


class TurboStreamTemplateProxy:
    def __init__(self, template_name, context, *, action, target, **template_kwargs):
        self.action = action
        self.target = target
        self.template_name = template_name
        self.context = context
        self.template_kwargs = template_kwargs

    def __str__(self):
        return self.render()

    def render(self):
        return render_turbo_stream_template(
            self.template_name,
            self.context,
            action=self.action,
            target=self.target,
            **self.template_kwargs
        )

    def response(self, request, **kwargs):
        return TurboStreamTemplateResponse(
            request,
            self.template_name,
            self.context,
            action=self.action,
            target=self.target,
            **{**self.template_kwargs, **kwargs}
        )


class TurboFrame:
    def __init__(self, dom_id):
        self.dom_id = dom_id

    def __str__(self):
        return self.render()

    def render(self, content=""):
        return render_turbo_frame(dom_id=self.dom_id, content=content)

    def response(self, content="", **response_kwargs):
        return TurboFrameResponse(
            dom_id=self.dom_id, content=content, **response_kwargs
        )

    def template(self, template_name, context=None, **template_kwargs):
        return TurboFrameTemplateProxy(
            template_name, context, dom_id=self.dom_id, **template_kwargs
        )


class TurboFrameTemplateProxy:
    def __init__(self, template_name, context, *, dom_id, **template_kwargs):
        self.template_name = template_name
        self.context = context
        self.template_kwargs = template_kwargs
        self.dom_id = dom_id

    def __str__(self):
        return self.render()

    def render(self):
        return render_turbo_frame_template(
            self.template_name, self.context, dom_id=self.dom_id, **self.template_kwargs
        )

    def response(self, request, **kwargs):
        return TurboFrameTemplateResponse(
            request,
            self.template_name,
            self.context,
            dom_id=self.dom_id,
            **{**self.template_kwargs, **kwargs}
        )
