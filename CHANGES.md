# Changelog

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
