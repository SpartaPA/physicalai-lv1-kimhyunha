#include <rclcpp/rclcpp.hpp>
#include <turtlesim/msg/pose.hpp>
#include <std_msgs/msg/float32.hpp>
#include <rcl_interfaces/msg/set_parameters_result.hpp>
#include <cmath>

class TurtleDistanceCpp : public rclcpp::Node {
public:
  TurtleDistanceCpp() : Node("turtle_distance_node") {
    this->declare_parameter("publish_rate", 10.0);
    publish_rate_ = this->get_parameter("publish_rate").as_double();
    RCLCPP_INFO(this->get_logger(), "publish_rate=%.1f Hz", publish_rate_);

    sub_ = this->create_subscription<turtlesim::msg::Pose>(
      "/turtle1/pose", 10,
      [this](turtlesim::msg::Pose::SharedPtr msg){ latest_ = msg; });

    pub_ = this->create_publisher<std_msgs::msg::Float32>("/turtle_distance", 10);

    timer_ = this->create_wall_timer(
      std::chrono::duration<double>(1.0 / publish_rate_),
      std::bind(&TurtleDistanceCpp::timer_callback, this));

    param_handle_ = this->add_on_set_parameters_callback(
      std::bind(&TurtleDistanceCpp::param_callback, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "TurtleDistanceCpp started: sub /turtle1/pose -> pub /turtle_distance @%.1fHz", publish_rate_);
  }

private:
  rcl_interfaces::msg::SetParametersResult param_callback(const std::vector<rclcpp::Parameter> & params) {
    RCLCPP_INFO(this->get_logger(), "param_callback 호출됨");
    rcl_interfaces::msg::SetParametersResult result;
    result.successful = true;
    for (auto & p : params) {
      if (p.get_name() == "publish_rate" && p.as_double() > 0) {
        publish_rate_ = p.as_double();
        timer_->cancel();
        timer_ = this->create_wall_timer(
          std::chrono::duration<double>(1.0 / publish_rate_),
          std::bind(&TurtleDistanceCpp::timer_callback, this));
        RCLCPP_INFO(this->get_logger(), "publish_rate 변경: %.1f Hz", publish_rate_);
      }
    }
    return result;
  }

  void timer_callback() {
    if (!latest_) return;
    std_msgs::msg::Float32 out;
    out.data = std::hypot(latest_->x, latest_->y);
    pub_->publish(out);
  }

  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr sub_;
  rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr pub_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr param_handle_;
  turtlesim::msg::Pose::SharedPtr latest_{nullptr};
  double publish_rate_{10.0};
};

int main(int argc, char** argv){
  rclcpp::init(argc, argv);
  auto node = std::make_shared<TurtleDistanceCpp>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
