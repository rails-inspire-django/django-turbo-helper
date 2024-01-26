import unittest
from unittest import mock

import pytest

import turbo_helper.channels.broadcasts
from tests.testapp.models import TodoItem
from tests.utils import assert_dom_equal
from turbo_helper import dom_id
from turbo_helper.channels.broadcasts import (
    broadcast_action_to,
    broadcast_render_to,
    broadcast_stream_to,
)

pytestmark = pytest.mark.django_db


class TestBroadcastStreamTo:
    def test_broadcast_stream_to(self, monkeypatch):
        mock_cable_broadcast = mock.MagicMock(name="cable_broadcast")
        monkeypatch.setattr(
            turbo_helper.channels.broadcasts, "cable_broadcast", mock_cable_broadcast
        )

        ################################################################################

        broadcast_stream_to("test", content="hello world")

        mock_cable_broadcast.assert_called_with(
            group_name="test", message="hello world"
        )

        ################################################################################
        todo_item = TodoItem.objects.create(description="Test Model")

        broadcast_stream_to(todo_item, content="hello world")

        mock_cable_broadcast.assert_called_with(
            group_name=dom_id(todo_item), message="hello world"
        )

        ################################################################################
        todo_item = TodoItem.objects.create(description="Test Model")

        broadcast_stream_to(todo_item, "test", content="hello world")

        mock_cable_broadcast.assert_called_with(
            group_name=f"{dom_id(todo_item)}_test", message="hello world"
        )


class TestBroadcastActionTo:
    def test_broadcast_action_to(self, monkeypatch):
        mock_cable_broadcast = mock.MagicMock(name="cable_broadcast")
        monkeypatch.setattr(
            turbo_helper.channels.broadcasts, "cable_broadcast", mock_cable_broadcast
        )

        ################################################################################

        broadcast_action_to("tasks", action="remove", target="new_task")

        assert mock_cable_broadcast.call_args.kwargs["group_name"] == "tasks"
        assert_dom_equal(
            mock_cable_broadcast.call_args.kwargs["message"],
            '<turbo-stream action="remove" target="new_task"><template></template></turbo-stream>',
        )

        ################################################################################
        todo_item = TodoItem.objects.create(description="Test Model")

        broadcast_action_to(todo_item, action="remove", target="new_task")

        mock_cable_broadcast.assert_called_with(
            group_name=dom_id(todo_item), message=unittest.mock.ANY
        )

        ################################################################################
        todo_item = TodoItem.objects.create(description="Test Model")

        broadcast_action_to(todo_item, "test", action="remove", target="new_task")

        mock_cable_broadcast.assert_called_with(
            group_name=f"{dom_id(todo_item)}_test", message=unittest.mock.ANY
        )


class TestBroadcastRenderTo:
    def test_broadcast_render_to(self, monkeypatch):
        mock_cable_broadcast = mock.MagicMock(name="cable_broadcast")
        monkeypatch.setattr(
            turbo_helper.channels.broadcasts, "cable_broadcast", mock_cable_broadcast
        )

        ################################################################################
        todo_item = TodoItem.objects.create(description="test")

        broadcast_render_to(
            todo_item,
            template="todoitem.turbo_stream.html",
            context={
                "instance": todo_item,
            },
        )

        mock_cable_broadcast.assert_called_with(
            group_name=dom_id(todo_item), message=unittest.mock.ANY
        )

        assert_dom_equal(
            mock_cable_broadcast.call_args.kwargs["message"],
            '<turbo-stream action="append" target="todo_list"><template><div>test</div></template></turbo-stream>',
        )
