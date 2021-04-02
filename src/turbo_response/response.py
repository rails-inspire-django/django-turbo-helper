import http
from typing import Any, Dict, Iterable, Mapping, Optional, Union

from django.forms.renderers import BaseRenderer
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    StreamingHttpResponse,
)
from django.template.response import TemplateResponse

from .constants import TURBO_STREAM_MIME_TYPE, Action
from .renderers import render_turbo_frame, render_turbo_stream


class HttpResponseSeeOther(HttpResponseRedirect):
    """Redirect with 303 status"""

    status_code = http.HTTPStatus.SEE_OTHER


class TurboStreamResponseMixin:
    """Automatically sets the correct turbo-stream content type."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            content_type=f"{TURBO_STREAM_MIME_TYPE}; charset=utf-8", *args, **kwargs
        )


class TurboStreamStreamingResponse(TurboStreamResponseMixin, StreamingHttpResponse):
    """Handles turbo-stream streaming responses. Generator should yield individual
    turbo-stream tags.

    For example:

    .. code-block:: python

        def render():

            for i in range(3):

                yield render_turbo_stream(
                    "OK",
                    Action.REPLACE,
                    target=f"item-{i}"
                )

        return TurboStreamStreamingResponse(render())
    """


class TurboStreamResponse(TurboStreamResponseMixin, HttpResponse):
    """Basic turbo-stream response.

    If action and target are provided, will automatically wrap the
    response in <turbo-stream> tags. Otherwise you should provide the
    turbo-stream content string yourself (using e.g. *render_turbo_stream*)
    or an iterable of turbo-streams.
    """

    def __init__(
        self,
        content: Union[Iterable[str], str] = "",
        *,
        action: Optional[Action] = None,
        target: Optional[str] = None,
        is_safe: bool = False,
        renderer: Optional[BaseRenderer] = None,
        **response_kwargs,
    ):
        if action and target and isinstance(content, str):
            content = render_turbo_stream(
                action, target, content, is_safe=is_safe, renderer=renderer
            )
        super().__init__(content, **response_kwargs)


class TurboStreamTemplateResponse(TurboStreamResponseMixin, TemplateResponse):
    """Handles turbo-stream template response.

    Adds the following variables to the template:

    - **is_turbo_stream**
    - **turbo_stream_action**
    - **turbo_stream_target**

    """

    is_turbo_stream = True

    def __init__(
        self,
        request: HttpRequest,
        template: Union[str, Iterable[str]],
        context: Optional[Dict[str, Any]] = None,
        *,
        action: Action,
        target: str,
        renderer: Optional[BaseRenderer] = None,
        **kwargs,
    ):

        super().__init__(
            request,
            template,
            {
                **(context or {}),
                "turbo_stream_action": action.value,
                "turbo_stream_target": target,
                "is_turbo_stream": True,
            },
            **kwargs,
        )

        self._target = target
        self._action = action
        self._renderer = renderer

    @property
    def rendered_content(self) -> str:
        return render_turbo_stream(
            action=self._action,
            target=self._target,
            content=super().rendered_content,
            renderer=self._renderer,
            is_safe=True,
        )


class TurboFrameResponse(HttpResponse):
    """Handles turbo-frame template response."""

    def __init__(
        self,
        content: str = "",
        *,
        dom_id: str,
        is_safe: bool = False,
        renderer: Optional[BaseRenderer] = None,
        **response_kwargs,
    ):
        super().__init__(
            render_turbo_frame(dom_id, content, is_safe=is_safe, renderer=renderer),
            **response_kwargs,
        )


class TurboFrameTemplateResponse(TemplateResponse):
    """Handles turbo-stream template response.

    Adds the following variables to the template:

    - **is_turbo_frame**
    - **turbo_frame_dom_id**

    """

    is_turbo_frame = True

    def __init__(
        self,
        request: HttpRequest,
        template: Union[str, Iterable[str]],
        context: Optional[Mapping[str, Any]] = None,
        *,
        dom_id,
        renderer: Optional[BaseRenderer] = None,
        **kwargs,
    ):

        super().__init__(
            request,
            template,
            {**(context or {}), "turbo_frame_dom_id": dom_id, "is_turbo_frame": True},
            **kwargs,
        )

        self._dom_id = dom_id
        self._renderer = renderer

    @property
    def rendered_content(self) -> str:
        return render_turbo_frame(
            self._dom_id,
            super().rendered_content,
            is_safe=True,
            renderer=self._renderer,
        )
