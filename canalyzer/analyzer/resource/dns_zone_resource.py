from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import retail_price, configuration
from canalyzer.analyzer.azure_clients import dns_client
from . import Resource


class DnsZoneResource(Resource):
    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        super().__init__(resource_group, resource)
        self.skuName = None
        self.record_sets = None

    @property
    def price(self):
        if self._price is not None:
            return self._price
        items = retail_price.from_filters(
            serviceFamily="Networking",
            serviceName="Azure DNS",
            productName="Azure DNS",
            armRegionName="",
            skuName=self.skuName,
            meterName=f"{self.skuName} Zones",
        )
        if not items:
            self._logger.warning(
                f"No price found for {self.name} at {self.resource_group.name}"
            )
            return None
        if len(items) > 2:
            self._logger.warning(
                f"Multiple price items for {self.name} at {self.resource_group.name}:\n{json.dumps(items, indent=2)}"
            )
            self._logger.warning("Using first match")

        self._price = 0
        record_sets_counter = self.record_sets
        items_price = {int(x["tierMinimumUnits"]): x["retailPrice"] for x in items}
        items_price_keys = sorted(items_price.keys())
        items_price_keys.reverse()
        for min_qty in items_price_keys:
            unit_price = items_price[min_qty]
            if record_sets_counter > min_qty:
                self._price += (record_sets_counter - min_qty) * unit_price
                record_sets_counter = min_qty

        return self._price
