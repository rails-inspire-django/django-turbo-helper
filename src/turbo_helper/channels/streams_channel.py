from actioncable import ActionCableConsumer, CableChannel
from django.core.signing import Signer

from .stream_name import verify_signed_stream_key

signer = Signer()


class TurboStreamCableChannel(CableChannel):
    def __init__(self, consumer: ActionCableConsumer, identifier_key, params=None):
        self.params = params if params else {}
        self.identifier_key = identifier_key
        self.consumer = consumer
        self.group_name = None

    async def subscribe(self):
        flag, stream_name = verify_signed_stream_key(self.params["signed_stream_name"])
        self.group_name = stream_name
        if flag:
            await self.consumer.subscribe_group(self.group_name, self)

    async def unsubscribe(self):
        await self.consumer.unsubscribe_group(self.group_name, self)
