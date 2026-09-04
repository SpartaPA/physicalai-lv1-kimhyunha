from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    bringup_share = get_package_share_directory('turtle_cpp_full_bringup')
    config_file = os.path.join(bringup_share, 'config', 'params.yaml')
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='turtlesim'),
        Node(package='turtle_cpp', executable='turtle_distance_cpp', name='turtle_distance_node',
             parameters=[config_file]),
        Node(package='turtle_cpp', executable='turtle_alarm_cpp', name='distance_alarm_node',
             parameters=[{'warn_distance': 2.5}]),
        Node(package='turtle_cpp', executable='turtle_square_cpp', name='square_node'),
        # Node(package='turtle_cpp', executable='rotate_client_cpp', name='rotate_client', parameters=[{'theta': 1.57}]),
    ])
