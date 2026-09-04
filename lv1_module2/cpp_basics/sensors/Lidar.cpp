#include "Lidar.hpp"
#include <iostream>

Lidar::Lidar(const std::string& name) : Sensor(name) {}

Lidar::~Lidar() {
    std::cout << "[Destruct] Lidar: " << name_ << "\n";
}

double Lidar::read() {
    return 1.25; // Lidar 측정값 예시
}