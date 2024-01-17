# Extend Turbo Stream

## Simple Example

You can extend Turbo Stream Action by `register_turbo_stream_action` decorator.

```python
from turbo_helper import (
  register_turbo_stream_action,
  turbo_stream,
)


# register toast action
@register_turbo_stream_action("toast")
def toast(target, content=None, **kwargs):
  position = kwargs.get('position', 'left')
  return turbo_stream.action(
    "toast", target=target, message=kwargs['message'], position=position
  )


turbo_stream.toast("dom_id", message="hello world", position="right")
# <turbo-stream action="toast" target="dom_id" message="hello world" position="right">
```

Or you can render it in template:

```django
{% load turbo_helper %}

{% turbo_stream "toast" "target" message="Hello Word" position="right" %}{% endturbo_stream %}
```

Next, you can update your frontend code to make it work with new `action`

[https://turbo.hotwired.dev/handbook/streams#custom-actions](https://turbo.hotwired.dev/handbook/streams#custom-actions)

## Ecosystem

There are some good projects on GitHub that can save our time:

1. [https://github.com/marcoroth/turbo_power](https://github.com/marcoroth/turbo_power)
2. [https://github.com/hopsoft/turbo_boost-streams](https://github.com/hopsoft/turbo_boost-streams)

For example, to add css class to a DOM element, we can use

```python
turbo_stream.add_css_class(
  targets="#element", classes="container text-center"
)
```

and it can generate HTML snippet like this

```html
<turbo-stream targets="#element" action="add_css_class" classes="container text-center"><template></template></turbo-stream>
```

And registering the action handler on the frontend side, we can add css class on server side, without writing Javascript code.

Now "django-turbo-helper" already contains some `turbo_power` actions, please check the source code and test cases for more details.

| Turbo Power Actions |
|---------------------|
| graft               |
| morph               |
| add_css_class       |
| dispatch_event      |
| notification        |
| redirect_to         |
| turbo_frame_reload  |
| turbo_frame_set_src |
