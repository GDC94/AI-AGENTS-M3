"""Application settings read once from the environment and the .env file."""

from typing import Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: SecretStr

    router_model: str = Field(default="gpt-4o-mini", min_length=1)
    specialist_model: str = Field(default="gpt-4o-mini", min_length=1)
    judge_model: str = Field(default="gpt-4.1", min_length=1)
    embedding_model: str = Field(default="text-embedding-3-small", min_length=1)
    llm_temperature: float = Field(default=0.0, ge=0.0, le=2.0)

    similarity_threshold: float = Field(default=0.325, ge=0.0, le=1.0)
    retrieval_top_k: int = Field(default=4, ge=1)
    chunk_max_tokens: int = Field(default=800, ge=1)
    chunk_overlap_tokens: int = Field(default=120, ge=0)

    langfuse_public_key: SecretStr | None = None
    langfuse_secret_key: SecretStr | None = None
    langfuse_host: str | None = None

    @model_validator(mode="after")
    def _overlap_smaller_than_chunk(self) -> Self:
        if self.chunk_overlap_tokens >= self.chunk_max_tokens:
            raise ValueError("chunk_overlap_tokens must be smaller than chunk_max_tokens")
        return self


def load_settings() -> Settings:
    """Read settings from the environment and the .env file in the working directory."""
    return Settings()
