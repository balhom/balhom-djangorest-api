"""
Provides app exceptions classes.
"""
from django.utils.translation import gettext_lazy as _
from core.exceptions import AppBadRequestException


CANNOT_MAKE_CONVERSION_ERROR = 20


class CannotMakeConversionException(AppBadRequestException):
    """
    Exception used when a currency conversion fails.
    """

    def __init__(self):
        detail = _("Cannot make conversion")
        super().__init__(detail, CANNOT_MAKE_CONVERSION_ERROR)
