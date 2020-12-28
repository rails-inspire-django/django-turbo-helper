# Django
from django.core.exceptions import ImproperlyConfigured

# Local
from .response import (
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)


class TurboStreamResponseMixin:
    turbo_stream_action = None
    turbo_stream_target = None

    def get_turbo_stream_action(self):
        return self.turbo_stream_action

    def get_turbo_stream_target(self):
        return self.turbo_stream_target

    def get_response_content():
        return ""

    def render_turbo_stream_response(self, **context):

        target = self.get_turbo_stream_target()
        action = self.get_turbo_stream_action()

        if target is None:
            raise ImproperlyConfigured("turbo_stream_target must be set")

        if action is None:
            raise ImproperlyConfigured("turbo_stream_action must be set")

        return TurboStreamResponse(
            self.get_response_content(), target=target, action=action,
        )


class TurboStreamTemplateResponseMixin(TurboStreamResponseMixin):
    """Use with ContextMixin subclass"""

    turbo_stream_template = None

    def get_turbo_stream_template(self):
        return self.turbo_stream_template

    def render_turbo_stream_response(self, **context):

        template = self.get_turbo_stream_template()
        target = self.get_turbo_stream_target()
        action = self.get_turbo_stream_action()

        if template is None:
            raise ImproperlyConfigured("turbo_stream_template must be set")

        if target is None:
            raise ImproperlyConfigured("turbo_stream_target must be set")

        if action is None:
            raise ImproperlyConfigured("turbo_stream_action must be set")

        return TurboStreamTemplateResponse(
            request=self.request,
            template=template,
            target=target,
            action=action,
            context=self.get_context_data(context),
            using=self.template_engine,
        )


class TurboStreamFormMixin(TurboStreamTemplateResponseMixin):
    """Use with FormView"""

    def form_invalid(self, form):
        return self.render_turbo_stream_response(form=form)


class TurboFrameResponseMixin:
    turbo_frame_dom_id = None

    def get_turbo_frame_dom_id(self):
        return self.turbo_frame_dom_id

    def get_response_content():
        return ""

    def render_turbo_frame_response(self, **context):
        dom_id = self.get_turbo_frame_dom_id()

        if dom_id is None:
            raise ImproperlyConfigured("turbo_frame_dom_id must be set")

        return TurboFrameResponse(self.get_response_content(), dom_id=dom_id,)


class TurboFrameTemplateResponseMixin(TurboFrameResponseMixin):
    """Use with ContextMixin subclass"""

    turbo_frame_template = None

    def get_turbo_frame_template(self):
        return self.turbo_frame_template

    def render_turbo_frame_response(self, **context):

        template = self.get_turbo_frame_template()
        dom_id = self.get_turbo_frame_dom_id()

        if template is None:
            raise ImproperlyConfigured("turbo_frame_template must be set")

        if dom_id is None:
            raise ImproperlyConfigured("turbo_frame_dom_id must be set")

        return TurboFrameTemplateResponse(
            request=self.request,
            template=template,
            dom_id=dom_id,
            context=self.get_context_data(context),
            using=self.template_engine,
        )
