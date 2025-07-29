from typing import Tuple
from cooptools.coopEnum import CardinalPosition
import cooptools.geometry_utils.rect_utils as rect
import cooptools.geometry_utils.vector_utils as vec
from cooptools.anchor import Anchor2D
from cooptools.transform import Rotation

class PlanarRectangle:

    def __init__(self,
                 pt: vec.FloatVec2D, #x, y
                 dims: vec.FloatVec2D, #w, h
                 anchor_cardinality: CardinalPosition = None):
        self.anchor = Anchor2D(
            pt=pt,
            dims=dims,
            cardinality=anchor_cardinality
        )

    def with_margin(self, margin: int | vec.IterVec):
        '''
        margin is either uniform or in the form l, t, r, b
        '''
        if type(margin) == int:
            margin = [margin, margin, margin, margin]

        return PlanarRectangle(pt=(self.X - margin[0],
                                   self.Y - margin[3]),
                                dims=(self.Width + margin[0] + margin[2]
                                 , self.height + margin[1] + margin[3]),
                               anchor_cardinality=CardinalPosition.BOTTOM_LEFT)


    def as_tuple(self):
        return (self.X, self.Y, self.Width, self.Height)

    def contains_point(self, point: Tuple[float, float]):
        return rect.rect_contains_point(self.as_tuple(), point)

    def overlaps(self, other):
        if not type(other) == PlanarRectangle and not type(other) == Tuple:
            raise TypeError(f"Cannot compare object of type {type(other)} to PlanarRectangle for overlaps()")

        if type(other) == PlanarRectangle:
            other = other.as_tuple()

        return rect.overlaps(self.as_tuple(), other)

    def align(self, pt: Tuple[float, float], alignment: CardinalPosition):
        self.anchor = Anchor2D.from_anchor(self.anchor,
                                           pt=pt,
                                           cardinality=alignment)

    def corner_generator(self):
        return self.anchor.corner_generator()

    @property
    def X(self):
        return self.BottomLeft[0]

    @X.setter
    def X(self, value):
        self.anchor = Anchor2D.from_anchor(self.anchor, pt=(value, self.anchor.pt[1]))

    @property
    def Y(self):
        return self.BottomLeft[1]

    @Y.setter
    def Y(self, value):
        self.anchor = Anchor2D.from_anchor(self.anchor, pt=(self.anchor.pt[0], value))

    @property
    def Width(self) -> float:
        return self.anchor.dims[0]

    @Width.setter
    def Width(self, value) -> float:
        self.anchor = Anchor2D.from_anchor(self.anchor, dims=(value, self.anchor.dims[1]))

    @property
    def Height(self) -> float:
        return self.anchor.dims[1]

    @Height.setter
    def Height(self, value) -> float:
        self.anchor = Anchor2D.from_anchor(self.anchor, dims=(self.anchor.dims[0], value))

    @property
    def Dims(self) -> vec.FloatVec2D:
        return self.anchor.dims

    @property
    def Center(self) -> vec.FloatVec2D:
        return self.anchor.pos(CardinalPosition.CENTER)

    @property
    def TopRight(self) -> vec.FloatVec2D:
        return self.anchor.pos(CardinalPosition.TOP_RIGHT)

    @property
    def TopLeft(self) -> vec.FloatVec2D:
        return self.anchor.pos(CardinalPosition.TOP_LEFT)

    @property
    def BottomRight(self) -> vec.FloatVec2D:
        return self.anchor.pos(CardinalPosition.BOTTOM_RIGHT)

    @property
    def BottomLeft(self) -> vec.FloatVec2D:
        return self.anchor.pos(CardinalPosition.BOTTOM_LEFT)

    @property
    def TopCenter(self) -> vec.FloatVec2D:
        return self.anchor.pos(CardinalPosition.TOP_CENTER)

    @property
    def BottomCenter(self) -> vec.FloatVec2D:
        return self.anchor.pos(CardinalPosition.BOTTOM_CENTER)

    @property
    def RightCenter(self) -> vec.FloatVec2D:
        return self.anchor.pos(CardinalPosition.RIGHT_CENTER)

    @property
    def LeftCenter(self) -> vec.FloatVec2D:
        return self.anchor.pos(CardinalPosition.LEFT_CENTER)

    @property
    def Corners(self):
        return [x for x in self.corner_generator()]

    @property
    def BoundingCircleRadius(self) -> float:
        return vec.distance_between(self.Corners[0], self.Center)

    def __str__(self):
        sig = 1
        return f"{[(round(p[0], sig), round(p[1], sig)) for p in self.Corners]}:, Size: W{self.width} x H{self.height}"


