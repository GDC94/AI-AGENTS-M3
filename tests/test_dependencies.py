import ast
import re
import sys
import tomllib
from importlib.metadata import packages_distributions
from pathlib import Path

import orchestration

PACKAGE_ROOT = Path(orchestration.__file__).parent
REPO_ROOT = PACKAGE_ROOT.parents[1]
TESTS_ROOT = REPO_ROOT / "tests"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"


def normalize_distribution(name: str) -> str:
    return name.lower().replace("_", "-")


def declared_distributions(groups: tuple[str, ...] = ()) -> set[str]:
    pyproject = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
    requirements = list(pyproject["project"]["dependencies"])
    for group in groups:
        requirements.extend(pyproject["dependency-groups"][group])
    return {normalize_distribution(re.match(r"[A-Za-z0-9_.-]+", requirement).group()) for requirement in requirements}


def imported_top_level_modules(root: Path) -> set[str]:
    modules = set()
    for path in root.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                modules.add(node.module.split(".")[0])
            elif isinstance(node, ast.Import):
                modules.update(alias.name.split(".")[0] for alias in node.names)
    return modules - set(sys.stdlib_module_names) - {"orchestration", "tests"}


def undeclared_modules(root: Path, declared: set[str]) -> list[str]:
    providers = packages_distributions()
    return sorted(
        module
        for module in imported_top_level_modules(root)
        if not any(normalize_distribution(distribution) in declared for distribution in providers.get(module, []))
    )


def test_every_module_the_source_imports_is_a_declared_dependency():
    assert undeclared_modules(PACKAGE_ROOT, declared_distributions()) == []


def test_every_module_the_tests_import_is_a_declared_dependency_or_dev_dependency():
    assert undeclared_modules(TESTS_ROOT, declared_distributions(groups=("dev",))) == []
