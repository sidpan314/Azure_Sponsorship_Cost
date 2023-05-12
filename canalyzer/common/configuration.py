import os
import json
import logging
from .utils import str_is_true, to_snake_case

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class SmtpConfiguration:
    def __init__(self) -> None:
        self.subject = "Azure Cost Analysis"
        self.from_address = "Azure Cost Analyzer Bot <no-reply@example.com>"
        self.to_address = None
        self.host = None
        self.port = None
        self.user = None
        self.password = None

    # Commented out as we won't be loading SMTP configuration from file anymore
    # def load_from_file(self, json_content: dict):
    #     for k in json_content.keys():
    #         if to_snake_case(k) in dir(self):
    #             self.__setattr__(to_snake_case(k), json_content[k])

    def load_from_env(self):
        self.subject = os.environ.get("CANALYYZER_SMTP_SUBJECT", self.subject)
        self.from_address = os.environ.get("CANALYYZER_SMTP_FROM", self.from_address)
        self.to_address = os.environ.get("CANALYYZER_SMTP_TO", self.to_address)
        self.host = os.environ.get("CANALYYZER_SMTP_HOST", self.host)
        self.port = os.environ.get("CANALYYZER_SMTP_PORT", self.port)
        self.user = os.environ.get("CANALYYZER_SMTP_USER", self.user)
        self.password = os.environ.get("CANALYYZER_SMTP_PASSWORD", self.password)


class Configuration:
    def __init__(self) -> None:
        self._logger = logging.getLogger(
            "canalyzer.analyzer." + self.__class__.__name__
        )
        self.tenant_id = ""
        self.client_id = ""
        self.client_secret = ""
        self.subscription_id = ""
        self.hours_by_month = 731
        self.hide_extensions = True
        self.hide_ignored_types = True
        self.currency = "USD"
        self.analysis_detail_level = 0
        self.analysis_output_path = None
        self.column_width = {"ResourceGroup": 60, "Resource": 48}
        self.smtp = SmtpConfiguration()

    def load(self):
        self._logger.info("Loading configuration")
        # Commented out as we won't be loading configuration from file anymore
        # self.__from_file()
        self.__from_env()
        self._logger.debug(self)

    def __from_env(self):
        self._logger.debug("Loading environment variables")
        self.tenant_id = os.environ.get("CANALYYZER_TENANT_ID", self.tenant_id)
        self.client_id = os.environ.get("CANALYYZER_CLIENT_ID", self.client_id)
        self.currency = os.environ.get("CANALYYZER_CURRENCY", self.currency)
        self.client_secret = os.environ.get(
            "CANALYYZER_CLIENT_SECRET", self.client_secret
        )
        self.subscription_id = os.environ.get(
            "CANALYYZER_SUBSCRIPTION_ID", self.subscription_id
        )
        self.hours_by_month = int(
            os.environ.get("CANALYYZER_HOURS_BY_MONTH", self.hours_by_month)
        )

        self.hide_extensions = str_is_true(
            os.environ.get("CANALYYZER_HIDE_EXTENSIONS", self.hide_extensions)
        )
        self.hide_ignored_types = str_is_true(
            os.environ.get("CANALYYZER_HIDE_IGNORED_TYPES", self.hide_ignored_types)
        )
        self.smtp.load_from_env()

        # Commented out as we won't be loading configuration from file anymore
    # def __from_file(self):
    #     self._logger.debug("Loading settings json file 'appsettings.json'")
    #     settings_path = os.path.join("appsettings.json")
    #     if os.path.exists(settings_path) and os.path.isfile(settings_path):
    #         with open(settings_path, "r") as fp:
    #             file_content = json.load(fp)
    #             for k in file_content.keys():
    #                 if k == "smtp":
    #                     self.smtp.load_from_file(file_content[k])
    #                 elif to_snake_case(k) in dir(self):
    #                    self.__setattr__(to_snake_case(k), file_content[k])
    #     # debug code to print file content
    #         print("File content:", file_content)
    #     else:
    #         self._logger.debug("Settings file 'appsettings.json' not found")


    def __repr__(self) -> str:
        return f"""<Configuration 
    Tenant ID: {self.tenant_id}
    Client ID: {self.client_id}
    Client Secret: {'[MASKED]' if self.client_secret != "" else ''}
    Subscription ID: {self.subscription_id}
>"""


configuration = Configuration()
configuration.load()
