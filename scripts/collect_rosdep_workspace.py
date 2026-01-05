#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

GREEN = "\033[0;32m"
RED = "\033[0;31m"
RESET = "\033[0m"

# This script collects only package.xml files from the workspace.
# They are used to run rosdep in a Docker build layer so dependency
# installation can be cached. If we copied full packages, any source
# change would invalidate the cache and force rosdep to rerun.

SCRIPTS_DIR = Path(__file__).resolve().parent
ISAAC_ROS_COMMON_DIR = SCRIPTS_DIR.parent
DOCKER_DIR = ISAAC_ROS_COMMON_DIR / "docker"

BUILD_DIR = DOCKER_DIR / "build"
OUT_SRC_DIR = BUILD_DIR / "src"


def find_workspace_root(start: Path) -> Path:
    for p in [start] + list(start.parents):
        if (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate workspace root containing src/")


WORKSPACE_ROOT = find_workspace_root(SCRIPTS_DIR)
SRC_DIR = WORKSPACE_ROOT / "src"

print(f"{GREEN}Workspace root: {WORKSPACE_ROOT}{RESET}")
print(f"{GREEN}Scanning: {SRC_DIR}{RESET}")
print(f"{GREEN}Output: {BUILD_DIR}{RESET}")

if BUILD_DIR.exists():
    shutil.rmtree(BUILD_DIR)

OUT_SRC_DIR.mkdir(parents=True)
(BUILD_DIR / "COLCON_IGNORE").touch()

seen_packages = {}
count = 0

for pkg_xml in SRC_DIR.rglob("package.xml"):
    if BUILD_DIR in pkg_xml.parents:
        continue

    pkg_name = pkg_xml.parent.name

    if pkg_name in seen_packages:
        print(
            f"{RED}ERROR: Duplicate package name '{pkg_name}' found:{RESET}\n"
            f"  - {seen_packages[pkg_name]}\n"
            f"  - {pkg_xml}"
        )
        sys.exit(1)

    seen_packages[pkg_name] = pkg_xml

    dst = OUT_SRC_DIR / pkg_name
    dst.mkdir(parents=True)

    shutil.copy(pkg_xml, dst / "package.xml")
    count += 1

print(f"{GREEN}Collected {count} package.xml files{RESET}")
