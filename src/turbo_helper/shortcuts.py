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


def get_response_format(request):
    """
    Inspired by Rails

    respond_to do |format|
      format.turbo_stream { render turbo_stream: turbo_stream_template }
    end
    """
    if request.accepts(TURBO_STREAM_MIME_TYPE):
        return ResponseFormat.TurboStream
    elif request.accepts("application/json"):
        return ResponseFormat.JSON
    else:
        return ResponseFormat.HTML


@contextmanager
def response_format(request):
    """
    Get supported response format from request headers

    html, json, turbo_stream
    """
    resp_format = get_response_format(request)
    try:
        yield resp_format
    finally:
        # Clean-up code, if needed
        pass
