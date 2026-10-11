import pytest
from langchain_core.language_models import BaseChatModel

from orchestration.config import load_settings
from orchestration.llm import build_chat_model
from tests.keys import requires_keys


@pytest.mark.parametrize("model_name", ["gpt-4o-mini", "gpt-4.1"])
def test_builds_chat_model_for_each_role_without_network(model_name):
    model = build_chat_model(model_name, api_key="sk-test", temperature=0.0)

    assert isinstance(model, BaseChatModel)
    assert model.model_name == model_name
    assert model.temperature == 0.0


def test_passes_the_api_key_to_the_model():
    model = build_chat_model("gpt-4o-mini", api_key="sk-role", temperature=0.3)

    assert model.openai_api_key.get_secret_value() == "sk-role"
    assert model.temperature == 0.3


@pytest.mark.integration
@requires_keys("OPENAI_API_KEY")
def test_router_model_answers_a_real_prompt():
    settings = load_settings()
    model = build_chat_model(
        settings.router_model,
        api_key=settings.openai_api_key.get_secret_value(),
        temperature=settings.llm_temperature,
    )

    reply = model.invoke("Reply with the single word: pong")

    assert "pong" in reply.content.lower()
