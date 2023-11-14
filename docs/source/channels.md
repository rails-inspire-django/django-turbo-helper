# Django-Channels

```{warning}
This approach is not recommended anymore, please consider using [turbo_stream_from](./template-tags.md#turbo-stream-from) instead.
```

This library can also be used with [django-channels](https://channels.readthedocs.io/en/stable/). As with multiple streams, you can use the **TurboStream** class to broadcast turbo-stream content from your consumers.

```python
from turbo_response import render_turbo_stream, render_turbo_stream_template
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def chat_message(self, event):

        # DB methods omitted for brevity
        message = await self.get_message(event["message"]["id"])
        num_unread_messages = await self.get_num_unread_messages()

        if message:
            await self.send(
                TurboStream("unread_message_counter")
                .replace.render(str(num_unread_messages))
            )

            await self.send(
                TurboStream("messages").append.template(
                  "chat/_message.html",
                  {"message": message, "user": self.scope['user']},
                ).render()
            )
```

See the django-channels documentation for more details on setting up ASGI and channels. Note that you will need to set up your WebSockets in the client, for example in a Stimulus controller:

```javascript
import { Controller } from 'stimulus';
import { connectStreamSource, disconnectStreamSource } from '@hotwired/turbo';

export default class extends Controller {
  static values = {
    socketUrl: String,
  };

  connect() {
    this.source = new WebSocket(this.socketUrlValue);
    connectStreamSource(this.source);
  }

  disconnect() {
    if (this.source) {
      disconnectStreamSource(this.source);
      this.source.close();
      this.source = null;
    }
  }
}
```
