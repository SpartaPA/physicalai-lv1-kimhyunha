import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from turtle_interfaces.msg import Waypoint, WaypointList

class WaypointPublisher(Node):
    def __init__(self):
        super().__init__('waypoint_publisher')
        self.declare_parameter('num_points', 4)  # 0이면 빈 목록 → 경고 후 발행 건너뜀
        self.pub = self.create_publisher(WaypointList, '/waypoints', 10)
        self.timer = self.create_timer(1.0, self.publish)
        self.get_logger().info('WaypointPublisher on /waypoints (WaypointList) 1Hz')

    def publish(self):
        hdr = Header(stamp=self.get_clock().now().to_msg(), frame_id='world')
        all_points = [
            Waypoint(x=1.0, y=1.0, tolerance=0.1, label='a'),
            Waypoint(x=4.0, y=2.0, tolerance=0.2, label='b'),
            Waypoint(x=2.0, y=5.0, tolerance=0.15, label='c'),
            Waypoint(x=5.5, y=5.5, tolerance=0.1, label='home'),
        ]
        n = int(self.get_parameter('num_points').value)
        wps = all_points[:max(0, n)]
        if not wps:
            self.get_logger().warn('빈 경유점 목록(num_points=0), 발행을 건너뜁니다')
            return
        msg = WaypointList(header=hdr, waypoints=wps)
        self.pub.publish(msg)
        self.get_logger().info(f'published WaypointList {len(wps)} points')

def main(args=None):
    rclpy.init(args=args)
    node = WaypointPublisher()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        try:
            if rclpy.ok():
                node.destroy_node()
        except Exception:
            pass
        try:
            if rclpy.ok():
                rclpy.shutdown()
        except Exception:
            pass
if __name__ == '__main__':
    main()
