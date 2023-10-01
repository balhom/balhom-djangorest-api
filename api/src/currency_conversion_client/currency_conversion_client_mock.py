"""
Provides a Currency Conversion Test client class.
"""


from currency_conversion_client.exceptions import CannotMakeConversionException


class CurrencyConversionClientMock:

    def __init__(self):
        self.currency_codes = ["EUR", "USD", "CAD"]
        self.currency_conversions = [
            {
                "code": "USD",
                "conversions": [
                        {
                            "code": "CAD",
                            "value": 1.356
                        },
                    {
                            "code": "EUR",
                            "value": 0.945875
                    }
                ]
            },
            {
                "code": "EUR",
                "conversions": [
                        {
                            "code": "CAD",
                            "value": 1.43352
                        },
                    {
                            "code": "USD",
                            "value": 1.05713
                    }
                ]
            },
            {
                "code": "CAD",
                "conversions": [
                        {
                            "code": "EUR",
                            "value": 0.697635
                        },
                    {
                            "code": "USD",
                            "value": 0.737505
                    }
                ]
            }
        ]

    def get_currency_codes(self) -> list[str]:
        return self.currency_codes

    def get_conversion(self, currency_from: str, currency_to: str) -> float:
        if currency_from == currency_to:
            return 1

        for conversion in self.currency_conversions:
            if conversion["code"] == currency_from:
                for value in conversion["conversions"]:
                    if value["code"] == currency_to:
                        return value["value"]
                raise CannotMakeConversionException()
        raise CannotMakeConversionException()
