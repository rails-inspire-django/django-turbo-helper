# Standard Library
import http

# Django
from django import forms

# Third Party Libraries
import pytest

# Django Turbo Response
from turbo_response.shortcuts import redirect_303, render_form_response

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


class TestRenderFormResponse:
    class MyForm(forms.Form):
        comment = forms.CharField()

    def test_render_turbo_stream_no_errors(self, rf):
        req = rf.get("/")
        form = self.MyForm()
        resp = render_form_response(
            req,
            form,
            "my_form.html",
            turbo_stream_target="my-form",
            turbo_stream_template="_my_form.html",
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.context_data["form"] == form
        assert resp.context_data["turbo_stream_target"] == "my-form"

    def test_render_turbo_stream_errors(self, rf):
        req = rf.get("/")
        form = self.MyForm({})
        # missing comment, should be error
        assert not form.is_valid()
        assert form.errors
        resp = render_form_response(
            req,
            form,
            "my_form.html",
            turbo_stream_target="my-form",
            turbo_stream_template="_my_form.html",
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.context_data["form"] == form
        assert resp.context_data["turbo_stream_target"] == "my-form"

    def test_render_no_errors(self, rf):
        req = rf.get("/")
        form = self.MyForm()
        resp = render_form_response(req, form, "my_form.html")
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.context_data["form"] == form

    def test_render_errors(self, rf):
        req = rf.get("/")
        form = self.MyForm({})
        # missing comment, should be error
        assert not form.is_valid()
        assert form.errors
        resp = render_form_response(req, form, "my_form.html")
        assert resp.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
        assert resp.context_data["form"] == form
