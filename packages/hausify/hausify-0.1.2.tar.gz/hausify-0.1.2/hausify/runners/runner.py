import os
import subprocess
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Callable
from typing import Union

from hausify.util.search import find_parent_configs


@dataclass
class ToolCommand:
    """Represents a CLI command to be executed for a specific python tool."""

    # The configuration file used for this command
    config: str = ""

    # The list of files to be processed by this command
    files: list[str] = field(default_factory=list)

    # The command line arguments to be executed
    argv: list[str] = field(default_factory=list)

    # Environment variables to be set/overriden for this command
    env: dict[str, str] = field(default_factory=dict)


@dataclass
class ToolResult:
    """Represents the result of executing a command for a specific python tool.

    Runners should abstract away the individual tool's execution details
    and provide a consistent interface for results.
    """

    # The configuration file used for this command
    config: str = ""

    # The list of files processed by this command
    files: list[str] = field(default_factory=list)

    # The logs produced by this command
    logs: list[str] = field(default_factory=list)

    # Whether the command was successful
    success: bool = True

    # Any errors produced by this command
    errors: list[str] = field(default_factory=list)


class PythonTool:
    """Base class for Python tools that can be executed on a set of files.

    This class provides a framework for executing commands in parallel and handling
    the results in a consistent manner.
    Subclasses should implement the `build_commands` and `handle_result` methods
    to define how commands are built and how results are processed.
    """

    # The tool's prioritized list of configuration file names to search for
    _configs: list[str] = []

    def __init__(
        self,
        root: Path,
        files: list[Path],
        exec_cmd: Callable[..., subprocess.CompletedProcess] = subprocess.run,
    ):
        self._root = root
        self._files = files
        self._iterations = find_parent_configs(root, files, self._configs)
        self._exec_cmd = exec_cmd

    def build_commands(self, config: Path, files: list[Path]) -> list[ToolCommand]:
        """Builds a list of ToolCommand instances for a given configuration and
        set of files.

        This method should be implemented by subclasses to define how
        commands are built for the specific tool.
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def handle_result(
        self,
        cmd: ToolCommand,
        output: Union[subprocess.CompletedProcess, subprocess.CalledProcessError],
    ) -> ToolResult:
        """Handles the result of executing a command.

        This method should be implemented by subclasses to define how
        results are processed for the specific tool.
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def execute(self, exec: ThreadPoolExecutor) -> list[ToolResult]:
        """Builds and executes commands in parallel using a ThreadPoolExecutor.

        This method collects all commands to be executed, submits them
        to the executor, and processes the results once all commands
        have completed. It returns a list of ToolResult instances, each
        representing the result of a command execution.
        """
        all_futures: list[tuple[ToolCommand, Future]] = []
        for config, fileset in self._iterations.items():
            if len(fileset) == 0:
                continue
            commands = self.build_commands(config, fileset)
            for cmd in commands:
                future = exec.submit(self._run_thread, cmd.argv, cmd.env)
                all_futures.append((cmd, future))

        results = []
        for cmd, future in all_futures:
            try:
                output = future.result()
                results.append(self.handle_result(cmd, output))
            except subprocess.CalledProcessError as e:
                results.append(self.handle_result(cmd, e))

        return results

    def _run_thread(
        self, argv: list[str], env: dict[str, str]
    ) -> subprocess.CompletedProcess:
        """Runs a command in a separate thread with the given arguments and
        environment.

        This method is used to execute commands in parallel using a
        ThreadPoolExecutor.
        """
        _env = os.environ.copy()
        _env.update(env)
        return self._exec_cmd(
            argv, capture_output=True, text=True, check=True, env=_env
        )
