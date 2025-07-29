import unittest
from coopstructs.geometry.lines.line import Line
from coopstructs.geometry.vectors.vectorN import Vector2
import coopstructs.geometry as geom

class Test_Line(unittest.TestCase):
    def test__lineobj_intersection(self):
        # arrange
        line1 = Line(Vector2(0.0, 0.0), Vector2(10.0, 0.0))
        line2 = Line(Vector2(5.0, -5.0), Vector2(5.0, 5.0))

        # act
        inter = line1.intersection(line2)

        # assert
        self.assertEqual(inter, (5, 0))

    def test__line_intersection(self):
        # arrange
        a0 = (0.0, 0.0)
        a1 = (10.0, 0.0)
        b0 = (5.0, -5.0)
        b1 = (5.0, 5.0)

        l1 = (a0, a1)
        l2 = (b0, b1)

        # act
        inter = geom.line_intersection_2d(l1, l2)

        # assert
        self.assertEqual(inter, (5, 0))

    def test__lineobj_intersection__at_end(self):
        # arrange
        line1 = Line(Vector2(0.0, 0.0), Vector2(10.0, 0.0))
        line2 = Line(Vector2(10.0, -5.0), Vector2(10.0, 5.0))

        # act
        inter = line1.intersection(line2)

        # assert
        self.assertEqual(inter, (10, 0))

    def test__line_intersection__at_end(self):
        # arrange
        a0 = (0.0, 0.0)
        a1 = (10.0, 0.0)
        b0 = (10.0, -5.0)
        b1 = (10.0, 5.0)

        l1 = (a0, a1)
        l2 = (b0, b1)

        # act
        inter = geom.line_intersection_2d(l1, l2)

        # assert
        self.assertEqual(inter, (10, 0))

    def test__lineobj_intersection__not_on_segment_no_extend(self):
        # arrange
        line1 = Line(Vector2(0.0, 0.0), Vector2(10.0, 0.0))
        line2 = Line(Vector2(11.0, -5.0), Vector2(11.0, 5.0))

        # act
        inter = line1.intersection(line2)

        # assert
        self.assertEqual(inter, None)

    def test__line_intersection__not_on_segment_no_extend(self):
        # arrange
        a0 = (0.0, 0.0)
        a1 = (10.0, 0.0)
        b0 = (11.0, -5.0)
        b1 = (11.0, 5.0)

        l1 = (a0, a1)
        l2 = (b0, b1)

        # act
        inter = geom.line_intersection_2d(l1, l2)

        # assert
        self.assertEqual(inter, None)

    def test__lineobj_intersection__not_on_segment_extend(self):
        # arrange
        line1 = Line(Vector2(0.0, 0.0), Vector2(10.0, 0.0))
        line2 = Line(Vector2(11.0, -5.0), Vector2(11.0, 5.0))

        # act
        inter = line1.intersection(line2, extend=True)

        # assert
        self.assertEqual(inter, (11, 0))


    def test__line_intersection__not_on_segment_extend(self):
        # arrange
        a0 = (0.0, 0.0)
        a1 = (10.0, 0.0)
        b0 = (11.0, -5.0)
        b1 = (11.0, 5.0)

        l1 = (a0, a1)
        l2 = (b0, b1)

        # act
        inter = geom.line_intersection_2d(l1, l2, extend=True)

        # assert
        self.assertEqual(inter, (11, 0))


    def test__collinear_points__all_on_line(self):
        a = (0, 1)
        b = (0, 2)
        c = (0, 3)
        d = (0, 4)
        e = (0, 5)
        f = (0, 6)
        self.assertTrue(geom.collinear_points([a, b, c, d, e, f]), f"All points should be on line")

    def test__collinear_points__not_all_on_line(self):
        a = (0, 1)
        b = (0, 2)
        c = (0, 3)
        d = (0, 4)
        e = (0, 5)
        f = (1, 6)
        self.assertFalse(geom.collinear_points([a, b, c, d, e, f]), f"All points should not be on line")

    def test__collinear_points__some_points_equivelant(self):
        a = (0, 1)
        b = (0, 1)
        c = (0, 3)
        self.assertTrue(geom.collinear_points([a, b, c]), f"All points should be on line")

    def test__collinear_points__float_equivelance(self):
        a = (0, 1.000000001)
        b = (0, 1.000000002)
        c = (0, 3)
        self.assertTrue(geom.collinear_points([a, b, c]), f"All points should be on line")

    def test__collinear_points__all_points_same(self):
        a = (0, 1)
        b = (0, 1)
        c = (0, 1)
        self.assertTrue(geom.collinear_points([a, b, c]), f"All points should be on line")





