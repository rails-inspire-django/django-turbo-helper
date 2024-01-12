import enum

TURBO_STREAM_MIME_TYPE = "text/vnd.turbo-stream.html"


class ResponseFormat(enum.Enum):
    HTML = "html"
    JSON = "json"
    TurboStream = "turbo_stream"
