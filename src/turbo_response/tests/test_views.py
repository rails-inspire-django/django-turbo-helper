# Django Turbo Response
from turbo_response.views import TurboStreamTemplateView, TurboStreamView


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
            template_name = "_include.html"

        req = rf.get("/")
        resp = MyView.as_view(
            turbo_stream_target="test", turbo_stream_action="replace"
        )(req)

        assert resp.status_code == 200
        assert "text/html; turbo-stream;" in resp["Content-Type"]
        assert "is_turbo_stream" in resp.context_data
        assert resp.template_name == ["_include.html"]
        assert resp.render().content.startswith(
            b'<turbo-stream action="replace" target="test"><template><div>hello'
        )
