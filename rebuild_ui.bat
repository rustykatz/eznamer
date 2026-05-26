@echo off
REM Converts a .ui file to a .py file using pyuic5

SET UI_FILE=app\gui_list.ui
SET PY_FILE=app\gui_list.py

echo Converting %UI_FILE% to %PY_FILE%...
pyuic5 -o %PY_FILE% %UI_FILE%

IF %ERRORLEVEL% EQU 0 (
    echo Done.
) ELSE (
    echo Failed to convert UI file.
)

pause
