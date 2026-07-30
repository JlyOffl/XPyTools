#!/usr/bin/env sh
set -eu

HOST="${1:-127.0.0.1}"
PORT="${2:-8000}"

if [ -x ".venv/bin/python" ]; then
  PYTHON=".venv/bin/python"
else
  PYTHON="python3"
fi

echo "Starting server on ${HOST}:${PORT}"
exec "$PYTHON" -m uvicorn main:app --host "$HOST" --port "$PORT"
