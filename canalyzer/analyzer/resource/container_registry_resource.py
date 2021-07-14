from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import retail_price
from canalyzer.analyzer.azure_clients import container_registry_client, configuration
from . import Resource


class ContainerRegistryResource(Resource):
    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        super().__init__(resource_group, resource)
        self.extra = container_registry_client.registries.get(
            self.resource_group.name, self.name
        )

    @property
    def price(self):
        if self._price is not None:
            return self._price
        items = retail_price.from_filters(
            serviceFamily="Containers",
            serviceName="Container Registry",
            productName="Container Registry",
            armRegionName=self.location,
            skuName=self.extra.sku.name,
            meterName=f"{self.extra.sku.name} Registry Unit",
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
        self._set_unit_of_measure(items[0]["unitOfMeasure"])
        self._price = items[0]["retailPrice"]
        return self._price

    # @property
    # def price_by_month(self):
    #     return (
    #         (self.price / 24) * configuration.hours_by_month
    #         if self.price is not None
    #         else None
    #     )
