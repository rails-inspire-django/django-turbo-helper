import enum


class Action(enum.Enum):
    """Turbo-Stream action parameter"""

    AFTER = "after"
    APPEND = "append"
    BEFORE = "before"
    PREPEND = "prepend"
    REMOVE = "remove"
    REPLACE = "replace"
    UPDATE = "update"


TURBO_STREAM_MIME_TYPE = "text/vnd.turbo-stream.html"
