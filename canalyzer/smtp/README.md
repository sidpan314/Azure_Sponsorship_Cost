# SMTP sender

CLI tool to send SMTP emails with files attachment, and html body support.

## Configuration

This tool supports configuration through environment variables and a JSON file (`appsettings.json` located on the repository root, inside the `smtp` key). The parameters are (using the `JSON - `env var` format):

- `subject` - `CANALYYZER_SMTP_SUBJECT`: Subject used on the email to send. Defaults to `Azure Cost Analysis`
- `fromAddress` - `CANALYYZER_SMTP_FROM`: EMail address to show as sender. Defaults to `Azure Cost Analyzer Bot <no-reply@example.com>`
- `toAddress` - `CANALYYZER_SMTP_TO`: EMails list, separated with `", "` which will receive the email.
- `host` - `CANALYYZER_SMTP_HOST`: SMTP host to use.
- `port` - `CANALYYZER_SMTP_PORT`: SMTP port.
- `user` - `CANALYYZER_SMTP_USER`: SMTP user
- `password` - `CANALYYZER_SMTP_PASSWORD`: SMTP password

For example:

```json
{
  "smtp": {
    "subject": "Azure Cost Analysis",
    "from_address": "Azure Cost Analyzer Bot <no-reply@example.com>",
    "to_address": "target@example.com",
    "host": "smtp.gmail.com",
    "port": "465",
    "user": "user@example.com",
    "password": "user_super_secret_password"
  }
}
```

## How to use

```
$ python ./canalyzer/smtp/ --help
Usage: python -m  [OPTIONS] HTML_BODY PLAIN_BODY

Options:
  -a, --attach TEXT
  --help             Show this message and exit.
```

### Arguments

- `HTML_BODY` Absolute or relative path to a HTML file. This will be used as the mail body rich content.
- `HTML_BODY` Absolute or relative path to a text file. This will be used as the mail body plain content.

### Options

- `--attach`: Absolute or relative path to a file. This will be attached to the email. This options can be used multiple times if you want to attach multiple files.

## Examples

Send an email with one file attached:

```
$ python ./canalyzer/smtp/ output_summary.html output.md -a output.pdf
```

Send an email with two files attached:

```
$ python ./canalyzer/smtp/ output_summary.html output.md -a output.pdf -a another_output.txt
```
