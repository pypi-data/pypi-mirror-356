from pydantic import BaseModel, Field

from common_py.model import enums
from external.a79.src.models.tools import ToolOutput


class SendEmailInput(BaseModel):
    recipient: str = Field(
        description="Email recipient",
        json_schema_extra={
            "mandatory": True,
            "field_type": enums.CustomDataType.EMAIL.value,
        },
    )
    subject: str = Field(description="Email subject")
    body: str = Field(description="Plain text email content")


class SendEmailOutput(ToolOutput):
    pass
