from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import retail_price, configuration
from canalyzer.analyzer.azure_clients import sql_client
from . import Resource


class SqlDatabaseResource(Resource):
    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        super().__init__(resource_group, resource)
        self.server = self.name.split("/")[0]
        self.name = self.name.split("/")[-1]
        self.extra = sql_client.databases.get(
            self.resource_group.name, self.server, self.name
        )

    @property
    def price(self):
        if self._price is not None:
            return self._price
        items = (
            self.__price_items_general_purpose
            if self.extra.sku.tier == "GeneralPurpose"
            else self.__price_items_dtus
        )
        if not items:
            self._logger.warning(
                f"No price found for {self.name} at {self.resource_group.name}"
            )
            return None
        if len(items) > 1:
            self._logger.warning(
                f"Multiple price items for {self.name} at {self.resource_group.name}:\n{json.dumps(items, indent=2)}"
            )
            self._logger.warning("Using first match")
        self._set_unit_of_measure(items[0]["unitOfMeasure"])
        self._price = items[0]["retailPrice"]
        return self._price

    @property
    def __price_items_general_purpose(self):
        skuName = f"{self.extra.sku.capacity} vCore{' Zone Redundancy' if self.extra.zone_redundant else ''}"
        return retail_price.from_filters(
            productName=f"SQL Database Single/Elastic Pool General Purpose - Compute {self.extra.sku.family}",
            serviceFamily="Databases",
            serviceName="SQL Database",
            armRegionName=self.location,
            skuName=skuName,
            meterName=f"{'Zone Redundancy ' if self.extra.zone_redundant else ''}vCore",
        )

    @property
    def __price_items_dtus(self):
        skuName = (
            "B"
            if self.extra.sku.name == "Basic"
            else self.extra.requested_service_objective_name
        )
        return retail_price.from_filters(
            productName=f"SQL Database Single {self.extra.sku.name}",
            serviceFamily="Databases",
            serviceName="SQL Database",
            armRegionName=self.location,
            skuName=skuName,
            endswith_meterName="DTUs",
        )
