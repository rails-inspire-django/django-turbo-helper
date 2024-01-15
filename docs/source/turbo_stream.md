# Turbo Stream

## Render from Django View

```python
from turbo_helper import (
    turbo_stream,
)

# simple example
turbo_stream.append("dom_id", "OK")
turbo_stream.append("dom_id", content="OK")

# template example
turbo_stream.append("dom_id", template="simple.html", context={"msg": "my content"}, request=request)
```

Turbo Stream built-in actions are supported in syntax `turbo_stream.xxx`:

- append
- prepend
- replace
- update
- remove
- before
- after

### TurboStreamResponse

In Django view, we should use `TurboStreamResponse` to wrap Turbo Stream elements so the client can recognize it.

```python
from turbo_helper import TurboStreamResponse

# render multiple turbo stream elements in one response
return TurboStreamResponse([
  turbo_stream.append("message", template="message.html", context={"msg": "my content"}, request=request),
  turbo_stream.update("form", template="form.html", context={"form": form}, request=request),
])
```

Or cleaner way:

```python
from turbo_helper import turbo_stream

# render multiple turbo stream elements in one response
return turbo_stream.response([
  turbo_stream.append("message", template="message.html", context={"msg": "my content"}, request=request),
  turbo_stream.update("form", template="form.html", context={"form": form}, request=request),
])
```

## Render from Django Template

`turbo_stream` can help us generate `turbo-stream` element in Django template.

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

## Extend Turbo Stream Action

You can extend Turbo Stream Action by `register_turbo_stream_action` decorator.

```python
from turbo_helper import (
    register_turbo_stream_action,
    turbo_stream,
)

# register toast action
@register_turbo_stream_action("toast")
def toast(target, message, position="left"):
  return turbo_stream.render_action(
    "toast", target=target, data_message=message, data_position=position
  )


turbo_stream.toast("dom_id", message="hello world", position="right")
# <turbo-stream action="toast" target="dom_id" data-message="hello world" data-position="right">
```

## Targeting Multiple Elements

To target multiple elements with a single action, use the `targets` attribute with a CSS query selector instead of the `target` attribute

```python
turbo_stream.append_all(
  ".old_records", template="simple.html", context={"msg": "my content"}
)

# <turbo-stream action="append" targets=".old_records">
```

Or template tag

```django
{% turbo_stream_all "remove" ".old_records" %}{% endturbo_stream_all %}
```
