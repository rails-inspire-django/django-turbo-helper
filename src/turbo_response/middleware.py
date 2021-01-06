# Standard Library
from typing import Callable

# Django
from django.http import HttpRequest, HttpResponse


class TurboStreamMiddleware:
    """Adds bool attribute 'accept_turbo_stream' to request if the Turbo Stream accept header is present."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.accept_turbo_stream = "text/html; turbo-stream" in request.headers.get(
            "Accept", ""
        )
        return self.get_response(request)
