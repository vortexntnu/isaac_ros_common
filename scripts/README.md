# Isaac ROS Dev Build Scripts

For Jetson or x86_64:
  `run_dev.sh` creates a dev environment with ROS 2 installed. By default, the directory `/workspaces/isaac_ros-dev` in the container is mapped from `~/workspaces/isaac_ros-dev` on the host machine if it exists OR the current working directory from where the script was invoked otherwise. The host directory the container maps to can be explicitly set by running the script with the desired path as the first argument:
  `run_dev.sh -d <path to workspace>`

  `run_dev_rosdep.sh` launches the `ros2_humble.deps.realsense` image. That image now defaults `RMW_IMPLEMENTATION` to Cyclone DDS and creates `~/.realsense-config.json` with DDS enabled and `device-mask: 511` when the file does not already exist. This is required for D555 DDS discovery by `realsense2_camera` inside the container.
