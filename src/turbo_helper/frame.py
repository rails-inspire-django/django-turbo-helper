from typing import Any, Dict, List, Optional, Union

from django.http import HttpRequest

from .renderers import render_turbo_frame
from .response import TurboFrameResponse, TurboFrameTemplateResponse
from .template import render_turbo_frame_template


class TurboFrameTemplate:
    """Wraps template functionality."""

    def __init__(
        self,
        template_name: Union[str, List[str]],
        context: Optional[Dict[str, Any]] = None,
        *,
        dom_id: str,
        **template_kwargs,
    ):
        self.template_name = template_name
        self.context = context
        self.template_kwargs = template_kwargs
        self.dom_id = dom_id

    def render(self, **kwargs) -> str:
        """
        :param content: enclosed content
        :return: a *<turbo-frame>* string
        """
        return render_turbo_frame_template(
            self.template_name,
            self.context,
            dom_id=self.dom_id,
            **{**self.template_kwargs, **kwargs},
        )

    def response(
        self, request: Optional[HttpRequest] = None, **kwargs
    ) -> TurboFrameTemplateResponse:
        request = request or self.template_kwargs.pop("request", None)
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

    def render(self, content: str = "", **kwargs) -> str:
        """
        :param content: enclosed content

        :return: a *<turbo-frame>* string
        """
        return render_turbo_frame(dom_id=self.dom_id, content=content, **kwargs)

    def response(self, content: str = "", **kwargs) -> TurboFrameResponse:
        """
        :param content: enclosed content
        :param is_safe: mark content safe for HTML escaping.

        :return: a *<turbo-frame>* HTTP response
        """
        return TurboFrameResponse(dom_id=self.dom_id, content=content, **kwargs)

    def template(
        self,
        template_name: Union[str, List[str]],
        context=Optional[Dict[str, Any]],
        **template_kwargs,
    ) -> TurboFrameTemplate:
        """
        :param template_name: Django template name(s)
        :param context: template context
        :return: a *<turbo-frame>* HTTP response
        """
        return TurboFrameTemplate(
            template_name, context, dom_id=self.dom_id, **template_kwargs
        )
