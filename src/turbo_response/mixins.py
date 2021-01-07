# Standard Library
import http
from typing import Any, Dict, Iterable, Optional

# Django
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse

# Local
from .redirects import HttpResponseSeeOther
from .renderers import Action
from .response import (
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)


class TurboStreamResponseMixin:
    """Mixin to handle turbo-stream responses"""

    turbo_stream_action: Optional[Action] = None
    turbo_stream_target: Optional[str] = None

    def get_turbo_stream_action(self) -> Optional[Action]:
        """Returns the turbo-stream action parameter

        :return: turbo-stream action
        """
        return self.turbo_stream_action

    def get_turbo_stream_target(self) -> Optional[str]:
        """Returns the turbo-stream target parameter

        :return: turbo-stream target
        """
        return self.turbo_stream_target

    def get_response_content(self) -> str:
        """Returns turbo-stream content."""

        return ""

    def render_turbo_stream_response(self, **response_kwargs) -> TurboStreamResponse:
        """Returns a turbo-stream response."""
        if (target := self.get_turbo_stream_target()) is None:
            raise ImproperlyConfigured("target is None")

        if (action := self.get_turbo_stream_action()) is None:
            raise ImproperlyConfigured("action is None")

        return TurboStreamResponse(
            action=action,
            target=target,
            content=self.get_response_content(),
            **response_kwargs,
        )


class TurboStreamTemplateResponseMixin(TurboStreamResponseMixin):
    """Handles turbo-stream template responses."""

    def get_turbo_stream_template_names(self) -> Iterable[str]:
        """Returns list of template names."""
        return self.get_template_names()

    def render_turbo_stream_template_response(
        self, context: Dict[str, Any], **response_kwargs
    ) -> TurboStreamTemplateResponse:
        """Renders a turbo-stream template response.

        :param context: template context
        :type context: dict

        """

        if (target := self.get_turbo_stream_target()) is None:
            raise ImproperlyConfigured("target is None")

        if (action := self.get_turbo_stream_action()) is None:
            raise ImproperlyConfigured("action is None")

        return TurboStreamTemplateResponse(
            request=self.request,
            template=self.get_turbo_stream_template_names(),
            target=target,
            action=action,
            context=context,
            using=self.template_engine,
        )


class TurboFormMixin:
    """Mixin for handling form validation. Ensures response
    has 422 status on invalid and 303 on success"""

    def form_invalid(self, form: forms.Form) -> HttpResponse:
        return self.render_to_response(
            self.get_context_data(form=form),
            status=http.HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    def form_valid(self, form: forms.Form) -> HttpResponse:
        return HttpResponseSeeOther(self.get_success_url())


class TurboFormModelMixin(TurboFormMixin):
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class TurboFrameResponseMixin:
    turbo_frame_dom_id = None

    def get_turbo_frame_dom_id(self) -> Optional[str]:
        return self.turbo_frame_dom_id

    def get_response_content(self) -> str:
        return ""

    def render_turbo_frame_response(self, **response_kwargs) -> TurboFrameResponse:

        if (dom_id := self.get_turbo_frame_dom_id()) is None:
            raise ValueError("dom_id must be specified")

        return TurboFrameResponse(
            content=self.get_response_content(), dom_id=dom_id, **response_kwargs,
        )


class TurboFrameTemplateResponseMixin(TurboFrameResponseMixin):
    """Handles turbo-frame template responses."""

    def render_turbo_frame_template_response(
        self, context: Dict[str, Any], **response_kwargs
    ) -> TurboFrameTemplateResponse:
        """Returns a turbo-frame response.

        :param context: template context

        """
        if (dom_id := self.get_turbo_frame_dom_id()) is None:
            raise ValueError("dom_id must be specified")

        return TurboFrameTemplateResponse(
            request=self.request,
            template=self.get_template_names(),
            dom_id=dom_id,
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )
