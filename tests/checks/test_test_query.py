import json

import pytest
from pydantic import ValidationError

from orchestration.checks import load_test_queries


def make_item(id="hr-01", **overrides):
    item = {
        "id": id,
        "query": "¿Cuántos días de vacaciones tengo?",
        "expected_area": "hr",
        "expected_section": "Vacaciones",
        "asker": "staff",
        "type": "direct",
        "split": "calibration",
    }
    return item | overrides


def write_file(tmp_path, items):
    path = tmp_path / "test_queries.json"
    path.write_text(json.dumps(items), encoding="utf-8")
    return path


def test_loader_returns_only_the_requested_split(tmp_path):
    path = write_file(
        tmp_path,
        [make_item("a", split="calibration"), make_item("b", split="validation"), make_item("c")],
    )

    loaded = load_test_queries(path, "validation")

    assert [test_query.id for test_query in loaded] == ["b"]


def test_loader_reads_every_field(tmp_path):
    path = write_file(tmp_path, [make_item()])

    [test_query] = load_test_queries(path, "calibration")

    assert (test_query.query, test_query.expected_area, test_query.expected_section) == (
        "¿Cuántos días de vacaciones tengo?",
        "hr",
        "Vacaciones",
    )
    assert (test_query.asker, test_query.type, test_query.split) == ("staff", "direct", "calibration")


def test_expected_section_is_absent_for_out_of_scope_and_unanswerable(tmp_path):
    item = make_item(expected_area="out_of_scope", expected_section=None, type="out_of_scope")
    path = write_file(tmp_path, [item])

    [test_query] = load_test_queries(path, "calibration")

    assert test_query.expected_section is None


@pytest.mark.parametrize(
    "bad",
    [{"type": "tricky"}, {"split": "test"}, {"expected_area": "legal"}, {"asker": "robot"}],
)
def test_loader_rejects_unknown_values(tmp_path, bad):
    path = write_file(tmp_path, [make_item(**bad)])

    with pytest.raises(ValidationError):
        load_test_queries(path, "calibration")


def test_loader_rejects_an_unknown_requested_split(tmp_path):
    path = write_file(tmp_path, [make_item()])

    with pytest.raises(ValueError):
        load_test_queries(path, "holdout")


@pytest.mark.parametrize(
    "bad",
    [
        # out_of_scope type without the out_of_scope Area
        {"type": "out_of_scope", "expected_section": None},
        # out_of_scope Area on a type that reaches a Specialist
        {"expected_area": "out_of_scope", "expected_section": None},
        # direct or frontier without an expected Section
        {"type": "direct", "expected_section": None},
        {"type": "frontier", "expected_section": None},
        # unanswerable with an expected Section
        {"type": "unanswerable", "expected_section": "Vacaciones"},
        # out_of_scope with an expected Section
        {"type": "out_of_scope", "expected_area": "out_of_scope"},
    ],
)
def test_loader_rejects_inconsistent_type_area_and_section(tmp_path, bad):
    path = write_file(tmp_path, [make_item(**bad)])

    with pytest.raises(ValidationError):
        load_test_queries(path, "calibration")


def test_loader_accepts_the_consistent_combinations(tmp_path):
    items = [
        make_item("a", type="direct"),
        make_item("b", type="frontier"),
        make_item("c", type="unanswerable", expected_section=None),
        make_item("d", type="out_of_scope", expected_area="out_of_scope", expected_section=None),
    ]

    assert len(load_test_queries(write_file(tmp_path, items), "calibration")) == 4
