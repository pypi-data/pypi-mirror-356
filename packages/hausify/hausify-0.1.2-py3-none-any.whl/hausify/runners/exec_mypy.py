import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable
from typing import Union

from hausify.runners.runner import PythonTool
from hausify.runners.runner import ToolCommand
from hausify.runners.runner import ToolResult


class MyPyRunner(PythonTool):
    """Runner for the mypy type checker.

    This runner finds mypy configuration files in the source tree and
    executes mypy on the provided files, excluding any test files (those
    ending with _test.py).
    """

    _configs = ["mypy.ini", ".mypy.ini", "pyproject.toml", "setup.cfg"]

    def build_commands(self, config: Path, files: list[Path]) -> list[ToolCommand]:
        """Build mypy command for a set of files with a specific config."""

        non_test_files = [str(f) for f in files if not f.name.endswith("_test.py")]

        cmd = ToolCommand(
            config=str(config),
            files=non_test_files,
            argv=[
                "mypy",
                "--show-error-codes",
                "--show-column-numbers",
            ],
            env={
                "MYPY_FORCE_COLOR": "1",
            },
        )

        if config.is_file():
            cmd.argv.append(f"--config-file={str(config)}")

        cmd.argv.extend(non_test_files)
        return [cmd]

    def handle_result(
        self,
        cmd: ToolCommand,
        output: Union[subprocess.CompletedProcess, subprocess.CalledProcessError],
    ) -> ToolResult:
        result = ToolResult(
            config=cmd.config,
            files=cmd.files,
        )

        if isinstance(output, subprocess.CompletedProcess):
            result.success = True
            result.logs.extend(output.stdout.split("\n"))
        elif isinstance(output, subprocess.CalledProcessError):
            result.success = False
            if output.stderr != "":
                result.logs.extend(output.stdout.split("\n"))
                result.errors.extend(output.stderr.split("\n"))
            else:
                result.errors.extend(output.stdout.split("\n"))
        return result


def exec_mypy(
    root: Path,
    files: list[Path],
    exec_cmd: Callable = subprocess.run,
) -> list[ToolResult]:
    runner = MyPyRunner(root, files, exec_cmd=exec_cmd)
    with ThreadPoolExecutor() as exec:
        results = runner.execute(exec)

    return results
