
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.analysis.differentiation
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.utils
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import jpype
import typing



class GNSSParameters(java.io.Serializable):
    """
    public class GNSSParameters extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        This class is a simple container for generic ephemeris description parameters of GNSS satellites (almanac or broadcast
        model ephemeris).
    
        Also see:
            :meth:`~serialized`
    """
    def getAf0(self) -> float:
        """
        
            Returns:
                the Clock correcting parameter af0 (s)
        
        
        """
        ...
    def getAf1(self) -> float:
        """
        
            Returns:
                the Clock correcting parameter af1 (s/s)
        
        
        """
        ...
    def getAf2(self) -> float:
        """
        
            Returns:
                the Clock correcting parameter af2 (s/s^2)
        
        
        """
        ...
    def getCic(self) -> float:
        """
        
            Returns:
                the Amplitude of the cosine harmonic correction term to the angle of inclination (rad)
        
        
        """
        ...
    def getCis(self) -> float:
        """
        
            Returns:
                the Amplitude of the sine harmonic correction term to the angle of inclination (rad)
        
        
        """
        ...
    def getCrc(self) -> float:
        """
        
            Returns:
                the Amplitude of the cosine harmonic correction term to the orbit radius (m)
        
        
        """
        ...
    def getCrs(self) -> float:
        """
        
            Returns:
                the Amplitude of the sine harmonic correction term to the orbit radius (m)
        
        
        """
        ...
    def getCuc(self) -> float:
        """
        
            Returns:
                the Amplitude of the cosine harmonic correction term to the argument of latitude (rad)
        
        
        """
        ...
    def getCus(self) -> float:
        """
        
            Returns:
                the Amplitude of the sine harmonic correction term to the argument of latitude (rad)
        
        
        """
        ...
    def getDeltaN(self) -> float:
        """
        
            Returns:
                the Mean motion difference from computed value (rad/s)
        
        
        """
        ...
    def getDeltaNRate(self) -> float:
        """
        
            Returns:
                the Rate of mean motion difference from computed value (rad/s^2)
        
        
        """
        ...
    def getEccentricity(self) -> float:
        """
        
            Returns:
                the eccentricity
        
        
        """
        ...
    def getGnssType(self) -> 'GNSSType':
        """
        
            Returns:
                the gnssType
        
        
        """
        ...
    def getI(self) -> float:
        """
        
            Returns:
                the orbital inclination
        
        
        """
        ...
    def getMeanAnomalyInit(self) -> float:
        """
        
            Returns:
                the initial mean anomaly
        
        
        """
        ...
    def getOmegaInit(self) -> float:
        """
        
            Returns:
                the initial right ascension of ascending node
        
        
        """
        ...
    def getOmegaRate(self) -> float:
        """
        
            Returns:
                the Rate of right ascension
        
        
        """
        ...
    def getSqrtA(self) -> float:
        """
        
            Returns:
                the square root of the semi-major axis
        
        
        """
        ...
    def getW(self) -> float:
        """
        
            Returns:
                the Argument of perigee
        
        
        """
        ...
    def getaRate(self) -> float:
        """
        
            Returns:
                the Change rate in semi-major axis (m/s)
        
        
        """
        ...
    def getiRate(self) -> float:
        """
        
            Returns:
                the Rate of inclination angle (rad/s)
        
        
        """
        ...
    def gettRef(self) -> float:
        """
        
            Returns:
                the number of seconds in the week
        
        
        """
        ...

