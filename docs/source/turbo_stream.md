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
turbo_stream.append(
  "dom_id",
  template="simple.html",
  context={"msg": "my content"},
  request=request
)
```

Notes:

1. `request`, `context` are optional
2. If `content` is not set, then `template` is required to render the `content`.

Turbo Stream built-in actions are all supported in syntax `turbo_stream.xxx`:

- append
- prepend
- replace
- update
- remove
- before
- after
- morph

### TurboStreamResponse

In Django view, we should use `TurboStreamResponse` to wrap Turbo Stream elements so the client can recognize it.

```python
from turbo_helper import TurboStreamResponse

# render multiple turbo stream elements in one response
return TurboStreamResponse([
  turbo_stream.append(
    "message",
    template="message.html",
    context={"msg": "my content"},
    request=request
  ),
  turbo_stream.update(
    "form",
    template="form.html",
    context={"form": form},
    request=request
  ),
])
```

Or cleaner way:

```python
from turbo_helper import turbo_stream

# render multiple turbo stream elements in one response
return turbo_stream.response([
  turbo_stream.append(
    "message",
    template="message.html",
    context={"msg": "my content"},
    request=request
  ),
  turbo_stream.update(
    "form",
    template="form.html",
    context={"form": form},
    request=request
  ),
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
