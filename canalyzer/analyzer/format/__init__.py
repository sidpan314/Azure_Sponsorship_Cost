from canalyzer.analyzer.azure_subscription import AzureSubscription
from canalyzer.analyzer.resource.resource import Resource
from canalyzer.analyzer.resource_group import ResourceGroup
from .format import Format
from .markdown_format import MarkdownFormat
from .supported_format import *


def getFormatInstance(type: str):
    if type == FORMAT_JSON:
        raise NotImplementedError("This format is not yet implemented")
    if type == FORMAT_MARKDOWN:
        return MarkdownFormat()
    return Format()


class MultiFormat(Format):
    def __init__(self, formats) -> None:
        self.formats = [getFormatInstance(x) for x in formats]

    def add_resource_details(self, resource: Resource):
        for format in self.formats:
            format.add_resource_details(resource)

    def add_resource_group_summary(self, resource_group: ResourceGroup):
        for format in self.formats:
            format.add_resource_group_summary(resource_group)

    def add_subscription_resource_groups(self, resource_groups: "list[ResourceGroup]"):
        for format in self.formats:
            format.add_subscription_resource_groups(resource_groups)

    def add_subscription_summary(self, azure_subscription: AzureSubscription):
        for format in self.formats:
            format.add_subscription_summary(azure_subscription)
