# Markdown to HTML

CLI tool to convert Markdown files to HTML

## How to use

From the repository root:

```
$ python ./canalyzer/markdown_to_html/ --help
Usage: python -m  [OPTIONS] INPUT_FILE

Options:
  -o, --output TEXT
  --with-summary
  --css TEXT
  --premailer
  --help             Show this message and exit.
```

### Arguments

- `INPUT_FILE`: Absolute or relative path to the Markdown file to be converted

### Options

- `--output`: Sets the file path and name of the generated HTML. The extension will be added by this tool.
- `--with-summary`: If set, generate a summary HTML file using only the resource groups table and the total estimated monthly cost.
- `--css`: Path to CSS file. These styles will be injected into any generated HTML file.
- `--premailer`: If any style is injected this option will apply the `premailer` module to the final HTML file. The `premailer` will convert any style block to inline style in every HTML tag, very useful when sending as an email body.

## Examples

Convert the `output.md` file to HTML, generate a summary, inject CSS, and process it with `premailer`

```
$ python ./canalyzer/markdown_to_html/ output.md  --css styles.css --with-summary --premailer
```
