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

exec "$@"
