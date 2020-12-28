# Django
from django.http import HttpResponse, StreamingHttpResponse
from django.template.response import TemplateResponse

# Local
from .utils import (
    render_turbo_frame,
    render_turbo_stream,
    validate_turbo_frame,
    validate_turbo_stream,
)


class TurboStreamResponseMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(content_type="text/html; turbo-stream;", *args, **kwargs)


class TurboStreamStreamingResponse(TurboStreamResponseMixin, StreamingHttpResponse):
    ...


class TurboStreamResponse(TurboStreamResponseMixin, HttpResponse):
    def __init__(self, action, target, *args, **kwargs):
        super().__init__(
            render_turbo_stream(action, target), *args, **kwargs,
        )


class TurboStreamTemplateResponse(TurboStreamResponseMixin, TemplateResponse):
    def __init__(self, request, template, context, *, action, target, **kwargs):

        validate_turbo_stream(action, target)

        super().__init__(
            request,
            template,
            context
            | {
                "turbo_stream_target": target,
                "turbo_stream_action": action,
                "is_turbo_stream": True,
            },
            **kwargs,
        )

        self._target = target
        self._action = action

    @property
    def rendered_content(self):
        return render_turbo_stream(
            action=self._action, target=self._target, content=super().rendered_content
        )


class TurboFrameTemplateResponse(TemplateResponse):
    def __init__(self, request, template, context, dom_id, **kwargs):

        validate_turbo_frame(dom_id)

        super().__init__(
            request,
            template,
            context | {"turbo_frame_dom_id": dom_id, "is_turbo_frame": True},
            **kwargs,
        )

        self._dom_id = dom_id

    @property
    def rendered_content(self):
        return render_turbo_frame(self._dom_id, super().rendered_content)
