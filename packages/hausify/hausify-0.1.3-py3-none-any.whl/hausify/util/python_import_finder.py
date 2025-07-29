import ast
from pathlib import Path


class PythonImportFinder:
    """A class that finds import lines in a Python file.

    This uses the `ast` module to parse the Python file and identify
    import statements. It then provides methods for getting contiguous
    ranges of import blocks and trailing empty lines.
    """

    def __init__(self) -> None:
        self.lines: list[str] = []
        self.tree: ast.Module = ast.parse("")

    def load_source_file(self, filename: Path) -> None:
        """Load a source file into the finder."""

        with open(filename, "r", encoding="utf-8") as f:
            raw_file = f.read()
            self.lines = raw_file.splitlines()
            self.tree = ast.parse(raw_file, filename=filename)

    def load_source_string(
        self, source: str, filename: Path = Path("<string>")
    ) -> None:
        """Load a source string into the finder."""
        self.lines = source.splitlines()
        self.tree = ast.parse(source, filename=filename)

    def get_formatting_ranges(self) -> list[tuple[int, int]]:
        """Get the ranges of lines that should be formatted."""
        import_ranges = _get_import_line_ranges(self.tree)
        empty_ranges = _get_empty_line_ranges(self.lines)

        import_plus_trailing = _merge_trailing_empty_lines(
            import_ranges=import_ranges,
            empty_line_ranges=empty_ranges,
        )

        inverted_ranges = _invert_ranges(import_plus_trailing, len(self.lines))
        return inverted_ranges


def _merge_consecutive_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge consecutive ranges into single ranges."""
    if not ranges:
        return []

    sorted_ranges = sorted(ranges, key=lambda x: x[0])

    i = 0
    merged_ranges = []
    while i < len(sorted_ranges):
        start = sorted_ranges[i][0]
        end = sorted_ranges[i][1]

        j = i + 1
        while j < len(sorted_ranges) and sorted_ranges[j][0] <= end + 1:
            end = max(end, sorted_ranges[j][1])
            j += 1

        merged_ranges.append((start, end))
        i = j

    return merged_ranges


def _get_import_line_ranges(tree: ast.Module) -> list[tuple[int, int]]:
    """Get the line ranges of import statements in the AST."""
    import_lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            start_line = node.lineno
            end_line = node.end_lineno if node.end_lineno is not None else start_line
            import_lines.append((start_line, end_line))

    return _merge_consecutive_ranges(import_lines)


def _get_empty_line_ranges(source_lines: list[str]) -> list[tuple[int, int]]:
    empty_ranges = []
    i = 0
    for i, line in enumerate(source_lines):
        if line.strip() == "":
            empty_ranges.append((i + 1, i + 1))  # Store 1-based line numbers

    return _merge_consecutive_ranges(empty_ranges)


def _invert_ranges(
    ranges: list[tuple[int, int]], total_lines: int
) -> list[tuple[int, int]]:
    """Invert the ranges to get the lines that are not in the ranges."""
    if not ranges:
        return [(1, total_lines)]

    inverted_ranges = []
    last_end = 0

    for start, end in ranges:
        if start > last_end + 1:
            inverted_ranges.append((last_end + 1, start - 1))
        last_end = end

    if last_end < total_lines:
        inverted_ranges.append((last_end + 1, total_lines))

    return inverted_ranges


def _merge_trailing_empty_lines(
    import_ranges: list[tuple[int, int]],
    empty_line_ranges: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Merge trailing empty lines with import ranges."""
    if not import_ranges:
        return []

    if not empty_line_ranges:
        return import_ranges

    space_range_by_start = {start: (start, end) for start, end in empty_line_ranges}
    space_range_by_end = {end: (start, end) for start, end in empty_line_ranges}

    merged_ranges = []
    for start, end in import_ranges:

        if start - 1 in space_range_by_end:
            # start = space_range_by_end[start - 1][0]
            pass

        if end + 1 in space_range_by_start:
            end = space_range_by_start[end + 1][1]

        merged_ranges.append((start, end))

    # Now merge any consecutive ranges
    return _merge_consecutive_ranges(merged_ranges)
