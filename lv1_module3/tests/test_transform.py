"""문제 5 — 동차변환 inv_T 검증 (pytest). [학생 작성용 템플릿]

지시문이 요구하는 것은 `inv_T` 검증이지만,
점/방향 구분과 벡터화, 최소자승까지 함께 검증해 두면 이후 문제에서 안전하다.

실행: 프로젝트 루트에서  pytest -v
"""

import numpy as np
import pytest

from src.rotation import rot_x, rot_y, rot_z
from src.transform import (
    inv_T,
    least_squares_normal_equation,
    make_T,
    transform_direction,
    transform_point,
    transform_points,
)


@pytest.fixture
def T():
    """테스트에 쓸 대표 동차변환 하나."""
    R = rot_z(0.9) @ rot_y(-0.35) @ rot_x(1.3)
    return make_T(R, [0.35, -0.15, 0.55])


def test_inv_T_gives_identity(T):
    assert np.allclose(inv_T(T) @ T, np.eye(4)), "inv_T(T) @ T != I"
    assert np.allclose(T @ inv_T(T), np.eye(4)), "T @ inv_T(T) != I"


def test_inv_T_matches_generic_inverse(T):
    assert np.allclose(inv_T(T), np.linalg.inv(T))  # np.linalg.inv 는 검산용


def test_point_and_direction_differ(T):
    p = np.array([1.0, 2.0, 3.0])
    assert np.allclose(transform_point(T, p) - transform_direction(T, p), T[:3, 3]), \
        "점-방향 차이가 병진 벡터와 다름"
    v = np.array([1.0, 0.0, 0.0])
    assert np.isclose(np.dot(transform_direction(T, v), transform_direction(T, v)), 1.0), \
        "방향 변환이 길이를 보존하지 않음"


def test_transform_points_is_vectorized(T):
    rng = np.random.default_rng(42)
    P = rng.standard_normal((25, 3))
    assert np.allclose(transform_points(T, P),
                        np.array([transform_point(T, q) for q in P])), "벡터화 결과 불일치"


def test_roundtrip_through_inverse(T):
    rng = np.random.default_rng(42)
    P = rng.standard_normal((25, 3))
    assert np.allclose(transform_points(inv_T(T), transform_points(T, P)), P), "왕복 복원 실패"


def test_least_squares_matches_lstsq():
    rng = np.random.default_rng(42)
    A = rng.standard_normal((20, 3))
    b = A @ np.array([1.0, -2.0, 0.5]) + rng.standard_normal(20) * 0.01
    x, r = least_squares_normal_equation(A, b)
    xl, *_ = np.linalg.lstsq(A, b, rcond=None)  # 검산용
    assert np.allclose(x, xl), "lstsq 와 불일치"
    assert np.allclose(A.T @ r, 0.0, atol=1e-8), "잔차가 열공간에 수직하지 않음"
