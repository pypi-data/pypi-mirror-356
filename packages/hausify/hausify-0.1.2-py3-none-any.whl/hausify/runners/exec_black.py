import subprocess
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from pathlib import Path
from typing import Callable
from typing import Union

from hausify.runners.runner import PythonTool
from hausify.runners.runner import ToolCommand
from hausify.runners.runner import ToolResult
from hausify.util.python_import_finder import PythonImportFinder


class BlackFormatMode(str, Enum):
    FIX = "fix"
    CHECK = "check"


class BlackRunner(PythonTool):
    """Runner for the Black code formatter.

    This runner finds Black configuration files in the source tree and
    executes Black on the provided files, either fixing them or checking
    their format (mode).
    """

    _configs = ["pyproject.toml"]

    def __init__(
        self,
        root: Path,
        files: list[Path],
        exec_cmd: Callable,
        mode: BlackFormatMode = BlackFormatMode.CHECK,
    ):
        self._mode = mode
        super().__init__(root, files, exec_cmd)

    def build_commands(self, config: Path, files: list[Path]) -> list[ToolCommand]:
        """Build a Black command for each file in the provided list.

        This method detects where imports are in the file and IGNORES
        these lines when formatting. This allows isort to run first and
        not conflict with Black.
        """

        all_commands = []
        for filename in files:
            if filename.suffix not in (".py", ".pyi"):
                continue

            cmd = ToolCommand(
                config=str(config),
                files=[str(filename)],
                argv=["black", "--color"],
            )

            if self._mode == BlackFormatMode.CHECK:
                cmd.argv.append("--check")
                cmd.argv.append("--diff")

            if config.is_file():
                cmd.argv.extend(["--config", str(config)])

            finder = PythonImportFinder()
            finder.load_source_file(Path(filename))
            for start, end in finder.get_formatting_ranges():
                cmd.argv.extend(["--line-ranges", f"{start}-{end}"])
            cmd.argv.append(str(filename))
            all_commands.append(cmd)

        return all_commands

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


def exec_black(
    root: Path,
    files: list[Path],
    exec_cmd: Callable = subprocess.run,
    mode: BlackFormatMode = BlackFormatMode.CHECK,
) -> list[ToolResult]:
    runner = BlackRunner(root, files, exec_cmd, mode)
    with ThreadPoolExecutor() as exec:
        results = runner.execute(exec)

    return results
