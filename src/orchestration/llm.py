"""Chat model factory: the composition layer calls it once per role."""

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


def build_chat_model(model_name: str, api_key: str, temperature: float) -> BaseChatModel:
    """Build an OpenAI chat model. No network call happens until the model is invoked."""
    return ChatOpenAI(model=model_name, api_key=api_key, temperature=temperature)
