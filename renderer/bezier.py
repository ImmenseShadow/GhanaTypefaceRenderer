"""
BÉZIER MATHEMATICS
Purpose:
    Calculate points on linear, quadratic, and cubic Bézier curves.

Algorithm steps:
    1. Receive the curve's control points and a parameter t.
    2. Check that t lies between 0 and 1.
    3. Evaluate the appropriate Bézier equation independently for x and y.
    4. Return the calculated point as an (x, y) tuple.

The linear interpolation function is the basic operation behind the
quadratic and cubic Bézier equations.
"""


def _check_t(t):
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be between 0 and 1 inclusive")


def linear_interpolation(p0, p1, t):
    """Return the point a fraction t of the way from p0 to p1."""
    _check_t(t)
    x = (1 - t) * p0[0] + t * p1[0]
    y = (1 - t) * p0[1] + t * p1[1]
    return x, y


def quadratic_bezier(p0, p1, p2, t):
    """
    Evaluate a quadratic Bézier curve.
    p0 and p2 are endpoints; p1 is the control point.
    """
    _check_t(t)
    one_minus_t = 1 - t

    x = (one_minus_t ** 2 * p0[0]
         + 2 * one_minus_t * t * p1[0]
         + t ** 2 * p2[0])
    y = (one_minus_t ** 2 * p0[1]
         + 2 * one_minus_t * t * p1[1]
         + t ** 2 * p2[1])

    return x, y


def cubic_bezier(p0, p1, p2, p3, t):
    """
    Evaluate a cubic Bézier curve.
    p0 and p3 are endpoints; p1 and p2 are control points.
    """
    _check_t(t)
    one_minus_t = 1 - t

    x = (one_minus_t ** 3 * p0[0]
         + 3 * one_minus_t ** 2 * t * p1[0]
         + 3 * one_minus_t * t ** 2 * p2[0]
         + t ** 3 * p3[0])
    y = (one_minus_t ** 3 * p0[1]
         + 3 * one_minus_t ** 2 * t * p1[1]
         + 3 * one_minus_t * t ** 2 * p2[1]
         + t ** 3 * p3[1])

    return x, y
