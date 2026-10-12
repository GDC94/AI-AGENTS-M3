import pytest
from pydantic import ValidationError

from orchestration.config import load_settings

ENV_VARS = (
    "OPENAI_API_KEY",
    "ROUTER_MODEL",
    "SPECIALIST_MODEL",
    "JUDGE_MODEL",
    "EMBEDDING_MODEL",
    "LLM_TEMPERATURE",
    "SIMILARITY_THRESHOLD",
    "RETRIEVAL_TOP_K",
    "CHUNK_MAX_TOKENS",
    "CHUNK_OVERLAP_TOKENS",
    "LANGFUSE_PUBLIC_KEY",
    "LANGFUSE_SECRET_KEY",
    "LANGFUSE_HOST",
)


@pytest.fixture(autouse=True)
def isolated_env(monkeypatch, tmp_path):
    """Run each test with no settings in the environment and no .env file."""
    for var in ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.chdir(tmp_path)


def test_defaults_when_only_openai_key_is_set(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    settings = load_settings()

    assert settings.openai_api_key.get_secret_value() == "sk-test"
    assert settings.router_model == "gpt-4o-mini"
    assert settings.specialist_model == "gpt-4o-mini"
    assert settings.judge_model == "gpt-4.1"
    assert settings.embedding_model == "text-embedding-3-small"
    assert settings.llm_temperature == 0.0
    assert settings.similarity_threshold == 0.325
    assert settings.retrieval_top_k == 4
    assert settings.chunk_max_tokens == 800
    assert settings.chunk_overlap_tokens == 120
    assert settings.langfuse_public_key is None
    assert settings.langfuse_secret_key is None
    assert settings.langfuse_host is None


def test_every_variable_is_read_from_the_environment(monkeypatch):
    values = {
        "OPENAI_API_KEY": "sk-env",
        "ROUTER_MODEL": "router-x",
        "SPECIALIST_MODEL": "specialist-x",
        "JUDGE_MODEL": "judge-x",
        "EMBEDDING_MODEL": "embedding-x",
        "LLM_TEMPERATURE": "0.5",
        "SIMILARITY_THRESHOLD": "0.6",
        "RETRIEVAL_TOP_K": "5",
        "CHUNK_MAX_TOKENS": "500",
        "CHUNK_OVERLAP_TOKENS": "50",
        "LANGFUSE_PUBLIC_KEY": "pk-lf",
        "LANGFUSE_SECRET_KEY": "sk-lf",
        "LANGFUSE_HOST": "https://langfuse.example",
    }
    for name, value in values.items():
        monkeypatch.setenv(name, value)

    settings = load_settings()

    assert settings.openai_api_key.get_secret_value() == "sk-env"
    assert settings.router_model == "router-x"
    assert settings.specialist_model == "specialist-x"
    assert settings.judge_model == "judge-x"
    assert settings.embedding_model == "embedding-x"
    assert settings.llm_temperature == 0.5
    assert settings.similarity_threshold == 0.6
    assert settings.retrieval_top_k == 5
    assert settings.chunk_max_tokens == 500
    assert settings.chunk_overlap_tokens == 50
    assert settings.langfuse_public_key.get_secret_value() == "pk-lf"
    assert settings.langfuse_secret_key.get_secret_value() == "sk-lf"
    assert settings.langfuse_host == "https://langfuse.example"


def test_reads_values_from_dotenv_file(tmp_path):
    (tmp_path / ".env").write_text("OPENAI_API_KEY=sk-dotenv\nJUDGE_MODEL=judge-dotenv\n")

    settings = load_settings()

    assert settings.openai_api_key.get_secret_value() == "sk-dotenv"
    assert settings.judge_model == "judge-dotenv"


def test_missing_openai_key_fails_validation():
    with pytest.raises(ValidationError, match="openai_api_key"):
        load_settings()


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("LLM_TEMPERATURE", "3"),
        ("SIMILARITY_THRESHOLD", "1.5"),
        ("RETRIEVAL_TOP_K", "0"),
        ("CHUNK_MAX_TOKENS", "0"),
        ("CHUNK_OVERLAP_TOKENS", "-1"),
    ],
)
def test_out_of_range_values_fail_validation(monkeypatch, name, value):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv(name, value)

    with pytest.raises(ValidationError):
        load_settings()


def test_overlap_must_be_smaller_than_chunk_size(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("CHUNK_MAX_TOKENS", "100")
    monkeypatch.setenv("CHUNK_OVERLAP_TOKENS", "100")

    with pytest.raises(ValidationError):
        load_settings()


def test_secrets_are_not_shown_in_repr(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-hidden")

    assert "sk-hidden" not in repr(load_settings())
