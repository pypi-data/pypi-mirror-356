from pydantic import BaseModel

from external.a79.src.models.tools import ToolOutput


class GetLatestCompanyFilingTextInput(BaseModel):
    company_identifier: str
    filing_types: list[str]


class GetLatestCompanyFilingTextOutput(ToolOutput):
    content: dict[str, str]