class Rectangle:
    @classmethod
    def from_meta(cls, x, y, width, height, rotation_rads: float = None, cardinality: CardinalPosition = None):
        return Rectangle.from_tuple(rect=(x, y, width, height),
                                    rotation_rads=rotation_rads,
                                    anchor_cardinality=cardinality)

    @classmethod
    def from_tuple(cls, rect: Tuple[float, float, float, float],
                   anchor_cardinality: CardinalPosition = None,
                   inverted_y: bool = False,
                   rotation_rads: float = None):
        return Rectangle(
            pt=(rect[0], rect[1]),
            dims=(rect[2], rect[3]),
            rotation_rads=rotation_rads,
            anchor_cardinality=anchor_cardinality
        )


    def __init__(self,
                 pt: vec.FloatVec2D,  # x, y
                 dims: vec.FloatVec2D,  # w, h
                 rotation_rads: float = None,
                 anchor_cardinality: CardinalPosition = None):
        self.planar = PlanarRectangle(
            pt=pt,
            dims=dims,
            anchor_cardinality=anchor_cardinality
        )

        self._rot = Rotation(
            rads=[0, 0, rotation_rads or 0],
            rotation_point_provider=lambda: self.planar.anchor.pt
        )

    def _rotated_points_around_anchor(self,
                                     points: vec.IterVec):
        ret = self._rot.rotated_points(points)
        return ret

    @property
    def UnRotatedCorners(self):
        return self.planar.Corners

    @property
    def Corners(self):
        return [p[:2] for p in self._rot.rotated_points(self.UnRotatedCorners)]

    @property
    def RotationRads(self):
        return self._rot.Rads[2]

    @property
    def Center(self) -> Tuple[float, float]:
        return self.planar.Center

    @property
    def Dims(self):
        return self.planar.Dims

    @property
    def Width(self):
        return self.planar.Width

    @property
    def Height(self):
        return self.planar.Height

    @property
    def AnchorPos(self):
        return self.planar.anchor.pos()

    def __str__(self):
        sig = 1
        return f"{[(round(p[0], sig), round(p[1], sig)) for p in self.Corners]}:, Size: W{self.Width} x H{self.Height}"

    def __repr__(self):
        return str(self)

if __name__ == '__main__':
    import math

    def test_planar_anchored_bl():
        prect = PlanarRectangle((100, 100),
                                dims=(100, 400))
        corners = prect.Corners
        assert prect.BottomLeft == corners[0] == (100, 100)
        assert prect.TopLeft == corners[1] == (100, 500)
        assert prect.TopRight == corners[2] == (200, 500)
        assert prect.BottomRight == corners[3] == (200, 100)
        assert prect.Center == (150, 300)
        assert prect.LeftCenter == (100, 300)
        assert prect.TopCenter == (150, 500)
        assert prect.RightCenter == (200, 300)
        assert prect.BottomCenter == (150, 100)

    def test_planar_anchored_center():
        prect = PlanarRectangle((100, 100),
                                dims=(100, 400),
                                anchor_cardinality=CardinalPosition.CENTER)
        corners = prect.Corners
        assert prect.BottomLeft == corners[0] == (50, -100)
        assert prect.TopLeft == corners[1] == (50, 300)
        assert prect.TopRight == corners[2] == (150, 300)
        assert prect.BottomRight == corners[3] == (150, -100)
        assert prect.Center == (100, 100)
        assert prect.LeftCenter == (50, 100)
        assert prect.TopCenter == (100, 300)
        assert prect.RightCenter == (150, 100)
        assert prect.BottomCenter == (100, -100)

    def test_rect_anchored_bl():
        rect = Rectangle((100, 100),
                         (200, 400),
                            rotation_rads=math.pi / 2,
                            # anchor_cardinality=CardinalPosition.CENTER
                         )
        #
        # print(rect.UnRotatedCorners)
        # print(rect.Corners)

        assert vec.equivelant(rect.UnRotatedCorners, [(100, 100), (100, 500), (300, 500), (300, 100)])
        assert vec.equivelant(rect.Corners, [(100.0, 100.0), (-300.0, 100.0), (-300.0, 300.0), (100.0, 300.0)])

        # print(rect)


    def test_rect_anchored_center():
        rect = Rectangle((100, 100),
                         (200, 400),
                         rotation_rads=math.pi / 2,
                         anchor_cardinality=CardinalPosition.CENTER
                         )
        #
        # print(rect.UnRotatedCorners)
        # print(rect.Corners)

        assert vec.equivelant(rect.UnRotatedCorners, [(0.0, -100.0), (0.0, 300.0), (200.0, 300.0), (200.0, -100.0)])
        assert vec.equivelant(rect.Corners, [(300.0, 0), (-100.0, 0), (-100.0, 200.0), (300.0, 200.0)])

    def t1():
        r = Rectangle.from_meta(0, 0, 100, 200, math.pi/2)


    test_planar_anchored_bl()
    test_planar_anchored_center()
    test_rect_anchored_bl()
    test_rect_anchored_center()
    t1()






