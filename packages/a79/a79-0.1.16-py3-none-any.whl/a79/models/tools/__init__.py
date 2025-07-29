import typing as t

from pydantic import BaseModel, Field

from common_py.workflow.nodes.node import HumanReadableNodeOutput

DEFAULT: t.Any = object()
"""
Sentinel value for when a field has not been provided as input.
"""


class ToolSummary(BaseModel):
    short_summary: str
    long_summary: HumanReadableNodeOutput = Field(default_factory=HumanReadableNodeOutput)


class ToolOutput(BaseModel):
    tool_summary: ToolSummary
