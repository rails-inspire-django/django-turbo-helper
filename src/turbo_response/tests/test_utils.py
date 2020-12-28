# Third Party Libraries
import pytest

# Django Turbo Response
from turbo_response.exceptions import InvalidTurboFrame, InvalidTurboStream
from turbo_response.utils import (
    render_turbo_frame,
    render_turbo_stream,
    validate_turbo_frame,
    validate_turbo_stream,
)


class TestValidateTurboStream:
    def test_not_acceptable_action(self):
        with pytest.raises(InvalidTurboStream):
            validate_turbo_stream(action="invalid", target="test")

    def test_action_is_none(self):
        with pytest.raises(InvalidTurboStream):
            validate_turbo_stream(action=None, target="test")

    def test_target_is_none(self):
        with pytest.raises(InvalidTurboStream):
            validate_turbo_stream(action="replace", target=None)

    def test_is_valid(self):
        validate_turbo_stream(action="replace", target="test")


class TestValidateTurboFrame:
    def test_missing_dom_id(self):
        with pytest.raises(InvalidTurboFrame):
            validate_turbo_frame(dom_id=None)

    def test_is_valid(self):
        validate_turbo_frame(dom_id="test")


class TestRenderTurboStream:
    def test_invalid(self):
        with pytest.raises(InvalidTurboStream):
            render_turbo_stream(action="invalid", target="test")

    def test_render_empty_stream(self):
        s = render_turbo_stream(action="remove", target="test")
        assert (
            s
            == '<turbo-stream action="remove" target="test"><template></template></turbo-stream>'
        )

    def test_render_content(self):
        s = render_turbo_stream(
            action="remove", target="test", content="<div>my content</div>",
        )
        assert (
            s
            == '<turbo-stream action="remove" target="test"><template><div>my content</div></template></turbo-stream>'
        )


class TestRenderTurboFrame:
    def test_invalid(self):
        with pytest.raises(InvalidTurboFrame):
            render_turbo_frame(dom_id=None)

    def test_render_empty_frame(self):
        s = render_turbo_frame("test")
        assert s == '<turbo-frame id="test"></turbo-frame>'

    def test_render_content(self):
        s = render_turbo_frame(dom_id="test", content="<div>my content</div>",)
        assert s == '<turbo-frame id="test"><div>my content</div></turbo-frame>'
