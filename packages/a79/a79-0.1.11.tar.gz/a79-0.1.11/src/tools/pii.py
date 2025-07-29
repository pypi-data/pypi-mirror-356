from external.a79.src.a79.client import A79Client
from external.a79.src.models.tools import DEFAULT
from external.a79.src.models.tools.pii_models import RedactInput, RedactOutput

__all__ = ["RedactInput", "RedactOutput", "redact"]


def redact(*, text: str = DEFAULT) -> RedactOutput:
    """
    Redact PII (Personally Identifiable Information) from input text using LLM.
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = RedactInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="pii", name="redact", input=input_model.model_dump()
    )
    return RedactOutput.model_validate(output_model)
