from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer.azure_clients import private_dns_client
from . import DnsZoneResource


class PrivateDnsZoneResource(DnsZoneResource):
    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        super().__init__(resource_group, resource)
        self.skuName = "Private"
        self.extra = private_dns_client.private_zones.get(
            self.resource_group.name, self.name
        )
        self.record_sets = self.extra.number_of_record_sets
