#!/usr/bin/env python3
import shutil
from pathlib import Path

# scripts/ → isaac_ros_common/scripts
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

print(f"[rosdep] Workspace root: {WORKSPACE_ROOT}")
print(f"[rosdep] Scanning: {SRC_DIR}")
print(f"[rosdep] Output: {BUILD_DIR}")

# Clean old build dir
if BUILD_DIR.exists():
    shutil.rmtree(BUILD_DIR)

OUT_SRC_DIR.mkdir(parents=True)

# Ensure colcon ignores this directory
(BUILD_DIR / "COLCON_IGNORE").touch()

count = 0

for pkg_xml in SRC_DIR.rglob("package.xml"):
    # Never re-copy generated files
    if BUILD_DIR in pkg_xml.parents:
        continue

    pkg_name = pkg_xml.parent.name
    dst = OUT_SRC_DIR / pkg_name
    dst.mkdir(parents=True, exist_ok=True)

    shutil.copy(pkg_xml, dst / "package.xml")
    count += 1

print(f"[rosdep] Collected {count} package.xml files")
