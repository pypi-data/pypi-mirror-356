from coopstructs.sectorTree import SectorTree
from coopstructs.geometry import Rectangle
import unittest

class Test_SectorTree(unittest.TestCase):
    def test_init_some_sectortrees(self):
        #arrange
        area_rect = Rectangle.from_tuple(rect=(0, 0, 250, 750))
        a_dims = (3, 4)
        b_dims = (4, 2)
        c_dims = (8, 12)

        #act
        a = SectorTree(area_rect=area_rect,
                       capacity=1,
                       shape=a_dims)
        b = SectorTree(area_rect=area_rect,
                       capacity=1,
                       shape=b_dims)
        c = SectorTree(area_rect=area_rect,
                       capacity=1,
                       shape=c_dims)

        #assert
        self.assertEqual(a_dims, a.grid.Shape)
        self.assertEqual(b_dims, b.grid.Shape)
        self.assertEqual(c_dims, c.grid.Shape)

    def test_fill_a_sectortree(self):
        #arrange
        area_rect = Rectangle.from_tuple(rect=(0, 0, 100, 200))
        dims = (2, 2)
        a = SectorTree(area_rect=area_rect,
                       capacity=1,
                       shape=dims)


        #act
        a.add_update_client("a", (49, 99))
        a.add_update_client("b", (49, 101))
        a.add_update_client("c", (51, 99))
        a.add_update_client("d", (51, 101))
        a.add_update_client("e", (52, 102))


        #assert
        self.assertEqual(len(a.ClientMappings[(0, 0)]), 1)
        self.assertEqual(len(a.ClientMappings[(1, 0)]), 1)
        self.assertEqual(len(a.ClientMappings[(0, 1)]), 1)
        self.assertEqual(len(a.ClientMappings[(1, 1)]), 2)
