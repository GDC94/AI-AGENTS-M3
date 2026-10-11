from orchestration.checks import TestQuery, abstained, retrieval_hit, routing_correct
from orchestration.routing import Route
from orchestration.section import RetrievedSection
from orchestration.support_answer import SupportAnswer


def make_test_query(**overrides):
    fields = {
        "id": "hr-01",
        "query": "¿Cuántos días de vacaciones tengo?",
        "expected_area": "hr",
        "expected_section": "Vacaciones",
        "asker": "staff",
        "type": "direct",
        "split": "calibration",
    }
    return TestQuery(**(fields | overrides))


def make_answer(target="hr", titles=("Vacaciones",), abstained=False):
    return SupportAnswer(
        query="q",
        route=Route(reasoning="r", target=target),
        answer="a",
        sections=[RetrievedSection(title=title, text="t", similarity=0.9) for title in titles],
        abstained=abstained,
        trace_id="t1",
    )


def test_routing_correct_when_target_equals_expected_area():
    assert routing_correct(make_answer(target="hr"), make_test_query(expected_area="hr")) is True


def test_routing_incorrect_for_a_route_to_the_wrong_area():
    assert routing_correct(make_answer(target="tech"), make_test_query(expected_area="hr")) is False


def test_routing_correct_for_out_of_scope_expected_and_routed():
    query = make_test_query(expected_area="out_of_scope", expected_section=None, type="out_of_scope")

    assert routing_correct(make_answer(target="out_of_scope", titles=()), query) is True


def test_retrieval_hit_when_expected_section_is_among_those_used():
    answer = make_answer(titles=("Otra", "Vacaciones"))

    assert retrieval_hit(answer, make_test_query()) is True


def test_retrieval_miss_when_expected_section_was_not_used():
    assert retrieval_hit(make_answer(titles=("Otra",)), make_test_query()) is False


def test_retrieval_miss_when_no_section_was_used():
    assert retrieval_hit(make_answer(titles=(), abstained=True), make_test_query()) is False


def test_retrieval_miss_when_the_test_query_has_no_expected_section():
    query = make_test_query(expected_section=None, type="unanswerable")

    assert retrieval_hit(make_answer(), query) is False


def test_abstained_is_true_when_the_answer_abstained():
    assert abstained(make_answer(titles=(), abstained=True), make_test_query()) is True


def test_abstained_is_false_when_the_answer_is_grounded_whatever_the_type():
    unanswerable = make_test_query(expected_section=None, type="unanswerable")

    assert abstained(make_answer(abstained=False), make_test_query()) is False
    assert abstained(make_answer(abstained=False), unanswerable) is False


def test_routing_incorrect_for_an_out_of_scope_query_routed_to_an_area():
    query = make_test_query(expected_area="out_of_scope", expected_section=None, type="out_of_scope")

    assert routing_correct(make_answer(target="hr"), query) is False
