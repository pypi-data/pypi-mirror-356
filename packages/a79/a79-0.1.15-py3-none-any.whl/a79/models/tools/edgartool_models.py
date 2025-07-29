from pydantic import BaseModel

from external.a79.src.a79.models.tools import ToolOutput


class GetLatestCompanyFilingTextInput(BaseModel):
    company_identifier: str
    filing_types: list[str]


class GetLatestCompanyFilingTextOutput(ToolOutput):
    content: dict[str, str]
