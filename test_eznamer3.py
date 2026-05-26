"""Tests for Ez-Namer helper behavior.

These tests focus on helpers that do not require interacting with a running
Qt window.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List

import pytest

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


def test_compare_directories_equal(tmp_path: Path):
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    dir1.mkdir()
    dir2.mkdir()
    for name in ("x.mkv", "y.mkv"):
        (dir1 / name).write_text("1")
        (dir2 / name).write_text("1")
    assert ez.MyMainWindow._compare_directories(dir1, dir2)


def test_compare_directories_unequal(tmp_path: Path):
    dir1 = tmp_path / "d1"
    dir2 = tmp_path / "d2"
    dir1.mkdir()
    dir2.mkdir()
    (dir1 / "only_in_1.mkv").write_text("1")
    assert not ez.MyMainWindow._compare_directories(dir1, dir2)


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


def test_delete_files_calls_send2trash(monkeypatch, tmp_dir_with_files: Path):
    called: List[str] = []

    def fake_send(path: str):
        called.append(Path(path).name)

    monkeypatch.setattr(ez, "send2trash", type("S", (), {"send2trash": staticmethod(fake_send)}))

    target = tmp_dir_with_files / "extra.txt"
    ez.MyMainWindow._delete_files([target])
    assert called == ["extra.txt"]
