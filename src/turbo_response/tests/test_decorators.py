# Standard Library
import http

# Django
from django.http import HttpResponse

# Django Turbo Response
from turbo_response import (
    TurboStream,
    TurboStreamResponse,
    TurboStreamStreamingResponse,
)
from turbo_response.decorators import turbo_stream_response


class TestTurboStreamResponse:
    def test_view_returns_response(self, rf):
        req = rf.get("/")

        @turbo_stream_response
        def my_view(req):
            return HttpResponse("OK")

        resp = my_view(req)
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert resp.status_code == http.HTTPStatus.OK

    def test_view_returns_string(self, rf):
        req = rf.get("/")

        @turbo_stream_response
        def my_view(req):
            return TurboStream("messages").replace.render("hello")

        resp = my_view(req)

        assert resp.status_code == http.HTTPStatus.OK
        assert isinstance(resp, TurboStreamResponse)
        assert resp["Content-Type"] == "text/vnd.turbo-stream.html; charset=utf-8"
        assert 'target="messages"' in str(resp.content)

    def test_view_returns_list(self, rf):
        req = rf.get("/")

        @turbo_stream_response
        def my_view(req):
            return [
                TurboStream("messages").replace.render("hello"),
                TurboStream("header").replace.render("world"),
            ]

        resp = my_view(req)

        assert isinstance(resp, TurboStreamResponse)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/vnd.turbo-stream.html; charset=utf-8"
        assert 'target="messages"' in str(resp.content)
        assert 'target="header"' in str(resp.content)

    def test_view_returns_generator(self, rf):
        req = rf.get("/")

        @turbo_stream_response
        def my_view(req):
            yield TurboStream("messages").replace.render("hello")
            yield TurboStream("header").replace.render("world")

        resp = my_view(req)

        assert isinstance(resp, TurboStreamStreamingResponse)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/vnd.turbo-stream.html; charset=utf-8"
        items = list(resp.streaming_content)
        assert len(items) == 2
        assert 'target="messages"' in str(items[0])
        assert 'target="header"' in str(items[1])
