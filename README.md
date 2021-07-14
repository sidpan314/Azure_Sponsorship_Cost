# Azure Cost Analyzer - CAnalyzer

If you or your company are granted a Microsoft's Azure Sponsorship and are trying to estimate the monthly cost of your resources, this tool is for you.

## Motivation

This type of subscription at this time has no access to the consumption API provided by Azure. If you try to use the [Usage List](https://docs.microsoft.com/en-us/cli/azure/consumption/usage?view=azure-cli-latest) command from the azure cli will output:

```
$ az consumption usage list
Command group 'consumption' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
(422) Cost Management supports only Enterprise Agreement, Web direct and Microsoft Customer Agreement offer types. Subscription <YOUR_SUBSCRIPTION_ID> is not associated with a valid offer type. Cost Management supports only Enterprise Agreement, Web direct and Microsoft Customer Agreement offer types. Subscription <YOUR_SUBSCRIPTION_ID> is not associated with a valid offer type. (Request ID: <REQUEST_ID>)
```

The same with any other consumption related command (with same or similar output)

Using the [Sponsorship Dashboard](https://www.microsoftazuresponsorships.com/Usage) we can see total credits usage and by-resource usage. But how about resource groups usage or specific resource usage.

We have multiple projects and multiple resource groups but we don't have easy access to costs or usage. Of course, we can use the [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) but it's a manual job

## Tools

This repository contains 3 tools with specific use case:

- [Analyzer](canalyzer/analyzer/README.md): The core of the project. It's job is to analyze a subscription and generate a minimum monthly cost (aproximate because of limitations) report
- [Markdown to HTML](canalyzer/markdown_to_html/README.md): Converts markdown files to HTML using the [markdown package](https://python-markdown.github.io/). Supports CSS injection and _EMail Ready_ output
- [SMTP](canalyzer/smtp/README.md): Send emails using the SMTP protocol. Supports for HTML body and attachments are implemented

> The details of each tool are located in the respectic folder. Follow the links.

## How to use

Create a new virtual environment. In this case we use `pipenv` and a local `venv` directory

```
$ mkdir .venv
$ pipenv shell
$ pipenv install
```

Refers to any tool if you want to know how to use it.

## Automation

### Convert HTML to PDF

If you want to send the whole analysis as a PDF attachment you can use [`wkhtmltopdf`](https://wkhtmltopdf.org/), integrated in the docker image. This script converts the generated HTML (using `markdown_to_html`) to pdf:

```
wkhtmltopdf input.html output.pdf
```
