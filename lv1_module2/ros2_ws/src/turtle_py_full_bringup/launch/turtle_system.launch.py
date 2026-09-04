from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    bringup_share = get_package_share_directory('turtle_py_full_bringup')
    config_file = os.path.join(bringup_share, 'config', 'params.yaml')
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='turtlesim'),
        Node(package='turtle_py', executable='turtle_distance', name='turtle_distance_node',
             parameters=[config_file]),
        Node(package='turtle_py', executable='turtle_alarm', name='distance_alarm_node',
             parameters=[{'warn_distance': 2.5}]),
        Node(package='turtle_py', executable='turtle_square', name='square_node'),
        # 액션 클라이언트 (필요시 주석 해제: ros2 launch turtle_py_full_bringup turtle_system.launch.py theta:=1.57)
        # Node(package='turtle_py', executable='turtle_rotate', name='rotate_client', parameters=[{'theta': 1.57}]),
        # C++ 동일 규격 노드 (문제 4 교차 검증용, 기본 비활성 시 주석)
        # Node(package='turtle_cpp', executable='turtle_distance_cpp', name='turtle_distance_cpp', parameters=[config_file]),
        # Node(package='turtle_cpp', executable='turtle_alarm_cpp', name='turtle_alarm_cpp', parameters=[{'warn_distance': 3.0}]),
    ])
