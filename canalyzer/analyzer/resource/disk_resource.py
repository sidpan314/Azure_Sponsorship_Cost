from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import retail_price
from canalyzer.analyzer.azure_clients import compute_client
from . import Resource


class DiskResource(Resource):
    STANDARD_SIZES = {
        32: "S4",
        64: "S6",
        128: "S10",
        256: "S15",
        512: "S20",
        1024: "S30",
        2048: "S40",
        4096: "S50",
        8192: "S60",
        16384: "S70",
        32767: "S80",
    }
    SSD_SIZES = {
        4: "E1",
        8: "E2",
        16: "E3",
        32: "E4",
        64: "E6",
        128: "E10",
        256: "E15",
        512: "E20",
        1024: "E30",
        2048: "E40",
        4096: "E50",
        8192: "E60",
        16384: "E70",
        32767: "E80",
    }
    PREMIUM_SSD_SIZES = {
        4: "P1",
        8: "P2",
        16: "P3",
        32: "P4",
        64: "P6",
        128: "P10",
        256: "P15",
        512: "P20",
        1024: "P30",
        2048: "P40",
        4096: "P50",
        8192: "P60",
        16384: "P70",
        32767: "P80",
    }

    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        super().__init__(resource_group, resource)
        self.extra = compute_client.disks.get(self.resource_group.name, self.name)

    @property
    def __avaliability(self):
        return self.extra.sku.name.split("_")[-1]

    @property
    def price(self):
        if self._price is not None:
            return self._price
        tier = None
        if self.extra.sku.name.startswith("Premium_"):
            tier = self.__get_tier(self.PREMIUM_SSD_SIZES)
        elif self.extra.sku.name.startswith("StandardSSD_"):
            tier = self.__get_tier(self.SSD_SIZES)
        elif self.extra.sku.name.startswith("Standard_"):
            tier = self.__get_tier(self.STANDARD_SIZES)
        else:
            self._logger.error(
                f"No disk tier found for {self.name} at {self.resource_group.name}"
            )

        items = retail_price.from_filters(
            serviceFamily="Storage",
            serviceName="Storage",
            armRegionName=self.location,
            skuName=f"{tier} {self.__avaliability}",
        )
        items = [
            x
            for x in items
            if "Disk" in x["productName"]
            and "Mounts" not in x["meterName"]
            and "- Free" not in x["meterName"]
            and x["meterName"] != "Disk Operations"
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

    def __get_tier(self, sizes: dict):
        if not self.extra.tier:
            size = self.extra.disk_size_gb
            tier_index = [s for s in sizes.keys() if size <= s][0]
            return sizes[tier_index]
        else:
            return self.extra.tier
