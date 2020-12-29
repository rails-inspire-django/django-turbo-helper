# Django
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    TemplateView,
    UpdateView,
    View,
)

# Local
from .mixins import (
    TurboFrameResponseMixin,
    TurboFrameTemplateResponseMixin,
    TurboStreamFormMixin,
    TurboStreamResponseMixin,
    TurboStreamTemplateResponseMixin,
)


class TurboStreamView(TurboStreamResponseMixin, View):
    """Renders a simple turbo stream view"""

    def dispatch(self, *args, **kwargs):
        return self.render_turbo_stream_response()


class TurboStreamTemplateView(TurboStreamTemplateResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_turbo_stream_response(context, **response_kwargs)


class TurboStreamFormView(TurboStreamFormMixin, FormView):
    ...


class TurboStreamCreateView(TurboStreamFormMixin, CreateView):
    ...


class TurboStreamUpdateView(TurboStreamFormMixin, UpdateView):
    ...


class TurboStreamDeleteView(TurboStreamResponseMixin, DeleteView):
    turbo_stream_action = "remove"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_turbo_stream_response()


class TurboFrameView(TurboFrameResponseMixin, View):
    def dispatch(self, *args, **kwargs):
        return self.render_turbo_frame_response()


class TurboFrameTemplateView(TurboFrameTemplateResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_turbo_frame_response(context, **response_kwargs)
