# Django
# Standard Library
from typing import Any, Dict, Iterable, Union

from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from django.template.response import TemplateResponse

# Local
from .renderers import Action, render_turbo_frame, render_turbo_stream


class TurboStreamResponseMixin:
    """Automatically sets the correct turbo-stream content type."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            content_type="text/html; turbo-stream; charset=utf-8", *args, **kwargs
        )


class TurboStreamStreamingResponse(TurboStreamResponseMixin, StreamingHttpResponse):
    """Handles turbo-stream responses. Generator should yield individual
    turbo-stream strings."""


class TurboStreamResponse(TurboStreamResponseMixin, HttpResponse):
    """Basic turbo-stream response."""

    def __init__(self, content: str = "", *, action: Action, target: str, **kwargs):
        super().__init__(
            render_turbo_stream(action, target, content), **kwargs,
        )


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
        context: Dict[str, Any],
        *,
        action: Action,
        target: str,
        **kwargs
    ):

        super().__init__(
            request,
            template,
            {
                **context,
                "turbo_stream_action": action.value,
                "turbo_stream_target": target,
                "is_turbo_stream": True,
            },
            **kwargs,
        )

        self._target = target
        self._action = action

    @property
    def rendered_content(self) -> str:
        return render_turbo_stream(
            action=self._action, target=self._target, content=super().rendered_content
        )


class TurboFrameResponse(HttpResponse):
    """Handles turbo-frame template response."""

    def __init__(self, content: str = "", *, dom_id: str, **kwargs):
        super().__init__(
            render_turbo_frame(dom_id, content), **kwargs,
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
        context: Dict[str, Any],
        *,
        dom_id,
        **kwargs
    ):

        super().__init__(
            request,
            template,
            {**context, "turbo_frame_dom_id": dom_id, "is_turbo_frame": True},
            **kwargs,
        )

        self._dom_id = dom_id

    @property
    def rendered_content(self) -> str:
        return render_turbo_frame(self._dom_id, super().rendered_content)
