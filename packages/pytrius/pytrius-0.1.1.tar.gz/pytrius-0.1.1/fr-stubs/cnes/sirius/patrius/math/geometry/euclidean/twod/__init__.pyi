
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.geometry
import fr.cnes.sirius.patrius.math.geometry.euclidean.oned
import fr.cnes.sirius.patrius.math.geometry.partitioning
import fr.cnes.sirius.patrius.math.linear
import java.awt.geom
import java.lang
import java.text
import java.util
import jpype
import typing



class EnumPolygon(java.lang.Enum['EnumPolygon']):
    """
    public enum EnumPolygon extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.EnumPolygon`>
    
        Define the type of 2D polygon
    
        Since:
            3.2
    """
    DEGENERATED: typing.ClassVar['EnumPolygon'] = ...
    CROSSING_BORDER: typing.ClassVar['EnumPolygon'] = ...
    CONVEX: typing.ClassVar['EnumPolygon'] = ...
    CONCAVE: typing.ClassVar['EnumPolygon'] = ...
    def getName(self) -> str:
        """
            Getter for the enumerate name.
        
            Returns:
                name
        
        
        """
        ...
    def isWellFormed(self) -> bool:
        """
            A well formed polygon is CONCAVE or CONVEX
        
            Returns:
                boolean to indicate if polygon is well formed
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'EnumPolygon':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                : if this enum type has no constant with the specified name
                : if the argument is null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['EnumPolygon']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (EnumPolygon c : EnumPolygon.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class Euclidean2D(fr.cnes.sirius.patrius.math.geometry.Space):
    """
    public final class Euclidean2D extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.geometry.Space`
    
        This class implements a three-dimensional space.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def getDimension(self) -> int:
        """
            Get the dimension of the space.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Space.getDimension` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Space`
        
            Returns:
                dimension of the space
        
        
        """
        ...
    @staticmethod
    def getInstance() -> 'Euclidean2D':
        """
            Get the unique instance.
        
            Returns:
                the unique instance
        
        
        """
        ...
    def getSubSpace(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Euclidean1D:
        """
            Get the n-1 dimension subspace of this space.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Space.getSubSpace` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Space`
        
            Returns:
                n-1 dimension sub-space of this space
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Space.getDimension`
        
        
        """
        ...

class Line(fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane[Euclidean2D], fr.cnes.sirius.patrius.math.geometry.partitioning.Embedding[Euclidean2D, fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Euclidean1D]):
    """
    public class Line extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane`<:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Euclidean2D`>, :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Embedding`<:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Euclidean2D`,:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Euclidean1D`>
    
        This class represents an oriented line in the 2D plane.
    
        An oriented line can be defined either by prolongating a line segment between two points past these points, or by one
        point and an angular direction (in trigonometric orientation).
    
        Since it is oriented the two half planes at its two sides are unambiguously identified as a left half plane and a right
        half plane. This can be used to identify the interior and the exterior in a simple way by local properties only when
        part of a line is used to define part of a polygon boundary.
    
        A line can also be used to completely define a reference frame in the plane. It is sufficient to select one specific
        point in the line (the orthogonal projection of the original reference frame on the line) and to use the unit vector in
        the line direction and the orthogonal vector oriented from left half plane to right half plane. We define two
        coordinates by the process, the *abscissa* along the line, and the *offset* across the line. All points of the plane are
        uniquely identified by these two coordinates. The line is the set of points at zero offset, the left half plane is the
        set of points with negative offsets and the right half plane is the set of points with positive offsets.
    
        Since:
            3.0
    """
    @typing.overload
    def __init__(self, line: 'Line'): ...
    @typing.overload
    def __init__(self, vector2D: 'Vector2D', double: float): ...
    @typing.overload
    def __init__(self, vector2D: 'Vector2D', vector2D2: 'Vector2D'): ...
    def contains(self, vector2D: 'Vector2D') -> bool:
        """
            Check if the line contains a point.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): point to check
        
            Returns:
                true if p belongs to the line
        
        
        """
        ...
    def copySelf(self) -> 'Line':
        """
            Copy the instance.
        
            The instance created is completely independant of the original one. A deep copy is used, none of the underlying objects
            are shared (except for immutable objects).
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane.copySelf` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane`
        
            Returns:
                a new hyperplane, copy of the instance
        
        
        """
        ...
    def distance(self, vector2D: 'Vector2D') -> float:
        """
            Compute the distance between the instance and a point.
        
            This is a shortcut for invoking FastMath.abs(getOffset(p)), and provides consistency with what is in the
            fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line class.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): to check
        
            Returns:
                distance between the instance and the point
        
            Since:
                3.1
        
        
        """
        ...
    def getAngle(self) -> float:
        """
            Get the angle of the line.
        
            Returns:
                the angle of the line with respect to the abscissa axis
        
        
        """
        ...
    @typing.overload
    def getOffset(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]) -> float:
        """
            Get the offset (oriented distance) of a parallel line.
        
            This method should be called only for parallel lines otherwise the result is not meaningful.
        
            The offset is 0 if both lines are the same, it is positive if the line is on the right side of the instance and negative
            if it is on the left side, according to its natural orientation.
        
            Parameters:
                line (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Line`): line to check
        
            Returns:
                offset of the line
        
        public double getOffset(:class:`~fr.cnes.sirius.patrius.math.geometry.Vector`<:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Euclidean2D`> point)
        
            Get the offset (oriented distance) of a point.
        
            The offset is 0 if the point is on the underlying hyperplane, it is positive if the point is on one particular side of
            the hyperplane, and it is negative if the point is on the other side, according to the hyperplane natural orientation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane.getOffset` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane`
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.geometry.Vector`<:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Euclidean2D`> point): point to check
        
            Returns:
                offset of the point
        
        
        """
        ...
    @typing.overload
    def getOffset(self, line: 'Line') -> float: ...
    def getOriginOffset(self) -> float:
        """
            Get the offset of the origin.
        
            Returns:
                the offset of the origin
        
        
        """
        ...
    def getPointAt(self, vector1D: fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Vector1D, double: float) -> 'Vector2D':
        """
            Get one point from the plane.
        
            Parameters:
                abscissa (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Vector1D`): desired abscissa for the point
                offset (double): desired offset for the point
        
            Returns:
                one point in the plane, with given abscissa and offset relative to the line
        
        
        """
        ...
    def getReverse(self) -> 'Line':
        """
            Get the reverse of the instance.
        
            Get a line with reversed orientation with respect to the instance. A new object is built, the instance is untouched.
        
            Returns:
                a new line, with orientation opposite to the instance orientation
        
        
        """
        ...
    @staticmethod
    def getTransform(affineTransform: java.awt.geom.AffineTransform) -> fr.cnes.sirius.patrius.math.geometry.partitioning.Transform[Euclidean2D, fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Euclidean1D]: ...
    def intersection(self, line: 'Line') -> 'Vector2D':
        """
            Get the intersection point of the instance and another line.
        
            Parameters:
                other (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Line`): other line
        
            Returns:
                intersection point of the instance and the other line or null if there are no intersection points
        
        
        """
        ...
    def isParallelTo(self, line: 'Line') -> bool:
        """
            Check the instance is parallel to another line.
        
            Parameters:
                line (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Line`): other line to check
        
            Returns:
                true if the instance is parallel to the other line (they can have either the same or opposite orientations)
        
        
        """
        ...
    @typing.overload
    def reset(self, vector2D: 'Vector2D', double: float) -> None:
        """
            Reset the instance as if built from two points.
        
            The line is oriented from p1 to p2
        
            Parameters:
                p1 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): first point
                p2 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): second point
        
            Reset the instance as if built from a line and an angle.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): point belonging to the line
                alpha (double): angle of the line with respect to abscissa axis
        
        
        """
        ...
    @typing.overload
    def reset(self, vector2D: 'Vector2D', vector2D2: 'Vector2D') -> None: ...
    def revertSelf(self) -> None:
        """
            Revert the instance.
        
        """
        ...
    def sameOrientationAs(self, hyperplane: fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane[Euclidean2D]) -> bool: ...
    def setAngle(self, double: float) -> None:
        """
            Set the angle of the line.
        
            Parameters:
                angleIn (double): new angle of the line with respect to the abscissa axis
        
        
        """
        ...
    def setOriginOffset(self, double: float) -> None:
        """
            Set the offset of the origin.
        
            Parameters:
                offset (double): offset of the origin
        
        
        """
        ...
    def toSpace(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Euclidean1D]) -> 'Vector2D': ...
    def toSubSpace(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]) -> fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Vector1D: ...
    def translateToPoint(self, vector2D: 'Vector2D') -> None:
        """
            Translate the line to force it passing by a point.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): point by which the line should pass
        
        
        """
        ...
    def wholeHyperplane(self) -> 'SubLine':
        """
            Build a sub-hyperplane covering the whole hyperplane.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane.wholeHyperplane` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane`
        
            Returns:
                a sub-hyperplane covering the whole hyperplane
        
        
        """
        ...
    def wholeSpace(self) -> 'PolygonsSet':
        """
            Build a region covering the whole space.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane.wholeSpace` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane`
        
            Returns:
                a region containing the instance (really a :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.PolygonsSet`
                instance)
        
        
        """
        ...

class PolygonsSet(fr.cnes.sirius.patrius.math.geometry.partitioning.AbstractRegion[Euclidean2D, fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Euclidean1D]):
    """
    public class PolygonsSet extends :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.AbstractRegion`<:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Euclidean2D`,:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Euclidean1D`>
    
        This class represents a 2D region: a set of polygons.
    
        Since:
            3.0
    """
    MIN_POINT_NB: typing.ClassVar[int] = ...
    """
    public static final int MIN_POINT_NB
    
        Minimum number of points to build a polygon.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, double: float, *vector2D: 'Vector2D'): ...
    @typing.overload
    def __init__(self, vector2DArray: typing.Union[typing.List[typing.MutableSequence['Vector2D']], jpype.JArray]): ...
    @typing.overload
    def __init__(self, bSPTree: fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree[Euclidean2D]): ...
    @typing.overload
    def __init__(self, collection: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane[Euclidean2D]], typing.Sequence[fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane[Euclidean2D]], typing.Set[fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane[Euclidean2D]]]): ...
    def buildNew(self, bSPTree: fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree[Euclidean2D]) -> 'PolygonsSet': ...
    def checkPolygonSet(self) -> bool:
        """
            Method to check PolygonSet based on three criteria (three checks) :
        
              - Classification of polygons must not be CROSSING_BORDERS or DEGENERATED
              - Size of polygon must be different from Double.POSITIVE_INFINITY (open-loop polygon)
        
            Remarks :
        
              - If both criteria are satisfied, polygon will have at least three points
              - If constructor null is used, second exception cannot be reached (vertices are automatically sorted in TRIGO sense, which
                prevent crossing borders)
              - If constructor null is used, third exception cannot be reached (the first will be reached before)
        
        
            Returns:
                true if previous criteria are satisfied
        
        
        """
        ...
    def getBiggerLength(self) -> float:
        """
            Get the polygon's bigger length, i.e. the largest size among its points.
        
            Returns:
                the polygon's bigger length
        
        
        """
        ...
    def getClassification(self) -> EnumPolygon:
        """
        
            Returns:
                the classification
        
        
        """
        ...
    def getMaxX(self) -> float:
        """
        
            Returns:
                the maxX
        
        
        """
        ...
    def getMaxY(self) -> float:
        """
        
            Returns:
                the maxY
        
        
        """
        ...
    def getMinX(self) -> float:
        """
        
            Returns:
                the minX
        
        
        """
        ...
    def getMinY(self) -> float:
        """
        
            Returns:
                the minY
        
        
        """
        ...
    def getVertices(self) -> typing.MutableSequence[typing.MutableSequence['Vector2D']]:
        """
            Get the vertices of the polygon.
        
            The polygon boundary can be represented as an array of loops, each loop being itself an array of vertices.
        
            In order to identify open loops which start and end by infinite edges, the open loops arrays start with a null point. In
            this case, the first non null point and the last point of the array do not represent real vertices, they are dummy
            points intended only to get the direction of the first and last edge. An open loop consisting of a single infinite line
            will therefore be represented by a three elements array with one null point followed by two dummy points. The open loops
            are always the first ones in the loops array.
        
            If the polygon has no boundary at all, a zero length loop array will be returned.
        
            All line segments in the various loops have the inside of the region on their left side and the outside on their right
            side when moving in the underlying line direction. This means that closed loops surrounding finite areas obey the direct
            trigonometric orientation.
        
            Returns:
                vertices of the polygon, organized as oriented boundary loops with the open loops first (the returned value is
                guaranteed to be non-null)
        
        
        """
        ...
    @staticmethod
    def sortVerticies(vector2DArray: typing.Union[typing.List[typing.MutableSequence['Vector2D']], jpype.JArray], boolean: bool) -> typing.MutableSequence[typing.MutableSequence['Vector2D']]:
        """
            Method to sort vertices according to a specific sense : (trigonometric or clockwise)
        
            Parameters:
                v (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`[][]): array of vertices
                trigo (boolean): true if trigonometric sense
        
            Returns:
                the sorted polygons
        
        
        """
        ...

