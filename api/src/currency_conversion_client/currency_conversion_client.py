"""
Provides a Currency Conversion client class.
"""
import logging
import requests
from django.conf import settings

from currency_conversion_client.exceptions import CannotMakeConversionException

logger = logging.getLogger(__name__)


class CurrencyConversionClient:
    """
    Currency Conversion API service client.
    """

    def __init__(self):
        logger.info(
            "Using:\n%s\n%s",
            settings.CURRENCY_CONVERSION_API_URL,
            settings.CURRENCY_CONVERSION_API_KEY
        )

    def get_currency_codes(self) -> list[str]:
        response = requests.get(
            f"{settings.CURRENCY_CONVERSION_API_URL}/api/v1/currency",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"APIKey {settings.CURRENCY_CONVERSION_API_KEY}"
            },
            timeout=10
        )
        return list(response.content)

    def get_conversion(self, currency_from: str, currency_to: str) -> float:
        if currency_from == currency_to:
            return 1

        response = requests.get(
            f"{settings.CURRENCY_CONVERSION_API_URL}/api/v1/conversion/{currency_from}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"APIKey {settings.CURRENCY_CONVERSION_API_KEY}"
            },
            timeout=10
        )
        for value in response.content["conversions"]:
            if value["code"] == currency_to:
                return float(value["value"])
        raise CannotMakeConversionException()
