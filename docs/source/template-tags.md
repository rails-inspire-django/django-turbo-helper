# Template Tags

Generate `turbo-frame` and `turbo-stream` from Django template is now the **recommended** way since it is more clean and easy to understand.

## dom_id

`dom_id` is a helper method that returns a unique DOM ID based on the object's class name and ID

```html
{% load turbo_helper %}

{% dom_id instance %}               ->  task_1
{% dom_id instance 'detail' %}      ->  detail_task_1
{% dom_id Task %}                   ->  new_task
```

1. `dom_id` first argument can be string, instance or Model class
2. `dom_id` second argument is optional string that will be used as `prefix`.
3. The `dom_id` can help make the id generation behavior consistent across the project, and save our time to update it in `turbo-stream` or `turbo-frame` element.
4. You can also use it in your Django view code.

## turbo_frame

This tag can help us generate `turbo-frame` element in Django template.

```html
{% load turbo_helper %}

{% url 'message-create' as src %}
{% turbo_frame "message_create" src=src %}
  Loading...
{% endturbo_frame %}
```

or you can use it with `dom_id`

```html
{% load turbo_helper %}

{% dom_id instance 'detail' as dom_id %}
{% turbo_frame dom_id class="flex-1" %}
  {% include 'components/detail.html' %}
{% endturbo_frame %}
```

Notes:

1. First argument is `turbo frame id`
2. Other arguments can be passed as `key=value` pairs

## turbo_stream

This tag can help us generate `turbo-stream` element in Django template.

```html
{% load turbo_helper %}

{% turbo_stream 'append' 'messages' %}
  {% include 'core/components/message.html' %}
{% endturbo_stream %}

{% turbo_stream 'update' 'new_task' %}
  {% include 'components/create.html' %}
{% endturbo_stream %}
```

Notes:

1. First argument is `turbo stream action`
2. Second argument is `turbo stream target`
3. Other arguments can be passed as `key=value` pairs
4. We can generate **multiple**  turbo stream elements in one template and render it in one response, and update multiple part of the page in one response.

You can return Turbo Stream resposne in Django view like this:

```python
from turbo_response.response import TurboStreamResponse
from django.template.loader import render_to_string

context = {}
html = render_to_string(
    "partial/task_list.turbo_stream.html",
    context,
    request=self.request,
)
return TurboStreamResponse(html)
```

The code in Django view would be much cleaner and easier to maintain.

## turbo_stream_from

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
from turbo_response.cable_channel import TurboStreamCableChannel

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
from turbo_response.channel_helper import broadcast_render_to

broadcast_render_to(
    ["chat", instance.chat_id],
    template="message_append.turbo_stream.html",
    context={
        "instance": instance,
    },
)
```

The `["chat", instance.chat_id]` **should** match the positional arguments in the `turbo_stream_from` tag.

The web page can be updated in real time, through Turbo Stream over Websocket.
