#!/bin/bash
# Minimal runtime entrypoint for the Orbbec Femto Bolt container.

set -euo pipefail

run_as_root() {
  if [ "$(id -u)" -eq 0 ]; then
    "$@"
  elif command -v sudo >/dev/null 2>&1; then
    sudo -n "$@" 2>/dev/null || sudo "$@"
  else
    "$@"
  fi
}

if [ -f "/opt/ros/${ROS_DISTRO}/setup.bash" ]; then
  # Allow ROS setup scripts to export undefined variables.
  set +u
  source "/opt/ros/${ROS_DISTRO}/setup.bash"
  set -u
fi

if [ -f "${HOME}/orbbec_ws/install/setup.bash" ]; then
  set +u
  source "${HOME}/orbbec_ws/install/setup.bash"
  set -u
fi

if [ -S /run/udev/control ]; then
  if command -v udevadm >/dev/null 2>&1; then
    echo "[entrypoint] Reloading udev rules"
    run_as_root udevadm control --reload-rules && run_as_root udevadm trigger || \
      echo "[entrypoint] udev reload failed"
  else
    echo "[entrypoint] Skipping udev reload (udevadm not installed)"
  fi
else
  echo "[entrypoint] Skipping udev reload (udev control socket not available)"
fi

exec "$@"
