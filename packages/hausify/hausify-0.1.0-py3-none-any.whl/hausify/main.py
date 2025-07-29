import datetime as dt
import sys
from subprocess import run as subprocess_run
from typing import Optional

from hausify.args import parse_args
from hausify.runners import exec_black
from hausify.runners import exec_docformatter
from hausify.runners import exec_flake8
from hausify.runners import exec_isort
from hausify.runners import exec_mypy
from hausify.runners.runner import ToolResult
from hausify.timings import Timings
from hausify.util.filesystem import SourceTree


def main() -> None:
    args = parse_args()

    tree = SourceTree(
        args.rootdir,
        args.files,
        args.exclude_dir,
    )

    should_exit = False

    tool_timings: dict[str, Timings] = {}

    if args.tool == "all" or args.tool == "isort":
        tool_timings["isort"] = Timings()
        results = exec_isort(
            tree.rootdir,
            tree.source_files,
            exec_cmd=subprocess_run,
            mode=args.isort_mode,
        )
        tool_timings["isort"].stop()
        if any(result.success is False for result in results):
            should_exit = True
            print_results("ISORT", results)

    if args.tool == "all" or args.tool == "docformatter":
        tool_timings["docformatter"] = Timings()
        results = exec_docformatter(
            tree.rootdir,
            tree.source_files,
            exec_cmd=subprocess_run,
            mode=args.docformatter_mode,
        )
        tool_timings["docformatter"].stop()
        if any(result.success is False for result in results):
            should_exit = True
            print_results("DOCFORMATTER", results)

    if args.tool == "all" or args.tool == "mypy":
        tool_timings["mypy"] = Timings()
        results = exec_mypy(
            tree.rootdir,
            tree.source_files,
            exec_cmd=subprocess_run,
        )
        tool_timings["mypy"].stop()
        if any(result.success is False for result in results):
            should_exit = True
            print_results("MYPY", results)

    if args.tool == "all" or args.tool == "black":
        tool_timings["black"] = Timings()
        results = exec_black(
            tree.rootdir,
            tree.source_files,
            exec_cmd=subprocess_run,
            mode=args.black_mode,
        )
        tool_timings["black"].stop()
        if any(result.success is False for result in results):
            should_exit = True
            print_results("BLACK", results)

    if args.tool == "all" or args.tool == "flake8":
        tool_timings["flake8"] = Timings()
        results = exec_flake8(
            tree.rootdir,
            tree.source_files,
            exec_cmd=subprocess_run,
        )
        tool_timings["flake8"].stop()
        if any(result.success is False for result in results):
            should_exit = True
            print_results("FLAKE8", results)

    if should_exit:
        sys.exit(1)


def print_timings(timings: dict[str, Timings]) -> None:
    """Print timings for each tool."""
    print("\n\nTIMINGS:")
    print("=" * 20)
    for tool, timing in timings.items():
        if timing is not None:
            duration_ms = timing.duration_ms
            print(f"{tool.upper()}: {duration_ms} ms")
        else:
            print(f"{tool.upper()}: Not executed")
    print("=" * 20, "\n\n")


def print_errors(tool: str, errors: str) -> None:
    pass


def print_results(tool: str, results: list[ToolResult]) -> None:
    """Print errors for a specific tool."""
    print("|  ", "=" * 20)
    print("|   TOOL:", tool.upper())
    print("|  ", "=" * 20)
    for result in results:
        if not result.success:
            print(f"|   == ERRORS (from config: {result.config})")
            for error in result.errors:
                if error.strip() == "":
                    continue
                print(f"|        {error}")
    print("\n" * 2)


if __name__ == "__main__":
    main()
