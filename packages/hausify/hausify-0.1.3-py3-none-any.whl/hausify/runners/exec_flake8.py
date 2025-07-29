import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable
from typing import Union

from hausify.runners.runner import PythonTool
from hausify.runners.runner import ToolCommand
from hausify.runners.runner import ToolResult


class Flake8Runner(PythonTool):
    """Runner for the Flake8 linter.

    This runner finds Flake8 configuration files in the source tree and
    executes Flake8 on the provided files.
    """

    _configs = [".flake8", "setup.cfg", "tox.ini"]

    def build_commands(self, config: Path, files: list[Path]) -> list[ToolCommand]:
        """Build a Flake8 command for each file in the provided list."""
        cmd = ToolCommand(
            config=str(config),
            files=[str(f) for f in files],
            argv=["flake8", "--color=always"],
        )
        if config.is_file():
            cmd.argv.extend(["--config", str(config)])
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
        elif isinstance(output, subprocess.CalledProcessError):
            result.success = False
            if output.stderr != "":
                result.logs.extend(output.stdout.split("\n"))
                result.errors.extend(output.stderr.split("\n"))
            else:
                result.errors.extend(output.stdout.split("\n"))
        return result


def exec_flake8(
    root: Path,
    files: list[Path],
    exec_cmd: Callable = subprocess.run,
) -> list[ToolResult]:
    runner = Flake8Runner(root, files, exec_cmd)
    with ThreadPoolExecutor() as executor:
        results = runner.execute(executor)

    return results


def _run_flake8_on_set(
    fileset: list[Path],
    config: Path,
    exec_cmd: Callable = subprocess.run,
) -> str:
    """Run flake8 on a set of files with a specific config."""

    cmd = [
        "flake8",
        "--color=always",
    ]
    if config.is_file():
        cmd.extend(["--config", str(config)])

    cmd.extend(str(f) for f in fileset)

    try:
        result = exec_cmd(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout + e.stderr
