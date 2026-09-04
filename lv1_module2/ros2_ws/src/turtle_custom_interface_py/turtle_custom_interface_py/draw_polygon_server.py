import math
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from geometry_msgs.msg import Twist
from turtle_interfaces.action import DrawPolygon

class DrawPolygonServer(Node):
    def __init__(self):
        super().__init__('draw_polygon_server')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.server = ActionServer(
            self, DrawPolygon, 'draw_polygon',
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb)
        self.get_logger().info('DrawPolygon action server ready on draw_polygon (sides, side_length) -> total_distance, feedback per side')

    def goal_cb(self, goal_request):
        if goal_request.sides < 3:
            self.get_logger().warn(f'goal rejected sides={goal_request.sides} <3')
            return GoalResponse.REJECT
        if goal_request.side_length <= 0:
            self.get_logger().warn(f'goal rejected side_length={goal_request.side_length} <=0')
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        self.get_logger().warn('cancel requested -> stopping')
        # 즉시 정지
        self.pub.publish(Twist())
        return CancelResponse.ACCEPT

    async def execute_cb(self, goal_handle):
        sides = int(goal_handle.request.sides)
        length = float(goal_handle.request.side_length)
        # 속도 가정: 선속 1.0 m/s, 각속 1.0 rad/s (turtlesim 단위)
        linear = 1.0
        angle = 2 * math.pi / sides
        total = 0.0
        self.get_logger().info(f'execute DrawPolygon sides={sides} length={length} angle={math.degrees(angle):.1f}deg')
        for i in range(sides):
            if goal_handle.is_cancel_requested:
                self.pub.publish(Twist())
                goal_handle.canceled()
                self.get_logger().warn(f'canceled at side {i}/{sides}')
                result = DrawPolygon.Result(total_distance=float(total))
                return result
            # 1 변 직진
            dur = length / linear
            t0 = time.time()
            while time.time() - t0 < dur:
                if goal_handle.is_cancel_requested:
                    break
                msg = Twist(); msg.linear.x = linear
                self.pub.publish(msg)
                await self._sleep(0.05)
            self.pub.publish(Twist())
            total += length
            # 회전
            rot_dur = angle / 1.0
            t0 = time.time()
            while time.time() - t0 < rot_dur:
                if goal_handle.is_cancel_requested:
                    break
                msg = Twist(); msg.angular.z = 1.0
                self.pub.publish(msg)
                await self._sleep(0.05)
            self.pub.publish(Twist())
            # 피드백
            fb = DrawPolygon.Feedback(completed_sides=i+1, progress=float((i+1)/sides))
            goal_handle.publish_feedback(fb)
            self.get_logger().info(f'feedback {i+1}/{sides} progress={fb.progress:.2f}')
            if goal_handle.is_cancel_requested:
                self.pub.publish(Twist())
                goal_handle.canceled()
                self.get_logger().warn(f'canceled after side {i+1}')
                return DrawPolygon.Result(total_distance=float(total))
        self.pub.publish(Twist())
        goal_handle.succeed()
        self.get_logger().info(f'succeeded total_distance={total:.2f}')
        return DrawPolygon.Result(total_distance=float(total))

    async def _sleep(self, sec):
        # rclpy awaitable sleep
        import asyncio
        await asyncio.sleep(sec)

def main(args=None):
    rclpy.init(args=args)
    node = DrawPolygonServer()
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
