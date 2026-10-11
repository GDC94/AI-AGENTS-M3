"""The Judge's result for one grounded Answer."""

from typing import Annotated

from pydantic import BaseModel, Field

# Strict: a float such as 7.0 or a string such as "7" is rejected, not coerced.
Rating = Annotated[int, Field(strict=True, ge=1, le=10)]


class QualityVerdict(BaseModel):
    """Four Ratings from 1 to 10 and a Reason in Spanish.

    `reason` comes first so the model explains itself before rating,
    mirroring `Route.reasoning`.
    """

    reason: str = Field(description="Why these Ratings, in one to three sentences, written in Spanish.")
    quality: Rating = Field(description="Overall quality of the Answer.")
    relevance: Rating = Field(description="Dimension: does the Answer address what the Query asks.")
    completeness: Rating = Field(description="Dimension: does the Answer cover everything the Sections say about it.")
    accuracy: Rating = Field(description="Dimension: is every claim supported by the Sections used.")

    def ratings_by_name(self) -> dict[str, int]:
        """Every Rating under its field name (quality, relevance, completeness, accuracy), in field order.

        Named after the Ratings, not the Dimensions: `quality` is the overall Rating, not a Dimension.
        """
        return {name: getattr(self, name) for name in type(self).model_fields if name != "reason"}
