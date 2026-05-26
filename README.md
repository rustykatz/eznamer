# Ez-Namer

Written by Russell Wong.

## What is Ez-Namer?

Ez-Namer is a user-friendly bulk file renaming app for organizing large batches
of photos and videos. It provides a PyQt GUI for filtering files, selecting a
rename batch, applying a naming pattern, and optionally keeping a mirror folder
in sync.

![Image of App](https://github.com/rustykatz/eznamer/blob/master/Resources/App_V2_0.PNG)

## Quick Start

Install the dependencies, then run the main app:

```powershell
python -m pip install -r requirements.txt
python eznamer.py
```

Then:

1. Click **Change** beside **Directory** to select the folder containing files to rename.
2. Optionally enter a search filter and click **Apply** beside **Search Filter**.
3. Select the files to rename in the list.
4. Enter the base name, season, starting episode index, file extension, and pattern.
5. Click **Re-Name Selected Files**.
6. Use **Undo** if you need to revert the most recent rename batch.

The default rename pattern is:

```text
{name} - S{season:02}E{idx:02}{ext}
```

Example output:

```text
Show Name - S01E01.mkv
Show Name - S01E02.mkv
```

## Mirror Mode

Mirror mode lets you rename matching files in a second folder at the same time.

1. Select the main directory.
2. Select the mirror directory.
3. Enable the mirror checkbox.
4. Ez-Namer checks whether both folders contain the same file names.
5. If the folders match, rename actions apply to both folders.

## Current Files

| File | Purpose |
| --- | --- |
| `eznamer.py` | Current main GUI app. |
| `eznamer2.py` | Transitional older copy. Safe to remove after tests and any references no longer depend on it. |
| `eznamer_legacy.py` | Original command-line version. |
| `gui_list.py` | Generated PyQt UI code. |
| `gui_list.ui` | Qt Designer source file. |
| `test_eznamer3.py` | Tests for the refactored helper behavior. |

## Dependencies

Ez-Namer requires Python 3 and the packages listed in `requirements.txt`:

| Module | Purpose |
| --- | --- |
| `PyQt5` | GUI framework. |
| `send2trash` | Safely sends deleted files to the recycle bin. |

## Development Notes

If the UI is edited in Qt Designer, regenerate `gui_list.py` from `gui_list.ui`
before testing the app.

## Legacy Command-Line Version

The legacy version is available as `eznamer_legacy.py`. It uses terminal-style
commands such as `ls`, `cd`, `add`, `adde`, `stage`, `rf`, `del`, and `clear`.

To run it:

```powershell
python eznamer_legacy.py
```
