from __future__ import annotations
from typing import TYPE_CHECKING
import json
import math

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import retail_price
from canalyzer.analyzer.azure_clients import (
    recovery_service_client,
    recovery_service_backup_client,
)
from azure.mgmt.recoveryservicesbackup.models import FabricName
from . import Resource


class RecoveryVaultResource(Resource):
    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        super().__init__(resource_group, resource)
        self.extra = recovery_service_client.vaults.get(
            self.resource_group.name, self.name
        )
        self.usage = [
            x
            for x in recovery_service_client.usages.list_by_vaults(
                self.resource_group.name, self.name
            )
            if x.current_value
        ]
        self.item_count = None
        self.storage_usage = []
        for x in self.usage:
            if x.name.value == "ProtectedItemCount":
                self.item_count = x.current_value
            if x.name.value.endswith("StorageUsage"):
                self.storage_usage.append(
                    {
                        "type": x.name.value.replace("StorageUsage", ""),
                        "size": x.current_value / math.pow(1024, 3),
                    }
                )
        # print(self.item_count)
        # print(json.dumps(self.storage_usage, indent=2))
        # self.protected_items = (
        #     recovery_service_backup_client.backup_protected_items.list(
        #         self.name, self.resource_group.name
        #     )
        # )
        # for x in list(self.protected_items):
        #     # print(json.dumps(x.as_dict(), indent=2))
        #     # print(x.properties.container_name)
        #     # print(x.name)
        #     f = recovery_service_backup_client.recovery_points.list(
        #         self.name,
        #         self.resource_group.name,
        #         FabricName.AZURE,
        #         x.properties.container_name,
        #         x.name,
        #     )
        #     for y in list(f):
        #         print(json.dumps(y.as_dict(), indent=2))

        # f = recovery_service_backup_client.backup_usage_summaries.list(
        #     self.name, self.resource_group.name
        # )
        # for x in list(f):
        #     print(json.dumps(x.as_dict(), indent=2))

    @property
    def price(self):
        if self._price is not None:
            return self._price
        price = 0 if self.storage_usage else None
        for storage in self.storage_usage:
            items = retail_price.from_filters(
                serviceFamily="Storage",
                serviceName="Backup",
                armRegionName=self.location,
                skuName=f"Standard",
                meterName=f"{storage['type']} Data Stored",
            )
            if not items:
                self._logger.warning(
                    f"No price found for {storage['type']} Storage Type on {self.name} at {self.resource_group.name}"
                )
                continue
            if len(items) > 1:
                self._logger.warning(
                    f"Multiple price items for {storage['type']} Storage Type on {self.name} at {self.resource_group.name}:\n{json.dumps(items, indent=2)}"
                )
                self._logger.warning("Using first match")
            price += items[0]["retailPrice"] * storage["size"]
        self._price = price
        return self._price
