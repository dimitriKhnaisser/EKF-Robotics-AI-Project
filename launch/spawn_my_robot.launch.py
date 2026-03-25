from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Path to your URDF
    urdf_file = os.path.join(
        get_package_share_directory('my_robot_pkg'),
        'urdf',
        'my_robot.urdf'
    )
    ekf_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('my_robot_pkg'),
            'launch',
            'ekf.launch.py'
        )
    )
)

    return LaunchDescription([
        # Start Gazebo
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),

        # Run robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            arguments=[urdf_file]
        ),

        # Spawn your robot in Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'minimal_robot', '-file', urdf_file],
            output='screen'
        ),
        Node(
            package='my_robot_pkg',
            executable='ground_truth_extraction',
            name='ground_truth_extraction',
            output='screen'
        ),
        Node(
            package='my_robot_pkg',
            executable='auto_rectangle',  # your motion script
            name='auto_rectangle',
            output='screen'
        ),
        Node(
            package='my_robot_pkg',
            executable='noisy_odom',
            name='noisy_odom'
        ),
        Node(
            package='my_robot_pkg',
            executable='noisy_data_extraction',
            name='noisy_data_extraction'
        ),
        Node(
            package='my_robot_pkg',
            executable='imu_fix',
            name='imu_fix'
        ),
        Node(
            package='my_robot_pkg',
            executable='ekf_data_extraction',
            name='ekf_data_extraction'
        ),
        ekf_launch,
    ])