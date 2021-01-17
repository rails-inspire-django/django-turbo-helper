# Standard Library
import http
from typing import Any, Dict, Iterable, Optional, Union

# Django
from django.forms import Form
from django.http import HttpRequest
from django.template.response import TemplateResponse

# Local
from .constants import Action
from .renderers import render_turbo_frame, render_turbo_stream
from .response import (
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)
from .template import render_turbo_frame_template, render_turbo_stream_template


class TurboStreamAction:
    """Returns strings and responses for a specific Turbo Stream action type."""

    def __init__(self, target: str, action: Action):
        """
        :param target: Turbo Stream target
        :param action: Turbo Stream action
        """
        self.action = action
        self.target = target

    def render(self, content: str = "") -> str:
        """
        :param content: enclosed content
        :return: a *<turbo-stream>* string
        """
        return render_turbo_stream(
            action=self.action, target=self.target, content=content
        )

    def response(self, content: str = "", **response_kwargs) -> TurboStreamResponse:
        """
        :param content: enclosed content
        :return: a *<turbo-stream>* HTTP response wrapper
        """
        return TurboStreamResponse(
            action=self.action, target=self.target, content=content, **response_kwargs
        )

    def template(
        self, template_name: str, context=Optional[Dict[str, Any]], **template_kwargs
    ):
        """
        :param template_name: Django template name
        :param context: template context

        :return: a *<turbo-stream>* template wrapper
        """
        return TurboStreamTemplateProxy(
            template_name,
            context,
            action=self.action,
            target=self.target,
            **template_kwargs,
        )


class TurboStream:
    """
    Class for creating Turbo Stream strings and responses.
    """

    def __init__(self, target: str):
        """
        :param target: stream target
        """
        self.target = target

    @property
    def append(self) -> TurboStreamAction:
        return TurboStreamAction(self.target, Action.APPEND)

    @property
    def prepend(self) -> TurboStreamAction:
        return TurboStreamAction(self.target, Action.PREPEND)

    @property
    def remove(self) -> TurboStreamAction:
        return TurboStreamAction(self.target, Action.REMOVE)

    @property
    def replace(self) -> TurboStreamAction:
        return TurboStreamAction(self.target, Action.REPLACE)

    @property
    def update(self) -> TurboStreamAction:
        return TurboStreamAction(self.target, Action.UPDATE)


class TurboStreamTemplateProxy:
    """Wraps template functionality."""

    def __init__(self, template_name, context, *, action, target, **template_kwargs):
        self.action = action
        self.target = target
        self.template_name = template_name
        self.context = context
        self.template_kwargs = template_kwargs

    def render(self) -> str:
        return render_turbo_stream_template(
            self.template_name,
            self.context,
            action=self.action,
            target=self.target,
            **self.template_kwargs,
        )

    def response(self, request: HttpRequest, **kwargs) -> TurboStreamTemplateResponse:
        return TurboStreamTemplateResponse(
            request,
            self.template_name,
            self.context,
            action=self.action,
            target=self.target,
            **{**self.template_kwargs, **kwargs},
        )


class TurboFrameTemplateProxy:
    """Wraps template functionality."""

    def __init__(
        self,
        template_name: str,
        context: Dict[str, Any],
        *,
        dom_id: str,
        **template_kwargs,
    ):
        self.template_name = template_name
        self.context = context
        self.template_kwargs = template_kwargs
        self.dom_id = dom_id

    def render(self) -> str:
        """
        :param content: enclosed content
        :return: a *<turbo-frame>* string
        """
        return render_turbo_frame_template(
            self.template_name, self.context, dom_id=self.dom_id, **self.template_kwargs
        )

    def response(self, request: HttpRequest, **kwargs) -> TurboFrameTemplateResponse:
        return TurboFrameTemplateResponse(
            request,
            self.template_name,
            self.context,
            dom_id=self.dom_id,
            **{**self.template_kwargs, **kwargs},
        )


class TurboFrame:
    """Class for creating Turbo Frame strings and responses."""

    def __init__(self, dom_id: str):
        """
        :param dom_id: DOM ID of turbo frame
        """
        self.dom_id = dom_id

    def render(self, content: str = "") -> str:
        """
        :param content: enclosed content
        :return: a *<turbo-frame>* string
        """
        return render_turbo_frame(dom_id=self.dom_id, content=content)

    def response(self, content: str = "", **response_kwargs) -> TurboFrameResponse:
        """
        :param content: enclosed content
        :return: a *<turbo-frame>* HTTP response
        """
        return TurboFrameResponse(
            dom_id=self.dom_id, content=content, **response_kwargs
        )

    def template(
        self, template_name: str, context=Optional[Dict[str, Any]], **template_kwargs
    ) -> TurboFrameTemplateProxy:
        """
        :param template_name: Django template name(s)
        :param context: template context
        :return: a *<turbo-frame>* HTTP response
        """
        return TurboFrameTemplateProxy(
            template_name, context, dom_id=self.dom_id, **template_kwargs
        )


def render_form_response(
    request: HttpRequest,
    form: Form,
    template: Union[str, Iterable[str]],
    context: Optional[Dict[str, Any]] = None,
    **response_kwargs,
) -> TemplateResponse:
    """Returns a TemplateResponse with the correct status if the form contains errors."""

    return TemplateResponse(
        request,
        template,
        context={"form": form, **(context or {})},
        status=http.HTTPStatus.UNPROCESSABLE_ENTITY
        if form.errors
        else http.HTTPStatus.OK,
        **response_kwargs,
    )
