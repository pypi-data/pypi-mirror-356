from pathlib import Path


def build_test_file_structure(test_paths: list[Path], tmp_path: Path) -> Path:
    """Build a test file structure based on the provided paths.

    Note: tmp_path is the pytest fixture that provides a temporary directory.
    """
    for source_file in test_paths:
        curr_dir = tmp_path / source_file.parent
        curr_dir.mkdir(parents=True, exist_ok=True)
        if source_file.name != "":
            with open(curr_dir / source_file.name, "w") as f:
                f.write(f"This is a test file in {source_file.name}.")

    return tmp_path
