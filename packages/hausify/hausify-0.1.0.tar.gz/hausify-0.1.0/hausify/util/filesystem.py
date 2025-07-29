import os
import re
import warnings
from pathlib import Path

_default_exclude_dirs = set(
    [
        r"__pycache__",
        r"\.git",
        r"\.pytest_cache",
        r"\.mypy_cache",
        r"\.venv",
    ]
)


class SourceTree:
    rootdir: Path
    source_files: list[Path]

    def __init__(
        self,
        rootdir: str,
        source_files: list[str],
        exclude_dirs: list[str],
    ):
        """Initialize the SourceTree with a root directory and source files.

        Args:
            rootdir (str): The root directory of the project. If empty, it will try
                to find the git root.
            source_files (list[str]): List of source files relative to the root directory.
            exclude_dirs (list[str]): List of directory patterns to exclude from discovery.
        """
        self.rootdir: Path = _discover_root(rootdir)

        self.source_files: list[Path] = []

        if len(source_files) == 0:
            self.source_files = _discover_source_files(self.rootdir, exclude_dirs)
        else:
            self.source_files = _resolve_source_files(self.rootdir, source_files)


def _get_git_root() -> Path:
    """Get the resolved root directory of the git repository."""
    try:
        return Path(os.popen("git rev-parse --show-toplevel").read().strip()).resolve()
    except Exception as e:
        cwd = Path.cwd()
        warnings.warn(
            f"Could not determine git root directory: {e}. Using current working directory instead."
        )
        return cwd.resolve()


def _discover_root(rootdir: str) -> Path:
    """Discover the root directory of the project.

    If `rootdir` is empty, it will try to find the git root directory.
    """
    if not rootdir:
        return _get_git_root()
    else:
        return Path(rootdir).resolve()


def _discover_source_files(rootdir: Path, exclude_dirs: list[str]) -> list[Path]:
    """Discover source files in the root directory, excluding specified
    directories."""
    exclude_dir_patterns = set(exclude_dirs).union(_default_exclude_dirs)

    dir_tests = [re.compile(exclude_dir) for exclude_dir in exclude_dir_patterns]
    keep_files = []
    for root, dir, files in os.walk(rootdir, topdown=True):
        keep_dirs = []
        for d in dir:
            if not any(match.match(d) for match in dir_tests):
                keep_dirs.append(d)
        dir[:] = keep_dirs
        for file in files:
            if not file.endswith((".py", ".pyi")):
                continue
            file_path = Path(root) / file
            keep_files.append(file_path.resolve())

    return keep_files


def _resolve_source_files(rootdir: Path, source_files: list[str]) -> list[Path]:
    """Resolve source files to absolute paths."""
    resolved_files = []
    for file in source_files:
        as_path = Path(file)

        if not as_path.is_absolute():
            as_path = rootdir / as_path

        if not as_path.exists():
            continue

        resolved_files.append(as_path.resolve())
    return resolved_files
