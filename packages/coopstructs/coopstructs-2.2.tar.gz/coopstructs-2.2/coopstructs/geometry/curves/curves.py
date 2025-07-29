from abc import ABC, abstractmethod
from coopstructs.geometry.vectors.vectorN import Vector2
from cooptools.geometry_utils.line_utils import collinear_points
from typing import List, Callable, Tuple, Dict
from coopstructs.geometry import Rectangle, Line, Triangle, Circle
from uuid import uuid4
from coopstructs.geometry.curves.enums import Orientation
import cooptools.geometry_utils.curve_utils as utils
import cooptools.geometry_utils.circle_utils as circ
from cooptools.common import verify_val, bounding_box_of_points
import math
import numpy as np
from cooptools.coopEnum import CircleDirection

class Curve(ABC):
    @classmethod
    @abstractmethod
    def from_points(cls, points: List[Vector2], naming_provider: Callable[[], str]) -> (List, List):
        pass

    @classmethod
    def from_dict(cls, curve_dict: Dict):
        raise NotImplementedError()

    def __init__(self, origin: Vector2, id: str=None):
        self.origin = origin
        self.id = id or uuid4()

    def __str__(self):
        return f"{type(self).__name__} starting at {self.point_at_t(0)} and terminating at {self.point_at_t(1)} [{self.id}]"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def _end_point(self):
        raise NotImplementedError()

    @abstractmethod
    def _control_points(self) -> List[Vector2]:
        raise NotImplementedError()

    def point_representation(self, resolution: int = None) -> List[Vector2]:
        if resolution is None:
            resolution = 30
        if resolution < 2:
            return []

        increment = 1 / resolution

        result = []
        t = 0
        for i in range(resolution):
            new_point = self.point_at_t(i / (resolution - 1) )
            if len(result) == 0 or new_point != result[-1]:
                result.append(new_point)
            t += increment

        return result

    def line_representation(self, resolution: int=None) -> List[Line]:
        b_points = self.point_representation(resolution)
        if b_points is None:
            return None

        ret = []
        for ii in range(0, len(b_points)):
            if ii == 0:
                continue
            else:
                start = Vector2(b_points[ii - 1].x, b_points[ii - 1].y)
                end = Vector2(b_points[ii].x, b_points[ii].y)

                if start != end:
                    ret.append(Line(start, end))
        return ret

    def bounding_box(self, resolution: int) -> Tuple[float, float, float, float]:
        return bounding_box_of_points([x.as_tuple() for x in self.point_representation(resolution=resolution)])

    @abstractmethod
    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:
        pass

    @abstractmethod
    def point_at_t(self, t: float) -> Vector2:
        pass

    @abstractmethod
    def tangent_at_t(self, t: float) -> Vector2:
        pass

    def derivative_at_t(self, t: float) -> float:
        tan = self.tangent_at_t(t)
        return tan.y / tan.x

    @property
    def Length(self):
        lines = self.line_representation()
        return sum([x.length for x in lines])

    @property
    def EndPoint(self):
        return self._end_point()

    @property
    def ControlPoints(self) -> List[Vector2]:
        return self._control_points()

    @property
    def ControlLines(self) ->List[Line]:
        cps = self.ControlPoints
        return [
            Line(origin=cps[ii], destination=cps[ii+1]) for ii in range(len(cps) - 1)
        ]

    @property
    def MidPoint(self) -> Vector2:
        return self.point_at_t(0.5)

