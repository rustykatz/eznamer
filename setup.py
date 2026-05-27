import sys
from pathlib import Path

from cx_Freeze import setup, Executable

PROJECT_ROOT = Path(__file__).resolve().parent

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"],
    "excludes": ["tkinter"],
    "include_files": [
        (str(PROJECT_ROOT / "app" / "breeze_resources.py"), "app/breeze_resources.py"),
        (str(PROJECT_ROOT / "app" / "gui_list.py"), "app/gui_list.py"),
        (str(PROJECT_ROOT / "resources"), "resources"),
    ],
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="EZNamerProgram",
    version="3.0",
    description="Bulk file renaming made easy",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "app/eznamer.py",
            base=base,
            icon=str(PROJECT_ROOT / "resources" / "Icon256x256.ico"),
        )
    ],
)
