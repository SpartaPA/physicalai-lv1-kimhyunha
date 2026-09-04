import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import math
class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.br = TransformBroadcaster(self)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.cb, 10)
        self.get_logger().info('TF world -> turtle1 broadcaster ready')
    def cb(self, msg):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'turtle1'
        t.transform.translation.x = float(msg.x)
        t.transform.translation.y = float(msg.y)
        t.transform.translation.z = 0.0
        # yaw theta -> quaternion z/w
        t.transform.rotation.x = 0.0; t.transform.rotation.y = 0.0
        t.transform.rotation.z = math.sin(msg.theta/2); t.transform.rotation.w = math.cos(msg.theta/2)
        self.br.sendTransform(t)
def main(args=None):
    rclpy.init(args=args); n=TFBroadcaster(); 
    try: rclpy.spin(n)
    except KeyboardInterrupt:
        pass
    except rclpy.executors.ExternalShutdownException: pass
    finally: n.destroy_node(); rclpy.shutdown()
