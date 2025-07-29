
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes.directions
import fr.cnes.sirius.patrius.attitudes.kinematics
import fr.cnes.sirius.patrius.attitudes.multi
import fr.cnes.sirius.patrius.attitudes.orientations
import fr.cnes.sirius.patrius.attitudes.profiles
import fr.cnes.sirius.patrius.attitudes.slew
import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.frames.configuration
import fr.cnes.sirius.patrius.frames.transformations
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.math.util
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.time
import fr.cnes.sirius.patrius.utils
import fr.cnes.sirius.patrius.utils.legs
import java.io
import java.lang
import java.util
import jpype
import typing



class AbstractAttitudeEphemerisGenerator:
    """
    public abstract class AbstractAttitudeEphemerisGenerator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This abstract class handles the generation of attitude ephemeris from an attitude laws sequence
        :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`.
    
    
        The ephemeris generation can be done using a fixed time step or a variable time step, setting the generation time
        interval (the default value is the time interval of the sequence), and the treatment to apply to the transition points
        of the sequence (ignore them, compute the attitude of the initial date of the laws, compute the attitude of the initial
        and final date of the laws).
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.FixedStepAttitudeEphemerisGenerator`,
            :class:`~fr.cnes.sirius.patrius.attitudes.VariableStepAttitudeEphemerisGenerator`
    """
    START_TRANSITIONS: typing.ClassVar[int] = ...
    """
    public static final int START_TRANSITIONS
    
        The start date of the laws are computed.
    
        Also see:
            :meth:`~constant`
    
    
    """
    START_END_TRANSITIONS: typing.ClassVar[int] = ...
    """
    public static final int START_END_TRANSITIONS
    
        The start and the end point of the laws are computed.
    
        Also see:
            :meth:`~constant`
    
    
    """
    NO_TRANSITIONS: typing.ClassVar[int] = ...
    """
    public static final int NO_TRANSITIONS
    
        The transition points are ignored.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self, strictAttitudeLegsSequence: 'StrictAttitudeLegsSequence'['AttitudeLeg'], int: int, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    @typing.overload
    def generateEphemeris(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> java.util.SortedSet['Attitude']: ...
    @typing.overload
    def generateEphemeris(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, frame: fr.cnes.sirius.patrius.frames.Frame) -> java.util.SortedSet['Attitude']: ...
    def getPreviousAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> 'Attitude': ...

class Attitude(fr.cnes.sirius.patrius.time.TimeStamped, fr.cnes.sirius.patrius.time.TimeShiftable['Attitude'], fr.cnes.sirius.patrius.time.TimeInterpolable['Attitude'], java.lang.Comparable['Attitude'], java.io.Serializable):
    """
    public class Attitude extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, :class:`~fr.cnes.sirius.patrius.time.TimeShiftable`<:class:`~fr.cnes.sirius.patrius.attitudes.Attitude`>, :class:`~fr.cnes.sirius.patrius.time.TimeInterpolable`<:class:`~fr.cnes.sirius.patrius.attitudes.Attitude`>, `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.attitudes.Attitude`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class handles attitude definition at a given date.
    
        This class represents the rotation from a reference frame to a "frame of interest", as well as its spin (axis and
        rotation rate).
    
        The angular coordinates describe the orientation and angular velocity of the frame of interest in the reference frame.
    
        Consequently, defining xSat_Rsat = Vector3D.PLUS_I, one can compute xSat_Rref = rot.applyTo(xSat_Rsat).
    
        The state can be slightly shifted to close dates. This shift is based on a linear extrapolation for attitude taking the
        spin rate into account. It is *not* intended as a replacement for proper attitude propagation but should be sufficient
        for either small time shifts or coarse accuracy.
    
        The instance :code:`Attitude` is guaranteed to be immutable.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.orbits.Orbit`, :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`,
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, timeStampedAngularCoordinates: fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, angularCoordinates: fr.cnes.sirius.patrius.utils.AngularCoordinates): ...
    def compareTo(self, attitude: 'Attitude') -> int:
        """
            Compare this attitude with another attitude.
        
            The attitudes are compared with respect to their dates, by chronological order.
        
        
            If they are defined at the same date, they are then compared with respect to their hashCode.
        
        
            This hashCode comparison is arbitrary but allows to be compliant with the equals method, i.e. this method returns 0 only
            if the attitudes are equal.
        
            Specified by:
                 in interface 
        
            Parameters:
                attitude (:class:`~fr.cnes.sirius.patrius.attitudes.Attitude`): other attitude to compare the instance to
        
            Returns:
        
                  - a negative integer: when this attitude is before, or simultaneous with a lower hashCode
                  - zero: when this attitude is simultaneous and with the same hashCode
                  - a positive integer: when this attitude is after, or simultaneous with a higher hashCode
        
        
            Raises:
                : if the two compared attitudes have the same date, the same hashCode, but aren't equal (very unlikely situation)
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date of attitude parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                date of the attitude parameters
        
        
        """
        ...
    def getOrientation(self) -> fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates:
        """
            Get the complete orientation including spin and spin derivatives.
        
            Returns:
                complete orientation including spin and spin derivatives
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.attitudes.Attitude.getRotation`,
                :meth:`~fr.cnes.sirius.patrius.attitudes.Attitude.getSpin`,
                :meth:`~fr.cnes.sirius.patrius.attitudes.Attitude.getRotationAcceleration`
        
        
        """
        ...
    def getReferenceFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the reference frame.
        
            Returns:
                referenceFrame reference frame from which attitude is defined.
        
        
        """
        ...
    def getRotation(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation:
        """
            Get the attitude rotation.
        
            Returns:
                attitude satellite rotation from reference frame.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.attitudes.Attitude.getOrientation`,
                :meth:`~fr.cnes.sirius.patrius.attitudes.Attitude.getSpin`
        
        
        """
        ...
    def getRotationAcceleration(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getSpin(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the satellite spin.
        
            The spin vector is defined in **satellite** frame.
        
            Returns:
                spin satellite spin (axis and velocity).
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.attitudes.Attitude.getOrientation`,
                :meth:`~fr.cnes.sirius.patrius.attitudes.Attitude.getRotation`
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @typing.overload
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection['Attitude'], typing.Sequence['Attitude'], typing.Set['Attitude']]) -> 'Attitude': ...
    @typing.overload
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection['Attitude'], typing.Sequence['Attitude'], typing.Set['Attitude']], boolean: bool) -> 'Attitude': ...
    @typing.overload
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection['Attitude'], typing.Sequence['Attitude'], typing.Set['Attitude']], boolean: bool, angularDerivativesFilter: fr.cnes.sirius.patrius.utils.AngularDerivativesFilter) -> 'Attitude': ...
    @typing.overload
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection['Attitude'], typing.Sequence['Attitude'], typing.Set['Attitude']], angularDerivativesFilter: fr.cnes.sirius.patrius.utils.AngularDerivativesFilter) -> 'Attitude': ...
    def mapAttitudeToArray(self) -> typing.MutableSequence[float]:
        """
            Convert Attitude to state array.
        
            Returns:
                the state vector representing the Attitude.
        
        
        """
        ...
    def shiftedBy(self, double: float) -> 'Attitude':
        """
            Get a time-shifted attitude.
        
            The state can be slightly shifted to close dates. This shift is based on a linear extrapolation for attitude taking the
            spin rate into account. It is *not* intended as a replacement for proper attitude propagation but should be sufficient
            for either small time shifts or coarse accuracy. This method does not take into account the derivatives of spin: the new
            attitude does not contain the spin derivatives.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeShiftable.shiftedBy` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeShiftable`
        
            Parameters:
                dt (double): time shift in seconds
        
            Returns:
                a new attitude, shifted with respect to the instance (which is immutable)
        
        
        """
        ...
    @staticmethod
    def slerp(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, attitude: 'Attitude', attitude2: 'Attitude', frame: fr.cnes.sirius.patrius.frames.Frame, boolean: bool) -> 'Attitude': ...
    @typing.overload
    def withReferenceFrame(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> 'Attitude': ...
    @typing.overload
    def withReferenceFrame(self, frame: fr.cnes.sirius.patrius.frames.Frame, boolean: bool) -> 'Attitude': ...

class AttitudeChronologicalComparator(java.util.Comparator[Attitude], java.io.Serializable):
    """
    public final class AttitudeChronologicalComparator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Comparator <http://docs.oracle.com/javase/8/docs/api/java/util/Comparator.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.attitudes.Attitude`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class is a comparator used to compare the Attitude objects in the ephemeris set. This comparators allows two
        identical attitudes ephemeris to be kept in the set; this feature is important to compute two ephemeris at the attitude
        transition points.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeEphemerisGenerator`, :meth:`~serialized`
    """
    def __init__(self): ...
    def compare(self, attitude: Attitude, attitude2: Attitude) -> int:
        """
            Compare two Attitude instances.
        
            Specified by:
                 in interface 
        
            Parameters:
                o1 (:class:`~fr.cnes.sirius.patrius.attitudes.Attitude`): first Attitude instance
                o2 (:class:`~fr.cnes.sirius.patrius.attitudes.Attitude`): second Attitude instance
        
            Returns:
                a negative integer or a positive integer as the first instance is before or after the second one. If the two instances
                are simultaneous, returns 1 (to avoid deleting attitude instances in the ephemeris set).
        
        
        """
        ...

class AttitudeFrame(fr.cnes.sirius.patrius.frames.Frame):
    """
    public class AttitudeFrame extends :class:`~fr.cnes.sirius.patrius.frames.Frame`
    
        This class is a special implementation of the :class:`~fr.cnes.sirius.patrius.frames.Frame` class; it represents a
        dynamic spacecraft frame, i.e. a dynamic frame whose orientation is defined by an attitude provider.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeTransformProvider`, :meth:`~serialized`
    """
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, attitudeProvider: 'AttitudeProvider', frame: fr.cnes.sirius.patrius.frames.Frame): ...
    def getAttitudeProvider(self) -> 'AttitudeProvider':
        """
            Gets the attitude provider defining the orientation of the frame.
        
            Returns:
                the attitude provider defining the orientation of the frame.
        
        
        """
        ...

