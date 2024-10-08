# Changelog

## [2.1.4]

1. Automatically change the status code in the middleware to 422 for failed form submissions requested by Turbo.
2. Add doc about `django-lifecycle` package.
3. Add doc about `morph` method in Turbo Stream.

## [2.1.3]

1. Work with `Turbo 8 morph-refreshes`
2. Add decorator `after_create_commit, after_update_commit, after_destroy_commit`.
3. Add `broadcast_action_to`, `broadcast_refresh_to` to broadcast action to the channels.

## [2.1.2]

1. Update to work with django-actioncable>=1.0.4
2. Support part of [turbo_power](https://github.com/marcoroth/turbo_power) turbo stream actions.
3. Update multi-format response solution.

## [2.1.0]

**Breaking Change**

1. Refactored the whole project and the way to render Turbo Frame and Turbo Stream.
2. Please check the documentation to see how to use the new API.

## [2.0.1]

1. Update doc config
2. Update `pyproject.toml`

## [2.0.0]

1. Rename from `turbo_response` to `turbo_helper`
2. Make `dom_id` respect `to_key` method just like Rails
3. Add `response_format` so developer can return different response format in clean way.

## [1.0.3]

1. Add `turbo_stream_from` tag and make it work with [django-actioncable](https://github.com/AccordBox/django-actioncable)

## [1.0.2]

1. Import `dom_id`, `turbo_frame`, `turbo_stream` template tags.

## [0.0.52] - 2021-9-6

Support multiple targets

## [0.0.51] - 2021-8-20

TurboCreateView/TurboUpdateView inheritance fix

## [0.0.50] - 2021-7-5

Add BEFORE and AFTER actions

## [0.0.49] - 2021-5-12

Use format_html for rendering

## [0.0.48] - 2021-4-9

Add support for Django 3.2

Add rendering options to mixin classes

## [0.0.47] - 2021-4-4

Removing support for Python 3.7

## [0.0.46] - 2021-4-2

Remove tests dir from distribution

## [0.0.45] - 2021-4-2

Refactor renderers and remove dependency on form widget renderer classes

## [0.0.44] - 2021-4-2

Allow renderer as arg for all stream and frame mixins/classes

## [0.0.40] - 2021-4-2

Use file-based templates for rendering streams/frames

## [0.0.39] - 2021-4-2

Fix for https://github.com/rails-inspire-django/django-turbo-helper/issues/5

## [0.0.36] - 2021-3-30

**render_form_response** adds turbo_stream_template name to context

**turbo_stream_response** decorator

## [0.0.35] - 2021-2-17

**render_form_response** can optionally re-render form as turbo stream

## [0.0.34] - 2021-2-13

Tidy up argument parsing in API

## [0.0.33] - 2021-2-4

Mixin **TurboFormAdapterMixin** added

## [0.0.32] - 2021-2-2

Refactoring modules

## [0.0.31] - 2021-2-2

Refactoring mixin classes

## [0.0.30] - 2021-2-1

**TurboStreamIterableResponse** removed

**TurboStreamFormMixin** and turbo-stream form views added

## [0.0.29] - 2021-1-27

**TurboStreamIterableResponse** deprecated

**TurboStreamMiddleware** removed

## [0.0.28] - 2021-1-22

Support for Python 3.7

## [0.0.27] - 2021-1-21

Bugfix for Turbo-Frame header in middleware

## [0.0.26] - 2021-1-17

Added **TurboMiddleware** (replacing **TurboStreamMiddleware**).

Removed **TemplateFormResponse**.

## [0.0.24] - 2021-1-17

Added **render_form_response** shortcut.

## [0.0.23] - 2021-1-14

Added **TurboStreamIterableResponse** class.

## [0.0.22] - 2021-1-14

Added **TemplateFormResponse** class which automatically sets correct status based on form error state.

## [0.0.21] - 2021-1-13

Middleware now accepts content type **text/vnd.turbo-stream.html*.

## [0.0.20] - 2021-1-13

Deprecated mixin methods removed.

Update response content type from *text/html; turbo-stream* to *text/vnd.turbo-stream.html*:

https://github.com/hotwired/turbo/releases/tag/v7.0.0-beta.3

## [0.0.19] - 2021-1-13

Changes to mixin APIs.

## [0.0.18] - 2021-1-12

**TurboStreamDeleteView** automatically resolves target based on model name+PK.

## [0.0.17] - 2021-1-7

Added **HttpResponseSeeOther** class and **redirect_303** shortcut function.

## [0.0.16] - 2021-1-7

Ensure all form mixins/views return a 303 on redirect as per Turbo docs.

## [0.0.15] - 2021-1-7

Removed protocol classes and mypy pre-commit requirement

## [0.0.14] - 2021-1-6

Dependency bugfix

## [0.0.13] - 2021-1-6

Added type hinting, tidy up of mixin class inheritance.

## [0.0.12] - 2021-1-5

Update form handling for changes in @hotwired/turbo 7.0.0-beta.2:

  - **TurboStreamFormMixin** class and supporting classes removed
  - **TurboFormMixin** class added that just returns a 422 response on invalid
  - **TurboStreamFormView**, **TurboStreamCreateView** and **TurboStreamUpdateView** classes removed
  - **TurboFormView**, **TurboCreateView** and **TurboUpdateView** classes added, using new **TurboFormMixin**

## [0.0.10] - 2020-12-30

Remove __str__ methods from TurboStream and TurboFrame classes

## [0.0.9] - 2020-12-30

Add render() method to template proxies

## [0.0.8] - 2020-12-30

### Added

TurboStream and TurboFrame classes
