import http

import pytest

from turbo_helper.shortcuts import redirect_303, respond_to

pytestmark = pytest.mark.django_db


class TestRedirect303:
    def test_plain_url(self):
        resp = redirect_303("/")
        assert resp.status_code == http.HTTPStatus.SEE_OTHER
        assert resp.url == "/"

    def test_view_name(self):
        resp = redirect_303("index")
        assert resp.status_code == http.HTTPStatus.SEE_OTHER
        assert resp.url == "/"

    def test_model(self, todo):
        resp = redirect_303(todo)
        assert resp.status_code == http.HTTPStatus.SEE_OTHER
        assert resp.url == f"/todos/{todo.id}/"


class TestResponseTo:
    def test_response_to(self, rf):
        req = rf.get("/", HTTP_ACCEPT="*/*")
        with respond_to(req) as resp:
            """
            wildcard only work for HTML
            """
            assert resp.html
            assert not resp.turbo_stream
            assert not resp.json

        req = rf.get("/", HTTP_ACCEPT="text/vnd.turbo-stream.html")
        with respond_to(req) as resp:
            assert resp.turbo_stream
            assert not resp.html
            assert not resp.json

        req = rf.get(
            "/", HTTP_ACCEPT="text/html; charset=utf-8, application/json; q=0.9"
        )
        with respond_to(req) as resp:
            assert not resp.turbo_stream
            assert resp.html
            assert resp.json

        req = rf.get(
            "/",
            HTTP_ACCEPT="text/vnd.turbo-stream.html, text/html, application/xhtml+xml",
        )
        with respond_to(req) as resp:
            assert resp.turbo_stream
            assert resp.html
            assert not resp.json
