from dataclasses import dataclass

import pytest


def test_python_import_finder_returns_correct_non_import_ranges():
    @dataclass
    class TestCase:
        name: str
        source_lines: list[str]
        expected_ranges: list[tuple[int, int]]

        @property
        def source(self) -> str:
            return "\n".join(self.source_lines)

    TEST_CASES: list[TestCase] = [
        TestCase(
            name="Basic imports",
            source_lines=[
                "import os",
                "import sys",
                "",
                "def foo():",
                "    pass",
            ],
            expected_ranges=[(4, 5)],
        ),
        TestCase(
            name="Imports inside function",
            source_lines=[
                "def foo():",
                "    import os",
                "    import sys",
                "    ",
                "    ",
                "    # a comment",
                "    2 + 2",
                "    return 42",
            ],
            expected_ranges=[(1, 1), (6, 8)],
        ),
    ]

    from hausify.util.python_import_finder import PythonImportFinder

    for test_case in TEST_CASES:
        finder = PythonImportFinder()
        finder.load_source_string(test_case.source)
        actual_ranges = finder.get_formatting_ranges()
        assert (
            actual_ranges == test_case.expected_ranges
        ), f"Failed on {test_case.name}: expected {test_case.expected_ranges}, got {actual_ranges}"


def test__merge_consecutive_ranges_success_cases():
    @dataclass
    class TestCase:
        name: str
        input_ranges: list[tuple[int, int]]
        expected_ranges: list[tuple[int, int]]

    TEST_CASES: list[TestCase] = [
        TestCase(
            name="No ranges",
            input_ranges=[],
            expected_ranges=[],
        ),
        TestCase(
            name="Single range",
            input_ranges=[(1, 2)],
            expected_ranges=[(1, 2)],
        ),
        TestCase(
            name="Consecutive ranges",
            input_ranges=[(1, 2), (3, 4)],
            expected_ranges=[(1, 4)],
        ),
        TestCase(
            name="Non-consecutive",
            input_ranges=[(1, 2), (4, 5)],
            expected_ranges=[(1, 2), (4, 5)],
        ),
        TestCase(
            name="Overlapping",
            input_ranges=[(1, 4), (3, 6)],
            expected_ranges=[(1, 6)],
        ),
        TestCase(
            name="Unordered, all merge",
            input_ranges=[(5, 7), (1, 3), (4, 4)],
            expected_ranges=[(1, 7)],
        ),
        TestCase(
            name="Single lines",
            input_ranges=[(1, 1), (2, 2), (4, 4), (5, 5)],
            expected_ranges=[(1, 2), (4, 5)],
        ),
    ]

    from hausify.util.python_import_finder import _merge_consecutive_ranges

    for test_case in TEST_CASES:
        actual_ranges = _merge_consecutive_ranges(test_case.input_ranges)
        assert (
            actual_ranges == test_case.expected_ranges
        ), f"Failed on {test_case.name}: expected {test_case.expected_ranges}, got {actual_ranges}"


def test__get_import_line_ranges_success_cases():
    @dataclass
    class TestCase:
        name: str
        input_lines: list[str]
        expected_ranges: list[tuple[int, int]]

        @property
        def source(self) -> str:
            return "\n".join(self.input_lines)

    TEST_CASES: list[TestCase] = [
        TestCase(
            name="Basic imports",
            input_lines=[
                "import os",
                "import sys",
                "",
                "def foo():",
                "    pass",
            ],
            expected_ranges=[
                (1, 2),
            ],
        ),
        TestCase(
            name="Imports inside function",
            input_lines=[
                "def foo():",
                "    import os",
                "    import sys",
                "    pass",
            ],
            expected_ranges=[
                (2, 3),
            ],
        ),
        TestCase(
            name="No imports",
            input_lines=[
                "def foo():",
                "    pass",
            ],
            expected_ranges=[],
        ),
        TestCase(
            name="Multiple imports with empty lines",
            input_lines=[
                "import os",
                "",
                "",
                "import sys",
                "",
                "def foo():",
                "    pass",
            ],
            expected_ranges=[
                (1, 1),
                (4, 4),
            ],
        ),
    ]

    from ast import parse

    from hausify.util.python_import_finder import _get_import_line_ranges

    for test_case in TEST_CASES:
        ast = parse(test_case.source)
        actual_ranges = _get_import_line_ranges(ast)
        assert (
            actual_ranges == test_case.expected_ranges
        ), f"Failed on {test_case.name}: expected {test_case.expected_ranges}, got {actual_ranges}"


