import pytest
from django.template import Context, Template

from tests.testapp.models import TodoItem
from turbo_response.templatetags.turbo_helper import dom_id

pytestmark = pytest.mark.django_db


def render(template, context):
    return Template(template).render(Context(context))


class TestDomId:
    def test_instance(self, todo):
        result = dom_id(todo)
        assert "todoitem_1" == result

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
