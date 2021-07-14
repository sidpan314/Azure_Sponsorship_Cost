# Analyzer

CLI tool to analyze Azure Subscriptions resources and save to file in supported formats

## Supported Formats

- Markdown

## Configuration

This tool supports configuration through environment variables and a JSON file (`appsettings.json` located on the repository root). The parameters are (using the `JSON - `env var` format):

- `clientId` - `CANALYYZER_CLIENT_ID`: Azure's Service Principal valid client id on the target tenant and subscription.
- `clientSecret` - `CANALYYZER_CLIENT_SECRET`: Azure's Service Principal valid client secret on the target tenant and subscription. This secret corresponds to the previous client id
- `tenantId` - `CANALYYZER_TENANT_ID`: Azure's Tenant ID to analyze
- `subscriptionId` - `CANALYYZER_SUBSCRIPTION_ID`: Azure's Subscription ID to analyze. This must exist in the provided Azure Tenant
- `currency` - `CANALYYZER_CURRENCY`: Currency code to use while fetching retail prices using the [Azure Retail Price REST API](https://docs.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices#supported-currencies)
- `hideExtensions` - `CANALYYZER_HIDE_EXTENSIONS`: If `True` (default) hides any extension resource
- `hideIgnoredTypes` - `CANALYYZER_HIDE_IGNORED_TYPES`: If `True` (default) hides ignored resource types. You can find [here](resource/resource_list.py#L43) the complete list of ignored types (mostly because there is no current way to get an estimated monthly cost)

## How to use

Create a valid Service Principal with `Reader` role and `sdk-auth` enabled. You can find an example script in the [`create_rbac.sh` ](../../scripts/create_rbac.sh) file. Save the tenant id, client id, and secret in the appsettings.json file or use environment variables as described in the [Configuration](#configuration) section

From the root of this repository:

```
$ python ./canalyzer/analyzer/ --help
Usage: python -m  [OPTIONS]

Options:
  -d, --detail                 [x>=0]
  -r, --resource-group TEXT
  -o, --output TEXT
  -f, --format [markdown|csv]
  --version
  --help                       Show this message and exit.
```

### Options

- `--detail`: Sets the detail level on the generated output. 0 is the less detailed level. Up to level 3 is supported.
- `--resource-group` Sets the specific resource group to analyze. If this is not set it will analyze the entire subscription. This option allows multiple values. For example: `-r rg1 -r rg2 -r rg3`
- `--output`: Sets the output path and file name of the generated report. The file extension will be added based on the file format set.
- `--format`: Sets the file format of the generated report. The default format is `markdown`. This option allows multiple supported values.

## Examples

Analyze the entire subscription and generate a markdown report:

```
$ python ./canalyzer/analyzer/
```

Analyze the entire subscription and generate a markdown report with a specific file name:

```
$ python ./canalyzer/analyzer/ -o ../../generated_report
```

Analyze one resource group and generate a markdown report:

```
$ python ./canalyzer/analyzer/ -r resource_group_a
```

Analyze two resource groups and generate a markdown report:

```
$ python ./canalyzer/analyzer/ -r resource_group_a -r resource_group_b
```

Analyze one resource group with level 2 details and generate a markdown report:

```
$ python ./canalyzer/analyzer/ -r resource_group_a -d 2
```