class Segment:
    """
    public class Segment extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Simple container for a two-points segment.
    
        Since:
            3.0
    """
    @typing.overload
    def __init__(self, vector2D: 'Vector2D', vector2D2: 'Vector2D'): ...
    @typing.overload
    def __init__(self, vector2D: 'Vector2D', vector2D2: 'Vector2D', line: Line): ...
    def distance(self, vector2D: 'Vector2D') -> float:
        """
            Calculates the shortest distance from a point to this line segment.
        
            If the perpendicular extension from the point to the line does not cross in the bounds of the line segment, the shortest
            distance to the two end points will be returned.
            Algorithm adapted from: ` Thread @ Codeguru
            <http://www.codeguru.com/forum/printthread.php?s=cc8cf0596231f9a7dba4da6e77c29db3&t=194400&pp=15&page=1>`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): to check
        
            Returns:
                distance between the instance and the point
        
            Since:
                3.1
        
        
        """
        ...
    def getClosestPoint(self, vector2D: 'Vector2D') -> 'Vector2D':
        """
            Returns closest point of provided point belonging to segment.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): a point
        
            Returns:
                closest point of provided point belonging to segment
        
        
        """
        ...
    def getEnd(self) -> 'Vector2D':
        """
            Get the end point of the segment.
        
            Returns:
                end point of the segment
        
        
        """
        ...
    def getIntersection(self, segment: 'Segment') -> 'Vector2D':
        """
            Returns the intersection between two segments, null if there is no intersection.
        
            Parameters:
                segment (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Segment`): a segment
        
            Returns:
                the intersection between two segments, null if there is no intersection
        
        
        """
        ...
    def getLine(self) -> Line:
        """
            Get the line containing the segment.
        
            Returns:
                line containing the segment
        
        
        """
        ...
    def getStart(self) -> 'Vector2D':
        """
            Get the start point of the segment.
        
            Returns:
                start point of the segment
        
        
        """
        ...

