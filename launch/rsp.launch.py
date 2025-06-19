import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro

def generate_launch_description():

    # Use sim time launch argument - if needed
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_ros2_control = LaunchConfiguration('use_ros2_control')

    # Get path to the package and xacro file
    pkg_path = get_package_share_directory('mandooka')
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')

    # Process the xacro file
    robot_description_config = Command(['xacro ', xacro_file, ' use_ros2_control:=', use_ros2_control])

    # Define robot_state_publisher node
    params = {
        'robot_description': robot_description_config,
        'use_sim_time': use_sim_time
    }

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # Return LaunchDescription object
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time if true'
        ),
        DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2_control if true'
        ),        
        node_robot_state_publisher
    ])
