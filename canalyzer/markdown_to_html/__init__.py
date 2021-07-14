from canalyzer.common.utils import read_all_content_from_file
import os
import logging
import markdown
from markdown.extensions.toc import TocExtension
import premailer


class MarkdownToHtml:
    def __init__(
        self,
        input_file: str,
        output_file: str,
        styles_file: str = None,
        apply_premailer: bool = False,
    ) -> None:
        self._logger = logging.getLogger(
            "canalyzer.markdown_to_html." + self.__class__.__name__
        )
        self.input_file = input_file
        self.styles_file = styles_file
        self.apply_premailer = apply_premailer
        self.output_file = output_file + ".html"
        self.output_summary_file = output_file + "_summary.html"

    def generate_html(self, gen_summary=False):
        html = None
        html_summary = None
        if os.path.isfile(self.input_file):
            self._logger.debug(f"Reading input file: {self.input_file}")
            content = read_all_content_from_file(self.input_file)
            _, extension = os.path.splitext(self.input_file)
            if extension.lower() == ".md":
                if gen_summary:
                    self._logger.debug("Extracting file summary and converting to html")
                    html_summary = self.__markdown_to_html(
                        self.__get_markdown_content_summary(content)
                    )
                self._logger.debug("Converting markdown file to html")
                html = self.__markdown_to_html(content)
            else:
                self._logger.error("Unsupported filetype")
        else:
            self._logger.error("Invalid file path")

        self._logger.debug("Processing html")
        html = self.__apply_premailer(self.__inject_css(html))
        with open(self.output_file, "w") as fp:
            fp.write(html)

        if gen_summary:
            self._logger.debug("Processing summary html")
            html_summary = self.__apply_premailer(
                self.__inject_css(html_summary),
            )
            with open(self.output_summary_file, "w") as fp:
                fp.write(html_summary)

    def __apply_premailer(self, html):
        if self.apply_premailer:
            self._logger.debug("Processing css styles using premailer")
            return premailer.transform(html)
        return html

    def __markdown_to_html(self, content: str):
        return markdown.markdown(
            content,
            extensions=[
                "tables",
                TocExtension(toc_depth="2-2", title="Table of Contents"),
                "attr_list",
            ],
        )

    def __inject_css(self, html: str) -> str:
        if html is not None and self.styles_file and os.path.isfile(self.styles_file):
            self._logger.debug("Injecting css file")

            html = f"""<div class="canalyzer">
{html}
</div>
"""
            html = self.__load_css() + "\n" + html
        return html

    def __load_css(self):
        return f"""
<style type="text/css">
{read_all_content_from_file(self.styles_file)}
</style>
"""

    def __get_markdown_content_summary(self, text: str) -> str:
        content_summary = ""
        heading_limit = "## "
        heading_limit_count = 1
        for line in text.splitlines(keepends=True):
            if line.startswith(heading_limit):
                heading_limit_count -= 1
            if heading_limit_count == -1:
                break
            content_summary += line

        # We don't need TOC
        content_summary = content_summary.replace("[TOC]", "")
        return content_summary
