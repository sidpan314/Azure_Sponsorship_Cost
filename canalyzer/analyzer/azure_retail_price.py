import json
import logging
import requests
from canalyzer.analyzer import configuration

HOUR = 1
MONTH = 2


class AzureRetailPrice:
    def __init__(self) -> None:
        self._logger = logging.getLogger(
            "canalyzer.analyzer." + self.__class__.__name__
        )
        self.cache_data = {}
        self._url = "https://prices.azure.com/api/retail/prices"

    @property
    def __get_uri(self):
        return f"{self._url}?currencyCode='{configuration.currency}'"

    def __get_json(self, uri):
        self._logger.debug(uri)
        response = requests.get(uri)
        return response.json()

    def __get_with_filters(self, filters: str = None):
        uri = f"{self.__get_uri}{f'&$filter={filters}' if filters else ''}"
        return self.__get_json(uri)

    def __parse_filter(self, key: str, value: str):
        key_parts = key.split("_")
        if len(key_parts) == 1:
            return f"{key} eq '{value}'"
        return f"{key_parts[0]}({key_parts[1]}, '{value}')"

    def from_filters(self, **kwargs):
        if "priceType" not in kwargs:
            kwargs["priceType"] = "Consumption"
        filters = " and ".join(
            [
                f"{self.__parse_filter(k, kwargs[k])}"
                for k in kwargs
                if kwargs[k] is not None
            ]
        )
        if filters not in self.cache_data:
            self.cache_data[filters] = []
            response = self.__get_with_filters(filters)
            self.cache_data[filters] += response["Items"]
            while response["NextPageLink"] is not None:
                response = self.__get_json(response["NextPageLink"])
                self.cache_data[filters] += response["Items"]
        return self.cache_data[filters]

    def apply_tier_minimum_units(self, value: float, items: dict) -> float:
        price = 0.0
        current_value = value
        items_price = {int(x["tierMinimumUnits"]): x["retailPrice"] for x in items}
        items_price_keys = sorted(items_price.keys())
        items_price_keys.reverse()
        for min_qty in items_price_keys:
            unit_price = items_price[min_qty]
            if current_value > min_qty:
                self._logger.debug(
                    f"Appliying tier minimun units: current_value={current_value} - min_qty={min_qty} - unit_price={unit_price}"
                )
                price += (current_value - min_qty) * unit_price
                current_value = min_qty
        return price


retail_price = AzureRetailPrice()
