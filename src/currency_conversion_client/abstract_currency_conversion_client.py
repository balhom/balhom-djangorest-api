"""
Provides a Currency Conversion client class.
"""
from abc import ABC, abstractmethod


class AbstractCurrencyConversionClient(ABC):

    @abstractmethod
    def get_currency_codes(self) -> list[str]:
        pass

    @abstractmethod
    def get_conversion(self, currency_from: str, currency_to: str) -> float:
        pass
