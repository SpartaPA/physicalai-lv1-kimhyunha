# physicalai-lv1-kimhyunha

Physical AI Lv.1 과제 저장소 (모듈 1~4). 과제 지시문은 [reference](reference)에 있다.

## 구성

- [lv1_module1](lv1_module1) — 배달 로봇 온보딩 (연산 분담·SSH/udev·Git 협업)
  - [report.md](lv1_module1/report.md) — 문제 1~3 설계·명령어·출력
  - `rules/99-robot-sensor.rules` — 센서 고정 이름 udev 규칙
  - `images/` — 실행 캡처
- [lv1_module2](lv1_module2) — turtlesim ROS2 패키지 (rclpy·rclcpp·Service/Action·launch·bag·pytest)
  - [report.md](lv1_module2/report.md) — 문제별 실행 명령·출력
  - `cpp_basics/` — 문제 1·2 (g++, CMake, 센서 클래스)
  - `ros2_ws/src/` — `turtle_py`, `turtle_cpp` 등 패키지 전체 (ROS 2 Humble)
  - `screenshots/`, `bags/` — 캡처·rosbag 기록
- [lv1_module3](lv1_module3) — 로봇 좌표 변환 수학 라이브러리 (NumPy)
  - [src](lv1_module3/src) — `vectors.py`, `rotation.py`, `transform.py`, `coordinate_chain.py`
  - [tests](lv1_module3/tests) — pytest 82개
  - [notebooks](lv1_module3/notebooks) — 문제별 노트북 6개 (실행 결과 포함)
- [lv1_module4](lv1_module4) — 픽앤플레이스 자세 추정 + 궤적 시연
  - `notebooks/` — `01_pipeline.ipynb`, `02_interpolation.ipynb`, `03_pose_estimation.ipynb`
  - `src/` — `pose_pipeline.py` + 모듈 ③ 라이브러리
  - `tests/`, `requirements.txt`, `demo.gif`, `presentation.md`

## 제출 태그

- `과제1-1,2,3-제출` — 모듈 1~3 제출 커밋
- `과제1-4-제출` — 모듈 4 포함 전체 제출 커밋
