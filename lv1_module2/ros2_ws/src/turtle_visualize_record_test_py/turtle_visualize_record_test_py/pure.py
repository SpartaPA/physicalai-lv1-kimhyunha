import math
def distance_to_goal(x, y, gx, gy):
    if any(not isinstance(v, (int,float)) for v in (x,y,gx,gy)):
        raise TypeError("numeric required")
    return math.hypot(gx - x, gy - y)

def angle_to_goal(x, y, theta, gx, gy):
    if any(not isinstance(v, (int,float)) for v in (x,y,theta,gx,gy)):
        raise TypeError("numeric required")
    raw = math.atan2(gy - y, gx - x) - theta
    # -pi ~ pi 정규화
    while raw > math.pi: raw -= 2*math.pi
    while raw < -math.pi: raw += 2*math.pi
    return raw

def is_waypoint_reached(x, y, wx, wy, tol):
    if tol < 0:
        raise ValueError("tolerance must be >=0")
    return math.hypot(wx - x, wy - y) <= tol
