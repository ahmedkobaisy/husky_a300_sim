# Husky A300 ROS 2 Jazzy Simulation (Docker-Based)

## Project Overview

This project provides a reproducible simulation setup for the Clearpath Husky A300 using ROS 2 Jazzy inside Docker.

The system includes:

* LiDAR-based SLAM
* Teleoperation via ROS 2 topics
* Sensor bridging between Gazebo and ROS 2
* Visualization in RViz (TF, LaserScan, Map, Camera)
* Map saving using Nav2

The development was performed under constrained hardware conditions (low VRAM), requiring headless simulation and multiple debugging steps across Gazebo, ROS 2, TF, and QoS configurations.

---

## Environment

* OS: Ubuntu 24.04 (Noble)
* ROS 2: Jazzy Jalisco
* Gazebo: Harmonic (via clearpath_gz)
* Docker: docker-compose / Dev Container
* Base Image: osrf/ros:jazzy-desktop

### Packages / Repositories

* slam_toolbox
* nav2_bringup
* nav2_map_server
* ros_gz_bridge
* teleop_twist_keyboard
* clearpath_gz
* clearpath_nav2_demos
* clearpath_config

---

## Build

```bash
docker compose build --no-cache
docker compose up --build
```

Enter container:

```bash
docker exec -it husky_jazzy_sim bash
```

Setup workspace:

```bash
cd /ros2_ws/src
git clone https://github.com/clearpathrobotics/clearpath_nav2_demos
cd /ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select clearpath_nav2_demos
```

---

## Run

### X11 Setup (for GUI)

```bash
xhost +local:root
touch /tmp/.docker.xauth
xauth nlist "$DISPLAY" | sed -e 's/^..../ffff/' | xauth -f /tmp/.docker.xauth nmerge -
```

### Launch Simulation

Headless (recommended):

```bash
ros2 launch launch/sim.launch.py gz_args:="-s -r"
```

With GUI:

```bash
ros2 launch launch/sim.launch.py
```


---

### Run SLAM

```bash
ros2 launch clearpath_nav2_demos slam.launch.py use_rviz:=false
```

---

### RViz

```bash
rviz2 -d /ros2_ws/rviz/husky_demo.rviz
```

Required settings:

* Fixed Frame: odom
* Map QoS: Transient Local

---

### Teleoperation

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

---

### Save Map

```bash
ros2 run nav2_map_server map_saver_cli -f /ros2_ws/config/map \
--ros-args -p map:=/cpr_a300_0001/map
```

---

## Stop / Cleanup

```bash
pkill -f ros2
pkill -f gz
docker compose down
```
 ## Verify Everything
  
# All topics
ros2 topic list | grep cpr_a300

# LiDAR
ros2 topic hz /cpr_a300_0001/sensors/lidar2d_0/scan

# Camera
ros2 topic hz /cpr_a300_0001/camera/image

# Map
ros2 topic hz /cpr_a300_0001/map

# TF
ros2 topic hz /tf


## Troubleshooting

### Simulation crashes (VRAM limitation)

Error: Rendering crash / Ogre2 issues
Cause: Limited GPU memory (~128MB)
Fix:

```bash
ros2 launch launch/sim.launch.py gz_args:="-s"
```

---

### Gazebo crashes on restart

Error: Escalating to SIGKILL
Cause: Missing OpenGL fallback inside container
Fix:

```bash
export LIBGL_ALWAYS_SOFTWARE=1
export MESA_GL_VERSION_OVERRIDE=3.3
export MESA_GLSL_VERSION_OVERRIDE=330
export GZ_RENDER_ENGINE_GUI=ogre
export GZ_PARTIAL_RENDERING=1
```

---

### LiDAR not publishing

Error: scan topic missing
Cause: Incorrect topic or sensor configuration
Fix: Use correct topic:

```
/cpr_a300_0001/sensors/lidar2d_0/scan
```

---

### LiDAR data not reaching ROS 2

Cause: Missing or incorrect bridge configuration
Fix:

```yaml
- ros_topic_name: "/cpr_a300_0001/sensors/lidar2d_0/scan"
  gz_topic_name: "/cpr_a300_0001/sensors/lidar2d_0/scan"
  ros_type_name: "sensor_msgs/msg/LaserScan"
  gz_type_name: "gz.msgs.LaserScan"
  direction: GZ_TO_ROS
  lazy: false
```

---

### No map in RViz

Error: No map received
Cause: QoS mismatch
Fix: Set Map display QoS to Transient Local

---

### SLAM not building map

Cause 1: Topic mismatch
Fix: Ensure SLAM subscribes to the correct scan topic

Cause 2: TF not global
Fix: Relay TF from namespaced topic to global /tf

---

### Robot not moving

Cause 1: Wrong topic
Use:

```
/cpr_a300_0001/platform/cmd_vel
```

Cause 2: Wrong message type
Fix: Use TwistStamped instead of Twist

Cause 3: QoS mismatch

```bash
--qos-reliability best_effort
```

---

### Teleop not working

Cause: Controller expects TwistStamped
Fix: Use a conversion node (Twist → TwistStamped)

---

### Missing robot.yaml

Fix:

```bash
mkdir -p /root/.clearpath /etc/clearpath
cp /ros2_ws/config/robot.yaml /root/.clearpath/robot.yaml
cp /ros2_ws/config/robot.yaml /etc/clearpath/robot.yaml
```

---

### Wrong battery model

Error: Invalid battery model
Fix:

```yaml
model: S_24V20_U1
```

---

### No camera topic

Cause: Camera not defined in robot configuration
Fix: Add camera to robot.yaml and bridge configuration

---

## Notes

* Namespace: /cpr_a300_0001
* TF Tree: map → odom → base_link
* SLAM publishes: /cpr_a300_0001/map
* RViz Fixed Frame: odom
* QoS: Best Effort for LaserScan
* docker exec does not inherit environment variables → define in .bashrc or entrypoint
* /config is volume-mounted (no rebuild required)

---

## Optional Extension

The use of a Gazebo actor (dynamic entity in the simulation) was considered as an optional extension to introduce moving obstacles and evaluate SLAM robustness under dynamic conditions.

This was not implemented in the current version of the project.
