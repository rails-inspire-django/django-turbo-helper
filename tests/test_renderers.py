from turbo_response import Action, render_turbo_frame, render_turbo_stream


class TestRenderTurboStream:
    def test_render_empty_stream(self):
        s = render_turbo_stream(action=Action.REMOVE, target="test")
        assert (
            s
            == '<turbo-stream action="remove" target="test"><template></template></turbo-stream>'
        )

    def test_render_content(self):
        s = render_turbo_stream(
            action=Action.REPLACE,
            target="test",
            content="my content",
        )
        assert (
            s
            == '<turbo-stream action="replace" target="test"><template>my content</template></turbo-stream>'
        )

    def test_render_multiple_targets(self):
        s = render_turbo_stream(
            action=Action.REPLACE,
            target=".test",
            content="my content",
            is_multiple=True,
        )
        assert (
            s
            == '<turbo-stream action="replace" targets=".test"><template>my content</template></turbo-stream>'
        )

    def test_render_content_xss(self):
        s = render_turbo_stream(
            action=Action.REPLACE,
            target="test",
            content="<script></script>",
        )
        assert (
            s
            == '<turbo-stream action="replace" target="test"><template>&lt;script&gt;&lt;/script&gt;</template></turbo-stream>'
        )

    def test_render_content_is_safe(self):
        s = render_turbo_stream(
            action=Action.REPLACE,
            target="test",
            content="<script></script>",
            is_safe=True,
        )
        assert (
            s
            == '<turbo-stream action="replace" target="test"><template><script></script></template></turbo-stream>'
        )


class TestRenderTurboFrame:
    def test_render_empty_frame(self):
        s = render_turbo_frame("test")
        assert s == '<turbo-frame id="test"></turbo-frame>'

    def test_render_content(self):
        s = render_turbo_frame(
            dom_id="test",
            content="my content",
        )
        assert s == '<turbo-frame id="test">my content</turbo-frame>'

    def test_render_xss(self):
        s = render_turbo_frame(
            dom_id="test",
            content="<script></script>",
        )
        assert s == '<turbo-frame id="test">&lt;script&gt;&lt;/script&gt;</turbo-frame>'

    def test_render_content_is_safe(self):
        s = render_turbo_frame(
            dom_id="test",
            content="<script></script>",
            is_safe=True,
        )
        assert s == '<turbo-frame id="test"><script></script></turbo-frame>'
