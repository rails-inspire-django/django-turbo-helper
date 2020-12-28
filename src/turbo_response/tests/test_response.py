# Django Turbo Response
from turbo_response.response import (
    TurboFrameResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)


class TestTurboStreamResponse:
    def test_render(self):
        resp = TurboStreamResponse("OK", action="remove", target="test")
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        assert resp.content.startswith(
            b'<turbo-stream action="remove" target="test"><template>OK'
        )


class TestTurboFrameResponse:
    def test_render(self):
        resp = TurboFrameResponse("OK", dom_id="test")
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert resp.content.startswith(b'<turbo-frame id="test">OK')


class TestTurboStreamTemplateResponse:
    def test_render(self, rf):
        req = rf.get("/")
        resp = TurboStreamTemplateResponse(
            req, "simple.html", {"testvar": 1}, action="update", target="test"
        )
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        assert resp.context_data["is_turbo_stream"]
        assert resp.context_data["turbo_stream_action"] == "update"
        assert resp.context_data["turbo_stream_target"] == "test"
        assert resp.context_data["testvar"] == 1
        content = resp.render().content
        assert content.startswith(b'<turbo-stream action="update" target="test"')
        assert b"my content" in content
