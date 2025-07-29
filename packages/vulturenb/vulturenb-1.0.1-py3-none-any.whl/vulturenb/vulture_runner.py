from pathlib import Path

import vulture
import vulture.core


def find_unused_code(paths: list[Path]) -> list[vulture.core.Item]:
    """Call the vulture library to find unused code."""
    v = vulture.Vulture()
    v.scavenge([str(p) for p in paths])
    return v.get_unused_code()


def filter_duplicates(items: list[vulture.core.Item]) -> list[vulture.core.Item]:
    """Filter out duplicate items based on filename, first line number, and name."""
    seen = set()
    filtered = []
    for item in items:
        key = (item.filename, item.first_lineno, item.name)
        if key not in seen:
            seen.add(key)
            filtered.append(item)
    return filtered