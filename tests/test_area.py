from orchestration.area import AREA_DESCRIPTIONS, Area


def test_area_has_exactly_hr_tech_and_finance():
    assert {area.value for area in Area} == {"hr", "tech", "finance"}


def test_area_values_are_plain_strings():
    assert Area.HR == "hr"
    assert Area("finance") is Area.FINANCE


def test_every_area_has_a_non_empty_ascii_description():
    assert set(AREA_DESCRIPTIONS) == set(Area)
    for description in AREA_DESCRIPTIONS.values():
        assert description.strip()
        assert description.isascii()
