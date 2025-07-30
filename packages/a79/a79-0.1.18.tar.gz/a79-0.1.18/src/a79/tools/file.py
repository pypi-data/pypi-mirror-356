from external.a79.src.a79.client import A79Client
from external.a79.src.models.tools import DEFAULT
from external.a79.src.models.tools.file_models import (
    GetFileContentInput,
    GetFileContentOutput,
)

__all__ = [
    "GetFileContentInput",
    "GetFileContentOutput",
    "read_csv",
    "read_pdf",
    "read_text",
    "extract_audio_transcript",
]


def read_csv(*, file_name: str) -> GetFileContentOutput:
    """Read CSV file content and return as DataFrame.

    This tool specifically handles CSV files and returns the content as a
    structured DataFrame along with metadata.

    Args:
        input: GetFileContentInput containing file_name to query

    Returns:
        GetFileContentOutput containing CSV data as DataFrame and metadata
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = GetFileContentInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="file", name="read_csv", input=input_model.model_dump()
    )
    return GetFileContentOutput.model_validate(output_model)


def read_pdf(*, file_name: str) -> GetFileContentOutput:
    """Read PDF file content and return as extracted text.

    This tool specifically handles PDF files and returns the extracted text
    content along with PDF-specific metadata.

    Args:
        input: GetFileContentInput containing file_name to query

    Returns:
        GetFileContentOutput containing PDF text content and metadata
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = GetFileContentInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="file", name="read_pdf", input=input_model.model_dump()
    )
    return GetFileContentOutput.model_validate(output_model)


def read_text(*, file_name: str) -> GetFileContentOutput:
    """Read plain text file content.

    This tool specifically handles plain text files and returns the raw
    text content.

    Args:
        input: GetFileContentInput containing file_name to query

    Returns:
        GetFileContentOutput containing plain text content and metadata
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = GetFileContentInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="file", name="read_text", input=input_model.model_dump()
    )
    return GetFileContentOutput.model_validate(output_model)


def extract_audio_transcript(*, file_name: str) -> GetFileContentOutput:
    """Extract transcript from audio file.

    This tool specifically handles audio files and returns the extracted
    transcript text.

    Args:
        input: GetFileContentInput containing file_name to query

    Returns:
        GetFileContentOutput containing audio transcript and metadata
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = GetFileContentInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="file", name="extract_audio_transcript", input=input_model.model_dump()
    )
    return GetFileContentOutput.model_validate(output_model)
