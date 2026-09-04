import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
class MarkerPub(Node):
    def __init__(self):
        super().__init__('marker_publisher')
        self.pub = self.create_publisher(Marker, '/waypoint_markers', 10)
        self.timer = self.create_timer(1.0, self.publish)
        self.get_logger().info('Marker publisher /waypoint_markers (Fixed Frame: world)')
    def publish(self):
        m = Marker()
        m.header.frame_id = 'world'; m.header.stamp = self.get_clock().now().to_msg()
        m.ns = 'waypoints'; m.id = 0; m.type = Marker.SPHERE_LIST; m.action = Marker.ADD
        m.scale.x = 0.3; m.scale.y = 0.3; m.scale.z = 0.3
        m.color.r = 1.0; m.color.g = 0.0; m.color.b = 0.0; m.color.a = 1.0
        pts = [(1,1,0),(4,2,0),(2,5,0),(5.5,5.5,0)]
        m.points = [Point(x=float(x), y=float(y), z=float(z)) for x,y,z in pts]
        self.pub.publish(m)
def main(args=None):
    rclpy.init(args=args); n=MarkerPub();
    try: rclpy.spin(n)
    except KeyboardInterrupt:
        pass
    except rclpy.executors.ExternalShutdownException: pass
    finally: n.destroy_node(); rclpy.shutdown()
