import subprocess
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from pathlib import Path
from typing import Callable
from typing import Union

from hausify.runners.runner import PythonTool
from hausify.runners.runner import ToolCommand
from hausify.runners.runner import ToolResult


class DocFormatterMode(str, Enum):
    FIX = "fix"
    CHECK = "check"


class DocFormatterRunner(PythonTool):
    """Runner for the docformatter tool.

    This runner finds docformatter configuration files in the source
    tree and executes docformatter on the provided files.
    """

    _configs = ["pyproject.toml"]

    def __init__(
        self,
        root: Path,
        files: list[Path],
        exec_cmd: Callable,
        mode: DocFormatterMode = DocFormatterMode.CHECK,
    ) -> None:
        self._mode = mode
        super().__init__(root, files, exec_cmd)

    def build_commands(self, config: Path, files: list[Path]) -> list[ToolCommand]:
        """Build a docformatter command for each file in the provided list."""
        cmd = ToolCommand(
            config=str(config),
            files=[str(f) for f in files],
            argv=[
                "docformatter",
            ],
        )

        if self._mode == DocFormatterMode.CHECK:
            cmd.argv.append("--check")
            cmd.argv.append("--diff")
        else:
            cmd.argv.append("--in-place")

        if config.is_file():
            cmd.argv.extend(["--config", str(config)])

        cmd.argv.extend(str(f) for f in files)
        return [cmd]

    def handle_result(
        self,
        cmd: ToolCommand,
        output: Union[subprocess.CompletedProcess, subprocess.CalledProcessError],
    ) -> ToolResult:
        result = ToolResult(config=cmd.config, files=cmd.files)
        if isinstance(output, subprocess.CompletedProcess):
            result.success = output.returncode == 0
            result.logs.extend(output.stdout.split("\n"))
            if output.stderr:
                result.errors.extend(output.stderr.split("\n"))
        elif isinstance(output, subprocess.CalledProcessError):
            # If the command failed, we assume it was not successful
            result.success = False
            # result.logs.extend(output.stdout.split("\n"))
            result.errors.extend(output.stdout.split("\n"))
        return result


def exec_docformatter(
    root: Path,
    files: list[Path],
    exec_cmd: Callable = subprocess.run,
    mode: DocFormatterMode = DocFormatterMode.CHECK,
) -> list[ToolResult]:
    """Executes docformatter on the provided files."""
    runner = DocFormatterRunner(root, files, exec_cmd, mode)
    with ThreadPoolExecutor() as executor:
        results = runner.execute(executor)

    return results
