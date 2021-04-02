import http

from django import forms
from django.views.generic import CreateView

import pytest

from turbo_response import Action
from turbo_response.mixins import TurboFormAdapterMixin
from turbo_response.renderers import Jinja2
from turbo_response.tests.testapp.forms import TodoForm
from turbo_response.tests.testapp.models import TodoItem
from turbo_response.views import (
    TurboCreateView,
    TurboFormView,
    TurboFrameTemplateView,
    TurboFrameView,
    TurboStreamCreateView,
    TurboStreamDeleteView,
    TurboStreamFormView,
    TurboStreamTemplateView,
    TurboStreamUpdateView,
    TurboStreamView,
    TurboUpdateView,
)

pytestmark = pytest.mark.django_db


class MyForm(forms.Form):
    description = forms.CharField()


class TestTurboFormAdapterView:
    """Adapt an existing view without touching internals"""

    class MyView(TurboFormAdapterMixin, CreateView):
        form_class = TodoForm
        model = TodoItem
        success_url = "/done/"

    def test_get(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "form" in resp.context_data
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_get_with_explicit_target(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "form" in resp.context_data
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_post_with_validation_errors(self, rf):
        req = rf.post("/", {})
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_post_success(self, rf):
        req = rf.post("/", {"description": "ok"})
        resp = self.MyView.as_view()(req)
        assert resp.url == "/done/"
        assert resp.status_code == http.HTTPStatus.SEE_OTHER
        assert TodoItem.objects.count() == 1


class TestTurboStreamView:
    def test_get(self, rf):
        class MyView(TurboStreamView):
            def get_response_content(self):
                return "hello"

        req = rf.get("/")
        resp = MyView.as_view(
            turbo_stream_target="test", turbo_stream_action=Action.REPLACE
        )(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert "text/vnd.turbo-stream.html;" in resp["Content-Type"]
        assert resp.content.startswith(
            b'<turbo-stream action="replace" target="test"><template>hello'
        )

    def test_get_xss(self, rf):
        class MyView(TurboStreamView):
            def get_response_content(self):
                return "<script />"

        req = rf.get("/")
        resp = MyView.as_view(
            turbo_stream_target="test", turbo_stream_action=Action.REPLACE
        )(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert "text/vnd.turbo-stream.html;" in resp["Content-Type"]
        assert resp.content.startswith(
            b'<turbo-stream action="replace" target="test"><template>&lt;script /&gt;'
        )

    def test_get_is_safe(self, rf):
        class MyView(TurboStreamView):
            def get_response_content(self):
                return "<script />"

            def render_turbo_stream(self, **kwargs):
                return super().render_turbo_stream(is_safe=True, **kwargs)

        req = rf.get("/")
        resp = MyView.as_view(
            turbo_stream_target="test", turbo_stream_action=Action.REPLACE
        )(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert "text/vnd.turbo-stream.html;" in resp["Content-Type"]
        assert resp.content.startswith(
            b'<turbo-stream action="replace" target="test"><template><script />'
        )


class TestTurboStreamTemplateView:
    def test_get(self, rf):
        class MyView(TurboStreamTemplateView):
            template_name = "simple.html"

            def get_context_data(self, **kwargs):
                return {**kwargs, "msg": "my content"}

        req = rf.get("/")
        resp = MyView.as_view(
            turbo_stream_target="test", turbo_stream_action=Action.REPLACE
        )(req)

        assert resp.status_code == http.HTTPStatus.OK
        assert "text/vnd.turbo-stream.html;" in resp["Content-Type"]
        assert "is_turbo_stream" in resp.context_data
        assert resp.template_name == ["simple.html"]
        assert resp.render().content.startswith(
            b'<turbo-stream action="replace" target="test"><template><div>my content'
        )


class TestTurboCreateView:
    class MyView(TurboCreateView):
        form_class = TodoForm
        model = TodoItem
        success_url = "/done/"

    def test_get(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "form" in resp.context_data
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_get_with_explicit_target(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "form" in resp.context_data
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_post_with_validation_errors(self, rf):
        req = rf.post("/", {})
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_post_success(self, rf):
        req = rf.post("/", {"description": "ok"})
        resp = self.MyView.as_view()(req)
        assert resp.url == "/done/"
        assert resp.status_code == http.HTTPStatus.SEE_OTHER
        assert TodoItem.objects.count() == 1


class TestTurboStreamCreateView:
    class MyView(TurboStreamCreateView):
        form_class = TodoForm
        model = TodoItem
        success_url = "/done/"

    def test_get(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "is_turbo_stream" not in resp.context_data
        assert "form" in resp.context_data
        assert resp.context_data["turbo_stream_target"] == "form-todoitem"
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_post_with_validation_errors(self, rf):
        req = rf.post("/", {})
        resp = self.MyView.as_view()(req)
        assert "is_turbo_stream" in resp.context_data
        assert "form" in resp.context_data
        assert resp.context_data["turbo_stream_target"] == "form-todoitem"
        assert resp.template_name == ["testapp/_todoitem_form.html"]

    def test_post_success(self, rf):
        req = rf.post("/", {"description": "ok"})
        resp = self.MyView.as_view()(req)
        assert resp.url == "/done/"
        assert resp.status_code == http.HTTPStatus.SEE_OTHER
        assert TodoItem.objects.count() == 1


class TestTurboUpdateView:
    class MyView(TurboUpdateView):
        form_class = TodoForm
        model = TodoItem
        success_url = "/done/"

    def test_get(self, rf, todo):
        req = rf.get("/")
        resp = self.MyView.as_view()(req, pk=todo.pk)
        assert resp.status_code == http.HTTPStatus.OK
        assert "form" in resp.context_data
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_post_with_validation_errors(self, rf, todo):
        req = rf.post("/", {})
        resp = self.MyView.as_view()(req, pk=todo.pk)
        assert resp.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_post_success(self, rf, todo):
        req = rf.post("/", {"description": "updated!"})
        resp = self.MyView.as_view()(req, pk=todo.pk)
        assert resp.url == "/done/"
        assert resp.status_code == http.HTTPStatus.SEE_OTHER
        todo.refresh_from_db()
        assert todo.description == "updated!"


class TestTurboStreamUpdateView:
    class MyView(TurboStreamUpdateView):
        form_class = TodoForm
        model = TodoItem
        success_url = "/done/"

    def test_get(self, rf, todo):
        req = rf.get("/")
        resp = self.MyView.as_view()(req, pk=todo.pk)
        assert resp.status_code == http.HTTPStatus.OK
        assert "is_turbo_stream" not in resp.context_data
        assert "form" in resp.context_data
        assert resp.context_data["turbo_stream_target"] == f"form-todoitem-{todo.pk}"
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_post_with_validation_errors(self, rf, todo):
        req = rf.post("/", {})
        resp = self.MyView.as_view()(req, pk=todo.pk)
        assert "is_turbo_stream" in resp.context_data
        assert resp.context_data["turbo_stream_target"] == f"form-todoitem-{todo.pk}"
        assert resp.template_name == ["testapp/_todoitem_form.html"]

    def test_post_success(self, rf, todo):
        req = rf.post("/", {"description": "updated!"})
        resp = self.MyView.as_view()(req, pk=todo.pk)
        assert resp.url == "/done/"
        assert resp.status_code == http.HTTPStatus.SEE_OTHER
        todo.refresh_from_db()
        assert todo.description == "updated!"


class TestTurboFormView:
    class MyView(TurboFormView):
        form_class = MyForm
        template_name = "my_form.html"
        success_url = "/done/"

    def test_get(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "form" in resp.context_data
        assert resp.template_name == ["my_form.html"]

    def test_post_with_validation_errors(self, rf):
        req = rf.post("/", {})
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
        assert resp.template_name == ["my_form.html"]

    def test_post_success(self, rf):
        req = rf.post("/", {"description": "ok"})
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.SEE_OTHER
        assert resp.url == "/done/"


class TestTurboStreamFormView:
    class MyView(TurboStreamFormView):
        form_class = MyForm
        template_name = "my_form.html"
        success_url = "/done/"
        turbo_stream_target = "my-form"

    def test_get(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "form" in resp.context_data
        assert "is_turbo_stream" not in resp.context_data
        assert resp.context_data["turbo_stream_target"] == "my-form"
        assert resp.template_name == ["my_form.html"]

    def test_post_with_validation_errors(self, rf):
        req = rf.post("/", {})
        resp = self.MyView.as_view()(req)
        assert "is_turbo_stream" in resp.context_data
        assert resp.context_data["turbo_stream_target"] == "my-form"
        assert resp.template_name == ["_my_form.html"]

    def test_post_success(self, rf):
        req = rf.post("/", {"description": "ok"})
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.SEE_OTHER
        assert resp.url == "/done/"


class TestTurboStreamDeleteView:
    class MyView(TurboStreamDeleteView):
        template_name = "simple.html"
        model = TodoItem

    def test_post(self, rf, todo):
        req = rf.post("/")
        resp = self.MyView.as_view()(req, pk=todo.pk)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/vnd.turbo-stream.html; charset=utf-8"
        assert f'target="todoitem-{todo.pk}"' in str(resp.content)
        assert TodoItem.objects.count() == 0


class TestTurboFrameView:
    def test_get(self, rf):
        class MyView(TurboFrameView):
            turbo_frame_dom_id = "test"

            def get_response_content(self):
                return "done"

        req = rf.get("/")
        resp = MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert resp.content == b'<turbo-frame id="test">done</turbo-frame>'

    def test_get_jinja2(self, rf):
        class MyView(TurboFrameView):
            turbo_frame_dom_id = "test"

            def get_response_content(self):
                return "done"

            def render_turbo_frame(self):
                return super().render_turbo_frame(renderer=Jinja2())

        req = rf.get("/")
        resp = MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert resp.content == b'<turbo-frame id="test">done</turbo-frame>'

    def test_get_xss(self, rf):
        class MyView(TurboFrameView):
            turbo_frame_dom_id = "test"

            def get_response_content(self):
                return "<script />"

        req = rf.get("/")
        resp = MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert resp.content == b'<turbo-frame id="test">&lt;script /&gt;</turbo-frame>'

    def test_get_is_safe(self, rf):
        class MyView(TurboFrameView):
            turbo_frame_dom_id = "test"

            def get_response_content(self):
                return "<script />"

            def render_turbo_frame(self):
                return super().render_turbo_frame(is_safe=True)

        req = rf.get("/")
        resp = MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert resp.content == b'<turbo-frame id="test"><script /></turbo-frame>'


class TestTurboFrameTemplateView:
    class MyView(TurboFrameTemplateView):
        turbo_frame_dom_id = "test"
        template_name = "simple.html"

        def get_context_data(self, **kwargs):
            return {**kwargs, "msg": "my content"}

    def test_get(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert resp.render().content.startswith(
            b'<turbo-frame id="test"><div>my content</div>'
        )
