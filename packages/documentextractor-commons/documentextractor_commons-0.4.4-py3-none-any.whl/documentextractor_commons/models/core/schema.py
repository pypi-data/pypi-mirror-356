from __future__ import annotations

from enum import Enum

class AttributeType(str, Enum):
    TEXT = "Text"
    NUMBER = "Number"
    DATE = "Date"
    TIME = "Time"
    DATETIME = "DateTime"
    NAME = "Name"

    @classmethod
    def _missing_(cls, value):
        if(value=="Other"):
            return AttributeType.TEXT
        return super()._missing_(value)

class AttributeSource(str, Enum):
    DOC_DATA = "data"
    DOC_INSIGHT = "insight"
    ERP_SAP = "sap"
    ERP_HUBSPOT = "hubspot"