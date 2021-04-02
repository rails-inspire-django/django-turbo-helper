# Django
from django.http import HttpResponse

# Third Party Libraries
import pytest

# Django Turbo Response
from turbo_response.middleware import TurboMiddleware


@pytest.fixture
def get_response():
    return lambda req: HttpResponse()


class TestTurboMiddeware:
    def test_accept_header_not_found(self, rf, get_response):
        req = rf.get("/", HTTP_ACCEPT="text/html")
        TurboMiddleware(get_response)(req)
        assert not req.turbo
        assert req.turbo.frame is None

    def test_accept_header_found(self, rf, get_response):
        req = rf.get("/", HTTP_ACCEPT="text/vnd.turbo-stream.html")
        TurboMiddleware(get_response)(req)
        assert req.turbo
        assert req.turbo.frame is None

    def test_turbo_frame(self, rf, get_response):
        req = rf.get(
            "/",
            HTTP_ACCEPT="text/vnd.turbo-stream.html",
            HTTP_TURBO_FRAME="my-playlist",
        )
        TurboMiddleware(get_response)(req)
        assert req.turbo
        assert req.turbo.frame == "my-playlist"