def test__get_empty_line_ranges_success_cases():
    @dataclass
    class TestCase:
        name: str
        input_lines: list[str]
        expected_ranges: list[tuple[int, int]]

    TEST_CASES: list[TestCase] = [
        TestCase(
            name="No empty lines",
            input_lines=[
                "def foo():",
                "    pass",
            ],
            expected_ranges=[],
        ),
        TestCase(
            name="Single empty line",
            input_lines=[
                "def foo():",
                "",
                "    pass",
            ],
            expected_ranges=[(2, 2)],
        ),
        TestCase(
            name="Multiple consecutive empty lines",
            input_lines=[
                "def foo():",
                "",
                "",
                "    pass",
            ],
            expected_ranges=[(2, 3)],
        ),
        TestCase(
            name="Empty lines at start and end",
            input_lines=[
                "",
                "def foo():",
                "",
                "    pass",
                "",
            ],
            expected_ranges=[(1, 1), (3, 3), (5, 5)],
        ),
        TestCase(
            name="Multiple empty lines with code in between",
            input_lines=[
                "def foo():",
                "",
                "    pass",
                "",
                "",
                "def bar():",
                "",
            ],
            expected_ranges=[(2, 2), (4, 5), (7, 7)],
        ),
    ]

    from hausify.util.python_import_finder import _get_empty_line_ranges

    for test_case in TEST_CASES:
        actual_ranges = _get_empty_line_ranges(test_case.input_lines)
        assert (
            actual_ranges == test_case.expected_ranges
        ), f"Failed on {test_case.name}: expected {test_case.expected_ranges}, got {actual_ranges}"


def test__invert_ranges_success_cases():
    @dataclass
    class TestCase:
        name: str
        input_ranges: list[tuple[int, int]]
        total_lines: int
        expected_ranges: list[tuple[int, int]]

    TEST_CASES: list[TestCase] = [
        TestCase(
            name="No ranges",
            input_ranges=[],
            total_lines=5,
            expected_ranges=[(1, 5)],
        ),
        TestCase(
            name="Single range",
            input_ranges=[(2, 3)],
            total_lines=5,
            expected_ranges=[(1, 1), (4, 5)],
        ),
        TestCase(
            name="Multiple ranges",
            input_ranges=[(1, 2), (4, 5)],
            total_lines=5,
            expected_ranges=[(3, 3)],
        ),
        TestCase(
            name="Trailing includes",
            input_ranges=[(1, 4)],
            total_lines=10,
            expected_ranges=[(5, 10)],
        ),
    ]

    from hausify.util.python_import_finder import _invert_ranges

    for test_case in TEST_CASES:
        actual_ranges = _invert_ranges(test_case.input_ranges, test_case.total_lines)
        assert (
            actual_ranges == test_case.expected_ranges
        ), f"Failed on {test_case.name}: expected {test_case.expected_ranges}, got {actual_ranges}"


def test__merge_trailing_empty_lines_success_cases():
    @dataclass
    class TestCase:
        name: str
        import_ranges: list[tuple[int, int]]
        empty_line_ranges: list[tuple[int, int]]
        expected_ranges: list[tuple[int, int]]

    TEST_CASES: list[TestCase] = [
        TestCase(
            name="No imports",
            import_ranges=[],
            empty_line_ranges=[(1, 1)],
            expected_ranges=[],
        ),
        TestCase(
            name="No empty lines",
            import_ranges=[(1, 2)],
            empty_line_ranges=[],
            expected_ranges=[(1, 2)],
        ),
        TestCase(
            name="Merge single import with trailing empty lines",
            import_ranges=[(1, 2)],
            empty_line_ranges=[(3, 4)],
            expected_ranges=[(1, 4)],
        ),
        TestCase(
            name="Multiple imports with trailing empty lines",
            import_ranges=[(1, 2), (10, 20)],
            empty_line_ranges=[(3, 6), (21, 30)],
            expected_ranges=[(1, 6), (10, 30)],
        ),
    ]

    from hausify.util.python_import_finder import _merge_trailing_empty_lines

    for test_case in TEST_CASES:
        actual_ranges = _merge_trailing_empty_lines(
            test_case.import_ranges,
            test_case.empty_line_ranges,
        )
        assert (
            actual_ranges == test_case.expected_ranges
        ), f"Failed on {test_case.name}: expected {test_case.expected_ranges}, got {actual_ranges}"
