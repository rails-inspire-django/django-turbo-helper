import http

from django.http import HttpRequest

from turbo_helper import TurboStream


class TestTurboStream:
    def test_render(self):
        s = TurboStream("my-form").append.render("OK")
        assert (
            s
            == '<turbo-stream action="append" target="my-form"><template>OK</template></turbo-stream>'
        )

    def test_render_multiple(self):
        s = TurboStream(".my-forms", is_multiple=True).append.render("OK")
        assert (
            s
            == '<turbo-stream action="append" targets=".my-forms"><template>OK</template></turbo-stream>'
        )

    def test_render_xss(self):
        s = TurboStream("my-form").append.render("<script></script>")
        assert (
            s
            == '<turbo-stream action="append" target="my-form"><template>&lt;script&gt;&lt;/script&gt;</template></turbo-stream>'
        )

    def test_render_is_safe(self):
        s = TurboStream("my-form").append.render("<script></script>", is_safe=True)
        assert (
            s
            == '<turbo-stream action="append" target="my-form"><template><script></script></template></turbo-stream>'
        )

    def test_template(self):
        s = (
            TurboStream("my-form")
            .append.template("simple.html", {"msg": "my content"})
            .render()
        )
        assert "my content" in s
        assert '<turbo-stream action="append" target="my-form">' in s

    def test_template_csrf(self):
        s = (
            TurboStream("my-form")
            .append.template("csrf.html", {"msg": "my content"}, request=HttpRequest())
            .render()
        )
        assert "my content" in s
        assert '<input type="hidden" name="csrfmiddlewaretoken"' in s
        assert '<turbo-stream action="append" target="my-form">' in s

    def test_template_multiple(self):
        s = (
            TurboStream(".my-forms", is_multiple=True)
            .append.template("simple.html", {"msg": "my content"})
            .render()
        )
        assert "my content" in s
        assert '<turbo-stream action="append" targets=".my-forms">' in s

    def test_template_xss(self):
        s = (
            TurboStream("my-form")
            .append.template("simple.html", {"msg": "<script></script>"})
            .render()
        )
        assert "&lt;script&gt;&lt;/script&gt;" in s
        assert '<turbo-stream action="append" target="my-form">' in s

    def test_template_with_req_init(self, rf):
        s = (
            TurboStream("my-form")
            .append.template("simple.html", {"msg": "my content"}, request=rf.get("/"))
            .render()
        )
        assert "my content" in s
        assert '<turbo-stream action="append" target="my-form">' in s

    def test_template_with_req_arg(self, rf):
        s = (
            TurboStream("my-form")
            .append.template("simple.html", {"msg": "my content"})
            .render(request=rf.get("/"))
        )
        assert "my content" in s
        assert '<turbo-stream action="append" target="my-form">' in s

    def test_response(self):
        resp = TurboStream("my-form").append.response("OK")
        assert resp.status_code == http.HTTPStatus.OK
        assert b"OK" in resp.content
        assert b'<turbo-stream action="append" target="my-form"' in resp.content

    def test_response_xss(self):
        resp = TurboStream("my-form").append.response("<script></script>")
        assert resp.status_code == http.HTTPStatus.OK
        assert b"&lt;script&gt;&lt;/script&gt;" in resp.content
        assert b'<turbo-stream action="append" target="my-form"' in resp.content

    def test_response_is_safe(self):
        resp = TurboStream("my-form").append.response("<script></script>", is_safe=True)
        assert resp.status_code == http.HTTPStatus.OK
        assert b"<script></script>" in resp.content
        assert b'<turbo-stream action="append" target="my-form"' in resp.content

    def test_template_response_req_init(self, rf):
        req = rf.get("/")
        resp = (
            TurboStream("my-form")
            .append.template("simple.html", {"msg": "my content"}, request=req)
            .response()
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert "is_turbo_stream" in resp.context_data
        assert resp._request == req
        content = resp.render().content
        assert b"my content" in content
        assert b'<turbo-stream action="append" target="my-form"' in content

    def test_template_response(self, rf):
        req = rf.get("/")
        resp = (
            TurboStream("my-form")
            .append.template("simple.html", {"msg": "my content"})
            .response(req)
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert "is_turbo_stream" in resp.context_data
        assert resp._request == req
        content = resp.render().content
        assert b"<div>my content</div>" in content
        assert b'<turbo-stream action="append" target="my-form"' in content
