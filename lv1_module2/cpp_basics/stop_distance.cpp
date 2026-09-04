#include <iostream>
#include <cmath>

int main(int argc, char** argv) {
    // 기본값: 속도(v) = 10.0 m/s, 마찰계수(mu) = 0.7
    double v = 10.0;
    double mu = 0.7;
    const double g = 9.81;

    if (argc >= 2) v = std::stod(argv[1]);
    if (argc >= 3) mu = std::stod(argv[2]);

    // 제동 거리 공식: d = v^2 / (2 * mu * g)
    double distance = (v * v) / (2.0 * mu * g);

    std::cout << "[Stop Distance Calculator]\n";
    std::cout << "Speed: " << v << " m/s, Friction: " << mu << "\n";
    std::cout << "Stopping Distance: " << distance << " meters\n";

    return 0;
}