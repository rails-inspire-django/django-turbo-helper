import pathlib
from functools import lru_cache
from typing import Dict, Optional

from django.template import Template
from django.template.backends.django import DjangoTemplates as DjangoTemplatesBackend
from django.template.engine import Engine
from django.template.loader import get_template
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe

from .constants import Action


class BaseRenderer:
    """This classes is based on django form widget renderer: we can determine
    the template engine used to render the wrapper templates in settings or per instance."""

    def get_template(self, template_name: str) -> Template:
        raise NotImplementedError("subclasses must implement get_template()")

    def render(self, template_name: str, context: Dict) -> str:
        template = self.get_template(template_name)
        return template.render(context).strip()


def render_turbo_stream(
    action: Action,
    target: str,
    content: str = "",
    is_safe: bool = False,
    renderer: Optional[BaseRenderer] = None,
) -> str:
    """Wraps content in correct <turbo-stream> tags.

    :param action: action type
    :param target: the DOM ID target of the stream
    :param content: content to be wrapped. Can be empty.
    :param is_safe: mark content safe for HTML escaping.
    :param renderer: template renderer class

    :return: *<turbo-stream>* string
    """
    if is_safe:
        content = mark_safe(content)

    renderer = renderer or get_default_renderer()

    return renderer.render(
        "turbo_response/turbo_stream.html",
        {"action": action.value, "target": target, "content": content},
    )


def render_turbo_frame(
    dom_id: str,
    content: str = "",
    is_safe: bool = False,
    renderer: Optional[BaseRenderer] = None,
) -> str:
    """

    Wraps a response in correct *<turbo-frame>* tags.

    :param dom_id: a DOM ID present in the content
    :param content: content of the turbo-frame
    :param is_safe: mark content safe for HTML escaping.
    :param renderer: template renderer class

    :return: *<turbo-frame>* string
    """
    if is_safe:
        content = mark_safe(content)

    renderer = renderer or get_default_renderer()

    return renderer.render(
        "turbo_response/turbo_frame.html", {"dom_id": dom_id, "content": content}
    )


@lru_cache()
def get_default_renderer() -> BaseRenderer:
    """Get the default renderer class.

    :return: renderer subclass: default DjangoTemplates

    """
    from django.conf import settings

    renderer_class_name = getattr(
        settings, "TURBO_RESPONSE_RENDERER", "turbo_response.renderers.DjangoTemplates"
    )

    renderer_class = import_string(renderer_class_name)
    return renderer_class()


class EngineMixin:
    backend: Engine

    def get_template(self, template_name: str) -> Template:
        return self.engine.get_template(template_name)

    @cached_property
    def engine(self) -> Engine:
        return self.backend(
            {
                "APP_DIRS": True,
                "DIRS": [pathlib.Path(__file__).parent / self.backend.app_dirname],
                "NAME": "turbo_response",
                "OPTIONS": {},
            }
        )


class DjangoTemplates(EngineMixin, BaseRenderer):
    backend = DjangoTemplatesBackend


class Jinja2(EngineMixin, BaseRenderer):
    @cached_property
    def backend(self) -> Engine:
        from django.template.backends.jinja2 import Jinja2

        return Jinja2


class TemplatesSetting(BaseRenderer):
    def get_template(self, template_name: str) -> Template:
        return get_template(template_name)
