# Turbo Frame

This tag can help us generate `turbo-frame` element in Django template.

```html
{% load turbo_helper %}

{% url 'message-create' as src %}
{% turbo_frame "message_create" src=src %}
  Loading...
{% endturbo_frame %}
```

or you can use it with the powerful `dom_id` tag.

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
