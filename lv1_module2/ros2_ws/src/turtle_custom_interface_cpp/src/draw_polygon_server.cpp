#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <turtle_interfaces/action/draw_polygon.hpp>
#include <cmath>
#include <thread>

class DrawPolygonServer : public rclcpp::Node {
public:
  using DrawPolygon = turtle_interfaces::action::DrawPolygon;
  using GoalHandle = rclcpp_action::ServerGoalHandle<DrawPolygon>;
  DrawPolygonServer() : Node("draw_polygon_server") {
    pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
    server_ = rclcpp_action::create_server<DrawPolygon>(
      this, "draw_polygon",
      [](const rclcpp_action::GoalUUID&, std::shared_ptr<const DrawPolygon::Goal> g){
        if (g->sides < 3) return rclcpp_action::GoalResponse::REJECT;
        if (g->side_length <= 0) return rclcpp_action::GoalResponse::REJECT;
        return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
      },
      [](std::shared_ptr<GoalHandle>){ return rclcpp_action::CancelResponse::ACCEPT; },
      [this](std::shared_ptr<GoalHandle> gh){ std::thread([this, gh]{ execute(gh); }).detach(); });
    RCLCPP_INFO(this->get_logger(), "DrawPolygon cpp server ready on draw_polygon");
  }
private:
  void execute(std::shared_ptr<GoalHandle> gh){
    auto goal = gh->get_goal();
    int sides = goal->sides;
    double len = goal->side_length;
    double angle = 2*M_PI / sides;
    double total = 0;
    RCLCPP_INFO(this->get_logger(), "execute sides=%d len=%.2f angle=%.1fdeg", sides, len, angle*180/M_PI);
    for (int i=0;i<sides;i++){
      if (gh->is_canceling()){
        pub_->publish(geometry_msgs::msg::Twist());
        auto res = std::make_shared<DrawPolygon::Result>(); res->total_distance = total;
        gh->canceled(res);
        RCLCPP_WARN(this->get_logger(), "canceled at %d/%d", i, sides);
        return;
      }
      // straight
      double dur = len / 1.0;
      auto t0 = this->now();
      while ((this->now()-t0).seconds() < dur){
        if (gh->is_canceling()) break;
        geometry_msgs::msg::Twist m; m.linear.x = 1.0; pub_->publish(m);
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
      }
      pub_->publish(geometry_msgs::msg::Twist());
      total += len;
      // rotate
      double rdur = angle / 1.0;
      t0 = this->now();
      while ((this->now()-t0).seconds() < rdur){
        if (gh->is_canceling()) break;
        geometry_msgs::msg::Twist m; m.angular.z = 1.0; pub_->publish(m);
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
      }
      pub_->publish(geometry_msgs::msg::Twist());
      auto fb = std::make_shared<DrawPolygon::Feedback>();
      fb->completed_sides = i+1; fb->progress = float((i+1)/(double)sides);
      gh->publish_feedback(fb);
      RCLCPP_INFO(this->get_logger(), "feedback %d/%d progress=%.2f", i+1, sides, fb->progress);
      if (gh->is_canceling()){
        pub_->publish(geometry_msgs::msg::Twist());
        auto res = std::make_shared<DrawPolygon::Result>(); res->total_distance = total;
        gh->canceled(res);
        return;
      }
    }
    pub_->publish(geometry_msgs::msg::Twist());
    auto res = std::make_shared<DrawPolygon::Result>(); res->total_distance = total;
    gh->succeed(res);
    RCLCPP_INFO(this->get_logger(), "succeeded total=%.2f", total);
  }
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr pub_;
  rclcpp_action::Server<DrawPolygon>::SharedPtr server_;
};

int main(int argc, char** argv){
  rclcpp::init(argc, argv);
  auto n = std::make_shared<DrawPolygonServer>();
  rclcpp::spin(n);
  rclcpp::shutdown();
  return 0;
}
