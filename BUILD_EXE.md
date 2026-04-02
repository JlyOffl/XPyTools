Building a single-file executable (Windows) using PyInstaller

Prerequisites
- Activate your project's Python environment (recommended) and ensure dependencies from `requirements.txt` are installed.
- Install PyInstaller: `pip install pyinstaller`

Create single-file executable

From the project root (`c:\temp\XPyTools`) run:

```powershell
pyinstaller --onefile \
  --add-data "Settings;Settings" \
  --add-data "ssl;ssl" \
  --add-data "discord_sent_ids.json;." \
  --hidden-import=starlette.testclient \
  run_spaces_poller.py
```

Notes
- The `--add-data` separator on Windows is `;` (as shown). Adjust paths if your files live elsewhere.
- The built exe will be in `dist\run_spaces_poller.exe`.
- This bundles the poller that calls the FastAPI app in-process (no external uvicorn process needed).
- If your app depends on external resources (DB credentials, certs, etc.) ensure the files in `Settings` and `ssl` are present and reachable.

Running the exe

Double-click `dist\run_spaces_poller.exe` or run from PowerShell:

```powershell
.\dist\run_spaces_poller.exe --interval 300
```
