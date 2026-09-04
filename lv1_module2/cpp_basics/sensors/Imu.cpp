#include "Imu.hpp"
#include <iostream>

Imu::Imu(const std::string& name) : Sensor(name) {}

Imu::~Imu() {
    std::cout << "[Destruct] Imu: " << name_ << "\n";
}

double Imu::read() {
    return 9.81; // IMU 측정값 예시
}