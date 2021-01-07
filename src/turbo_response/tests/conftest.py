# Third Party Libraries
import pytest

# Django Turbo Response
from turbo_response.tests.testapp.models import TodoItem


@pytest.fixture
def todo():
    return TodoItem.objects.create(description="test")
