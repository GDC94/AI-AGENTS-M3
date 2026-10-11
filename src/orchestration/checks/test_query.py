"""Test Queries: Queries with a known expected Route, read from the author's JSON file."""

import json
from pathlib import Path
from typing import Literal, get_args

from pydantic import BaseModel, Field, TypeAdapter

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
