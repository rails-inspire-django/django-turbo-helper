from contextlib import contextmanager
from typing import Union

from django.db.models import Model
from django.shortcuts import resolve_url

from .constants import TURBO_STREAM_MIME_TYPE, ResponseFormat
from .response import HttpResponseSeeOther


def redirect_303(to: Union[str, Model], *args, **kwargs) -> HttpResponseSeeOther:
    """Sends an HTTP 303 redirect.

    All arguments are forwarded to django.shortcuts.resolve_url to generate the redirect URL.

    https://github.com/django/django/blob/9c436a09b3a641874881706495ae07293aa97c2f/django/shortcuts.py#L151
    """
    return HttpResponseSeeOther(resolve_url(to, *args, **kwargs))


def get_respond_to(request):
    resp_format = ResponseFormat()

    # TODO: move logic to ResponseFormat class
    if request.accepts(TURBO_STREAM_MIME_TYPE):
        resp_format.turbo_stream = True

    if request.accepts("application/json"):
        resp_format.json = True

    if request.accepts("text/html"):
        resp_format.html = True

    return resp_format


@contextmanager
def respond_to(request):
    """
    Inspired by Rails

    https://www.writesoftwarewell.com/how-respond_to-method-works-rails/

    respond_to do |format|
      format.turbo_stream { render turbo_stream: turbo_stream_template }
    end
    """
    resp_format: ResponseFormat = get_respond_to(request)
    try:
        yield resp_format
    finally:
        # Clean-up code, if needed
        pass
