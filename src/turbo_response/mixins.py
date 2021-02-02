# Standard Library
import http
import warnings
from typing import Any, Callable, Dict, List, Optional, Type

# Django
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.template.engine import Engine
from django.views.generic.edit import FormMixin

# Local
from .constants import Action
from .response import HttpResponseSeeOther
from .turbo_frame import TurboFrame
from .turbo_stream import TurboStream, TurboStreamAction


class TurboStreamMixin:
    turbo_stream_action: Optional[Action] = None
    turbo_stream_target: Optional[str] = None

    def get_turbo_stream(self) -> TurboStreamAction:
        return TurboStream(self.get_turbo_stream_target_or_raise()).action(
            self.get_turbo_stream_action_or_raise()
        )

    def get_turbo_stream_action_or_raise(self) -> Action:
        """Returns the turbo-stream action parameter

        :return: turbo-stream action
        :raise: ImproperlyConfigured
        """
        action = self.get_turbo_stream_action()
        if not action:
            raise ImproperlyConfigured(
                f"turbo stream action not defined in {self.__class__}.get_turbo_stream_action"
            )
        return action

    def get_turbo_stream_action(self) -> Optional[Action]:
        """Returns the turbo-stream action parameter

        :return: turbo-stream action
        """
        return self.turbo_stream_action

    def get_turbo_stream_target_or_raise(self) -> str:
        """Returns the turbo-stream action parameter

        :return: turbo-stream target
        :raise: ImproperlyConfigured
        """
        target = self.get_turbo_stream_target()
        if not target:
            raise ImproperlyConfigured(
                f"turbo stream target not defined in {self.__class__}.get_turbo_stream_target"
            )
        return target

    def get_turbo_stream_target(self) -> Optional[str]:
        """Returns the turbo-stream target parameter

        :return: turbo-stream target
        """
        return self.turbo_stream_target


class TurboFrameMixin:
    turbo_frame_dom_id: Optional[str] = None

    def get_turbo_frame(self) -> TurboFrame:
        return TurboFrame(self.get_turbo_frame_dom_id_or_raise())

    def get_turbo_frame_dom_id_or_raise(self) -> str:

        dom_id = self.get_turbo_frame_dom_id()
        if not dom_id:
            raise ImproperlyConfigured(
                "turbo frame dom ID not defined in {self.__class__}.get_turbo_frame_dom_id"
            )
        return dom_id

    def get_turbo_frame_dom_id(self) -> Optional[str]:
        """Should return a valid DOM ID target for the turbo frame."""
        return self.turbo_frame_dom_id


class TurboStreamResponseMixin(TurboStreamMixin):
    """Handles turbo-stream responses"""

    def get_response_content(self) -> str:
        """Returns turbo-stream content."""

        return ""

    def render_turbo_stream(self, **response_kwargs) -> HttpResponse:
        """Returns a turbo-stream response."""
        return self.get_turbo_stream().response(
            self.get_response_content(), **response_kwargs
        )


class TurboStreamTemplateResponseMixin(TurboStreamMixin):
    """Handles turbo-stream template responses."""

    request: HttpRequest
    template_engine: Engine
    get_template_names: Callable

    def render_turbo_stream(
        self, context: Dict[str, Any], **response_kwargs
    ) -> HttpResponse:
        """Renders a turbo-stream template response.

        :param context: template context
        """

        return (
            self.get_turbo_stream()
            .template(self.get_template_names(), context, using=self.template_engine)
            .response(self.request)
        )


class TurboFormMixin(FormMixin):
    """Mixin for handling form validation. Ensures response
    has 422 status on invalid and 303 on success"""

    def form_invalid(self, form: forms.Form) -> HttpResponse:
        return self.render_to_response(
            self.get_context_data(form=form),
            status=http.HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    def form_valid(self, form: forms.Form) -> HttpResponse:
        super().form_valid(form)  # type: ignore
        return HttpResponseSeeOther(self.get_success_url())


class TurboFormModelMixin(TurboFormMixin):

    object: Optional[Model]

    def form_valid(self, form: forms.Form) -> HttpResponse:
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class TurboStreamFormMixin(TurboStreamMixin, TurboFormMixin):
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

    # deprecated
    target: Optional[str] = None

    # deprecated
    action: Action = Action.REPLACE

    turbo_stream_action: Action = Action.REPLACE

    turbo_stream_template_prefix: str = "_"
    turbo_stream_template_name: Optional[str] = None

    template_engine: Engine
    get_template_names: Callable

    def resolve_turbo_stream_template_name(self, template_name):
        """By default template name will have underscore prefix"""
        start, join, name = template_name.rpartition("/")
        return start + join + self.turbo_stream_template_prefix + name

    def get_turbo_stream_target(self) -> Optional[str]:
        # "target" is deprecated: should be turbo_stream_target
        target = getattr(self, "target", None)
        if target:
            warnings.warn("'target' is deprecated: use turbo_stream_target instead")
            return target

        return super().get_turbo_stream_target()

    def get_turbo_stream_action(self) -> Optional[Action]:
        if hasattr(self, "action") and self.action != Action.REPLACE:
            warnings.warn("'action' is deprecated: use turbo_stream_action instead")
            return self.action
        return super().get_turbo_stream_action()

    def get_turbo_stream_template_names(self) -> List[str]:
        if self.turbo_stream_template_name:
            return [self.turbo_stream_template_name]
        return [
            self.resolve_turbo_stream_template_name(template)
            for template in self.get_template_names()
        ]

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        if "turbo_stream_target" not in kwargs:
            kwargs["turbo_stream_target"] = self.get_turbo_stream_target_or_raise()

        return super().get_context_data(**kwargs)

    def render_turbo_stream_response(self, **context) -> HttpResponse:

        stream = self.get_turbo_stream()

        return stream.template(
            self.get_turbo_stream_template_names(),
            context=self.get_context_data(
                is_turbo_stream=True, turbo_stream_target=stream.target, **context
            ),
            using=self.template_engine,
        ).response(self.request)

    def form_invalid(self, form: forms.Form) -> HttpResponse:
        return self.render_turbo_stream_response(form=form)


class TurboStreamFormModelMixin(TurboStreamFormMixin):
    object: Optional[Model]
    model: Type[Model]

    def get_turbo_stream_target(self) -> Optional[str]:
        target = super().get_turbo_stream_target()
        if target:
            return target

        if isinstance(self.object, Model):
            return f"form-{self.object._meta.model_name}-{self.object.pk}"

        elif self.model:
            return f"form-{self.model._meta.model_name}"

        return None

    def form_valid(self, form: forms.Form) -> HttpResponse:
        self.object = form.save()
        return super().form_valid(form)


class TurboFrameResponseMixin(TurboFrameMixin):
    """Renders turbo-frame responses"""

    def get_response_content(self) -> str:
        return ""

    def render_turbo_frame(self, **response_kwargs) -> HttpResponse:
        """Renders a turbo frame to response."""

        return self.get_turbo_frame().response(
            self.get_response_content(), **response_kwargs
        )


class TurboFrameTemplateResponseMixin(TurboFrameMixin):
    """Handles turbo-frame template responses."""

    request: HttpRequest
    template_engine: Engine
    get_template_names: Callable

    def render_turbo_frame(
        self, context: Dict[str, Any], **response_kwargs
    ) -> HttpResponse:
        """Returns a turbo-frame response.

        :param context: template context
        """
        return (
            self.get_turbo_frame()
            .template(self.get_template_names(), context, using=self.template_engine)
            .response(self.request)
        )
