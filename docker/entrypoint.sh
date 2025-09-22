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

exec "$@"
