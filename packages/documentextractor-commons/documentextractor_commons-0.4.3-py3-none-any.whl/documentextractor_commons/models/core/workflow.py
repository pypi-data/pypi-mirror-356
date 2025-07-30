from enum import Enum

class DocType(str, Enum):
    INVOICE = "invoice"
    RESUME = "resume"
    FINANCIAL_STATEMENT = "financial_statement"
    PRESENTATION = "presentation"
    CONTRACT = "contract"
    LETTER = "letter"
    EMAIL = "email"
    TIMETABLE = "timetable"
    FORM = "form"
    SURVEY = "survey"
    CERTIFICATE = "certificate"

    @classmethod
    def _missing_(cls, value):
        if(value=="none"):
            return None
        return super()._missing_(value)