# Update Page in Real Time via Websocket

Use Websocket and Turbo Stream to update the web page in real time, without writing Javascript.

This can help render `turbo-cable-stream-source` in Django template

`<turbo-cable-stream-source>` is a custom element provided by [turbo-rails](https://github.com/hotwired/turbo-rails/blob/097d8f90cf0c5ed24ac6b1a49cead73d49fa8ab5/app/javascript/turbo/cable_stream_source_element.js), with it, we can send Turbo Stream over the websocket connection and update the page in real time.

To import `turbo-cable-stream-source` element to the frontend, there are two ways:

```html
<script type="module">
  import 'https://cdn.jsdelivr.net/npm/@hotwired/turbo-rails@7.3.0/+esm'
</script>
```

Or you can [Jump start frontend project bundled by Webpack](https://github.com/AccordBox/python-webpack-boilerplate#jump-start-frontend-project-bundled-by-webpack) and install it via `npm install`

After frontend work is done, to support Actioncable on the server, please install [django-actioncable](https://github.com/AccordBox/django-actioncable).

In `routing.py`, register `TurboStreamCableChannel`

```python
from actioncable import cable_channel_register
from turbo_helper.cable_channel import TurboStreamCableChannel

cable_channel_register(TurboStreamCableChannel)
```

In Django template, we can subscribe to stream source like this:

```html
{% load turbo_helper %}

{% turbo_stream_from 'chat' view.kwargs.chat_pk %}
```

`turbo_stream_from` can accept multiple positional arguments

Then in Python code, we can send Turbo Stream to the stream source like this

```python
from turbo_helper.channel_helper import broadcast_render_to

broadcast_render_to(
    "chat",
    instance.chat_id,
    template="message_append.turbo_stream.html",
    context={
        "instance": instance,
    },
)
```

1. `arguments` **should** match the arguments passed in the `turbo_stream_from` tag.
2. `keyword arguments` `template` and `context` are used to render the template.

The web page can be updated in real time, through Turbo Stream over Websocket.
