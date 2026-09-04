import math
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from std_msgs.msg import Float32
from rcl_interfaces.msg import SetParametersResult


class TurtleDistanceNode(Node):
    def __init__(self):
        super().__init__('turtle_distance_node')
        # 최신 자세 보관용
        self.latest_pose: Pose | None = None

        # 구독: /turtle1/pose -> 콜백은 보관만
        self.sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        # 발행: /turtle_distance (Float32) 10Hz
        self.declare_parameter('publish_rate', 10.0)
        self.publish_rate = float(self.get_parameter('publish_rate').value)
        if self.publish_rate <= 0:
            self.get_logger().warn(
                f'잘못된 publish_rate={self.publish_rate}, 기본값 10.0Hz로 동작합니다')
            self.publish_rate = 10.0
        self.get_logger().info(f"publish_rate={self.publish_rate}Hz")
        self.pub = self.create_publisher(Float32, '/turtle_distance', 10)
        self.timer = self.create_timer(1.0 / self.publish_rate, self.timer_callback)
        self.add_on_set_parameters_callback(self.param_callback)

        self.get_logger().info('TurtleDistanceNode started: sub /turtle1/pose -> pub /turtle_distance @10Hz')

    def pose_callback(self, msg: Pose):
        # 최신 자세만 보관, 계산은 하지 않음
        self.latest_pose = msg

    def param_callback(self, params):
        self.get_logger().info('param_callback 호출됨')
        for p in params:
            if p.name == 'publish_rate':
                if p.value > 0:
                    self.publish_rate = float(p.value)
                    self.timer.cancel()
                    self.timer = self.create_timer(1.0 / self.publish_rate, self.timer_callback)
                    self.get_logger().info(f'publish_rate 변경: {self.publish_rate}Hz')
                else:
                    self.get_logger().warn(
                        f'잘못된 publish_rate={p.value} 무시, 현재 {self.publish_rate}Hz 유지')
        return SetParametersResult(successful=True)

    def timer_callback(self):
        if self.latest_pose is None:
            return
        x = self.latest_pose.x
        y = self.latest_pose.y
        dist = math.sqrt(x * x + y * y)  # 원점(0,0)에서의 거리
        out = Float32()
        out.data = float(dist)
        self.pub.publish(out)
        # 필요시 로그 (10Hz라 너무 많으면 주석)
        self.get_logger().debug(f'distance_node.py: distance={dist:.3f} from pose x={x:.2f} y={y:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = TurtleDistanceNode()
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
