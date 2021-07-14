#! /usr/local/bin/python
import sys, os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../.."))

from canalyzer.analyzer.format.supported_format import (
    FORMAT_CSV,
    FORMAT_MARKDOWN,
)
import click
from canalyzer.common.log import logger


def __version(ctx=None, param=None, value=None):
    if ctx is not None and (not value or ctx.resilient_parsing):
        return
    text = "CAnalyzer -  Azure Cost Analyzer - v1.0.0"
    if ctx:
        print(text)
        ctx.exit()
    else:
        logger.info(text)


@click.command()
@click.option("-d", "--detail", count=True)
@click.option("-r", "--resource-group", "rg_names", type=str, default=None)
@click.option("-o", "--output", type=str, default="output")
@click.option(
    "-f",
    "--format",
    "output_formats",
    type=click.Choice([FORMAT_MARKDOWN, FORMAT_CSV], case_sensitive=False),
    default=[FORMAT_MARKDOWN],
    multiple=True,
)
@click.option(
    "--version", is_flag=True, callback=__version, expose_value=False, is_eager=True
)
def analyze(detail, rg_names: str, output: str, output_formats: "tuple[str]"):
    __version()
    from canalyzer.analyzer import AzureSubscription, configuration
    from canalyzer.analyzer.format import MultiFormat

    configuration.analysis_detail_level = detail or 0
    configuration.analysis_output_path = output
    subscription = AzureSubscription()
    output = MultiFormat(output_formats)
    output.add_subscription_summary(subscription)
    if rg_names is not None:
        for rg_name in rg_names.split(","):
            subscription.get_resource_group(rg_name)
    else:
        subscription.get_all_resource_groups()

    output.add_subscription_resource_groups(subscription.resource_groups)
    for rg in subscription.resource_groups:
        output.add_resource_group_summary(rg)
        if configuration.analysis_detail_level >= 2:
            for r in rg.resources:
                output.add_resource_details(r)


if __name__ == "__main__":
    analyze()

# /subscriptions/8dc5e1a2-cc8e-4926-92e5-0a09e19ffa47/resourceGroups/gitlab/providers/Microsoft.Compute/virtualMachines/GitLabRunner01
# https://management.azure.com/subscriptions/8dc5e1a2-cc8e-4926-92e5-0a09e19ffa47/providers/Microsoft.Consumption/pricesheets/default?api-version=2019-10-01
