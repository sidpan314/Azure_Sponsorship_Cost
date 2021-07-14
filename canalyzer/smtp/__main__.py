import sys, os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../.."))

import click
from canalyzer.smtp import HtmlEmail
from canalyzer.common.log import logging, logger

_logger = logging.getLogger("canalyzer.smtp")


@click.command()
@click.argument("html_body")
@click.argument("plain_body")
@click.option("--attach", "-a", type=str, multiple=True)
def main(html_body: str, plain_body: str, attach: "tuple[str]"):
    _logger.info("CAnalyzer - SMTP Sender")
    html_email = HtmlEmail(html_body, plain_body)
    html_email.send(attach)


if __name__ == "__main__":
    main()
