from external.a79.src.a79.client import A79Client
from external.a79.src.models.tools import DEFAULT
from external.a79.src.models.tools.clinical_trials_search_models import (
    ClinicalTrialRecord,
    ClinicalTrialResult,
    ClinicalTrialsSearchInput,
    ClinicalTrialsSearchOutput,
    ClinicalTrialsSearchResponse,
    ToolSummary,
)

__all__ = [
    "ClinicalTrialRecord",
    "ClinicalTrialResult",
    "ClinicalTrialsSearchInput",
    "ClinicalTrialsSearchOutput",
    "ClinicalTrialsSearchResponse",
    "ToolSummary",
    "clinical_trials_search",
]


def clinical_trials_search(
    *,
    condition: str,
    location: str | None = DEFAULT,
    status: str | None = DEFAULT,
    page_size: int | None = DEFAULT,
) -> ClinicalTrialsSearchOutput:
    """
    Search for clinical trials using ClinicalTrials.gov API.
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = ClinicalTrialsSearchInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="clinical_trials_search",
        name="clinical_trials_search",
        input=input_model.model_dump(),
    )
    return ClinicalTrialsSearchOutput.model_validate(output_model)
