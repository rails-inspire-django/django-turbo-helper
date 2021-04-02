from typing import Any, Dict, List, Optional, Union

from django.http import HttpRequest

from .constants import Action
from .renderers import render_turbo_stream
from .response import TurboStreamResponse, TurboStreamTemplateResponse
from .template import render_turbo_stream_template


class TurboStreamTemplate:
    """Wraps template functionality."""

    def __init__(
        self,
        template_name: Union[str, List[str]],
        context: Optional[Dict[str, Any]] = None,
        *,
        action: Action,
        target: str,
        **template_kwargs,
    ):
        self.action = action
        self.target = target
        self.template_name = template_name
        self.context = context
        self.template_kwargs = template_kwargs

    def render(self, **kwargs) -> str:
        return render_turbo_stream_template(
            self.template_name,
            self.context,
            action=self.action,
            target=self.target,
            **{**self.template_kwargs, **kwargs},
        )

    def response(
        self, request: Optional[HttpRequest] = None, **kwargs
    ) -> TurboStreamTemplateResponse:
        request = request or self.template_kwargs.pop("request", None)
        return TurboStreamTemplateResponse(
            request,
            self.template_name,
            self.context,
            action=self.action,
            target=self.target,
            **{**self.template_kwargs, **kwargs},
        )


class TurboStreamAction:
    """Returns strings and responses for a specific Turbo Stream action type."""

    def __init__(self, target: str, action: Action):
        """
        :param target: Turbo Stream target
        :param action: Turbo Stream action
        """
        self.action = action
        self.target = target

    def render(
        self,
        content: str = "",
        **kwargs,
    ) -> str:
        """
        :param content: enclosed content

        :return: a *<turbo-stream>* string
        """
        return render_turbo_stream(
            action=self.action, target=self.target, content=content, **kwargs
        )

    def response(
        self,
        content: str = "",
        **kwargs,
    ) -> TurboStreamResponse:
        """
        :param content: enclosed content
        :return: a *<turbo-stream>* HTTP response wrapper
        """
        return TurboStreamResponse(
            action=self.action,
            target=self.target,
            content=content,
            **kwargs,
        )

    def template(
        self,
        template_name: Union[str, List[str]],
        context: Optional[Dict[str, Any]] = None,
        **template_kwargs,
    ) -> TurboStreamTemplate:
        """
        :param template_name: Django template name
        :param context: template context

        :return: a *<turbo-stream>* template wrapper
        """
        return TurboStreamTemplate(
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

    def action(self, action: Action) -> TurboStreamAction:
        return TurboStreamAction(self.target, action)

    @property
    def append(self) -> TurboStreamAction:
        return self.action(Action.APPEND)

    @property
    def prepend(self) -> TurboStreamAction:
        return self.action(Action.PREPEND)

    @property
    def remove(self) -> TurboStreamAction:
        return self.action(Action.REMOVE)

    @property
    def replace(self) -> TurboStreamAction:
        return self.action(Action.REPLACE)

    @property
    def update(self) -> TurboStreamAction:
        return self.action(Action.UPDATE)