class SubLine(fr.cnes.sirius.patrius.math.geometry.partitioning.AbstractSubHyperplane[Euclidean2D, fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Euclidean1D]):
    """
    public class SubLine extends :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.AbstractSubHyperplane`<:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Euclidean2D`,:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Euclidean1D`>
    
        This class represents a sub-hyperplane for :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Line`.
    
        Since:
            3.0
    """
    @typing.overload
    def __init__(self, segment: Segment): ...
    @typing.overload
    def __init__(self, vector2D: 'Vector2D', vector2D2: 'Vector2D'): ...
    @typing.overload
    def __init__(self, hyperplane: fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane[Euclidean2D], region: fr.cnes.sirius.patrius.math.geometry.partitioning.Region[fr.cnes.sirius.patrius.math.geometry.euclidean.oned.Euclidean1D]): ...
    def getSegments(self) -> java.util.List[Segment]: ...
    def intersection(self, subLine: 'SubLine', boolean: bool) -> 'Vector2D':
        """
            Get the intersection of the instance and another sub-line.
        
            This method is related to the :meth:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Line.intersection` method in
            the :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Line` class, but in addition to compute the point along
            infinite lines, it also checks the point lies on both sub-line ranges.
        
            Parameters:
                subLine (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.SubLine`): other sub-line which may intersect instance
                includeEndPoints (boolean): if true, endpoints are considered to belong to instance (i.e. they are closed sets) and may be returned, otherwise
                    endpoints are considered to not belong to instance (i.e. they are open sets) and intersection occurring on endpoints
                    lead to null being returned
        
            Returns:
                the intersection point if there is one, null if the sub-lines don't intersect
        
        
        """
        ...
    def side(self, hyperplane: fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane[Euclidean2D]) -> fr.cnes.sirius.patrius.math.geometry.partitioning.Side: ...
    def split(self, hyperplane: fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane[Euclidean2D]) -> fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane.SplitSubHyperplane[Euclidean2D]: ...

