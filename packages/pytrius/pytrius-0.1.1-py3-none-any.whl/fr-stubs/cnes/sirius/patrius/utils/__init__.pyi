
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis.differentiation
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.time
import fr.cnes.sirius.patrius.utils.exception
import fr.cnes.sirius.patrius.utils.legs
import fr.cnes.sirius.patrius.utils.serializablefunction
import java.io
import java.lang
import java.util
import java.util.function
import jpype
import typing



class AngularCoordinates(fr.cnes.sirius.patrius.time.TimeShiftable['AngularCoordinates'], java.io.Serializable):
    """
    public class AngularCoordinates extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeShiftable`<:class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Simple container for rotation/rotation rate/rotation acceleration triplet.
    
        When applied to frames, the rotation here describes the orientation of the frame of interest in the reference frame.
        This means that defining X_ref=(1,0,0) in the reference frame, the vector X_interest (X axis of the frame of interest,
        still expressed in the reference frame) is obtained by : rotation.applyTo(X_ref).
    
        The rotation rate (respectively the rotation acceleration) is the vector describing the rotation velocity (rotation
        acceleration) of the frame of interest relatively to the reference frame. This rotation rate (rotation acceleration)
        vector is always expressed in the frame of interest.
    
        The state can be slightly shifted to close dates. This shift is based on an approximate solution of the fixed
        acceleration motion. It is *not* intended as a replacement for proper attitude propagation but should be sufficient for
        either small time shifts or coarse accuracy.
    
        This class is the angular counterpart to :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`.
    
        Instances of this class are guaranteed to be immutable.
    
        Also see:
            :meth:`~serialized`
    """
    IDENTITY: typing.ClassVar['AngularCoordinates'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates` IDENTITY
    
        Fixed orientation parallel with reference frame (identity rotation, zero rotation rate, zero rotation acceleration).
    
    """
    MINUS_TWO: typing.ClassVar[float] = ...
    """
    public static final double MINUS_TWO
    
        Constant number: -2
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, boolean: bool): ...
    @typing.overload
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates3: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates4: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double: float): ...
    @typing.overload
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates3: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates4: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double: float, boolean: bool): ...
    @typing.overload
    def addOffset(self, angularCoordinates: 'AngularCoordinates') -> 'AngularCoordinates':
        """
            Add an offset from the instance.
        
            The instance rotation is applied first and the offset is applied afterward. Note that angular coordinates do *not*
            commute under this operation, i.e. :code:`a.addOffset(b)` and :code:`b.addOffset(a)` lead to *different* results in most
            cases.
        
            The rotation of the angular coordinates returned here is a composition of R_instance first and then R_offset. But to
            compose them, we first have to express them in the same frame : R_offset has to be expressed in the reference frame of
            the instance. So it becomes : R_instance o R_offset o R_instance^-1. The total composed rotation is then : (R_instance o
            R_offset o R_instance^-1) o R_instance, wich can be simplified as R_instance o R_offset.
        
            The two methods :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.addOffset` and
            :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.subtractOffset` are designed so that round trip applications are
            possible. This means that both :code:`ac1.subtractOffset(ac2).addOffset(ac2)` and
            :code:`ac1.addOffset(ac2).subtractOffset(ac2)` return angular coordinates equal to ac1.
        
            Parameters:
                offset (:class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`): offset to subtract
                computeSpinDerivatives (boolean): true if spin derivatives must be computed. If not, spin derivative is set to *null*
        
            Returns:
                new instance, with offset subtracted
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.subtractOffset`
        
            Add an offset from the instance.
        
            The instance rotation is applied first and the offset is applied afterward. Note that angular coordinates do *not*
            commute under this operation, i.e. :code:`a.addOffset(b)` and :code:`b.addOffset(a)` lead to *different* results in most
            cases.
        
            The rotation of the angular coordinates returned here is a composition of R_instance first and then R_offset. But to
            compose them, we first have to express them in the same frame : R_offset has to be expressed in the reference frame of
            the instance. So it becomes : R_instance o R_offset o R_instance^-1. The total composed rotation is then : (R_instance o
            R_offset o R_instance^-1) o R_instance, wich can be simplified as R_instance o R_offset.
        
            The two methods :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.addOffset` and
            :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.subtractOffset` are designed so that round trip applications are
            possible. This means that both :code:`ac1.subtractOffset(ac2).addOffset(ac2)` and
            :code:`ac1.addOffset(ac2).subtractOffset(ac2)` return angular coordinates equal to ac1.
        
            **Warning:**spin derivative is not computed.
        
            Parameters:
                offset (:class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`): offset to subtract
        
            Returns:
                new instance, with offset subtracted
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.subtractOffset`
        
        
        """
        ...
    @typing.overload
    def addOffset(self, angularCoordinates: 'AngularCoordinates', boolean: bool) -> 'AngularCoordinates': ...
    @typing.overload
    def applyTo(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates:
        """
            Apply the rotation to a pv coordinates.
        
            Parameters:
                pv (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`): vector to apply the rotation to
        
            Returns:
                a new pv coordinates which is the image of u by the rotation
        
            Apply the rotation to a pv coordinates.
        
            Parameters:
                pv (:class:`~fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates`): vector to apply the rotation to
        
            Returns:
                a new pv coordinates which is the image of u by the rotation
        
        
        """
        ...
    @typing.overload
    def applyTo(self, timeStampedPVCoordinates: 'TimeStampedPVCoordinates') -> 'TimeStampedPVCoordinates': ...
    @typing.overload
    @staticmethod
    def createFromModifiedRodrigues(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> 'AngularCoordinates':
        """
            Convert a modified Rodrigues vector and derivatives to angular coordinates.
        
            **Warning:**spin derivative is not computed.
        
            Parameters:
                r (double[][]): modified Rodrigues vector (with first and second times derivatives)
        
            Returns:
                angular coordinates
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.getModifiedRodrigues`
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def createFromModifiedRodrigues(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], boolean: bool) -> 'AngularCoordinates':
        """
            Convert a modified Rodrigues vector and derivatives to angular coordinates.
        
            Parameters:
                r (double[][]): modified Rodrigues vector (with first and second times derivatives)
                computeSpinDerivatives (boolean): true if spin derivatives should be computed. If not, spin derivative is set to *null*
        
            Returns:
                angular coordinates
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.getModifiedRodrigues`
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @staticmethod
    def estimateRate(rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, rotation2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Estimate rotation rate between two orientations.
        
            Estimation is based on a simple fixed rate rotation during the time interval between the two orientations.
        
            Those two orientation must be expressed in the same frame.
        
            Parameters:
                start (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation`): start orientation
                end (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation`): end orientation
                dt (double): time elapsed between the dates of the two orientations
        
            Returns:
                rotation rate allowing to go from start to end orientations
        
        
        """
        ...
    @typing.overload
    def getModifiedRodrigues(self, double: float) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Convert rotation, rate and acceleration to modified Rodrigues vector and derivatives.
        
            The modified Rodrigues vector is tan(θ/4) u where θ and u are the rotation angle and axis respectively.
        
            **Warning:**spin derivative is not computed.
        
            Parameters:
                sign (double): multiplicative sign for quaternion components
        
            Returns:
                modified Rodrigues vector and derivatives (vector on row 0, first derivative on row 1, second derivative on row 2)
        
            Also see:
        
            Convert rotation, rate and acceleration to modified Rodrigues vector and derivatives.
        
            The modified Rodrigues vector is tan(θ/4) u where θ and u are the rotation angle and axis respectively.
        
            Parameters:
                sign (double): multiplicative sign for quaternion components
                computeSpinDerivative (boolean): true if spin derivatives should be computed. If not, spin derivative is set to *null*
        
            Returns:
                modified Rodrigues vector and derivatives (vector on row 0, first derivative on row 1, second derivative on row 2)
        
            Also see:
        
        
        """
        ...
    @typing.overload
    def getModifiedRodrigues(self, double: float, boolean: bool) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getRotation(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation:
        """
            Get the rotation.
        
            Returns:
                the rotation.
        
        
        """
        ...
    def getRotationAcceleration(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the rotation acceleration.
        
            Returns:
                the rotation acceleration vector dΩ/dt (rad/s²). May be null if not computed at some point.
        
        
        """
        ...
    def getRotationRate(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the rotation rate.
        
            Returns:
                the rotation rate vector (rad/s).
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @typing.overload
    def revert(self) -> 'AngularCoordinates':
        """
            Revert a rotation/rotation rate/rotation acceleration triplet. Build a triplet which reverse the effect of another
            triplet.
        
            **Warning:**spin derivative is not computed.
        
            Returns:
                a new triplet whose effect is the reverse of the effect of the instance
        
        
        """
        ...
    @typing.overload
    def revert(self, boolean: bool) -> 'AngularCoordinates':
        """
            Revert a rotation/rotation rate/rotation acceleration triplet. Build a triplet which reverse the effect of another
            triplet.
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives must be computed. If not, spin derivative is set to *null*
        
            Returns:
                a new triplet whose effect is the reverse of the effect of the instance
        
        """
        ...
    @typing.overload
    def shiftedBy(self, double: float) -> 'AngularCoordinates':
        """
            Get a time-shifted state.
        
            The state can be slightly shifted to close dates. This shift is based on an approximate solution of the fixed
            acceleration motion. It is *not* intended as a replacement for proper attitude propagation but should be sufficient for
            either small time shifts or coarse accuracy.
        
            **Warning:**spin derivative is not computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeShiftable.shiftedBy` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeShiftable`
        
            Parameters:
                dt (double): time shift in seconds
        
            Returns:
                a new state, shifted with respect to the instance (which is immutable)
        
            Get a time-shifted state.
        
            The state can be slightly shifted to close dates. This shift is based on an approximate solution of the fixed
            acceleration motion. It is *not* intended as a replacement for proper attitude propagation but should be sufficient for
            either small time shifts or coarse accuracy.
        
            Parameters:
                dt (double): time shift in seconds
                computeSpinDerivatives (boolean): true if spin derivatives should be computed. If not, spin derivative is set to *null*
        
            Returns:
                a new state, shifted with respect to the instance (which is immutable)
        
        
        """
        ...
    @typing.overload
    def shiftedBy(self, double: float, boolean: bool) -> 'AngularCoordinates': ...
    @typing.overload
    def subtractOffset(self, angularCoordinates: 'AngularCoordinates') -> 'AngularCoordinates':
        """
            Subtract an offset from the instance.
        
            The instance rotation is applied first and the offset is applied afterward. Note that angular coordinates do *not*
            commute under this operation, i.e. :code:`a.subtractOffset(b)` and :code:`b.subtractOffset(a)` lead to *different*
            results in most cases.
        
            The two methods :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.addOffset` and
            :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.subtractOffset` are designed so that round trip applications are
            possible. This means that both :code:`ac1.subtractOffset(ac2).addOffset(ac2)` and
            :code:`ac1.addOffset(ac2).subtractOffset(ac2)` return angular coordinates equal to ac1.
        
            Parameters:
                offset (:class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`): offset to subtract
                computeSpinDerivatives (boolean): true if spin derivatives must be computed If not, spin derivative is set to *null*
        
            Returns:
                new instance, with offset subtracted
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.addOffset`
        
            Subtract an offset from the instance.
        
            The instance rotation is applied first and the offset is applied afterward. Note that angular coordinates do *not*
            commute under this operation, i.e. :code:`a.subtractOffset(b)` and :code:`b.subtractOffset(a)` lead to *different*
            results in most cases.
        
            The two methods :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.addOffset` and
            :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.subtractOffset` are designed so that round trip applications are
            possible. This means that both :code:`ac1.subtractOffset(ac2).addOffset(ac2)` and
            :code:`ac1.addOffset(ac2).subtractOffset(ac2)` return angular coordinates equal to ac1.
        
            **Warning:**spin derivative is not computed.
        
            Parameters:
                offset (:class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`): offset to subtract
        
            Returns:
                new instance, with offset subtracted
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.addOffset`
        
        
        """
        ...
    @typing.overload
    def subtractOffset(self, angularCoordinates: 'AngularCoordinates', boolean: bool) -> 'AngularCoordinates': ...

class AngularDerivativesFilter(java.lang.Enum['AngularDerivativesFilter']):
    """
    public enum AngularDerivativesFilter extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.utils.AngularDerivativesFilter`>
    
        Enumerate for selecting which derivatives to use in :class:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates`
        interpolation.
    
        Since:
            3.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.utils.CartesianDerivativesFilter`
    """
    USE_R: typing.ClassVar['AngularDerivativesFilter'] = ...
    USE_RR: typing.ClassVar['AngularDerivativesFilter'] = ...
    USE_RRA: typing.ClassVar['AngularDerivativesFilter'] = ...
    @staticmethod
    def getFilter(int: int) -> 'AngularDerivativesFilter':
        """
            Get the filter corresponding to a maximum derivation order.
        
            Parameters:
                order (int): maximum derivation order
        
            Returns:
                the month corresponding to the string
        
            Raises:
                : if the order is out of range
        
        
        """
        ...
    def getMaxOrder(self) -> int:
        """
            Get the maximum derivation order.
        
            Returns:
                maximum derivation order
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'AngularDerivativesFilter':
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
    def values() -> typing.MutableSequence['AngularDerivativesFilter']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (AngularDerivativesFilter c : AngularDerivativesFilter.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class CartesianDerivativesFilter(java.lang.Enum['CartesianDerivativesFilter']):
    """
    public enum CartesianDerivativesFilter extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.utils.CartesianDerivativesFilter`>
    
        Enumerate for selecting which derivatives to use in :class:`~fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates` and
        interpolation.
    
        Since:
            3.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.utils.AngularDerivativesFilter`
    """
    USE_P: typing.ClassVar['CartesianDerivativesFilter'] = ...
    USE_PV: typing.ClassVar['CartesianDerivativesFilter'] = ...
    USE_PVA: typing.ClassVar['CartesianDerivativesFilter'] = ...
    @staticmethod
    def getFilter(int: int) -> 'CartesianDerivativesFilter':
        """
            Get the filter corresponding to a maximum derivation order.
        
            Parameters:
                order (int): maximum derivation order
        
            Returns:
                the month corresponding to the string
        
            Raises:
                : if the order is out of range
        
        
        """
        ...
    def getMaxOrder(self) -> int:
        """
            Get the maximum derivation order.
        
            Returns:
                maximum derivation order
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'CartesianDerivativesFilter':
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
    def values() -> typing.MutableSequence['CartesianDerivativesFilter']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (CartesianDerivativesFilter c : CartesianDerivativesFilter.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class Constants:
    """
    public interface Constants
    
        Set of useful physical constants.
    """
    KM_TO_M: typing.ClassVar[float] = ...
    """
    static final double KM_TO_M
    
        Conversion factor: kilometers to meters.
    
        Also see:
            :meth:`~constant`
    
    
    """
    SPEED_OF_LIGHT: typing.ClassVar[float] = ...
    """
    static final double SPEED_OF_LIGHT
    
        Speed of light: 299792458.0 m/s.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JULIAN_DAY: typing.ClassVar[float] = ...
    """
    static final double JULIAN_DAY
    
        Duration of a mean solar day: 86400.0 s.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JULIAN_YEAR: typing.ClassVar[float] = ...
    """
    static final double JULIAN_YEAR
    
        Duration of a julian year: 365.25 :meth:`~fr.cnes.sirius.patrius.utils.Constants.JULIAN_DAY`.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JULIAN_DAY_CENTURY: typing.ClassVar[float] = ...
    """
    static final double JULIAN_DAY_CENTURY
    
        Number of julian days in a century.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JULIAN_CENTURY: typing.ClassVar[float] = ...
    """
    static final double JULIAN_CENTURY
    
        Duration of a julian century: 36525 :meth:`~fr.cnes.sirius.patrius.utils.Constants.JULIAN_DAY`.
    
        Also see:
            :meth:`~constant`
    
    
    """
    ARC_SECONDS_TO_RADIANS: typing.ClassVar[float] = ...
    """
    static final double ARC_SECONDS_TO_RADIANS
    
        Conversion factor from arc seconds to radians: 2*PI/(360*60*60).
    
        Also see:
            :meth:`~constant`
    
    
    """
    RADIANS_TO_SEC: typing.ClassVar[float] = ...
    """
    static final double RADIANS_TO_SEC
    
        Conversion factor from radians to seconds: 86400 / 2*PI.
    
        Also see:
            :meth:`~constant`
    
    
    """
    G0_STANDARD_GRAVITY: typing.ClassVar[float] = ...
    """
    static final double G0_STANDARD_GRAVITY
    
        Standard gravity constant, used in maneuvers definition: 9.80665 m/s :sup:`2` .
    
        Also see:
            :meth:`~constant`
    
    
    """
    SUN_RADIUS: typing.ClassVar[float] = ...
    """
    static final double SUN_RADIUS
    
        Sun radius: 695500000 m.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MOON_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double MOON_EQUATORIAL_RADIUS
    
        Moon equatorial radius: 1737400 m.
    
        Also see:
            :meth:`~constant`
    
    
    """
    WGS84_EARTH_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double WGS84_EARTH_EQUATORIAL_RADIUS
    
        Earth equatorial radius from WGS84 model: 6378137.0 m.
    
        Also see:
            :meth:`~constant`
    
    
    """
    WGS84_EARTH_FLATTENING: typing.ClassVar[float] = ...
    """
    static final double WGS84_EARTH_FLATTENING
    
        Earth flattening from WGS84 model: 1.0 / 298.257223563.
    
        Also see:
            :meth:`~constant`
    
    
    """
    WGS84_EARTH_ANGULAR_VELOCITY: typing.ClassVar[float] = ...
    """
    static final double WGS84_EARTH_ANGULAR_VELOCITY
    
        Earth angular velocity from WGS84 model: 7.292115e-5 rad/s.
    
        Also see:
            :meth:`~constant`
    
    
    """
    WGS84_EARTH_MU: typing.ClassVar[float] = ...
    """
    static final double WGS84_EARTH_MU
    
        Earth gravitational constant from WGS84 model: 3.986004418 m :sup:`3` /s :sup:`2` .
    
        Also see:
            :meth:`~constant`
    
    
    """
    WGS84_EARTH_C20: typing.ClassVar[float] = ...
    """
    static final double WGS84_EARTH_C20
    
        Earth un-normalized second zonal coefficient from WGS84 model: .
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRS80_EARTH_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double GRS80_EARTH_EQUATORIAL_RADIUS
    
        Earth equatorial radius from GRS80 model: 6378137.0 m.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRS80_EARTH_FLATTENING: typing.ClassVar[float] = ...
    """
    static final double GRS80_EARTH_FLATTENING
    
        Earth flattening from GRS80 model: 1.0 / 298.257222101.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRS80_EARTH_ANGULAR_VELOCITY: typing.ClassVar[float] = ...
    """
    static final double GRS80_EARTH_ANGULAR_VELOCITY
    
        Earth angular velocity from GRS80 model: 7.292115e-5 rad/s.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRS80_EARTH_MU: typing.ClassVar[float] = ...
    """
    static final double GRS80_EARTH_MU
    
        Earth gravitational constant from GRS80 model: 3.986005e14 m :sup:`3` /s :sup:`2` .
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRS80_EARTH_C20: typing.ClassVar[float] = ...
    """
    static final double GRS80_EARTH_C20
    
        Earth un-normalized second zonal coefficient from GRS80 model: -1.08263e-3.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EGM96_EARTH_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double EGM96_EARTH_EQUATORIAL_RADIUS
    
        Earth equatorial radius from EGM96 model: 6378136.3 m.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EGM96_EARTH_MU: typing.ClassVar[float] = ...
    """
    static final double EGM96_EARTH_MU
    
        Earth gravitational constant from EGM96 model: 3.986004415 m :sup:`3` /s :sup:`2` .
    
        Also see:
            :meth:`~constant`
    
    
    """
    EGM96_EARTH_C20: typing.ClassVar[float] = ...
    """
    static final double EGM96_EARTH_C20
    
        Earth un-normalized second zonal coefficient from EGM96 model: -1.08262668355315e-3.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EGM96_EARTH_C30: typing.ClassVar[float] = ...
    """
    static final double EGM96_EARTH_C30
    
        Earth un-normalized third zonal coefficient from EGM96 model: 2.53265648533224e-6.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EGM96_EARTH_C40: typing.ClassVar[float] = ...
    """
    static final double EGM96_EARTH_C40
    
        Earth un-normalized fourth zonal coefficient from EGM96 model: 1.619621591367e-6.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EGM96_EARTH_C50: typing.ClassVar[float] = ...
    """
    static final double EGM96_EARTH_C50
    
        Earth un-normalized fifth zonal coefficient from EGM96 model: 2.27296082868698e-7.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EGM96_EARTH_C60: typing.ClassVar[float] = ...
    """
    static final double EGM96_EARTH_C60
    
        Earth un-normalized sixth zonal coefficient from EGM96 model: -5.40681239107085e-7.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRIM5C1_EARTH_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double GRIM5C1_EARTH_EQUATORIAL_RADIUS
    
        Earth equatorial radius from GRIM5C1 model: 6378136.46 m.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRIM5C1_EARTH_FLATTENING: typing.ClassVar[float] = ...
    """
    static final double GRIM5C1_EARTH_FLATTENING
    
        Earth flattening from GRIM5C1 model: 1.0 / 298.25765.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRIM5C1_EARTH_ANGULAR_VELOCITY: typing.ClassVar[float] = ...
    """
    static final double GRIM5C1_EARTH_ANGULAR_VELOCITY
    
        Earth angular velocity from GRIM5C1 model: 7.292115e-5 rad/s.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRIM5C1_EARTH_MU: typing.ClassVar[float] = ...
    """
    static final double GRIM5C1_EARTH_MU
    
        Earth gravitational constant from GRIM5C1 model: 3.986004415 m :sup:`3` /s :sup:`2` .
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRIM5C1_EARTH_C20: typing.ClassVar[float] = ...
    """
    static final double GRIM5C1_EARTH_C20
    
        Earth un-normalized second zonal coefficient from GRIM5C1 model: -1.082626110612609e-3.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRIM5C1_EARTH_C30: typing.ClassVar[float] = ...
    """
    static final double GRIM5C1_EARTH_C30
    
        Earth un-normalized third zonal coefficient from GRIM5C1 model: 2.536150841690056e-6.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRIM5C1_EARTH_C40: typing.ClassVar[float] = ...
    """
    static final double GRIM5C1_EARTH_C40
    
        Earth un-normalized fourth zonal coefficient from GRIM5C1 model: 1.61936352497151e-6.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRIM5C1_EARTH_C50: typing.ClassVar[float] = ...
    """
    static final double GRIM5C1_EARTH_C50
    
        Earth un-normalized fifth zonal coefficient from GRIM5C1 model: 2.231013736607540e-7.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GRIM5C1_EARTH_C60: typing.ClassVar[float] = ...
    """
    static final double GRIM5C1_EARTH_C60
    
        Earth un-normalized sixth zonal coefficient from GRIM5C1 model: -5.402895357302363e-7.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EIGEN5C_EARTH_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double EIGEN5C_EARTH_EQUATORIAL_RADIUS
    
        Earth equatorial radius from EIGEN5C model: 6378136.46 m.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EIGEN5C_EARTH_MU: typing.ClassVar[float] = ...
    """
    static final double EIGEN5C_EARTH_MU
    
        Earth gravitational constant from EIGEN5C model: 3.986004415 m :sup:`3` /s :sup:`2` .
    
        Also see:
            :meth:`~constant`
    
    
    """
    EIGEN5C_EARTH_C20: typing.ClassVar[float] = ...
    """
    static final double EIGEN5C_EARTH_C20
    
        Earth un-normalized second zonal coefficient from EIGEN5C model: -1.082626457231767e-3.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EIGEN5C_EARTH_C30: typing.ClassVar[float] = ...
    """
    static final double EIGEN5C_EARTH_C30
    
        Earth un-normalized third zonal coefficient from EIGEN5C model: 2.532547231862799e-6.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EIGEN5C_EARTH_C40: typing.ClassVar[float] = ...
    """
    static final double EIGEN5C_EARTH_C40
    
        Earth un-normalized fourth zonal coefficient from EIGEN5C model: 1.619964434136e-6.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EIGEN5C_EARTH_C50: typing.ClassVar[float] = ...
    """
    static final double EIGEN5C_EARTH_C50
    
        Earth un-normalized fifth zonal coefficient from EIGEN5C model: 2.277928487005437e-7.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EIGEN5C_EARTH_C60: typing.ClassVar[float] = ...
    """
    static final double EIGEN5C_EARTH_C60
    
        Earth un-normalized sixth zonal coefficient from EIGEN5C model: -5.406653715879098e-7.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_GAUSSIAN_GRAVITATIONAL_CONSTANT: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_GAUSSIAN_GRAVITATIONAL_CONSTANT
    
        Gaussian gravitational constant: 0.01720209895 √(AU :sup:`3` /d :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_ASTRONOMICAL_UNIT: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_ASTRONOMICAL_UNIT
    
        Astronomical Unit: 149597870691 m.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_SUN_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_SUN_GM
    
        Sun attraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_SUN_MERCURY_MASS_RATIO: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_SUN_MERCURY_MASS_RATIO
    
        Sun/Mercury mass ratio: 6023600.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_MERCURY_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_MERCURY_GM
    
        Sun/Mercury attraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_SUN_VENUS_MASS_RATIO: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_SUN_VENUS_MASS_RATIO
    
        Sun/Venus mass ratio: 408523.71.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_VENUS_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_VENUS_GM
    
        Sun/Venus attraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_SUN_EARTH_PLUS_MOON_MASS_RATIO: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_SUN_EARTH_PLUS_MOON_MASS_RATIO
    
        Sun/(Earth + Moon) mass ratio: 328900.56.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_EARTH_PLUS_MOON_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_EARTH_PLUS_MOON_GM
    
        Sun/(Earth + Moon) attraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_EARTH_MOON_MASS_RATIO: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_EARTH_MOON_MASS_RATIO
    
        Earth/Moon mass ratio: 81.30059.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_MOON_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_MOON_GM
    
        Moon attraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_EARTH_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_EARTH_GM
    
        Earth attraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_SUN_MARS_SYSTEM_MASS_RATIO: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_SUN_MARS_SYSTEM_MASS_RATIO
    
        Sun/(Mars system) mass ratio: 3098708.0.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_MARS_SYSTEM_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_MARS_SYSTEM_GM
    
        Sun/(Mars system) attraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_SUN_JUPITER_SYSTEM_MASS_RATIO: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_SUN_JUPITER_SYSTEM_MASS_RATIO
    
        Sun/(Jupiter system) mass ratio: 1047.3486.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_JUPITER_SYSTEM_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_JUPITER_SYSTEM_GM
    
        Sun/(Jupiter system) ttraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_SUN_SATURN_SYSTEM_MASS_RATIO: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_SUN_SATURN_SYSTEM_MASS_RATIO
    
        Sun/(Saturn system) mass ratio: 3497.898.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_SATURN_SYSTEM_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_SATURN_SYSTEM_GM
    
        Sun/(Saturn system) attraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_SUN_URANUS_SYSTEM_MASS_RATIO: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_SUN_URANUS_SYSTEM_MASS_RATIO
    
        Sun/(Uranus system) mass ratio: 22902.98.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_URANUS_SYSTEM_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_URANUS_SYSTEM_GM
    
        Sun/(Uranus system) attraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_SUN_NEPTUNE_SYSTEM_MASS_RATIO: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_SUN_NEPTUNE_SYSTEM_MASS_RATIO
    
        Sun/(Neptune system) mass ratio: 19412.24.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_NEPTUNE_SYSTEM_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_NEPTUNE_SYSTEM_GM
    
        Sun/(Neptune system) attraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_SUN_PLUTO_SYSTEM_MASS_RATIO: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_SUN_PLUTO_SYSTEM_MASS_RATIO
    
        Sun/(Pluto system) mass ratio: 1.35e8.
    
        Also see:
            :meth:`~constant`
    
    
    """
    JPL_SSD_PLUTO_SYSTEM_GM: typing.ClassVar[float] = ...
    """
    static final double JPL_SSD_PLUTO_SYSTEM_GM
    
        Sun/(Pluto system) ttraction coefficient (m :sup:`3` /s :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    PERFECT_GAS_CONSTANT: typing.ClassVar[float] = ...
    """
    static final double PERFECT_GAS_CONSTANT
    
        Perfect gas constant (Jmol :sup:`-1` K :sup:`-1` .
    
        Also see:
            :meth:`~constant`
    
    
    """
    AVOGADRO_CONSTANT: typing.ClassVar[float] = ...
    """
    static final double AVOGADRO_CONSTANT
    
        Avogadro constant.
    
        Also see:
            :meth:`~constant`
    
    
    """
    CONST_SOL_W_M2: typing.ClassVar[float] = ...
    """
    static final double CONST_SOL_W_M2
    
        Solar constant (W/M**2). see "obelixtype.f90 in OBELIX software"
    
        Also see:
            :meth:`~constant`
    
    
    """
    CONST_SOL_N_M2: typing.ClassVar[float] = ...
    """
    static final double CONST_SOL_N_M2
    
        Solar constant (N/M**2). see "obelixtype.f90 in OBELIX software"
    
        Also see:
            :meth:`~constant`
    
    
    """
    CONST_SOL_STELA: typing.ClassVar[float] = ...
    """
    static final double CONST_SOL_STELA
    
        Solar Constant (N/M**2).
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_DEFAULT_LOS_CX: typing.ClassVar[float] = ...
    """
    static final double STELA_DEFAULT_LOS_CX
    
        Default drag coefficient used in MEAN_CONSTANT F107 computation.
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_LOS_K0: typing.ClassVar[float] = ...
    """
    static final double STELA_LOS_K0
    
        k0 coefficient used in MEAN_CONSTANT F107 computation.
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_LOS_K1: typing.ClassVar[float] = ...
    """
    static final double STELA_LOS_K1
    
        k1 coefficient used in MEAN_CONSTANT F107 computation.
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_LOS_K2: typing.ClassVar[float] = ...
    """
    static final double STELA_LOS_K2
    
        k2 coefficient used in MEAN_CONSTANT F107 computation.
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_LOS_F107: typing.ClassVar[float] = ...
    """
    static final double STELA_LOS_F107
    
        F10.7 constant for stela los
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_LOS_AP: typing.ClassVar[float] = ...
    """
    static final double STELA_LOS_AP
    
        AP constant for stela los
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_SPACE_OBJECT_NAME: typing.ClassVar[str] = ...
    """
    static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` STELA_SPACE_OBJECT_NAME
    
        Space object name.
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_SPACE_OBJECT_MASS: typing.ClassVar[float] = ...
    """
    static final double STELA_SPACE_OBJECT_MASS
    
        Space object mass (kg).
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_SPACE_OBJECT_MEAN_AREA: typing.ClassVar[float] = ...
    """
    static final double STELA_SPACE_OBJECT_MEAN_AREA
    
        Space object mean area (m :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_SPACE_OBJECT_REF_AREA: typing.ClassVar[float] = ...
    """
    static final double STELA_SPACE_OBJECT_REF_AREA
    
        Space object reflectivity area (m :sup:`2` ).
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_SPACE_OBJECT_REFLECT_COEF: typing.ClassVar[float] = ...
    """
    static final double STELA_SPACE_OBJECT_REFLECT_COEF
    
        Space object reflection coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_CONSTANT_DRAG_COEFFICIENT: typing.ClassVar[float] = ...
    """
    static final double STELA_CONSTANT_DRAG_COEFFICIENT
    
        Constant drag coefficient value.
    
        Also see:
            :meth:`~constant`
    
    
    """
    CRITICAL_PROGRADE_INCLINATION: typing.ClassVar[float] = ...
    """
    static final double CRITICAL_PROGRADE_INCLINATION
    
        Critical prograde inclination from 4 - 5 × sin :sup:`2` i = 0 see "Fundamentals of Astrodynamics and Applications", 3rd
        Edition, D. A. Vallado, p.646
    
    """
    CRITICAL_RETROGRADE_INCLINATION: typing.ClassVar[float] = ...
    """
    static final double CRITICAL_RETROGRADE_INCLINATION
    
        Critical retrograde inclination from 4 - 5 × sin :sup:`2` i = 0 see "Fundamentals of Astrodynamics and Applications",
        3rd Edition, D. A. Vallado, p.646
    
    """
    GRAVITATIONAL_CONSTANT: typing.ClassVar[float] = ...
    """
    static final double GRAVITATIONAL_CONSTANT
    
        Gravitational constant (CODATA): 6.67384 × 10 :sup:`-11` m :sup:`3` kg :sup:`-1` s :sup:`-2` .
    
        Also see:
            :meth:`~constant`
    
    
    """
    CGU: typing.ClassVar[float] = ...
    """
    static final double CGU
    
        OBELIX gravitational constant.
    
        Also see:
            :meth:`~constant`
    
    
    """
    SEIDELMANN_UA: typing.ClassVar[float] = ...
    """
    static final double SEIDELMANN_UA
    
        UA from the 1992 Astronomical Almanac by P. Kenneth Seidelmann.
    
        Also see:
            :meth:`~constant`
    
    
    """
    CNES_STELA_UA: typing.ClassVar[float] = ...
    """
    static final double CNES_STELA_UA
    
        UA from the 1992 Astronomical Almanac by P. Kenneth Seidelmann.
    
        Also see:
            :meth:`~constant`
    
    
    """
    CNES_STELA_AE: typing.ClassVar[float] = ...
    """
    static final double CNES_STELA_AE
    
        CNES Stela reference equatorial radius.
    
        Also see:
            :meth:`~constant`
    
    
    """
    CNES_STELA_MU: typing.ClassVar[float] = ...
    """
    static final double CNES_STELA_MU
    
        CNES Stela reference mu.
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_COOK_GAZ_CONSTANT: typing.ClassVar[float] = ...
    """
    static final double STELA_COOK_GAZ_CONSTANT
    
        Cook perfect gaz constant.
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_COOK_MOLAR_MASS_OXYGEN: typing.ClassVar[float] = ...
    """
    static final double STELA_COOK_MOLAR_MASS_OXYGEN
    
        Cook molar mass of oxygen atom.
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_COOK_WALL_TEMPERATURE: typing.ClassVar[float] = ...
    """
    static final double STELA_COOK_WALL_TEMPERATURE
    
        Cook wall temperature (K).
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_COOK_ACCOMODATION: typing.ClassVar[float] = ...
    """
    static final double STELA_COOK_ACCOMODATION
    
        Cook accomodation constant.
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_LOS_EARTH_RADIUS: typing.ClassVar[float] = ...
    """
    static final double STELA_LOS_EARTH_RADIUS
    
        LOS Earth Radius (m).
    
        Also see:
            :meth:`~constant`
    
    
    """
    STELA_Z_LIMIT_ATMOS: typing.ClassVar[float] = ...
    """
    static final double STELA_Z_LIMIT_ATMOS
    
        Altitude of the upper atmospheric boundary (m).
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_LIGHT_VELOCITY: typing.ClassVar[float] = ...
    """
    static final double IERS92_LIGHT_VELOCITY
    
        IERS92 light velocity in vacuum (meters per second) from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_UA: typing.ClassVar[float] = ...
    """
    static final double IERS92_UA
    
        IERS92 UA (m) from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_EARTH_GRAVITATIONAL_PARAMETER: typing.ClassVar[float] = ...
    """
    static final double IERS92_EARTH_GRAVITATIONAL_PARAMETER
    
        IERS92 Earth standard gravitational parameter (m :sup:`3` s :sup:`2` ) from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_EARTH_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double IERS92_EARTH_EQUATORIAL_RADIUS
    
        IERS92 Earth standard gravitational parameter (m) from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_EARTH_FLATTENING: typing.ClassVar[float] = ...
    """
    static final double IERS92_EARTH_FLATTENING
    
        IERS92 Earth flattening from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_EARTH_ROTATION_RATE: typing.ClassVar[float] = ...
    """
    static final double IERS92_EARTH_ROTATION_RATE
    
        IERS92 Earth rotation rate (rad/s) from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_EARTH_J2: typing.ClassVar[float] = ...
    """
    static final double IERS92_EARTH_J2
    
        IERS92 Earth J2 parameter from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_SUN_GRAVITATIONAL_PARAMETER: typing.ClassVar[float] = ...
    """
    static final double IERS92_SUN_GRAVITATIONAL_PARAMETER
    
        IERS92 Sun standard gravitational parameter from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_SUN_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double IERS92_SUN_EQUATORIAL_RADIUS
    
        IERS92 Sun equatorial radius from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_SUN_FLATTENING: typing.ClassVar[float] = ...
    """
    static final double IERS92_SUN_FLATTENING
    
        IERS92 Sun flattening from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_SUN_ROTATION_RATE: typing.ClassVar[float] = ...
    """
    static final double IERS92_SUN_ROTATION_RATE
    
        IERS92 Sun rotation rate from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_MOON_GRAVITATIONAL_PARAMETER: typing.ClassVar[float] = ...
    """
    static final double IERS92_MOON_GRAVITATIONAL_PARAMETER
    
        IERS92 Moon standard gravitational parameter from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_MOON_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double IERS92_MOON_EQUATORIAL_RADIUS
    
        IERS92 Moon equatorial radius from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_MOON_FLATTENING: typing.ClassVar[float] = ...
    """
    static final double IERS92_MOON_FLATTENING
    
        IERS92 Moon flattening from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    IERS92_MOON_ROTATION_RATE: typing.ClassVar[float] = ...
    """
    static final double IERS92_MOON_ROTATION_RATE
    
        IERS92 Moon rotation rate from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_LIGHT_VELOCITY: typing.ClassVar[float] = ...
    """
    static final double UAI1994_LIGHT_VELOCITY
    
        UAI1994 light velocity in vacuum (meters per second) from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_UA: typing.ClassVar[float] = ...
    """
    static final double UAI1994_UA
    
        UAI1994 UA (m) from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_PRECESSION_RATE: typing.ClassVar[float] = ...
    """
    static final double UAI1994_PRECESSION_RATE
    
        UAI1994 precession rate (arcseconds/century) from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_OBLIQUITY: typing.ClassVar[float] = ...
    """
    static final double UAI1994_OBLIQUITY
    
        UAI1994 obliquity of the ecliptic (arcseconds) from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_GRAVITATIONAL_CONSTANT: typing.ClassVar[float] = ...
    """
    static final double UAI1994_GRAVITATIONAL_CONSTANT
    
        UAI1994 gravitational constant (m :sup:`3` kg :sup:`-1` s :sup:`-2` ) from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_SOLAR_RADIATION_PRESSURE: typing.ClassVar[float] = ...
    """
    static final double UAI1994_SOLAR_RADIATION_PRESSURE
    
        UAI1994 solar radiation pressure coefficient from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_EARTH_GRAVITATIONAL_PARAMETER: typing.ClassVar[float] = ...
    """
    static final double UAI1994_EARTH_GRAVITATIONAL_PARAMETER
    
        UAI1994 Earth standard gravitational parameter from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_EARTH_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double UAI1994_EARTH_EQUATORIAL_RADIUS
    
        UAI1994 Earth standard gravitational parameter from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_EARTH_FLATTENING: typing.ClassVar[float] = ...
    """
    static final double UAI1994_EARTH_FLATTENING
    
        UAI1994 Earth flattening from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_EARTH_ROTATION_RATE: typing.ClassVar[float] = ...
    """
    static final double UAI1994_EARTH_ROTATION_RATE
    
        UAI1994 Earth rotation rate from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_EARTH_J2: typing.ClassVar[float] = ...
    """
    static final double UAI1994_EARTH_J2
    
        UAI1994 Earth J2 parameter from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_SUN_GRAVITATIONAL_PARAMETER: typing.ClassVar[float] = ...
    """
    static final double UAI1994_SUN_GRAVITATIONAL_PARAMETER
    
        UAI1994 Sun standard gravitational parameter from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_SUN_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double UAI1994_SUN_EQUATORIAL_RADIUS
    
        UAI1994 Sun equatorial radius from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_SUN_FLATTENING: typing.ClassVar[float] = ...
    """
    static final double UAI1994_SUN_FLATTENING
    
        UAI1994 Sun flattening from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_SUN_ROTATION_RATE: typing.ClassVar[float] = ...
    """
    static final double UAI1994_SUN_ROTATION_RATE
    
        UAI1994 Sun rotation rate from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_MOON_GRAVITATIONAL_PARAMETER: typing.ClassVar[float] = ...
    """
    static final double UAI1994_MOON_GRAVITATIONAL_PARAMETER
    
        UAI1994 Moon standard gravitational parameter from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_MOON_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    static final double UAI1994_MOON_EQUATORIAL_RADIUS
    
        UAI1994 Moon equatorial radius from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_MOON_FLATTENING: typing.ClassVar[float] = ...
    """
    static final double UAI1994_MOON_FLATTENING
    
        UAI1994 Moon flattening from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UAI1994_MOON_ROTATION_RATE: typing.ClassVar[float] = ...
    """
    static final double UAI1994_MOON_ROTATION_RATE
    
        UAI1994 Moon rotation rate from CNES COMPAS_Base data set.
    
        Also see:
            :meth:`~constant`
    
    
    """

class PatriusConfiguration:
    """
    public final class PatriusConfiguration extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Utility class for setting global configuration parameters.
    """
    @staticmethod
    def getCacheSlotsNumber() -> int:
        """
            Get the number of slots to use in caches.
        
            Returns:
                number of slots to use in caches
        
        
        """
        ...
    @staticmethod
    def getPatriusCompatibilityMode() -> 'PatriusConfiguration.PatriusVersionCompatibility':
        """
        
            Returns:
                the type of compatibility mode
        
        
        """
        ...
    @staticmethod
    def setCacheSlotsNumber(int: int) -> None:
        """
            Set the number of slots to use in caches.
        
            Parameters:
                slotsNumber (int): number of slots to use in caches
        
        
        """
        ...
    @staticmethod
    def setPatriusCompatibilityMode(patriusVersionCompatibility: 'PatriusConfiguration.PatriusVersionCompatibility') -> None:
        """
        
            Parameters:
                patriusCompatibilityModel (:class:`~fr.cnes.sirius.patrius.utils.PatriusConfiguration.PatriusVersionCompatibility`): the Patrius compatibility mode to set
        
        
        """
        ...
    class PatriusVersionCompatibility(java.lang.Enum['PatriusConfiguration.PatriusVersionCompatibility']):
        OLD_MODELS: typing.ClassVar['PatriusConfiguration.PatriusVersionCompatibility'] = ...
        MIXED_MODELS: typing.ClassVar['PatriusConfiguration.PatriusVersionCompatibility'] = ...
        NEW_MODELS: typing.ClassVar['PatriusConfiguration.PatriusVersionCompatibility'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'PatriusConfiguration.PatriusVersionCompatibility': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['PatriusConfiguration.PatriusVersionCompatibility']: ...

class StringTablePrinter:
    """
    public class StringTablePrinter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This utility class allows to print a table as a formatted String with dynamic columns widths.
    """
    DEFAULT_BOLD_LINE_SEPARATOR: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_BOLD_LINE_SEPARATOR
    
        The default String representing the bold line separator.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_STANDARD_LINE_SEPARATOR: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_STANDARD_LINE_SEPARATOR
    
        The default String representing the standard line separator.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_VERTICAL_SEPARATOR: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_VERTICAL_SEPARATOR
    
        The default String representing the vertical separator of the middle columns.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_LEFT_VERTICAL_SEPARATOR: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_LEFT_VERTICAL_SEPARATOR
    
        The default String representing the vertical separator of the left column.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_RIGHT_VERTICAL_SEPARATOR: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_RIGHT_VERTICAL_SEPARATOR
    
        The default String representing the vertical separator of the right column.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, string: str, stringArray: typing.Union[typing.List[str], jpype.JArray]): ...
    @typing.overload
    def __init__(self, stringArray: typing.Union[typing.List[str], jpype.JArray]): ...
    def addBoldLineSeparator(self) -> None:
        """
            Add a line full of bold separators.
        
        """
        ...
    @typing.overload
    def addLine(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], string: str) -> None:
        """
            Add the values as a line to the table.
        
            Parameters:
                values (double[]): The array describing each column value of the new line
                fmt (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): The format used to convert the double values into String
        
            Raises:
                : if the provided array does not have the same dimension than the header
        
        """
        ...
    @typing.overload
    def addLine(self, string: str, doubleArray: typing.Union[typing.List[float], jpype.JArray], string2: str) -> None:
        """
            Add the values as a line to the table.
        
        
            The first column is described by a String.
        
            Parameters:
                leftColumn (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): The first column of the line represented by a String
                values (double[]): The other columns of the line represented by double values (must have the same dimension as the header minus one, as the
                    left column is not described by this array)
                fmt (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): The format used to convert the double values into String
        
            Raises:
                : if the provided array dimension is not compatible with the header (:code:`values.length + 1 =! getNbColumns()`)
        
        
        """
        ...
    @typing.overload
    def addLine(self, stringArray: typing.Union[typing.List[str], jpype.JArray]) -> None:
        """
            Add a line to the table.
        
            Note: the given array must have the same size as the header used in the constructor (see
            :meth:`~fr.cnes.sirius.patrius.utils.StringTablePrinter.getNbColumns` ).
        
            Parameters:
                line (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`[]): The array describing each column value of the new line
        
            Raises:
                : if the provided array does not have the same dimension than the header
        
        """
        ...
    def addStandardLineSeparator(self) -> None:
        """
            Add a line full of standard separators.
        
        """
        ...
    def clear(self) -> None:
        """
            Clear the title and the table (the header remains).
        
        """
        ...
    def getBoldLineSeparator(self) -> str:
        """
            Getter for the String representing the bold line separator.
        
            Returns:
                the String representing the bold line separator
        
        
        """
        ...
    def getNbColumns(self) -> int:
        """
            Getter for the number of columns in the table.
        
            Returns:
                the number of columns in the table
        
        
        """
        ...
    def getStandardLineSeparator(self) -> str:
        """
            Getter for the String representing the standard line separator.
        
            Returns:
                the String representing the standard line separator
        
        
        """
        ...
    def getStringAlign(self) -> 'StringTablePrinter.StringAlign':
        """
            Getter for the text alignment mode.
        
            Returns:
                the text alignment mode
        
        
        """
        ...
    def getVerticalLeftSeparator(self) -> str:
        """
            Getter for the String representing the vertical separator of the left column.
        
            Returns:
                the String representing the vertical separator of the left column
        
        
        """
        ...
    def getVerticalRightSeparator(self) -> str:
        """
            Getter for the String representing the vertical separator of the right column.
        
            Returns:
                the String representing the vertical separator of the right column
        
        
        """
        ...
    def getVerticalSeparator(self) -> str:
        """
            Getter for the String representing the vertical separator of the middle columns.
        
            Returns:
                the String representing the vertical separator of the middle columns
        
        
        """
        ...
    @staticmethod
    def printDouble(double: float, string: str) -> str:
        """
            Print a double as a String in the provided format.
        
            Parameters:
                value (double): Value to print
                fmt (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): The format used to convert the double values into String
        
            Returns:
                the printed value
        
        
        """
        ...
    def setBoldLineSeparator(self, string: str) -> None:
        """
            Setter for the String representing the bold line separator.
        
            Parameters:
                boldLineSeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): String representing the bold line separator to set
        
        
        """
        ...
    def setStandardLineSeparator(self, string: str) -> None:
        """
            Setter for the String representing the standard line separator.
        
            Parameters:
                standardLineSeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): String representing the standard line separator to set
        
        
        """
        ...
    def setStringAlign(self, stringAlign: 'StringTablePrinter.StringAlign') -> None:
        """
            Setter for the text alignment mode (:meth:`~fr.cnes.sirius.patrius.utils.StringTablePrinter.StringAlign.RIGHT` by
            default).
        
            Parameters:
                stringAlign (:class:`~fr.cnes.sirius.patrius.utils.StringTablePrinter.StringAlign`): Text alignment mode to set
        
        
        """
        ...
    def setTitle(self, string: str) -> None:
        """
            Optionally, add a centered title (will be displayed before the header).
        
            Note: the title's length must be shorter than the total table width minus the left and right columns separator lengths.
        
            Parameters:
                title (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): Centered table (:code:`null` to disable)
        
        
        """
        ...
    def setVerticalLeftSeparator(self, string: str) -> None:
        """
            Setter for the String representing the vertical separator of the left column.
        
            Parameters:
                verticalLeftSeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): String representing the vertical separator of the left column to set
        
        
        """
        ...
    def setVerticalRightSeparator(self, string: str) -> None:
        """
            Setter for the String representing the vertical separator of the right column.
        
            Parameters:
                verticalRightSeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): String representing the vertical separator of the right column to set
        
        
        """
        ...
    def setVerticalSeparator(self, string: str) -> None:
        """
            Setter for the String representing the vertical separator of the middle columns.
        
            Parameters:
                verticalSeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): String representing the vertical separator of the middle columns to set
        
        
        """
        ...
    def switchLastLineBold(self) -> None:
        """
            Change the last table line into a line full of bold separators.
        
            This method can be useful when the table is built with several standard lines separator depending on conditions and we
            still want to use a bold line at the end of the table.
        
        """
        ...
    @typing.overload
    def toString(self) -> str:
        """
            Return a string representation of the formatted table.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of the formatted table
        
        """
        ...
    @typing.overload
    def toString(self, int: int) -> str:
        """
            Return a string representation of the formatted table.
        
            Parameters:
                indentation (int): Indent the array of N spaces
        
            Returns:
                a string representation of the formatted table
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NotPositiveException`: if :code:`indentation < 0`
        
        
        """
        ...
    class StringAlign(java.lang.Enum['StringTablePrinter.StringAlign']):
        LEFT: typing.ClassVar['StringTablePrinter.StringAlign'] = ...
        RIGHT: typing.ClassVar['StringTablePrinter.StringAlign'] = ...
        CENTER: typing.ClassVar['StringTablePrinter.StringAlign'] = ...
        def pad(self, string: str, int: int) -> str: ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'StringTablePrinter.StringAlign': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['StringTablePrinter.StringAlign']: ...

class TimeIt:
    """
    public class TimeIt extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class allows to perform a benchmark of a runnable function.
    """
    DEFAULT_NB_RUNS: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_NB_RUNS
    
        Default number of runs.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_WARMUP_FACTOR: typing.ClassVar[int] = ...
    """
    public static final long DEFAULT_WARMUP_FACTOR
    
        Default warmup factor.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, runnable: typing.Union[java.lang.Runnable, typing.Callable]): ...
    @typing.overload
    def __init__(self, runnable: typing.Union[java.lang.Runnable, typing.Callable], long: int, int: int, boolean: bool): ...
    @typing.overload
    def __init__(self, runnable: typing.Union[java.lang.Runnable, typing.Callable], long: int, int: int, long2: int): ...
    def getMaxTime(self) -> float:
        """
            Returns the maximum time it takes to perform the function to benchmark (evaluated on a batch of
            :meth:`~fr.cnes.sirius.patrius.utils.TimeIt.nbLoops`).
        
            Returns:
                the maximum computation time
        
        
        """
        ...
    def getMeanTime(self) -> float:
        """
            Returns the arithmetic mean of the computation time it takes to perform the function to benchmark (evaluated on a batch
            of :meth:`~fr.cnes.sirius.patrius.utils.TimeIt.nbLoops`).
        
            Returns:
                the mean
        
        
        """
        ...
    def getMinTime(self) -> float:
        """
            Returns the minimum computation time it takes to perform the function to benchmark (evaluated on a batch of
            :meth:`~fr.cnes.sirius.patrius.utils.TimeIt.nbLoops`).
        
            Returns:
                the minimum computation time
        
        
        """
        ...
    def getStandardDeviationTime(self) -> float:
        """
            Returns the standard deviation of the computation time it takes to perform the function to benchmark (evaluated on a
            batch of :meth:`~fr.cnes.sirius.patrius.utils.TimeIt.nbLoops`).
        
            Returns:
                the standard deviation
        
        
        """
        ...
    def getTimes(self) -> typing.MutableSequence[float]:
        """
            Returns the computation times it takes to perform the function to benchmark on each batch of "nbLoops" runs.
        
            Returns:
                the computation times
        
        
        """
        ...
    @staticmethod
    def loopsPerSecondEstimator(runnable: typing.Union[java.lang.Runnable, typing.Callable]) -> float:
        """
            Estimates very approximately the number of loops per seconds that can be done by the provided function.
        
            The estimation takes around 0.2 seconds (unless 1 run takes more than 0.2).
        
            Parameters:
                benchmarkFunction (`Runnable <http://docs.oracle.com/javase/8/docs/api/java/lang/Runnable.html?is-external=true>`): The function to benchmark
        
            Returns:
                the number of loops per second that can be done. Returns 1 if a loop takes more than 1 second.
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of the benchmark evaluation statistical results.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of the benchmark evaluation statistical results
        
        
        """
        ...

class TimeStampedDouble(fr.cnes.sirius.patrius.time.TimeStamped):
    """
    public class TimeStampedDouble extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
    
        An array of `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>` object that as a
        :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` attached to it.
    
        Since:
            4.13
    """
    @typing.overload
    def __init__(self, double: float, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                date attached to the object
        
        
        """
        ...
    def getDouble(self) -> float:
        """
            Getter for the double attached to the date.
        
        
            If there is a more than one component array attached, first component is returned.
        
            Returns:
                a double associated with the date
        
        
        """
        ...
    def getDoubles(self) -> typing.MutableSequence[float]:
        """
            Getter for the array of doubles.
        
            Returns:
                the doubles
        
        
        """
        ...

class TimeStampedPVCoordinates(fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, fr.cnes.sirius.patrius.time.TimeStamped):
    """
    public class TimeStampedPVCoordinates extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
    
        :class:`~fr.cnes.sirius.patrius.time.TimeStamped` version of
        :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`.
    
        Instances of this class are guaranteed to be immutable.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double2: float, pVCoordinates2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double2: float, pVCoordinates2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double3: float, pVCoordinates3: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double2: float, pVCoordinates2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double3: float, pVCoordinates3: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double4: float, pVCoordinates4: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fieldVector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.FieldVector3D[fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure]): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates): ...
    @staticmethod
    def buildInterpolationFunction(timeStampedPVCoordinatesArray: typing.Union[typing.List['TimeStampedPVCoordinates'], jpype.JArray], int: int, int2: int, cartesianDerivativesFilter: CartesianDerivativesFilter, boolean: bool) -> java.util.function.Function[fr.cnes.sirius.patrius.time.AbsoluteDate, 'TimeStampedPVCoordinates']: ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates.equals` in
                class :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`
        
        
        """
        ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                date attached to the object
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates.hashCode` in
                class :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`
        
        
        """
        ...
    @staticmethod
    def interpolate(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, cartesianDerivativesFilter: CartesianDerivativesFilter, collection: typing.Union[java.util.Collection['TimeStampedPVCoordinates'], typing.Sequence['TimeStampedPVCoordinates'], typing.Set['TimeStampedPVCoordinates']]) -> 'TimeStampedPVCoordinates': ...
    def shiftedBy(self, double: float) -> 'TimeStampedPVCoordinates':
        """
            Get a time-shifted state.
        
            The state can be slightly shifted to close dates. This shift is based on a simple Taylor expansion. It is *not* intended
            as a replacement for proper orbit propagation (it is not even Keplerian!) but should be sufficient for either small time
            shifts or coarse accuracy.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeShiftable.shiftedBy` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeShiftable`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates.shiftedBy` in
                class :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`
        
            Parameters:
                dt (double): time shift in seconds
        
            Returns:
                a new state, shifted with respect to the instance (which is immutable)
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.AbsoluteDate.shiftedBy`,
                :meth:`~fr.cnes.sirius.patrius.attitudes.Attitude.shiftedBy`, :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.shiftedBy`,
                :meth:`~fr.cnes.sirius.patrius.propagation.SpacecraftState.shiftedBy`
        
        
        """
        ...
    def toString(self) -> str:
        """
            Return a string representation of this position/velocity pair.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates.toString` in
                class :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`
        
            Returns:
                string representation of this position/velocity pair
        
        
        """
        ...

class TimeStampedString(fr.cnes.sirius.patrius.time.TimeStamped):
    """
    public class TimeStampedString extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
    
        An array of `null <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` object that as a
        :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` attached to it.
    """
    @typing.overload
    def __init__(self, string: str, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, stringArray: typing.Union[typing.List[str], jpype.JArray], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                date attached to the object
        
        
        """
        ...
    def getString(self) -> str:
        """
            Get the string (first component of the array if it was constructed with an array).
        
            Returns:
                the string
        
        
        """
        ...
    def getStrings(self) -> typing.MutableSequence[str]:
        """
            Get the strings.
        
            Returns:
                the array of strings
        
        
        """
        ...

class UtilsPatrius:
    """
    public final class UtilsPatrius extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Epsilon constants
    
        Since:
            1.1
    """
    EPSILON: typing.ClassVar[float] = ...
    """
    public static final double EPSILON
    
        Smallest positive number such that 1 - EPSILON is not numerically equal to 1.
    
    """
    DOUBLE_COMPARISON_EPSILON: typing.ClassVar[float] = ...
    """
    public static final double DOUBLE_COMPARISON_EPSILON
    
        Epsilon used for doubles relative comparison
    
        Also see:
            :meth:`~constant`
    
    
    """
    GEOMETRY_EPSILON: typing.ClassVar[float] = ...
    """
    public static final double GEOMETRY_EPSILON
    
        Epsilon for the geometry aspects.
    
        Also see:
            :meth:`~constant`
    
    
    """

class TimeStampedAngularCoordinates(AngularCoordinates, fr.cnes.sirius.patrius.time.TimeStamped, java.lang.Comparable['TimeStampedAngularCoordinates']):
    """
    public class TimeStampedAngularCoordinates extends :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates`>
    
        :class:`~fr.cnes.sirius.patrius.time.TimeStamped` version of :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`.
    
        Instances of this class are guaranteed to be immutable.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates3: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates4: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates3: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates4: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double: float, boolean: bool): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, angularCoordinates: AngularCoordinates): ...
    @typing.overload
    def addOffset(self, angularCoordinates: AngularCoordinates) -> 'TimeStampedAngularCoordinates':
        """
            Add an offset from the instance.
        
            We consider here that the offset rotation is applied first and the instance is applied afterward. Note that angular
            coordinates do *not* commute under this operation, i.e. :code:`a.addOffset(b)` and :code:`b.addOffset(a)` lead to
            *different* results in most cases.
        
            The two methods :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.addOffset` and
            :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.subtractOffset` are designed so that round trip
            applications are possible. This means that both :code:`ac1.subtractOffset(ac2).addOffset(ac2)` and
            :code:`ac1.addOffset(ac2).subtractOffset(ac2)` return angular coordinates equal to ac1.
        
            **Warning:**spin derivative is not computed.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.addOffset` in
                class :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`
        
            Parameters:
                offset (:class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`): offset to subtract
        
            Returns:
                new instance, with offset subtracted
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.subtractOffset`
        
            Add an offset from the instance.
        
            We consider here that the offset rotation is applied first and the instance is applied afterward. Note that angular
            coordinates do *not* commute under this operation, i.e. :code:`a.addOffset(b)` and :code:`b.addOffset(a)` lead to
            *different* results in most cases.
        
            The two methods :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.addOffset` and
            :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.subtractOffset` are designed so that round trip
            applications are possible. This means that both :code:`ac1.subtractOffset(ac2).addOffset(ac2)` and
            :code:`ac1.addOffset(ac2).subtractOffset(ac2)` return angular coordinates equal to ac1.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.addOffset` in
                class :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`
        
            Parameters:
                offset (:class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`): offset to subtract
                computeSpinDerivatives (boolean): true if spin derivatives should be computed. If not, spin derivative is set to *null*
        
            Returns:
                new instance, with offset subtracted
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.subtractOffset`
        
        
        """
        ...
    @typing.overload
    def addOffset(self, angularCoordinates: AngularCoordinates, boolean: bool) -> 'TimeStampedAngularCoordinates': ...
    def compareTo(self, timeStampedAngularCoordinates: 'TimeStampedAngularCoordinates') -> int:
        """
            Compare this time stamped angular coordinates with another time stamped angular coordinates.
        
            The time stamped angular coordinates are compared with respect to their dates, by chronological order.
        
        
            If they are defined at the same date, they are then compared with respect to their hashCode.
        
        
            This hashCode comparison is arbitrary but allows to be compliant with the equals method, i.e. this method returns 0 only
            if the time stamped angular coordinates are equal.
        
            Specified by:
                 in interface 
        
            Parameters:
                orientation (:class:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates`): other time stamped angular coordinates to compare the instance to
        
            Returns:
        
                  - a negative integer: when this time stamped angular coordinates is before, or simultaneous with a lower hashCode
                  - zero: when this time stamped angular coordinates is simultaneous and with the same hashCode
                  - a positive integer: when this time stamped angular coordinates is after, or simultaneous with a higher hashCode
        
        
            Raises:
                : if the two compared time stamped angular coordinates have the same date, the same hashCode, but aren't equal (very
                    unlikely situation)
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.equals` in
                class :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`
        
        
        """
        ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                date attached to the object
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.hashCode` in
                class :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def interpolate(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, angularDerivativesFilter: AngularDerivativesFilter, collection: typing.Union[java.util.Collection['TimeStampedAngularCoordinates'], typing.Sequence['TimeStampedAngularCoordinates'], typing.Set['TimeStampedAngularCoordinates']]) -> 'TimeStampedAngularCoordinates': ...
    @typing.overload
    @staticmethod
    def interpolate(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, angularDerivativesFilter: AngularDerivativesFilter, collection: typing.Union[java.util.Collection['TimeStampedAngularCoordinates'], typing.Sequence['TimeStampedAngularCoordinates'], typing.Set['TimeStampedAngularCoordinates']], boolean: bool) -> 'TimeStampedAngularCoordinates': ...
    @typing.overload
    def revert(self) -> 'TimeStampedAngularCoordinates':
        """
            Revert a rotation/rotation rate/rotation acceleration triplet. Build a triplet which reverse the effect of another
            triplet.
        
            **Warning:**spin derivative is not computed.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.revert` in
                class :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`
        
            Returns:
                a new triplet whose effect is the reverse of the effect of the instance
        
        
        """
        ...
    @typing.overload
    def revert(self, boolean: bool) -> 'TimeStampedAngularCoordinates':
        """
            Revert a rotation/rotation rate/rotation acceleration triplet. Build a triplet which reverse the effect of another
            triplet.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.revert` in
                class :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`
        
            Parameters:
                computeSpinDerivative (boolean): true if spin derivative should be computed. If not, spin derivative is set to *null*
        
            Returns:
                a new triplet whose effect is the reverse of the effect of the instance
        
        """
        ...
    @typing.overload
    def shiftedBy(self, double: float) -> 'TimeStampedAngularCoordinates':
        """
            Get a time-shifted state.
        
            The state can be slightly shifted to close dates. This shift is based on an approximate solution of the fixed
            acceleration motion. It is *not* intended as a replacement for proper attitude propagation but should be sufficient for
            either small time shifts or coarse accuracy.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.shiftedBy` in
                class :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`
        
            Parameters:
                dt (double): time shift in seconds
                computeSpinDerivative (boolean): true if spin derivative should be computed. If not, spin derivative is set to *null*
        
            Returns:
                a new state, shifted with respect to the instance (which is immutable)
        
            Get a time-shifted state.
        
            The state can be slightly shifted to close dates. This shift is based on an approximate solution of the fixed
            acceleration motion. It is *not* intended as a replacement for proper attitude propagation but should be sufficient for
            either small time shifts or coarse accuracy.
        
            **Warning:**spin derivative is not computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeShiftable.shiftedBy` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeShiftable`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.shiftedBy` in
                class :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`
        
            Parameters:
                dt (double): time shift in seconds
        
            Returns:
                a new state, shifted with respect to the instance (which is immutable)
        
        
        """
        ...
    @typing.overload
    def shiftedBy(self, double: float, boolean: bool) -> 'TimeStampedAngularCoordinates': ...
    @typing.overload
    def subtractOffset(self, angularCoordinates: AngularCoordinates) -> 'TimeStampedAngularCoordinates':
        """
            Subtract an offset from the instance.
        
            We consider here that the offset rotation is applied first and the instance is applied afterward. Note that angular
            coordinates do *not* commute under this operation, i.e. :code:`a.subtractOffset(b)` and :code:`b.subtractOffset(a)` lead
            to *different* results in most cases.
        
            The two methods :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.addOffset` and
            :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.subtractOffset` are designed so that round trip
            applications are possible. This means that both :code:`ac1.subtractOffset(ac2).addOffset(ac2)` and
            :code:`ac1.addOffset(ac2).subtractOffset(ac2)` return angular coordinates equal to ac1.
        
            **Warning:**spin derivative is not computed.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.subtractOffset` in
                class :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`
        
            Parameters:
                offset (:class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`): offset to subtract
        
            Returns:
                new instance, with offset subtracted
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.addOffset`
        
            Subtract an offset from the instance.
        
            We consider here that the offset rotation is applied first and the instance is applied afterward. Note that angular
            coordinates do *not* commute under this operation, i.e. :code:`a.subtractOffset(b)` and :code:`b.subtractOffset(a)` lead
            to *different* results in most cases.
        
            The two methods :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.addOffset` and
            :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.subtractOffset` are designed so that round trip
            applications are possible. This means that both :code:`ac1.subtractOffset(ac2).addOffset(ac2)` and
            :code:`ac1.addOffset(ac2).subtractOffset(ac2)` return angular coordinates equal to ac1.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.subtractOffset` in
                class :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`
        
            Parameters:
                offset (:class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`): offset to subtract
                computeSpinDerivatives (boolean): true if spin derivatives should be computed. If not, spin derivative is set to *null*
        
            Returns:
                new instance, with offset subtracted
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.utils.TimeStampedAngularCoordinates.addOffset`
        
        
        """
        ...
    @typing.overload
    def subtractOffset(self, angularCoordinates: AngularCoordinates, boolean: bool) -> 'TimeStampedAngularCoordinates': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.utils")``.

    AngularCoordinates: typing.Type[AngularCoordinates]
    AngularDerivativesFilter: typing.Type[AngularDerivativesFilter]
    CartesianDerivativesFilter: typing.Type[CartesianDerivativesFilter]
    Constants: typing.Type[Constants]
    PatriusConfiguration: typing.Type[PatriusConfiguration]
    StringTablePrinter: typing.Type[StringTablePrinter]
    TimeIt: typing.Type[TimeIt]
    TimeStampedAngularCoordinates: typing.Type[TimeStampedAngularCoordinates]
    TimeStampedDouble: typing.Type[TimeStampedDouble]
    TimeStampedPVCoordinates: typing.Type[TimeStampedPVCoordinates]
    TimeStampedString: typing.Type[TimeStampedString]
    UtilsPatrius: typing.Type[UtilsPatrius]
    exception: fr.cnes.sirius.patrius.utils.exception.__module_protocol__
    legs: fr.cnes.sirius.patrius.utils.legs.__module_protocol__
    serializablefunction: fr.cnes.sirius.patrius.utils.serializablefunction.__module_protocol__
