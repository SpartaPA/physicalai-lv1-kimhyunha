import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from turtlesim.action import RotateAbsolute

class RotateClient(Node):
    def __init__(self):
        super().__init__('rotate_client')
        self.declare_parameter('theta', 1.57)  # 목표 각도 rad
        self.declare_parameter('cancel_after_sec', 0.0)  # 0이면 취소 안 함
        self.theta = float(self.get_parameter('theta').value)
        self.cancel_after = float(self.get_parameter('cancel_after_sec').value)
        self.client = ActionClient(self, RotateAbsolute, '/turtle1/rotate_absolute')
        self.get_logger().info(f'RotateClient wait_for_server /turtle1/rotate_absolute theta={self.theta:.2f} cancel_after={self.cancel_after}')
        self.timer = self.create_timer(0.5, self.try_send)

    def try_send(self):
        if not self.client.wait_for_server(timeout_sec=0.5):
            self.get_logger().warn('action server not ready /turtle1/rotate_absolute')
            return
        self.timer.cancel()
        goal = RotateAbsolute.Goal(theta=float(self.theta))
        self.get_logger().info(f'send_goal theta={self.theta:.2f}')
        future = self.client.send_goal_async(goal, feedback_callback=self.feedback_cb)
        future.add_done_callback(self.goal_response_cb)
        if self.cancel_after > 0:
            self.create_timer(self.cancel_after, self.cancel_cb)

    def feedback_cb(self, feedback):
        remaining = feedback.feedback.remaining
        self.get_logger().info(f'feedback remaining={remaining:.3f}')

    def goal_response_cb(self, future):
        handle = future.result()
        if not handle.accepted:
            self.get_logger().warn('goal rejected')
            rclpy.shutdown()
            return
        self.get_logger().info('goal accepted, waiting result...')
        self._goal_handle = handle
        handle.get_result_async().add_done_callback(self.result_cb)

    def cancel_cb(self):
        if hasattr(self, '_goal_handle'):
            self.get_logger().warn(f'cancel request after {self.cancel_after}s')
            self._goal_handle.cancel_goal_async()

    def result_cb(self, future):
        res = future.result()
        status = res.status  # 4: succeeded, 5: canceled 등
        delta = res.result.delta if res.result else float('nan')
        self.get_logger().info(f'result status={status} delta={delta:.3f}')
        # 정상 종료
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = RotateClient()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()
