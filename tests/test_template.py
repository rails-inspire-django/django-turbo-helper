from django.http import HttpRequest

from turbo_response import (
    Action,
    render_turbo_frame_template,
    render_turbo_stream_template,
)


class TestRenderTurboStreamTemplate:
    def test_render(self):
        s = render_turbo_stream_template(
            "simple.html", {"msg": "my content"}, action=Action.UPDATE, target="test"
        ).strip()
        assert (
            s
            == '<turbo-stream action="update" target="test"><template><div>my content</div></template></turbo-stream>'
        )

    def test_render_with_csrf(self):
        s = render_turbo_stream_template(
            "csrf.html",
            {"msg": "my content"},
            action=Action.UPDATE,
            target="test",
            request=HttpRequest(),
        ).strip()
        assert '<input type="hidden" name="csrfmiddlewaretoken"' in s
        assert "my content" in s

    def test_multiple(self):
        s = render_turbo_stream_template(
            "simple.html",
            {"msg": "my content"},
            action=Action.UPDATE,
            target=".tests",
            is_multiple=True,
        ).strip()
        assert (
            s
            == '<turbo-stream action="update" targets=".tests"><template><div>my content</div></template></turbo-stream>'
        )

    def test_render_with_xss(self):
        s = render_turbo_stream_template(
            "simple.html",
            {"msg": "<script></script>"},
            action=Action.UPDATE,
            target="test",
        ).strip()
        assert (
            s
            == '<turbo-stream action="update" target="test"><template><div>&lt;script&gt;&lt;/script&gt;</div></template></turbo-stream>'
        )


class TestRenderTurboTemplate:
    def test_render(self):
        s = render_turbo_frame_template(
            "simple.html", {"msg": "my content"}, dom_id="test"
        )
        assert s == '<turbo-frame id="test"><div>my content</div></turbo-frame>'

    def test_render_with_xss(self):
        s = render_turbo_frame_template(
            "simple.html", {"msg": "<script></script>"}, dom_id="test"
        )
        assert (
            s
            == '<turbo-frame id="test"><div>&lt;script&gt;&lt;/script&gt;</div></turbo-frame>'
        )
