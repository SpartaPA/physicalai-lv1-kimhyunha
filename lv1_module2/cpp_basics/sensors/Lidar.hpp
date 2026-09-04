#ifndef LIDAR_HPP
#define LIDAR_HPP

#include "Sensor.hpp"

class Lidar : public Sensor {
public:
    Lidar(const std::string& name);
    ~Lidar() override;

    double read() override;
};

#endif