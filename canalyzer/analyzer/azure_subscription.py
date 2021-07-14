import logging, json
from canalyzer.common.configuration import configuration
from canalyzer.analyzer.azure_clients import resource_client, subscription_client
from canalyzer.analyzer.resource_group import ResourceGroup, ResourceGroupList


class AzureSubscription:
    def __init__(self):
        self._logger = logging.getLogger(
            "canalyzer.analyzer." + self.__class__.__name__
        )
        self.extra = subscription_client.subscriptions.get(
            configuration.subscription_id
        )
        self.name = self.extra.display_name
        self.resource_groups: ResourceGroupList = ResourceGroupList()

    def get_all_resource_groups(self):
        self._logger.info("Getting subscription resource groups")
        groups = resource_client.resource_groups.list()
        for group in list(groups):
            if self.resource_groups.find_by_id(group.id) is None:
                self.resource_groups.add_resource_group(ResourceGroup(self, group))
        self.resource_groups.sort(key=lambda x: x.name.lower())
        self._logger.debug(f"\n{self.resource_groups}")
        self._logger.info(
            f"{len(self.resource_groups)} resource groups found on this subscription"
        )
        return self.resource_groups

    def get_resource_group(self, name: str):
        self._logger.info(f"Getting '{name}' resource group")
        try:
            group = resource_client.resource_groups.get(name)
            if self.resource_groups.find_by_id(group.id) is None:
                self.resource_groups.add_resource_group(ResourceGroup(self, group))
        except Exception as exc:
            self._logger.error(f"Error getting '{name}' resource group", exc_info=exc)
            return None
        return self.resource_groups.find_by_id(group.id)
