"""The single Langfuse client. The LangChain callback handler finds it without parameters."""

from langfuse import Langfuse


def init_langfuse(public_key: str, secret_key: str, host: str | None) -> Langfuse:
    """Initialise the Langfuse client from three explicit values (None host uses the SDK default)."""
    return Langfuse(public_key=public_key, secret_key=secret_key, host=host)
