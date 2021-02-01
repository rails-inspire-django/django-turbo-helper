# Standard Library
import http
from typing import Any, Callable, Dict, List, Optional, Type

# Django
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.template.engine import Engine

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

    request: HttpRequest
    template_engine: Engine
    get_template_names: Callable

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

    request: HttpRequest
    render_to_response: Callable
    get_success_url: Callable
    get_context_data: Callable

    def form_invalid(self, form: forms.Form) -> HttpResponse:
        return self.render_to_response(
            self.get_context_data(form=form),
            status=http.HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    def form_valid(self, form: forms.Form) -> HttpResponse:
        return HttpResponseSeeOther(self.get_success_url())


class TurboFormModelMixin(TurboFormMixin):

    object: Optional[Model]

    def form_valid(self, form: forms.Form) -> HttpResponse:
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class TurboStreamFormMixin(TurboFormMixin):
    """Returns a turbo stream when form is invalid.

    You should define a partial template corresponding to the template
    used to render the initial form, for example if your template
    is `posts/post_form.html` your partial template is `posts/_post_form.html`.

    The template should then be included in the form:

    .. code-block:: html

        {% include "_post_form.html" %}

    The form or container element should have an ID: this is provided as `turbo_stream_target` in
    the template context:


    .. code-block:: html

        <form method="POST" action=".." id="{{ turbo_stream_target }}">

    When the form is posted, if the form is invalid a turbo-stream element wrapping the
    partial content will be returned, including any validation errors.
    """

    action: Action = Action.REPLACE
    target: Optional[str] = None

    turbo_stream_template_prefix: str = "_"
    turbo_stream_template_name: Optional[str] = None

    template_engine: Engine
    get_template_names: Callable

    def resolve_turbo_stream_template_name(self, template_name):
        """By default template name will have underscore prefix"""
        start, join, name = template_name.rpartition("/")
        return start + join + self.turbo_stream_template_prefix + name

    def get_turbo_stream_target(self) -> str:
        if self.target:
            return self.target

        raise ImproperlyConfigured("target is not provided")

    def get_turbo_stream_action(self) -> Action:
        return self.action

    def get_turbo_stream_template_names(self) -> List[str]:
        if self.turbo_stream_template_name:
            return [self.turbo_stream_template_name]
        return [
            self.resolve_turbo_stream_template_name(template)
            for template in self.get_template_names()
        ]

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        if "turbo_stream_target" not in kwargs:
            kwargs["turbo_stream_target"] = self.get_turbo_stream_target()

        return super().get_context_data(**kwargs)

    def render_turbo_stream_response(self, **context) -> HttpResponse:
        target = self.get_turbo_stream_target()
        action = self.get_turbo_stream_action()

        return TurboStreamTemplateResponse(
            request=self.request,
            template=self.get_turbo_stream_template_names(),
            target=target,
            action=action,
            context=self.get_context_data(
                is_turbo_stream=True, target=target, **context
            ),
            using=self.template_engine,
        )

    def form_invalid(self, form: forms.Form) -> HttpResponse:
        return self.render_turbo_stream_response(form=form)


class TurboStreamFormModelMixin(TurboStreamFormMixin):
    object: Optional[Model]
    model: Type[Model]

    def get_turbo_stream_target(self) -> str:
        try:
            return super().get_turbo_stream_target()

        except ImproperlyConfigured:
            if isinstance(self.object, Model):
                return f"form-{self.object._meta.model_name}-{self.object.pk}"

            elif self.model:
                return f"form-{self.model._meta.model_name}"

            raise

    def form_valid(self, form: forms.Form) -> HttpResponse:
        self.object = form.save()
        return super().form_valid(form)


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

    request: HttpRequest
    template_engine: Engine
    get_template_names: Callable

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
