from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # In Jazzy nutzen wir clearpath_gz statt clearpath_simulator
    pkg_clearpath_gz = FindPackageShare('clearpath_gz')

    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg_clearpath_gz, 'launch', 'simulation.launch.py'])
        ]),
        launch_arguments={
            'setup_path': '/ros2_ws/config/' 
        }.items()
    )

    return LaunchDescription([
        sim_launch
    ])