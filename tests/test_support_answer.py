from orchestration.judging import QualityVerdict
from orchestration.routing import Route
from orchestration.section import RetrievedSection
from orchestration.support_answer import SupportAnswer, format_support_answer

TRACE_URL = "https://langfuse.example/trace/abc"


def make_answer(**overrides) -> SupportAnswer:
    fields = {
        "query": "¿Cuántos días de vacaciones tengo?",
        "route": Route(reasoning="Es una cuestión de permisos.", target="hr"),
        "answer": "Tienes 22 días laborables.",
        "sections": [
            RetrievedSection(title="Vacaciones anuales", text="22 días.", similarity=0.8123),
            RetrievedSection(title="Permisos", text="Otros permisos.", similarity=0.5),
        ],
        "abstained": False,
        "verdict": QualityVerdict(reason="Respuesta fiel.", quality=9, relevance=10, completeness=8, accuracy=9),
        "trace_id": "abc",
    }
    return SupportAnswer(**(fields | overrides))


def test_text_shows_the_query_the_route_target_and_its_reasoning():
    text = format_support_answer(make_answer(), TRACE_URL)

    assert "¿Cuántos días de vacaciones tengo?" in text
    assert "hr" in text
    assert "Es una cuestión de permisos." in text


def test_text_lists_each_section_title_with_its_similarity_to_three_decimals():
    text = format_support_answer(make_answer(), TRACE_URL)

    assert "Vacaciones anuales" in text
    assert "0.812" in text
    assert "Permisos" in text
    assert "0.500" in text


def test_text_says_so_when_no_sections_were_used():
    text = format_support_answer(make_answer(sections=[]), TRACE_URL)

    assert "none" in text.lower()


def test_text_shows_the_answer_the_abstained_flag_and_the_trace_link():
    text = format_support_answer(make_answer(abstained=True), TRACE_URL)

    assert "Tienes 22 días laborables." in text
    assert "abstained: True" in text
    assert TRACE_URL in text


def test_text_notes_when_there_is_no_trace_link():
    text = format_support_answer(make_answer(), None)

    assert "no trace link" in text.lower()


def test_text_shows_every_rating_and_the_reason_of_the_quality_verdict():
    text = format_support_answer(make_answer(), TRACE_URL)

    assert "quality: 9" in text
    assert "relevance: 10" in text
    assert "completeness: 8" in text
    assert "accuracy: 9" in text
    assert "Respuesta fiel." in text


def test_text_has_no_verdict_block_when_the_answer_was_not_judged():
    text = format_support_answer(make_answer(verdict=None), TRACE_URL)

    assert "verdict" not in text.lower()
