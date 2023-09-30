"""Cache Currency Converter client."""
from functools import lru_cache
from django.conf import settings
from currency_conversion_client.abstract_currency_conversion_client import AbstractCurrencyConversionClient
from currency_conversion_client.currency_conversion_client import CurrencyConversionClient
from currency_conversion_client.currency_conversion_client_mock import CurrencyConversionClientMock


@lru_cache
def get_currency_conversion_client() -> AbstractCurrencyConversionClient:
    """Create an instance of a KeycloakClient using singleton pattern."""
    if settings.TESTING:
        return CurrencyConversionClientMock()
    return CurrencyConversionClient()
