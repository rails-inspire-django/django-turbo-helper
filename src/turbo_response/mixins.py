# Standard Library
import http

# Local
from .response import (
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)


class TurboStreamResponseMixin:
    """Mixin to handle turbo-stream responses"""

    turbo_stream_action = None
    turbo_stream_target = None

    def get_turbo_stream_action(self):
        """Returns the turbo-stream action parameter

        :return: turbo-stream action
        :rtype: turbo_response.Action
        """
        return self.turbo_stream_action

    def get_turbo_stream_target(self):
        """Returns the turbo-stream target parameter

        :return: turbo-stream target
        :rtype: str
        """
        return self.turbo_stream_target

    def get_response_content(self):
        """Returns turbo-stream content.

        :rtype: str
        """

        return ""

    def render_turbo_stream_response(self, **response_kwargs):
        """Returns a turbo-stream response.

        :rtype: turbo_response.TurboStreamResponse
        """

        action = self.get_turbo_stream_action()
        target = self.get_turbo_stream_target()

        if action is None:
            raise ValueError("action must be specified")

        if target is None:
            raise ValueError("target must be specified")

        return TurboStreamResponse(
            action=action,
            target=target,
            content=self.get_response_content(),
            **response_kwargs,
        )


class TurboStreamTemplateResponseMixin(TurboStreamResponseMixin):
    """Handles turbo-stream template responses."""

    def get_turbo_stream_template_names(self):
        """Returns list of template names.

        :rtype: list
        """
        return self.get_template_names()

    def render_turbo_stream_response(self, context, **response_kwargs):
        """Renders a turbo-stream template response.

        :param context: template context
        :type context: dict

        :rtype: turbo_response.TurboStreamTemplateResponse
        """
        return TurboStreamTemplateResponse(
            request=self.request,
            template=self.get_turbo_stream_template_names(),
            target=self.get_turbo_stream_target(),
            action=self.get_turbo_stream_action(),
            context=context,
            using=self.template_engine,
        )


class TurboFormMixin:
    """Mixin for handling form validation. Ensures response
    has 422 status on invalid"""

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        return response


class TurboFrameResponseMixin:
    turbo_frame_dom_id = None

    def get_turbo_frame_dom_id(self):
        return self.turbo_frame_dom_id

    def get_response_content(self):
        return ""

    def render_turbo_frame_response(self, **response_kwargs):

        dom_id = self.get_turbo_frame_dom_id()
        if dom_id is None:
            raise ValueError("dom_id must be specified")

        return TurboFrameResponse(
            content=self.get_response_content(),
            dom_id=self.get_turbo_frame_dom_id(),
            **response_kwargs,
        )


class TurboFrameTemplateResponseMixin(TurboFrameResponseMixin):
    """Handles turbo-frame template responses."""

    def render_turbo_frame_response(self, context, **response_kwargs):
        """Returns a turbo-frame response.

        :param context: template context
        :type context: dict

        :rtype: turbo_response.TurboFrameTemplateResponse
        """
        return TurboFrameTemplateResponse(
            request=self.request,
            template=self.get_template_names(),
            dom_id=self.get_turbo_frame_dom_id(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )
