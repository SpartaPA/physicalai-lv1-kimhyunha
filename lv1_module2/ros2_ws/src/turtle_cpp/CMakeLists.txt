cmake_minimum_required(VERSION 3.8)
project(turtle_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(turtlesim REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(rclcpp_action REQUIRED)

add_executable(turtle_distance_cpp src/turtle_distance.cpp)
ament_target_dependencies(turtle_distance_cpp rclcpp std_msgs turtlesim)

add_executable(turtle_alarm_cpp src/turtle_alarm.cpp)
ament_target_dependencies(turtle_alarm_cpp rclcpp std_msgs)

add_executable(rotate_client_cpp src/rotate_client.cpp)
ament_target_dependencies(rotate_client_cpp rclcpp rclcpp_action turtlesim)

add_executable(turtle_square_cpp src/turtle_square.cpp)
ament_target_dependencies(turtle_square_cpp rclcpp geometry_msgs turtlesim std_srvs)

install(TARGETS
  turtle_distance_cpp
  turtle_alarm_cpp
  rotate_client_cpp
  turtle_square_cpp
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
