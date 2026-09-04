#ifndef IMU_HPP
#define IMU_HPP

#include "Sensor.hpp"

class Imu : public Sensor {
public:
    Imu(const std::string& name);
    ~Imu() override;

    double read() override;
};

#endif