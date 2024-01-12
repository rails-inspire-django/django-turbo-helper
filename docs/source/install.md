# Installation

**`django-turbo-response` has been renamed to `django-turbo-helper`, please update your requirements and update imports from `turbo_response` to `turbo_helper`.**

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

**Note**: This install does not include any client libraries (e.g. Turbo or Stimulus). You may wish to add these yourself using your preferred Javascript build tool, or use a CDN. Please refer to the Hotwire documentation on installing these libraries.

## Middleware

You can optionally install `turbo_helper.middleware.TurboMiddleware`. This adds the attribute `turbo` to your `request` if the Turbo client adds `Accept: text/vnd.turbo-stream.html;` to the header:

```python
MIDDLEWARE = [
    ...
    "turbo_helper.middleware.TurboMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...
]
```

This is useful if you want to check if a stream is requested, so you can optionally return a stream or a normal response:

```python
if request.turbo:
    # return Turbo Stream
else:
    # return normal response
```

If the request originates from a turbo-frame it will also set the `frame` property:

```python
if request.turbo.frame == "my-playlist":
    pass
```
