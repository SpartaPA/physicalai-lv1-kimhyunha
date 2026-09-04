cmake_minimum_required(VERSION 3.8)
project(turtle_custom_interface_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(turtle_interfaces REQUIRED)

add_executable(draw_polygon_server src/draw_polygon_server.cpp)
ament_target_dependencies(draw_polygon_server rclcpp rclcpp_action geometry_msgs turtle_interfaces)

add_executable(waypoint_publisher src/waypoint_publisher.cpp)
ament_target_dependencies(waypoint_publisher rclcpp std_msgs turtle_interfaces)

install(TARGETS draw_polygon_server waypoint_publisher DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
