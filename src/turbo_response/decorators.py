import functools
from typing import Callable, Generator

from django.http import HttpRequest, HttpResponse

from .response import TurboStreamResponse, TurboStreamStreamingResponse


def turbo_stream_response(view: Callable) -> Callable:
    @functools.wraps(view)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = view(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            return response
        if isinstance(response, Generator):
            return TurboStreamStreamingResponse(response)
        if isinstance(response, str):
            response = list(response)
        return TurboStreamResponse(response)

    return wrapper
