# Django Turbo Response
from turbo_response import TurboStream


class TestTurboStream:
    def test_render(self):
        s = TurboStream("my-form").append.render("OK")
        assert (
            s
            == '<turbo-stream action="append" target="my-form"><template>OK</template></turbo-stream>'
        )

    def test_template(self):
        s = TurboStream("my-form").append.template("simple.html", {}).render()
        assert "my content" in s
        assert '<turbo-stream action="append" target="my-form">' in s

    def test_template_with_req_init(self, rf):
        s = (
            TurboStream("my-form")
            .append.template("simple.html", {}, request=rf.get("/"))
            .render()
        )
        assert "my content" in s
        assert '<turbo-stream action="append" target="my-form">' in s

    def test_template_with_req_arg(self, rf):
        s = (
            TurboStream("my-form")
            .append.template("simple.html", {})
            .render(request=rf.get("/"))
        )
        assert "my content" in s
        assert '<turbo-stream action="append" target="my-form">' in s

    def test_response(self):
        resp = TurboStream("my-form").append.response("OK")
        assert resp.status_code == 200
        assert b"OK" in resp.content
        assert b'<turbo-stream action="append" target="my-form"' in resp.content

    def test_template_response_req_init(self, rf):
        req = rf.get("/")
        resp = (
            TurboStream("my-form")
            .append.template("simple.html", {}, request=req)
            .response()
        )
        assert resp.status_code == 200
        assert "is_turbo_stream" in resp.context_data
        assert resp._request == req
        content = resp.render().content
        assert b"my content" in content
        assert b'<turbo-stream action="append" target="my-form"' in content

    def test_template_response(self, rf):
        req = rf.get("/")
        resp = TurboStream("my-form").append.template("simple.html", {}).response(req)
        assert resp.status_code == 200
        assert "is_turbo_stream" in resp.context_data
        assert resp._request == req
        content = resp.render().content
        assert b"my content" in content
        assert b'<turbo-stream action="append" target="my-form"' in content
