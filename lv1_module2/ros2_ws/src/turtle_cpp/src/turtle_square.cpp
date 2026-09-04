#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <turtlesim/msg/pose.hpp>
#include <std_srvs/srv/set_bool.hpp>
#include <std_srvs/srv/trigger.hpp>

class SquareCpp : public rclcpp::Node {
public:
  SquareCpp() : Node("square_node") {
    pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
    pose_sub_ = this->create_subscription<turtlesim::msg::Pose>(
      "/turtle1/pose", 10, [this](turtlesim::msg::Pose::SharedPtr m){ latest_ = m; });
    srv_toggle_ = this->create_service<std_srvs::srv::SetBool>(
      "toggle_drive",
      [this](const std::shared_ptr<std_srvs::srv::SetBool::Request> req,
             std::shared_ptr<std_srvs::srv::SetBool::Response> res){
        enabled_ = req->data;
        res->success = true;
        res->message = std::string("drive ") + (enabled_ ? "ON" : "OFF");
        RCLCPP_INFO(this->get_logger(), "toggle_drive: %s", res->message.c_str());
      });
    srv_home_ = this->create_service<std_srvs::srv::Trigger>(
      "save_home",
      [this](const std::shared_ptr<std_srvs::srv::Trigger::Request>,
             std::shared_ptr<std_srvs::srv::Trigger::Response> res){
        if (!latest_) { res->success = false; res->message = "no pose yet"; }
        else {
          home_x_ = latest_->x; home_y_ = latest_->y; has_home_ = true;
          res->success = true;
          res->message = "home saved [" + std::to_string(home_x_) + ", " + std::to_string(home_y_) + "]";
        }
        RCLCPP_INFO(this->get_logger(), "save_home: %s", res->message.c_str());
      });
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(100),
      std::bind(&SquareCpp::timer_cb, this));
    RCLCPP_INFO(this->get_logger(), "SquareCpp started: /turtle1/cmd_vel + services toggle_drive/save_home");
  }
private:
  void timer_cb() {
    if (!enabled_) return;
    geometry_msgs::msg::Twist msg;
    if (state_ == 0) { msg.linear.x = 1.0; msg.angular.z = 0.0; steps_in_state_++; if (steps_in_state_ >= forward_steps_) { state_ = 1; steps_in_state_ = 0; } }
    else { msg.linear.x = 0.0; msg.angular.z = 1.0; steps_in_state_++; if (steps_in_state_ >= turn_steps_) { state_ = 0; steps_in_state_ = 0; } }
    pub_->publish(msg);
  }
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr pub_;
  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_sub_;
  rclcpp::Service<std_srvs::srv::SetBool>::SharedPtr srv_toggle_;
  rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr srv_home_;
  rclcpp::TimerBase::SharedPtr timer_;
  turtlesim::msg::Pose::SharedPtr latest_{nullptr};
  bool enabled_{true};
  double home_x_{0}, home_y_{0}; bool has_home_{false};
  int state_{0}, steps_in_state_{0};
  const int forward_steps_{20}, turn_steps_{16};
};
int main(int argc, char** argv){
  rclcpp::init(argc, argv);
  auto node = std::make_shared<SquareCpp>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
