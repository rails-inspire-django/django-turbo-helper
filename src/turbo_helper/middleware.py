import http
import threading
from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.utils.functional import SimpleLazyObject

from .constants import TURBO_STREAM_MIME_TYPE

_thread_locals = threading.local()


def get_current_request():
    return getattr(_thread_locals, "request", None)


def set_current_request(request):
    setattr(_thread_locals, "request", request)  # noqa: B010


class SetCurrentRequest:
    """
    Can let developer access Django request from anywhere

    https://github.com/zsoldosp/django-currentuser
    https://stackoverflow.com/questions/4716330/accessing-the-users-request-in-a-post-save-signal
    """

    def __init__(self, request):
        self.request = request

    def __enter__(self):
        set_current_request(self.request)

    def __exit__(self, exc_type, exc_value, traceback):
        # cleanup
        set_current_request(None)


class TurboData:
    def __init__(self, request: HttpRequest):
        # be careful about the */* from browser
        self.accept_turbo_stream = TURBO_STREAM_MIME_TYPE in request.headers.get(
            "Accept", ""
        )
        self.frame = request.headers.get("Turbo-Frame", None)
        self.request_id = request.headers.get("X-Turbo-Request-Id", None)

    def __bool__(self):
        """
        TODO: Deprecate
        """
        return self.accept_turbo_stream


class TurboMiddleware:
    """
    Task 1: Adds `turbo` attribute to request:
    1. `request.turbo` : True if request contains turbo header
    2. `request.turbo.frame`: DOM ID of requested Turbo-Frame (or None)

    Task 2: Auto change status code for Turbo Drive
    https://turbo.hotwired.dev/handbook/drive#redirecting-after-a-form-submission
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        with SetCurrentRequest(request):
            request.turbo = SimpleLazyObject(lambda: TurboData(request))

            response = self.get_response(request)

            if (
                request.method == "POST"
                and request.headers.get("X-Turbo-Request-Id")
                and response.get("Content-Type") != "text/vnd.turbo-stream.html"
            ):
                if response.status_code == http.HTTPStatus.OK:
                    response.status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY

                if response.status_code in (
                    http.HTTPStatus.MOVED_PERMANENTLY,
                    http.HTTPStatus.FOUND,
                ):
                    response.status_code = http.HTTPStatus.SEE_OTHER

        return response
