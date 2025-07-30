
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.orbits.orbitalparameters
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.time
import java.lang
import java.util
import jpype
import typing



class Orbit(fr.cnes.sirius.patrius.time.TimeStamped, fr.cnes.sirius.patrius.time.TimeShiftable['Orbit'], fr.cnes.sirius.patrius.time.TimeInterpolable['Orbit'], fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider):
    """
    public abstract class Orbit extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, :class:`~fr.cnes.sirius.patrius.time.TimeShiftable`<:class:`~fr.cnes.sirius.patrius.orbits.Orbit`>, :class:`~fr.cnes.sirius.patrius.time.TimeInterpolable`<:class:`~fr.cnes.sirius.patrius.orbits.Orbit`>, :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
    
        This class handles orbital parameters.
    
        For user convenience, both the Cartesian and the equinoctial elements are provided by this class, regardless of the
        canonical representation implemented in the derived class (which may be classical keplerian elements for example).
    
        The parameters are defined in a frame specified by the user. It is important to make sure this frame is consistent: it
        probably is inertial and centered on the central body. This information is used for example by some force models.
    
        The object :code:`OrbitalParameters` is guaranteed to be immutable.
    
        Also see:
            :meth:`~serialized`
    """
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getA(self) -> float:
        """
            Get the semi-major axis.
        
            Note that the semi-major axis is considered negative for hyperbolic orbits.
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date of orbital parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                date of the orbital parameters
        
        
        """
        ...
    def getE(self) -> float:
        """
            Get the eccentricity.
        
            Returns:
                eccentricity
        
        
        """
        ...
    def getEquinoctialEx(self) -> float:
        """
            Get the first component of the equinoctial eccentricity vector.
        
            Returns:
                first component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getEquinoctialEy(self) -> float:
        """
            Get the second component of the equinoctial eccentricity vector.
        
            Returns:
                second component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the frame in which the orbital parameters are defined.
        
            Returns:
                frame in which the orbital parameters are defined
        
        
        """
        ...
    def getHx(self) -> float:
        """
            Get hx = ix / (2 * cos(i/2)), where ix is the first component of the inclination vector. Another formulation is hx =
            tan(i/2) cos(Ω)
        
            Returns:
                first component of the inclination vector
        
        
        """
        ...
    def getHy(self) -> float:
        """
            Get hy = iy / (2 * cos(i/2)), where iy is the second component of the inclination vector. Another formulation is hy =
            tan(i/2) sin(Ω)
        
            Returns:
                second component of the inclination vector
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    @typing.overload
    def getJacobian(self, double: float, frame: fr.cnes.sirius.patrius.frames.Frame, frame2: fr.cnes.sirius.patrius.frames.Frame, orbitType: 'OrbitType', orbitType2: 'OrbitType', positionAngle: 'PositionAngle', positionAngle2: 'PositionAngle') -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    @typing.overload
    def getJacobian(self, frame: fr.cnes.sirius.patrius.frames.Frame, frame2: fr.cnes.sirius.patrius.frames.Frame, orbitType: 'OrbitType', orbitType2: 'OrbitType', positionAngle: 'PositionAngle', positionAngle2: 'PositionAngle') -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    @typing.overload
    def getJacobian(self, orbitType: 'OrbitType', orbitType2: 'OrbitType') -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Get coordinate conversion jacobian. The position is set to MEAN by default.
        
            Parameters:
                numerator (:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`): Numerator parameters.
                denominator (:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`): Denominator parameters.
        
            Returns:
                Jacobian matrix numerator / denominator.
        
            Get coordinate conversion jacobian.
        
            Parameters:
                numerator (:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`): Numerator parameters.
                denominator (:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`): Denominator parameters.
                positionAngle (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): Position Angle.
        
            Returns:
                Jacobian matrix numerator / denominator.
        
        public :class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix` getJacobian(:class:`~fr.cnes.sirius.patrius.frames.Frame` initFrame, :class:`~fr.cnes.sirius.patrius.frames.Frame` destFrame, :class:`~fr.cnes.sirius.patrius.orbits.OrbitType` initOrbitType, :class:`~fr.cnes.sirius.patrius.orbits.OrbitType` destOrbitType, :class:`~fr.cnes.sirius.patrius.orbits.PositionAngle` initAngleType, :class:`~fr.cnes.sirius.patrius.orbits.PositionAngle` destAngleType) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Computes the Jacobian of the transformation between the specified frames, orbit types and position angle types with
            respect to this orbit.
        
            The transformation is computed at the date of definition of the specified orbit. Since the Keplerian transition matrix
            is expressed in non-Cartesian coordinates, it cannot be computed for some frames (e.g. local orbital frames).
        
            Parameters:
                initFrame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the initial frame
                destFrame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the destination frame
                initOrbitType (:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`): the initial orbit type
                destOrbitType (:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`): the destination orbit type
                initAngleType (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the initial position angle
                destAngleType (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the destination position angle
        
            Returns:
                the jacobian of the transformation [6x6]
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if the orbit type conversion failed of jacobian frame conversion failed
        
        public :class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix` getJacobian(double dt, :class:`~fr.cnes.sirius.patrius.frames.Frame` initFrame, :class:`~fr.cnes.sirius.patrius.frames.Frame` destFrame, :class:`~fr.cnes.sirius.patrius.orbits.OrbitType` initOrbitType, :class:`~fr.cnes.sirius.patrius.orbits.OrbitType` destOrbitType, :class:`~fr.cnes.sirius.patrius.orbits.PositionAngle` initAngleType, :class:`~fr.cnes.sirius.patrius.orbits.PositionAngle` destAngleType) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Computes the Jacobian of the transformation between the specified frames, orbit types and position angle types with
            respect to this orbit and specified time shift.
        
            The transformation is computed at the date of definition of the specified orbit. Since the Keplerian transition matrix
            is expressed in non-Cartesian coordinates, it cannot be computed for some frames (e.g. local orbital frames).
        
            Parameters:
                dt (double): the time shift
                initFrame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the initial frame
                destFrame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the destination frame
                initOrbitType (:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`): the initial orbit type
                destOrbitType (:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`): the destination orbit type
                initAngleType (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the initial position angle
                destAngleType (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the destination position angle
        
            Returns:
                the jacobian of the transformation [6x6]
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if the orbit type conversion failed of jacobian frame conversion failed
        
        
        """
        ...
    @typing.overload
    def getJacobian(self, orbitType: 'OrbitType', orbitType2: 'OrbitType', positionAngle: 'PositionAngle') -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def getJacobianWrtCartesian(self, positionAngle: 'PositionAngle', doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None:
        """
            Compute the Jacobian of the orbital parameters with respect to the Cartesian parameters.
        
            Element :code:`jacobian[i][j]` is the derivative of parameter i of the orbit with respect to Cartesian coordinate j.
            This means each row correspond to one orbital parameter whereas columns 0 to 5 correspond to the Cartesian coordinates
            x, y, z, xDot, yDot and zDot.
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the position angle to use
                jacobian (double[][]): placeholder 6x6 (or larger) matrix to be filled with the Jacobian, if matrix is larger than 6x6, only the 6x6 upper left
                    corner will be modified
        
        
        """
        ...
    def getJacobianWrtParameters(self, positionAngle: 'PositionAngle', doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None:
        """
            Compute the Jacobian of the Cartesian parameters with respect to the orbital parameters.
        
            Element :code:`jacobian[i][j]` is the derivative of parameter i of the orbit with respect to Cartesian coordinate j.
            This means each row correspond to one orbital parameter whereas columns 0 to 5 correspond to the Cartesian coordinates
            x, y, z, xDot, yDot and zDot.
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the position angle to use
                jacobian (double[][]): placeholder 6x6 (or larger) matrix to be filled with the Jacobian, if matrix is larger than 6x6, only the 6x6 upper left
                    corner will be modified
        
        
        """
        ...
    def getKeplerianMeanMotion(self) -> float:
        """
            Get the keplerian mean motion.
        
            The keplerian mean motion is computed directly from semi major axis and central acceleration constant.
        
            Returns:
                keplerian mean motion in radians per second
        
        
        """
        ...
    def getKeplerianPeriod(self) -> float:
        """
            Get the keplerian period.
        
            The keplerian period is computed directly from semi major axis and central acceleration constant.
        
            Returns:
                keplerian period in seconds, or positive infinity for hyperbolic orbits
        
        
        """
        ...
    def getKeplerianTransitionMatrix(self, double: float) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Get keplerian transition matrix.
        
            The transition matrix for those different orbit types are equal : keplerian, equinoctial, equatorial and circular ; and
            is defined by dMda0 * IdMatrix.
        
            To compute the transition matrix for the other orbit types, we need to convert it using the Jacobian matrix between the
            equinoctial orbit type (or we could use keplerian, equatorial or circular orbit type as well, as there are identical)
            and the current orbit type.
        
            Parameters:
                dt (double): Propagation interval.
        
            Returns:
                Transition matrix given in the coordinates type of the input orbit (only valid for a position angle set to MEAN).
        
        
        """
        ...
    def getLE(self) -> float:
        """
            Get the eccentric longitude argument.
        
            Returns:
                eccentric longitude argument (rad)
        
        
        """
        ...
    def getLM(self) -> float:
        """
            Get the mean longitude argument.
        
            Returns:
                mean longitude argument (rad)
        
        
        """
        ...
    def getLv(self) -> float:
        """
            Get the true longitude argument.
        
            Returns:
                true longitude argument (rad)
        
        
        """
        ...
    def getMu(self) -> float:
        """
            Get the central acceleration constant.
        
            Returns:
                central acceleration constant
        
        
        """
        ...
    def getN(self) -> float:
        """
            Get the mean motion.
        
            Returns:
                mean motion (1/s)
        
        
        """
        ...
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.Frame: ...
    @typing.overload
    def getPVCoordinates(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates:
        """
            Get the :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates` in definition frame.
        
            Returns:
                pvCoordinates in the definition frame
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getPVCoordinates`
        
        
        """
        ...
    @typing.overload
    def getPVCoordinates(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    @typing.overload
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters:
        """
            Get underlying orbital parameters.
        
            Returns:
                orbital parameters
        
        
        """
        ...
    def getType(self) -> 'OrbitType':
        """
            Get the orbit type.
        
            Returns:
                orbit type
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def shiftedBy(self, double: float) -> 'Orbit':
        """
            Call the method :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.orbitShiftedBy` implemented in inherited classes of Orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeShiftable.shiftedBy` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeShiftable`
        
            Parameters:
                dt (double): time shift in seconds
        
            Returns:
                a new orbit, shifted with respect to the instance (which is immutable)
        
        
        """
        ...

class OrbitType(java.lang.Enum['OrbitType']):
    """
    public enum OrbitType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`>
    
        Enumerate for :class:`~fr.cnes.sirius.patrius.orbits.Orbit` parameters types.
    """
    CARTESIAN: typing.ClassVar['OrbitType'] = ...
    CIRCULAR: typing.ClassVar['OrbitType'] = ...
    EQUINOCTIAL: typing.ClassVar['OrbitType'] = ...
    ALTERNATE_EQUINOCTIAL: typing.ClassVar['OrbitType'] = ...
    APSIS: typing.ClassVar['OrbitType'] = ...
    EQUATORIAL: typing.ClassVar['OrbitType'] = ...
    KEPLERIAN: typing.ClassVar['OrbitType'] = ...
    def convertOrbit(self, orbit: Orbit, frame: fr.cnes.sirius.patrius.frames.Frame) -> Orbit: ...
    def convertType(self, orbit: Orbit) -> Orbit:
        """
            Convert an orbit to the instance type.
        
            The returned orbit is the specified instance itself if its type already matches, otherwise a new orbit of the proper
            type created
        
            Parameters:
                orbit (:class:`~fr.cnes.sirius.patrius.orbits.Orbit`): orbit to convert
        
            Returns:
                converted orbit with type guaranteed to match (so it can be cast safely)
        
        
        """
        ...
    def getCoordinateType(self, int: int, positionAngle: 'PositionAngle') -> fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate:
        """
            Gets the coordinate type associated with a given state vector index.
        
            Parameters:
                stateVectorIndex (int): the state vector index
                positionAngle (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the position angle type
        
            Returns:
                the coordinate type associated with the provided state vector index
        
            Raises:
                : if the provided state vector index is not between 0 and 5 (included)
        
        
        """
        ...
    def mapArrayToOrbit(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], positionAngle: 'PositionAngle', absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double2: float, frame: fr.cnes.sirius.patrius.frames.Frame) -> Orbit:
        """
            Convert state array to orbital parameters.
        
            Note that all implementations of this method *must* be consistent with the implementation of the null method for the
            corresponding orbit type in terms of parameters order and meaning.
        
            Parameters:
                array (double[]): state as a flat array
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the angle
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): integration date
                mu (double): central attraction coefficient used for propagation (m :sup:`3` /s :sup:`2` )
                frame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): frame in which integration is performed
        
            Returns:
                orbit corresponding to the flat array as a space dynamics object
        
        
        """
        ...
    def mapOrbitToArray(self, orbit: Orbit, positionAngle: 'PositionAngle', doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Convert orbit to state array.
        
            Note that all implementations of this method *must* be consistent with the implementation of the null method for the
            corresponding orbit type in terms of parameters order and meaning.
        
            Parameters:
                orbit (:class:`~fr.cnes.sirius.patrius.orbits.Orbit`): orbit to map
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the angle
                stateVector (double[]): flat array into which the state vector should be mapped
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'OrbitType':
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
    def values() -> typing.MutableSequence['OrbitType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (OrbitType c : OrbitType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class PositionAngle(java.lang.Enum['PositionAngle']):
    """
    public enum PositionAngle extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`>
    
        Enumerate for true, eccentric and mean position angles.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.orbits.KeplerianOrbit`, :class:`~fr.cnes.sirius.patrius.orbits.CircularOrbit`,
            :class:`~fr.cnes.sirius.patrius.orbits.EquinoctialOrbit`, :class:`~fr.cnes.sirius.patrius.orbits.ApsisOrbit`
    """
    MEAN: typing.ClassVar['PositionAngle'] = ...
    ECCENTRIC: typing.ClassVar['PositionAngle'] = ...
    TRUE: typing.ClassVar['PositionAngle'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'PositionAngle':
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
    def values() -> typing.MutableSequence['PositionAngle']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (PositionAngle c : PositionAngle.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class AlternateEquinoctialOrbit(Orbit):
    """
    public final class AlternateEquinoctialOrbit extends :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
    
        This class handles alternate equinoctial orbital parameters, which can support both circular and equatorial orbits.
    
        The parameters used internally are the alternate equinoctial elements (see
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters` for more information.
    
        The instance :code:`AlternateEquinoctialOrbit` is guaranteed to be immutable.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.orbits.Orbit`, :class:`~fr.cnes.sirius.patrius.orbits.KeplerianOrbit`,
            :class:`~fr.cnes.sirius.patrius.orbits.CircularOrbit`, :class:`~fr.cnes.sirius.patrius.orbits.CartesianOrbit`,
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double7: float): ...
    @typing.overload
    def __init__(self, orbit: Orbit): ...
    @typing.overload
    def __init__(self, iOrbitalParameters: fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.equals` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getA(self) -> float:
        """
            Get the semi-major axis. Note that the semi-major axis is considered negative for hyperbolic orbits.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getA` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getAlternateEquinoctialParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters:
        """
            Getter for underlying equinoctial parameters.
        
            Returns:
                equinoctial parameters
        
        
        """
        ...
    def getE(self) -> float:
        """
            Get the eccentricity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentricity
        
        
        """
        ...
    def getEquinoctialEx(self) -> float:
        """
            Get the first component of the eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                e cos(ω + Ω), first component of the eccentricity vector
        
        
        """
        ...
    def getEquinoctialEy(self) -> float:
        """
            Get the second component of the eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                e sin(ω + Ω), second component of the eccentricity vector
        
        
        """
        ...
    def getHx(self) -> float:
        """
            Get the first component of the inclination vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                tan(i/2) cos(Ω), first component of the inclination vector
        
        
        """
        ...
    def getHy(self) -> float:
        """
            Get the second component of the inclination vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                tan(i/2) sin(Ω), second component of the inclination vector
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getI` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    def getJacobianWrtParameters(self, positionAngle: PositionAngle, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None:
        """
            Compute the Jacobian of the Cartesian parameters with respect to the orbital parameters.
        
            Element :code:`jacobian[i][j]` is the derivative of parameter i of the orbit with respect to Cartesian coordinate j.
            This means each row correspond to one orbital parameter whereas columns 0 to 5 correspond to the Cartesian coordinates
            x, y, z, xDot, yDot and zDot.
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the position angle to use
                jacobian (double[][]): placeholder 6x6 (or larger) matrix to be filled with the Jacobian, if matrix is larger than 6x6, only the 6x6 upper left
                    corner will be modified
        
        
        """
        ...
    def getL(self, positionAngle: PositionAngle) -> float:
        """
            Get the longitude argument.
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the angle
        
            Returns:
                longitude argument (rad)
        
        
        """
        ...
    def getLE(self) -> float:
        """
            Get the eccentric longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                E + ω + Ω eccentric longitude argument (rad)
        
        
        """
        ...
    def getLM(self) -> float:
        """
            Get the mean longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLM` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                M + ω + Ω mean longitude argument (rad)
        
        
        """
        ...
    def getLv(self) -> float:
        """
            Get the true longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLv` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                v + ω + Ω true longitude argument (rad)
        
        
        """
        ...
    def getN(self) -> float:
        """
            Get the mean motion.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getN` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean motion (1/s)
        
        
        """
        ...
    def getParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters:
        """
            Get underlying orbital parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getParameters` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbital parameters
        
        
        """
        ...
    def getType(self) -> OrbitType:
        """
            Get the orbit type.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getType` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbit type
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.hashCode` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection[Orbit], typing.Sequence[Orbit], typing.Set[Orbit]]) -> 'AlternateEquinoctialOrbit': ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class ApsisOrbit(Orbit):
    """
    public final class ApsisOrbit extends :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
    
        This class handles periapsis/apoapsis parameters.
    
        The parameters used internally are the periapsis/apoapsis elements (see
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters` for more information.
    
        The instance :code:`ApsisOrbit` is guaranteed to be immutable.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.orbits.Orbit`, :class:`~fr.cnes.sirius.patrius.orbits.KeplerianOrbit`,
            :class:`~fr.cnes.sirius.patrius.orbits.CartesianOrbit`, :class:`~fr.cnes.sirius.patrius.orbits.EquinoctialOrbit`,
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double7: float): ...
    @typing.overload
    def __init__(self, orbit: Orbit): ...
    @typing.overload
    def __init__(self, iOrbitalParameters: fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.equals` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getA(self) -> float:
        """
            Get the semi-major axis.
        
            Note that the semi-major axis is considered negative for hyperbolic orbits.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getA` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getAnomaly(self, positionAngle: PositionAngle) -> float:
        """
            Get the anomaly.
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the angle
        
            Returns:
                anomaly (rad)
        
        
        """
        ...
    def getApoapsis(self) -> float:
        """
            Get the apoapsis.
        
            Returns:
                apoapsis (m)
        
        
        """
        ...
    def getApsisParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters:
        """
            Getter for underlying apsis parameters.
        
            Returns:
                apsis parameters
        
        
        """
        ...
    def getE(self) -> float:
        """
            Get the eccentricity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentricity
        
        
        """
        ...
    def getEquinoctialEx(self) -> float:
        """
            Get the first component of the equinoctial eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                first component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getEquinoctialEy(self) -> float:
        """
            Get the second component of the equinoctial eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                second component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getHx(self) -> float:
        """
            Get hx = ix / (2 * cos(i/2)), where ix is the first component of the inclination vector. Another formulation is hx =
            tan(i/2) cos(Ω)
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                first component of the inclination vector
        
        
        """
        ...
    def getHy(self) -> float:
        """
            Get hy = iy / (2 * cos(i/2)), where iy is the second component of the inclination vector. Another formulation is hy =
            tan(i/2) sin(Ω)
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                second component of the inclination vector
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getI` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    def getLE(self) -> float:
        """
            Get the eccentric longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentric longitude argument (rad)
        
        
        """
        ...
    def getLM(self) -> float:
        """
            Get the mean longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLM` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean longitude argument (rad)
        
        
        """
        ...
    def getLv(self) -> float:
        """
            Get the true longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLv` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                true longitude argument (rad)
        
        
        """
        ...
    def getN(self) -> float:
        """
            Get the mean motion. Get the mean motion.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getN` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean motion (1/s)
        
        
        """
        ...
    def getParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters:
        """
            Get underlying orbital parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getParameters` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbital parameters
        
        
        """
        ...
    def getPeriapsis(self) -> float:
        """
            Get the periapsis.
        
            Returns:
                periapsis (m)
        
        
        """
        ...
    def getPerigeeArgument(self) -> float:
        """
            Get the perigee argument.
        
            Returns:
                perigee argument (rad)
        
        
        """
        ...
    def getRightAscensionOfAscendingNode(self) -> float:
        """
            Get the right ascension of the ascending node.
        
            Returns:
                right ascension of the ascending node (rad)
        
        
        """
        ...
    def getType(self) -> OrbitType:
        """
            Get the orbit type.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getType` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbit type
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.hashCode` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection[Orbit], typing.Sequence[Orbit], typing.Set[Orbit]]) -> 'ApsisOrbit': ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class CartesianOrbit(Orbit):
    """
    public final class CartesianOrbit extends :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
    
        This class holds cartesian orbital parameters.
    
        The parameters used internally are the cartesian elements (see
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters` for more information.
    
        The instance :code:`CartesianOrbit` is guaranteed to be immutable.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.orbits.Orbit`, :class:`~fr.cnes.sirius.patrius.orbits.KeplerianOrbit`,
            :class:`~fr.cnes.sirius.patrius.orbits.CircularOrbit`, :class:`~fr.cnes.sirius.patrius.orbits.EquinoctialOrbit`,
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, orbit: Orbit): ...
    @typing.overload
    def __init__(self, iOrbitalParameters: fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.equals` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getA(self) -> float:
        """
            Get the semi-major axis.
        
            Note that the semi-major axis is considered negative for hyperbolic orbits.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getA` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getCartesianParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters:
        """
            Getter for underlying circular parameters.
        
            Returns:
                circular parameters
        
        
        """
        ...
    def getE(self) -> float:
        """
            Get the eccentricity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentricity
        
        
        """
        ...
    def getEquinoctialEx(self) -> float:
        """
            Get the first component of the equinoctial eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                first component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getEquinoctialEy(self) -> float:
        """
            Get the second component of the equinoctial eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                second component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getHx(self) -> float:
        """
            Get hx = ix / (2 * cos(i/2)), where ix is the first component of the inclination vector. Another formulation is hx =
            tan(i/2) cos(Ω)
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                first component of the inclination vector
        
        
        """
        ...
    def getHy(self) -> float:
        """
            Get hy = iy / (2 * cos(i/2)), where iy is the second component of the inclination vector. Another formulation is hy =
            tan(i/2) sin(Ω)
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                second component of the inclination vector
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getI` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    def getLE(self) -> float:
        """
            Get the eccentric longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentric longitude argument (rad)
        
        
        """
        ...
    def getLM(self) -> float:
        """
            Get the mean longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLM` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean longitude argument (rad)
        
        
        """
        ...
    def getLv(self) -> float:
        """
            Get the true longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLv` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                true longitude argument (rad)
        
        
        """
        ...
    def getN(self) -> float:
        """
            Get the mean motion.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getN` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean motion (1/s)
        
        
        """
        ...
    def getParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters:
        """
            Get underlying orbital parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getParameters` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbital parameters
        
        
        """
        ...
    def getType(self) -> OrbitType:
        """
            Get the orbit type.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getType` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbit type
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.hashCode` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection[Orbit], typing.Sequence[Orbit], typing.Set[Orbit]]) -> 'CartesianOrbit': ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class CircularOrbit(Orbit):
    """
    public final class CircularOrbit extends :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
    
        This class handles circular orbital parameters.
    
        The parameters used internally are the circular elements (see
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters` for more information.
    
        The instance :code:`CircularOrbit` is guaranteed to be immutable.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.orbits.Orbit`, :class:`~fr.cnes.sirius.patrius.orbits.KeplerianOrbit`,
            :class:`~fr.cnes.sirius.patrius.orbits.CartesianOrbit`, :class:`~fr.cnes.sirius.patrius.orbits.EquinoctialOrbit`,
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double7: float): ...
    @typing.overload
    def __init__(self, orbit: Orbit): ...
    @typing.overload
    def __init__(self, iOrbitalParameters: fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.equals` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getA(self) -> float:
        """
            Get the semi-major axis.
        
            Note that the semi-major axis is considered negative for hyperbolic orbits.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getA` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getAlpha(self, positionAngle: PositionAngle) -> float:
        """
            Get the latitude argument.
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the angle
        
            Returns:
                latitude argument (rad)
        
        
        """
        ...
    def getAlphaE(self) -> float:
        """
            Get the eccentric latitude argument.
        
            Returns:
                E + ω eccentric latitude argument (rad)
        
        
        """
        ...
    def getAlphaM(self) -> float:
        """
            Get the mean latitude argument.
        
            Returns:
                M + ω mean latitude argument (rad)
        
        
        """
        ...
    def getAlphaV(self) -> float:
        """
            Get the true latitude argument.
        
            Returns:
                v + ω true latitude argument (rad)
        
        
        """
        ...
    def getCircularEx(self) -> float:
        """
            Get the first component of the circular eccentricity vector.
        
            Returns:
                ex = e cos(ω), first component of the circular eccentricity vector
        
        
        """
        ...
    def getCircularEy(self) -> float:
        """
            Get the second component of the circular eccentricity vector.
        
            Returns:
                ey = e sin(ω), second component of the circular eccentricity vector
        
        
        """
        ...
    def getCircularParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters:
        """
            Getter for underlying circular parameters.
        
            Returns:
                circular parameters
        
        
        """
        ...
    def getE(self) -> float:
        """
            Get the eccentricity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentricity
        
        
        """
        ...
    def getEquinoctialEx(self) -> float:
        """
            Get the first component of the equinoctial eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                first component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getEquinoctialEy(self) -> float:
        """
            Get the second component of the equinoctial eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                second component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getHx(self) -> float:
        """
            Get hx = ix / (2 * cos(i/2)), where ix is the first component of the inclination vector. Another formulation is hx =
            tan(i/2) cos(Ω)
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                first component of the inclination vector
        
        
        """
        ...
    def getHy(self) -> float:
        """
            Get hy = iy / (2 * cos(i/2)), where iy is the second component of the inclination vector. Another formulation is hy =
            tan(i/2) sin(Ω)
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                second component of the inclination vector
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getI` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    def getLE(self) -> float:
        """
            Get the eccentric longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentric longitude argument (rad)
        
        
        """
        ...
    def getLM(self) -> float:
        """
            Get the mean longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLM` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean longitude argument (rad)
        
        
        """
        ...
    def getLv(self) -> float:
        """
            Get the true longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLv` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                true longitude argument (rad)
        
        
        """
        ...
    def getN(self) -> float:
        """
            Get the mean motion.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getN` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean motion (1/s)
        
        
        """
        ...
    def getParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters:
        """
            Get underlying orbital parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getParameters` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbital parameters
        
        
        """
        ...
    def getRightAscensionOfAscendingNode(self) -> float:
        """
            Get the right ascension of the ascending node.
        
            Returns:
                right ascension of the ascending node (rad)
        
        
        """
        ...
    def getType(self) -> OrbitType:
        """
            Get the orbit type.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getType` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbit type
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.hashCode` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection[Orbit], typing.Sequence[Orbit], typing.Set[Orbit]]) -> 'CircularOrbit': ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class EquatorialOrbit(Orbit):
    """
    public final class EquatorialOrbit extends :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
    
        This class handles non circular equatorial orbital parameters.
    
        The parameters used internally are the equatorial elements (see
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters` for more information.
    
        The instance :code:`EquatorialOrbit` is guaranteed to be immutable.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.orbits.Orbit`, :class:`~fr.cnes.sirius.patrius.orbits.CircularOrbit`,
            :class:`~fr.cnes.sirius.patrius.orbits.CartesianOrbit`, :class:`~fr.cnes.sirius.patrius.orbits.EquinoctialOrbit`,
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double7: float): ...
    @typing.overload
    def __init__(self, orbit: Orbit): ...
    @typing.overload
    def __init__(self, iOrbitalParameters: fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.equals` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getA(self) -> float:
        """
            Get the semi-major axis.
        
            Note that the semi-major axis is considered negative for hyperbolic orbits.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getA` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getAnomaly(self, positionAngle: PositionAngle) -> float:
        """
            Get the anomaly.
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the angle
        
            Returns:
                anomaly (rad)
        
        
        """
        ...
    def getE(self) -> float:
        """
            Get the eccentricity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentricity
        
        
        """
        ...
    def getEccentricAnomaly(self) -> float:
        """
            Get the eccentric anomaly.
        
            Returns:
                eccentric anomaly (rad)
        
        
        """
        ...
    def getEquatorialParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters:
        """
            Getter for underlying equatorial parameters.
        
            Returns:
                equatorial parameters
        
        
        """
        ...
    def getEquinoctialEx(self) -> float:
        """
            Get the first component of the equinoctial eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                first component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getEquinoctialEy(self) -> float:
        """
            Get the second component of the equinoctial eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                second component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getHx(self) -> float:
        """
            Get hx = ix / (2 * cos(i/2)), where ix is the first component of the inclination vector. Another formulation is hx =
            tan(i/2) cos(Ω)
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                first component of the inclination vector
        
        
        """
        ...
    def getHy(self) -> float:
        """
            Get hy = iy / (2 * cos(i/2)), where iy is the second component of the inclination vector. Another formulation is hy =
            tan(i/2) sin(Ω)
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                second component of the inclination vector
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getI` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    def getIx(self) -> float:
        """
            Get the first component of the inclination vector. ix = 2 sin(i/2) cos(Ω)
        
            Returns:
                first component of the inclination vector.
        
        
        """
        ...
    def getIy(self) -> float:
        """
            Get the second component of the inclination vector. iy = 2 sin(i/2) sin(Ω)
        
            Returns:
                second component of the inclination vector.
        
        
        """
        ...
    def getLE(self) -> float:
        """
            Get the eccentric longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentric longitude argument (rad)
        
        
        """
        ...
    def getLM(self) -> float:
        """
            Get the mean longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLM` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean longitude argument (rad)
        
        
        """
        ...
    def getLv(self) -> float:
        """
            Get the true longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLv` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                true longitude argument (rad)
        
        
        """
        ...
    def getMeanAnomaly(self) -> float:
        """
            Get the mean anomaly.
        
            Returns:
                mean anomaly (rad)
        
        
        """
        ...
    def getN(self) -> float:
        """
            Get the mean motion.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getN` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean motion (1/s)
        
        
        """
        ...
    def getParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters:
        """
            Get underlying orbital parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getParameters` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbital parameters
        
        
        """
        ...
    def getPomega(self) -> float:
        """
            Get the longitude of the periapsis (ω + Ω).
        
            Returns:
                longitude of the periapsis (rad)
        
        
        """
        ...
    def getTrueAnomaly(self) -> float:
        """
            Get the true anomaly.
        
            Returns:
                true anomaly (rad)
        
        
        """
        ...
    def getType(self) -> OrbitType:
        """
            Get the orbit type.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getType` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbit type
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.hashCode` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection[Orbit], typing.Sequence[Orbit], typing.Set[Orbit]]) -> 'EquatorialOrbit': ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class EquinoctialOrbit(Orbit):
    """
    public final class EquinoctialOrbit extends :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
    
        This class handles equinoctial orbital parameters, which can support both circular and equatorial orbits.
    
        The parameters used internally are the equinoctial elements (see
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters` for more information.
    
        The instance :code:`EquinoctialOrbit` is guaranteed to be immutable.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.orbits.Orbit`, :class:`~fr.cnes.sirius.patrius.orbits.KeplerianOrbit`,
            :class:`~fr.cnes.sirius.patrius.orbits.CircularOrbit`, :class:`~fr.cnes.sirius.patrius.orbits.CartesianOrbit`,
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double7: float): ...
    @typing.overload
    def __init__(self, orbit: Orbit): ...
    @typing.overload
    def __init__(self, iOrbitalParameters: fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.equals` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getA(self) -> float:
        """
            Get the semi-major axis.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getA` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getE(self) -> float:
        """
            Get the eccentricity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentricity
        
        
        """
        ...
    def getEquinoctialEx(self) -> float:
        """
            Get the first component of the eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                e cos(ω + Ω), first component of the eccentricity vector
        
        
        """
        ...
    def getEquinoctialEy(self) -> float:
        """
            Get the second component of the eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                e sin(ω + Ω), second component of the eccentricity vector
        
        
        """
        ...
    def getEquinoctialParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters:
        """
            Getter for underlying equinoctial parameters.
        
            Returns:
                equinoctial parameters
        
        
        """
        ...
    def getHx(self) -> float:
        """
            Get the first component of the inclination vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                tan(i/2) cos(Ω), first component of the inclination vector
        
        
        """
        ...
    def getHy(self) -> float:
        """
            Get the second component of the inclination vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                tan(i/2) sin(Ω), second component of the inclination vector
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getI` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    def getJacobianWrtParameters(self, positionAngle: PositionAngle, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None:
        """
            Compute the Jacobian of the Cartesian parameters with respect to the orbital parameters.
        
            Element :code:`jacobian[i][j]` is the derivative of parameter i of the orbit with respect to Cartesian coordinate j.
            This means each row correspond to one orbital parameter whereas columns 0 to 5 correspond to the Cartesian coordinates
            x, y, z, xDot, yDot and zDot.
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the position angle to use
                jacobian (double[][]): placeholder 6x6 (or larger) matrix to be filled with the Jacobian, if matrix is larger than 6x6, only the 6x6 upper left
                    corner will be modified
        
        
        """
        ...
    def getL(self, positionAngle: PositionAngle) -> float:
        """
            Get the longitude argument.
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the angle
        
            Returns:
                longitude argument (rad)
        
        
        """
        ...
    def getLE(self) -> float:
        """
            Get the eccentric longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                E + ω + Ω eccentric longitude argument (rad)
        
        
        """
        ...
    def getLM(self) -> float:
        """
            Get the mean longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLM` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                M + ω + Ω mean longitude argument (rad)
        
        
        """
        ...
    def getLv(self) -> float:
        """
            Get the true longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLv` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                v + ω + Ω true longitude argument (rad)
        
        
        """
        ...
    def getN(self) -> float:
        """
            Get the mean motion.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getN` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean motion (1/s)
        
        
        """
        ...
    def getParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters:
        """
            Get underlying orbital parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getParameters` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbital parameters
        
        
        """
        ...
    def getType(self) -> OrbitType:
        """
            Get the orbit type.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getType` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbit type
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.hashCode` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection[Orbit], typing.Sequence[Orbit], typing.Set[Orbit]]) -> 'EquinoctialOrbit': ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class KeplerianOrbit(Orbit):
    """
    public final class KeplerianOrbit extends :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
    
        This class handles traditional keplerian orbital parameters.
    
        The parameters used internally are the keplerian elements (see
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters` for more information.
    
        The instance :code:`KeplerianOrbit` is guaranteed to be immutable.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.orbits.Orbit`, :class:`~fr.cnes.sirius.patrius.orbits.CircularOrbit`,
            :class:`~fr.cnes.sirius.patrius.orbits.CartesianOrbit`, :class:`~fr.cnes.sirius.patrius.orbits.EquinoctialOrbit`,
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double7: float): ...
    @typing.overload
    def __init__(self, orbit: Orbit): ...
    @typing.overload
    def __init__(self, iOrbitalParameters: fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.equals` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getA(self) -> float:
        """
            Get the semi-major axis.
        
            Note that the semi-major axis is considered negative for hyperbolic orbits.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getA` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getAnomaly(self, positionAngle: PositionAngle) -> float:
        """
            Get the anomaly.
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the angle
        
            Returns:
                anomaly (rad)
        
        
        """
        ...
    def getE(self) -> float:
        """
            Get the eccentricity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentricity
        
        
        """
        ...
    def getEccentricAnomaly(self) -> float:
        """
            Get the eccentric anomaly.
        
            Returns:
                eccentric anomaly (rad)
        
        
        """
        ...
    def getEquinoctialEx(self) -> float:
        """
            Get the first component of the equinoctial eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                first component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getEquinoctialEy(self) -> float:
        """
            Get the second component of the equinoctial eccentricity vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getEquinoctialEy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                second component of the equinoctial eccentricity vector
        
        
        """
        ...
    def getHx(self) -> float:
        """
            Get hx = ix / (2 * cos(i/2)), where ix is the first component of the inclination vector. Another formulation is hx =
            tan(i/2) cos(Ω)
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHx` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                first component of the inclination vector
        
        
        """
        ...
    def getHy(self) -> float:
        """
            Get hy = iy / (2 * cos(i/2)), where iy is the second component of the inclination vector. Another formulation is hy =
            tan(i/2) sin(Ω)
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getHy` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                second component of the inclination vector
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getI` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    def getKeplerianParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters:
        """
            Getter for underlying keplerian parameters.
        
            Returns:
                keplerian parameters
        
        
        """
        ...
    def getLE(self) -> float:
        """
            Get the eccentric longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLE` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                eccentric longitude argument (rad)
        
        
        """
        ...
    def getLM(self) -> float:
        """
            Get the mean longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLM` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean longitude argument (rad)
        
        
        """
        ...
    def getLv(self) -> float:
        """
            Get the true longitude argument.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getLv` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                true longitude argument (rad)
        
        
        """
        ...
    def getMeanAnomaly(self) -> float:
        """
            Get the mean anomaly.
        
            Returns:
                mean anomaly (rad)
        
        
        """
        ...
    def getN(self) -> float:
        """
            Get the mean motion.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getN` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                mean motion (1/s)
        
        
        """
        ...
    def getParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters:
        """
            Get underlying orbital parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getParameters` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbital parameters
        
        
        """
        ...
    def getPerigeeArgument(self) -> float:
        """
            Get the perigee argument.
        
            Returns:
                perigee argument (rad)
        
        
        """
        ...
    def getRightAscensionOfAscendingNode(self) -> float:
        """
            Get the right ascension of the ascending node.
        
            Returns:
                right ascension of the ascending node (rad)
        
        
        """
        ...
    def getTrueAnomaly(self) -> float:
        """
            Get the true anomaly.
        
            Returns:
                true anomaly (rad)
        
        
        """
        ...
    def getType(self) -> OrbitType:
        """
            Get the orbit type.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.getType` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                orbit type
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.Orbit.hashCode` in class :class:`~fr.cnes.sirius.patrius.orbits.Orbit`
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection[Orbit], typing.Sequence[Orbit], typing.Set[Orbit]]) -> 'KeplerianOrbit': ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.orbits")``.

    AlternateEquinoctialOrbit: typing.Type[AlternateEquinoctialOrbit]
    ApsisOrbit: typing.Type[ApsisOrbit]
    CartesianOrbit: typing.Type[CartesianOrbit]
    CircularOrbit: typing.Type[CircularOrbit]
    EquatorialOrbit: typing.Type[EquatorialOrbit]
    EquinoctialOrbit: typing.Type[EquinoctialOrbit]
    KeplerianOrbit: typing.Type[KeplerianOrbit]
    Orbit: typing.Type[Orbit]
    OrbitType: typing.Type[OrbitType]
    PositionAngle: typing.Type[PositionAngle]
    orbitalparameters: fr.cnes.sirius.patrius.orbits.orbitalparameters.__module_protocol__
    pvcoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.__module_protocol__
