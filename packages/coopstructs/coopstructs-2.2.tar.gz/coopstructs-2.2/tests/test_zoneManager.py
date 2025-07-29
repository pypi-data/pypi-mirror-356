import unittest
from coopstructs.zones.zoneManager import ZoneManager
from coopstructs.geometry import Vector2
import random as rnd
from coopstructs.geometry import PolygonRegion
from coopstructs.zones.exceptions import ZoneDoesntExistException, ZoneAlreadyExistsException

class Test_ZoneManager(unittest.TestCase):

    def test__init_zm(self):
        # arrange
        zm = ZoneManager()

        # act

        # assert
        self.assertEqual(len(zm), 0)

    def test__init_zone(self):
        # arrange
        zm = ZoneManager()
        zone_name = 'test'
        n_points = 5
        points = [Vector2(rnd.randint(0, 10), rnd.randint(0, 10)) for x in range(n_points)]

        # act
        zm.init_new_zone(zone_name,
                         initial_points=points)

        # assert
        self.assertEqual(len(zm), 1)
        self.assertEqual(issubclass(type(zm[zone_name]), PolygonRegion), True)
        self.assertEqual(len(zm[zone_name].boundary_points), n_points)

    def test__init_zone__dup(self):
        # arrange
        zm = ZoneManager()
        zone_name = 'test'
        n_points = 5
        points = [Vector2(rnd.randint(0, 10), rnd.randint(0, 10)) for x in range(n_points)]
        zm.init_new_zone(zone_name, initial_points=points)

        # act
        action = lambda : zm.init_new_zone(zone_name, initial_points=points)

        # assert
        self.assertRaises(ZoneAlreadyExistsException, action)

    def test__add_to_zone(self):
        # arrange
        zm = ZoneManager()
        zone_name = 'test'
        n_points = 5
        points = [Vector2(rnd.randint(0, 10), rnd.randint(0, 10)) for x in range(n_points)]
        zm.init_new_zone(zone_name,
                         initial_points=points)

        # act
        zm.add_to_zone(zone_name, Vector2(5, 5))

        # assert
        self.assertEqual(len(zm), 1)
        self.assertEqual(issubclass(type(zm[zone_name]), PolygonRegion), True)
        self.assertEqual(len(zm[zone_name].boundary_points), n_points + 1)

    def test__add_to_zone__at_idx(self):
        # arrange
        zm = ZoneManager()
        zone_name = 'test'
        n_points = 5
        rnd.seed(0)
        points = [Vector2(rnd.randint(0, 10), rnd.randint(0, 10)) for x in range(n_points)]
        zm.init_new_zone(zone_name,
                         initial_points=points)
        idx = 3
        new = Vector2(5, 5)

        # act
        zm.add_to_zone(zone_name, new, idx)

        # assert
        self.assertEqual(len(zm), 1)
        self.assertEqual(issubclass(type(zm[zone_name]), PolygonRegion), True)
        self.assertEqual(len(zm[zone_name].boundary_points), n_points + 1)
        self.assertEqual(zm[zone_name].boundary_points[idx], new)

    def test__add_to_zone__zone_not_exists(self):
        # arrange
        zm = ZoneManager()
        zone_name = 'test'
        n_points = 5
        points = [Vector2(rnd.randint(0, 10), rnd.randint(0, 10)) for x in range(n_points)]
        zm.init_new_zone(zone_name,
                         initial_points=points)

        # act
        action = lambda: zm.add_to_zone("bad", Vector2(5, 5))

        # assert
        self.assertRaises(ZoneDoesntExistException, action)

    def test__remove_from_zone(self):
        # arrange
        zm = ZoneManager()
        zone_name = 'test'
        n_points = 5
        points = [Vector2(rnd.randint(0, 10), rnd.randint(0, 10)) for x in range(n_points)]
        zm.init_new_zone(zone_name,
                         initial_points=points)

        # act
        zm.remove_last_point_from_zone(zone_name)

        # assert
        self.assertEqual(len(zm), 1)
        self.assertEqual(issubclass(type(zm[zone_name]), PolygonRegion), True)
        self.assertEqual(len(zm[zone_name].boundary_points), n_points - 1)

    def test__remove_from_zone__zone_doesnt_exist(self):
        # arrange
        zm = ZoneManager()
        zone_name = 'test'
        n_points = 5
        points = [Vector2(rnd.randint(0, 10), rnd.randint(0, 10)) for x in range(n_points)]
        zm.init_new_zone(zone_name,
                         initial_points=points)

        # act
        action = lambda: zm.remove_last_point_from_zone('bad')

        # assert
        self.assertRaises(ZoneDoesntExistException, action)

    def test__remove_zone(self):
        # arrange
        zm = ZoneManager()
        zone_name = 'test'
        n_points = 5
        points = [Vector2(rnd.randint(0, 10), rnd.randint(0, 10)) for x in range(n_points)]
        zm.init_new_zone(zone_name,
                         initial_points=points)

        # act
        zm.delete_zone(zone_name)

        # assert
        self.assertEqual(len(zm), 0)

    def test__remove_zone__zone_doesnt_exist(self):
        # arrange
        zm = ZoneManager()
        zone_name = 'test'
        n_points = 5
        points = [Vector2(rnd.randint(0, 10), rnd.randint(0, 10)) for x in range(n_points)]
        zm.init_new_zone(zone_name,
                         initial_points=points)

        # act
        action = lambda: zm.delete_zone('bad')

        # assert
        self.assertRaises(ZoneDoesntExistException, action)

    def test__member_zones__point_in_one_zone(self):
        # arrange
        zm = ZoneManager()
        z1_name = 'z1'
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  Vector2(10, 10),
                  Vector2(0, 10)]
        zm.init_new_zone(z1_name,
                         initial_points=points)

        z2_name = 'z2'
        points = [Vector2(100, 100),
                  Vector2(110, 100),
                  Vector2(110, 110),
                  Vector2(100, 110)]
        zm.init_new_zone(z2_name,
                         initial_points=points)
        test_point = Vector2(5, 5)

        # act
        member_zones = zm.member_zones([test_point])

        # assert
        self.assertEqual(len(member_zones), 1)
        self.assertEqual(len(member_zones[test_point]), 1)
        self.assertEqual(member_zones[test_point][0], z1_name)

    def test__member_zones__point_in_no_zone(self):
        # arrange
        zm = ZoneManager()
        z1_name = 'z1'
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  Vector2(10, 10),
                  Vector2(0, 10)]
        zm.init_new_zone(z1_name,
                         initial_points=points)

        z2_name = 'z2'
        points = [Vector2(100, 100),
                  Vector2(110, 100),
                  Vector2(110, 110),
                  Vector2(100, 110)]
        zm.init_new_zone(z2_name,
                         initial_points=points)
        test_point = Vector2(50, 50)

        # act
        member_zones = zm.member_zones([test_point])

        # assert
        self.assertEqual(len(member_zones), 1)
        self.assertEqual(len(member_zones[test_point]), 0)

    def test__member_zones__point_in_mult_zones(self):
        # arrange
        zm = ZoneManager()
        z1_name = 'z1'
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  Vector2(10, 10),
                  Vector2(0, 10)]
        zm.init_new_zone(z1_name,
                         initial_points=points)

        z2_name = 'z2'
        points = [Vector2(5, 5),
                  Vector2(20, 5),
                  Vector2(20, 20),
                  Vector2(5, 20)]
        zm.init_new_zone(z2_name,
                         initial_points=points)
        test_point = Vector2(7, 7)

        # act
        member_zones = zm.member_zones([test_point])

        # assert
        self.assertEqual(len(member_zones), 1)
        self.assertEqual(len(member_zones[test_point]), 2)

    def test__member_zones__mult_points_in_zones(self):
        # arrange
        zm = ZoneManager()
        z1_name = 'z1'
        points = [Vector2(0, 0),
                  Vector2(10, 0),
                  Vector2(10, 10),
                  Vector2(0, 10)]
        zm.init_new_zone(z1_name,
                         initial_points=points)

        z2_name = 'z2'
        points = [Vector2(5, 5),
                  Vector2(20, 5),
                  Vector2(20, 20),
                  Vector2(5, 20)]
        zm.init_new_zone(z2_name,
                         initial_points=points)
        test_point0 = Vector2(7, 7)
        test_point1 = Vector2(1, 1)
        test_point2 = Vector2(15, 15)
        test_point3 = Vector2(20, 20)

        # act
        member_zones = zm.member_zones([test_point0, test_point1, test_point2, test_point3])

        # assert
        self.assertEqual(len(member_zones), 4)
        self.assertEqual(len(member_zones[test_point0]), 2)
        self.assertEqual(len(member_zones[test_point1]), 1)
        self.assertEqual(len(member_zones[test_point2]), 1)
        self.assertEqual(len(member_zones[test_point3]), 1)