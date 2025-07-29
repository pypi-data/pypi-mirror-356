import unittest
import coopstructs.geometry as geo

class Test_Geometry(unittest.TestCase):

    def test__point_in_poly__inside(self):
        poly = [
            (2, 2),
            (3, 3),
            (2, 3),
            (3, 2)
        ]

        point = (1, 1)
        self.assertFalse(geo.point_in_polygon(point, poly), f"Point should not be in polygon")

    def test__point_in_poly__outside(self):
        poly = [
            (2, 2),
            (3, 3),
            (2, 3),
            (3, 2)
        ]

        point = (2.5, 2.5)
        self.assertTrue(geo.point_in_polygon(point, poly), f"Point should be in polygon")