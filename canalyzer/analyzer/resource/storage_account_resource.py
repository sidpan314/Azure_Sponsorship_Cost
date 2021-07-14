from __future__ import annotations
from typing import TYPE_CHECKING
import math
import json
import datetime

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import retail_price
from canalyzer.analyzer.azure_clients import storage_client, monitor_management_client
from . import Resource


class StorageAccountResource(Resource):
    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        super().__init__(resource_group, resource)
        self.extra = storage_client.storage_accounts.get_properties(
            self.resource_group.name, self.name
        )
        self.used_capacity = None
        today = datetime.datetime.now().date()
        yesterday = today - datetime.timedelta(days=1)
        metrics_data = monitor_management_client.metrics.list(
            self.id,
            metricnames="UsedCapacity",
            timespan="{}/{}".format(yesterday, today),
            aggregation="Total",
        )
        for item in metrics_data.value:
            if item.name.value == "UsedCapacity":
                if (
                    len(item.timeseries)
                    and len(item.timeseries[0].data)
                    and item.timeseries[0].data[0].total
                ):
                    self.used_capacity = item.timeseries[0].data[0].total / math.pow(
                        1024, 3
                    )

    @property
    def info(self) -> dict:
        s_info = super().info
        s_info["Used Capacity"] = f"{self.used_capacity:.4f} GB"
        return s_info

    @property
    def __avaliability(self):
        avaliability = self.extra.sku.name.split("_")[-1]
        if avaliability == "RAGRS":
            avaliability = "RA-GRS"
        return avaliability

    @property
    def price(self):
        if self._price is not None:
            return self._price
        # This method assumes all capacity came from Blob Storage

        items = retail_price.from_filters(
            serviceFamily="Storage",
            serviceName="Storage",
            productName=f"General Block Blob{' v2' if self.extra.kind == 'StorageV2' else ''}",
            armRegionName=self.location,
            meterName=f"{self.extra.access_tier} {self.__avaliability} Data Stored",
        )
        items = [x for x in items if x["tierMinimumUnits"] == 0]

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
        self._price = items[0]["retailPrice"] * (
            self.used_capacity if self.used_capacity is not None else 0
        )
        return self._price
