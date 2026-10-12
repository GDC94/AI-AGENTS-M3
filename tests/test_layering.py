import ast
import json
from pathlib import Path

import pytest

import orchestration

PACKAGE_ROOT = Path(orchestration.__file__).parent
BUSINESS_PACKAGES = ("routing", "specialists", "judging", "checks")
INFRASTRUCTURE = ("langfuse", "chromadb", "langchain_chroma", "langgraph")


def imported_modules(path: Path) -> set[str]:
    modules = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
        elif isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
    return modules


@pytest.mark.parametrize("package", BUSINESS_PACKAGES)
def test_business_package_imports_no_infrastructure(package):
    offenders = [
        f"{path.relative_to(PACKAGE_ROOT)}: {module}"
        for path in (PACKAGE_ROOT / package).rglob("*.py")
        for module in imported_modules(path)
        if module.split(".")[0] in INFRASTRUCTURE
    ]

    assert offenders == []


def calls_load_settings(path: Path) -> bool:
    return any(
        isinstance(node, ast.Call)
        and (getattr(node.func, "id", None) == "load_settings" or getattr(node.func, "attr", None) == "load_settings")
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
    )


def test_only_the_composition_module_reads_settings():
    offenders = [
        str(path.relative_to(PACKAGE_ROOT))
        for path in PACKAGE_ROOT.rglob("*.py")
        if calls_load_settings(path)
    ]

    assert offenders == ["multi_agent_system.py"]


def test_no_test_query_text_appears_in_the_source():
    test_queries_file = PACKAGE_ROOT.parents[1] / "test_queries.json"
    queries = [entry["query"] for entry in json.loads(test_queries_file.read_text(encoding="utf-8"))]
    sources = {path: path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.rglob("*.py")}

    offenders = [
        f"{path.relative_to(PACKAGE_ROOT)}: {query}" for path, text in sources.items() for query in queries if query in text
    ]

    assert queries
    assert offenders == []
