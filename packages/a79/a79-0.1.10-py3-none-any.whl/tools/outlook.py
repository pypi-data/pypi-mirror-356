from external.a79.src.a79.client import A79Client
from external.a79.src.models.tools import DEFAULT
from external.a79.src.models.tools.outlook_models import (
    EmailItem,
    OutlookInput,
    OutlookOutput,
    ToolSummary,
)

__all__ = [
    "EmailItem",
    "OutlookInput",
    "OutlookOutput",
    "ToolSummary",
    "fetch_outlook_emails",
]


def fetch_outlook_emails(
    *,
    access_token: str,
    folder_name: str = DEFAULT,
    start_date: str | None = DEFAULT,
    end_date: str | None = DEFAULT,
) -> OutlookOutput:
    """
    Fetch emails from a specified Outlook folder, filtered by date and keywords.
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = OutlookInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="outlook", name="fetch_outlook_emails", input=input_model.model_dump()
    )
    return OutlookOutput.model_validate(output_model)
