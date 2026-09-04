#include <rclcpp/rclcpp.hpp>
#include <turtle_interfaces/msg/waypoint.hpp>
#include <turtle_interfaces/msg/waypoint_list.hpp>

class WaypointPublisher : public rclcpp::Node {
public:
  WaypointPublisher() : Node("waypoint_publisher"){
    pub_ = this->create_publisher<turtle_interfaces::msg::WaypointList>("/waypoints", 10);
    timer_ = this->create_wall_timer(std::chrono::seconds(1), [this]{
      turtle_interfaces::msg::WaypointList msg;
      msg.header.stamp = this->now();
      msg.header.frame_id = "world";
      turtle_interfaces::msg::Waypoint a; a.x=1; a.y=1; a.tolerance=0.1; a.label="a";
      turtle_interfaces::msg::Waypoint b; b.x=4; b.y=2; b.tolerance=0.2; b.label="b";
      turtle_interfaces::msg::Waypoint c; c.x=2; c.y=5; c.tolerance=0.15; c.label="c";
      turtle_interfaces::msg::Waypoint d; d.x=5.5; d.y=5.5; d.tolerance=0.1; d.label="home";
      msg.waypoints = {a,b,c,d};
      pub_->publish(msg);
      RCLCPP_INFO(this->get_logger(), "published WaypointList %zu", msg.waypoints.size());
    });
  }
private:
  rclcpp::Publisher<turtle_interfaces::msg::WaypointList>::SharedPtr pub_;
  rclcpp::TimerBase::SharedPtr timer_;
};
int main(int argc, char** argv){
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<WaypointPublisher>());
  rclcpp::shutdown();
  return 0;
}