class GNSSType(java.lang.Enum['GNSSType']):
    """
    public enum GNSSType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.GNSSType`>
    
        Enumerate for GNSS satellites type
    """
    GPS: typing.ClassVar['GNSSType'] = ...
    Galileo: typing.ClassVar['GNSSType'] = ...
    BeiDou: typing.ClassVar['GNSSType'] = ...
    def getEarthRotationRate(self) -> float:
        """
        
            Returns:
                the earthRotationRate (rad/s)
        
        
        """
        ...
    def getEpochDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
        
            Returns:
                the epoch date
        
        
        """
        ...
    def getMu(self) -> float:
        """
        
            Returns:
                the standard gravitational parameter (m^3/s^2) (m^3/s^2)
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'GNSSType':
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
    def values() -> typing.MutableSequence['GNSSType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (GNSSType c : GNSSType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class JacobianTransformationMatrix:
    """
    public final class JacobianTransformationMatrix extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class to define jacobian transformation matrix
    
        Since:
            4.1
    """
    @staticmethod
    def getJacobianCartesianToSpheric(pVCoordinates: 'PVCoordinates') -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @staticmethod
    def getJacobianSphericToCartesian(pVCoordinates: 'PVCoordinates') -> typing.MutableSequence[typing.MutableSequence[float]]: ...

class PVCoordinates(fr.cnes.sirius.patrius.time.TimeShiftable['PVCoordinates'], java.io.Serializable):
    """
    public class PVCoordinates extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeShiftable`<:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        Simple container for Position/Velocity/Acceleration triplets.
    
        The state can be slightly shifted to close dates. This shift is based on a simple quadratic model. It is *not* intended
        as a replacement for proper orbit propagation (it is not even Keplerian!) but should be sufficient for either small time
        shifts or coarse accuracy.
    
        This class is the angular counterpart to :class:`~fr.cnes.sirius.patrius.utils.AngularCoordinates`.
    
        Instances of this class are guaranteed to be immutable.
    
        Also see:
            :meth:`~serialized`
    """
    ZERO: typing.ClassVar['PVCoordinates'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates` ZERO
    
        Fixed position/velocity/acceleration at origin (both p, v and a are zero vectors).
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, double: float, pVCoordinates: 'PVCoordinates'): ...
    @typing.overload
    def __init__(self, double: float, pVCoordinates: 'PVCoordinates', double2: float, pVCoordinates2: 'PVCoordinates'): ...
    @typing.overload
    def __init__(self, double: float, pVCoordinates: 'PVCoordinates', double2: float, pVCoordinates2: 'PVCoordinates', double3: float, pVCoordinates3: 'PVCoordinates'): ...
    @typing.overload
    def __init__(self, double: float, pVCoordinates: 'PVCoordinates', double2: float, pVCoordinates2: 'PVCoordinates', double3: float, pVCoordinates3: 'PVCoordinates', double4: float, pVCoordinates4: 'PVCoordinates'): ...
    @typing.overload
    def __init__(self, fieldVector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.FieldVector3D[fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure]): ...
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, pVCoordinates: 'PVCoordinates', pVCoordinates2: 'PVCoordinates'): ...
    @staticmethod
    def crossProduct(pVCoordinates: 'PVCoordinates', pVCoordinates2: 'PVCoordinates') -> 'PVCoordinates':
        """
            Compute the cross-product of two instances. Computing the cross-products of two PVCoordinates means computing the first
            and second derivatives of the cross product of their positions. Therefore, this does not return a position, velocity,
            acceleration.
        
            Parameters:
                pv1 (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`): first instances
                pv2 (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`): second instances
        
            Returns:
                the cross product v1 ^ v2 as a new instance
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @staticmethod
    def estimateVelocity(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Estimate velocity between two positions.
        
            Estimation is based on a simple fixed velocity translation during the time interval between the two positions.
        
            Parameters:
                start (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): start position
                end (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): end position
                dt (double): time elapsed between the dates of the two positions
        
            Returns:
                velocity allowing to go from start to end positions
        
        
        """
        ...
    def getAcceleration(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the acceleration.
        
            Returns:
                the acceleration vector (m/s²).
        
        
        """
        ...
    def getAngularVelocity(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the angular velocity (spin) of this point as seen from the origin.
        
            The angular velocity vector is parallel to the
            :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates.getMomentum` and is computed by ω = p × v / ||p||²
        
            Returns:
                the angular velocity vector
        
            Also see:
                `Angular Velocity on Wikipedia <http://en.wikipedia.org/wiki/Angular_velocity>`
        
        
        """
        ...
    def getMomentum(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the momentum.
        
            This vector is the p ⊗ v where p is position, v is velocity and ⊗ is cross product. To get the real physical angular
            momentum you need to multiply this vector by the mass.
        
            The returned vector is recomputed each time this method is called, it is not cached.
        
            Returns:
                a new instance of the momentum vector (m :sup:`2` /s).
        
        
        """
        ...
    def getPosition(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the position.
        
            Returns:
                the position vector (m).
        
        
        """
        ...
    def getVelocity(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the velocity.
        
            Returns:
                the velocity vector (m/s).
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def negate(self) -> 'PVCoordinates':
        """
            Get the opposite of the instance.
        
            Returns:
                a new position-velocity which is opposite to the instance
        
        
        """
        ...
    def normalize(self) -> 'PVCoordinates':
        """
            Normalize the position part of the instance.
        
            The computed coordinates first component (position) will be a normalized vector, the second component (velocity) will be
            the derivative of the first component (hence it will generally not be normalized), and the third component
            (acceleration) will be the derivative of the second component (hence it will generally not be normalized).
        
            Returns:
                a new instance, with first component normalized and remaining component computed to have consistent derivatives
        
        
        """
        ...
    def shiftedBy(self, double: float) -> 'PVCoordinates':
        """
            Get a time-shifted state.
        
            The state can be slightly shifted to close dates. This shift is based on a simple Taylor expansion. It is *not* intended
            as a replacement for proper orbit propagation (it is not even Keplerian!) but should be sufficient for either small time
            shifts or coarse accuracy.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeShiftable.shiftedBy` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeShiftable`
        
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
    def toArray(self, boolean: bool) -> typing.MutableSequence[float]:
        """
            Get the vector PV coordinates as a dimension 9 or 6 array (if the acceleration is or is not included).
        
            Parameters:
                withAcceleration (boolean): Indicates if the acceleration data should be included (length = 9) or not (length = 6)
        
            Returns:
                vector PV coordinates
        
            Raises:
                : if the acceleration should be returned but it is not initialized
        
        
        """
        ...
    def toDerivativeStructureVector(self, int: int) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.FieldVector3D[fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure]: ...
    def toString(self) -> str:
        """
            Return a string representation of this position/velocity/acceleration triplet.
        
            Overrides:
                 in class 
        
            Returns:
                string representation of this position/velocity/acceleration triplet
        
        
        """
        ...

class PVCoordinatesProvider(java.io.Serializable):
    """
    public interface PVCoordinatesProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for PV coordinates providers.
    
        The PV coordinates provider interface can be used by any class used for position/velocity computation, for example
        celestial bodies or spacecraft position/velocity propagators, and many others...
    """
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.Frame: ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> PVCoordinates: ...

class Position(java.io.Serializable):
    """
    public interface Position extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        Since:
            1.0
    """
    def getPosition(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the position.
        
            Returns:
                the position vector.
        
        
        """
        ...

class AbstractBoundedPVProvider(PVCoordinatesProvider):
    """
    public abstract class AbstractBoundedPVProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
    
        This abstract class shall be extended to provides a PVCoordinates provider based on manipulation of PVCoordinates
        ephemeris. The method of the implemented interface
        :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider` is not implemented here and have to be
        implemented in extending classes to provide a position velocity for a given date.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, pVCoordinatesArray: typing.Union[typing.List[PVCoordinates], jpype.JArray], int: int, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.time.AbsoluteDate], jpype.JArray], iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex): ...
    @typing.overload
    def __init__(self, spacecraftStateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.propagation.SpacecraftState], jpype.JArray], int: int, iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex): ...
    def getDateRef(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the reference date.
        
            Returns:
                dateRef
        
        
        """
        ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Getter for the reference frame.
        
            Returns:
                pvFrame
        
        
        """
        ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Return the higher date authorized to call
            :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider.getPVCoordinates`.
        
            Returns:
                maximum ephemeris date
        
        
        """
        ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Return the lower date authorized to call
            :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider.getPVCoordinates`.
        
            Returns:
                minimum ephemeris date
        
        
        """
        ...
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the native frame, i.e. the raw frame in which PVCoordinates are expressed before transformation to user output
            frame.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider.getNativeFrame` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                the native frame
        
        
        """
        ...
    def getPreviousIndex(self) -> int:
        """
            Getter for the previous search index.
        
            Returns:
                previousIndex
        
        
        """
        ...
    def getSearchIndex(self) -> fr.cnes.sirius.patrius.math.utils.ISearchIndex:
        """
            Getter for the optimize index search algorithm.
        
            Returns:
                searchIndex
        
        
        """
        ...
    def indexValidity(self, int: int) -> int: ...

class AlmanacGNSSParameters(GNSSParameters):
    """
    public class AlmanacGNSSParameters extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.GNSSParameters`
    
    
        This class is a simple container for an almanac ephemeris description parameters of GNSS satellites (GPS, Galileo or
        BeiDou)
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, gNSSType: GNSSType, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float, double10: float): ...

class CNAVGNSSParameters(GNSSParameters):
    """
    public class CNAVGNSSParameters extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.GNSSParameters`
    
    
        This class is a simple container for a broadcast model CNAV ephemeris description parameters of GNSS satellites (GPS or
        BeiDou only)
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, gNSSType: GNSSType, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float, double10: float, double11: float, double12: float, double13: float, double14: float, double15: float, double16: float, double17: float, double18: float, double19: float, double20: float, double21: float): ...

class CardanMountPosition(Position):
    """
    public final class CardanMountPosition extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.Position`
    
    
        Since:
            1.0
    
        Also see:
            :meth:`~serialized`
    """
    ZERO: typing.ClassVar['CardanMountPosition'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.CardanMountPosition` ZERO
    
        Fixed position at origin (p is zero vector).
    
    """
    def __init__(self, double: float, double2: float, double3: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getPosition(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the position.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.Position.getPosition` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.Position`
        
            Returns:
                the position vector.
        
        
        """
        ...
    def getRange(self) -> float:
        """
            Get the range.
        
            Returns:
                the range
        
        
        """
        ...
    def getXangle(self) -> float:
        """
            Get the x angle.
        
            Returns:
                x angle
        
        
        """
        ...
    def getYangle(self) -> float:
        """
            Get the y angle.
        
            Returns:
                y angle
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def toString(self) -> str:
        """
            Produces the following String representation of the Cardan mount : (x angle, y angle, range).
        
            Overrides:
                 in class 
        
            Returns:
                string representation of this position
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#toString-->`
        
        
        """
        ...

class ConstantPVCoordinatesProvider(PVCoordinatesProvider):
    """
    public class ConstantPVCoordinatesProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
    
        This class implements the :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider` to store the
        position and the velocity of an object and the frame used for computation.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, pVCoordinates: PVCoordinates, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.Frame: ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> PVCoordinates: ...

class GNSSPVCoordinates(PVCoordinatesProvider):
    """
    public class GNSSPVCoordinates extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
    
    
        This class implements the PVCoordinatesProvider to compute position velocity of a GPS, Galileo or BeiDou constellation
        satellite from its almanac/broadcast model parameters.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, gNSSParameters: GNSSParameters, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    def getClockCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the correction term for the offset of the satellite's transmission time of signal
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Position's date
        
            Returns:
                the clock correction
        
        
        """
        ...
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.Frame: ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> PVCoordinates: ...
    def getRelativisticCorrection(self, double: float) -> float:
        """
            Compute the relativistic correction term for the satellite time correction
        
            Parameters:
                timek (double): time gap between the time of applicability (tref) and the time of the sought position
        
            Returns:
                the relativistic correction of the clock
        
        
        """
        ...

class LNAVGNSSParameters(GNSSParameters):
    """
    public class LNAVGNSSParameters extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.GNSSParameters`
    
    
        This class is a simple container for a broadcast model LNAV ephemeris description parameters of GNSS satellites (GPS,
        Galileo or BeiDou)
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, gNSSType: GNSSType, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float, double10: float, double11: float, double12: float, double13: float, double14: float, double15: float, double16: float, double17: float, double18: float, double19: float): ...

class PV(Position):
    """
    public interface PV extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.Position`
    
    
        Since:
            1.0
    """
    def getVelocity(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the velocity.
        
            Returns:
                the velocity vector.
        
        
        """
        ...

class TopocentricPosition(Position):
    """
    public final class TopocentricPosition extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.Position`
    
    
        Since:
            1.0
    
        Also see:
            :meth:`~serialized`
    """
    ZERO: typing.ClassVar['TopocentricPosition'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.TopocentricPosition` ZERO
    
        Fixed position at origin (p is zero vector).
    
    """
    def __init__(self, double: float, double2: float, double3: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getAzimuth(self) -> float:
        """
            Get the azimuth angle.
        
            Returns:
                azimuth angle
        
        
        """
        ...
    def getElevation(self) -> float:
        """
            Get the elevation angle.
        
            Returns:
                elevation angle
        
        
        """
        ...
    def getPosition(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the position.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.Position.getPosition` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.Position`
        
            Returns:
                the position vector.
        
        
        """
        ...
    def getRange(self) -> float:
        """
            Get the range.
        
            Returns:
                the range
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def toString(self) -> str:
        """
            Produces the following String representation of the topocentric coordinates : (elevation, azimuth, range).
        
            Overrides:
                 in class 
        
            Returns:
                string representation of this position
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#toString-->`
        
        
        """
        ...

class AbstractEphemerisPvHermiteLagrange(AbstractBoundedPVProvider):
    """
    public abstract class AbstractEphemerisPvHermiteLagrange extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.AbstractBoundedPVProvider`
    
        Abstract class defining common methods and elements for an interpolation of an ephemeris PV via Lagrange-Hermite
        methods.
    
        Also see:
            :meth:`~serialized`
    """
    ...

class CardanMountPV(PV):
    """
    public final class CardanMountPV extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PV`
    
    
        Since:
            1.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getCardanMountPosition(self) -> CardanMountPosition:
        """
            Get the Cardan mount position.
        
            Returns:
                the Cardan mount position.
        
        
        """
        ...
    def getPosition(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the position.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.Position.getPosition` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.Position`
        
            Returns:
                the position vector.
        
        
        """
        ...
    def getRange(self) -> float:
        """
            Get the range.
        
            Returns:
                the range.
        
        
        """
        ...
    def getRangeRate(self) -> float:
        """
            Get the range rate.
        
            Returns:
                the range rate.
        
        
        """
        ...
    def getVelocity(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the velocity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PV.getVelocity` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PV`
        
            Returns:
                the velocity vector.
        
        
        """
        ...
    def getXangle(self) -> float:
        """
            Get the angle of the rotation around the local North axis.
        
            Returns:
                the x angle.
        
        
        """
        ...
    def getXangleRate(self) -> float:
        """
            Get the angle rate of the rotation around the North axis.
        
            Returns:
                the x angle rate.
        
        
        """
        ...
    def getYangle(self) -> float:
        """
            Get the angle of the rotation around y' axis. Y' axis is the image of the West axis by the first rotation around the
            North axis.
        
            Returns:
                the y angle.
        
        
        """
        ...
    def getYangleRate(self) -> float:
        """
            Get the angle rate of the rotation around y' axis (which is the image of the West axis by the first rotation around the
            North axis).
        
            Returns:
                the y angle rate.
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def toString(self) -> str:
        """
            Produces the following String representation of the Topocentric coordinates : (x angle, y angle, range, x angle rate, y
            angle rate, range rate).
        
            Overrides:
                 in class 
        
            Returns:
                string representation of this position/velocity
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#toString-->`
        
        
        """
        ...

class TopocentricPV(PV):
    """
    public final class TopocentricPV extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PV`
    
    
        Since:
            1.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getAzimuth(self) -> float:
        """
            Get the azimuth angle.
        
            Returns:
                azimuth angle
        
        
        """
        ...
    def getAzimuthRate(self) -> float:
        """
            Get the azimuth rate.
        
            Returns:
                the azimuth rate
        
        
        """
        ...
    def getElevation(self) -> float:
        """
            Get the elevation angle.
        
            Returns:
                elevation angle
        
        
        """
        ...
    def getElevationRate(self) -> float:
        """
            Get the elevation rate.
        
            Returns:
                the elevation rate
        
        
        """
        ...
    def getPosition(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the position.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.Position.getPosition` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.Position`
        
            Returns:
                the position vector.
        
        
        """
        ...
    def getRange(self) -> float:
        """
            Get the range.
        
            Returns:
                the range
        
        
        """
        ...
    def getRangeRate(self) -> float:
        """
            Get the range rate.
        
            Returns:
                the range rate
        
        
        """
        ...
    def getTopocentricPosition(self) -> TopocentricPosition:
        """
            Get the Topocentric position.
        
            Returns:
                the Topocentric position.
        
        
        """
        ...
    def getVelocity(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the velocity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PV.getVelocity` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PV`
        
            Returns:
                the velocity vector.
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def toString(self) -> str:
        """
            Produces the following String representation of the Topocentric coordinates : (elevation, azimuth, range, elevation
            rate, azimuth rate, range rate).
        
            Overrides:
                 in class 
        
            Returns:
                string representation of this position/velocity
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#toString-->`
        
        
        """
        ...

class EphemerisPvHermite(AbstractEphemerisPvHermiteLagrange):
    """
    public class EphemerisPvHermite extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.AbstractEphemerisPvHermiteLagrange`
    
    
        This class extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.AbstractBoundedPVProvider` which implements
        :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider` and so provides a position velocity for a
        given date. The provided position velocity is based on a Hermite interpolation in a given position velocity ephemeris.
    
        The interpolation extracts position, velocity and eventually acceleration from the ephemeris depending on the number of
        sample points and the date to interpolate. Points extraction is based on an implementation of the ISearchIndex
        interface. This implementation should be based on a table of duration created from the date table with the duration = 0
        at the first index.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, pVCoordinatesArray: typing.Union[typing.List[PVCoordinates], jpype.JArray], vector3DArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D], jpype.JArray], frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.time.AbsoluteDate], jpype.JArray], iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex): ...
    @typing.overload
    def __init__(self, pVCoordinatesArray: typing.Union[typing.List[PVCoordinates], jpype.JArray], int: int, vector3DArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D], jpype.JArray], frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.time.AbsoluteDate], jpype.JArray], iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex): ...
    @typing.overload
    def __init__(self, spacecraftStateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.propagation.SpacecraftState], jpype.JArray], vector3DArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D], jpype.JArray], iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex): ...
    @typing.overload
    def __init__(self, spacecraftStateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.propagation.SpacecraftState], jpype.JArray], int: int, vector3DArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D], jpype.JArray], iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex): ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> PVCoordinates: ...

class EphemerisPvLagrange(AbstractEphemerisPvHermiteLagrange):
    """
    public class EphemerisPvLagrange extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.AbstractEphemerisPvHermiteLagrange`
    
    
        This class extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.AbstractBoundedPVProvider` which implements
        :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider` and so provides a position velocity for a
        given date. The provided position velocity is based on a Lagrange interpolation in a given position velocity ephemeris.
        Tabulated entries are chronologically classified.
    
        The interpolation extracts points from the ephemeris depending on the polynome order and the date to interpolate. Points
        extraction is based on an implementation of the ISearchIndex interface. This implementation should be based on a table
        of duration created from the date table with the duration = 0 at the first index.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, pVCoordinatesArray: typing.Union[typing.List[PVCoordinates], jpype.JArray], int: int, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.time.AbsoluteDate], jpype.JArray], iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex): ...
    @typing.overload
    def __init__(self, spacecraftStateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.propagation.SpacecraftState], jpype.JArray], int: int, iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex): ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> PVCoordinates: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.orbits.pvcoordinates")``.

    AbstractBoundedPVProvider: typing.Type[AbstractBoundedPVProvider]
    AbstractEphemerisPvHermiteLagrange: typing.Type[AbstractEphemerisPvHermiteLagrange]
    AlmanacGNSSParameters: typing.Type[AlmanacGNSSParameters]
    CNAVGNSSParameters: typing.Type[CNAVGNSSParameters]
    CardanMountPV: typing.Type[CardanMountPV]
    CardanMountPosition: typing.Type[CardanMountPosition]
    ConstantPVCoordinatesProvider: typing.Type[ConstantPVCoordinatesProvider]
    EphemerisPvHermite: typing.Type[EphemerisPvHermite]
    EphemerisPvLagrange: typing.Type[EphemerisPvLagrange]
    GNSSPVCoordinates: typing.Type[GNSSPVCoordinates]
    GNSSParameters: typing.Type[GNSSParameters]
    GNSSType: typing.Type[GNSSType]
    JacobianTransformationMatrix: typing.Type[JacobianTransformationMatrix]
    LNAVGNSSParameters: typing.Type[LNAVGNSSParameters]
    PV: typing.Type[PV]
    PVCoordinates: typing.Type[PVCoordinates]
    PVCoordinatesProvider: typing.Type[PVCoordinatesProvider]
    Position: typing.Type[Position]
    TopocentricPV: typing.Type[TopocentricPV]
    TopocentricPosition: typing.Type[TopocentricPosition]
