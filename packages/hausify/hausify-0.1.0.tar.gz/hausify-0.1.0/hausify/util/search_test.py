from dataclasses import dataclass
from pathlib import Path

from hausify.util.search import find_parent_configs
from hausify.util.testing.build_test_file_structure import build_test_file_structure  # NOQA


@dataclass
class FindParentConfigsTestCase:
    name: str
    source_tree: list[Path]
    config_tree: list[Path]
    args_rootdir: Path
    args_config_names: list[str]
    expected_configs: dict[Path, list[Path]]

    def run(self, tmp_path: Path):
        build_test_file_structure(self.source_tree + self.config_tree, tmp_path)

        actual = find_parent_configs(
            self.args_rootdir,
            self.source_tree,
            self.args_config_names,
        )

        assert actual == self.expected_configs, (
            f"Test {self.name} failed: expected {self.expected_configs}, "
            f"got {actual}"
        )


def test_find_parent_configs_single_config_in_root(tmp_path):
    test_case = FindParentConfigsTestCase(
        name="Single config file in root",
        source_tree=[
            tmp_path / "file1.py",
            tmp_path / "file2.py",
            tmp_path / "filea.py",
            tmp_path / "fileb.py",
        ],
        config_tree=[
            tmp_path / "config.yaml",
        ],
        args_rootdir=tmp_path,
        args_config_names=["config.yaml"],
        expected_configs={
            tmp_path: [],
            (tmp_path / "config.yaml"): [
                tmp_path / "file1.py",
                tmp_path / "file2.py",
                tmp_path / "filea.py",
                tmp_path / "fileb.py",
            ],
        },
    )

    test_case.run(tmp_path)


def test_find_parent_configs_multiple_configs_first_config_wins(tmp_path):
    test_case = FindParentConfigsTestCase(
        name="Multiple config files in root, first_config_wins",
        source_tree=[
            tmp_path / "file1.py",
            tmp_path / "file2.py",
            tmp_path / "filea.py",
            tmp_path / "fileb.py",
        ],
        config_tree=[
            tmp_path / "config.yaml",
            tmp_path / "config.abc",
        ],
        args_rootdir=tmp_path,
        args_config_names=["config.yaml", "config.abc"],
        expected_configs={
            tmp_path: [],
            (tmp_path / "config.yaml"): [
                tmp_path / "file1.py",
                tmp_path / "file2.py",
                tmp_path / "filea.py",
                tmp_path / "fileb.py",
            ],
        },
    )

    test_case.run(tmp_path)


def test_find_parent_configs_no_config_files(tmp_path):
    test_case = FindParentConfigsTestCase(
        name="No config files",
        source_tree=[
            tmp_path / "file1.py",
            tmp_path / "file2.py",
            tmp_path / "filea.py",
            tmp_path / "fileb.py",
        ],
        config_tree=[],
        args_rootdir=tmp_path,
        args_config_names=["config.yaml", "config.abc"],
        expected_configs={
            tmp_path: [
                tmp_path / "file1.py",
                tmp_path / "file2.py",
                tmp_path / "filea.py",
                tmp_path / "fileb.py",
            ],
        },
    )

    test_case.run(tmp_path)


def test_find_parent_configs_not_above_root(tmp_path):
    test_case = FindParentConfigsTestCase(
        name="Config file not above root",
        source_tree=[
            tmp_path / "above_root" / "root" / "file1.py",
            tmp_path / "above_root" / "root" / "file2.py",
        ],
        config_tree=[
            tmp_path / "above_root" / "config.yaml",
        ],
        args_rootdir=tmp_path / "above_root" / "root",
        args_config_names=["config.yaml"],
        expected_configs={
            (tmp_path / "above_root" / "root"): [
                tmp_path / "above_root" / "root" / "file1.py",
                tmp_path / "above_root" / "root" / "file2.py",
            ],
        },
    )

    test_case.run(tmp_path)
