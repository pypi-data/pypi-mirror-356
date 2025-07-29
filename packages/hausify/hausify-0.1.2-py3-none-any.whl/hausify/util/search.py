from pathlib import Path


def find_parent_configs(
    rootdir: Path,
    source_files: list[Path],
    config_names: list[str],
) -> dict[Path, list[Path]]:
    """Find parent configuration files in the source tree, and their source
    file groups.

    Args:
        rootdir (Path): The root directory of the project.
        source_files (list[Path]): List of source files to search for configuration files.
        config_names (list[str]): List of configuration file names to search for.
    Returns:
        dict[Path, list[Path]]: A dictionary mapping configuration file paths to their source files.
    """

    found_configs: dict[Path, list[Path]] = {rootdir: []}
    for source_file in source_files:
        found_path = rootdir
        for config in config_names:
            config_path = _find_closest_parent(source_file, config, rootdir)
            if config_path != rootdir:
                found_path = config_path
                break

        if found_path not in found_configs:
            found_configs[found_path] = []
        found_configs[found_path].append(source_file)

    return found_configs


def _find_closest_parent(
    file: Path,
    config: str,
    root: Path,
) -> Path:
    """Find the closest parent directory containing the specified configuration
    file.

    Args:
        file (Path): The file to start searching from.
        config (str): The name of the configuration file to search for.
    Returns:
        Path: The path to the closest parent directory containing the
          configuration file, or the root directory if not found.
    """
    current_dir = file.parent
    if not current_dir.exists():
        return root

    depth = 0
    while depth < 50:
        potential_config = current_dir / config
        if potential_config.exists() and potential_config.is_file():
            return potential_config

        if current_dir == root:
            return root

        current_dir = current_dir.parent
        depth += 1

    return root
