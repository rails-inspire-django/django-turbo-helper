# Django Turbo Response
# Django
from django import forms

from turbo_response.views import (
    TurboStreamFormView,
    TurboStreamTemplateView,
    TurboStreamView,
)


class MyForm(forms.Form):
    description = forms.CharField()


class TestTurboStreamView:
    def test_get(self, rf):
        class MyView(TurboStreamView):
            def get_response_content(self):
                return "hello"

        req = rf.get("/")
        resp = MyView.as_view(
            turbo_stream_target="test", turbo_stream_action="replace"
        )(req)
        assert resp.status_code == 200
        assert "text/html; turbo-stream;" in resp["Content-Type"]
        assert resp.content.startswith(
            b'<turbo-stream action="replace" target="test"><template>hello'
        )


class TestTurboStreamTemplateView:
    def test_get(self, rf):
        class MyView(TurboStreamTemplateView):
            template_name = "simple.html"

        req = rf.get("/")
        resp = MyView.as_view(
            turbo_stream_target="test", turbo_stream_action="replace"
        )(req)

        assert resp.status_code == 200
        assert "text/html; turbo-stream;" in resp["Content-Type"]
        assert "is_turbo_stream" in resp.context_data
        assert resp.template_name == ["simple.html"]
        assert resp.render().content.startswith(
            b'<turbo-stream action="replace" target="test"><template><div>my content'
        )


class TestTurboStreamFormView:
    class MyView(TurboStreamFormView):
        form_class = MyForm
        template_name = "my_form.html"
        turbo_stream_target = "my-form"
        success_url = "/done/"

    def test_get(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "is_turbo_stream" not in resp.context_data
        assert "form" in resp.context_data
        assert resp.template_name == ["my_form.html"]

    def test_post_with_validation_errors(self, rf):
        req = rf.post("/", {})
        resp = self.MyView.as_view()(req)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        assert resp.context_data["is_turbo_stream"]
        assert resp.context_data["turbo_stream_action"] == "replace"
        assert resp.context_data["turbo_stream_target"] == "my-form"
        assert resp.template_name == ["_my_form.html"]
        assert resp.render().content.startswith(b"<turbo-stream")

    def test_post_success(self, rf):
        req = rf.post("/", {"description": "ok"})
        resp = self.MyView.as_view()(req)
        assert resp.url == "/done/"
