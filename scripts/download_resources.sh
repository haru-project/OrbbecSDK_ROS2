#!/bin/bash

# Check if user is root/running with sudo
if [ "$(whoami)" != root ]; then
  echo "[download_resources] Please run this script with sudo"
  exit
fi

ROS_DISTRO=${ROS_DISTRO:-jazzy}

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT_DIR="$(cd "${CURR_DIR}/.." && pwd -P)"
RULE_FILE="${ROOT_DIR}/orbbec_camera/scripts/99-obsensor-libusb.rules"

echo "[download_resources] Script path: ${BASH_SOURCE[0]}"
echo "[download_resources] CURR_DIR=${CURR_DIR}"
echo "[download_resources] ROOT_DIR=${ROOT_DIR}"
echo "[download_resources] RULE_FILE=${RULE_FILE}"

if [ ! -f "${RULE_FILE}" ]; then
  echo "[download_resources] ERROR: Could not find udev rules file at ${RULE_FILE}"
  exit 1
fi

PLATFORM="$(uname -s)"
echo "[download_resources] Detected platform: ${PLATFORM}"

# assume you have sourced ROS environment, same blow
echo "[download_resources] Installing ROS dependencies"
apt-get update -y
apt-get install -y \
  libgflags-dev \
  nlohmann-json3-dev \
  ros-${ROS_DISTRO}-image-transport \
  ros-${ROS_DISTRO}-image-transport-plugins \
  ros-${ROS_DISTRO}-compressed-image-transport \
  ros-${ROS_DISTRO}-image-publisher \
  ros-${ROS_DISTRO}-camera-info-manager \
  ros-${ROS_DISTRO}-diagnostic-updater \
  ros-${ROS_DISTRO}-diagnostic-msgs \
  ros-${ROS_DISTRO}-statistics-msgs \
  ros-${ROS_DISTRO}-backward-ros \
  libdw-dev

if [ "${PLATFORM}" != "Darwin" ]; then
  # Install UDEV rules for USB device
  cp "${RULE_FILE}" /etc/udev/rules.d/99-obsensor-libusb.rules
  echo "[download_resources] Installed udev rules at /etc/udev/rules.d/99-obsensor-libusb.rules"
else
  echo "[download_resources] Skipping udev rule installation on macOS"
fi
echo "[download_resources] Reloading udev rules"
udevadm control --reload-rules && udevadm trigger
echo "[download_resources] Udev rules reload done"
echo "[download_resources] Finished"
