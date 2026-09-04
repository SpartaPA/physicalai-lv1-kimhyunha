#ifndef SENSOR_HPP
#define SENSOR_HPP

#include <string>
#include <iostream>

class Sensor {
protected:
    std::string name_;

public:
    Sensor(const std::string& name) : name_(name) {
        std::cout << "[Construct] Sensor: " << name_ << "\n";
    }

    // ★ 가상 소멸자 (다형성 삭제 시 필수)
    virtual ~Sensor() {
        std::cout << "[Destruct] Sensor: " << name_ << "\n";
    }

    // 순수 가상 함수 (인터페이스)
    virtual double read() = 0;

    std::string getName() const {
        return name_;
    }
};

#endif