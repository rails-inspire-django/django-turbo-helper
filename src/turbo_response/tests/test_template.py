# Django Turbo Response
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
