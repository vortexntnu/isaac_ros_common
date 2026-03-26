#!/usr/bin/env bash
set -euo pipefail

GREEN="\033[0;32m"
RED="\033[0;31m"
RESET="\033[0m"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

COLLECT_SCRIPT="${ROOT}/collect_rosdep_workspace.py"
RUN_DEV_SCRIPT="${ROOT}/run_dev.sh"

if [[ ! -f "${COLLECT_SCRIPT}" ]]; then
    echo -e "${RED}ERROR: collect_rosdep_workspace.py not found${RESET}"
    exit 1
fi

if [[ ! -f "${RUN_DEV_SCRIPT}" ]]; then
    echo -e "${RED}ERROR: run_dev.sh not found${RESET}"
    exit 1
fi

# Parse -n/--name before forwarding remaining args to run_dev.sh
CONTAINER_NAME_ARG=()
PASSTHROUGH_ARGS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        -n | --name)
            CONTAINER_NAME_ARG=(--container_name "$2")
            shift 2
            ;;
        *)
            PASSTHROUGH_ARGS+=("$1")
            shift
            ;;
    esac
done

echo -e "${GREEN}Generating rosdep build workspace${RESET}"
python3 "${COLLECT_SCRIPT}"

exec "${RUN_DEV_SCRIPT}" \
    --image_key ros2_humble.deps.realsense \
    "${CONTAINER_NAME_ARG[@]}" \
    "${PASSTHROUGH_ARGS[@]}"
