# Standard Library
import http
from typing import Union

# Django
from django.db.models import Model
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url


class HttpResponseSeeOther(HttpResponseRedirect):
    """Redirect with 303 status"""

    status_code = http.HTTPStatus.SEE_OTHER


def redirect_303(to: Union[str, Model], *args, **kwargs) -> HttpResponseSeeOther:
    """Sends an HTTP 303 redirect.

    :param to:  URL or view name or model instance. If model then calls `get_absolute_url()`.
    """
    return HttpResponseSeeOther(resolve_url(to, *args, **kwargs))
