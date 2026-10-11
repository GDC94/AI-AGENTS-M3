"""The Router's decision for one Query."""

from typing import Literal

from pydantic import BaseModel, Field

RouteTarget = Literal["hr", "tech", "finance", "out_of_scope"]


class Route(BaseModel):
    """One Area that resolves the Query's main request, or out_of_scope.

    `reasoning` comes first so the model explains itself before deciding,
    and the explanation is recorded in the trace.
    """

    reasoning: str = Field(description="Why this target resolves the main request, in one or two sentences.")
    target: RouteTarget = Field(description="The Area that resolves the main request, or out_of_scope.")
