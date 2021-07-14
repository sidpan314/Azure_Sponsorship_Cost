import sys, os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../.."))

from canalyzer.markdown_to_html import MarkdownToHtml
import click
from canalyzer.common.log import logging, logger

_logger = logging.getLogger("canalyzer.markdown_to_html")


@click.command()
@click.argument("input_file")
@click.option("--output", "-o", type=str, default="output")
@click.option("--with-summary", is_flag=True)
@click.option("--css", type=str, default=None)
@click.option("--premailer", is_flag=True)
def main(input_file: str, output: str, with_summary: bool, css: str, premailer: bool):
    _logger.info("CAnalyzer - Markdown to HTML converter")
    generator = MarkdownToHtml(input_file, output, css, apply_premailer=premailer)
    generator.generate_html(gen_summary=with_summary)


if __name__ == "__main__":
    main()
