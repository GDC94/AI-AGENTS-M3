from orchestration.area import Area
from orchestration.checks import SweepPoint, TestQuery, sweep_threshold
from orchestration.section import RetrievedSection


def make_test_query(id, area, type, section=None):
    return TestQuery(
        id=id,
        query=f"query {id}",
        expected_area=area,
        expected_section=section,
        asker="client",
        type=type,
        split="calibration",
    )


def fake_retrieve(*pairs):
    """A retrieval callable that always returns the given (title, similarity) pairs."""
    sections = [RetrievedSection(title=title, text="t", similarity=sim) for title, sim in pairs]
    calls = []

    def retrieve(query):
        calls.append(query)
        return sections

    retrieve.calls = calls
    return retrieve


def test_one_point_per_threshold_with_counts_that_follow_the_similarities():
    retrieve_by_area = {
        Area.HR: fake_retrieve(("Vacaciones", 0.60), ("Otra", 0.30)),
        Area.TECH: fake_retrieve(("Exportar", 0.50)),
        Area.FINANCE: fake_retrieve(("Mascotas", 0.40)),
    }
    test_queries = [
        make_test_query("hr-01", "hr", "direct", "Vacaciones"),
        make_test_query("tech-01", "tech", "frontier", "Exportar"),
        make_test_query("fin-01", "finance", "unanswerable"),
        make_test_query("oos-01", "out_of_scope", "out_of_scope"),
    ]

    points = sweep_threshold(retrieve_by_area, test_queries, [0.3, 0.5, 0.7])

    assert points == [
        SweepPoint(threshold=0.3, retrieval_hits=2, answerable=2, correct_abstentions=0, unanswerable=1),
        SweepPoint(threshold=0.5, retrieval_hits=2, answerable=2, correct_abstentions=1, unanswerable=1),
        SweepPoint(threshold=0.7, retrieval_hits=0, answerable=2, correct_abstentions=1, unanswerable=1),
    ]


def test_a_section_with_similarity_equal_to_the_threshold_is_kept():
    retrieve_by_area = {Area.HR: fake_retrieve(("Vacaciones", 0.5))}
    test_queries = [make_test_query("hr-01", "hr", "direct", "Vacaciones")]

    [point] = sweep_threshold(retrieve_by_area, test_queries, [0.5])

    assert point.retrieval_hits == 1


def test_a_hit_needs_the_expected_section_not_just_any_section():
    retrieve_by_area = {Area.HR: fake_retrieve(("Otra", 0.9))}
    test_queries = [make_test_query("hr-01", "hr", "direct", "Vacaciones")]

    [point] = sweep_threshold(retrieve_by_area, test_queries, [0.1])

    assert point.retrieval_hits == 0


def test_each_query_is_retrieved_once_from_its_expected_area_only():
    hr = fake_retrieve(("Vacaciones", 0.6))
    tech = fake_retrieve(("Exportar", 0.6))
    test_queries = [make_test_query("hr-01", "hr", "direct", "Vacaciones")]

    sweep_threshold({Area.HR: hr, Area.TECH: tech}, test_queries, [0.1, 0.2, 0.3])

    assert hr.calls == ["query hr-01"]
    assert tech.calls == []
