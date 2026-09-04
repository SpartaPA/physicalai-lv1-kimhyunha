import math, pytest
from turtle_visualize_record_test_py.pure import distance_to_goal, angle_to_goal, is_waypoint_reached

def test_distance_normal():
    assert distance_to_goal(0,0,3,4) == pytest.approx(5.0)
def test_distance_zero():
    assert distance_to_goal(1,1,1,1) == 0
def test_distance_type_error():
    with pytest.raises(TypeError):
        distance_to_goal("a",0,0,0)

def test_angle_normal():
    assert angle_to_goal(0,0,0, 1,0) == pytest.approx(0)
    assert angle_to_goal(0,0,0, 0,1) == pytest.approx(math.pi/2)
def test_angle_normalize():
    # raw > pi -> wrap
    assert angle_to_goal(0,0, math.pi, -1,0) == pytest.approx(0, abs=1e-6)
def test_angle_boundary():
    assert -math.pi <= angle_to_goal(0,0,0, -1, -0.001) <= math.pi

def test_reached_inside():
    assert is_waypoint_reached(0,0, 0.05,0, 0.1) is True
def test_reached_boundary():
    assert is_waypoint_reached(0,0, 0.1,0, 0.1) is True
def test_reached_outside():
    assert is_waypoint_reached(0,0, 0.2,0, 0.1) is False
def test_reached_negative_tol():
    with pytest.raises(ValueError):
        is_waypoint_reached(0,0,0,0, -1)

# # 실패  처리
# def test_distance_broken():
#     assert distance_to_goal(0,0,3,4) == pytest.approx(10.0)