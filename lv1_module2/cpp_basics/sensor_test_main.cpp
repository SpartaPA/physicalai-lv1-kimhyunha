#include "sensors/Sensor.hpp"
#include "sensors/Lidar.hpp"
#include "sensors/Imu.hpp"
#include <vector>
#include <memory>
#include <unordered_map>
#include <algorithm>
#include <iostream>

// 값을 범위 안으로 자르는 함수 템플릿 (double 속도·int 픽셀 양쪽에 적용)
template <typename T>
T clamp(T v, T lo, T hi) {
    if (v < lo) return lo;
    if (v > hi) return hi;
    return v;
}

// [Before specimen] 의도적인 메모리 누수: new 후 delete 누락 (루프)
// 보고서 문제2-5 before 로그용. 평소에는 호출하지 않고 simulateNoLeak()을 호출한다.
void simulateMemoryLeak(int n) {
    std::cout << "\n--- [Memory Leak Simulation Start] ---\n";
    for (int i = 0; i < n; ++i) {
        Sensor* leaked_sensor = new Lidar("Leaked_Lidar");
        std::cout << "Leaked sensor reading: " << leaked_sensor->read() << "\n";
        // delete leaked_sensor; 누락으로 인한 메모리 누수 발생
    }
    std::cout << "--- [Memory Leak Simulation End (Leaked!)] ---\n";
}

// [After] 누수 수정본: make_unique라 루프를 돌아도 자동 해제
void simulateNoLeak(int n) {
    std::cout << "\n--- [No-Leak Simulation Start] ---\n";
    for (int i = 0; i < n; ++i) {
        auto sensor = std::make_unique<Lidar>("Fixed_Lidar");
        std::cout << "Fixed sensor reading: " << sensor->read() << "\n";
    }
    std::cout << "--- [No-Leak Simulation End (Clean)] ---\n";
}

int main() {
    // -------------------------------------------------------------
    // 1. 스택 객체와 힙 객체의 소멸 시점 관찰
    // -------------------------------------------------------------
    std::cout << "=== 1. Stack vs Heap Object Destruction Test ===\n";
    {
        std::cout << "Entering inner block...\n";
        Lidar stack_lidar("Stack_Lidar");
        auto heap_lidar = std::make_unique<Lidar>("Heap_Lidar");
        std::cout << "Leaving inner block...\n";
    } // <-- 이 블록을 벗어나는 순간 스택 객체와 스마트 포인터가 가리키는 힙 객체가 자동 소멸함
    std::cout << "Exited inner block.\n\n";

    // -------------------------------------------------------------
    // 2. 다형성 루프 출력
    // -------------------------------------------------------------
    std::cout << "=== 2. Polymorphic Loop Test ===\n";
    std::vector<std::unique_ptr<Sensor>> sensors;
    sensors.push_back(std::make_unique<Lidar>("Front_Lidar"));
    sensors.push_back(std::make_unique<Imu>("Base_IMU"));
    sensors.push_back(std::make_unique<Lidar>("Rear_Lidar"));

    for (const auto& s : sensors) {
        std::cout << "Sensor [" << s->getName() << "] reading value: " << s->read() << "\n";
    }
    std::cout << "\n";

    // -------------------------------------------------------------
    // 3. unordered_map 과 vector 측정 로그 구성 및 count_if 활용
    // -------------------------------------------------------------
    std::cout << "=== 3. STL Map, Vector & count_if Test ===\n";

    // 센서 이름에서 최근 측정값을 찾는 unordered_map
    std::unordered_map<std::string, double> latest_readings;

    // 센서들의 측정 로그를 담는 vector
    std::vector<double> distance_logs;

    for (const auto& s : sensors) {
        double val = s->read();
        latest_readings[s->getName()] = val;
        distance_logs.push_back(val);
    }

    // map에 저장된 최근 측정값 확인 출력
    std::cout << "[Latest Readings Map]:\n";
    for (const auto& pair : latest_readings) {
        std::cout << "  - " << pair.first << ": " << pair.second << "\n";
    }

    // std::count_if 로 목표점까지 거리가 0.35 이내인 기록의 개수 세기
    // (센서 실측 외에 근거리 장애물 기록 0.2를 하나 추가해 카운트가 잡히는 것을 확인)
    distance_logs.push_back(0.2); // 근거리 기록 예시
    long count_within_035 = std::count_if(
        distance_logs.begin(),
        distance_logs.end(),
        [](double d) { return d <= 0.35; }
    );

    std::cout << "Number of distance records <= 0.35: " << count_within_035 << "\n\n";

    // -------------------------------------------------------------
    // 4. clamp 함수 템플릿을 double 속도·int 픽셀 양쪽에 적용
    // -------------------------------------------------------------
    std::cout << "=== 4. clamp Template Test ===\n";
    double speed = clamp(3.7, 0.0, 2.5); // double: 상한 초과 → 2.5
    int pixel = clamp(300, 0, 255);      // int: 상한 초과 → 255
    std::cout << "clamped speed (double): " << speed << "\n";
    std::cout << "clamped pixel (int): " << pixel << "\n\n";

    // -------------------------------------------------------------
    // 5. 메모리 누수 수정본 실행 (before 로그는 simulateMemoryLeak 호출로 재현)
    // -------------------------------------------------------------
    simulateNoLeak(3);

    return 0;
}