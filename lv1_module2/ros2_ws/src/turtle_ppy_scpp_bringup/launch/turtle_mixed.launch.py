from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    share = get_package_share_directory('turtle_ppy_scpp_bringup')
    config_file = os.path.join(share, 'config', 'params.yaml')
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='turtlesim'),
        # 발행자: rclpy (Python) - /turtle1/pose -> /turtle_distance
        Node(package='turtle_py', executable='turtle_distance', name='turtle_distance_node',
             parameters=[config_file]),
        # 수신자: rclcpp (C++) - /turtle_distance 구독, warn 로그
        Node(package='turtle_cpp', executable='turtle_alarm_cpp', name='distance_alarm_node',
             parameters=[{'warn_distance': 2.5}]),
        # 선택: 정사각형 주행은 py 버전으로 (cmd_vel 발행) - 혼합 검증용
        Node(package='turtle_py', executable='turtle_square', name='square_node'),
        # 액션 클라이언트 예시 (택1)
        # Node(package='turtle_py', executable='turtle_rotate', name='rotate_client', parameters=[{'theta': 1.57}]),
        # Node(package='turtle_cpp', executable='rotate_client_cpp', name='rotate_client_cpp', parameters=[{'theta': 0.0}]),
    ])
