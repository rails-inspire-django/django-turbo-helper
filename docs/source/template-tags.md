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