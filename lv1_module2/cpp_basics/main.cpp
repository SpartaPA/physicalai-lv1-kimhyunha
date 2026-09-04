#include "Motor.hpp"
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    // 기본값 설정: ID는 1, RPM은 0.0
    int motor_id = 1;
    double initial_rpm = 0.0;

    // 터미널 인자가 들어왔다면 값 덮어쓰기
    // 예: ./motor_app 2 250.0 (ID: 2, RPM: 250.0)
    if (argc >= 2) {
        motor_id = std::stoi(argv[1]);
    }
    if (argc >= 3) {
        initial_rpm = std::stod(argv[2]);
    }

    Motor left_motor(motor_id);
    left_motor.setRpm(initial_rpm);
    left_motor.printStatus();

    return 0;
}