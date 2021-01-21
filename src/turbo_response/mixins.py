# Standard Library
import http
from typing import Any, Dict, Optional

# Django
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse

# Local
from .constants import Action
from .redirects import HttpResponseSeeOther
from .response import (
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)


class TurboStreamArgsMixin:
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


class TurboFrameArgsMixin:
    turbo_frame_dom_id = None

    def get_turbo_frame_dom_id(self) -> Optional[str]:
        """Should return a valid DOM ID target for the turbo frame."""
        return self.turbo_frame_dom_id


class TurboStreamResponseMixin(TurboStreamArgsMixin):
    """Handles turbo-stream responses"""

    def get_response_content(self) -> str:
        """Returns turbo-stream content."""

        return ""

    def render_turbo_stream(self, **response_kwargs) -> TurboStreamResponse:
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


class TurboStreamTemplateResponseMixin(TurboStreamArgsMixin):
    """Handles turbo-stream template responses."""

    def render_turbo_stream(
        self, context: Dict[str, Any], **response_kwargs
    ) -> TurboStreamTemplateResponse:
        """Renders a turbo-stream template response.

        :param context: template context
        """

        if (target := self.get_turbo_stream_target()) is None:
            raise ImproperlyConfigured("target is None")

        if (action := self.get_turbo_stream_action()) is None:
            raise ImproperlyConfigured("action is None")

        return TurboStreamTemplateResponse(
            request=self.request,
            template=self.get_template_names(),
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


class TurboFrameResponseMixin(TurboFrameArgsMixin):
    """Renders turbo-frame responses"""

    def get_response_content(self) -> str:
        return ""

    def render_turbo_frame(self, **response_kwargs) -> TurboFrameResponse:
        """Renders a turbo frame to response."""

        if (dom_id := self.get_turbo_frame_dom_id()) is None:
            raise ValueError("dom_id must be specified")

        return TurboFrameResponse(
            content=self.get_response_content(),
            dom_id=dom_id,
            **response_kwargs,
        )


class TurboFrameTemplateResponseMixin(TurboFrameArgsMixin):
    """Handles turbo-frame template responses."""

    def render_turbo_frame(
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
