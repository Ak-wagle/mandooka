import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

# from launch.actions import ExecuteProcess

def generate_launch_description():

    package_name='mandooka'

    gazebo_params_file = os.path.join(get_package_share_directory(package_name),'config','gazebo_params.yaml')

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    # Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
             )

    # if gazebo doesn't open --> source /usr/share/gazebo/setup.bash

    # # explicitly pass the factory plugin for gazzebo to load the factory plugin
    # gazebo = IncludeLaunchDescription(
    # PythonLaunchDescriptionSource([
    #     os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
    # ]),
    # launch_arguments={
    #     'extra_gazebo_args': '--verbose -s libgazebo_ros_factory.so'
    # }.items())

    # # Explicitly passing the factory plugin
    # gazebo = ExecuteProcess(
    #     cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
    #     output='screen'
    # )

    # Spawner node from the gazebo_ros package. The entity name matters only if you have multiple robots.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'mandooka'],
                        output='screen')
    
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        diff_drive_spawner,
        joint_broad_spawner,
    ])