class Arc(Curve):

    @classmethod
    def from_points(cls, points: List[Vector2], naming_provider: Callable[[], str]) -> (List, List):
        curves = []

        if len(points) == 2 and points[0] == points[1]:
            return curves, points

        for ii in range(len(points) - 1):
            orientation = Orientation.orientation_of(points[ii], points[ii + 1])[0]
            if orientation in (Orientation.UP, Orientation.RIGHT, Orientation.DOWN, Orientation.LEFT):
                curves.append(LineCurve(id=naming_provider(), origin=points[ii], destination=points[ii + 1]))
            else:
                curves.append(Arc(orientation, points[ii],
                                  Vector2(abs(points[ii + 1].x - points[ii].x) * 2,
                                          abs(points[ii + 1].y - points[ii].y) * 2),
                                  id=naming_provider())
                              )
        return curves, []

    @classmethod
    def from_dict(cls, curve_dict: Dict):
        raise NotImplementedError()

    @classmethod
    def from_arcbox(cls, id: str, orientation: Orientation, origin: Vector2, arc_box_size: Vector2):
        return Arc(orientation, origin, arc_box_size, id=id)

    @classmethod
    def from_origin_and_destination(cls, id: str, orientation: Orientation, origin: Vector2, destination: Vector2):
        return Arc(orientation, origin, Vector2(destination.x - origin.x, destination.y - origin.y) * 2, id=id)

    def __init__(self, orientation: Orientation, origin: Vector2, arc_box_size: Vector2, id: str=None):
        super().__init__(id=id, origin=origin)
        self.orientation = orientation
        self.arc_box_size = arc_box_size
        self.arc_rad_start, self.arc_rad_end = Orientation.define_arc_radian_start_end(self.orientation)
        self._arc_box = Orientation.arc_box(self.orientation, self.origin, self.arc_box_size)
        self.mid_point = Vector2(self._arc_box[0] + self._arc_box[2] / 2.0, self._arc_box[1] + self._arc_box[3] / 2.0)

    def _control_points(self) -> List[Vector2]:
        return [self.origin, self.EndPoint]

    def _end_point(self):
        if self.orientation in (Orientation.DOWN_LEFT, Orientation.LEFT_DOWN):
            return Vector2(int(self.origin.x - self.arc_box_size.x / 2), int(self.origin.y + self.arc_box_size.y / 2))
        elif self.orientation in (Orientation.LEFT_UP, Orientation.UP_LEFT):
            return Vector2(int(self.origin.x - self.arc_box_size.x / 2), int(self.origin.y - self.arc_box_size.y / 2))
        elif self.orientation in (Orientation.UP_RIGHT, Orientation.RIGHT_UP):
            return Vector2(int(self.origin.x + self.arc_box_size.x / 2), int(self.origin.y - self.arc_box_size.y / 2))
        elif self.orientation in (Orientation.RIGHT_DOWN, Orientation.DOWN_RIGHT):
            return Vector2(int(self.origin.x + self.arc_box_size.x / 2), int(self.origin.y + self.arc_box_size.y / 2))
        else:
            raise Exception("Incorrect Curve type with orientation")

    def arc_box_as_rectangle(self) -> Rectangle:
        return Rectangle.from_tuple(
            (self._arc_box[0], self._arc_box[1], self._arc_box[2], self._arc_box[3])
        )

    @property
    def Length(self):
        ab = self.arc_box_as_rectangle()
        major = max(ab.height, ab.width) / 2
        minor = min(ab.height, ab.width) / 2
        return circ.arc_length_ramanujans_approx(self.arc_rad_start, self.arc_rad_end, major_radius=major, minor_radius=minor)

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:
        if close_circuit:
            raise NotImplementedError(f"Close circuit not implemented for type [{type(self)}]")

        end_point = self.EndPoint
        if self.orientation in (Orientation.UP_LEFT, Orientation.DOWN_LEFT) and next_point.x > end_point.x:
            return Vector2(end_point.x, next_point.y)
        elif self.orientation in (Orientation.UP_RIGHT, Orientation.DOWN_RIGHT) and next_point.x < end_point.x:
            return Vector2(end_point.x, next_point.y)
        elif self.orientation in (Orientation.RIGHT_UP, Orientation.LEFT_UP) and next_point.y > end_point.y:
            return Vector2(next_point.x, end_point.y)
        elif self.orientation in (Orientation.RIGHT_DOWN, Orientation.LEFT_DOWN) and next_point.y < end_point.y:
            return Vector2(next_point.x, end_point.y)
        else:
            return next_point

    def point_along_arc(self, radians: float):
        arc_box = self.arc_box_as_rectangle()

        a = arc_box.width / 2
        b = arc_box.height / 2

        x = a * math.cos(radians)
        y = - b * math.sin(radians)

        return Vector2(x, y) + self.mid_point

    def point_at_t(self, t: float) -> Vector2:
        return self.point_along_arc(t * math.pi / 2)

    def tangent_at_t(self, t: float) -> Vector2:
        pass

