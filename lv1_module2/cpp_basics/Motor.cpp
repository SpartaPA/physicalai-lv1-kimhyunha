#include "Motor.hpp"
#include <iostream> // cout을 쓰려면 여기에 꼭 있어야 함!

Motor::Motor(int id) : id_(id), rpm_(0.0) {}

void Motor::setRpm(double rpm) {
    rpm_ = rpm;
}

double Motor::getRpm() const {
    return rpm_;
}

void Motor::printStatus() const {
    std::cout << "Motor ID: " << id_ << ", Current RPM: " << rpm_ << "\n";
}