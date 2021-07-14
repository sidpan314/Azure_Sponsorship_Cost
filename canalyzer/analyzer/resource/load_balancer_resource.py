from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import retail_price, configuration
from canalyzer.analyzer.azure_clients import network_client
from . import Resource


class LoadBalancerResource(Resource):
    # Hourly price based on https://azure.microsoft.com/en-us/pricing/details/load-balancer/
    # Apparently, it's the same price on every azure region (except for US Gov regions)
    # This is set like this because I can't find the right filter for the retail price API
    FIRST_5_RULES_PRICE = 0.025
    ADDITTIONAL_RULE_PRICE = 0.01

    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        super().__init__(resource_group, resource)
        self.extra = network_client.load_balancers.get(
            self.resource_group.name, self.name
        )
        self.__rules_count = len(self.extra.load_balancing_rules)

    @property
    def price(self):
        if self._price is not None:
            return self._price
        if self.__rules_count == 0:
            self._price = 0
        else:
            self._price = self.FIRST_5_RULES_PRICE
            if self.__rules_count > 5:
                self._price += (self.__rules_count - 5) * self.ADDITTIONAL_RULE_PRICE
        return self._price

    @property
    def price_by_month(self):
        return (
            self.price * configuration.hours_by_month
            if self.price is not None
            else None
        )
