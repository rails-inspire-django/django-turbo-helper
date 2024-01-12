import http

import pytest

from turbo_helper.shortcuts import redirect_303

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
