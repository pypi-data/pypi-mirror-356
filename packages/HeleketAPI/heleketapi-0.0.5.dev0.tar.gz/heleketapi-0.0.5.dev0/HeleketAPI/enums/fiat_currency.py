from .base_enum import _BaseHeleketEnum


class FiatCurrency(_BaseHeleketEnum):
    """
    Listing of available fiat currencies.
    """

    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"