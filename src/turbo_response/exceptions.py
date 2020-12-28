# Django
from django.core.exceptions import ValidationError


class InvalidTurboStream(ValidationError):
    ...


class InvalidTurboFrame(ValidationError):
    ...
