
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.analysis.solver
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.signalpropagation
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import typing



class IDirection(java.io.Serializable):
    """
    public interface IDirection extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This is the main interface for directions.
    
        Since:
            1.1
    """
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class LightAberrationTransformation:
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, signalDirection: 'ITargetDirection.SignalDirection'): ...
    @typing.overload
    def __init__(self, vacuumSignalPropagation: fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation, signalDirection: 'ITargetDirection.SignalDirection'): ...
    @staticmethod
    def applyTo(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, signalDirection: 'ITargetDirection.SignalDirection') -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @staticmethod
    def computeAberrationAngle(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float: ...
    def getAberrationAngle(self) -> float: ...
    def getSignalDirection(self) -> 'ITargetDirection.SignalDirection': ...
    def getTransformedToTargetDirection(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class CelestialBodyPolesAxisDirection(IDirection):
    """
    public final class CelestialBodyPolesAxisDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`
    
        This direction is the axis defined by the two poles of a celestial body.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, celestialBody: fr.cnes.sirius.patrius.bodies.CelestialBody): ...
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class ConstantVectorDirection(IDirection):
    """
    public final class ConstantVectorDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`
    
        Direction described only by a vector constant in a frame
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
        
            Returns:
                the frame
        
        
        """
        ...
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class CrossProductDirection(IDirection):
    """
    public class CrossProductDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`
    
        This direction is the cross product of two directions
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, iDirection: IDirection, iDirection2: IDirection): ...
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class GlintApproximatePointingDirection(IDirection):
    """
    public final class GlintApproximatePointingDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`
    
    
        "Glint" direction pointing. It provides methods to compute Glint point G coordinates and to create a vector/line between
        a point and G.
    
        Glint point is the point of Sun reflexion on a body shape (the Earth for instance) as seen from a spacecraft.
    
        Light speed is currently never taken into account.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    @typing.overload
    def __init__(self, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, univariateSolver: fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver): ...
    def getGlintVectorPosition(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class GroundVelocityDirection(IDirection):
    """
    public class GroundVelocityDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`
    
        Ground velocity direction. This direction depends on the location of the target point on the ground surface and
        therefore it depends on the pointing direction and the body shape. The intersection between the pointing direction and
        the body shape defines the target point.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, iDirection: IDirection): ...
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class ITargetDirection(IDirection):
    """
    public interface ITargetDirection extends :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`
    
        This interface extends Directions for the directions described by a target point.
    
        Since:
            1.1
    
        Also see:
            :meth:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection.getVector`
    """
    @typing.overload
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    @typing.overload
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, signalDirection: 'ITargetDirection.SignalDirection', aberrationCorrection: 'ITargetDirection.AberrationCorrection', absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fixedDate: fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagationModel.FixedDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getTargetPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getTargetPvProvider(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Provides the :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider` associated to the target
            object.
        
            Returns:
                the PV coordinates provider of the target
        
        
        """
        ...
    @typing.overload
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, signalDirection: 'ITargetDirection.SignalDirection', aberrationCorrection: 'ITargetDirection.AberrationCorrection', absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fixedDate: fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagationModel.FixedDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    class AberrationCorrection(java.lang.Enum['ITargetDirection.AberrationCorrection']):
        NONE: typing.ClassVar['ITargetDirection.AberrationCorrection'] = ...
        LIGHT_TIME: typing.ClassVar['ITargetDirection.AberrationCorrection'] = ...
        STELLAR: typing.ClassVar['ITargetDirection.AberrationCorrection'] = ...
        ALL: typing.ClassVar['ITargetDirection.AberrationCorrection'] = ...
        def hasLightTime(self) -> bool: ...
        def hasStellarAberration(self) -> bool: ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'ITargetDirection.AberrationCorrection': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['ITargetDirection.AberrationCorrection']: ...
    class SignalDirection(java.lang.Enum['ITargetDirection.SignalDirection']):
        FROM_TARGET: typing.ClassVar['ITargetDirection.SignalDirection'] = ...
        TOWARD_TARGET: typing.ClassVar['ITargetDirection.SignalDirection'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'ITargetDirection.SignalDirection': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['ITargetDirection.SignalDirection']: ...

class MomentumDirection(IDirection):
    """
    public final class MomentumDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`
    
        Direction described either:
    
          - By a celestial body (the reference body of the orbit). For a given PVCoordinatesProvider origin point the associated
            vector is the normalised cross product of the position to the celestial body and the velocity (momentum vector).
          - By a :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`. In this case the momentum direction is
            simply the cross product between the position and the velocity of the
            :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider` at the required date.
    
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class NadirDirection(IDirection):
    """
    public final class NadirDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`
    
        Nadir direction. This direction depends on the body shape and the satellite position.
    
        This class is restricted to be used with :class:`~fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape`.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape): ...
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class NorthNormalToEclipticDirection(IDirection):
    """
    public class NorthNormalToEclipticDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`
    
        Direction towards normal of ecliptic plane as computed in GCRF.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class VelocityDirection(IDirection):
    """
    public final class VelocityDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`
    
        Direction defined for any PVCoordinatesProvider origin by its velocity vector, expressed in a reference frame (parameter
        of the constructor). The vector is then only projected in the input frame of the getVector or getLine methods.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class EarthCenterDirection(ITargetDirection):
    """
    public class EarthCenterDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection`
    
        Direction to Earth body center : the central body's center is the target point. This direction is directed toward GCRF
        frame origin (i.e. Earth center).
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, signalDirection: ITargetDirection.SignalDirection, aberrationCorrection: ITargetDirection.AberrationCorrection, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fixedDate: fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagationModel.FixedDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    @typing.overload
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getTargetPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getTargetPvProvider(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Provides the :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider` associated to the target
            object.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection.getTargetPvProvider` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection`
        
            Returns:
                the PV coordinates provider of the target
        
        
        """
        ...
    @typing.overload
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, signalDirection: ITargetDirection.SignalDirection, aberrationCorrection: ITargetDirection.AberrationCorrection, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fixedDate: fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagationModel.FixedDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class EarthToCelestialPointDirection(ITargetDirection):
    """
    public class EarthToCelestialPointDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection`
    
        Direction from Earth center to celestial point : the celestial point is the target point.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, celestialPoint: fr.cnes.sirius.patrius.bodies.CelestialPoint): ...
    @typing.overload
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, signalDirection: ITargetDirection.SignalDirection, aberrationCorrection: ITargetDirection.AberrationCorrection, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fixedDate: fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagationModel.FixedDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    @typing.overload
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getTargetPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getTargetPvProvider(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Provides the :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider` associated to the target
            object.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection.getTargetPvProvider` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection`
        
            Returns:
                the PV coordinates provider of the target
        
        
        """
        ...
    @typing.overload
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, signalDirection: ITargetDirection.SignalDirection, aberrationCorrection: ITargetDirection.AberrationCorrection, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fixedDate: fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagationModel.FixedDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class GenericTargetDirection(ITargetDirection):
    """
    public class GenericTargetDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection`
    
        Direction described by a target PVCoordinatesProvider. The vector is at any date computed from the given PVCoordinate
        origin to the target.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    @typing.overload
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, signalDirection: ITargetDirection.SignalDirection, aberrationCorrection: ITargetDirection.AberrationCorrection, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fixedDate: fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagationModel.FixedDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    @typing.overload
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getTargetPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getTargetPvProvider(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Provides the :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider` associated to the target
            object.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection.getTargetPvProvider` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection`
        
            Returns:
                the PV coordinates provider of the target
        
        
        """
        ...
    @typing.overload
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, signalDirection: ITargetDirection.SignalDirection, aberrationCorrection: ITargetDirection.AberrationCorrection, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fixedDate: fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagationModel.FixedDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class ToCelestialPointDirection(ITargetDirection):
    """
    public final class ToCelestialPointDirection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection`
    
        Direction described by a celestial point: the celestial point is the target point.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, celestialPoint: fr.cnes.sirius.patrius.bodies.CelestialPoint): ...
    @typing.overload
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, signalDirection: ITargetDirection.SignalDirection, aberrationCorrection: ITargetDirection.AberrationCorrection, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fixedDate: fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagationModel.FixedDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    @typing.overload
    def getLine(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    def getTargetPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getTargetPvProvider(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Provides the :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider` associated to the target
            object.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection.getTargetPvProvider` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.directions.ITargetDirection`
        
            Returns:
                the PV coordinates provider of the target
        
        
        """
        ...
    @typing.overload
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, signalDirection: ITargetDirection.SignalDirection, aberrationCorrection: ITargetDirection.AberrationCorrection, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fixedDate: fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagationModel.FixedDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getVector(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class BodyPointTargetDirection(GenericTargetDirection):
    """
    public class BodyPointTargetDirection extends :class:`~fr.cnes.sirius.patrius.attitudes.directions.GenericTargetDirection`
    
        This class extends the :class:`~fr.cnes.sirius.patrius.attitudes.directions.GenericTargetDirection` to create a
        direction with a target which is a :class:`~fr.cnes.sirius.patrius.bodies.BodyPoint`.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.attitudes.directions")``.

    BodyPointTargetDirection: typing.Type[BodyPointTargetDirection]
    CelestialBodyPolesAxisDirection: typing.Type[CelestialBodyPolesAxisDirection]
    ConstantVectorDirection: typing.Type[ConstantVectorDirection]
    CrossProductDirection: typing.Type[CrossProductDirection]
    EarthCenterDirection: typing.Type[EarthCenterDirection]
    EarthToCelestialPointDirection: typing.Type[EarthToCelestialPointDirection]
    GenericTargetDirection: typing.Type[GenericTargetDirection]
    GlintApproximatePointingDirection: typing.Type[GlintApproximatePointingDirection]
    GroundVelocityDirection: typing.Type[GroundVelocityDirection]
    IDirection: typing.Type[IDirection]
    ITargetDirection: typing.Type[ITargetDirection]
    LightAberrationTransformation: typing.Type[LightAberrationTransformation]
    MomentumDirection: typing.Type[MomentumDirection]
    NadirDirection: typing.Type[NadirDirection]
    NorthNormalToEclipticDirection: typing.Type[NorthNormalToEclipticDirection]
    ToCelestialPointDirection: typing.Type[ToCelestialPointDirection]
    VelocityDirection: typing.Type[VelocityDirection]