class CircularArc(Curve):
    @classmethod
    def from_points(cls, points: List[Vector2], naming_provider: Callable[[], str]) -> (List, List):
        leftover_points = []
        leftover_count = (len(points) - 1) % 3 if len(points) >= 3 else len(points)
        leftover_points = points[-leftover_count:] if leftover_count != 0 else leftover_points
        used_points = points[:-leftover_count] if leftover_count != 0 else points

        curves = []

        if len(points) < 3:
            return curves, points

        # A Cubic Bezier requires 4 control points, so operate in blocks of 4 (re-using the last each time)
        for ii in range(0, len(used_points) - 3, 3):
            curves.append(CircularArc(id=naming_provider(),
                                      origin=points[ii],
                                      destination=points[ii + 1],
                                      center=points[ii + 2]))

        return curves, leftover_points

    @classmethod
    def from_3_consecutive_points(cls, a: Vector2, b: Vector2, c: Vector2, naming_provider: Callable[[], str]):
        # First determine the circle that the points lie on
        circle = Circle.from_boundary_points(a, b, c)

        rads, direction = circle.rads_between_points(a.as_tuple(), c.as_tuple(), larger_chunk=False)

        if direction == CircleDirection.CLOCKWISE:
            ret = CircularArc(id=naming_provider(),
                              origin=a,
                              destination=c,
                              center=Vector2.from_tuple(circle.Center))
        elif direction == CircleDirection.COUNTERCLOCKWISE:
            ret = CircularArc(id=naming_provider(),
                              origin=c,
                              destination=a,
                              center=Vector2.from_tuple(circle.Center))
        else:
            raise ValueError(f"Unhandled direction {direction}")

        return ret

    @classmethod
    def from_dict(cls, curve_dict: Dict):
        raise NotImplementedError()

    def __init__(self, origin: Vector2, destination: Vector2, center: Vector2, id:str=None):
        """ Create a circle given a center, start, and end. The arc is assumed to be the counter-clockwise movement from origin to
        destination, so enter the o and d appropriately based on which segment between points is required"""
        if type(center) == tuple:
            center = Vector2.from_tuple(center)
        if type(origin) == tuple:
            origin = Vector2.from_tuple(origin)
        if type(destination) == tuple:
            destination = Vector2.from_tuple(destination)

        if origin == center or destination == center or origin == destination:
            raise ValueError(f"Origin, destination and center must all be different. Provided:"
                             f"\no: {origin}"
                             f"\nd: {destination}"
                             f"\nc: {center}")

        centered_o = origin - center
        centered_d = destination - center
        min_length = min(centered_o.length(), centered_d.length())

        scaled_o = centered_o.scaled_to_length(min_length)
        scaled_d = centered_d.scaled_to_length(min_length)

        used_o = center + scaled_o
        used_d = center + scaled_d

        super().__init__(id=id, origin=used_o)
        self.circle = Circle(center, radius=min_length)
        self.destination = used_d

    @property
    def center(self):
        return self.circle.center

    @property
    def angle_rads(self):
        return self.circle.rads_between_points(self.origin.as_tuple(), self.destination.as_tuple())

    @property
    def arc_length(self):
        return self.radius * self.angle_rads[0]

    @property
    def radius(self):
        return self.circle.radius

    @property
    def origin_rads(self):
        return self.circle.rads_of_point(self.origin.as_tuple())

    @property
    def destination_rads(self):
        return self.circle.rads_of_point(self.destination)

    def _end_point(self):
        return self.destination

    def _control_points(self) -> List[Vector2]:
        return [self.origin, self.destination, self.center]

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:
        raise NotImplementedError(f"force_circuit not implemented for type [{type(self)}]")

    def compute_circulararc_points(self, numPoints: int = None):
        if numPoints is None:
            numPoints = 30

        step_size = self.angle_rads[0] / numPoints
        start = self.circle.rads_of_point(self.origin.as_tuple())
        points = []
        for ii in range(0, numPoints):
            point = self.circle.point_at_angle(radians=start + ii * step_size)
            points.append(point)

        return points

    def point_at_t(self, t: float) -> Vector2:
        return Vector2.from_tuple(circ.point_at_angle(
            center=self.center,
            radius=self.radius,
            radians=self.origin_rads + t * self.angle_rads[0] * -1 * self.angle_rads[1].value
        ))

    def tangent_at_t(self, t: float) -> Vector2:
        raise NotImplementedError()

