# Standard Library
import http

# Third Party Libraries
import pytest

# Django Turbo Response
from turbo_response.redirects import HttpResponseSeeOther, redirect_303

pytestmark = pytest.mark.django_db


class TestHttpResponseSeeOther:
    def test_instance(self):
        resp = HttpResponseSeeOther("/")
        assert resp.url == "/"
        assert resp.status_code == http.HTTPStatus.SEE_OTHER


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
