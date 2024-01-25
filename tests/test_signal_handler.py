import pytest

from tests.testapp.models import TodoItem
from turbo_helper.signals import (
    after_create_commit,
    after_delete_commit,
    after_update_commit,
)

pytestmark = pytest.mark.django_db


class TestSignalHandler:
    def test_after_create_commit_signal_handler(self):
        handler_called_1 = False

        def handler_func_1(sender, instance, created, **kwargs):
            nonlocal handler_called_1
            handler_called_1 = True

        handler_called_2 = False

        def handler_func_2(sender, instance, created, **kwargs):
            nonlocal handler_called_2
            handler_called_2 = True

        decorated_handler = after_create_commit(sender=TodoItem)(  # noqa: F841
            handler_func_1
        )
        decorated_handler_2 = after_create_commit(sender=TodoItem)(  # noqa: F841
            handler_func_2
        )

        TodoItem.objects.create(description="Test Model")

        assert handler_called_1
        assert handler_called_2

    def test_after_update_commit_signal_handler(self):
        handler_called_1 = False

        def handler_func_1(sender, instance, created, **kwargs):
            nonlocal handler_called_1
            handler_called_1 = True

        handler_called_2 = False

        def handler_func_2(sender, instance, created, **kwargs):
            nonlocal handler_called_2
            handler_called_2 = True

        decorated_handler = after_update_commit(sender=TodoItem)(  # noqa: F841
            handler_func_1
        )
        decorated_handler_2 = after_update_commit(sender=TodoItem)(  # noqa: F841
            handler_func_2
        )

        todo_item = TodoItem.objects.create(description="Test Model")
        todo_item.description = "test"
        todo_item.save()

        assert handler_called_1
        assert handler_called_2

    def test_after_delete_commit_signal_handler(self):
        handler_called_1 = False

        def handler_func_1(sender, instance, **kwargs):
            nonlocal handler_called_1
            handler_called_1 = True

        handler_called_2 = False

        def handler_func_2(sender, instance, **kwargs):
            nonlocal handler_called_2
            handler_called_2 = True

        decorated_handler = after_delete_commit(sender=TodoItem)(  # noqa: F841
            handler_func_1
        )
        decorated_handler_2 = after_delete_commit(sender=TodoItem)(  # noqa: F841
            handler_func_2
        )

        todo_item = TodoItem.objects.create(description="Test Model")
        todo_item.delete()

        assert handler_called_1
        assert handler_called_2
