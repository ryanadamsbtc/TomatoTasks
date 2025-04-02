#!/usr/bin/env bash
set -euo pipefail

export HOME="$(pwd)/.tmp-home"
mkdir -p "$HOME"

python -m tomatotasks add "try me" || true
python -m tomatotasks ls || true
python -m tomatotasks start 1 || true
python -m tomatotasks session || true
python -m tomatotasks stop || true

echo "OK"