class AttitudeProvider(java.io.Serializable):
    """
    public interface AttitudeProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface represents an attitude provider model set.
    
        An attitude provider provides a way to compute an :class:`~fr.cnes.sirius.patrius.attitudes.Attitude` from an date and
        position-velocity local provider.
    """
    def computeSpinByFD(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeSpinDerivativeByFD(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...

class AttitudeTransformProvider(fr.cnes.sirius.patrius.frames.transformations.TransformProvider):
    """
    public class AttitudeTransformProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        This class is a :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider` for
        :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeFrame`; it provides, for a given date, the transformation
        corresponding to the spacecraft reference frame orientation with respect to the parent frame.
    
        Spin derivative is computed when required and correspond to spin derivative of underlying attitude provider.
    
        Frames configuration is unused.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeFrame`, :meth:`~serialized`
    """
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...

class IOrientationLaw(java.io.Serializable):
    """
    public interface IOrientationLaw extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface represents an orientation law, i.e. a law providing an orientation at a given date with respect to a
        given frame.
    
        Since:
            1.1
    """
    def getOrientation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation: ...

class OrientationFrame(fr.cnes.sirius.patrius.frames.Frame):
    """
    public class OrientationFrame extends :class:`~fr.cnes.sirius.patrius.frames.Frame`
    
        This class is a special implementation of the :class:`~fr.cnes.sirius.patrius.frames.Frame` class; it represents a
        dynamic orientation frame, i.e. a dynamic frame whose orientation is defined by
        :class:`~fr.cnes.sirius.patrius.attitudes.IOrientationLaw`.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.OrientationTransformProvider`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, iOrientationLaw: typing.Union[IOrientationLaw, typing.Callable], attitudeFrame: AttitudeFrame): ...
    @typing.overload
    def __init__(self, iOrientationLaw: typing.Union[IOrientationLaw, typing.Callable], attitudeFrame: AttitudeFrame, double: float): ...
    @typing.overload
    def __init__(self, iOrientationLaw: typing.Union[IOrientationLaw, typing.Callable], orientationFrame: 'OrientationFrame'): ...
    @typing.overload
    def __init__(self, iOrientationLaw: typing.Union[IOrientationLaw, typing.Callable], orientationFrame: 'OrientationFrame', double: float): ...

class OrientationTransformProvider(fr.cnes.sirius.patrius.frames.transformations.TransformProvider):
    """
    public class OrientationTransformProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        This class is a :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider` for
        :class:`~fr.cnes.sirius.patrius.attitudes.OrientationFrame`; it provides, for a given date, the transformation
        corresponding to the frame orientation with respect to the parent frame.
    
        Spin derivative is never computed and is either 0 or null. No analytical formula is available for spin derivative. Spin
        is already computed by finite differences.
    
        Frames configuration is unused.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.OrientationFrame`, :meth:`~serialized`
    """
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...

class AttitudeLaw(AttitudeProvider):
    """
    public interface AttitudeLaw extends :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
    
        This interface has been created to represent a generic attitude provider without an interval of validity: the attitude
        can be computed at any date.
    
        Since:
            1.3
    """
    ...

class AttitudeLeg(fr.cnes.sirius.patrius.utils.legs.Leg, AttitudeProvider):
    """
    public interface AttitudeLeg extends :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`, :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
    
        Interface for all *attitude legs*: :class:`~fr.cnes.sirius.patrius.utils.legs.Leg` and
        :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`.
    
        Since:
            4.7
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`, :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
    """
    LEG_NATURE: typing.ClassVar[str] = ...
    """
    static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` LEG_NATURE
    
        Default nature for attitude legs.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def computeSpinByFD(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeSpinDerivativeByFD(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'AttitudeLeg':
        """
            Creates a new leg from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...

class DirectionTrackingOrientation(IOrientationLaw):
    """
    public final class DirectionTrackingOrientation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.IOrientationLaw`
    
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, iDirection: fr.cnes.sirius.patrius.attitudes.directions.IDirection, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    def getOrientation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation: ...

class FixedStepAttitudeEphemerisGenerator(AbstractAttitudeEphemerisGenerator):
    """
    public final class FixedStepAttitudeEphemerisGenerator extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeEphemerisGenerator`
    
        This class handles the generation of attitude ephemeris from an attitude laws sequence
        :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`, using a fixed time step.
    
    
        The ephemeris generation can be done setting the generation time interval (the default value is the time interval of the
        sequence), and the treatment to apply to the transition points of the sequence (ignore them, compute the attitude of the
        initial date of the laws, compute the attitude of the initial and final date of the laws).
    
        Since:
            1.3
    """
    @typing.overload
    def __init__(self, strictAttitudeLegsSequence: 'StrictAttitudeLegsSequence', double: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    @typing.overload
    def __init__(self, strictAttitudeLegsSequence: 'StrictAttitudeLegsSequence', double: float, int: int, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...

_StrictAttitudeLegsSequence__L = typing.TypeVar('_StrictAttitudeLegsSequence__L', bound=AttitudeLeg)  # <L>
class StrictAttitudeLegsSequence(fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence[_StrictAttitudeLegsSequence__L], AttitudeProvider, typing.Generic[_StrictAttitudeLegsSequence__L]):
    """
    public class StrictAttitudeLegsSequence<L extends :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`> extends :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`<L> implements :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
    
        A “base” implementation of an *attitude legs sequence*. This implementation has strict legs which means legs cannot
        be simultaneous or overlap and are strictly ordered by starting date.
    
        Since:
            4.7
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`, :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'StrictAttitudeLegsSequence'[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'StrictAttitudeLegsSequence'[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def copy(self) -> fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'StrictAttitudeLegsSequence'[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'StrictAttitudeLegsSequence'[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def head(self, l: _StrictAttitudeLegsSequence__L) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[_StrictAttitudeLegsSequence__L]: ...
    def isSpinDerivativesComputation(self) -> bool:
        """
            Returns the spin derivatives computation flag.
        
            Returns:
                the spin derivatives computation flag
        
        
        """
        ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Parameters:
                computeSpinDerivativesIn (boolean): true if spin derivatives should be computed
        
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'StrictAttitudeLegsSequence'[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'StrictAttitudeLegsSequence'[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'StrictAttitudeLegsSequence'[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'StrictAttitudeLegsSequence'[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def sub(self, l: _StrictAttitudeLegsSequence__L, l2: _StrictAttitudeLegsSequence__L) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'StrictAttitudeLegsSequence'[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'StrictAttitudeLegsSequence'[_StrictAttitudeLegsSequence__L]: ...
    @typing.overload
    def tail(self, l: _StrictAttitudeLegsSequence__L) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[_StrictAttitudeLegsSequence__L]: ...

class VariableStepAttitudeEphemerisGenerator(AbstractAttitudeEphemerisGenerator):
    """
    public class VariableStepAttitudeEphemerisGenerator extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeEphemerisGenerator`
    
        This class handles the generation of attitude ephemeris from an attitude laws sequence
        :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`, using a variable time step.
    
    
        The ephemeris generation can be done setting the generation time interval (the default value is the time interval of the
        sequence), and the treatment to apply to the transition points of the sequence (ignore them, compute the attitude of the
        initial date of the laws, compute the attitude of the initial and final date of the laws).
    
        Since:
            1.3
    """
    @typing.overload
    def __init__(self, strictAttitudeLegsSequence: StrictAttitudeLegsSequence[AttitudeLeg], double: float, double2: float, double3: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    @typing.overload
    def __init__(self, strictAttitudeLegsSequence: StrictAttitudeLegsSequence[AttitudeLeg], double: float, double2: float, double3: float, int: int, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...

class AbstractAttitudeLaw(AttitudeLaw):
    """
    public abstract class AbstractAttitudeLaw extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLaw`
    
        This abstract class gather all common features to classes implementing the
        :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLaw` interface.
    
    
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getSpinDerivativesComputation(self) -> bool:
        """
            Get the value of the flag indicating if spin derivation computation is activated.
        
            Returns:
                true if the spin derivative have to be computed, false otherwise
        
        
        """
        ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...

class AttitudeLawLeg(AttitudeLeg):
    """
    public final class AttitudeLawLeg extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
    
        This class represents an attitude law version "attitude", with an interval of validity (whose borders are closed
        points).
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, attitudeLaw: AttitudeLaw, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, attitudeLaw: AttitudeLaw, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, string: str): ...
    @typing.overload
    def __init__(self, attitudeLaw: AttitudeLaw, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, string: str, boolean: bool): ...
    @typing.overload
    def __init__(self, attitudeLaw: AttitudeLaw, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval): ...
    @typing.overload
    def __init__(self, attitudeLaw: AttitudeLaw, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, string: str): ...
    @typing.overload
    def __init__(self, attitudeLaw: AttitudeLaw, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, string: str, boolean: bool): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'AttitudeLawLeg':
        """
            Creates a new leg from this one.
        
            Provided interval does not have to be included in current time interval.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Parameters:
                newIntervalOfValidity (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getAttitudeLaw(self) -> AttitudeLaw:
        """
            Gets the attitude law provider associated to the current attitude leg.
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLaw` of the current leg
        
        
        """
        ...
    def getNature(self) -> str:
        """
            Returns the nature of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getNature` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                The “nature” of the leg.
        
        
        """
        ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Returns the time interval of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getTimeInterval` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                the time interval of the leg.
        
        
        """
        ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Spin derivatives computation applies to underlying :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLawLeg.law`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...

class AttitudeLawModifier(AttitudeLaw):
    """
    public interface AttitudeLawModifier extends :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLaw`
    
        This interface represents an attitude law that modifies/wraps another underlying law.
    
        Since:
            5.1
    """
    def getUnderlyingAttitudeLaw(self) -> AttitudeLaw:
        """
            Get the underlying attitude law.
        
            Returns:
                underlying attitude law
        
        
        """
        ...

class AttitudeLegLaw(AttitudeLaw):
    """
    public class AttitudeLegLaw extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLaw`
    
        This class represents an attitude law version "attitudeLeg", with an interval of validity (whose borders are closed
        points) and attitude laws outside this interval of validity.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, attitudeLaw: AttitudeLaw, attitudeLeg: AttitudeLeg, attitudeLaw2: AttitudeLaw): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Spin derivatives computation applies to :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLegLaw.lawBefore`,
            :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLegLaw.leg` and
            :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLegLaw.lawAfter`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...

class AttitudesSequence(AttitudeLaw):
    """
    public class AttitudesSequence extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLaw`
    
        This classes manages a sequence of different attitude providers that are activated in turn according to switching
        events.
    
        Only one attitude provider in the sequence is in an active state. When one of the switch event associated with the
        active provider occurs, the active provider becomes the one specified with the event. A simple example is a provider for
        the sun lighted part of the orbit and another provider for the eclipse time. When the sun lighted provider is active,
        the eclipse entry event is checked and when it occurs the eclipse provider is activated. When the eclipse provider is
        active, the eclipse exit event is checked and when it occurs the sun lighted provider is activated again. This sequence
        is a simple loop.
    
        An active attitude provider may have several switch events and next provider settings, leading to different activation
        patterns depending on which events are triggered first. An example of this feature is handling switches to safe mode if
        some contingency condition is met, in addition to the nominal switches that correspond to proper operations. Another
        example is handling of maneuver mode.
    
    
        Since:
            5.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def addSwitchingCondition(self, attitudeLaw: AttitudeLaw, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, boolean: bool, boolean2: bool, attitudeLaw2: AttitudeLaw) -> None:
        """
            Add a switching condition between two attitude providers.
        
            An attitude provider may have several different switch events associated to it. Depending on which event is triggered,
            the appropriate provider is switched to.
        
            The switch events specified here must *not* be registered to the propagator directly. The proper way to register these
            events is to call :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudesSequence.registerSwitchEvents` once after all
            switching conditions have been set up. The reason for this is that the events will be wrapped before being registered.
        
            Parameters:
                before (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLaw`): attitude provider before the switch event occurrence
                switchEvent (:class:`~fr.cnes.sirius.patrius.events.EventDetector`): event triggering the attitude providers switch ; the event should generate ACTION.RESET_STATE when event occured. (may
                    be null for a provider without any ending condition, in this case the after provider is not referenced and may be null
                    too)
                switchOnIncrease (boolean): if true, switch is triggered on increasing event
                switchOnDecrease (boolean): if true, switch is triggered on decreasing event
                after (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLaw`): attitude provider to activate after the switch event occurrence (used only if switchEvent is non null)
        
        
        """
        ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def registerSwitchEvents(self, propagator: fr.cnes.sirius.patrius.propagation.Propagator) -> None:
        """
            Register all wrapped switch events to the propagator.
        
            This method must be called once before propagation, after the switching conditions have been set up by calls to
            :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudesSequence.addSwitchingCondition`.
        
            Parameters:
                propagator (:class:`~fr.cnes.sirius.patrius.propagation.Propagator`): propagator that will handle the events
        
        
        """
        ...
    def resetActiveProvider(self, attitudeLaw: AttitudeLaw) -> None:
        """
            Reset the active provider.
        
            Parameters:
                provider (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLaw`): the provider to activate
        
        
        """
        ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Spin derivatives computation does not apply to provided law. Call
            :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudesSequence.setSpinDerivativesComputation` on each law to
            activate/deactivate underlying law spin derivative computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class RelativeTabulatedAttitudeLaw(AttitudeLaw):
    """
    public class RelativeTabulatedAttitudeLaw extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLaw`
    
        This class represents a relative tabulated attitude law version "attitudeLeg", with an interval of validity (whose
        borders are closed points) and attitude laws outside this interval of validity, which can be of two types : a
        :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`, or an ExtrapolatedAttitudeLaw (private class)
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, list: java.util.List[fr.cnes.sirius.patrius.math.util.Pair[float, fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation]], aroundAttitudeType: 'RelativeTabulatedAttitudeLaw.AroundAttitudeType', aroundAttitudeType2: 'RelativeTabulatedAttitudeLaw.AroundAttitudeType'): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, list: java.util.List[fr.cnes.sirius.patrius.math.util.Pair[float, fr.cnes.sirius.patrius.utils.AngularCoordinates]], frame: fr.cnes.sirius.patrius.frames.Frame, aroundAttitudeType: 'RelativeTabulatedAttitudeLaw.AroundAttitudeType', aroundAttitudeType2: 'RelativeTabulatedAttitudeLaw.AroundAttitudeType'): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...
    class AroundAttitudeType(java.lang.Enum['RelativeTabulatedAttitudeLaw.AroundAttitudeType']):
        CONSTANT_ATT: typing.ClassVar['RelativeTabulatedAttitudeLaw.AroundAttitudeType'] = ...
        EXTRAPOLATED_ATT: typing.ClassVar['RelativeTabulatedAttitudeLaw.AroundAttitudeType'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'RelativeTabulatedAttitudeLaw.AroundAttitudeType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['RelativeTabulatedAttitudeLaw.AroundAttitudeType']: ...

class RelativeTabulatedAttitudeLeg(AttitudeLeg):
    """
    public class RelativeTabulatedAttitudeLeg extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
    
        This class implements the tabulated attitude leg relative to a reference date. WARNING : Double being less accurate than
        an AbsoluteDate, this class is less accurate than the :class:`~fr.cnes.sirius.patrius.attitudes.TabulatedAttitude`
        class.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, list: java.util.List[fr.cnes.sirius.patrius.math.util.Pair[float, fr.cnes.sirius.patrius.utils.AngularCoordinates]]): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, list: java.util.List[fr.cnes.sirius.patrius.math.util.Pair[float, fr.cnes.sirius.patrius.utils.AngularCoordinates]], string: str): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, list: java.util.List[fr.cnes.sirius.patrius.math.util.Pair[float, fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation]], frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, list: java.util.List[fr.cnes.sirius.patrius.math.util.Pair[float, fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation]], frame: fr.cnes.sirius.patrius.frames.Frame, int: int): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, list: java.util.List[fr.cnes.sirius.patrius.math.util.Pair[float, fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation]], frame: fr.cnes.sirius.patrius.frames.Frame, int: int, string: str): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, list: java.util.List[fr.cnes.sirius.patrius.math.util.Pair[float, fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation]], frame: fr.cnes.sirius.patrius.frames.Frame, string: str): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, list: java.util.List[fr.cnes.sirius.patrius.math.util.Pair[float, fr.cnes.sirius.patrius.utils.AngularCoordinates]], int: int, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, list: java.util.List[fr.cnes.sirius.patrius.math.util.Pair[float, fr.cnes.sirius.patrius.utils.AngularCoordinates]], int: int, frame: fr.cnes.sirius.patrius.frames.Frame, string: str): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'RelativeTabulatedAttitudeLeg':
        """
            Creates a new leg from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Parameters:
                newIntervalOfValidity (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getNature(self) -> str:
        """
            Returns the nature of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getNature` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                The “nature” of the leg.
        
        
        """
        ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Returns the time interval of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getTimeInterval` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                the time interval of the leg.
        
        
        """
        ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...

class Slew(AttitudeLeg):
    """
    public interface Slew extends :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
    
        This interface represents a slew model set.
    
        Since:
            1.1
    """
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'Slew':
        """
            Creates a new leg from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    @typing.overload
    def getAttitude(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...

class TabulatedAttitude(AttitudeLeg):
    """
    public class TabulatedAttitude extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
    
    
        This class implements the tabulated attitude leg.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`, :meth:`~serialized`
    """
    DEFAULT_INTERP_ORDER: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_INTERP_ORDER
    
        Default number of points used for interpolation.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, list: java.util.List[Attitude]): ...
    @typing.overload
    def __init__(self, list: java.util.List[Attitude], int: int): ...
    @typing.overload
    def __init__(self, list: java.util.List[Attitude], int: int, boolean: bool, string: str): ...
    @typing.overload
    def __init__(self, list: java.util.List[Attitude], int: int, string: str): ...
    @typing.overload
    def __init__(self, list: java.util.List[Attitude], string: str): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'TabulatedAttitude':
        """
            Creates a new leg from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Parameters:
                newIntervalOfValidity (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    @typing.overload
    def getAttitude(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Attitude: ...
    @typing.overload
    def getAttitude(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getAttitudes(self) -> java.util.List[Attitude]: ...
    def getDurations(self) -> typing.MutableSequence[float]:
        """
            Getter for the durations.
        
            Returns:
                the durations
        
        
        """
        ...
    def getNature(self) -> str:
        """
            Returns the nature of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getNature` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                The “nature” of the leg.
        
        
        """
        ...
    def getReferenceFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Getter for the reference frame.
        
            Returns:
                referenceFrame reference frame from which attitude is defined.
        
        
        """
        ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Returns the time interval of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getTimeInterval` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                the time interval of the leg.
        
        
        """
        ...
    def isSpinDerivativesComputation(self) -> bool:
        """
            Returns spin derivatives computation flag.
        
            Returns:
                spin derivatives computation flag
        
        
        """
        ...
    def setAngularDerivativesFilter(self, angularDerivativesFilter: fr.cnes.sirius.patrius.utils.AngularDerivativesFilter) -> None:
        """
            Setter for the filter to use in interpolation.
        
            Parameters:
                angularDerivativeFilter (:class:`~fr.cnes.sirius.patrius.utils.AngularDerivativesFilter`): the filter to set
        
        
        """
        ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...
    def setTimeInterval(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'TabulatedAttitude':
        """
            Return a new law with the specified interval.
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): new interval of validity
        
            Returns:
                new tabulated attitude law
        
        
        """
        ...

class AbstractGroundPointing(AbstractAttitudeLaw):
    """
    public abstract class AbstractGroundPointing extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
    
        Base class for ground pointing attitude providers.
    
        This class is a basic model for different kind of ground pointing attitude providers, such as : body center pointing,
        nadir pointing, target pointing, etc...
    
        The object :code:`GroundPointing` is guaranteed to be immutable.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`, :meth:`~serialized`
    """
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getBodyFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Getter for the body frame.
        
            Returns:
                body frame
        
        
        """
        ...
    def getBodyShape(self) -> fr.cnes.sirius.patrius.bodies.BodyShape:
        """
            Getter for the body shape.
        
            Returns:
                body shape
        
        
        """
        ...
    def getLosInSatFrame(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates:
        """
            Getter for the LOS in satellite frame axis.
        
            Returns:
                the LOS in satellite frame axis
        
        
        """
        ...
    def getLosNormalInSatFrame(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates:
        """
            Getter for the LOS normal axis in satellite frame.
        
            Returns:
                the LOS normal axis in satellite frame
        
        
        """
        ...

class AeroAttitudeLaw(AbstractAttitudeLaw):
    """
    public class AeroAttitudeLaw extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
    
        Class defining an aerodynamic attitude law by angle of attack, sideslip and velocity roll.
    
        Since:
            3.4
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid, double4: float, double5: float): ...
    @typing.overload
    def __init__(self, iParameterizableFunction: fr.cnes.sirius.patrius.math.parameter.IParameterizableFunction, iParameterizableFunction2: fr.cnes.sirius.patrius.math.parameter.IParameterizableFunction, iParameterizableFunction3: fr.cnes.sirius.patrius.math.parameter.IParameterizableFunction, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid): ...
    @typing.overload
    def __init__(self, iParameterizableFunction: fr.cnes.sirius.patrius.math.parameter.IParameterizableFunction, iParameterizableFunction2: fr.cnes.sirius.patrius.math.parameter.IParameterizableFunction, iParameterizableFunction3: fr.cnes.sirius.patrius.math.parameter.IParameterizableFunction, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid, double: float, double2: float): ...
    @staticmethod
    def aircraftToAero(double: float, double2: float, double3: float, double4: float, double5: float) -> typing.MutableSequence[float]: ...
    def getAngleOfAttack(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Getter for the angle of attack.
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): state
        
            Returns:
                the angle of attack.
        
        
        """
        ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getRollVelocity(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Getter for the roll velocity.
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): state
        
            Returns:
                the roll velocity.
        
        
        """
        ...
    def getSideSlipAngle(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Getter for the side slip angle.
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): state
        
            Returns:
                the side slip angle.
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class BodyCenterPointing(AbstractAttitudeLaw):
    """
    public class BodyCenterPointing extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
    
        This class handles body center pointing attitude provider.
    
        This class represents the attitude provider where the satellite z axis is pointing to a body center.
    
        The object :code:`BodyCenterPointing` is guaranteed to be immutable.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, boolean: bool): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...

class CelestialBodyPointed(AbstractAttitudeLaw):
    """
    public class CelestialBodyPointed extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
    
        This class handles a celestial body pointed attitude provider.
    
        The celestial body pointed law is defined by two main elements:
    
          - a celestial body towards which some satellite axis is exactly aimed
          - a phasing reference defining the rotation around the pointing axis
    
    
        The celestial body implicitly defines two of the three degrees of freedom and the phasing reference defines the
        remaining degree of freedom. This definition can be represented as first aligning exactly the satellite pointing axis to
        the current direction of the celestial body, and then to find the rotation around this axis such that the satellite
        phasing axis is in the half-plane defined by a cut line on the pointing axis and containing the celestial phasing
        reference.
    
        In order for this definition to work, the user must ensure that the phasing reference is **never** aligned with the
        pointing reference. Since the pointed body moves as the date changes, this should be ensured regardless of the date. A
        simple way to do this for Sun, Moon or any planet pointing is to choose a phasing reference far from the ecliptic plane.
        Using :code:`Vector3D.PLUS_K`, the equatorial pole, is perfect in these cases.
    
        Instances of this class are guaranteed to be immutable.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...

class ComposedAttitudeLaw(AbstractAttitudeLaw, AttitudeLawModifier):
    """
    public class ComposedAttitudeLaw extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw` implements :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLawModifier`
    
        This class represents a composed attitude law, defined by a main attitude law provider and a chained list of orientation
        laws.
    
    
        The main attitude law provides, for a given date, the dynamic frame representing the spacecraft orientation; this
        orientation is then progressively transformed using the orientation laws.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeFrame`,
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeTransformProvider`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, attitudeLaw: AttitudeLaw, linkedList: java.util.LinkedList[typing.Union[IOrientationLaw, typing.Callable]]): ...
    @typing.overload
    def __init__(self, attitudeLaw: AttitudeLaw, linkedList: java.util.LinkedList[typing.Union[IOrientationLaw, typing.Callable]], double: float): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getUnderlyingAttitudeLaw(self) -> AttitudeLaw:
        """
            Get the underlying attitude law.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLawModifier.getUnderlyingAttitudeLaw` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLawModifier`
        
            Returns:
                underlying attitude law
        
        
        """
        ...

class ConstantAttitudeLaw(AbstractAttitudeLaw):
    """
    public class ConstantAttitudeLaw extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
    
        This class handles a constant attitude law.
    
        Instances of this class are guaranteed to be immutable.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getReferenceFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Getter for the reference frame.
        
            Returns:
                the reference frame
        
        
        """
        ...
    def getRotation(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation:
        """
            Getter for the rotation from reference frame to satellite frame.
        
            Returns:
                the rotation from reference frame to satellite frame
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class ConstantSpinSlew(Slew):
    """
    public class ConstantSpinSlew extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.Slew`
    
    
        This class represents a constant spin slew.
    
        The Constant spin slew is a "simple" slew that computes the attitude of the satellite using a spherical interpolation of
        the quaternions representing the starting and ending attitudes.
    
    
        Some constraints, such as minimal maneuver duration or maximal angular velocity, must be taken into account during the
        maneuver computation.
    
    
        Like all the other attitude legs, its interval of validity has closed endpoints.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, attitude: Attitude, attitude2: Attitude): ...
    @typing.overload
    def __init__(self, attitude: Attitude, attitude2: Attitude, double: float, string: str): ...
    @typing.overload
    def __init__(self, attitude: Attitude, attitude2: Attitude, double: float, string: str, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, attitude: Attitude, attitude2: Attitude, string: str): ...
    @typing.overload
    def __init__(self, attitude: Attitude, attitude2: Attitude, string: str, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'ConstantSpinSlew':
        """
            Creates a new leg from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.Slew.copy` in interface :class:`~fr.cnes.sirius.patrius.attitudes.Slew`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Parameters:
                newIntervalOfValidity (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    @typing.overload
    def getAttitude(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getDuration(self) -> float: ...
    def getNature(self) -> str:
        """
            Returns the nature of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getNature` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                The “nature” of the leg.
        
        
        """
        ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Returns the time interval of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getTimeInterval` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                the time interval of the leg.
        
        
        """
        ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...

class FixedRate(AbstractAttitudeLaw):
    """
    public class FixedRate extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
    
        This class handles a simple attitude provider at constant rate around a fixed axis.
    
        This attitude provider is a simple linear extrapolation from an initial orientation, a rotation axis and a rotation
        rate. All this elements can be specified as a simple :class:`~fr.cnes.sirius.patrius.attitudes.Attitude`.
    
        Instances of this class are guaranteed to be immutable.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, attitude: Attitude): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getReferenceAttitude(self) -> Attitude:
        """
            Get the reference attitude.
        
            Returns:
                reference attitude
        
        
        """
        ...

class IsisSunAndPseudoSpinPointing(AbstractAttitudeLaw):
    """
    public class IsisSunAndPseudoSpinPointing extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
    
        This class handles SunIsis and PseudoSpin attitude provider. This law is composed of a base frame (SUN ISIS) defined as
    
    
        - Z_sun = direction Sun->Sat
    
    
        - X_sun = Z_sun^orbitalMomentum with sign so that X_sun(3) is negative (FLAG 1 if negated else 0)
    
    
        followed by a rotation about the Z_sun axis of angle:
    
    
        bias = - BETA_SIGN * alpha – PHI + FLAG * PI + (1 – BETA_SIGN) * PI/2
    
    
        where alpha is the Sat->Sun angle with Z in the LVLH XZ plane Note that due to simplifications in the computation (eg
        fixed sun, keplerian motion, fixed orbital plane) the angular velocity has an approximate error of O(E-7) rad/sec (real
        value is O(E-3) as driven by orbital period) and angular acceleration is not computed (zero), likely O(E-9) rad/s2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, iDirection: fr.cnes.sirius.patrius.attitudes.directions.IDirection, double: float, boolean: bool): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...

class IsisSunPointing(AbstractAttitudeLaw):
    """
    public class IsisSunPointing extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
    
        Implementation of ISIS Sun pointing attitude law. This class implements
        :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`, so the associated service
        :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.getAttitude` is available. ISIS Sun pointing law corresponds
        to an ordered attitude matching with the Sun axis (X_sun, Y_sun, Z_sun) computed in GCRF frame by specific formulae.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, iDirection: fr.cnes.sirius.patrius.attitudes.directions.IDirection): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...

class LofOffset(AbstractAttitudeLaw):
    """
    public class LofOffset extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
    
        Attitude law defined by fixed Roll, Pitch and Yaw angles (in any order) with respect to a local orbital frame.
    
        The attitude provider is defined as a rotation offset from some local orbital frame.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, lOFType: fr.cnes.sirius.patrius.frames.LOFType): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, lOFType: fr.cnes.sirius.patrius.frames.LOFType, rotationOrder: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.RotationOrder, double: float, double2: float, double3: float): ...
    @typing.overload
    def __init__(self, lOFType: fr.cnes.sirius.patrius.frames.LOFType): ...
    @typing.overload
    def __init__(self, lOFType: fr.cnes.sirius.patrius.frames.LOFType, rotationOrder: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.RotationOrder, double: float, double2: float, double3: float): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getLofType(self) -> fr.cnes.sirius.patrius.frames.LOFType:
        """
            Getter for the type of Local Orbital Frame.
        
            Returns:
                the type of Local Orbital Frame
        
        
        """
        ...
    def getPseudoInertialFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Getter for the inertial frame with respect to which orbit should be computed. This frame is the pivot in the
            transformation from the actual frame to the local orbital frame.
        
            Returns:
                the inertial frame with respect to which orbit should be computed. This frame is the pivot in the transformation from
                the actual frame to the local orbital frame
        
        
        """
        ...
    def getRotation(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation:
        """
            Getter for the rotation from reference frame to satellite frame.
        
            Returns:
                the rotation from reference frame to satellite frame
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class SpinStabilized(AbstractAttitudeLaw, AttitudeLawModifier):
    """
    public class SpinStabilized extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw` implements :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLawModifier`
    
        This class handles a spin stabilized attitude provider.
    
        Spin stabilized laws are handled as wrappers for an underlying non-rotating law. This underlying law is typically an
        instance of :class:`~fr.cnes.sirius.patrius.attitudes.CelestialBodyPointed` with the pointing axis equal to the rotation
        axis, but can in fact be anything.
    
        Instances of this class are guaranteed to be immutable.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, attitudeLaw: AttitudeLaw, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getAxis(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the rotation axis in satellite frame.
        
            Returns:
                the rotation axis in satellite frame
        
        
        """
        ...
    def getNonRotatingLaw(self) -> AttitudeLaw:
        """
            Getter for the underlying non-rotating attitude law.
        
            Returns:
                the underlying non-rotating attitude law
        
        
        """
        ...
    def getRate(self) -> float:
        """
            Getter for the spin rate in radians per seconds.
        
            Returns:
                the spin rate in radians per seconds
        
        
        """
        ...
    def getStartDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the start date of the rotation.
        
            Returns:
                the start date of the rotation
        
        
        """
        ...
    def getUnderlyingAttitudeLaw(self) -> AttitudeLaw:
        """
            Get the underlying attitude law.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLawModifier.getUnderlyingAttitudeLaw` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLawModifier`
        
            Returns:
                underlying attitude law
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class TabulatedSlew(TabulatedAttitude, Slew):
    """
    public final class TabulatedSlew extends :class:`~fr.cnes.sirius.patrius.attitudes.TabulatedAttitude` implements :class:`~fr.cnes.sirius.patrius.attitudes.Slew`
    
    
        This class represents a tabulated slew.
    
        Since:
            4.5
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, list: java.util.List[Attitude]): ...
    @typing.overload
    def __init__(self, list: java.util.List[Attitude], int: int): ...
    @typing.overload
    def __init__(self, list: java.util.List[Attitude], int: int, string: str): ...
    @typing.overload
    def __init__(self, list: java.util.List[Attitude], string: str): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'TabulatedSlew':
        """
            Creates a new leg from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.Slew.copy` in interface :class:`~fr.cnes.sirius.patrius.attitudes.Slew`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.TabulatedAttitude.copy` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.TabulatedAttitude`
        
            Parameters:
                newIntervalOfValidity (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    @typing.overload
    def getAttitude(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getSpinDerivatives(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class TargetPointing(AbstractAttitudeLaw):
    """
    public class TargetPointing extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
    
        This class handles target pointing attitude provider.
    
        This class represents the attitude provider where the satellite z axis is pointing to a ground point target.
    
        The target position is defined in a body frame specified by the user. It is important to make sure this frame is
        consistent.
    
        The object :code:`TargetPointing` is guaranteed to be immutable.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...

class TwoDirectionAttitudeLaw(AbstractAttitudeLaw):
    """
    public class TwoDirectionAttitudeLaw extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
    
    
        This class implements a generic two directions attitude law. The first direction is aligned with a given satellite axis,
        the second direction is aligned at best with another given satellite axis. If the two directions are collinear, an
        exception will be thrown in the :meth:`~fr.cnes.sirius.patrius.attitudes.TwoDirectionAttitudeLaw.getAttitude` method.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, iDirection: fr.cnes.sirius.patrius.attitudes.directions.IDirection, iDirection2: fr.cnes.sirius.patrius.attitudes.directions.IDirection, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, iDirection: fr.cnes.sirius.patrius.attitudes.directions.IDirection, iDirection2: fr.cnes.sirius.patrius.attitudes.directions.IDirection, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, double2: float): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getFirstAxis(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the satellite axis aligned with the first direction.
        
            Returns:
                the satellite axis aligned with the first direction
        
        
        """
        ...
    def getSecondAxis(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the satellite axis aligned at best with the second direction.
        
            Returns:
                the satellite axis aligned at best with the second direction
        
        
        """
        ...

class AbstractGroundPointingWrapper(AbstractGroundPointing, AttitudeLawModifier):
    """
    public abstract class AbstractGroundPointingWrapper extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractGroundPointing` implements :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLawModifier`
    
        This class leverages common parts for compensation modes around ground pointing attitudes.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, abstractGroundPointing: AbstractGroundPointing): ...
    @typing.overload
    def __init__(self, abstractGroundPointing: AbstractGroundPointing, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, abstractGroundPointing: AbstractGroundPointing, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    def getBaseState(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getCompensation(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, attitude: Attitude) -> fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates: ...
    def getGroundPointingLaw(self) -> AttitudeLaw:
        """
            Getter for the ground pointing attitude provider without yaw compensation.
        
            Returns:
                the ground pointing attitude provider without yaw compensation
        
        
        """
        ...
    def getUnderlyingAttitudeLaw(self) -> AttitudeLaw:
        """
            Get the underlying (ground pointing) attitude provider.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLawModifier.getUnderlyingAttitudeLaw` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLawModifier`
        
            Returns:
                underlying attitude provider
        
        
        """
        ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Spin derivatives computation applies to provided law
            :meth:`~fr.cnes.sirius.patrius.attitudes.AbstractGroundPointingWrapper.groundPointingLaw`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw.setSpinDerivativesComputation` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...

class BodyCenterGroundPointing(AbstractGroundPointing):
    """
    public class BodyCenterGroundPointing extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractGroundPointing`
    
        This class handles body center pointing attitude provider; the difference between
        :class:`~fr.cnes.sirius.patrius.attitudes.BodyCenterPointing` and this class is that the target point of the former is
        the body center, while that of the latter is the corresponding point on the ground.
    
        By default, the satellite z axis is pointing to the body frame center.
    
        Since:
            2.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.BodyCenterPointing`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape): ...
    @typing.overload
    def __init__(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class LofOffsetPointing(AbstractGroundPointing):
    """
    public class LofOffsetPointing extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractGroundPointing`
    
        This class provides a default attitude provider.
    
        The attitude pointing law is defined by an attitude provider and the satellite axis vector chosen for pointing.
    
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, attitudeProvider: AttitudeProvider, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, attitudeProvider: AttitudeProvider, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Spin derivatives computation applies to provided law
            :meth:`~fr.cnes.sirius.patrius.attitudes.LofOffsetPointing.attitudeLaw`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw.setSpinDerivativesComputation` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.AbstractAttitudeLaw`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...

class NadirPointing(AbstractGroundPointing):
    """
    public class NadirPointing extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractGroundPointing`
    
        This class handles nadir pointing attitude provider.
    
        This class represents the attitude provider where (by default) the satellite z axis is pointing to the vertical of the
        ground point under satellite.
    
        The object :code:`NadirPointing` is guaranteed to be immutable.
    
        This class is restricted to be used with :class:`~fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape`.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape): ...
    @typing.overload
    def __init__(self, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    def getTargetPV(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates: ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class SunPointing(TwoDirectionAttitudeLaw):
    """
    public class SunPointing extends :class:`~fr.cnes.sirius.patrius.attitudes.TwoDirectionAttitudeLaw`
    
    
        This class implements a Sun pointing attitude law. The first direction is the satellite-sun direction, the second
        direction is either the sun poles axis or the normal to the satellite orbit.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.directions.IDirection`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, celestialBodyFrame: fr.cnes.sirius.patrius.frames.CelestialBodyFrame, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, celestialBodyFrame: fr.cnes.sirius.patrius.frames.CelestialBodyFrame, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, celestialBody: fr.cnes.sirius.patrius.bodies.CelestialBody): ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class TargetGroundPointing(AbstractGroundPointing):
    """
    public class TargetGroundPointing extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractGroundPointing`
    
        This class handles target pointing attitude provider; while the class
        :class:`~fr.cnes.sirius.patrius.attitudes.TargetPointing` does not guarantee the target point belongs to the body
        surface, this class always provides a ground point target.
    
        By default, the satellite z axis is pointing to a ground point target.
    
        Since:
            2.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.attitudes.TargetPointing`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint): ...
    @typing.overload
    def __init__(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    @typing.overload
    def __init__(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    def getTargetPoint(self) -> fr.cnes.sirius.patrius.bodies.BodyPoint:
        """
            Getter for the target point.
        
            Returns:
                the target point
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class YawCompensation(AbstractGroundPointingWrapper):
    """
    public class YawCompensation extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractGroundPointingWrapper`
    
        This class handles yaw compensation attitude provider.
    
        Yaw compensation is mainly used for Earth observation satellites. As a satellites moves along its track, the image of
        ground points move on the focal point of the optical sensor. This motion is a combination of the satellite motion, but
        also on the Earth rotation and on the current attitude (in particular if the pointing includes Roll or Pitch offset). In
        order to reduce geometrical distortion, the yaw angle is changed a little from the simple ground pointing attitude such
        that the apparent motion of ground points is along a prescribed axis (orthogonal to the optical sensors rows), taking
        into account all effects.
    
        This attitude is implemented as a wrapper on top of an underlying ground pointing law that defines the roll and pitch
        angles.
    
        Instances of this class are guaranteed to be immutable.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, abstractGroundPointing: AbstractGroundPointing): ...
    @typing.overload
    def __init__(self, abstractGroundPointing: AbstractGroundPointing, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getCompensation(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, attitude: Attitude) -> fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates: ...
    def getYawAngle(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...

class YawSteering(AbstractGroundPointingWrapper):
    """
    public class YawSteering extends :class:`~fr.cnes.sirius.patrius.attitudes.AbstractGroundPointingWrapper`
    
        This class handles yaw steering law.
    
        Yaw steering is mainly used for low Earth orbiting satellites with no missions-related constraints on yaw angle. It sets
        the yaw angle in such a way the solar arrays have maximal lighting without changing the roll and pitch.
    
        The motion in yaw is smooth when the Sun is far from the orbital plane, but gets more and more *square like* as the Sun
        gets closer to the orbital plane. The degenerate extreme case with the Sun in the orbital plane leads to a yaw angle
        switching between two steady states, with instantaneaous π radians rotations at each switch, two times per orbit. This
        degenerate case is clearly not operationally sound so another pointing mode is chosen when Sun comes closer than some
        predefined threshold to the orbital plane.
    
        This class can handle (for now) only a theoretically perfect yaw steering (i.e. the yaw angle is exactly the optimal
        angle). Smoothed yaw steering with a few sine waves approaching the optimal angle will be added in the future if needed.
    
        This attitude is implemented as a wrapper on top of an underlying ground pointing law that defines the roll and pitch
        angles.
    
        Instances of this class are guaranteed to be immutable.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, abstractGroundPointing: AbstractGroundPointing, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, abstractGroundPointing: AbstractGroundPointing, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> Attitude: ...
    def getCompensation(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, attitude: Attitude) -> fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates: ...
    def getPhasingAxis(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the satellite axis that must be roughly in Sun direction.
        
            Returns:
                the satellite axis that must be roughly in Sun direction.
        
        
        """
        ...
    def getSun(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Returns the Sun.
        
            Returns:
                the Sun
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.attitudes")``.

    AbstractAttitudeEphemerisGenerator: typing.Type[AbstractAttitudeEphemerisGenerator]
    AbstractAttitudeLaw: typing.Type[AbstractAttitudeLaw]
    AbstractGroundPointing: typing.Type[AbstractGroundPointing]
    AbstractGroundPointingWrapper: typing.Type[AbstractGroundPointingWrapper]
    AeroAttitudeLaw: typing.Type[AeroAttitudeLaw]
    Attitude: typing.Type[Attitude]
    AttitudeChronologicalComparator: typing.Type[AttitudeChronologicalComparator]
    AttitudeFrame: typing.Type[AttitudeFrame]
    AttitudeLaw: typing.Type[AttitudeLaw]
    AttitudeLawLeg: typing.Type[AttitudeLawLeg]
    AttitudeLawModifier: typing.Type[AttitudeLawModifier]
    AttitudeLeg: typing.Type[AttitudeLeg]
    AttitudeLegLaw: typing.Type[AttitudeLegLaw]
    AttitudeProvider: typing.Type[AttitudeProvider]
    AttitudeTransformProvider: typing.Type[AttitudeTransformProvider]
    AttitudesSequence: typing.Type[AttitudesSequence]
    BodyCenterGroundPointing: typing.Type[BodyCenterGroundPointing]
    BodyCenterPointing: typing.Type[BodyCenterPointing]
    CelestialBodyPointed: typing.Type[CelestialBodyPointed]
    ComposedAttitudeLaw: typing.Type[ComposedAttitudeLaw]
    ConstantAttitudeLaw: typing.Type[ConstantAttitudeLaw]
    ConstantSpinSlew: typing.Type[ConstantSpinSlew]
    DirectionTrackingOrientation: typing.Type[DirectionTrackingOrientation]
    FixedRate: typing.Type[FixedRate]
    FixedStepAttitudeEphemerisGenerator: typing.Type[FixedStepAttitudeEphemerisGenerator]
    IOrientationLaw: typing.Type[IOrientationLaw]
    IsisSunAndPseudoSpinPointing: typing.Type[IsisSunAndPseudoSpinPointing]
    IsisSunPointing: typing.Type[IsisSunPointing]
    LofOffset: typing.Type[LofOffset]
    LofOffsetPointing: typing.Type[LofOffsetPointing]
    NadirPointing: typing.Type[NadirPointing]
    OrientationFrame: typing.Type[OrientationFrame]
    OrientationTransformProvider: typing.Type[OrientationTransformProvider]
    RelativeTabulatedAttitudeLaw: typing.Type[RelativeTabulatedAttitudeLaw]
    RelativeTabulatedAttitudeLeg: typing.Type[RelativeTabulatedAttitudeLeg]
    Slew: typing.Type[Slew]
    SpinStabilized: typing.Type[SpinStabilized]
    StrictAttitudeLegsSequence: typing.Type[StrictAttitudeLegsSequence]
    SunPointing: typing.Type[SunPointing]
    TabulatedAttitude: typing.Type[TabulatedAttitude]
    TabulatedSlew: typing.Type[TabulatedSlew]
    TargetGroundPointing: typing.Type[TargetGroundPointing]
    TargetPointing: typing.Type[TargetPointing]
    TwoDirectionAttitudeLaw: typing.Type[TwoDirectionAttitudeLaw]
    VariableStepAttitudeEphemerisGenerator: typing.Type[VariableStepAttitudeEphemerisGenerator]
    YawCompensation: typing.Type[YawCompensation]
    YawSteering: typing.Type[YawSteering]
    directions: fr.cnes.sirius.patrius.attitudes.directions.__module_protocol__
    kinematics: fr.cnes.sirius.patrius.attitudes.kinematics.__module_protocol__
    multi: fr.cnes.sirius.patrius.attitudes.multi.__module_protocol__
    orientations: fr.cnes.sirius.patrius.attitudes.orientations.__module_protocol__
    profiles: fr.cnes.sirius.patrius.attitudes.profiles.__module_protocol__
    slew: fr.cnes.sirius.patrius.attitudes.slew.__module_protocol__
