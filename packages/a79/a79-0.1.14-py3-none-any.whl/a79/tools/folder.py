from external.a79.src.a79.client import A79Client
from external.a79.src.models.tools import DEFAULT
from external.a79.src.models.tools.folder_models import (
    ListDatasourcesInput,
    ListDatasourcesOutput,
)

__all__ = ["ListDatasourcesInput", "ListDatasourcesOutput", "list_datasources"]


def list_datasources(
    *, folder_id: int, content_type: str = DEFAULT
) -> ListDatasourcesOutput:
    """
    Lists all datasources in a folder.
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = ListDatasourcesInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="folder", name="list_datasources", input=input_model.model_dump()
    )
    return ListDatasourcesOutput.model_validate(output_model)
