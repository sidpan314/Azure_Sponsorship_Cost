from __future__ import annotations
from typing import TYPE_CHECKING
import logging, json

if TYPE_CHECKING:
    from .azure_subscription import AzureSubscription
from .resource import Resource, ResourceList
from canalyzer.common.configuration import configuration
from .azure_clients import resource_client
import azure.core.exceptions


class ResourceGroup:
    def __init__(self, subscription: AzureSubscription, group) -> None:
        self._logger = logging.getLogger(
            "canalyzer.analyzer." + self.__class__.__name__
        )
        self.name = group.name
        self.id = group.id
        self.location = group.location
        self.subscription = subscription
        self.extra = resource_client.resource_groups.get(self.name)
        self.tags = self.extra.tags or {}
        self.resources: ResourceList = None

    def __repr__(self) -> str:
        return self.get_table_str(
            column_width=configuration.column_width[self.__class__.__name__]
        )
        # return f"{self.name:<{configuration.column_width[self.__class__.__name__]}}{self.location}"

    def get_table_str(self, separator="", column_width=0, include_price=False):
        printable_name = (
            self.name
            if len(self.name) < column_width or column_width == 0
            else f"{self.name[:column_width-6]}..."
        )
        price_column = (
            f"{separator}{self.price_by_month or 0:.6f}" if include_price else ""
        )
        return f"{printable_name:<{column_width}}{separator}{self.location:<{column_width}}{price_column}"

    def get_resources(self, force: bool = False) -> list[Resource]:
        if self.resources is None or force:
            self._logger.info(f"Getting resources from '{self.name}'")
            self.resources: ResourceList = ResourceList()

            resource_list = resource_client.resources.list_by_resource_group(
                self.name, expand="createdTime,changedTime"
            )
            for resource in list(resource_list):
                try:
                    self.resources.add_resource(self, resource)
                except azure.core.exceptions.ResourceNotFoundError as exc:
                    self._logger.error(exc)

            self._logger.debug(f"\n{self.resources}")
            self._logger.debug(f"Monthly cost: {self.price_by_month} ")
            self._logger.info(f"{len(self.resources)} resources found on '{self.name}'")

    @property
    def price_by_month(self):
        if self.resources is None:
            self.get_resources()
        return sum(
            [x.price_by_month for x in self.resources if x.price_by_month is not None]
        )


class ResourceGroupList(list):
    def add_resource_group(self, resource_group: ResourceGroup) -> bool:
        for x in self:
            if x.id == resource_group.id:
                return False
        self.append(resource_group)
        return True

    def find_by_name(self, name: str) -> ResourceGroup:
        for rg in self:
            if rg.name == name:
                return rg
        return None

    def find_by_id(self, id: str) -> ResourceGroup:
        for rg in self:
            if rg.id == id:
                return rg
        return None

    def __repr__(self) -> str:
        column_width = configuration.column_width["ResourceGroup"]
        text = (
            "Resource Group".ljust(column_width) + "Location".ljust(column_width) + "\n"
        )
        text += ("-" * (column_width * 2)) + "\n"
        text += "\n".join([str(x) for x in self])
        return text
