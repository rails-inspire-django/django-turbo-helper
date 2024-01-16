import pytest
from django.template import Context, Template

from tests.testapp.models import TodoItem
from turbo_helper import register_turbo_stream_action, turbo_stream
from turbo_helper.templatetags.turbo_helper import dom_id

pytestmark = pytest.mark.django_db


def render(template, context):
    return Template(template).render(Context(context))


class TestDomId:
    def test_instance(self, todo):
        result = dom_id(todo)
        assert "todoitem_1" == result

        setattr(todo, "to_key", "test_1")  # noqa: B010
        result = dom_id(todo)
        assert "todoitem_test_1" == result

    def test_model(self):
        result = dom_id(TodoItem)
        assert "new_todoitem" == result

    def test_string(self):
        result = dom_id("test")
        assert "test" == result

    def test_prefix(self, todo):
        result = dom_id(todo, "test")
        assert "test_todoitem_1" == result


class TestFrame:
    def test_string(self):
        template = """
        {% load turbo_helper %}

        {% turbo_frame "test" %}Loading...{% endturbo_frame %}
        """
        output = render(template, {}).strip()
        assert output == '<turbo-frame id="test">Loading...</turbo-frame>'

    def test_dom_id_variable(self):
        template = """
        {% load turbo_helper %}

        {% turbo_frame dom_id %}Loading...{% endturbo_frame %}
        """
        output = render(template, {"dom_id": "test"}).strip()
        assert output == '<turbo-frame id="test">Loading...</turbo-frame>'

    def test_src(self):
        template = """
        {% load turbo_helper %}

        {% turbo_frame dom_id src=src %}Loading...{% endturbo_frame %}
        """
        output = render(
            template, {"dom_id": "test", "src": "http://localhost:8000"}
        ).strip()
        assert (
            output
            == '<turbo-frame id="test" src="http://localhost:8000">Loading...</turbo-frame>'
        )

    def test_other_attributes(self):
        template = """
        {% load turbo_helper %}

        {% turbo_frame dom_id src=src lazy="loading" %}Loading...{% endturbo_frame %}
        """
        output = render(
            template, {"dom_id": "test", "src": "http://localhost:8000"}
        ).strip()
        assert (
            output
            == '<turbo-frame id="test" src="http://localhost:8000" lazy="loading">Loading...</turbo-frame>'
        )


class TestStream:
    def test_string(self):
        template = """
        {% load turbo_helper %}

        {% turbo_stream "append" 'test' %}Test{% endturbo_stream %}
        """
        output = render(template, {}).strip()
        assert (
            output
            == '<turbo-stream action="append" target="test"><template>Test</template></turbo-stream>'
        )

    def test_dom_id_variable(self):
        template = """
        {% load turbo_helper %}

        {% turbo_stream "append" dom_id %}Test{% endturbo_stream %}
        """
        output = render(template, {"dom_id": "test"}).strip()
        assert (
            output
            == '<turbo-stream action="append" target="test"><template>Test</template></turbo-stream>'
        )

    def test_custom_register(self):
        @register_turbo_stream_action("toast")
        def toast(target, content=None, **kwargs):
            position = kwargs.get("position", "left")
            return turbo_stream.render_action(
                "toast", target=target, message=kwargs["message"], position=position
            )

        template = """
        {% load turbo_helper %}

        {% turbo_stream "toast" dom_id message="Hello Word" position="right" %}{% endturbo_stream %}
        """
        output = render(template, {"dom_id": "test"}).strip()
        assert (
            '<turbo-stream action="toast" target="test" message="Hello Word" position="right">'
            in output
        )


class TestStreamAll:
    def test_string(self):
        template = """
        {% load turbo_helper %}

        {% turbo_stream_all "remove" ".old_records" %}{% endturbo_stream_all %}
        """
        output = render(template, {}).strip()
        assert (
            output
            == '<turbo-stream action="remove" targets=".old_records"><template></template></turbo-stream>'
        )

    def test_dom_id_variable(self):
        template = """
        {% load turbo_helper %}

        {% turbo_stream_all "remove" dom_id %}{% endturbo_stream_all %}
        """
        output = render(template, {"dom_id": ".test"}).strip()
        assert (
            output
            == '<turbo-stream action="remove" targets=".test"><template></template></turbo-stream>'
        )


class TestStreamFrom:
    def test_string(self):
        template = """
        {% load turbo_helper %}

        {% turbo_stream_from "test" %}
        """
        output = render(template, {}).strip()
        assert (
            output
            == '<turbo-cable-stream-source channel="TurboStreamCableChannel" signed-stream-name="test:1DyYXz2Y_VbgIPXC1AQ0ZGHhAx71uaZ36r4DFwXDaiU"></turbo-cable-stream-source>'
        )

    def test_dom_id_variable(self):
        template = """
        {% load turbo_helper %}

        {% turbo_stream_from "test" dom_id %}
        """
        output = render(template, {"dom_id": "todo_3"}).strip()
        assert (
            output
            == '<turbo-cable-stream-source channel="TurboStreamCableChannel" signed-stream-name="test_todo_3:7ZS0MxQWhRTCAnG3olGO9AJKfvos3iaHGoBMBt8ZbSM"></turbo-cable-stream-source>'
        )
