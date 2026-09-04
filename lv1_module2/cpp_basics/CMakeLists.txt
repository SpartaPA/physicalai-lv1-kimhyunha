cmake_minimum_required(VERSION 3.10)
project(cpp_basics)

# C++17 표준 설정
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 메모리 누수/오류 검출을 위한 AddressSanitizer 옵션 추가
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address -g")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=address")

# 1. 기존 모터 앱
add_executable(motor_app main.cpp Motor.cpp)

# 2. 기존 제동 거리 계산기
add_executable(stop_distance stop_distance.cpp)

# 3. 센서 테스트 앱 (sensors/ 폴더 안의 구현체 파일 경로 포함)
add_executable(sensor_test_app
        sensor_test_main.cpp
        sensors/Lidar.cpp
        sensors/Imu.cpp
)