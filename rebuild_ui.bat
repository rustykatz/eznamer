@echo off
REM Converts the Qt Designer .ui file to generated PyQt code.

SET SCRIPT_DIR=%~dp0
SET UI_FILE=%SCRIPT_DIR%app\gui_list.ui
SET PY_FILE=%SCRIPT_DIR%app\gui_list.py

echo Converting %UI_FILE% to %PY_FILE%...

IF EXIST "%SCRIPT_DIR%venv\Scripts\pyuic5.exe" (
    "%SCRIPT_DIR%venv\Scripts\pyuic5.exe" -o "%PY_FILE%" "%UI_FILE%"
) ELSE IF EXIST "%SCRIPT_DIR%.venv\Scripts\pyuic5.exe" (
    "%SCRIPT_DIR%.venv\Scripts\pyuic5.exe" -o "%PY_FILE%" "%UI_FILE%"
) ELSE (
    pyuic5 -o "%PY_FILE%" "%UI_FILE%"
)

IF %ERRORLEVEL% NEQ 0 (
    python -m PyQt5.uic.pyuic -o "%PY_FILE%" "%UI_FILE%"
)

IF %ERRORLEVEL% EQU 0 (
    echo Done.
) ELSE (
    echo Failed to convert UI file.
    echo Make sure PyQt5 is installed with: python -m pip install -r requirements.txt
)

pause
