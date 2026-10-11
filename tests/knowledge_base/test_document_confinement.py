import ast
from pathlib import Path

import orchestration

PACKAGE_ROOT = Path(orchestration.__file__).parent
KNOWLEDGE_BASE = PACKAGE_ROOT / "knowledge_base"


def imported_names(path: Path) -> set[str]:
    names = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom):
            names.update(f"{node.module}.{alias.name}" for alias in node.names)
        elif isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
    return names


def test_langchain_document_is_not_imported_outside_the_knowledge_base():
    offenders = [
        path.relative_to(PACKAGE_ROOT)
        for path in PACKAGE_ROOT.rglob("*.py")
        if KNOWLEDGE_BASE not in path.parents
        and any(name.endswith(".Document") or name.endswith(".documents") for name in imported_names(path))
    ]

    assert offenders == []
