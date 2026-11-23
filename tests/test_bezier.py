"""
BÉZIER UNIT TESTS
Algorithm steps:
    1. Choose simple control points with results that can be calculated by hand.
    2. Test that linear interpolation returns both endpoints and the midpoint.
    3. Test that quadratic and cubic curves start and end at their endpoints.
    4. Run the tests to catch mathematical errors before font rendering.
"""

import unittest

from renderer.bezier import (
    linear_interpolation,
    quadratic_bezier,
    cubic_bezier,
)


class TestBezierFunctions(unittest.TestCase):
    def test_linear_interpolation(self):
        self.assertEqual(linear_interpolation((10, 20), (50, 60), 0), (10, 20))
        self.assertEqual(linear_interpolation((10, 20), (50, 60), 0.5), (30, 40))
        self.assertEqual(linear_interpolation((10, 20), (50, 60), 1), (50, 60))

    def test_quadratic_endpoints(self):
        p0, p1, p2 = (0, 0), (10, 20), (20, 0)
        self.assertEqual(quadratic_bezier(p0, p1, p2, 0), p0)
        self.assertEqual(quadratic_bezier(p0, p1, p2, 1), p2)

    def test_cubic_endpoints(self):
        p0, p1, p2, p3 = (0, 0), (10, 20), (20, 20), (30, 0)
        self.assertEqual(cubic_bezier(p0, p1, p2, p3, 0), p0)
        self.assertEqual(cubic_bezier(p0, p1, p2, p3, 1), p3)

    def test_invalid_parameter(self):
        with self.assertRaises(ValueError):
            linear_interpolation((0, 0), (1, 1), 1.5)


if __name__ == "__main__":
    unittest.main()
