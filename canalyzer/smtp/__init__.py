import os
import logging
import datetime
from smtplib import SMTP_SSL
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from canalyzer.common.utils import read_all_content_from_file
from canalyzer.common import configuration


class HtmlEmail:
    def __init__(self, html_body, plain_body) -> None:
        self._logger = logging.getLogger("canalyzer.smtp." + self.__class__.__name__)
        self.html_body = self.__validate_file_and_read(html_body)
        self.plain_body = self.__validate_file_and_read(plain_body)
        self.smtp_configuration = configuration.smtp

    def __validate_file_and_read(self, file_path):
        if os.path.isfile(file_path):
            return read_all_content_from_file(file_path)
        else:
            self._logger.fatal(f"File not found: {file_path}")
            exit()

    def send(self, attachments: "tuple[str]"):

        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        multipart_msg = MIMEMultipart("alternative")
        multipart_msg["Subject"] = f"{self.smtp_configuration.subject} - {current_date}"
        multipart_msg["From"] = self.smtp_configuration.from_address
        multipart_msg["To"] = self.smtp_configuration.to_address
        multipart_msg.attach(MIMEText(self.plain_body, "plain"))
        multipart_msg.attach(MIMEText(self.html_body, "html"))

        for attachment in attachments:
            if not os.path.isfile(attachment):
                self._logger(f"File not found: {attachment}")
            filename = os.path.basename(attachment)
            main_type, sub_type = self.__get_mime_type(attachment)
            with open(attachment, "rb") as fp:
                mime_attachment = MIMEBase(main_type, sub_type)
                mime_attachment.set_payload(fp.read())
            encoders.encode_base64(mime_attachment)
            mime_attachment.add_header(
                "Content-Disposition",
                f"attachment; filename={current_date.replace(' ','_')}_{filename}",
            )
            multipart_msg.attach(mime_attachment)

        server = SMTP_SSL(
            host=self.smtp_configuration.host, port=self.smtp_configuration.port
        )
        server.login(
            user=self.smtp_configuration.user, password=self.smtp_configuration.password
        )
        server.sendmail(
            self.smtp_configuration.user,
            self.smtp_configuration.to_address.split(", "),
            multipart_msg.as_string(),
        )
        server.quit()

    def __get_mime_type(self, file_path):
        _, extension = os.path.splitext(file_path)
        maintype, _ = mimetypes.guess_type(extension)
        maintype = maintype or "application/octet-stream"
        maintype, subtype = maintype.split("/")
        return (maintype, subtype)
