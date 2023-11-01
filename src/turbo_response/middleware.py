from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.utils.functional import SimpleLazyObject

from .constants import TURBO_STREAM_MIME_TYPE


class TurboData:
    def __init__(self, request: HttpRequest):
        self.has_turbo_header = TURBO_STREAM_MIME_TYPE in request.headers.get(
            "Accept", ""
        )
        self.frame = request.headers.get("Turbo-Frame", None)

    def __bool__(self):
        return self.has_turbo_header


class TurboMiddleware:
    """Adds `turbo` attribute to request:
    1. `request.turbo` : True if request contains turbo header
    2. `request.turbo.frame`: DOM ID of requested Turbo-Frame (or None)
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.turbo = SimpleLazyObject(lambda: TurboData(request))
        return self.get_response(request)
