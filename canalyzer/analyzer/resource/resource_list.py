from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import configuration
from . import (
    Resource,
    VirtualMachineResource,
    VirtualMachineScaleSetResource,
    DiskResource,
    PublicIpAddressResource,
    RecoveryVaultResource,
    ClusterResource,
    LoadBalancerResource,
    StorageAccountResource,
    SqlDatabaseResource,
    PublicDnsZoneResource,
    PrivateDnsZoneResource,
    ContainerRegistryResource,
    LogAnalyticsWorkspaceResource,
)


class ResourceList(list):
    __type_to_class = {
        "Microsoft.ContainerService/managedClusters": ClusterResource,
        "Microsoft.Compute/disks": DiskResource,
        "Microsoft.Compute/virtualMachines": VirtualMachineResource,
        "Microsoft.Network/publicIPAddresses": PublicIpAddressResource,
        "Microsoft.RecoveryServices/vaults": RecoveryVaultResource,
        "Microsoft.Compute/virtualMachineScaleSets": VirtualMachineScaleSetResource,
        "Microsoft.Network/loadBalancers": LoadBalancerResource,
        "Microsoft.Storage/storageAccounts": StorageAccountResource,
        "Microsoft.Sql/servers/databases": SqlDatabaseResource,
        "Microsoft.SQL/servers/databases": SqlDatabaseResource,
        "Microsoft.Network/dnszones": PublicDnsZoneResource,
        "Microsoft.Network/privateDnsZones": PrivateDnsZoneResource,
        "Microsoft.ContainerRegistry/registries": ContainerRegistryResource,
        "Microsoft.OperationalInsights/workspaces": LogAnalyticsWorkspaceResource,
    }
    __ignored_types = [
        "Microsoft.Compute/availabilitySets",
        "Microsoft.ManagedIdentity/userAssignedIdentities",
        "Microsoft.Network/networkInterfaces",
        "Microsoft.Network/networkProfiles",
        "Microsoft.Network/networkSecurityGroups",
        "Microsoft.Network/privateDnsZones/virtualNetworkLink",
        "Microsoft.Network/virtualNetworks",
        "Microsoft.OperationsManagement/solutions",
        "Microsoft.Sql/servers",
        "Microsoft.Insights/dataCollectionRules",
        "Microsoft.Compute/sshPublicKeys",
    ]

    def add_resource(self, resource_group: ResourceGroup, resource):
        if configuration.hide_extensions and (
            resource.type.endswith("/extensions")
            or resource.type.endswith("/virtualNetworkLinks")
        ):
            return
        if configuration.hide_ignored_types and resource.type in self.__ignored_types:
            return
        self.append(
            self.__type_to_class.get(resource.type, Resource)(resource_group, resource)
        )

    def find_by_name(self, name: str) -> Resource:
        for rsc in self:
            if rsc.name == name:
                return rsc
        return None

    def find_by_type(self, resource_type: str) -> Resource:
        return [rsc for rsc in self if Path(rsc.type).match(resource_type)]

    def __repr__(self) -> str:
        column_width = configuration.column_width["Resource"]
        text = (
            "Resource".ljust(column_width)
            + "Type".ljust(column_width)
            + "Create date".ljust(column_width)
            + "Price".ljust(column_width)
            + "\n"
        )
        text += ("-" * (column_width * 4)) + "\n"
        text += "\n".join([str(x) for x in self])
        return text