class LineCurve(Curve):
    @classmethod
    def from_points(self, points, naming_provider: Callable[[], str]) -> (List, List):
        lines = []
        for ii in range(len(points) - 1):
            lines.append(LineCurve(points[ii], points[ii + 1], id=naming_provider()))
        return lines, []

    @classmethod
    def from_dict(cls, curve_dict: Dict):
        o = Vector2.from_json(curve_dict['controlPoints'][0])
        d = Vector2.from_json(curve_dict['controlPoints'][1])

        return LineCurve(origin=o, destination=d, id=curve_dict.get('id', None))

    def __init__(self, origin: Vector2, destination: Vector2, id: str=None):
        if origin == destination:
            raise ValueError(f"Origin and destination cannot be shared for a LineCurve")

        super().__init__(id=id, origin=origin)
        self.destination = destination

    def _control_points(self) -> List[Vector2]:
        return [self.origin, self.EndPoint]

    def line_representation(self, resolution:int=None):
        return [Line(self.origin, self.destination)]

    def _end_point(self):
        return self.destination

    @property
    def Length(self):
        return Line(self.origin, self.destination).length

    @property
    def Line(self):
        return Line(self.origin, self.destination)

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:
        if close_circuit:
            raise NotImplementedError(f"Close circuit not implemented for type [{type(self)}]")
        return next_point

    def point_at_t(self, t: float):
        if not (0 <= t <= 1):
            raise ValueError(f"t must be between 0 and 1 but {t} was provided")

        line_vector = self.EndPoint - self.origin
        t_vector = line_vector * t

        return self.origin + t_vector

    def tangent_at_t(self, t: float) -> Vector2:
        verify_val(t, gte=0, lte=1)
        return (self.EndPoint - self.origin).unit()

