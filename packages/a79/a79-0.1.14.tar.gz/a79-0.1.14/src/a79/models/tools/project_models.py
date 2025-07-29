from pydantic import BaseModel, Field

from common_py import constants
from external.a79.src.models.tools import ToolOutput


class CreateProjectInput(BaseModel):
    name: str = Field(default="Workflow generated project")
    description: str = Field(default="")
    datasource_ids: list[int] = Field(default=[])
    worksheet_id: int | None = Field(default=None, json_schema_extra={"mandatory": True})
    use_case: str = Field(default=constants.TEXT_RESEARCH_USECASE)


class CreateProjectOutput(ToolOutput):
    project_id: int = Field()
