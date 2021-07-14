from datetime import datetime
from canalyzer.common.utils import format_date
from canalyzer.analyzer.resource.resource import Resource
from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import configuration, AzureSubscription
from . import Format


class MarkdownFormat(Format):
    def __init__(self) -> None:
        super().__init__()
        self.document = ""
        self.document_path = f"{configuration.analysis_output_path}.md"

        with open(self.document_path, "w"):
            pass

    def add_subscription_summary(self, azure_subscription: AzureSubscription):
        self._write(f"# Azure Cost Analysis  - {azure_subscription.name}")
        self._write(f"\nCreated at: {format_date(datetime.now())}\n")
        self._write("\n[TOC]\n")

    def add_subscription_resource_groups(self, resource_groups: "list[ResourceGroup]"):
        rows = "\n".join(
            [f"|{x.get_table_str('|', include_price=True)}|" for x in resource_groups]
        )
        table = f"""
## Resources Table 
|Resource Group|Location|Price|
|----|----|----------|
{rows}


**Approximate minimum monthly total: {configuration.currency} {sum([x.price_by_month for x in resource_groups]):.6f}**

"""
        self._write(table)

    def add_resource_group_summary(self, resource_group: ResourceGroup):
        self._write(f"\n## Resource Group - {resource_group.name}")
        if configuration.analysis_detail_level > 0:
            self._write(f"\n* Location: {resource_group.location}")
        if resource_group.tags:
            self._write(
                "\n* Tags:\n"
                + "\n".join(
                    [f"\t* {x}: {resource_group.tags[x]}" for x in resource_group.tags]
                )
            )
        self._write(
            f"\n**Monthly Price: {configuration.currency} {resource_group.price_by_month:.6f}**\n\n"
        )
        if resource_group.resources:
            rows = "\n".join(
                [f"|{x.get_table_str('|')}|" for x in resource_group.resources]
            )
            table = f"""
### Resources Table
|Name|Type|Created At|Price|
|----|----|----------|-----|
{rows}

"""
            self._write(table)
        else:
            self._write(
                """
            
            
No resources available.

            """
            )

    def add_resource_details(self, resource: Resource):
        if configuration.analysis_detail_level < 2:
            return
        tags = "\n".join([f"\t* {x}: {resource.tags[x]}" for x in resource.tags])
        resource_info = resource.info
        info = "\n".join([f"\t* {x}: {resource_info[x]}" for x in resource_info])
        text = f"""
### Resource - {resource.name} ({resource.type})
* Location: {resource.location}
* Created At: {format_date(resource.created_date)}
* Updated At: {format_date(resource.changed_date)}
* Tags:
{tags}
* Additional Info:
{info}
* **Monthly Price: {configuration.currency} {resource.price_by_month or 0:.6f}**

"""
        self._write(text)

    def _write(self, text: str):
        self._logger.debug(f"Writting: {text}")
        with open(self.document_path, "a+") as fp:
            fp.write(text)
