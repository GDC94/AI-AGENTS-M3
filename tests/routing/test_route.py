from typing import get_args

from orchestration.area import Area
from orchestration.routing import Route


def test_route_targets_are_the_areas_plus_out_of_scope():
    targets = set(get_args(Route.model_fields["target"].annotation))

    assert targets == {area.value for area in Area} | {"out_of_scope"}


def test_reasoning_comes_before_target():
    assert list(Route.model_fields) == ["reasoning", "target"]
