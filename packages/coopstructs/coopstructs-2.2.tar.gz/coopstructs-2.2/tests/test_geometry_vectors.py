import unittest
from coopstructs.geometry.vectors.vectorN import Vector2, VectorN
import math

class test_vectors(unittest.TestCase):

    def test_bounded_by(self):
        a = Vector2(1, 2)
        b = Vector2(1, 3)
        c = Vector2(1, 4)

        assert b.bounded_by(a, c) is True, f"{b} should be bounded by {a, c}"
        assert a.bounded_by(b, c) is False, f"{a} should not be bounded by {b, c}"
        assert c.bounded_by(a, c) is True, f"{c} should be bounded by {a, c}"

    def test_multiply_by_scalar(self):
        a = Vector2(1, 2)

        assert (a * 4).length() == a.length() * 4

    def test_divide_by_scalar(self):
        a = Vector2(4, 2)

        assert (a / 4).length() == a.length() / 4

    def test_equality(self):
        a = Vector2(1, 2)
        b = Vector2(1, 3)
        c = Vector2(1, 4)
        d = Vector2(1, 2)
        e = Vector2(1.0, 2.0)

        f = VectorN()
        f.coords['x'] = 1
        f.coords['y'] = 2

        assert (a == b) is False, f"{a} should not equal {b}"
        assert (a == d) is True, f"{a} should equal {d}"
        assert (a == e) is True, f"{a} should equal {e}"

        assert (f == a) is True, f"IVector and Vector2 should be equal for {f} and {a}"

    def test_distance_from(self):
        a = Vector2(1, 2)
        b = Vector2(1, 3)

        assert (a.distance_from(b)) == 1, f"distance from {a} to {b} should be 1"

    def test_hadamard_division(self):
        a = Vector2(1, 2)
        c = Vector2(2, 4)

        assert (c.hadamard_division(a)) == Vector2(2, 2), f"hadamard division of {c} and {a} should be {Vector2(2, 2)}"
        assert (c.hadamard_division(2)) == Vector2(1, 2), f"hadamard division of {c} and {2} should be {Vector2(1, 2)}"

    def test_hadamard_multiplication(self):
        a = Vector2(1, 2)
        c = Vector2(1, 4)

        assert (c.hadamard_product(a)) == Vector2(1, 8), f"hadamard product of {c} and {a} should be {Vector2(1, 8)}"
        assert (c.hadamard_product(3)) == Vector2(3, 12)

    def test_is_close(self):
        f = VectorN()
        f.coords['x'] = 1
        f.coords['y'] = 2

        g = 1.0
        h = 1.0
        assert f._is_close(g, h) is True, f"{g} and {h} should be close"

    def test_subclassing(self):
        a = Vector2(1, 2)
        assert issubclass(type(a), VectorN) is True, f"{type(a)} should be subclass of {type(VectorN)}"

    def test_interpolate_linear(self):
        a = Vector2(1, 1)
        b = Vector2(2, 2)
        d = Vector2(11, 11)

        c = a.interpolate(b)
        e = a.interpolate(d, .9)

        assert c == Vector2(1.5, 1.5)
        assert e == Vector2(10, 10)

    def test_interpolate_Vector2_and_NVector(self):
        a = Vector2(1, 1)
        b = VectorN({"x": 2, "y": 2})

        c = a.interpolate(b)
        d = b.interpolate(a)

        e = a * 2
        f = Vector2(12, 12)
        g = e.interpolate(f, .9)

        assert c == Vector2(1.5, 1.5)
        assert d == Vector2(1.5, 1.5)
        assert g == Vector2(11, 11)

    def test_angle_between__no_input(self):
        a = Vector2(-5, 0)

        self.assertTrue(math.isclose(a.degrees_from(), 180), msg=f"{a.degrees_from()} is not equal to {math.pi}")

    def test_angle_between__two_vectors(self):
        a = Vector2(-5, 0)
        b = Vector2(0, 1)
        self.assertEqual(a.degrees_from(b), 90)

    def test_angle_between__two_vectors__min_chunk(self):
        a = Vector2(-5, 0)
        b = Vector2(0, 1)
        self.assertEqual(a.degrees_from(b, minimum_chunk=True), 90)

    def test_angle_between__two_vectors_greater_than_180(self):
        b = Vector2(-5, 0)
        a = Vector2(0, 1)
        self.assertEqual(a.degrees_from(b), 270)

    def test_angle_between__two_vectors_greater_than_180__min_chunk(self):
        b = Vector2(-5, 0)
        a = Vector2(0, 1)
        self.assertEqual(a.degrees_from(b, minimum_chunk=True), 90)

    def test__vector2__projectonto__withinyrange(self):
        end = Vector2(1, 10)
        start = Vector2(1, 20)

        p = Vector2(5, 15)

        projection = p.project_onto(end, start)

        self.assertEqual(projection, Vector2(1, 15))

    def test__vector2__projectonto__outsideyrange(self):
        c = Vector2(1, 4)
        d = Vector2(1, 2)

        p = Vector2(2, 1)

        self.assertEqual(p.project_onto(c, d), Vector2(1, 1))

    def test__iVector__closest_point_within_threshold__one_qualify(self):
        a = Vector2(1, 100)
        b = Vector2(50, 1)
        c = Vector2(1, 10)
        d = Vector2(1, 2)

        p = Vector2(2, 1)
        threshold = 10
        self.assertEqual(p.closest_within_threshold([a, b, c, d], distance_threshold=threshold), d)

    def test__iVector__closest_point_within_threshold__multiple_qualify(self):
        a = Vector2(1, 100)
        b = Vector2(50, 1)
        c = Vector2(1, 10)
        d = Vector2(1, 2)

        p = Vector2(2, 1)
        threshold = 20
        self.assertEqual(p.closest_within_threshold([a, b, c, d], distance_threshold=threshold), d)

    def test__iVector__closest_point_within_threshold__none_qualify(self):
        a = Vector2(1, 100)
        b = Vector2(50, 1)
        c = Vector2(1, 10)
        d = Vector2(1, 2)

        p = Vector2(2, 1)
        threshold = 1
        self.assertEqual(p.closest_within_threshold([a, b, c, d], distance_threshold=threshold), None)

    def test__iVector__closest_point_within_threshold__none_threshold(self):
        a = Vector2(1, 100)
        b = Vector2(50, 1)
        c = Vector2(1, 10)
        d = Vector2(1, 2)

        p = Vector2(2, 1)
        threshold = None
        self.assertEqual(p.closest_within_threshold([a, b, c, d], distance_threshold=threshold), d)

    def test__iVector__closest_point_within_threshold__neg_threshold(self):
        a = Vector2(1, 100)
        b = Vector2(50, 1)
        c = Vector2(1, 10)
        d = Vector2(1, 2)

        p = Vector2(2, 1)
        threshold = -1

        with self.assertRaises(ValueError):
            p.closest_within_threshold([a, b, c, d], distance_threshold=threshold)

    def test__point_in_poly__inside(self):
        poly = [
            Vector2(2, 2),
            Vector2(3, 3),
            Vector2(2, 3),
            Vector2(3, 2)
        ]

        point = Vector2(1, 1)
        self.assertFalse(point.in_polygon(poly), f"Point should not be in polygon")

    def test__point_in_poly__outside(self):
        poly = [
            Vector2(2, 2),
            Vector2(3, 3),
            Vector2(2, 3),
            Vector2(3, 2)
        ]

        point = Vector2(2.5, 2.5)
        self.assertTrue(point.in_polygon(poly), f"Point should be in polygon")