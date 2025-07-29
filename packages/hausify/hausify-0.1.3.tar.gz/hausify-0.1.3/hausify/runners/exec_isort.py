import subprocess
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from pathlib import Path
from typing import Callable
from typing import Union

from hausify.runners.runner import PythonTool
from hausify.runners.runner import ToolCommand
from hausify.runners.runner import ToolResult


class IsortMode(str, Enum):
    FIX = "fix"
    CHECK = "check"


class IsortRunner(PythonTool):
    """Runner for the isort import sorter.

    This runner finds isort configuration files in the source tree and
    sad fasd fasdf asdf asdf asdf asdf asdf f asdf asdasdf. asdf asdf
    asdfasdf. asdf lkasjdflkjasdflkasjdf executes isort on the provided
    files.
    """

    _configs = [".isort.cfg", "pyproject.toml", "setup.cfg", "tox.ini"]

    def __init__(
        self,
        root: Path,
        files: list[Path],
        exec_cmd: Callable,
        mode: IsortMode = IsortMode.CHECK,
    ) -> None:
        self._mode = mode
        super().__init__(root, files, exec_cmd)

    def build_commands(self, config: Path, files: list[Path]) -> list[ToolCommand]:
        """Build an isort command for each file in the provided list."""
        cmd = ToolCommand(
            config=str(config),
            files=[str(f) for f in files],
            argv=[
                "isort",
            ],
        )
        if self._mode == IsortMode.CHECK:
            cmd.argv.append("--check")
            cmd.argv.append("--diff")

        if config.is_file():
            cmd.argv.extend(["--settings-path", str(config)])

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
            result.errors.extend(output.stdout.split("\n"))
        return result


def exec_isort(
    root: Path,
    files: list[Path],
    exec_cmd: Callable = subprocess.run,
    mode: IsortMode = IsortMode.CHECK,
) -> list[ToolResult]:
    runner = IsortRunner(root, files, exec_cmd, mode)
    with ThreadPoolExecutor() as executor:
        results = runner.execute(executor)
    return results
