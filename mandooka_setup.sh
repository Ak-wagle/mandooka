#!/bin/bash

echo "[INFO] Enter sudo password..."
sudo -v

(sudo -v; while true; do sleep 60; sudo -n true; done) 2>/dev/null &

ARCH=$(uname -m)
echo "[INFO] Detected architecture: $ARCH"

install_common_packages() {
    echo "[INFO] Installing common ROS 2 packages..."
    sudo apt update
    sudo apt install -y \
        ros-humble-robot-state-publisher \
        ros-humble-joint-state-publisher \
        ros-humble-joint-state-publisher-gui \
        ros-humble-xacro \
        ros-humble-twist-mux \
        ros-humble-gazebo-ros \
        ros-humble-gazebo-ros-pkgs
}

install_sbc_packages() {
    echo "[INFO] Installing SBC specific packages..."
    sudo apt install -y \
        ros-humble-rplidar-ros \
        ros-humble-ros2-control \
        ros-humble-ros2-controllers
}

install_pc_packages() {
    echo "[INFO] Installing Remote PC specific packages..."
    sudo apt install -y \
        ros-humble-navigation2 \
        ros-humble-nav2-bringup \
        ros-humble-slam-toolbox \
        ros-humble-rviz2 \
        ros-humble-gazebo-plugins
}

if [ "$ARCH" = "aarch64" ]; then
    echo "[INFO] SBC detected."
    install_common_packages
    install_sbc_packages
else
    echo "[INFO] Remote PC detected."
    install_common_packages
    install_pc_packages
fi

echo "[INFO] Dependency installation completed"
