# Standard Library
from typing import Any, Dict

# Django
from django.http import HttpRequest, HttpResponse
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    TemplateView,
    UpdateView,
    View,
)

# Local
from . import Action
from .mixins import (
    TurboFormMixin,
    TurboFrameResponseMixin,
    TurboFrameTemplateResponseMixin,
    TurboStreamResponseMixin,
    TurboStreamTemplateResponseMixin,
)


class TurboStreamView(TurboStreamResponseMixin, View):
    """Renders a simple turbo-stream view"""

    def dispatch(self, *args, **kwargs) -> HttpResponse:
        return self.render_turbo_stream_response()


class TurboStreamTemplateView(TurboStreamTemplateResponseMixin, TemplateView):
    """Renders response template inside <turbo-stream> tags. """

    def render_to_response(
        self, context: Dict[str, Any], **response_kwargs
    ) -> HttpResponse:
        return self.render_turbo_stream_template_response(context, **response_kwargs)


class TurboFormView(TurboFormMixin, FormView):
    ...


class TurboCreateView(TurboFormMixin, CreateView):
    ...


class TurboUpdateView(TurboFormMixin, UpdateView):
    ...


class TurboStreamDeleteView(TurboStreamResponseMixin, DeleteView):
    """Handles a delete action, returning an empty turbo-stream "remove"
    response.
    """

    turbo_stream_action = Action.REMOVE

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        self.object.delete()
        return self.render_turbo_stream_response()


class TurboFrameView(TurboFrameResponseMixin, View):
    """Retuns a simple turbo-frame response."""

    def dispatch(self, *args, **kwargs) -> HttpResponse:
        return self.render_turbo_frame_response()


class TurboFrameTemplateView(TurboFrameTemplateResponseMixin, TemplateView):
    """Renders response template inside <turbo-frame> tags. """

    def render_to_response(
        self, context: Dict[str, Any], **response_kwargs
    ) -> HttpResponse:
        return self.render_turbo_frame_template_response(context, **response_kwargs)
