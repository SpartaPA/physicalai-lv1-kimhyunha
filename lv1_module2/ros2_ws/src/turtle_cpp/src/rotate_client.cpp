#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <turtlesim/action/rotate_absolute.hpp>

class RotateClientCpp : public rclcpp::Node {
public:
  using RotateAbsolute = turtlesim::action::RotateAbsolute;
  using GoalHandle = rclcpp_action::ClientGoalHandle<RotateAbsolute>;
  RotateClientCpp() : Node("rotate_client_cpp") {
    this->declare_parameter("theta", 1.57);
    this->declare_parameter("cancel_after_sec", 0.0);
    theta_ = this->get_parameter("theta").as_double();
    cancel_after_ = this->get_parameter("cancel_after_sec").as_double();
    client_ = rclcpp_action::create_client<RotateAbsolute>(this, "/turtle1/rotate_absolute");
    RCLCPP_INFO(this->get_logger(), "RotateClientCpp wait /turtle1/rotate_absolute theta=%.2f cancel_after=%.2f", theta_, cancel_after_);
    timer_ = this->create_wall_timer(std::chrono::milliseconds(500), [this]{ try_send(); });
  }
private:
  void try_send(){
    if (!client_->wait_for_action_server(std::chrono::milliseconds(500))) {
      RCLCPP_WARN(this->get_logger(), "action server not ready");
      return;
    }
    timer_->cancel();
    auto goal = RotateAbsolute::Goal(); goal.theta = theta_;
    RCLCPP_INFO(this->get_logger(), "send_goal theta=%.2f", theta_);
    auto opts = rclcpp_action::Client<RotateAbsolute>::SendGoalOptions();
    opts.feedback_callback = [this](GoalHandle::SharedPtr, const std::shared_ptr<const RotateAbsolute::Feedback> fb){
      RCLCPP_INFO(this->get_logger(), "feedback remaining=%.3f", fb->remaining);
    };
    opts.result_callback = [this](const GoalHandle::WrappedResult & res){
      auto status = (int)res.code; // 1: succeeded etc
      double delta = res.result ? res.result->delta : 0;
      RCLCPP_INFO(this->get_logger(), "result code=%d delta=%.3f", status, delta);
      rclcpp::shutdown();
    };
    client_->async_send_goal(goal, opts);
    if (cancel_after_ > 0) {
      cancel_timer_ = this->create_wall_timer(std::chrono::duration<double>(cancel_after_), [this]{
        RCLCPP_WARN(this->get_logger(), "cancel_after triggered (demo: manual cancel via CLI: ros2 action send_goal ... --feedback)");
        cancel_timer_->cancel();
      });
    }
  }
  rclcpp_action::Client<RotateAbsolute>::SharedPtr client_;
  rclcpp::TimerBase::SharedPtr timer_, cancel_timer_;
  double theta_{1.57}, cancel_after_{0};
};

int main(int argc, char** argv){
  rclcpp::init(argc, argv);
  auto node = std::make_shared<RotateClientCpp>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
