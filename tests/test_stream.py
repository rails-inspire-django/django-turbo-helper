from django.http import HttpRequest
from django.utils.safestring import mark_safe

from turbo_helper import (
    TURBO_STREAM_CONTENT_TYPE,
    register_turbo_stream_action,
    turbo_stream,
)


class TestTurboStream:
    def test_render(self):
        s = turbo_stream.append("dom_id", "OK")
        assert (
            s
            == '<turbo-stream action="append" target="dom_id"><template>OK</template></turbo-stream>'
        )

    def test_render_escape_behavior(self):
        s = turbo_stream.append("dom_id", "<script></script>")
        assert (
            s
            == '<turbo-stream action="append" target="dom_id"><template>&lt;script&gt;&lt;/script&gt;</template></turbo-stream>'
        )

        s = turbo_stream.append("dom_id", mark_safe("<script></script>"))
        assert (
            s
            == '<turbo-stream action="append" target="dom_id"><template><script></script></template></turbo-stream>'
        )

    def test_template(self):
        s = turbo_stream.append(
            "dom_id", template="simple.html", context={"msg": "my content"}
        )
        assert "my content" in s
        assert '<turbo-stream action="append" target="dom_id">' in s

    def test_template_csrf(self):
        s = turbo_stream.append(
            "dom_id",
            template="csrf.html",
            context={"msg": "my content"},
            request=HttpRequest(),
        )

        assert "my content" in s
        assert '<input type="hidden" name="csrfmiddlewaretoken"' in s
        assert '<turbo-stream action="append" target="dom_id">' in s

    def test_template_with_req_arg(self, rf):
        s = turbo_stream.append(
            "dom_id",
            template="simple.html",
            context={"msg": "my content"},
            request=rf.get("/"),
        )
        assert "my content" in s
        assert '<turbo-stream action="append" target="dom_id">' in s

    def test_template_multiple_targets(self):
        s = turbo_stream.append_all(
            ".old_records", template="simple.html", context={"msg": "my content"}
        )
        assert "my content" in s
        assert '<turbo-stream action="append" targets=".old_records">' in s

    def test_custom_register(self):
        # register toast action
        @register_turbo_stream_action("toast")
        def toast(target, message, position="left"):
            return turbo_stream.render_action(
                "toast", target=target, data_message=message, data_position=position
            )

        s = turbo_stream.toast("dom_id", message="hello world", position="right")
        assert (
            '<turbo-stream action="toast" target="dom_id" data-message="hello world" data-position="right">'
            in s
        )

        # test attributes escape
        s = turbo_stream.toast("dom_id", message='hello "world"', position="right")
        assert "hello &quot;world&quot;" in s

    def test_response(self, rf):
        response = turbo_stream.response(
            [
                turbo_stream.append("dom_id", "OK"),
                turbo_stream.append(
                    "dom_id_2",
                    template="simple.html",
                    context={"msg": "my content"},
                    request=rf.get("/"),
                ),
            ]
        )

        assert response.headers["content-type"] == TURBO_STREAM_CONTENT_TYPE

        assert (
            '<turbo-stream action="append" target="dom_id"><template>OK</template></turbo-stream>'
            in response.content.decode("utf-8")
        )

        assert "my content" in response.content.decode("utf-8")
        assert (
            '<turbo-stream action="append" target="dom_id_2">'
            in response.content.decode("utf-8")
        )
