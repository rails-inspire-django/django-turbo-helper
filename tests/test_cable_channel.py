import pytest
from actioncable import ActionCableConsumer, cable_channel_register, compact_encode_json
from actioncable.utils import async_cable_broadcast
from channels.testing import WebsocketCommunicator

from turbo_helper.cable_channel import TurboStreamCableChannel
from turbo_helper.channel_helper import generate_signed_stream_key

# register the TurboStreamCableChannel
cable_channel_register(TurboStreamCableChannel)


@pytest.mark.asyncio
async def test_subscribe():
    communicator = WebsocketCommunicator(
        ActionCableConsumer.as_asgi(), "/cable", subprotocols=["actioncable-v1-json"]
    )
    connected, subprotocol = await communicator.connect(timeout=10)
    assert connected
    response = await communicator.receive_json_from()
    assert response == {"type": "welcome"}

    # Subscribe
    group_name = "test"
    subscribe_command = {
        "command": "subscribe",
        "identifier": compact_encode_json(
            {
                "channel": TurboStreamCableChannel.__name__,
                "signed_stream_name": generate_signed_stream_key(group_name),
            }
        ),
    }

    await communicator.send_to(text_data=compact_encode_json(subscribe_command))
    response = await communicator.receive_json_from(timeout=10)
    assert response["type"] == "confirm_subscription"

    # Message
    await async_cable_broadcast(group_name, "html_snippet")

    response = await communicator.receive_json_from(timeout=5)
    assert response["message"] == "html_snippet"

    # Unsubscribe
    group_name = "test"
    subscribe_command = {
        "command": "unsubscribe",
        "identifier": compact_encode_json(
            {
                "channel": TurboStreamCableChannel.__name__,
                "signed_stream_name": generate_signed_stream_key(group_name),
            }
        ),
    }

    await communicator.send_to(text_data=compact_encode_json(subscribe_command))

    # Message
    await async_cable_broadcast(group_name, "html_snippet")

    assert await communicator.receive_nothing() is True

    # Close
    await communicator.disconnect()
