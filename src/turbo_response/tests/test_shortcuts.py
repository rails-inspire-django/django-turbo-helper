# Django Turbo Response
from turbo_response.shortcuts import TurboStream


class TestTurboStream:
    def test_render(self):
        s = TurboStream("my-form").append.render("OK")
        assert (
            s
            == '<turbo-stream action="append" target="my-form"><template>OK</template></turbo-stream>'
        )

    def test_str(self):
        s = str(TurboStream("my-form").remove)
        assert (
            s
            == '<turbo-stream action="remove" target="my-form"><template></template></turbo-stream>'
        )
