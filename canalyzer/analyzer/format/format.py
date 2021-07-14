from datetime import datetime
import logging
from canalyzer.analyzer.resource.resource import Resource
from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer.azure_subscription import AzureSubscription


class Format:
    def __init__(self) -> None:
        self._logger = logging.getLogger(
            "canalyzer.analyzer." + self.__class__.__name__
        )
        self.output = None

    def add_subscription_summary(self, azure_subscription: AzureSubscription):
        pass

    def add_subscription_resource_groups(self, resource_groups: "list[ResourceGroup]"):
        pass

    def add_resource_group_summary(self, resource_group: ResourceGroup):
        pass

    def add_resource_details(self, resource: Resource):
        pass
