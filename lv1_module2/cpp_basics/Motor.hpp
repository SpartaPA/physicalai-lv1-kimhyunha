#ifndef MOTOR_HPP
#define MOTOR_HPP

class Motor {
private:
    int id_;
    double rpm_;

public:
    Motor(int id);
    void setRpm(double rpm);
    double getRpm() const;
    void printStatus() const; // 선언만 남겨두기!
};

#endif