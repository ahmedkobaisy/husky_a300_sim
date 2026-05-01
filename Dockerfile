FROM osrf/ros:jazzy-desktop

# Install system dependencies & Clearpath packages
RUN apt-get update && apt-get install -y \
    ros-jazzy-clearpath-simulator \
    ros-jazzy-clearpath-desktop \
    ros-jazzy-slam-toolbox \
    ros-jazzy-nav2-bringup \
    ros-jazzy-teleop-twist-keyboard \
    ros-jazzy-ros-gz-bridge \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Workspace Setup
WORKDIR /ros2_ws

# Clone clearpath_nav2_demos
RUN . /opt/ros/jazzy/setup.sh && \
    mkdir -p /ros2_ws/src && \
    cd /ros2_ws/src && \
    git clone https://github.com/clearpathrobotics/clearpath_nav2_demos

# Copy your local files into workspace
COPY . /ros2_ws/

# Fix entrypoint line endings & permissions
RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix /ros2_ws/entrypoint.sh && \
    chmod +x /ros2_ws/entrypoint.sh && \
    rm -rf /var/lib/apt/lists/*

# Build the workspace
RUN . /opt/ros/jazzy/setup.sh && \
    cd /ros2_ws && \
    colcon build --packages-select clearpath_nav2_demos \
    --cmake-args -DCMAKE_BUILD_TYPE=Release

# Source ROS and workspace in .bashrc for interactive shells
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc && \
    echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc && \
    echo "export HUSKY_LASER_ENABLED=true" >> ~/.bashrc

ENTRYPOINT ["/ros2_ws/entrypoint.sh"]
CMD ["bash"]
