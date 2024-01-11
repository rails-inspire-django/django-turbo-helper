from typing import Any, Dict, Optional

from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView, FormView, TemplateView, UpdateView, View
from django.views.generic.detail import SingleObjectMixin

from . import Action
from .mixins import (
    TurboFormMixin,
    TurboFrameResponseMixin,
    TurboFrameTemplateResponseMixin,
    TurboStreamFormMixin,
    TurboStreamFormModelMixin,
    TurboStreamResponseMixin,
    TurboStreamTemplateResponseMixin,
)


class TurboStreamView(TurboStreamResponseMixin, View):
    """Renders a simple turbo-stream view"""

    def dispatch(self, *args, **kwargs) -> HttpResponse:
        return self.render_turbo_stream()


class TurboStreamTemplateView(TurboStreamTemplateResponseMixin, TemplateView):
    """Renders response template inside <turbo-stream> tags."""

    def render_to_response(
        self, context: Dict[str, Any], **response_kwargs
    ) -> HttpResponse:
        return self.render_turbo_stream(context, **response_kwargs)


class TurboFormView(TurboFormMixin, FormView):
    ...


class TurboCreateView(TurboFormMixin, CreateView):
    ...


class TurboUpdateView(TurboFormMixin, UpdateView):
    ...


class TurboStreamFormView(TurboStreamFormMixin, FormView):
    ...


class TurboStreamCreateView(TurboStreamFormModelMixin, CreateView):
    ...


class TurboStreamUpdateView(TurboStreamFormModelMixin, UpdateView):
    ...


class TurboStreamDeleteView(TurboStreamResponseMixin, SingleObjectMixin, View):
    """Handles a delete action, returning an empty turbo-stream "remove"
    response. The target will be automatically resolved as {model_name}-{PK}.
    """

    turbo_stream_action = Action.REMOVE

    def get_turbo_stream_target(self) -> Optional[str]:
        return f"{self.object._meta.model_name}-{self.object.pk}"

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.delete(request, *args, **kwargs)

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # problem: object target needs to be defined *before* object is
        # deleted as ID will be None. So we need to get the response first
        # in order to resolve the target ID.
        self.object = self.get_object()
        response = self.render_turbo_stream()
        self.object.delete()
        return response


class TurboFrameView(TurboFrameResponseMixin, View):
    """Retuns a simple turbo-frame response."""

    def dispatch(self, *args, **kwargs) -> HttpResponse:
        return self.render_turbo_frame()


class TurboFrameTemplateView(TurboFrameTemplateResponseMixin, TemplateView):
    """Renders response template inside <turbo-frame> tags."""

    def render_to_response(
        self, context: Dict[str, Any], **response_kwargs
    ) -> HttpResponse:
        return self.render_turbo_frame(context, **response_kwargs)
