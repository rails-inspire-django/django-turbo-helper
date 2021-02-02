# Changelog

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
