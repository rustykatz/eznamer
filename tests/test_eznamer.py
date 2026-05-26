"""Tests for Ez-Namer helper behavior.

These tests focus on helpers that do not require interacting with a running
Qt window.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Callable, List

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

import eznamer as ez


logging.getLogger(ez.__name__).setLevel(logging.CRITICAL)


@pytest.fixture()
def tmp_dir_with_files(tmp_path: Path) -> Path:
    """Create a temporary directory with three sample files."""
    for name in ("a.mkv", "b.mkv", "extra.txt"):
        (tmp_path / name).write_text("dummy")
    return tmp_path


@pytest.mark.parametrize(
    "substr,expected",
    [
        (".mkv", {"a.mkv", "b.mkv"}),
        ("a", {"a.mkv", "extra.txt"}),
        ("nonexistent", set()),
    ],
)
def test_select_by_substr(tmp_dir_with_files: Path, substr: str, expected: set[str]):
    assert set(ez.MyMainWindow._select_by_substr(tmp_dir_with_files, substr)) == expected


def test_select_by_substr_uses_natural_case_insensitive_order(tmp_path: Path):
    for name in ("Episode 10.mkv", "episode 2.mkv", "Episode 1.mkv"):
        (tmp_path / name).write_text("dummy")

    assert ez.MyMainWindow._select_by_substr(tmp_path, ".mkv") == [
        "Episode 1.mkv",
        "episode 2.mkv",
        "Episode 10.mkv",
    ]


@pytest.mark.parametrize(
    "dir1_files,dir2_files,expected",
    [
        ({"x.mkv", "y.mkv"}, {"x.mkv", "y.mkv"}, True),
        ({"only_in_1.mkv"}, set(), False),
    ],
)
def test_compare_directories_by_file_names(
    tmp_path: Path,
    dir1_files: set[str],
    dir2_files: set[str],
    expected: bool,
):
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    dir1.mkdir()
    dir2.mkdir()
    for name in dir1_files:
        (dir1 / name).write_text("1")
    for name in dir2_files:
        (dir2 / name).write_text("1")

    assert ez.MyMainWindow._compare_directories(dir1, dir2) is expected


def test_rename_files_success(tmp_dir_with_files: Path):
    stage = ["a.mkv", "b.mkv"]
    history = ez.MyMainWindow._rename_files(
        dir_path=tmp_dir_with_files,
        stage=stage,
        base="Show",
        ext=".mkv",
        index="1",
        season="1",
        pattern="{name} - S{season:02}E{idx:02}{ext}",
    )
    expected_names = {"Show - S01E01.mkv", "Show - S01E02.mkv", "extra.txt"}
    assert {f.name for f in tmp_dir_with_files.iterdir()} == expected_names
    assert history[0][0].name == "Show - S01E01.mkv"
    assert history[0][1].name == "a.mkv"


def test_rename_files_accepts_custom_pattern_and_starting_numbers(tmp_dir_with_files: Path):
    history = ez.MyMainWindow._rename_files(
        dir_path=tmp_dir_with_files,
        stage=["a.mkv", "b.mkv"],
        base="Planet Earth",
        ext=".mp4",
        index="9",
        season="2",
        pattern="{name}.s{season:02}.e{idx:03}{ext}",
    )

    expected_names = {"Planet Earth.s02.e009.mp4", "Planet Earth.s02.e010.mp4", "extra.txt"}
    assert {f.name for f in tmp_dir_with_files.iterdir()} == expected_names
    assert [(new.name, old.name) for new, old in history] == [
        ("Planet Earth.s02.e009.mp4", "a.mkv"),
        ("Planet Earth.s02.e010.mp4", "b.mkv"),
    ]


def test_rename_files_invalid_numbers_do_not_touch_files(tmp_dir_with_files: Path):
    history = ez.MyMainWindow._rename_files(
        dir_path=tmp_dir_with_files,
        stage=["a.mkv"],
        base="Show",
        ext=".mkv",
        index="not-a-number",
        season="1",
        pattern="{name} - S{season:02}E{idx:02}{ext}",
    )

    assert not history
    assert (tmp_dir_with_files / "a.mkv").exists()


def test_rename_files_skips_missing_source_and_continues_without_incrementing(tmp_dir_with_files: Path):
    history = ez.MyMainWindow._rename_files(
        dir_path=tmp_dir_with_files,
        stage=["missing.mkv", "a.mkv"],
        base="Show",
        ext=".mkv",
        index="7",
        season="1",
        pattern="{name} - S{season:02}E{idx:02}{ext}",
    )

    assert [(new.name, old.name) for new, old in history] == [("Show - S01E07.mkv", "a.mkv")]
    assert (tmp_dir_with_files / "Show - S01E07.mkv").exists()
    assert (tmp_dir_with_files / "b.mkv").exists()


def test_rename_files_skip_existing(tmp_dir_with_files: Path):
    (tmp_dir_with_files / "Show - S01E01.mkv").write_text("dummy")
    stage = ["a.mkv"]
    history = ez.MyMainWindow._rename_files(
        dir_path=tmp_dir_with_files,
        stage=stage,
        base="Show",
        ext=".mkv",
        index="1",
        season="1",
        pattern="{name} - S{season:02}E{idx:02}{ext}",
    )
    assert not history
    assert (tmp_dir_with_files / "a.mkv").exists()


def test_rename_files_skips_when_source_already_has_target_name(tmp_dir_with_files: Path):
    history = ez.MyMainWindow._rename_files(
        dir_path=tmp_dir_with_files,
        stage=["a.mkv"],
        base="a",
        ext=".mkv",
        index="1",
        season="1",
        pattern="{name}{ext}",
    )

    assert history == []
    assert (tmp_dir_with_files / "a.mkv").exists()


def test_rename_files_bad_pattern_does_not_touch_files(tmp_dir_with_files: Path):
    history = ez.MyMainWindow._rename_files(
        dir_path=tmp_dir_with_files,
        stage=["a.mkv"],
        base="Show",
        ext=".mkv",
        index="1",
        season="1",
        pattern="{missing_key}{ext}",
    )

    assert history == []
    assert (tmp_dir_with_files / "a.mkv").exists()


def test_delete_files_continues_after_send2trash_error(monkeypatch, tmp_dir_with_files: Path):
    called: List[str] = []

    def fake_send(path: str):
        called.append(Path(path).name)
        if Path(path).name == "a.mkv":
            raise OSError("trash unavailable")

    monkeypatch.setattr(ez, "send2trash", type("S", (), {"send2trash": staticmethod(fake_send)}))

    ez.MyMainWindow._delete_files([tmp_dir_with_files / "a.mkv", tmp_dir_with_files / "b.mkv"])
    assert called == ["a.mkv", "b.mkv"]


def test_apply_rename_batch_renames_main_and_mirror_and_records_one_batch(tmp_path: Path):
    main_dir = tmp_path / "main"
    mirror_dir = tmp_path / "mirror"
    main_dir.mkdir()
    mirror_dir.mkdir()
    for directory in (main_dir, mirror_dir):
        (directory / "a.mkv").write_text("a")
        (directory / "b.mkv").write_text("b")

    history: List[List[tuple[Path, Path]]] = []
    batch = ez.MyMainWindow._apply_rename_batch(
        rename_history=history,
        cur_path=main_dir,
        mirror_path=mirror_dir,
        mirror_enabled=True,
        stage=["a.mkv", "b.mkv"],
        base="Show",
        ext=".mkv",
        index="3",
        season="4",
        pattern="{name} - S{season:02}E{idx:02}{ext}",
    )

    expected_names = {"Show - S04E03.mkv", "Show - S04E04.mkv"}
    assert {p.name for p in main_dir.iterdir()} == expected_names
    assert {p.name for p in mirror_dir.iterdir()} == expected_names
    assert history == [batch]
    assert [(new.parent.name, new.name, old.name) for new, old in batch] == [
        ("main", "Show - S04E03.mkv", "a.mkv"),
        ("main", "Show - S04E04.mkv", "b.mkv"),
        ("mirror", "Show - S04E03.mkv", "a.mkv"),
        ("mirror", "Show - S04E04.mkv", "b.mkv"),
    ]


def test_on_delete_files_delegates_checked_paths_and_refreshes(tmp_path: Path):
    deleted: List[Path] = []
    refresh_calls: List[str] = []
    window = _DeleteOnlyWindow(
        cur_path=tmp_path,
        checked_files=["a.mkv", "b.mkv"],
        deleted=deleted,
        record=refresh_calls.append,
    )

    ez.MyMainWindow._on_delete_files(window)

    assert deleted == [tmp_path / "a.mkv", tmp_path / "b.mkv"]
    assert refresh_calls == ["files", "mirror"]


def test_on_undo_restores_last_rename_batch(tmp_path: Path):
    original_a = tmp_path / "a.mkv"
    original_b = tmp_path / "b.mkv"
    renamed_a = tmp_path / "Show - S01E01.mkv"
    renamed_b = tmp_path / "Show - S01E02.mkv"
    renamed_a.write_text("a")
    renamed_b.write_text("b")

    refresh_calls: List[str] = []
    window = _UndoOnlyWindow(refresh_calls.append)
    window._rename_history = [[(renamed_a, original_a), (renamed_b, original_b)]]

    ez.MyMainWindow._on_undo(window)

    assert sorted(p.name for p in tmp_path.iterdir()) == ["a.mkv", "b.mkv"]
    assert window._rename_history == []
    assert refresh_calls == ["files", "mirror"]


def test_on_undo_skips_when_original_name_exists(tmp_path: Path):
    original = tmp_path / "a.mkv"
    renamed = tmp_path / "Show - S01E01.mkv"
    original.write_text("original")
    renamed.write_text("renamed")

    refresh_calls: List[str] = []
    window = _UndoOnlyWindow(refresh_calls.append)
    window._rename_history = [[(renamed, original)]]

    ez.MyMainWindow._on_undo(window)

    assert original.read_text() == "original"
    assert renamed.read_text() == "renamed"
    assert window._rename_history == []
    assert refresh_calls == ["files", "mirror"]


class _UndoOnlyWindow:
    def __init__(self, record: Callable[[str], None]) -> None:
        self._rename_history = []
        self._record = record

    def _refresh_file_list(self) -> None:
        self._record("files")

    def _refresh_mirror_status_if_checked(self) -> None:
        self._record("mirror")


class _DeleteOnlyWindow:
    def __init__(
        self,
        cur_path: Path,
        checked_files: List[str],
        deleted: List[Path],
        record: Callable[[str], None],
    ) -> None:
        self.cur_path = cur_path
        self._checked = checked_files
        self._deleted = deleted
        self._record = record

    def _checked_files(self) -> List[str]:
        return self._checked

    def _delete_files(self, paths: List[Path]) -> None:
        self._deleted.extend(paths)

    def _refresh_file_list(self) -> None:
        self._record("files")

    def _refresh_mirror_status_if_checked(self) -> None:
        self._record("mirror")
