## turbo_refreshes_with

This template tag generates HTML meta tags for Turbo Drive to control the refresh method and scroll behavior in Turbo 8.0+ ([currently in beta](https://github.com/hotwired/turbo/releases/tag/v8.0.0-beta.4)).

### Parameters

- `method` (optional, default: `'replace'`): Specifies the refresh method. Must be one of `'replace'` or `'morph'`.
- `scroll` (optional, default: `'reset'`): Specifies the scroll behavior. Must be one of `'reset'` or `'preserve'`.

### Behavior

This tag creates HTML meta tags defining the Turbo Frames' refresh method and scroll behavior based on the provided parameters. If the provided parameters are not within the valid options, a `ValidationError` is raised.

### Example Usage

```django
{% load turbo_helper %}

<!-- Generate Turbo Frames refresh meta tags -->
{% turbo_refreshes_with method='replace' scroll='reset' %}
```