class CubicBezier(Curve):

    @classmethod
    def from_dict(cls, curve_dict: Dict):
        cps = []
        for pt_data in curve_dict['controlPoints']:
            pt = Vector2.from_json(pt_data)
            cps.append(pt)

        return CubicBezier(control_points=cps, id=curve_dict.get('id', None))

    def point_at_t(self, t: float):
        return Vector2.from_tuple(utils.cubic_bezier_point_at_t(t, [x.as_tuple() for x in self.ControlPoints]))

    def tangent_at_t(self, t: float) -> Vector2:
        return Vector2.from_tuple(utils.cubic_bezier_tangent_at_t(t, [x.as_tuple() for x in self.ControlPoints])).unit()

    @classmethod
    def as_circular_arcs(cls, curve, tolerance: float = 0.1):
        if not type(curve) == CubicBezier:
            raise TypeError(f"provided value was not of type {CubicBezier}. {type(curve)} provided")

        # find inflection points
        inflection_points = utils.cubic_bezier_inflection_points(control_points=[x.as_tuple() for x in curve.ControlPoints])

        # handle inflection points on curve
        if len(inflection_points) > 0:
            sub_divisions = curve.sub_divide_at_t(inflection_points[0][1])
            arcs = [CubicBezier.as_circular_arcs(x, tolerance) for x in sub_divisions]
            return [item for sublist in arcs for item in sublist]

        # handle check if circle is a good approximater
        if curve.origin != curve.EndPoint:
            circle = curve.biarc_circle()
            deviation = cls.max_delta_on_circle(curve, circle) if circle is not None else None
            if circle is None:
                # no arcs for this curve since the circle could not be defined (straight line bezier)
                return []
            elif deviation < tolerance or curve.Length < tolerance:
                # approximating arc is withing tolerance, return the arc
                return [CircularArc.from_3_consecutive_points(a=Vector2.from_tuple(circle.known_boundary_points[0]),
                                                              b=Vector2.from_tuple(circle.known_boundary_points[1]),
                                                              c=Vector2.from_tuple(circle.known_boundary_points[2]),
                                                              naming_provider=lambda: str(uuid4()))]

            # handle subdivide and try again
            sub_divisions = curve.sub_divide_at_t(0.5)
            arcs = [CubicBezier.as_circular_arcs(x, tolerance) for x in sub_divisions]
            return [item for sublist in arcs for item in sublist]
        else:
            return []

    @classmethod
    def max_delta_on_circle(cls, curve, biarc_circle: Circle, comparison_points: int = 10):
        max_delta = 0
        for point in curve.point_representation(resolution=comparison_points):
            dist_from_center = (point - Vector2.from_tuple(biarc_circle.center)).length()
            deviation = abs(biarc_circle.radius - dist_from_center)
            if deviation > max_delta:
                max_delta = deviation

        return max_delta

    @classmethod
    def from_points(cls, points: List[Vector2], naming_provider: Callable[[], str]) -> (List, List):
        leftover_points = []
        leftover_count = (len(points) - 1) % 3 if len(points) >= 4 else len(points)
        leftover_points = points[-leftover_count:] if leftover_count != 0 else leftover_points
        used_points = points[:-leftover_count] if leftover_count != 0 else points

        curves = []

        if len(points) < 4:
            return curves, points

        # A Cubic Bezier requires 4 control points, so operate in blocks of 4 (re-using the last each time)
        for ii in range(0, len(used_points) - 3, 3):
            curves.append(CubicBezier(points[ii:ii + 4], id=naming_provider()))

        return curves, leftover_points

    def __init__(self, control_points: List[Vector2], id: str=None):
        verify_val(len(control_points), eq=4)

        if all(point.distance_from(control_points[0]) < .001 for point in control_points):
            raise ValueError(f"the provided control points are invalid as they are all the same: {control_points[0]}")

        Curve.__init__(self, control_points[0], id)
        self._cps = control_points

    def _control_points(self) -> List[Vector2]:
        return self._cps

    def _end_point(self):
        return self.ControlPoints[-1]

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:

        if close_circuit:
            return next_point.project_onto(self.ControlPoints[0], self.ControlPoints[1])
        else:
            return next_point.project_onto(self.ControlPoints[-1], self.ControlPoints[-2])

    def biarc_circle(self) -> Circle:
        """The circle that is defined by the 2 end points of the spline and the mid point"""

        p1 = self.ControlPoints[0]
        p4 = self.ControlPoints[3]

        p1_ = p1 + self.tangent_at_t(0)
        p4_ = p4 + self.tangent_at_t(1)

        try:
            line1 = Line(origin=p1, destination=p1_)
            line2 = Line(origin=p4, destination=p4_)
            V = line1.intersection(line2)
        except:
            return None

        if V is None:
            if not collinear_points([x.as_tuple() for x in [p1, self.point_at_t(0.5), p4]]):
                return Circle.from_boundary_points(p1, self.point_at_t(0.5), p4)
            if not collinear_points([x.as_tuple() for x in [p1, self.point_at_t(0.25), p4]]):
                return Circle.from_boundary_points(p1, self.point_at_t(0.25), p4)
            raise ValueError(f"EndPoints are collinear with attempted mid points")

        if not collinear_points([p1.as_tuple(), V, p4.as_tuple()]):
            tri = Triangle(p1.as_tuple(), V, p4.as_tuple())
            incentre = tri.incentre()

            biarc_circ = Circle.from_boundary_points(p1, incentre, p4)
        else:
            return None

        return biarc_circ

    def sub_divide_at_t(self, t: float):
        return [CubicBezier(control_points=[Vector2.from_tuple(p1),
                                            Vector2.from_tuple(r2),
                                            Vector2.from_tuple(r3),
                                            Vector2.from_tuple(point_t)], id=str(uuid4())) for p1, r2, r3, point_t in
                utils.cubic_bezier_sub_divide_at_t(t, [x.as_tuple() for x in self.ControlPoints])]


