# Standard Library
import http
from typing import Dict, List, Optional, Union

# Django
from django.db.models import Model
from django.forms import Form
from django.http import HttpRequest
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse

# Local
from .constants import Action
from .response import HttpResponseSeeOther
from .stream import TurboStream


def redirect_303(to: Union[str, Model], *args, **kwargs) -> HttpResponseSeeOther:
    """Sends an HTTP 303 redirect.

    :param to:  URL or view name or model instance. If model then calls `get_absolute_url()`.
    """
    return HttpResponseSeeOther(resolve_url(to, *args, **kwargs))


def render_form_response(
    request: HttpRequest,
    form: Form,
    template: Union[str, List[str]],
    context: Optional[Dict] = None,
    *,
    turbo_stream_template: Optional[Union[str, List[str]]] = None,
    turbo_stream_target: Optional[str] = None,
    turbo_stream_action: Action = Action.REPLACE,
    **response_kwargs,
) -> TemplateResponse:
    """Returns a TemplateResponse with the correct status if the form contains errors.

    If `turbo_stream_template` is provided along with `turbo_stream_target`, a TurboStream
    response will be returned instead if there are form validation errors.
    """

    context = {"form": form, **(context or {})}

    if turbo_stream_template and turbo_stream_target:
        context.update(
            {
                "turbo_stream_target": turbo_stream_target,
                "turbo_stream_template": turbo_stream_template,
            }
        )

        if form.errors:
            return (
                TurboStream(turbo_stream_target)
                .action(turbo_stream_action)
                .template(turbo_stream_template, context)
                .response(request, **response_kwargs)
            )

    return TemplateResponse(
        request,
        template,
        context,
        status=http.HTTPStatus.UNPROCESSABLE_ENTITY
        if form.errors
        else http.HTTPStatus.OK,
        **response_kwargs,
    )
