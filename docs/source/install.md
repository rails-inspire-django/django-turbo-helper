# Installation

```{note}
This package does not include any Javascript library, you may wish to add these yourself using your preferred Javascript build tool, or use a CDN.

Please check <a href="https://turbo.hotwired.dev/handbook/installing" target="_blank">Hotwire Doc</a>
```

## Requirements

This library requires Python 3.8+ and Django 3.2+.

## Getting Started

```shell
pip install django-turbo-helper
```

Next update **INSTALLED_APPS**:

```python
INSTALLED_APPS = [
  "turbo_helper",
  ...
]
```

## Middleware

You can optionally install `turbo_helper.middleware.TurboMiddleware`. This adds the attribute `turbo` to your `request`.

```python
MIDDLEWARE = [
    ...
    "turbo_helper.middleware.TurboMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...
]
```

If the request originates from a turbo-frame, we can get the value from the `request.turbo.frame`

```django
{% turbo_frame request.turbo.frame %}
  {% include 'template.html' %}
{% endturbo_frame %}
```
