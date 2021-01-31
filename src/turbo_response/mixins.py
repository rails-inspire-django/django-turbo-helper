# Standard Library
import http
from typing import Any, Dict, List, Optional

# Django
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
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
        target = self.get_turbo_stream_target()
        action = self.get_turbo_stream_action()

        if target is None:
            raise ImproperlyConfigured("target is None")

        if action is None:
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

        target = self.get_turbo_stream_target()
        action = self.get_turbo_stream_action()

        if target is None:
            raise ImproperlyConfigured("target is None")

        if action is None:
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
    def form_valid(self, form: forms.Form) -> HttpResponse:
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class TurboStreamFormModelMixin(TurboFormMixin):
    """Returns a turbo stream when form is invalid."""

    action: Action = Action.REPLACE
    target: Optional[str] = None

    def get_turbo_stream_target(self) -> str:
        if self.target:
            return self.target

        if isinstance(self.object, Model):
            return f"form-{self.object._meta.model_name}-{self.object.pk}"

        elif self.model:
            return f"form-{self.model._meta.model_name}"

        raise ImproperlyConfigured("target is not provided")

    def get_turbo_stream_action(self) -> Action:
        return self.action

    def get_turbo_stream_template_names(self) -> List[str]:
        """By default template name will have underscore prefix"""
        return [
            _resolve_partial_name(template) for template in self.get_template_names()
        ]

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        if "target" not in kwargs:
            kwargs["target"] = self.get_turbo_stream_target()

        if "action" not in kwargs:
            kwargs["action"] = self.get_turbo_stream_action()

        return super().get_context_data(**kwargs)

    def form_valid(self, form: forms.Form) -> HttpResponse:
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form: forms.Form) -> HttpResponse:
        target = self.get_turbo_stream_target()
        action = self.get_turbo_stream_action()

        return TurboStreamTemplateResponse(
            request=self.request,
            template=self.get_turbo_stream_template_names(),
            target=target,
            action=action,
            context=self.get_context_data(
                form=form, target=target, is_turbo_stream=True
            ),
            using=self.template_engine,
        )


class TurboFrameResponseMixin(TurboFrameArgsMixin):
    """Renders turbo-frame responses"""

    def get_response_content(self) -> str:
        return ""

    def render_turbo_frame(self, **response_kwargs) -> TurboFrameResponse:
        """Renders a turbo frame to response."""

        dom_id = self.get_turbo_frame_dom_id()

        if dom_id is None:
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
        dom_id = self.get_turbo_frame_dom_id()
        if dom_id is None:
            raise ValueError("dom_id must be specified")

        return TurboFrameTemplateResponse(
            request=self.request,
            template=self.get_template_names(),
            dom_id=dom_id,
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )


def _resolve_partial_name(template, prefix="_"):
    start, _, name = template.rpartition("/")
    return start + "/" + prefix + name
