from turbo_response import TurboFrame
from turbo_response.renderers import Jinja2


class TestTurboFrame:
    def test_render(self):
        s = TurboFrame("my-form").render("OK")
        assert s == '<turbo-frame id="my-form">OK</turbo-frame>'

    def test_render_jinja2(self):
        s = TurboFrame("my-form").render("OK", renderer=Jinja2())
        assert s == '<turbo-frame id="my-form">OK</turbo-frame>'

    def test_render_xss(self):
        s = TurboFrame("my-form").render("<script></script>")
        assert (
            s == '<turbo-frame id="my-form">&lt;script&gt;&lt;/script&gt;</turbo-frame>'
        )

    def test_render_is_safe(self):
        s = TurboFrame("my-form").render("<script></script>", is_safe=True)
        assert s == '<turbo-frame id="my-form"><script></script></turbo-frame>'

    def test_template(self):
        s = (
            TurboFrame("my-form")
            .template("simple.html", {"msg": "my content"})
            .render()
        )
        assert "my content" in s
        assert '<turbo-frame id="my-form">' in s

    def test_template_jinja2(self):
        s = (
            TurboFrame("my-form")
            .template("simple.html", {"msg": "my content"})
            .render(renderer=Jinja2())
        )
        assert "my content" in s
        assert '<turbo-frame id="my-form">' in s

    def test_response(self):
        resp = TurboFrame("my-form").response("OK")
        assert resp.status_code == 200
        assert b"OK" in resp.content
        assert b'<turbo-frame id="my-form"' in resp.content

    def test_response_jinja2(self):
        resp = TurboFrame("my-form").response("OK", renderer=Jinja2())
        assert resp.status_code == 200
        assert b"OK" in resp.content
        assert b'<turbo-frame id="my-form"' in resp.content

    def test_response_xss(self):
        resp = TurboFrame("my-form").response("<script></script>")
        assert resp.status_code == 200
        assert b"&lt;script&gt;&lt;/script&gt;" in resp.content
        assert b'<turbo-frame id="my-form"' in resp.content

    def test_response_is_safe(self):
        resp = TurboFrame("my-form").response("<script></script>", is_safe=True)
        assert resp.status_code == 200
        assert b"<script></script>" in resp.content
        assert b'<turbo-frame id="my-form"' in resp.content

    def test_template_render(self, rf):
        req = rf.get("/")
        s = (
            TurboFrame("my-form")
            .template("simple.html", {"msg": "my content"}, request=req)
            .render()
        )
        assert "my content" in s
        assert '<turbo-frame id="my-form"' in s

    def test_template_render_jinja2(self, rf):
        req = rf.get("/")
        s = (
            TurboFrame("my-form")
            .template("simple.html", {"msg": "my content"}, request=req)
            .render(renderer=Jinja2())
        )
        assert "my content" in s
        assert '<turbo-frame id="my-form"' in s

    def test_template_render_xss(self, rf):
        req = rf.get("/")
        s = (
            TurboFrame("my-form")
            .template("simple.html", {"msg": "<script></script>"}, request=req)
            .render()
        )
        assert "&lt;script&gt;&lt;/script&gt;" in s
        assert '<turbo-frame id="my-form"' in s

    def test_template_render_req_in_arg(self, rf):
        req = rf.get("/")
        s = (
            TurboFrame("my-form")
            .template("simple.html", {"msg": "my content"})
            .render(request=req)
        )
        assert "my content" in s
        assert '<turbo-frame id="my-form"' in s

    def test_template_response(self, rf):
        req = rf.get("/")
        resp = (
            TurboFrame("my-form")
            .template("simple.html", {"msg": "my content"}, request=req)
            .response()
        )
        assert resp.status_code == 200
        assert "is_turbo_frame" in resp.context_data
        assert resp._request == req
        content = resp.render().content
        assert b"my content" in content
        assert b'<turbo-frame id="my-form"' in content

    def test_template_response_jinja2(self, rf):
        req = rf.get("/")
        resp = (
            TurboFrame("my-form")
            .template("simple.html", {"msg": "my content"}, request=req)
            .response(renderer=Jinja2())
        )
        assert resp.status_code == 200
        assert "is_turbo_frame" in resp.context_data
        assert resp._request == req
        content = resp.render().content
        assert b"my content" in content
        assert b'<turbo-frame id="my-form"' in content

    def test_template_response_req_in_arg(self, rf):
        req = rf.get("/")
        resp = (
            TurboFrame("my-form")
            .template("simple.html", {"msg": "my content"})
            .response(req)
        )
        assert resp.status_code == 200
        assert "is_turbo_frame" in resp.context_data
        assert resp._request == req
        content = resp.render().content
        assert b"<div>my content</div>" in content
        assert b'<turbo-frame id="my-form"' in content
