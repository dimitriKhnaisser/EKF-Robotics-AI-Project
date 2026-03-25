from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():

    config = os.path.join(
        '/home/dimi/ros2_ws/src/my_robot_pkg/config',
        'ekf.yaml'
    )

    return LaunchDescription([

        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[config]
        )
    ])