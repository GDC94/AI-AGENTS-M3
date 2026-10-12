import ast
from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

from tests.keys import requires_keys

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_PATH = REPO_ROOT / "multi_agent_system.ipynb"

SECTION_HEADINGS = [
    "## 1. Setup and imports",
    "## 2. Document loading and vector stores",
    "## 3. Agent definition (Specialists)",
    "## 4. Orchestrator and routing",
    "## 5. Tests and examples",
    "## 6. Langfuse integration",
]


def read_notebook() -> nbformat.NotebookNode:
    return nbformat.read(NOTEBOOK_PATH, as_version=4)


def code_cells(notebook: nbformat.NotebookNode) -> list[nbformat.NotebookNode]:
    return [cell for cell in notebook.cells if cell.cell_type == "code"]


def test_notebook_has_the_six_section_headings_in_order():
    headings = [
        line
        for cell in read_notebook().cells
        if cell.cell_type == "markdown"
        for line in cell.source.splitlines()
        if line.startswith("## ")
    ]

    assert headings == SECTION_HEADINGS


def test_no_code_cell_defines_a_function_or_a_class():
    for cell in code_cells(read_notebook()):
        definitions = [
            node for node in ast.walk(ast.parse(cell.source)) if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef)
        ]
        assert definitions == [], cell.source


def test_the_last_code_cell_flushes_langfuse():
    last_cell = code_cells(read_notebook())[-1]

    assert ".flush()" in last_cell.source


@pytest.mark.integration
@requires_keys("OPENAI_API_KEY", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY")
def test_notebook_runs_top_to_bottom_without_errors():
    notebook = read_notebook()

    # Raises CellExecutionError if any cell fails; the executed copy is not written back.
    NotebookClient(
        notebook, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(REPO_ROOT)}}
    ).execute()
