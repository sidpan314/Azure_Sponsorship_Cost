from __future__ import annotations
from typing import TYPE_CHECKING
import math
import json
import datetime

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import retail_price
from canalyzer.analyzer.azure_clients import (
    log_analytics_client,
    log_analytics_data_client,
    monitor_management_client,
)
from azure.loganalytics.models.query_body import QueryBody
from . import Resource


class LogAnalyticsWorkspaceResource(Resource):
    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        super().__init__(resource_group, resource)
        self.extra = log_analytics_client.workspaces.get(
            self.resource_group.name, self.name
        )

    @property
    def monthly_usage(self) -> float:
        result = log_analytics_data_client.query(
            self.extra.customer_id,
            QueryBody(
                query="""Usage
| where TimeGenerated > startofday(ago(30d))
| where IsBillable == true
| summarize TotalVolumeGB = sum(Quantity) / 1000 
                """,
            ),
        )
        if result and result.tables and result.tables[0].rows:
            return result.tables[0].rows[0][0]
        return 0.0

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
            serviceFamily="Management and Governance",
            serviceName="Log Analytics",
            productName="Log Analytics",
            armRegionName=self.location,
            meterName="Data Ingestion",
            type=None,
        )

        if not items:
            self._logger.warning(
                f"No price found for {self.name} at {self.resource_group.name}"
            )
            return None
        self._price = retail_price.apply_tier_minimum_units(self.monthly_usage, items)
        return self._price


#  Average_% Free Inodes,
#  Average_% Free Space,
#  Average_% Used Inodes,
#  Average_% Used Space,
#  Average_Disk Read Bytes/sec,
#  Average_Disk Reads/sec,
#  Average_Disk Transfers/sec,
#  Average_Disk Write Bytes/sec,
#  Average_Disk Writes/sec,
#  Average_Free Megabytes,
#  Average_Logical Disk Bytes/sec,
#  Average_% Available Memory,
#  Average_% Available Swap Space,
#  Average_% Used Memory,
#  Average_% Used Swap Space,
#  Average_Available MBytes Memory,
#  Average_Available MBytes Swap,
#  Average_Page Reads/sec,
#  Average_Page Writes/sec,
#  Average_Pages/sec,
#  Average_Used MBytes Swap Space,
#  Average_Used Memory MBytes,
#  Average_Total Bytes Transmitted,
#  Average_Total Bytes Received,
#  Average_Total Bytes,
#  Average_Total Packets Transmitted,
#  Average_Total Packets Received,
#  Average_Total Rx Errors,
#  Average_Total Tx Errors,
#  Average_Total Collisions,
#  Average_Avg. Disk sec/Read,
#  Average_Avg. Disk sec/Transfer,
#  Average_Avg. Disk sec/Write,
#  Average_Physical Disk Bytes/sec,
#  Average_Pct Privileged Time,
#  Average_Pct User Time,
#  Average_Used Memory kBytes,
#  Average_Virtual Shared Memory,
#  Average_% DPC Time,
#  Average_% Idle Time,
#  Average_% Interrupt Time,
#  Average_% IO Wait Time,
#  Average_% Nice Time,
#  Average_% Privileged Time,
#  Average_% Processor Time,
#  Average_% User Time,
#  Average_Free Physical Memory,
#  Average_Free Space in Paging Files,
#  Average_Free Virtual Memory,
#  Average_Processes,
#  Average_Size Stored In Paging Files,
#  Average_Uptime,Average_Users,
#  Average_Current Disk Queue Length,
#  Average_Available MBytes,
#  Average_% Committed Bytes In Use,
#  Average_Bytes Received/sec,
#  Average_Bytes Sent/sec,
#  Average_Bytes Total/sec,
#  Average_Processor Queue Length,
#  Heartbeat,
#  Update,
#  Event
