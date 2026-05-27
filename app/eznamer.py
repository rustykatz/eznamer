from __future__ import annotations

import logging
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import send2trash
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent / "app"
else:
    APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import breeze_resources  # noqa: F401  # ensures :/dark.qss resource is available
from gui_list import Ui_MainWindow


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    HOME = Path.home()
    RESOURCE_DIR = APP_DIR.parent / "resources"
    WINDOW_ICON = RESOURCE_DIR / "Icon32x32.png"
    DEFAULT_DIRECTORY = HOME / "Videos"
    DEFAULT_MIRROR_DIR = HOME / "Videos"
    DEFAULT_INDEX = 1
    DEFAULT_SEASON = 1
    DEFAULT_EXTENSION = ".mkv"
    DEFAULT_PATTERN = "{name} - S{season:02}E{idx:02}{ext}"


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(str(Config.WINDOW_ICON)))

        self.cur_path: Path = Config.DEFAULT_DIRECTORY
        self.mirror_path: Path = Config.DEFAULT_MIRROR_DIR
        self.mirror_enabled: bool = False
        self._rename_history: List[List[Tuple[Path, Path]]] = []

        self._connect_signals()
        self._populate_defaults()
        self._refresh_file_list()

    def _connect_signals(self) -> None:
        u = self.ui
        u.btn_dir_change.clicked.connect(self._on_change_dir)
        u.btn_dir_apply.clicked.connect(self._on_apply_dir)
        u.btn_dir_use_dir_name.clicked.connect(self._on_use_dir_name)
        u.btn_dir_change_mirror.clicked.connect(lambda: self._on_change_dir(mirror=True))
        u.btn_dir_apply_mirror.clicked.connect(lambda: self._on_apply_dir(mirror=True))
        u.btn_filter_apply.clicked.connect(self._refresh_file_list)
        u.btn_files_select_all.clicked.connect(lambda: self._set_all_check_states(Qt.Checked))
        u.btn_files_deselect.clicked.connect(lambda: self._set_all_check_states(Qt.Unchecked))
        u.btn_files_refresh.clicked.connect(self._refresh_file_list)
        u.btn_files_apply.clicked.connect(self._on_apply_files)
        u.btn_files_delete.clicked.connect(self._on_delete_files)
        u.btn_files_undo.clicked.connect(self._on_undo)
        if hasattr(u, "btn_files_move"):
            u.btn_files_move.clicked.connect(self._on_move_files)
        u.checkbox_mirror.stateChanged.connect(self._on_toggle_mirror)

    def _populate_defaults(self) -> None:
        u = self.ui
        u.line_directory.setText(str(Config.DEFAULT_DIRECTORY))
        u.line_directory_mirror.setText(str(Config.DEFAULT_MIRROR_DIR))
        u.line_index.setText(str(Config.DEFAULT_INDEX))
        u.line_season.setText(str(Config.DEFAULT_SEASON))
        u.line_extension.setText(Config.DEFAULT_EXTENSION)
        u.line_pattern.setText(Config.DEFAULT_PATTERN)

    def _on_toggle_mirror(self, state: int) -> None:
        if state == Qt.Checked:
            self.mirror_enabled = self._compare_directories(self.cur_path, self.mirror_path)
            self.ui.lbl_mirror_check.setText("Same files" if self.mirror_enabled else "Mismatch")
        else:
            self.mirror_enabled = False
            self.ui.lbl_mirror_check.clear()

    def _refresh_mirror_status_if_checked(self) -> None:
        if self.ui.checkbox_mirror.isChecked():
            self._on_toggle_mirror(Qt.Checked)

    def _on_change_dir(self, *, mirror: bool = False) -> None:
        title = "Select Mirror Folder" if mirror else "Select Folder"
        start_dir = str(self.mirror_path if mirror else self.cur_path)
        new_dir = QFileDialog.getExistingDirectory(self, title, start_dir, QFileDialog.ShowDirsOnly)
        if not new_dir:
            return
        if mirror:
            self.ui.line_directory_mirror.setText(new_dir)
        else:
            self.ui.line_directory.setText(new_dir)
        self._on_apply_dir(mirror=mirror)

    def _on_apply_dir(self, *, mirror: bool = False) -> None:
        txt = self.ui.line_directory_mirror.text() if mirror else self.ui.line_directory.text()
        path = Path(txt).expanduser()
        if not path.is_dir():
            LOGGER.error("Invalid directory: %s", path)
            return
        if mirror:
            self.mirror_path = path
            self._refresh_mirror_status_if_checked()
        else:
            self.cur_path = path
            self._refresh_file_list()
            self._refresh_mirror_status_if_checked()

    def _on_use_dir_name(self) -> None:
        self.ui.line_name.setText(self.cur_path.stem)

    def _refresh_file_list(self) -> None:
        files = self._select_by_substr(self.cur_path, self.ui.line_filter.text())
        lw = self.ui.listWidget
        lw.blockSignals(True)
        lw.clear()
        for i, fname in enumerate(files, 1):
            item = QListWidgetItem(f"{i}. {fname}")
            item.setCheckState(Qt.Unchecked)
            lw.addItem(item)
        lw.blockSignals(False)

    def _set_all_check_states(self, state: Qt.CheckState) -> None:
        for i in range(self.ui.listWidget.count()):
            self.ui.listWidget.item(i).setCheckState(state)

    def _checked_files(self) -> List[str]:
        full = self._select_by_substr(self.cur_path, self.ui.line_filter.text())
        return [
            full[i]
            for i in range(self.ui.listWidget.count())
            if self.ui.listWidget.item(i).checkState() == Qt.Checked
        ]

    def _on_apply_files(self) -> None:
        stage = self._checked_files()
        if not stage:
            return

        base = self.ui.line_name.text().strip()
        ext = self.ui.line_extension.text().strip()
        idx = self.ui.line_index.text().strip()
        season = self.ui.line_season.text().strip()
        pattern = self.ui.line_pattern.text().strip()
        if not (base and ext and idx and season and pattern):
            LOGGER.error("Name, extension, index, season, and pattern are required.")
            return

        self._apply_rename_batch(
            rename_history=self._rename_history,
            cur_path=self.cur_path,
            mirror_path=self.mirror_path,
            mirror_enabled=self.mirror_enabled,
            stage=stage,
            base=base,
            ext=ext,
            index=idx,
            season=season,
            pattern=pattern,
        )
        self._refresh_file_list()
        self._refresh_mirror_status_if_checked()

    def _on_move_files(self) -> None:
        dest_dir = QFileDialog.getExistingDirectory(self, "Move files to", str(Config.HOME), QFileDialog.ShowDirsOnly)
        if not dest_dir:
            return
        dest = Path(dest_dir)
        for fname in self._checked_files():
            try:
                shutil.move(str(self.cur_path / fname), str(dest / fname))
            except Exception as exc:
                LOGGER.error("Move failed for %s: %s", fname, exc)
        self._refresh_file_list()
        self._refresh_mirror_status_if_checked()

    def _on_delete_files(self) -> None:
        self._delete_files([self.cur_path / f for f in self._checked_files()])
        self._refresh_file_list()
        self._refresh_mirror_status_if_checked()

    def _on_undo(self) -> None:
        if not self._rename_history:
            LOGGER.info("Nothing to undo.")
            return

        undone: List[str] = []
        for newp, oldp in reversed(self._rename_history.pop()):
            try:
                if not newp.exists():
                    LOGGER.warning("Undo skipped for %s: file no longer exists", newp)
                    continue
                if oldp.exists():
                    LOGGER.error("Undo skipped for %s: %s already exists", newp, oldp)
                    continue
                newp.rename(oldp)
                undone.append(f"{newp.name} -> {oldp.name}")
            except Exception as exc:
                LOGGER.error("Undo failed for %s: %s", newp, exc)

        if undone:
            LOGGER.info("Undo completed:\n%s", "\n".join(undone))
        self._refresh_file_list()
        self._refresh_mirror_status_if_checked()

    @staticmethod
    def _natural_key(name: str) -> List[object]:
        return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]

    @classmethod
    def _select_by_substr(cls, path: Path, substr: str) -> List[str]:
        if not path.is_dir():
            LOGGER.error("Invalid directory: %s", path)
            return []
        return sorted(
            (f.name for f in path.iterdir() if f.is_file() and substr in f.name),
            key=cls._natural_key,
        )

    @staticmethod
    def _delete_files(paths: List[Path]) -> None:
        for p in paths:
            try:
                send2trash.send2trash(str(p))
            except Exception as exc:
                LOGGER.error("Delete error for %s: %s", p, exc)

    @classmethod
    def _apply_rename_batch(
        cls,
        *,
        rename_history: List[List[Tuple[Path, Path]]],
        cur_path: Path,
        mirror_path: Path,
        mirror_enabled: bool,
        stage: List[str],
        base: str,
        ext: str,
        index: str,
        season: str,
        pattern: str,
    ) -> List[Tuple[Path, Path]]:
        batch: List[Tuple[Path, Path]] = []
        batch += cls._rename_files(cur_path, stage, base, ext, index, season, pattern)
        if mirror_enabled:
            batch += cls._rename_files(mirror_path, stage, base, ext, index, season, pattern)
        if batch:
            rename_history.append(batch)
        return batch

    @staticmethod
    def _compare_directories(d1: Path, d2: Path) -> bool:
        try:
            return {f.name for f in d1.iterdir() if f.is_file()} == {f.name for f in d2.iterdir() if f.is_file()}
        except Exception as exc:
            LOGGER.error("Directory comparison failed: %s", exc)
            return False

    @staticmethod
    def _rename_files(
        dir_path: Path,
        stage: List[str],
        base: str,
        ext: str,
        index: str,
        season: str,
        pattern: str,
    ) -> List[Tuple[Path, Path]]:
        try:
            idx = int(index)
            season_number = int(season)
        except ValueError as exc:
            LOGGER.error("Index and season must be numbers: %s", exc)
            return []

        if not dir_path.is_dir():
            LOGGER.error("Invalid rename directory: %s", dir_path)
            return []

        renamed: List[Tuple[Path, Path]] = []
        for original in stage:
            src = dir_path / original
            try:
                dst = dir_path / pattern.format(name=base, ext=ext, idx=idx, season=season_number)
                if not src.exists():
                    LOGGER.warning("SKIPPED: %s does not exist", src.name)
                    continue
                if dst.exists():
                    LOGGER.warning("SKIPPED: %s already exists", dst.name)
                    continue
                if src == dst:
                    LOGGER.warning("SKIPPED: %s already has the target name", src.name)
                    continue
                src.rename(dst)
                renamed.append((dst, src))
                LOGGER.info("Renamed: %s -> %s", src.name, dst.name)
                idx += 1
            except Exception as exc:
                LOGGER.error("Rename failed for %s: %s", original, exc)
        return renamed


class Controller:
    def show_main(self) -> None:
        self.window_main = MyMainWindow()
        self.window_main.show()


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    file = QFile(":/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
