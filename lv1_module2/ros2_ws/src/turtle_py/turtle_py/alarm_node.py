import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class DistanceAlarmNode(Node):
    def __init__(self):
        super().__init__('distance_alarm_node')
        self.declare_parameter('warn_distance', 2.5)
        self.warn_distance = float(self.get_parameter('warn_distance').value)
        self.sub = self.create_subscription(Float32, '/turtle_distance', self.callback, 10)
        self.add_on_set_parameters_callback(self.param_callback)
        self.get_logger().info(f'DistanceAlarmNode started: warn_distance={self.warn_distance} on /turtle_distance')

    def param_callback(self, params):
        from rcl_interfaces.msg import SetParametersResult
        for p in params:
            if p.name == 'warn_distance':
                self.warn_distance = float(p.value)
                self.get_logger().info(f'warn_distance 변경: {self.warn_distance}')
        return SetParametersResult(successful=True)

    def callback(self, msg: Float32):
        if msg.data > self.warn_distance:
            self.get_logger().warn(f'거리 경고! {msg.data:.2f} > {self.warn_distance} (원점으로부터)')

def main(args=None):
    rclpy.init(args=args)
    node = DistanceAlarmNode()
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
