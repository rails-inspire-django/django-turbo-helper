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

    def get_response_content(self):
        return ""

    def render_turbo_stream_response(self):

        return TurboStreamResponse(
            action=self.get_turbo_stream_action(),
            target=self.get_turbo_stream_target(),
            content=self.get_response_content(),
        )


class TurboStreamTemplateResponseMixin(TurboStreamResponseMixin):
    """Use with ContextMixin subclass"""

    def get_turbo_stream_template_names(self):
        return self.get_template_names()

    def render_turbo_stream_response(self, context, **response_kwargs):
        return TurboStreamTemplateResponse(
            request=self.request,
            template=self.get_turbo_stream_template_names(),
            target=self.get_turbo_stream_target(),
            action=self.get_turbo_stream_action(),
            context=context,
            using=self.template_engine,
        )


class PartialTemplateResolverMixin(TurboStreamTemplateResponseMixin):

    partial_template_prefix = "_"
    turbo_stream_template_name = None

    def get_partial_template_names(self):
        def resolve_name(name):
            start, part, end = name.rpartition("/")
            return "".join([start, part, self.partial_template_prefix, end])

        return [resolve_name(name) for name in self.get_template_names()]

    def get_turbo_stream_template_names(self):
        return (
            [self.turbo_stream_template_name]
            if self.turbo_stream_template_name
            else self.get_partial_template_names()
        )


class TurboStreamFormMixin(PartialTemplateResolverMixin):
    turbo_stream_action = "replace"

    def form_invalid(self, form):
        return self.render_turbo_stream_response(self.get_context_data(form=form))


class TurboFrameResponseMixin:
    turbo_frame_dom_id = None

    def get_turbo_frame_dom_id(self):
        return self.turbo_frame_dom_id

    def get_response_content(self):
        return ""

    def render_turbo_frame_response(self, **response_kwargs):

        return TurboFrameResponse(
            content=self.get_response_content(),
            dom_id=self.get_turbo_frame_dom_id(),
            **response_kwargs
        )


class TurboFrameTemplateResponseMixin(TurboFrameResponseMixin):
    """Use with ContextMixin subclass"""

    def render_turbo_frame_response(self, context, **response_kwargs):
        return TurboFrameTemplateResponse(
            request=self.request,
            template=self.get_template_names(),
            dom_id=self.get_turbo_frame_dom_id(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )
