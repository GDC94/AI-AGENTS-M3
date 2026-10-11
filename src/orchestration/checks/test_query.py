"""Test Queries: Queries with a known expected Route, read from the author's JSON file."""

import json
from pathlib import Path
from typing import Literal, get_args

from pydantic import BaseModel, Field, TypeAdapter, model_validator

from orchestration.routing import RouteTarget

AskerKind = Literal["client", "staff"]
QueryType = Literal["direct", "frontier", "out_of_scope", "unanswerable"]
Split = Literal["calibration", "validation"]


class TestQuery(BaseModel):
    __test__ = False  # not a pytest class, despite the name

    id: str = Field(min_length=1)
    query: str = Field(min_length=1)
    expected_area: RouteTarget
    # Absent for out_of_scope and unanswerable Test Queries.
    expected_section: str | None = None
    asker: AskerKind
    type: QueryType
    split: Split

    @model_validator(mode="after")
    def check_fields_agree(self) -> "TestQuery":
        if (self.type == "out_of_scope") != (self.expected_area == "out_of_scope"):
            raise ValueError("type is out_of_scope if and only if expected_area is out_of_scope")
        if (self.expected_section is not None) != self.is_answerable:
            raise ValueError("expected_section is present if and only if type is direct or frontier")
        return self

    @property
    def is_answerable(self) -> bool:
        """The Knowledge Base holds the answer (direct or frontier)."""
        return self.type in ("direct", "frontier")

    @property
    def is_unanswerable(self) -> bool:
        """The Query has an Area but its Knowledge Base holds no answer."""
        return self.type == "unanswerable"


def load_test_queries(path: Path | str, split: Split) -> list[TestQuery]:
    """Read the JSON file (a list of Test Queries) and keep only the requested split.

    Every item is validated, whatever its split, so a typo in the validation split
    is found while calibrating.
    """
    if split not in get_args(Split):
        raise ValueError(f"Unknown split {split!r}; expected one of {get_args(Split)}")
    items = json.loads(Path(path).read_text(encoding="utf-8"))
    test_queries = TypeAdapter(list[TestQuery]).validate_python(items)
    return [test_query for test_query in test_queries if test_query.split == split]
