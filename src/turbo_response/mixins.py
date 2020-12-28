# Django
from django.core.exceptions import ImproperlyConfigured

# Local
from .response import TurboStreamTemplateResponse


class TurboStreamMixin:
    """Use with ContextMixin subclass"""

    turbo_stream_action = None
    turbo_stream_target = None
    turbo_stream_template = None

    def get_turbo_stream_action(self):
        return self.turbo_stream_action

    def get_turbo_stream_target(self):
        return self.turbo_stream_target

    def get_turbo_stream_template(self):
        return self.turbo_stream_template

    def render_turbo_stream_response(self, **context):

        template = self.get_turbo_stream_template()
        target = self.get_turbo_stream_target()
        action = self.get_turbo_stream_action()

        if template is None:
            raise ImproperlyConfigured("turbo_stream_template must be set")

        if target is None:
            raise ImproperlyConfigured("turbo_stream_target must be set")

        if action is None:
            raise ImproperlyConfigured("turbo_stream_action must be set")

        return TurboStreamTemplateResponse(
            request=self.request,
            template=template,
            target=target,
            action=action,
            context=self.get_context_data(context),
            using=self.template_engine,
        )


class TurboStreamFormMixin(TurboStreamMixin):
    """Use with FormView"""

    def form_invalid(self, form):
        return self.render_turbo_stream_response(form=form)
