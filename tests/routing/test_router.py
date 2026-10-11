import pytest

from orchestration.config import load_settings
from orchestration.llm import build_chat_model
from orchestration.routing import build_router
from tests.keys import requires_keys

# Sample Queries for this test only; they never enter the official Test Queries file.
SAMPLE_QUERIES = [
    ("¿Cuántos días de vacaciones me corresponden por año?", "hr"),
    ("Mi cuenta de la plataforma quedó bloqueada después de varios intentos.", "tech"),
    ("¿Dónde descargo la factura del último mes de nuestro organismo?", "finance"),
    ("¿Quién ganó el partido de fútbol de ayer?", "out_of_scope"),
]


@pytest.mark.integration
@requires_keys("OPENAI_API_KEY")
@pytest.mark.parametrize(("query", "expected_target"), SAMPLE_QUERIES)
def test_real_router_routes_sample_queries(query, expected_target):
    settings = load_settings()
    router = build_router(
        build_chat_model(
            settings.router_model,
            api_key=settings.openai_api_key.get_secret_value(),
            temperature=settings.llm_temperature,
        )
    )

    route = router.invoke(query)

    assert route.target == expected_target
    assert route.reasoning.strip()
