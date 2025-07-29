import unittest
from coopstructs.geometry.curves.curves import Curve, Arc, LineCurve, CubicBezier, CatmullRom
from coopstructs.geometry.curves.curveBuilder import CurveBuilder
from coopstructs.geometry.curves.enums import CurveType
from coopstructs.geometry import Vector2
import random as rnd

class test_curves(unittest.TestCase):
    def test__cubicbezier__forcecontinuity(self):
        a = Vector2(1, 2)
        b = Vector2(1, 3)
        c = Vector2(1, 4)
        d = Vector2(1, 2)

        bezier = CubicBezier([a, b, c, d], 'a')

        not_continuous = Vector2(2, 1)
        continuous = bezier.force_continuity(not_continuous)

        self.assertEqual(continuous, Vector2(1, 1))

    def test__catmullrom__forcecontinuity(self):
        a = Vector2(1, 2)
        b = Vector2(1, 3)
        c = Vector2(1, 4)
        d = Vector2(1, 2)

        curve = CatmullRom([a, b, c, d], 'a')

        not_continuous = Vector2(2, 1)
        continuous = curve.force_continuity(not_continuous)

        self.assertEqual(continuous,not_continuous)

    def test__line__forcecontinuity(self):
        a = Vector2(1, 2)
        b = Vector2(1, 3)
        c = Vector2(1, 4)
        d = Vector2(1, 2)

        curve = LineCurve('a', a, b)

        not_continuous = Vector2(2, 1)
        continuous = curve.force_continuity(not_continuous)

        self.assertEqual(continuous,not_continuous)


    def test__catmullrom__makecurve(self):
        builder = CurveBuilder(lambda: "1")

        points = []

        rnd.seed(0)
        for ii in range(10):
            points.append(Vector2(rnd.randint(0, 100), rnd.randint(0, 100)))

        curves, leftover = builder.curves_from_points(curve_type=CurveType.CATMULLROM, points=points)

        self.assertEqual(len(curves), 1)
        self.assertEqual(len(leftover), 0)

    def test__catmullrom__computecatmullpoints(self):
        builder = CurveBuilder(lambda: "1")

        points = []

        rnd.seed(0)
        for ii in range(10):
            points.append(Vector2(rnd.randint(0, 100), rnd.randint(0, 100)))

        curves, leftover = builder.curves_from_points(curve_type=CurveType.CATMULLROM, points=points)

        curve = curves[0]
        catmullpoints = curve.point_representation()

        self.assertGreater(len(catmullpoints), 0)

    def test__curvebuilder__forcecontinuity__nocurves(self):
        builder = CurveBuilder(lambda: "1")

        not_continuous = Vector2(2, 1)
        continuous = builder.force_continuity(not_continuous)

        self.assertEqual(continuous,not_continuous)


    def test__curvebuilder__forcecontinuity__withcurves(self):
        builder = CurveBuilder(lambda: "1")

        a = Vector2(1, 2)
        b = Vector2(1, 3)
        c = Vector2(1, 4)
        d = Vector2(1, 2)

        builder.set_curve_type(CurveType.CUBICBEZIER)

        builder.add_point(a)
        builder.add_point(b)
        builder.add_point(c)
        builder.add_point(d)

        not_continuous = Vector2(2, 1)
        continuous = builder.force_continuity(not_continuous)

        self.assertEqual(continuous, Vector2(1, 1))

    def test__curvebuilder__forcecontinuity__BezierStartingNextCurve(self):
        builder = CurveBuilder(lambda: "1")

        a = Vector2(1, 2)
        b = Vector2(1, 3)
        c = Vector2(1, 4)
        d = Vector2(1, 2)

        builder.set_curve_type(CurveType.CUBICBEZIER)

        builder.add_point(a)
        builder.add_point(b)
        builder.add_point(c)
        builder.add_point(d)

        not_continuous = Vector2(2, 1)
        continuous = builder.force_continuity(not_continuous)

        self.assertEqual(continuous, Vector2(1, 1))


    def test__curvebuilder__forcecontinuity__BezierNotStartingNextCurve(self):
        builder = CurveBuilder(lambda: "1")

        a = Vector2(1, 2)
        b = Vector2(1, 3)
        c = Vector2(1, 4)
        d = Vector2(1, 2)
        e = Vector2(1, 1)

        builder.set_curve_type(CurveType.CUBICBEZIER)

        builder.add_point(a)
        builder.add_point(b)
        builder.add_point(c)
        builder.add_point(d)
        builder.add_point(e)

        not_continuous = Vector2(100.5, 100.5)
        continuous = builder.force_continuity(not_continuous)

        self.assertEqual(continuous, not_continuous)

    def test__curvebuilder__forcecontinuity__BezierNotFullCurve(self):
        builder = CurveBuilder(lambda: "1")

        a = Vector2(1, 2)
        b = Vector2(1, 3)

        builder.set_curve_type(CurveType.CUBICBEZIER)

        builder.add_point(a)
        builder.add_point(b)

        not_continuous = Vector2(100.5, 100.5)
        continuous = builder.force_continuity(not_continuous)

        self.assertEqual(continuous, not_continuous)


    def test__curvebuilder__forcecontinuity__BezierOnePoint(self):
        builder = CurveBuilder(lambda: "1")

        a = Vector2(1, 2)

        builder.set_curve_type(CurveType.CUBICBEZIER)

        builder.add_point(a)

        not_continuous = Vector2(100.5, 100.5)
        continuous = builder.force_continuity(not_continuous)

        self.assertEqual(continuous, not_continuous)

    def test__curvebuilder__Bezier__CurvesFromPoints(self):
        builder = CurveBuilder(lambda: "1")

        points = []

        rnd.seed(0)
        for ii in range(16):
            points.append(Vector2(rnd.randint(0, 100), rnd.randint(0, 100)))

        curves, _ = builder.curves_from_points(CurveType.CUBICBEZIER, points)
        self.assertEqual(len(curves), 5)

    def test__curvebuilder__Bezier__CurvesFromPointsWithExtra(self):
        builder = CurveBuilder(lambda: "1")

        points = []

        rnd.seed(0)
        for ii in range(18):
            points.append(Vector2(rnd.randint(0, 100), rnd.randint(0, 100)))

        curves, points = builder.curves_from_points(CurveType.CUBICBEZIER, points)
        self.assertEqual(len(curves), 5)
        self.assertEqual(len(points), 2)

    def test__line__point_at_t(self):
        a = Vector2(0, 0)
        b = Vector2(10, 10)

        lc = LineCurve(a, b)

        self.assertEqual(lc.point_at_t(0.5), Vector2(5, 5))

    def test__line__derivative_at_t(self):
        a = Vector2(0, 0)
        b = Vector2(10, 10)

        lc = LineCurve(a, b)

        self.assertEqual(lc.derivative_at_t(0.5), 1)
        self.assertEqual(lc.derivative_at_t(0.75), 1)
        self.assertEqual(lc.derivative_at_t(0.25), 1)

    def test__line__derivative_at_t__2(self):
        a = Vector2(2, 11)
        b = Vector2(-5, -10)

        lc = LineCurve(a, b)

        self.assertEqual(lc.derivative_at_t(0.5), 3)
        self.assertEqual(lc.derivative_at_t(0.75), 3)
        self.assertEqual(lc.derivative_at_t(0.25), 3)