class CubicUniformBasisSpline(Curve):
    @classmethod
    def from_dict(cls, curve_dict: Dict):
        cps = []
        for pt_data in curve_dict['controlPoints']:
            pt = Vector2.from_json(pt_data)
            cps.append(pt)

        return CubicUniformBasisSpline(control_points=cps, id=curve_dict.get('id', None))

    def __init__(self, control_points: List[Vector2], id: str=None):
        verify_val(len(control_points), gte=4)

        if all(point.distance_from(control_points[0]) < .001 for point in control_points):
            raise ValueError(f"the provided control points are invalid as they are all the same: {control_points[0]}")

        Curve.__init__(self, control_points[0], id)
        self._cps = control_points
        self.degree = 3


    def _control_points_for_segment(self, i: int):
        return self._cps[i:i+4]


    def _render_formula(self, t, deriv_order: int):
        seg_idx = min(int(t * self.nSegments), self.nSegments - 1)
        t_in_seg = (t - seg_idx / self.nSegments) * (self.nSegments)

        if deriv_order == 0:
            t_M = np.array([1, t_in_seg, t_in_seg ** 2, t_in_seg**3])
        elif deriv_order == 1:
            t_M = np.array([0, 1, 2 * t_in_seg, 3 * t_in_seg ** 2])
        elif deriv_order == 2:
            t_M = np.array([0, 0, 2, 6 * t_in_seg])
        else:
            raise ValueError(f"Unhandled deriv_order {deriv_order}")

        cbsm = self.cubic_basis_spline_matrix()

        pts = np.array([x.as_tuple() for x in self._control_points_for_segment(seg_idx)])

        poly_M = t_M.dot(cbsm)
        val = poly_M.dot(pts)

        return Vector2(x=val[0], y=val[1])

    def point_at_t(self, t: float) -> Vector2:
        return self._render_formula(t, deriv_order=0)

    def tangent_at_t(self, t: float) -> Vector2:
        return self._render_formula(t, deriv_order=1)

    def cubic_basis_spline_matrix(self):
        return 1/ 6 * np.array(
            [[1, 4, 1, 0],
            [-3, 0, 3, 0],
            [3, -6, 3, 0],
            [-1, 3, -3, 1]]
        )

    def _control_points(self) -> List[Vector2]:
        return self._cps

    def _end_point(self):
        pass

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:
        pass

    def from_points(cls, points: List[Vector2], naming_provider: Callable[[], str]) -> (List, List):
        pass

    @property
    def nSegments(self):
        return len(self.ControlPoints) - self.degree

    @classmethod
    def basis_to_bezier_matrix(cls, control_points):

        CubicBasisToCubicBezierMatrix = np.array([
            [1, 4, 1, 0],
            [0, 4, 2, 0],
            [0, 2, 4, 0],
            [0, 1, 4, 1]]) * (1 / 6)

        # Convert the basis spline into a list of Bezier segments. When there are n control points, there will be n-3 Bezier
        # segments (for cubic basis spline).

        control_points = np.array(control_points)
        bezierNodes = np.dot(CubicBasisToCubicBezierMatrix, control_points)
        return bezierNodes

    @property
    def AsCubicBezier(self) -> List[CubicBezier]:
        bezies = []
        for ii in range(3, len(self._cps)):
            relevant_nodes = self._cps[ii-3:ii+1]
            converted_points = CubicUniformBasisSpline.basis_to_bezier_matrix([x.as_tuple() for x in relevant_nodes])
            bezie_nodes = [Vector2.from_tuple((x[0], x[1])) for x in converted_points]

            bezies.append(CubicBezier(control_points=bezie_nodes))

        return bezies


