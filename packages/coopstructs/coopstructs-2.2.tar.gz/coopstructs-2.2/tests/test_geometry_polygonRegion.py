import unittest
from coopstructs.geometry.polygonRegion import PolygonRegion
from coopstructs.geometry.vectors.vectorN import Vector2
import random as rnd

class Test_Geometry_PolygonRegion(unittest.TestCase):

    def test__init_poly(self):
        # arrange
        n_points = 5
        points = [Vector2(rnd.randint(0, 10), rnd.randint(0, 10)) for x in range(n_points)]

        # act
        poly = PolygonRegion(boundary_points=points)

        # assert
        self.assertEqual(len(poly), n_points)

    def test__with_additional_points__convex__outside(self):
        # arrange
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  Vector2(10, 10),
                  Vector2(0, 10)]

        poly = PolygonRegion(boundary_points=points)
        new = Vector2(5, 15)

        # act
        poly2 = poly.with_additional_point(new, convex=True)

        # assert
        self.assertEqual(len(poly2), 5)

    def test__with_additional_points__convex__inside(self):
        # arrange
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  Vector2(10, 10),
                  Vector2(0, 10)]

        poly = PolygonRegion(boundary_points=points)
        new = Vector2(5, 5)

        # act
        poly2 = poly.with_additional_point(new, convex=True)

        # assert
        self.assertEqual(len(poly2), 4)

    def test__with_additional_points__not_convex__outside(self):
        # arrange
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  Vector2(10, 10),
                  Vector2(0, 10)]

        poly = PolygonRegion(boundary_points=points)
        new = Vector2(5, 15)

        # act
        poly2 = poly.with_additional_point(new, convex=False)

        # assert
        self.assertEqual(len(poly2), 5)

    def test__with_additional_points__not_convex__inside(self):
        # arrange
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  Vector2(10, 10),
                  Vector2(0, 10)]

        poly = PolygonRegion(boundary_points=points)
        new = Vector2(5, 5)

        # act
        poly2 = poly.with_additional_point(new, convex=False)

        # assert
        self.assertEqual(len(poly2), 5)

    def test__idxs_of_point(self):
        # arrange
        interesting = Vector2(10, 10)
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  interesting,
                  Vector2(0, 10),
                  interesting,
                  interesting]

        poly = PolygonRegion(boundary_points=points)

        # act
        idxs = poly.idxs_of_point([interesting])[interesting]

        # assert
        self.assertEqual(idxs, [2, 4, 5])

    def test__insersection_boundary_idxs_from_origin(self):
        # arrange
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  Vector2(10, 10),
                  Vector2(0, 10)]
        poly = PolygonRegion(points)
        new = Vector2(11, 4)

        # act
        bnds = poly.insersection_boundary_idxs_from_origin(new, Vector2(5, 5))

        #assert
        self.assertEqual(len(bnds), 1)
        self.assertEqual(bnds[0], (1, 2))

    def test__insersection_boundary_idxs_from_origin_none(self):
        # arrange
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  Vector2(10, 10),
                  Vector2(0, 10)]
        poly = PolygonRegion(points)
        new = Vector2(11, 4)

        # act
        bnds = poly.insersection_boundary_idxs_from_origin(new, Vector2(11, 1))

        #assert
        self.assertEqual(len(bnds), 0)

    def test__with_additional_points__between_bounds(self):
        # arrange
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  Vector2(10, 10),
                  Vector2(0, 10)]
        poly = PolygonRegion(points)
        new = Vector2(11, 4)
        bnds = poly.insersection_boundary_idxs_from_origin(new, Vector2(5, 5))

        # act
        poly2 = poly.with_additional_point(new, at_idx=bnds[0][1])

        # assert
        self.assertEqual(poly2.boundary_points[bnds[0][1]], new)

