# Standard Library
import functools
from typing import Callable, Generator

# Django
from django.http import HttpRequest, HttpResponse

# Local
from .response import TurboStreamResponse, TurboStreamStreamingResponse


def turbo_stream_response(view: Callable) -> Callable:
    @functools.wraps(view)
    def wrapper(request: HttpRequest, *args, **kwargs):
        response = view(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            return response
        if isinstance(response, Generator):
            return TurboStreamStreamingResponse(response)
        if isinstance(response, str):
            response = list(response)
        return TurboStreamResponse(response)

    return wrapper
