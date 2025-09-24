FROM ghcr.io/haru-project/perception-jazzy-base:latest

ARG ROS_DISTRO=jazzy
ENV ROS_DISTRO=${ROS_DISTRO}
ENV DEBIAN_FRONTEND=noninteractive

# Install the dependencies that scripts/download_resources.sh would normally
# pull in when running on a host system.
RUN sudo apt-get update && sudo apt-get install -y \
    udev \
    usbutils \
    v4l-utils \
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

# Ensure runtime user belongs to device groups
RUN sudo usermod -aG video ${HARU_USER} && sudo usermod -aG plugdev ${HARU_USER}

# Ship udev rules for Orbbec devices
COPY --chown=root:root orbbec_camera/scripts/99-obsensor-libusb.rules /etc/udev/rules.d/99-obsensor-libusb.rules
RUN sudo chmod 644 /etc/udev/rules.d/99-obsensor-libusb.rules && \
    sudo udevadm control --reload-rules || true

WORKDIR /home/${HARU_USER}/orbbec_ws/src
COPY --chown=${HARU_USER}:${HARU_GROUP} . /home/${HARU_USER}/orbbec_ws/src/OrbbecSDK_ROS2

WORKDIR /home/${HARU_USER}/orbbec_ws
RUN sudo chown -R ${HARU_USER}:${HARU_GROUP} /home/${HARU_USER}/orbbec_ws && \
    bash -lc "source /opt/ros/${ROS_DISTRO}/setup.bash && colcon build --merge-install --event-handlers console_direct+" && \
    rm -rf build log

COPY --chown=${HARU_USER}:${HARU_GROUP} docker/entrypoint.sh ${HOME}/entrypoint.sh
RUN sudo chmod +x ${HOME}/entrypoint.sh
