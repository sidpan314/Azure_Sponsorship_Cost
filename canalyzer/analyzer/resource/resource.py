from __future__ import annotations
from canalyzer.common.utils import format_date
from typing import TYPE_CHECKING
import logging
import json

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from canalyzer.analyzer import configuration


class Resource:
    UNIT_HOUR = 1
    UNIT_DAY = 2
    UNIT_MONTH = 3

    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        self._logger = logging.getLogger(
            "canalyzer.analyzer." + self.__class__.__name__
        )
        self.name = resource.name
        self.type = resource.type
        self.location = resource.location
        self.created_date = resource.created_time
        self.changed_date = resource.changed_time
        self.id = resource.id
        self.resource_group = resource_group
        self.subscription = resource_group.subscription
        self._price = None
        self.unit_of_measure = self.UNIT_MONTH
        self.tags = resource.tags or {}

    def __repr__(self) -> str:
        return self.get_table_str(column_width=configuration.column_width["Resource"])

    def get_table_str(self, separator="", column_width=0):
        printable_name = (
            self.name
            if len(self.name) < column_width or column_width == 0
            else f"{self.name[:column_width-6]}..."
        )
        price_str = (
            f"{self.price_by_month:.6f}" if self.price_by_month is not None else None
        )
        return f"{printable_name:<{column_width}}{separator}{self.type:<{column_width}}{separator}{format_date(self.created_date):<{column_width}}{separator}{price_str}"

    def _set_unit_of_measure(self, item_unit_of_measure: str):
        item_unit_of_measure = item_unit_of_measure.lower()
        if "day" in item_unit_of_measure or "/d" in item_unit_of_measure:
            self.unit_of_measure = self.UNIT_DAY
        elif "hour" in item_unit_of_measure or "/h" in item_unit_of_measure:
            self.unit_of_measure = self.UNIT_HOUR
        elif "month" in item_unit_of_measure:
            self.unit_of_measure = self.UNIT_MONTH

    @property
    def info(self) -> dict:
        return {}

    @property
    def price(self):
        return self._price

    @property
    def price_by_month(self):
        if self.price is None:
            return None
        if self.unit_of_measure == self.UNIT_DAY:
            return (self.price / 24) * configuration.hours_by_month
        if self.unit_of_measure == self.UNIT_HOUR:
            return self.price * configuration.hours_by_month
        return self.price
