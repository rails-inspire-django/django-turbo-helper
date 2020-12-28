# Local
from .response import (
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)


class PartialTemplateResolverMixin:
    partial_template_prefix = "_"
    """Attempts to guess name of template based on prefix.
    For example, if your template is "todos/todo_form.html"
    then `get_partial_template_names()` will return
    "todos/_todo_form.html".
    """

    def get_partial_template_names(self):
        def resolve_name(name):
            start, part, end = name.rpartition("/")
            return "".join([start, part, self.partial_template_prefix, end])

        return [resolve_name(name) for name in self.get_template_names()]


class TurboStreamResponseMixin:
    turbo_stream_action = None
    turbo_stream_target = None

    def get_turbo_stream_action(self):
        return self.turbo_stream_action

    def get_response_content(self):
        return ""

    def render_turbo_stream_response(self):

        return TurboStreamResponse(
            self.get_turbo_stream_action(),
            self.get_turbo_stream_target(),
            self.get_response_content(),
        )


class TurboStreamTemplateResponseMixin(
    PartialTemplateResolverMixin, TurboStreamResponseMixin
):
    """Use with ContextMixin subclass"""

    turbo_stream_template = None

    def get_turbo_stream_template_names(self):
        return self.turbo_stream_template or self.get_partial_template_names()

    def render_turbo_stream_response(self, **context):
        return TurboStreamTemplateResponse(
            request=self.request,
            template=self.get_turbo_stream_template_names(),
            target=self.get_turbo_stream_target(),
            action=self.get_turbo_stream_action(),
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

    def get_response_content(self):
        return ""

    def render_turbo_frame_response(self):
        return TurboFrameResponse(
            self.get_response_content(), dom_id=self.get_turbo_frame_dom_id(),
        )


class TurboFrameTemplateResponseMixin(TurboFrameResponseMixin):
    """Use with ContextMixin subclass"""

    turbo_frame_template = None

    def get_turbo_frame_template_names(self):
        return self.turbo_frame_template or self.get_partial_template_names()

    def render_turbo_frame_response(self, **context):
        return TurboFrameTemplateResponse(
            request=self.request,
            template=self.get_turbo_frame_template_names(),
            dom_id=self.get_turbo_frame_params(),
            context=self.get_context_data(context),
            using=self.template_engine,
        )
