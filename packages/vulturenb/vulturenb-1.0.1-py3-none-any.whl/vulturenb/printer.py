import re
from pathlib import Path

import vulture.core
from rich.console import Console
from rich.table import Table

console = Console()

type_colors = {
    "attribute": "bold #00ffff",
    "class": "bold #ff00ff",
    "function": "bold #1e90ff",
    "import": "bold #32cd32",
    "method": "bold #ffd700",
    "property": "bold #ff4500",
    "variable": "bold #f0e68c",
    "unreachable_code": "bold #696969",
}


def color_message(msg: str) -> str:
    """Colorize the message in the vulture output for better readability."""
    return re.sub(r"'([^']+)'", r"'[green]\1[/]'", msg)


def print_unused_code(items: list[vulture.core.Item], base_paths: list[Path]) -> None:
    """Format and print the unused code items in a table."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Type", style="bold", width=18)
    table.add_column("File", style="cyan", overflow="fold")
    table.add_column("Line", style="yellow", width=6, justify="right")
    table.add_column("Name", style="green", overflow="fold")
    table.add_column("Message", overflow="fold")

    for item in items:
        color = type_colors.get(item.typ, "white")
        typ_text = f"[{color}]{item.typ}[/]"

        for base in base_paths:
            try:
                short_path = Path(item.filename).relative_to(base)
                break
            except ValueError:
                continue
        else:
            short_path = Path(item.filename).name

        table.add_row(
            typ_text,
            str(short_path),
            str(item.first_lineno),
            item.name,
            color_message(item.message),
        )

    console.print(table)