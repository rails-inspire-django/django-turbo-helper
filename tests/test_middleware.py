import http

import pytest
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)

from turbo_helper.middleware import TurboMiddleware
from turbo_helper.response import TurboStreamResponse


@pytest.fixture
def get_response():
    return lambda req: HttpResponse()


class TestTurboMiddleware:
    def test_accept_header_not_found(self, rf, get_response):
        headers = {
            "ACCEPT": "text/html",
        }
        headers = {f"HTTP_{key.upper()}": value for key, value in headers.items()}
        req = rf.get("/", **headers)
        TurboMiddleware(get_response)(req)
        assert not req.turbo
        assert req.turbo.frame is None

    def test_accept_header_found(self, rf, get_response):
        headers = {
            "ACCEPT": "text/vnd.turbo-stream.html",
        }
        headers = {f"HTTP_{key.upper()}": value for key, value in headers.items()}
        req = rf.get("/", **headers)
        TurboMiddleware(get_response)(req)
        assert req.turbo
        assert req.turbo.frame is None

    def test_turbo_frame(self, rf, get_response):
        headers = {
            "ACCEPT": "text/vnd.turbo-stream.html",
            "TURBO_FRAME": "my-playlist",
        }
        headers = {
            f"HTTP_{key.upper()}": value for key, value in headers.items()
        }  # Add "HTTP_" prefix
        req = rf.get("/", **headers)
        TurboMiddleware(get_response)(req)
        assert req.turbo
        assert req.turbo.frame == "my-playlist"


class TestTurboMiddlewareAutoChangeStatusCode:
    def test_post_failed_form_submission(self, rf):
        headers = {
            "ACCEPT": "text/vnd.turbo-stream.html",
            "X-Turbo-Request-Id": "d4165765-488b-41a0-82b6-39126c40e3e0",
        }
        headers = {
            f"HTTP_{key.upper()}": value for key, value in headers.items()
        }  # Add "HTTP_" prefix
        req = rf.post("/", **headers)

        def form_submission(request):
            # in Django, failed form submission will return 200
            return HttpResponse()

        resp = TurboMiddleware(form_submission)(req)

        assert resp.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize(
        "response_class", [HttpResponseRedirect, HttpResponsePermanentRedirect]
    )
    def test_post_succeed_form_submission(self, rf, response_class):
        headers = {
            "ACCEPT": "text/vnd.turbo-stream.html",
            "X-Turbo-Request-Id": "d4165765-488b-41a0-82b6-39126c40e3e0",
        }
        headers = {
            f"HTTP_{key.upper()}": value for key, value in headers.items()
        }  # Add "HTTP_" prefix
        req = rf.post("/", **headers)

        def form_submission(request):
            # in Django, failed form submission will return 301, 302
            return response_class("/success/")

        resp = TurboMiddleware(form_submission)(req)

        assert resp.status_code == http.HTTPStatus.SEE_OTHER

    def test_post_turbo_stream(self, rf, get_response):
        """
        Do not change if response is TurboStreamResponse
        """
        headers = {
            "ACCEPT": "text/vnd.turbo-stream.html",
            "X-Turbo-Request-Id": "d4165765-488b-41a0-82b6-39126c40e3e0",
        }
        headers = {
            f"HTTP_{key.upper()}": value for key, value in headers.items()
        }  # Add "HTTP_" prefix
        req = rf.post("/", **headers)

        def form_submission(request):
            return TurboStreamResponse()

        resp = TurboMiddleware(form_submission)(req)
        assert resp.status_code == http.HTTPStatus.OK
