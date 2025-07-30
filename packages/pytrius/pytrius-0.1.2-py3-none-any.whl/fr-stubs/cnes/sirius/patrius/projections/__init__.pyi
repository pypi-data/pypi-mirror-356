
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.math.geometry.euclidean.twod
import java.io
import java.lang
import java.util
import jpype
import typing



class EnumLineProperty(java.lang.Enum['EnumLineProperty']):
    STRAIGHT: typing.ClassVar['EnumLineProperty'] = ...
    GREAT_CIRCLE: typing.ClassVar['EnumLineProperty'] = ...
    STRAIGHT_RHUMB_LINE: typing.ClassVar['EnumLineProperty'] = ...
    NONE: typing.ClassVar['EnumLineProperty'] = ...
    def getName(self) -> str: ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'EnumLineProperty': ...
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['EnumLineProperty']: ...

class IProjection(java.io.Serializable):
    """
    public interface IProjection extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for projections on an ellipsoid.
    
        Since:
            3.2
    """
    @typing.overload
    def applyInverseTo(self, double: float, double2: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @typing.overload
    def applyInverseTo(self, double: float, double2: float, double3: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @typing.overload
    def applyTo(self, double: float, double2: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D: ...
    @typing.overload
    def applyTo(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D: ...
    def canMap(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> bool:
        """
            Returns a boolean depending if the ellipsoid point can be map with the selected projection method.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.bodies.EllipsoidPoint`): point to test if representable
        
            Returns:
                true if the ellipsoid point can be represented on the map with the chosen projection method
        
        
        """
        ...
    def getLineProperty(self) -> EnumLineProperty:
        """
            Getter for the line property.
        
            Returns:
                line property
        
        
        """
        ...
    def getMaximumEastingValue(self) -> float:
        """
            Getter for the maximum value for X projected.
        
            Returns:
                the maximum value for X projected
        
        
        """
        ...
    def getMaximumLatitude(self) -> float:
        """
            Getter for the maximum latitude that the projection can map.
        
            Returns:
                the maximum latitude that the projection can map
        
        
        """
        ...
    def getReference(self) -> fr.cnes.sirius.patrius.bodies.BodyShape:
        """
            Getter for the system of reference used.
        
            Returns:
                the system of reference
        
        
        """
        ...
    def isConformal(self) -> bool:
        """
            Inform the user if the direct transformation is a conformal 's one (If yes, it preserves angles).
        
            Returns:
                a boolean
        
        
        """
        ...
    def isEquivalent(self) -> bool:
        """
            Inform the user if the direct transformation is an equivalent 's one (If yes, it preserves surfaces).
        
            Returns:
                a boolean
        
        
        """
        ...

class ProjectionEllipsoidUtils:
    ELLIPSOID_PRECISION: typing.ClassVar[float] = ...
    @staticmethod
    def computeBearing(ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, ellipsoidPoint2: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> float: ...
    @staticmethod
    def computeCenterPointAlongLoxodrome(ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, ellipsoidPoint2: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @staticmethod
    def computeInverseMeridionalDistance(double: float, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid) -> float: ...
    @staticmethod
    def computeInverseRectifyingLatitude(double: float, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid) -> float: ...
    @staticmethod
    def computeLoxodromicDistance(ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, ellipsoidPoint2: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> float: ...
    @staticmethod
    def computeMercatorLatitude(double: float, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid) -> float: ...
    @staticmethod
    def computeMeridionalDistance(double: float, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid) -> float: ...
    @typing.overload
    @staticmethod
    def computeOrthodromicDistance(double: float, double2: float, double3: float, double4: float, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid) -> float: ...
    @typing.overload
    @staticmethod
    def computeOrthodromicDistance(ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, ellipsoidPoint2: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> float: ...
    @staticmethod
    def computePointAlongLoxodrome(ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, double: float, double2: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @staticmethod
    def computePointAlongOrthodrome(ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, double: float, double2: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @staticmethod
    def computeRadiusEastWest(double: float, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid) -> float: ...
    @staticmethod
    def computeSphericalAzimuth(ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, ellipsoidPoint2: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> float: ...
    @staticmethod
    def discretizeGreatCircle(ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, ellipsoidPoint2: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, double: float) -> java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]: ...
    @staticmethod
    def discretizeRhumbLine(ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, ellipsoidPoint2: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, double: float) -> java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]: ...
    @staticmethod
    def getEccentricity(oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid) -> float: ...
    @staticmethod
    def getSeries(oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid) -> typing.MutableSequence[float]: ...

class AbstractProjection(IProjection):
    def __init__(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint): ...
    @typing.overload
    def applyInverseTo(self, double: float, double2: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @typing.overload
    def applyInverseTo(self, double: float, double2: float, double3: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @typing.overload
    def applyInverseTo(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]: ...
    @typing.overload
    def applyInverseTo(self, list: java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]) -> java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]: ...
    @typing.overload
    def applyTo(self, double: float, double2: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D: ...
    @typing.overload
    def applyTo(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D: ...
    @typing.overload
    def applyTo(self, list: java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]) -> java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]: ...
    def applyToAndDiscretize(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, ellipsoidPoint2: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, double: float, boolean: bool) -> java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]: ...
    @staticmethod
    def discretize(vector2D: fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D, vector2D2: fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D, double: float, boolean: bool) -> java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]: ...
    def discretizeAndApplyTo(self, list: java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint], enumLineProperty: EnumLineProperty, double: float) -> java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]: ...
    def discretizeCircleAndApplyTo(self, list: java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint], double: float) -> java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]: ...
    def discretizeRhumbAndApplyTo(self, list: java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint], double: float) -> java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]: ...
    def getDistortionFactor(self, double: float) -> float: ...
    def getPivotPoint(self) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    def getReference(self) -> fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape: ...

class IdentityProjection(AbstractProjection):
    """
    public class IdentityProjection extends :class:`~fr.cnes.sirius.patrius.projections.AbstractProjection`
    
        This is the identity projection defined by
    
    
        :code:`X = Lon Y = Lat`
    
    
    
        The pivot point has a latitude and longitude to 0.
    
        Since:
            3.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape): ...
    @typing.overload
    def applyInverseTo(self, double: float, double2: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint:
        """
            Inverse projection.
        
        
            Returns ellipsoid coordinates.
        
            Parameters:
                x (double): abscissa coordinate
                y (double): ordinate coordinate
        
            Returns:
                ellipsoid coordinates
        
            This is the Two standard parallel Mercator Projection model. The latitude and the longitude of the given point to
            convert can be defined from any natural origin and the user can set the altitude.
        
            Parameters:
                x (double): abscissa coordinate
                y (double): ordinate coordinate
                alt (double): altitude coordinate
        
            Returns:
                coordinate
        
        
        """
        ...
    @typing.overload
    def applyInverseTo(self, double: float, double2: float, double3: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @typing.overload
    def applyInverseTo(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]: ...
    @typing.overload
    def applyInverseTo(self, list: java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]) -> java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]: ...
    @typing.overload
    def applyTo(self, double: float, double2: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D:
        """
            Returns Easting value and Northing value in meters from latitude and longitude coordinates.
        
            Parameters:
                lat (double): latitude of the point to project
                lon (double): longitude of the point to project
        
            Returns:
                Vector2D containing Easting value and Northing value in meters
        
        
        """
        ...
    @typing.overload
    def applyTo(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D:
        """
            Returns Easting value and Northing value in meters from the point coordinates.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.bodies.EllipsoidPoint`): the point to transform
        
            Returns:
                Vector2D containing Easting value and Northing value in meters
        
        """
        ...
    @typing.overload
    def applyTo(self, list: java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]) -> java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]: ...
    def canMap(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> bool:
        """
            Returns a boolean depending if the ellipsoid point can be map with the selected projection method.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.bodies.EllipsoidPoint`): point to test if representable
        
            Returns:
                true if the ellipsoid point can be represented on the map with the chosen projection method
        
        
        """
        ...
    def getDistortionFactor(self, double: float) -> float:
        """
            Getter for the scale factor at a specific latitude.
        
        
            The result is the fraction Mercator distance / real distance.
        
            **WARNING: this method must not be used with the :class:`~fr.cnes.sirius.patrius.projections.IdentityProjection` class :
            it always returns an :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`.**
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.projections.AbstractProjection.getDistortionFactor` in
                class :class:`~fr.cnes.sirius.patrius.projections.AbstractProjection`
        
            Parameters:
                lat (double): latitude
        
            Returns:
                the distortion factor
        
        
        """
        ...
    def getLineProperty(self) -> EnumLineProperty:
        """
            Getter for the line property.
        
            Returns:
                line property
        
        
        """
        ...
    def getMaximumEastingValue(self) -> float:
        """
            Getter for the maximum value for X projected.
        
            Returns:
                the maximum value for X projected
        
        
        """
        ...
    def getMaximumLatitude(self) -> float:
        """
            Getter for the maximum latitude that the projection can map.
        
            Returns:
                the maximum latitude that the projection can map
        
        
        """
        ...
    def isConformal(self) -> bool:
        """
            Inform the user if the direct transformation is a conformal 's one (If yes, it preserves angles).
        
            Returns:
                a boolean
        
        
        """
        ...
    def isEquivalent(self) -> bool:
        """
            Inform the user if the direct transformation is an equivalent 's one (If yes, it preserves surfaces).
        
            Returns:
                a boolean
        
        
        """
        ...

class Mercator(AbstractProjection):
    MAX_LATITUDE: typing.ClassVar[float] = ...
    @typing.overload
    def __init__(self, double: float, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape): ...
    @typing.overload
    def __init__(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, double: float, boolean: bool, boolean2: bool): ...
    @typing.overload
    def applyInverseTo(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]: ...
    @typing.overload
    def applyInverseTo(self, list: java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]) -> java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]: ...
    @typing.overload
    def applyInverseTo(self, double: float, double2: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @typing.overload
    def applyInverseTo(self, double: float, double2: float, double3: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @typing.overload
    def applyTo(self, list: java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]) -> java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]: ...
    @typing.overload
    def applyTo(self, double: float, double2: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D: ...
    @typing.overload
    def applyTo(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D: ...
    def canMap(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> bool: ...
    def getAzimuth(self) -> float: ...
    def getDistortionFactor(self, double: float) -> float: ...
    def getLineProperty(self) -> EnumLineProperty: ...
    def getMaximumEastingValue(self) -> float: ...
    def getMaximumLatitude(self) -> float: ...
    def getMaximumNorthingValue(self) -> float: ...
    def getScaleFactor(self, double: float) -> float: ...
    def isConformal(self) -> bool: ...
    def isEquivalent(self) -> bool: ...

class GeneralizedFlamsteedSamson(Mercator):
    def __init__(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint, double: float): ...
    @typing.overload
    def applyInverseTo(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]: ...
    @typing.overload
    def applyInverseTo(self, list: java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]) -> java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]: ...
    @typing.overload
    def applyInverseTo(self, double: float, double2: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @typing.overload
    def applyInverseTo(self, double: float, double2: float, double3: float) -> fr.cnes.sirius.patrius.bodies.EllipsoidPoint: ...
    @typing.overload
    def applyTo(self, list: java.util.List[fr.cnes.sirius.patrius.bodies.EllipsoidPoint]) -> java.util.List[fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D]: ...
    @typing.overload
    def applyTo(self, double: float, double2: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D: ...
    @typing.overload
    def applyTo(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D: ...
    def getLineProperty(self) -> EnumLineProperty: ...
    def isConformal(self) -> bool: ...
    def isEquivalent(self) -> bool: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.projections")``.

    AbstractProjection: typing.Type[AbstractProjection]
    EnumLineProperty: typing.Type[EnumLineProperty]
    GeneralizedFlamsteedSamson: typing.Type[GeneralizedFlamsteedSamson]
    IProjection: typing.Type[IProjection]
    IdentityProjection: typing.Type[IdentityProjection]
    Mercator: typing.Type[Mercator]
    ProjectionEllipsoidUtils: typing.Type[ProjectionEllipsoidUtils]
