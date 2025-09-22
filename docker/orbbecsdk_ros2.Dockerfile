FROM ghcr.io/haru-project/perception-jazzy-base:latest

ARG ROS_DISTRO=jazzy
ENV ROS_DISTRO=${ROS_DISTRO}
ENV DEBIAN_FRONTEND=noninteractive

# General dependencies for Orbbec SDK build and runtime
RUN sudo apt-get update && sudo apt-get install -y \
    udev \
    usbutils \
    libglfw3 \
    libgl1 \
    libasound2-data \
    ros-${ROS_DISTRO}-joint-state-publisher \
    golang-go \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo-dev \
    python3-vcstools \
    debconf-utils \
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
    libdw-dev && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*

# Ensure the updated udev rules are applied
RUN sudo udevadm control --reload-rules && sudo udevadm trigger

COPY --chown=${HARU_USER}:${HARU_GROUP} docker/entrypoint.sh ${HOME}/entrypoint.sh
RUN sudo chmod +x ${HOME}/entrypoint.sh
