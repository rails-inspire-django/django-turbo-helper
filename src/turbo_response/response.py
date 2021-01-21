# Standard Library
from typing import Any, Dict, Iterable, Optional, Union

# Django
from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from django.template.response import TemplateResponse

# Local
from .constants import TURBO_STREAM_MIME_TYPE, Action
from .renderers import render_turbo_frame, render_turbo_stream


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


class TurboStreamIterableResponse(TurboStreamResponseMixin, HttpResponse):
    """Handles turbo-stream iterator responses. Each item should be wrapped in
    turbo-stream tags.

    For example:

    .. code-block:: python

        return TurboStreamIterableResponse(
            [
                render_turbo_stream(
                    "OK",
                    Action.REPLACE,
                    target=f"item-{i}"
                ) for i in range(3)
            ]
        )
    """


class TurboStreamResponse(TurboStreamResponseMixin, HttpResponse):
    """Basic turbo-stream response.
    You can pass in a single text value which will be wrapped in a turbo-stream tag.

    """

    def __init__(self, content: str = "", *, action: Action, target: str, **kwargs):
        super().__init__(
            render_turbo_stream(action, target, content),
            **kwargs,
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
        **kwargs,
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
            render_turbo_frame(dom_id, content),
            **kwargs,
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
        context: Optional[Dict[str, Any]] = None,
        *,
        dom_id,
        **kwargs,
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
