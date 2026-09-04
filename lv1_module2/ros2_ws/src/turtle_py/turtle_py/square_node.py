import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import SetBool, Trigger

class SquareNode(Node):
    def __init__(self):
        super().__init__('square_node')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.state = 0
        self.steps_in_state = 0
        self.forward_steps = 20
        self.turn_steps = 16
        self.enabled = True
        self.latest_pose: Pose | None = None
        self.home: tuple[float, float] | None = None

        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_cb, 10)
        self.srv_toggle = self.create_service(SetBool, 'toggle_drive', self.set_bool_cb)
        self.srv_home = self.create_service(Trigger, 'save_home', self.trigger_cb)

        self.timer = self.create_timer(0.1, self.timer_cb)
        self.get_logger().info('SquareNode started: /turtle1/cmd_vel 정사각형, services toggle_drive(SetBool)/save_home(Trigger)')

    def pose_cb(self, msg: Pose):
        self.latest_pose = msg

    def set_bool_cb(self, req: SetBool.Request, res: SetBool.Response):
        self.enabled = bool(req.data)
        res.success = True
        res.message = f"drive {'ON' if self.enabled else 'OFF'}"
        self.get_logger().info(f'toggle_drive: {res.message}')
        return res

    def trigger_cb(self, req: Trigger.Request, res: Trigger.Response):
        if self.latest_pose is None:
            res.success = False
            res.message = "no pose yet"
        else:
            self.home = (float(self.latest_pose.x), float(self.latest_pose.y))
            res.success = True
            res.message = f"home saved {self.home}"
        self.get_logger().info(f'save_home: {res.message}')
        return res

    def timer_cb(self):
        if not self.enabled:
            return
        msg = Twist()
        if self.state == 0:
            msg.linear.x = 1.0
            msg.angular.z = 0.0
            self.steps_in_state += 1
            if self.steps_in_state >= self.forward_steps:
                self.state = 1
                self.steps_in_state = 0
        else:
            msg.linear.x = 0.0
            msg.angular.z = 1.0
            self.steps_in_state += 1
            if self.steps_in_state >= self.turn_steps:
                self.state = 0
                self.steps_in_state = 0
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = SquareNode()
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
