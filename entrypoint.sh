#!/bin/bash
set -e

# ROS 2 Umgebung laden
source "/opt/ros/jazzy/setup.bash"

# Falls vorhanden, den lokalen Workspace laden
if [ -f "/ros2_ws/install/setup.bash" ]; then
  source "/ros2_ws/install/setup.bash"
fi

# Enable Husky LiDAR
export HUSKY_LASER_ENABLED=true

# Auto-copy robot.yaml to required locations
mkdir -p /root/.clearpath /etc/clearpath
cp /ros2_ws/config/robot.yaml /root/.clearpath/robot.yaml
cp /ros2_ws/config/robot.yaml /etc/clearpath/robot.yaml

exec "$@"
