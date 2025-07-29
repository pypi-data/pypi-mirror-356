
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.events.detectors
import fr.cnes.sirius.patrius.fieldsofview
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.frames.transformations
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.stat.descriptive
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import jpype
import typing



class BodyShapeFitter:
    """
    public class BodyShapeFitter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Body shape fitter, allowing to build shapes fitted on the main Shape. The fitting criteria are described in the
        associated methods.
    
        This class offers an optimal internal caching strategy to improve speed, by storing in cache the fitted ellipsoid
        computed. Each of them is thus computed once.
    
        This class implements the interface :class:`~fr.cnes.sirius.patrius.bodies.BodyShape`
    
        Since:
            4.14
    """
    def __init__(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape): ...
    _getEllipsoid__T = typing.TypeVar('_getEllipsoid__T', bound=fr.cnes.sirius.patrius.bodies.AbstractEllipsoidBodyShape)  # <T>
    def getEllipsoid(self, ellipsoidType: 'BodyShapeFitter.EllipsoidType') -> _getEllipsoid__T:
        """
            Getter for the ellipsoid of the desired type. Once computed, the required ellipsoid is stored for future use.
        
            Parameters:
                ellipsoidTypeIn (:class:`~fr.cnes.sirius.patrius.bodies.mesh.BodyShapeFitter.EllipsoidType`): the type of the ellipsoid to be returned
        
            Returns:
                the desired ellipsoid
        
        
        """
        ...
    class EllipsoidType(java.lang.Enum['BodyShapeFitter.EllipsoidType']):
        SPHERE_FITTED: typing.ClassVar['BodyShapeFitter.EllipsoidType'] = ...
        SPHERE_INNER: typing.ClassVar['BodyShapeFitter.EllipsoidType'] = ...
        SPHERE_OUTER: typing.ClassVar['BodyShapeFitter.EllipsoidType'] = ...
        ONE_AXIS_ELLIPSOID_FITTED: typing.ClassVar['BodyShapeFitter.EllipsoidType'] = ...
        ONE_AXIS_ELLIPSOID_INNER: typing.ClassVar['BodyShapeFitter.EllipsoidType'] = ...
        ONE_AXIS_ELLIPSOID_OUTER: typing.ClassVar['BodyShapeFitter.EllipsoidType'] = ...
        THREE_AXIS_ELLIPSOID_FITTED: typing.ClassVar['BodyShapeFitter.EllipsoidType'] = ...
        THREE_AXIS_ELLIPSOID_INNER: typing.ClassVar['BodyShapeFitter.EllipsoidType'] = ...
        THREE_AXIS_ELLIPSOID_OUTER: typing.ClassVar['BodyShapeFitter.EllipsoidType'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'BodyShapeFitter.EllipsoidType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['BodyShapeFitter.EllipsoidType']: ...

class FacetBodyShape(fr.cnes.sirius.patrius.bodies.AbstractBodyShape):
    def __init__(self, string: str, celestialBodyFrame: fr.cnes.sirius.patrius.frames.CelestialBodyFrame, meshProvider: 'MeshProvider'): ...
    @typing.overload
    def buildPoint(self, lLHCoordinatesSystem: fr.cnes.sirius.patrius.bodies.LLHCoordinatesSystem, double: float, double2: float, double3: float, string: str) -> 'FacetPoint': ...
    @typing.overload
    def buildPoint(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, string: str) -> 'FacetPoint': ...
    @typing.overload
    def buildPoint(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, string: str) -> 'FacetPoint': ...
    @typing.overload
    def closestPointTo(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> 'FacetPoint': ...
    @typing.overload
    def closestPointTo(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'FacetPoint': ...
    @typing.overload
    def closestPointTo(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, string: str) -> 'FacetPoint': ...
    @typing.overload
    def closestPointTo(self, line: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line) -> typing.MutableSequence['FacetPoint']: ...
    @typing.overload
    def closestPointTo(self, line: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence['FacetPoint']: ...
    def distanceTo(self, line: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getApparentRadius(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinatesProvider2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, propagationDelayType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType) -> float: ...
    def getEncompassingSphereRadius(self) -> float: ...
    def getFieldData(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, iFieldOfView: fr.cnes.sirius.patrius.fieldsofview.IFieldOfView, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> 'FieldData': ...
    def getIntersection(self, line: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'Intersection': ...
    @typing.overload
    def getIntersectionPoint(self, line: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'FacetPoint': ...
    @typing.overload
    def getIntersectionPoint(self, line: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> 'FacetPoint': ...
    @typing.overload
    def getIntersectionPoint(self, line: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, string: str) -> 'FacetPoint': ...
    def getIntersectionPoints(self, line: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence['FacetPoint']: ...
    def getMaxNorm(self) -> float: ...
    def getMaxSlope(self) -> float: ...
    def getMeshProvider(self) -> 'MeshProvider': ...
    def getMinNorm(self) -> float: ...
    @typing.overload
    def getNeighbors(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint, double: float) -> java.util.List['Triangle']: ...
    @typing.overload
    def getNeighbors(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint, int: int) -> java.util.List['Triangle']: ...
    @typing.overload
    def getNeighbors(self, triangle: 'Triangle', double: float) -> java.util.List['Triangle']: ...
    @typing.overload
    def getNeighbors(self, triangle: 'Triangle', int: int) -> java.util.List['Triangle']: ...
    @typing.overload
    def getNeighbors(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float) -> java.util.List['Triangle']: ...
    @typing.overload
    def getNeighbors(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, int: int) -> java.util.List['Triangle']: ...
    def getNeverEnlightenedTriangles(self, list: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider) -> java.util.List['Triangle']: ...
    def getNeverVisibleTriangles(self, list: java.util.List[fr.cnes.sirius.patrius.propagation.SpacecraftState], iFieldOfView: fr.cnes.sirius.patrius.fieldsofview.IFieldOfView) -> java.util.List['Triangle']: ...
    def getOverPerpendicularSteepFacets(self) -> java.util.List['Triangle']: ...
    def getThreshold(self) -> float: ...
    def getTriangles(self) -> typing.MutableSequence['Triangle']: ...
    def getVisibleAndEnlightenedTriangles(self, list: java.util.List[fr.cnes.sirius.patrius.propagation.SpacecraftState], pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, iFieldOfView: fr.cnes.sirius.patrius.fieldsofview.IFieldOfView) -> java.util.List['Triangle']: ...
    def isDefaultLLHCoordinatesSystem(self) -> bool: ...
    def isInEclipse(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider) -> bool: ...
    def isMasked(self, triangle: 'Triangle', vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool: ...
    def isVisible(self, triangle: 'Triangle', vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, iFieldOfView: fr.cnes.sirius.patrius.fieldsofview.IFieldOfView, transform: fr.cnes.sirius.patrius.frames.transformations.Transform) -> bool: ...
    def resize(self, marginType: fr.cnes.sirius.patrius.bodies.BodyShape.MarginType, double: float) -> 'FacetBodyShape': ...
    def setMaxApparentRadiusSteps(self, int: int) -> None: ...
    def setThreshold(self, double: float) -> None: ...

class FacetBodyShapeStatistics:
    """
    public class FacetBodyShapeStatistics extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class containing statistics methods for the FacetBodyShape object.
    
        Since:
            4.11
    """
    def __init__(self, facetBodyShape: FacetBodyShape): ...
    def computeStatisticsForAltitude(self, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid) -> fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics: ...
    def computeStatisticsForRadialDistance(self, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid) -> fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics: ...

class FacetPoint(fr.cnes.sirius.patrius.bodies.AbstractBodyPoint):
    @typing.overload
    def __init__(self, facetBodyShape: FacetBodyShape, lLHCoordinates: fr.cnes.sirius.patrius.bodies.LLHCoordinates, string: str): ...
    @typing.overload
    def __init__(self, facetBodyShape: FacetBodyShape, lLHCoordinatesSystem: fr.cnes.sirius.patrius.bodies.LLHCoordinatesSystem, double: float, double2: float, double3: float, string: str): ...
    @typing.overload
    def __init__(self, facetBodyShape: FacetBodyShape, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, string: str): ...
    @typing.overload
    def __init__(self, facetBodyShape: FacetBodyShape, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, string: str): ...
    def getBodyShape(self) -> FacetBodyShape: ...
    def getClosestPointOnShape(self) -> 'FacetPoint': ...
    def getClosestTriangles(self) -> java.util.List['Triangle']: ...
    def getRadialProjectionOnShape(self) -> 'FacetPoint': ...
    @typing.overload
    def toString(self) -> str: ...
    @typing.overload
    def toString(self, lLHCoordinatesSystem: fr.cnes.sirius.patrius.bodies.LLHCoordinatesSystem) -> str: ...

class FieldData:
    """
    public class FieldData extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Data container for :class:`~fr.cnes.sirius.patrius.bodies.mesh.FacetBodyShape` field data. Field data are data related
        to a :class:`~fr.cnes.sirius.patrius.bodies.mesh.FacetBodyShape` set of triangles at a given date. In particular given a
        list of visible triangles, it can provides a contour.
    
        Since:
            4.6
    """
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, list: java.util.List['Triangle'], facetBodyShape: FacetBodyShape): ...
    def getContour(self) -> java.util.List[FacetPoint]: ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the date.
        
            Returns:
                the date
        
        
        """
        ...
    def getVisibleSurface(self) -> float:
        """
            Getter for the visible surface. This is the sum of all the visible triangles surface.
        
            Returns:
                the visible surface
        
        
        """
        ...
    def getVisibleTriangles(self) -> java.util.List['Triangle']: ...

class Intersection:
    """
    public class Intersection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Intersection data. An intersection consists in a 3D point and an owning triangle
        :class:`~fr.cnes.sirius.patrius.bodies.mesh.Triangle`.
    
        Since:
            4.6
    """
    def __init__(self, triangle: 'Triangle', vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @staticmethod
    def append(intersectionArray: typing.Union[typing.List['Intersection'], jpype.JArray], intersectionArray2: typing.Union[typing.List['Intersection'], jpype.JArray]) -> typing.MutableSequence['Intersection']:
        """
            Appends two arrays together.
        
            Parameters:
                array1 (:class:`~fr.cnes.sirius.patrius.bodies.mesh.Intersection`[]): first array
                array2 (:class:`~fr.cnes.sirius.patrius.bodies.mesh.Intersection`[]): second array
        
            Returns:
                [array1, array2]
        
        
        """
        ...
    def getPoint(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Returns the intersection point in input frame.
        
            Returns:
                the intersection point in input frame
        
        
        """
        ...
    def getTriangle(self) -> 'Triangle':
        """
            Return the intersecting triangle.
        
            Returns:
                the intersecting triangle
        
        
        """
        ...

class MeshProvider(java.io.Serializable):
    """
    public interface MeshProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Generic mesh provider. This interface represents a mesh provider, i.e. a class which provides the list of
        :class:`~fr.cnes.sirius.patrius.bodies.mesh.Triangle` and :class:`~fr.cnes.sirius.patrius.bodies.mesh.Vertex` of a given
        mesh.
    
        This class is to be used in conjunction with :class:`~fr.cnes.sirius.patrius.bodies.mesh.FacetBodyShape` for body mesh
        loading.
    
        Since:
            4.6
    """
    def getTriangles(self) -> typing.MutableSequence['Triangle']:
        """
            Returns the list of triangles of the mesh.
        
            Returns:
                list of triangles of the mesh
        
        
        """
        ...
    def getVertices(self) -> java.util.Map[int, 'Vertex']: ...

class Triangle(java.io.Serializable):
    """
    public class Triangle extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        3D triangle definition. A triangle contains 3 3D-points or "vertices" (defined by
        :class:`~fr.cnes.sirius.patrius.bodies.mesh.Vertex` class). This class also stores data related to the triangle for
        efficient computation (center, surface, normal vector, neighboring
        :class:`~fr.cnes.sirius.patrius.bodies.mesh.Triangle`).
    
        Since:
            4.6
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int, vertex: 'Vertex', vertex2: 'Vertex', vertex3: 'Vertex'): ...
    @typing.overload
    def closestPointTo(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Computes the points of the triangle and the line realizing the shortest distance.
        
            If the line intersects the triangle, the returned points are identical. Semi-finite lines are handled by this method.
        
            Parameters:
                line (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line`): the line
        
            Returns:
                the two points : first the one from the line, and the one from the shape.
        
            Getter for the closest point of triangle to provided point.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): a point
        
            Returns:
                closest point of triangle to provided point
        
        
        """
        ...
    @typing.overload
    def closestPointTo(self, line: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D]: ...
    def distanceTo(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes minimal distance between provided line and triangle **provided that the line does not cross this triangle**.
        
            This method is package-protected and is not supposed to be used by user. It assumes that the line does not cross this
            triangle.
        
            Parameters:
                line (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line`): line
        
            Returns:
                minimal distance between the provided line and this triangle
        
            Computes distance from triangle to provided.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): point
        
            Returns:
                minimal distance between the provided point and this triangle
        
        
        """
        ...
    @staticmethod
    def dotProduct(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Fast dot product of two 3D vectors.
        
            Parameters:
                v1 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): First vector
                v2 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): Second vector
        
            Returns:
                dot product of two 3D vectors
        
        
        """
        ...
    def getCenter(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the triangle barycenter.
        
            Returns:
                the triangle barycenter
        
        
        """
        ...
    def getID(self) -> int:
        """
            Getter for the triangle identifier.
        
            Returns:
                the triangle identifier
        
        
        """
        ...
    def getIntersection(self, line: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the intersection point with triangle, null if there is no intersection or if line is included in triangle.
        
            Algorithm from article "Fast, Minimum Storage Ray/Triangle Intersection" from Thomas Moller, 1997.
        
            Parameters:
                line (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line`): line of sight (considered infinite)
        
            Returns:
                intersection point with triangle, null if there is no intersection
        
        
        """
        ...
    def getNeighbors(self) -> java.util.List['Triangle']: ...
    def getNormal(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the normal to the triangle.
        
            Returns:
                the normal to the triangle
        
        
        """
        ...
    def getSphereRadius(self) -> float:
        """
            Getter for the encompassing sphere radius squared.
        
            Returns:
                the encompassing sphere radius squared
        
        
        """
        ...
    def getSurface(self) -> float:
        """
            Getter for the triangle surface.
        
            Returns:
                the triangle surface
        
        
        """
        ...
    def getVertices(self) -> typing.MutableSequence['Vertex']:
        """
            Getter for the triangle vertices.
        
            Returns:
                the triangle vertices
        
        
        """
        ...
    def isHandled(self) -> bool:
        """
            Returns a boolean representing triangle status for fast algorithms. This boolean can be set alternatively to true/false.
        
            Returns:
                triangle status
        
        
        """
        ...
    def isNeighborByVertexID(self, triangle: 'Triangle') -> bool:
        """
            Returns true if provided triangle is a neighbor by checking their vertices ID (i.e. has 2 identical vertex ID).
        
            Parameters:
                triangle (:class:`~fr.cnes.sirius.patrius.bodies.mesh.Triangle`): a triangle
        
            Returns:
                true if provided triangle is a neighbor by checking their vertices ID (i.e. has 2 identical vertex ID)
        
        
        """
        ...
    def isVisible(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool:
        """
            Returns true if the triangle is visible from the provided position (culling test).
        
            Parameters:
                position (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): position
        
            Returns:
                true if the triangle is visible
        
        
        """
        ...
    def pointInTriangle(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool:
        """
            Check if the projection on triangle's plane of a point of space belongs to the triangle.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): a point of space
        
            Returns:
                true if the point's projection belongs to the triangle, false otherwise
        
        
        """
        ...
    def setHandled(self, boolean: bool) -> None:
        """
            Set a boolean representing triangle status for fast algorithms. This boolean can be set alternatively to true/false.
        
            Parameters:
                handled (boolean): status to set
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class Vertex(java.io.Serializable):
    """
    public class Vertex extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        3D vertex definition. A vertex is a 3D point. For efficient computation, this class also stores the list of
        :class:`~fr.cnes.sirius.patrius.bodies.mesh.Triangle` "owning" the vertex.
    
        Since:
            4.6
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    def getID(self) -> int:
        """
            Returns the vertex identifier.
        
            Returns:
                the vertex identifier
        
        
        """
        ...
    def getNeighbors(self) -> java.util.List[Triangle]: ...
    def getPosition(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Returns the vertex 3D position.
        
            Returns:
                the vertex 3D position
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class EllipsoidMeshLoader(MeshProvider):
    def __init__(self, string: str): ...
    def getTriangles(self) -> typing.MutableSequence[Triangle]: ...
    def getVertices(self) -> java.util.Map[int, Vertex]: ...
    def toObjFile(self, string: str) -> None: ...

class ObjMeshLoader(MeshProvider):
    """
    public class ObjMeshLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.bodies.mesh.MeshProvider`
    
        .obj format mesh loader. .obj format is defined here: https://fr.wikipedia.org/wiki/Objet_3D_(format_de_fichier).
    
        Read data is considered to be in km.
    
        This readers reads only "vertex" lines (starting with 'v' character) and "facet" lines (starting with 'f' character)
    
        Since:
            4.6
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str): ...
    def getName(self) -> str:
        """
            Getter for the name of the loaded object.
        
            Returns:
                the name of the object (may be null)
        
        
        """
        ...
    def getTriangles(self) -> typing.MutableSequence[Triangle]:
        """
            Returns the list of triangles of the mesh.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.bodies.mesh.MeshProvider.getTriangles` in
                interface :class:`~fr.cnes.sirius.patrius.bodies.mesh.MeshProvider`
        
            Returns:
                list of triangles of the mesh
        
        
        """
        ...
    def getVertices(self) -> java.util.Map[int, Vertex]: ...
    class DataType(java.lang.Enum['ObjMeshLoader.DataType']):
        NAME: typing.ClassVar['ObjMeshLoader.DataType'] = ...
        VERTEX: typing.ClassVar['ObjMeshLoader.DataType'] = ...
        TEXTURE: typing.ClassVar['ObjMeshLoader.DataType'] = ...
        NORMAL: typing.ClassVar['ObjMeshLoader.DataType'] = ...
        FACE: typing.ClassVar['ObjMeshLoader.DataType'] = ...
        COMMENT: typing.ClassVar['ObjMeshLoader.DataType'] = ...
        GROUP: typing.ClassVar['ObjMeshLoader.DataType'] = ...
        OTHER: typing.ClassVar['ObjMeshLoader.DataType'] = ...
        @staticmethod
        def getDataType(string: str) -> 'ObjMeshLoader.DataType': ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'ObjMeshLoader.DataType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['ObjMeshLoader.DataType']: ...

class StarConvexFacetBodyShape(FacetBodyShape, fr.cnes.sirius.patrius.bodies.StarConvexBodyShape):
    """
    public class StarConvexFacetBodyShape extends :class:`~fr.cnes.sirius.patrius.bodies.mesh.FacetBodyShape` implements :class:`~fr.cnes.sirius.patrius.bodies.StarConvexBodyShape`
    
        Star-convex facet body shape defined by a list of facets. A facet is a 3D triangle defined in the body frame.
    
        This class extends the class :class:`~fr.cnes.sirius.patrius.bodies.mesh.FacetBodyShape` and implements the interface
        :class:`~fr.cnes.sirius.patrius.bodies.StarConvexBodyShape`.
    
        Since:
            4.11
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str, celestialBodyFrame: fr.cnes.sirius.patrius.frames.CelestialBodyFrame, meshProvider: MeshProvider): ...
    def resize(self, marginType: fr.cnes.sirius.patrius.bodies.BodyShape.MarginType, double: float) -> 'StarConvexFacetBodyShape':
        """
            Resize the geometric body shape by a margin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.bodies.BodyShape.resize` in interface :class:`~fr.cnes.sirius.patrius.bodies.BodyShape`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.bodies.mesh.FacetBodyShape.resize` in
                class :class:`~fr.cnes.sirius.patrius.bodies.mesh.FacetBodyShape`
        
            Parameters:
                marginType (:class:`~fr.cnes.sirius.patrius.bodies.BodyShape.MarginType`): margin type to be used
                marginValue (double): margin value to be used (in meters if the margin type is DISTANCE)
        
            Returns:
                resized geometric body shape with the margin
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.bodies.mesh")``.

    BodyShapeFitter: typing.Type[BodyShapeFitter]
    EllipsoidMeshLoader: typing.Type[EllipsoidMeshLoader]
    FacetBodyShape: typing.Type[FacetBodyShape]
    FacetBodyShapeStatistics: typing.Type[FacetBodyShapeStatistics]
    FacetPoint: typing.Type[FacetPoint]
    FieldData: typing.Type[FieldData]
    Intersection: typing.Type[Intersection]
    MeshProvider: typing.Type[MeshProvider]
    ObjMeshLoader: typing.Type[ObjMeshLoader]
    StarConvexFacetBodyShape: typing.Type[StarConvexFacetBodyShape]
    Triangle: typing.Type[Triangle]
    Vertex: typing.Type[Vertex]