class CatmullRom(Curve):

    @classmethod
    def from_points(cls, points: List[Vector2], naming_provider: Callable[[], str]) -> (List, List):
        leftover_points = []
        leftover_count = len(points) if len(points) < 4 else 0
        leftover_points = points if leftover_count != 0 else leftover_points
        used_points = points if leftover_count == 0 else []

        curves = []

        if len(used_points) < 4:
            return [], points

        # A Cubic Bezier requires 4 control points, so operate in blocks of 3 (re-using the last each time)
        curves.append(CatmullRom(points, naming_provider()))
        return curves, leftover_points

    @classmethod
    def from_dict(cls, curve_dict: Dict):
        raise NotImplementedError()

    def __init__(self, control_points: List[Vector2], id: str = None):
        Curve.__init__(self, control_points[0], id)

        if len(control_points) < 4:
            raise ValueError(
                f"Invalid input for control points. Must have at least 4 values but list of length {len(control_points)} was provided: [{control_points}]")
        self._cps = control_points

    def _control_points(self) -> List[Vector2]:
        return self._cps

    def _end_point(self):
        return self.ControlPoints[-1]

    def force_continuity(self, next_point: Vector2, close_circuit: bool = False) -> Vector2:
        if close_circuit:
            raise NotImplementedError(f"Close circuit not implemented for type [{type(self)}]")
        return next_point

    def point_at_t(self, t: float):
        reso = 30
        return self.point_representation(resolution=reso)[int(t * reso)]

    def point_representation(self, resolution: int = None) -> List[Vector2]:
        return [Vector2.from_tuple(x) for x in utils.catmull_points([x.as_tuple() for x in self.ControlPoints], numPoints=resolution)]

    def tangent_at_t(self, t: float) -> Vector2:
        raise NotImplementedError()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from cooptools.plotting import plot_series
    from cooptools.colors import Color
    import random as rnd
    from pprint import pprint

    def test1():
        rnd.seed(50)
        cb_og = CubicBezier(control_points=[Vector2(rnd.uniform(0, 10), rnd.uniform(0, 10)),
                                            Vector2(rnd.uniform(0, 10), rnd.uniform(0, 10)),
                                            Vector2(rnd.uniform(0, 10), rnd.uniform(0, 10)),
                                            Vector2(rnd.uniform(0, 10), rnd.uniform(0, 10))])
        cb_subs = cb_og.sub_divide_at_t(0.5)
        biarc = cb_og.biarc_circle()

        fig, ax = plt.subplots()

        plot_series(points=[x.as_tuple() for x in cb_og.point_representation(30)], ax=ax)
        # plot_series(points=[biarc.point_at_angle(degrees=x) for x in range(360)], ax=ax, line_style='--')

        # for sub in cb_subs:
        #     color = Color.random()
        #     # plot_series(points=[x.as_tuple() for x in sub.point_representation(30)], ax=ax, color=color)
        #     biarc = sub.biarc_circle()
        #     # plot_series(points=[biarc.point_at_angle(degrees=x) for x in range(360)], ax=ax, line_style='--', color=color)


        circs = CubicBezier.as_circular_arcs(cb_og, tolerance=.001)
        for ii, c in enumerate(circs):
            if c.circle.radius < 1:
                plot_series(points=[c.circle.point_at_angle(degrees=x) for x in range(360)], ax=ax, line_style='dotted', color=Color.GREY)

            plot_series(points=[c.point_at_t(t=x/100).as_tuple() for x in range(100)], ax=ax, line_style='--')

        plt.show(block=True)

    def test2():

        cub = CubicUniformBasisSpline(control_points=[Vector2(rnd.uniform(0, 10), rnd.uniform(0, 10)) for x in range(10)])
        pprint(cub)
        pprint(cub.AsCubicBezier)

    # test1()
    test2()