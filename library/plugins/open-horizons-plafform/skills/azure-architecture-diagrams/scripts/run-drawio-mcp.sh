#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
PYTHON_BIN="${VENV_DIR}/bin/python"
REQUIREMENTS="${SCRIPT_DIR}/requirements.txt"
SERVER="${SCRIPT_DIR}/drawio_mcp_server.py"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

if ! "${PYTHON_BIN}" -c "import mcp" >/dev/null 2>&1; then
  "${PYTHON_BIN}" -m pip install --quiet --upgrade pip
  "${PYTHON_BIN}" -m pip install --quiet -r "${REQUIREMENTS}"
fi

exec "${PYTHON_BIN}" "${SERVER}"
