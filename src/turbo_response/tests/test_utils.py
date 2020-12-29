# Django Turbo Response
from turbo_response.utils import (
    Action,
    render_turbo_frame,
    render_turbo_frame_template,
    render_turbo_stream,
    render_turbo_stream_template,
)


class TestRenderTurboStream:
    def test_render_empty_stream(self):
        s = render_turbo_stream(action=Action.REMOVE, target="test")
        assert (
            s
            == '<turbo-stream action="remove" target="test"><template></template></turbo-stream>'
        )

    def test_render_content(self):
        s = render_turbo_stream(
            action=Action.REPLACE, target="test", content="<div>my content</div>",
        )
        assert (
            s
            == '<turbo-stream action="replace" target="test"><template><div>my content</div></template></turbo-stream>'
        )


class TestRenderTurboFrame:
    def test_render_empty_frame(self):
        s = render_turbo_frame("test")
        assert s == '<turbo-frame id="test"></turbo-frame>'

    def test_render_content(self):
        s = render_turbo_frame(dom_id="test", content="<div>my content</div>",)
        assert s == '<turbo-frame id="test"><div>my content</div></turbo-frame>'


class TestRenderTurboStreamTemplate:
    def test_render(self):
        s = render_turbo_stream_template(
            "simple.html", {}, action=Action.UPDATE, target="test"
        )
        assert (
            s
            == '<turbo-stream action="update" target="test"><template><div>my content</div></template></turbo-stream>'
        )


class TestRenderTurboTemplate:
    def test_render(self):
        s = render_turbo_frame_template("simple.html", {}, dom_id="test")
        assert s == '<turbo-frame id="test"><div>my content</div></turbo-frame>'
