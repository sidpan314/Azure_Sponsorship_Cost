from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from canalyzer.analyzer.resource_group import ResourceGroup
from . import Resource


class ClusterResource(Resource):
    def __init__(self, resource_group: ResourceGroup, resource) -> None:
        super().__init__(resource_group, resource)

    @property
    def price(self):
        if self._price is not None:
            return self._price
        self._price = 0
        return self._price
