# Standard Library
import http
from typing import Any, Dict, Iterable, Optional, Union

# Django
from django.db.models import Model
from django.forms import Form
from django.http import HttpRequest
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse

# Local
from .response import HttpResponseSeeOther


def redirect_303(to: Union[str, Model], *args, **kwargs) -> HttpResponseSeeOther:
    """Sends an HTTP 303 redirect.

    :param to:  URL or view name or model instance. If model then calls `get_absolute_url()`.
    """
    return HttpResponseSeeOther(resolve_url(to, *args, **kwargs))


def render_form_response(
    request: HttpRequest,
    form: Form,
    template: Union[str, Iterable[str]],
    context: Optional[Dict[str, Any]] = None,
    **response_kwargs,
) -> TemplateResponse:
    """Returns a TemplateResponse with the correct status if the form contains errors."""

    return TemplateResponse(
        request,
        template,
        context={"form": form, **(context or {})},
        status=http.HTTPStatus.UNPROCESSABLE_ENTITY
        if form.errors
        else http.HTTPStatus.OK,
        **response_kwargs,
    )
