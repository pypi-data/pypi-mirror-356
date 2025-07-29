import tempfile
from pathlib import Path

import nbconvert


def convert(ipynb_path: Path) -> Path:
    """Convert a Jupyter Notebook to a Python file."""
    exporter = nbconvert.PythonExporter()
    code, _ = exporter.from_filename(str(ipynb_path))
    py_path = Path(tempfile.gettempdir()) / (ipynb_path.stem + ".py")
    py_path.write_text(code)
    return py_path.resolve()


def convert_ipynbs(paths: list[Path]) -> list[Path]:
    """Convert Jupyter Notebooks to Python files."""
    tmp_files = []
    for path in paths:
        if path.is_file() and path.suffix == ".ipynb":
            tmp_files.append(convert(path))
        elif path.is_dir():
            for p in path.rglob("*.ipynb"):
                tmp_files.append(convert(p))
    return tmp_files