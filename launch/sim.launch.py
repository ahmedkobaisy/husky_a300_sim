from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    pkg_clearpath_gz = FindPackageShare('clearpath_gz')

    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg_clearpath_gz, 'launch', 'simulation.launch.py'])
        ]),
        launch_arguments={
            'setup_path': '/ros2_ws/config/'
        }.items()
    )

    # LiDAR Bridge (no lazy mode)
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='scan_bridge',
        arguments=['--ros-args', '-p',
                  'config_file:=/ros2_ws/config/bridge.yaml'],
        output='screen'
    )

    # Twist Converter (Twist → TwistStamped)
    twist_converter = ExecuteProcess(
        cmd=['python3', '/ros2_ws/config/twist_converter.py'],
        output='screen'
    )

    return LaunchDescription([
        sim_launch,
        bridge_node,
        twist_converter
    ])
