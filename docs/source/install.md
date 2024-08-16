# Installation

```{note}
This package does not include any Javascript library, you may wish to add these yourself using your preferred Javascript build tool, or use a CDN.

Please check <a href="https://turbo.hotwired.dev/handbook/installing" target="_blank">Hotwire Doc</a> for more details
```

## Requirements

This library requires Python 3.8+ and Django 3.2+.

## Getting Started

```shell
$ pip install django-turbo-helper
```

Next update **INSTALLED_APPS**:

```python
INSTALLED_APPS = [
  "turbo_helper",
  ...
]
```

## Middleware

Add `turbo_helper.middleware.TurboMiddleware` to the `MIDDLEWARE` in Django settings file.

```python
MIDDLEWARE = [
    ...
    "turbo_helper.middleware.TurboMiddleware",   # new
    ...
]
```

With the `TurboMiddleware` we have `request.turbo` object which we can access in Django view or template. It will also help us to change the response status code to `422` if the POST request come from Turbo and the form validation failed.

If the request originates from a turbo-frame, we can get the value from the `request.turbo.frame`

```django
{% load turbo_helper %}

{% if request.turbo.frame %}

  {% turbo_frame request.turbo.frame %}
    {% include 'template.html' %}
  {% endturbo_frame %}

{% endif %}
```

Or we can use `request.turbo.accept_turbo_stream` to check if the request accepts turbo stream response.

```python
if request.turbo.accept_turbo_stream:
  # return turbo stream response
else:
  # return normal HTTP response
```
