import http

from django.http import HttpResponse, HttpResponseRedirect

from .constants import TURBO_STREAM_MIME_TYPE


class HttpResponseSeeOther(HttpResponseRedirect):
    status_code = http.HTTPStatus.SEE_OTHER


class TurboStreamResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(content_type=TURBO_STREAM_MIME_TYPE, *args, **kwargs)
