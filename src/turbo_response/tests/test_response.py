# Django Turbo Response
from turbo_response.response import TurboFrameResponse, TurboStreamResponse


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
