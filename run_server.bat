@echo off
setlocal

set HOST=%1
if "%HOST%"=="" set HOST=127.0.0.1

set PORT=%2
if "%PORT%"=="" set PORT=8000

if exist ".venv\Scripts\python.exe" (
  set PYTHON=.venv\Scripts\python.exe
) else (
  set PYTHON=py
)

echo Starting server on %HOST%:%PORT%
%PYTHON% -m uvicorn main:app --host %HOST% --port %PORT%

endlocal
