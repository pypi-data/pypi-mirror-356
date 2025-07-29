import unittest
from coopstructs.geometry.circles.circle import Circle
from coopstructs.geometry.vectors.vectorN import Vector2
import coopstructs.geometry.vectors.vector_utils as vect

class Test_Geometry_Circle(unittest.TestCase):
    def test__circle__created_with_points(self):
        p1 = Vector2(1, 3)
        p2 = Vector2(6, 5)
        p3 = Vector2(2, 9)

        circ = Circle.from_boundary_points(p1, p2, p3)

        for point in circ.known_boundary_points:
            self.assertAlmostEqual(vect.distance_between(point, circ.Center), circ.radius, 5)