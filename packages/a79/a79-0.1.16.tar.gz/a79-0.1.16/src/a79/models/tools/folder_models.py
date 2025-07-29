from pydantic import BaseModel, Field

from common_py.model import enums
from external.a79.src.a79.models.tools import ToolOutput


class ListDatasourcesInput(BaseModel):
    folder_id: int = Field(
        description="The ID of the folder to read datasources from",
        json_schema_extra={"field_type": enums.CustomDataType.FOLDER.value},
    )
    content_type: str = Field(default="", description="Filter by content type")


class ListDatasourcesOutput(ToolOutput):
    datasource_ids: list[int] = Field(default_factory=list)
