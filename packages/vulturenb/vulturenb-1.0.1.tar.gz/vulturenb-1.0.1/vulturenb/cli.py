import contextlib
import sys
from pathlib import Path

from loguru import logger

from vulturenb.notebook_converter import convert_ipynbs
from vulturenb.printer import print_unused_code
from vulturenb.vulture_runner import filter_duplicates, find_unused_code


def main() -> None:
    """Run the main function of the CLI."""
    if len(sys.argv) <= 1:
        logger.error("No input paths provided. Exiting.")
        return

    input_paths: list[Path] = [Path(p).resolve() for p in sys.argv[1:]]
    tmp_py_files = convert_ipynbs(input_paths)
    all_paths = input_paths + tmp_py_files

    unused_code = find_unused_code(all_paths)
    filtered = filter_duplicates(unused_code)

    print_unused_code(filtered, input_paths)

    for f in tmp_py_files:
        with contextlib.suppress(Exception):
            f.unlink()


if __name__ == "__main__":
    main()