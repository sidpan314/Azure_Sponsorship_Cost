from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import retail_price, configuration
from canalyzer.analyzer.azure_clients import compute_client
from . import Resource


class VirtualMachineResource(Resource):
    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        super().__init__(resource_group, resource)
        self.extra = compute_client.virtual_machines.get(
            self.resource_group.name, self.name
        )

    def __is_linux(self):
        return self.extra.storage_profile.os_disk.os_type == "Linux"

    @property
    def price(self):
        if self._price is not None:
            return self._price
        items = retail_price.from_filters(
            serviceFamily="Compute",
            serviceName="Virtual Machines",
            armRegionName=self.location,
            armSkuName=self.extra.hardware_profile.vm_size,
        )
        items = [
            x
            for x in items
            if (self.__is_linux() and "Windows" not in x["productName"])
            or (not self.__is_linux() and "Windows" in x["productName"])
        ]
        items = [
            x
            for x in items
            if "Low Priority" not in x["skuName"] and "Spot" not in x["skuName"]
        ]
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
        self._price = items[0]["retailPrice"]
        return self._price

    @property
    def price_by_month(self):
        return (
            self.price * configuration.hours_by_month
            if self.price is not None
            else None
        )
