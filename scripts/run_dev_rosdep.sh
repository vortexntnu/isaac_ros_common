#!/usr/bin/env bash
set -euo pipefail

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

COLLECT_SCRIPT="${ROOT}/collect_rosdep_workspace.py"
RUN_DEV_SCRIPT="${ROOT}/run_dev.sh"

if [[ ! -f "${COLLECT_SCRIPT}" ]]; then
    echo "[rosdep] ERROR: collect_rosdep_workspace.py not found"
    exit 1
fi

if [[ ! -f "${RUN_DEV_SCRIPT}" ]]; then
    echo "[rosdep] ERROR: run_dev.sh not found"
    exit 1
fi

echo "=== [rosdep] Generating rosdep build workspace ==="
python3 "${COLLECT_SCRIPT}"

echo "=== [rosdep] Launching Isaac ROS dev container (with rosdep layer) ==="

exec "${RUN_DEV_SCRIPT}" \
    --image_key ros2_humble.deps.rosdep \
    "$@"
