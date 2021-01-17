This package provides helpers for server-side rendering of [Hotwired/Turbo](https://turbo.hotwire.dev/) streams and frames.

**Disclaimer**: the Hotwired/Turbo client libraries are, at time of writing, still in Beta. We expect there will be breaking changes until the first stable release. This package, and the Turbo client, should therefore be used with caution in a production environment. The version used in testing is *@hotwired/turbo==7.0.0-beta.3*.


## Requirements

This library is tested for Python 3.8+.

## Installation

> pip install django-turbo-response

To install from Git:

> git clone https://github.com/hotwire-django/django-turbo-response

> cd django-turbo-response

> python setup.py install

**Note**: This library does not include any client libraries (Turbo or Stimulus). You may wish to add these yourself using your preferred Javascript build tool, or use a CDN. Please refer to the Hotwire documentation on installing these libraries.

Full documentation on ReadTheDocs:

https://django-turbo-response.readthedocs.io/en/latest/

## License

This project is covered by the MIT license.
