#!/bin/bash
# entrypoint.sh

set -e

if [ -f "/opt/ros/${ROS_DISTRO}/setup.bash" ]; then
  # Load the ROS environment provided by the base image
  source "/opt/ros/${ROS_DISTRO}/setup.bash"
fi

if [ -f "${HOME}/orbbec_ws/install/setup.bash" ]; then
  source "${HOME}/orbbec_ws/install/setup.bash"
fi

if [ -S /run/udev/control ]; then
  echo "[entrypoint] Reloading udev rules"
  sudo udevadm control --reload-rules && sudo udevadm trigger || echo "[entrypoint] udev reload failed"
else
  echo "[entrypoint] Skipping udev reload (udev control socket not available)"
fi

exec "$@"
