import ast
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
