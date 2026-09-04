#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/float32.hpp>
#include <rcl_interfaces/msg/set_parameters_result.hpp>

class TurtleAlarmCpp : public rclcpp::Node {
public:
  TurtleAlarmCpp() : Node("distance_alarm_node") {
    this->declare_parameter("warn_distance", 2.5);
    warn_distance_ = this->get_parameter("warn_distance").as_double();

    sub_ = this->create_subscription<std_msgs::msg::Float32>(
      "/turtle_distance", 10,
      std::bind(&TurtleAlarmCpp::callback, this, std::placeholders::_1));

    param_handle_ = this->add_on_set_parameters_callback(
      std::bind(&TurtleAlarmCpp::param_callback, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "DistanceAlarmCpp started: warn_distance=%.2f on /turtle_distance", warn_distance_);
  }

private:
  rcl_interfaces::msg::SetParametersResult param_callback(const std::vector<rclcpp::Parameter> & params) {
    rcl_interfaces::msg::SetParametersResult result;
    result.successful = true;
    for (auto & p : params) {
      if (p.get_name() == "warn_distance") {
        warn_distance_ = p.as_double();
        RCLCPP_INFO(this->get_logger(), "warn_distance 변경: %.2f", warn_distance_);
      }
    }
    return result;
  }

  void callback(const std_msgs::msg::Float32::SharedPtr msg) {
    if (msg->data > warn_distance_) {
      RCLCPP_WARN(this->get_logger(), "거리 경고! %.2f > %.2f (원점으로부터)", msg->data, warn_distance_);
    }
  }

  rclcpp::Subscription<std_msgs::msg::Float32>::SharedPtr sub_;
  rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr param_handle_;
  double warn_distance_{2.5};
};

int main(int argc, char** argv){
  rclcpp::init(argc, argv);
  auto node = std::make_shared<TurtleAlarmCpp>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