class Vector2D(fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]):
    """
    public class Vector2D extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`<:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Euclidean2D`>
    
        This class represents a 2D vector.
    
        Instances of this class are guaranteed to be immutable.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    ZERO: typing.ClassVar['Vector2D'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D` ZERO
    
        Origin (coordinates: 0, 0).
    
    """
    NaN: typing.ClassVar['Vector2D'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D` NaN
    
        A vector with all coordinates set to NaN.
    
    """
    POSITIVE_INFINITY: typing.ClassVar['Vector2D'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D` POSITIVE_INFINITY
    
        A vector with all coordinates set to positive infinity.
    
    """
    NEGATIVE_INFINITY: typing.ClassVar['Vector2D'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D` NEGATIVE_INFINITY
    
        A vector with all coordinates set to negative infinity.
    
    """
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, vector2D: 'Vector2D'): ...
    @typing.overload
    def __init__(self, double: float, vector2D: 'Vector2D', double2: float, vector2D2: 'Vector2D'): ...
    @typing.overload
    def __init__(self, double: float, vector2D: 'Vector2D', double2: float, vector2D2: 'Vector2D', double3: float, vector2D3: 'Vector2D'): ...
    @typing.overload
    def __init__(self, double: float, vector2D: 'Vector2D', double2: float, vector2D2: 'Vector2D', double3: float, vector2D3: 'Vector2D', double4: float, vector2D4: 'Vector2D'): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def add(self, double: float, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]) -> 'Vector2D': ...
    @typing.overload
    def add(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]) -> 'Vector2D': ...
    @staticmethod
    def angle(vector2D: 'Vector2D', vector2D2: 'Vector2D') -> float:
        """
            Compute the angular separation between two vectors.
        
            This method computes the angular separation between two vectors using the dot product for well separated vectors and the
            cross product for almost aligned vectors. This allows to have a good accuracy in all cases, even for vectors very close
            to each other.
        
            Parameters:
                p1 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): first vector
                p2 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): second vector
        
            Returns:
                angular separation between v1 and v2
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if either vector has a null norm
        
        
        """
        ...
    @typing.overload
    def distance(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]) -> float:
        """
            Compute the distance between two vectors according to the L :sub:`2` norm.
        
            Calling this method is equivalent to calling: :code:`p1.subtract(p2).getNorm()` except that no intermediate vector is
            built
        
            Parameters:
                p1 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): first vector
                p2 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): second vector
        
            Returns:
                the distance between p1 and p2 according to the L :sub:`2` norm
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def distance(vector2D: 'Vector2D', vector2D2: 'Vector2D') -> float: ...
    def distance1(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]) -> float: ...
    @typing.overload
    def distanceInf(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]) -> float:
        """
            Compute the distance between two vectors according to the L :sub:`∞` norm.
        
            Calling this method is equivalent to calling: :code:`p1.subtract(p2).getNormInf()` except that no intermediate vector is
            built
        
            Parameters:
                p1 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): first vector
                p2 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): second vector
        
            Returns:
                the distance between p1 and p2 according to the L :sub:`∞` norm
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def distanceInf(vector2D: 'Vector2D', vector2D2: 'Vector2D') -> float: ...
    @typing.overload
    def distanceSq(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]) -> float:
        """
            Compute the square of the distance between two vectors.
        
            Calling this method is equivalent to calling: :code:`p1.subtract(p2).getNormSq()` except that no intermediate vector is
            built
        
            Parameters:
                p1 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): first vector
                p2 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): second vector
        
            Returns:
                the square of the distance between p1 and p2
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def distanceSq(vector2D: 'Vector2D', vector2D2: 'Vector2D') -> float: ...
    @typing.overload
    def dotProduct(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]) -> float:
        """
            Compute the dot product between two vectors.
        
            Parameters:
                p1 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): first vector
                p2 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): second vector
        
            Returns:
                the dot product between p1 and p2
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def dotProduct(vector2D: 'Vector2D', vector2D2: 'Vector2D') -> float: ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two 2D vectors.
        
            If all coordinates of two 2D vectors are exactly the same, and none are :code:`Double.NaN`, the two 2D vectors are
            considered to be equal.
        
            :code:`NaN` coordinates are considered to affect globally the vector and be equals to each other - i.e, if either (or
            all) coordinates of the 2D vector are equal to :code:`Double.NaN`, the 2D vector is equal to
            :meth:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D.NaN`.
        
            Overrides:
                 in class 
        
            Parameters:
                other (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two 2D vector objects are equal, false if object is null, not an instance of Vector2D, or not equal to this
                Vector2D instance
        
        
        """
        ...
    def getAlpha(self) -> float:
        """
            For a given vector, get the angle between vector and X-axis counted in counter-clockwise direction: 0 corresponds to
            Vector2D(1, 0), and increasing values are counter-clockwise.
        
            Returns:
                the angle between vector and X-axis counted in counter-clockwise direction (α) (between -PI and +PI)
        
        
        """
        ...
    def getNorm(self) -> float:
        """
            Get the L :sub:`2` norm for the vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.getNorm` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Returns:
                Euclidean norm for the vector
        
        
        """
        ...
    def getNorm1(self) -> float:
        """
            Get the L :sub:`1` norm for the vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.getNorm1` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Returns:
                L :sub:`1` norm for the vector
        
        
        """
        ...
    def getNormInf(self) -> float:
        """
            Get the L :sub:`∞` norm for the vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.getNormInf` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Returns:
                L :sub:`∞` norm for the vector
        
        
        """
        ...
    def getNormSq(self) -> float:
        """
            Get the square of the norm for the vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.getNormSq` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Returns:
                square of the Euclidean norm for the vector
        
        
        """
        ...
    def getRealVector(self) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Get a RealVector with identical data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.getRealVector` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Returns:
                the RealVector
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.math.linear.RealVector`
        
        
        """
        ...
    def getSpace(self) -> fr.cnes.sirius.patrius.math.geometry.Space:
        """
            Get the space to which the vector belongs.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.getSpace` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Returns:
                containing space
        
        
        """
        ...
    def getX(self) -> float:
        """
            Get the abscissa of the vector.
        
            Returns:
                abscissa of the vector
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D.Vector2D`
        
        
        """
        ...
    def getY(self) -> float:
        """
            Get the ordinate of the vector.
        
            Returns:
                ordinate of the vector
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D.Vector2D`
        
        
        """
        ...
    def getZero(self) -> 'Vector2D':
        """
            Get the null vector of the vectorial space or origin point of the affine space.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.getZero` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Returns:
                null vector of the vectorial space or origin point of the affine space
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the 2D vector.
        
            All NaN values have the same hash code.
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def isInfinite(self) -> bool:
        """
            Returns true if any coordinate of this vector is infinite and none are NaN; false otherwise
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.isInfinite` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Returns:
                true if any coordinate of this vector is infinite and none are NaN; false otherwise
        
        
        """
        ...
    def isNaN(self) -> bool:
        """
            Returns true if any coordinate of this vector is NaN; false otherwise
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.isNaN` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Returns:
                true if any coordinate of this vector is NaN; false otherwise
        
        
        """
        ...
    def negate(self) -> 'Vector2D':
        """
            Get the opposite of the instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.negate` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Returns:
                a new vector which is opposite to the instance
        
        
        """
        ...
    def normalize(self) -> 'Vector2D':
        """
            Get a normalized vector aligned with the instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.normalize` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Returns:
                a new normalized vector
        
        
        """
        ...
    def scalarMultiply(self, double: float) -> 'Vector2D':
        """
            Multiply the instance by a scalar.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.scalarMultiply` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Parameters:
                a (double): scalar
        
            Returns:
                a new vector
        
        
        """
        ...
    @typing.overload
    def subtract(self, double: float, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]) -> 'Vector2D': ...
    @typing.overload
    def subtract(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D]) -> 'Vector2D': ...
    def toArray(self) -> typing.MutableSequence[float]:
        """
            Get the vector coordinates as a dimension 2 array.
        
            Returns:
                vector coordinates
        
            Also see:
        
        
        """
        ...
    @typing.overload
    def toString(self) -> str:
        """
            Get a string representation of this vector.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this vector
        
        """
        ...
    @typing.overload
    def toString(self, numberFormat: java.text.NumberFormat) -> str:
        """
            Get a string representation of this vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Vector.toString` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
        
            Parameters:
                format (`NumberFormat <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>`): the custom format for components
        
            Returns:
                a string representation of this vector
        
        
        """
        ...

class Vector2DFormat(fr.cnes.sirius.patrius.math.geometry.VectorFormat[Euclidean2D]):
    """
    public class Vector2DFormat extends :class:`~fr.cnes.sirius.patrius.math.geometry.VectorFormat`<:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Euclidean2D`>
    
        Formats a 2D vector in components list format "{x; y}".
    
        The prefix and suffix "{" and "}" and the separator "; " can be replaced by any user-defined strings. The number format
        for components can be configured.
    
        White space is ignored at parse time, even if it is in the prefix, suffix or separator specifications. So even if the
        default separator does include a space character that is used at format time, both input string "{1;1}" and " { 1 ; 1 }
        " will be parsed without error and the same vector will be returned. In the second case, however, the parse position
        after parsing will be just after the closing curly brace, i.e. just before the trailing space.
    
        Since:
            3.0
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str, string2: str, string3: str): ...
    @typing.overload
    def __init__(self, string: str, string2: str, string3: str, numberFormat: java.text.NumberFormat): ...
    @typing.overload
    def __init__(self, numberFormat: java.text.NumberFormat): ...
    @typing.overload
    def format(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[fr.cnes.sirius.patrius.math.geometry.Space]) -> str: ...
    @typing.overload
    def format(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[Euclidean2D], stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @typing.overload
    @staticmethod
    def getInstance() -> 'Vector2DFormat':
        """
            Returns the default 2D vector format for the current locale.
        
            Returns:
                the default 2D vector format.
        
        """
        ...
    @typing.overload
    @staticmethod
    def getInstance(locale: java.util.Locale) -> 'Vector2DFormat':
        """
            Returns the default 2D vector format for the given locale.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): the specific locale used by the format.
        
            Returns:
                the 2D vector format specific to the given locale.
        
        
        """
        ...
    @typing.overload
    def parse(self, string: str) -> Vector2D:
        """
            Parses a string to produce a :class:`~fr.cnes.sirius.patrius.math.geometry.Vector` object.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.VectorFormat.parse` in
                class :class:`~fr.cnes.sirius.patrius.math.geometry.VectorFormat`
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
        
            Returns:
                the parsed :class:`~fr.cnes.sirius.patrius.math.geometry.Vector` object.
        
        """
        ...
    @typing.overload
    def parse(self, string: str, parsePosition: java.text.ParsePosition) -> Vector2D:
        """
            Parses a string to produce a :class:`~fr.cnes.sirius.patrius.math.geometry.Vector` object.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.VectorFormat.parse` in
                class :class:`~fr.cnes.sirius.patrius.math.geometry.VectorFormat`
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
                pos (`ParsePosition <http://docs.oracle.com/javase/8/docs/api/java/text/ParsePosition.html?is-external=true>`): input/output parsing parameter.
        
            Returns:
                the parsed :class:`~fr.cnes.sirius.patrius.math.geometry.Vector` object.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.geometry.euclidean.twod")``.

    EnumPolygon: typing.Type[EnumPolygon]
    Euclidean2D: typing.Type[Euclidean2D]
    Line: typing.Type[Line]
    PolygonsSet: typing.Type[PolygonsSet]
    Segment: typing.Type[Segment]
    SubLine: typing.Type[SubLine]
    Vector2D: typing.Type[Vector2D]
    Vector2DFormat: typing.Type[Vector2DFormat]
