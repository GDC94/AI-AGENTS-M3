import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIREMENTS_PATH = REPO_ROOT / "requirements.txt"

ASSIGNMENT_PACKAGES = {
    "langchain",
    "langchain-openai",
    "langfuse",
    "openai",
    "chromadb",
    "tiktoken",
    "python-dotenv",
    "jupyter",
    "ipykernel",
}


def read_pinned_packages() -> set[str]:
    pinned = re.findall(r"^([A-Za-z0-9_.-]+)==", REQUIREMENTS_PATH.read_text(), flags=re.MULTILINE)
    return {name.lower().replace("_", "-") for name in pinned}


def test_requirements_file_pins_the_nine_packages_the_assignment_lists():
    assert ASSIGNMENT_PACKAGES <= read_pinned_packages()
