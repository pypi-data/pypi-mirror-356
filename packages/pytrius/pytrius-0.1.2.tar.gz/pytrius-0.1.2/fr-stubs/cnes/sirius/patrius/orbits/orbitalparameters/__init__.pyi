
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import java.io
import java.lang
import typing



class IOrbitalParameters:
    """
    public interface IOrbitalParameters
    
        Interface for orbital parameters.
    
        Since:
            3.0
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
    def getAlternateEquinoctialParameters(self) -> 'AlternateEquinoctialParameters':
        """
            Convert current orbital parameters into alternate equinoctial parameters.
        
            Returns:
                current orbital parameters converted into alternate equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters`
        
        
        """
        ...
    def getApsisAltitudeParameters(self, double: float) -> 'ApsisAltitudeParameters':
        """
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
        
        """
        ...
    def getApsisRadiusParameters(self) -> 'ApsisRadiusParameters':
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        
        """
        ...
    def getCartesianParameters(self) -> 'CartesianParameters':
        """
            Convert current orbital parameters into cartesian parameters.
        
            Returns:
                current orbital parameters converted into cartesian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters`
        
        
        """
        ...
    def getCircularParameters(self) -> 'CircularParameters':
        """
            Convert current orbital parameters into circular parameters.
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    def getEquatorialParameters(self) -> 'EquatorialParameters':
        """
            Convert current orbital parameters into equatorial parameters.
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        
        """
        ...
    def getEquinoctialParameters(self) -> 'EquinoctialParameters':
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        
        """
        ...
    def getKeplerianParameters(self) -> 'KeplerianParameters':
        """
            Convert current orbital parameters into Keplerian parameters.
        
            Returns:
                current orbital parameters converted into Keplerian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters`
        
        
        """
        ...
    def getMu(self) -> float:
        """
            Getter for the central acceleration constant.
        
            Returns:
                central acceleration constant
        
        
        """
        ...
    def getReentryParameters(self, double: float, double2: float) -> 'ReentryParameters':
        """
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
                f (double): flattening (f = (a-b)/a)
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
        
        """
        ...
    def getStelaEquinoctialParameters(self) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        
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

class OrbitalCoordinate:
    """
    public interface OrbitalCoordinate
    
        Interface for classes listing the coordinates associated with a type of orbital parameters.
    """
    @staticmethod
    def checkStateVectorIndex(int: int) -> None:
        """
            Static method to check if the state vector index is valid (between 0 and 5 (included)).
        
            Parameters:
                stateVectorIndex (int): the state vector index
        
            Raises:
                : if the provided state vector index is not between 0 and 5 (included)
        
        
        """
        ...
    def convertTo(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> 'OrbitalCoordinate':
        """
            Gets the coordinate type associated with the same state vector index in a given orbit type and position angle type.
        
            Parameters:
                orbitType (:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`): the target orbit type
                positionAngle (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the target position angle type
        
            Returns:
                the coordinate type associated with the same state vector index in the specified orbit and position angle types
        
        
        """
        ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Gets the orbit type to which this orbital coordinate is related.
        
            Returns:
                the orbit type to which this orbital coordinate is related
        
        
        """
        ...
    def getStateVectorIndex(self) -> int:
        """
            Gets the index of the coordinate in the state vector array.
        
            Returns:
                the index of the coordinate in the state vector array.
        
        
        """
        ...

class AbstractOrbitalParameters(IOrbitalParameters, java.io.Serializable):
    """
    public abstract class AbstractOrbitalParameters extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Abstract class for orbital parameters.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float): ...
    def getMu(self) -> float:
        """
            Getter for the central acceleration constant.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.getMu` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Returns:
                central acceleration constant
        
        
        """
        ...

class AlternateEquinoctialCoordinate(java.lang.Enum['AlternateEquinoctialCoordinate'], OrbitalCoordinate):
    """
    public enum AlternateEquinoctialCoordinate extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialCoordinate`> implements :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
    
        Enumerates the different types of coordinate associated with the alternate equinoctial parameters.
    """
    MEAN_MOTION: typing.ClassVar['AlternateEquinoctialCoordinate'] = ...
    E_X: typing.ClassVar['AlternateEquinoctialCoordinate'] = ...
    E_Y: typing.ClassVar['AlternateEquinoctialCoordinate'] = ...
    H_X: typing.ClassVar['AlternateEquinoctialCoordinate'] = ...
    H_Y: typing.ClassVar['AlternateEquinoctialCoordinate'] = ...
    TRUE_LONGITUDE_ARGUMENT: typing.ClassVar['AlternateEquinoctialCoordinate'] = ...
    MEAN_LONGITUDE_ARGUMENT: typing.ClassVar['AlternateEquinoctialCoordinate'] = ...
    ECCENTRIC_LONGITUDE_ARGUMENT: typing.ClassVar['AlternateEquinoctialCoordinate'] = ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Gets the orbit type to which this orbital coordinate is related.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getOrbitType` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the orbit type to which this orbital coordinate is related
        
        
        """
        ...
    def getStateVectorIndex(self) -> int:
        """
            Gets the index of the coordinate in the state vector array.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getStateVectorIndex` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the index of the coordinate in the state vector array.
        
        
        """
        ...
    _valueOf_2__T = typing.TypeVar('_valueOf_2__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(int: int, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> 'AlternateEquinoctialCoordinate':
        """
            Gets the coordinate type associated with a given state vector index.
        
            Parameters:
                stateVectorIndex (int): the state vector index
                positionAngle (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the position angle type (only used for the longitude argument)
        
            Returns:
                the coordinate type associated with the provided state vector index
        
            Raises:
                : if the provided state vector index is not between 0 and 5 (included)
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'AlternateEquinoctialCoordinate':
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
    def valueOf(class_: typing.Type[_valueOf_2__T], string: str) -> _valueOf_2__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['AlternateEquinoctialCoordinate']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (AlternateEquinoctialCoordinate c : AlternateEquinoctialCoordinate.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class ApsisAltitudeCoordinate(java.lang.Enum['ApsisAltitudeCoordinate'], OrbitalCoordinate):
    """
    public enum ApsisAltitudeCoordinate extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeCoordinate`> implements :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
    
        Enumerates the different types of coordinate associated with the periapsis/apoapsis altitude parameters.
    """
    PERIAPSIS_ALTITUDE: typing.ClassVar['ApsisAltitudeCoordinate'] = ...
    APOAPSIS_ALTITUDE: typing.ClassVar['ApsisAltitudeCoordinate'] = ...
    INCLINATION: typing.ClassVar['ApsisAltitudeCoordinate'] = ...
    PERIAPSIS_ARGUMENT: typing.ClassVar['ApsisAltitudeCoordinate'] = ...
    RIGHT_ASCENSION_OF_ASCENDING_NODE: typing.ClassVar['ApsisAltitudeCoordinate'] = ...
    TRUE_ANOMALY: typing.ClassVar['ApsisAltitudeCoordinate'] = ...
    MEAN_ANOMALY: typing.ClassVar['ApsisAltitudeCoordinate'] = ...
    ECCENTRIC_ANOMALY: typing.ClassVar['ApsisAltitudeCoordinate'] = ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Gets the orbit type to which this orbital coordinate is related.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getOrbitType` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the orbit type to which this orbital coordinate is related
        
        
        """
        ...
    def getStateVectorIndex(self) -> int:
        """
            Gets the index of the coordinate in the state vector array.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getStateVectorIndex` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the index of the coordinate in the state vector array.
        
        
        """
        ...
    _valueOf_2__T = typing.TypeVar('_valueOf_2__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(int: int, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> 'ApsisAltitudeCoordinate':
        """
            Gets the coordinate type associated with a given state vector index.
        
            Parameters:
                stateVectorIndex (int): the state vector index
                positionAngle (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the position angle type (only used for the anomaly)
        
            Returns:
                the coordinate type associated with the provided state vector index
        
            Raises:
                : if the provided state vector index is not between 0 and 5 (included)
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'ApsisAltitudeCoordinate':
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
    def valueOf(class_: typing.Type[_valueOf_2__T], string: str) -> _valueOf_2__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['ApsisAltitudeCoordinate']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (ApsisAltitudeCoordinate c : ApsisAltitudeCoordinate.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class ApsisRadiusCoordinate(java.lang.Enum['ApsisRadiusCoordinate'], OrbitalCoordinate):
    """
    public enum ApsisRadiusCoordinate extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusCoordinate`> implements :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
    
        Enumerates the different types of coordinate associated with the periapsis/apoapsis radius parameters.
    """
    PERIAPSIS: typing.ClassVar['ApsisRadiusCoordinate'] = ...
    APOAPSIS: typing.ClassVar['ApsisRadiusCoordinate'] = ...
    INCLINATION: typing.ClassVar['ApsisRadiusCoordinate'] = ...
    PERIAPSIS_ARGUMENT: typing.ClassVar['ApsisRadiusCoordinate'] = ...
    RIGHT_ASCENSION_OF_ASCENDING_NODE: typing.ClassVar['ApsisRadiusCoordinate'] = ...
    TRUE_ANOMALY: typing.ClassVar['ApsisRadiusCoordinate'] = ...
    MEAN_ANOMALY: typing.ClassVar['ApsisRadiusCoordinate'] = ...
    ECCENTRIC_ANOMALY: typing.ClassVar['ApsisRadiusCoordinate'] = ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Gets the orbit type to which this orbital coordinate is related.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getOrbitType` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the orbit type to which this orbital coordinate is related
        
        
        """
        ...
    def getStateVectorIndex(self) -> int:
        """
            Gets the index of the coordinate in the state vector array.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getStateVectorIndex` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the index of the coordinate in the state vector array.
        
        
        """
        ...
    _valueOf_2__T = typing.TypeVar('_valueOf_2__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(int: int, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> 'ApsisRadiusCoordinate':
        """
            Gets the coordinate type associated with a given state vector index.
        
            Parameters:
                stateVectorIndex (int): the state vector index
                positionAngle (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the position angle type (only used for the anomaly)
        
            Returns:
                the coordinate type associated with the provided state vector index
        
            Raises:
                : if the provided state vector index is not between 0 and 5 (included)
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'ApsisRadiusCoordinate':
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
    def valueOf(class_: typing.Type[_valueOf_2__T], string: str) -> _valueOf_2__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['ApsisRadiusCoordinate']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (ApsisRadiusCoordinate c : ApsisRadiusCoordinate.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class CartesianCoordinate(java.lang.Enum['CartesianCoordinate'], OrbitalCoordinate):
    """
    public enum CartesianCoordinate extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianCoordinate`> implements :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
    
        Enumerates the different coordinates associated with the cartesian parameters.
    """
    X: typing.ClassVar['CartesianCoordinate'] = ...
    Y: typing.ClassVar['CartesianCoordinate'] = ...
    Z: typing.ClassVar['CartesianCoordinate'] = ...
    VX: typing.ClassVar['CartesianCoordinate'] = ...
    VY: typing.ClassVar['CartesianCoordinate'] = ...
    VZ: typing.ClassVar['CartesianCoordinate'] = ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Gets the orbit type to which this orbital coordinate is related.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getOrbitType` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the orbit type to which this orbital coordinate is related
        
        
        """
        ...
    def getStateVectorIndex(self) -> int:
        """
            Gets the index of the coordinate in the state vector array.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getStateVectorIndex` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the index of the coordinate in the state vector array.
        
        
        """
        ...
    _valueOf_2__T = typing.TypeVar('_valueOf_2__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(int: int) -> 'CartesianCoordinate':
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
        
            Gets the coordinate type associated with a given state vector index.
        
            Parameters:
                stateVectorIndex (int): the state vector index
        
            Returns:
                the coordinate type associated with the provided state vector index
        
            Raises:
                : if the provided state vector index is not between 0 and 5 (included)
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'CartesianCoordinate': ...
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_2__T], string: str) -> _valueOf_2__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['CartesianCoordinate']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (CartesianCoordinate c : CartesianCoordinate.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class CircularCoordinate(java.lang.Enum['CircularCoordinate'], OrbitalCoordinate):
    """
    public enum CircularCoordinate extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularCoordinate`> implements :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
    
        Enumerates the different types of coordinate associated with the circular parameters.
    """
    SEMI_MAJOR_AXIS: typing.ClassVar['CircularCoordinate'] = ...
    E_X: typing.ClassVar['CircularCoordinate'] = ...
    E_Y: typing.ClassVar['CircularCoordinate'] = ...
    INCLINATION: typing.ClassVar['CircularCoordinate'] = ...
    RIGHT_ASCENSION_OF_ASCENDING_NODE: typing.ClassVar['CircularCoordinate'] = ...
    TRUE_LATITUDE_ARGUMENT: typing.ClassVar['CircularCoordinate'] = ...
    MEAN_LATITUDE_ARGUMENT: typing.ClassVar['CircularCoordinate'] = ...
    ECCENTRIC_LATITUDE_ARGUMENT: typing.ClassVar['CircularCoordinate'] = ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Gets the orbit type to which this orbital coordinate is related.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getOrbitType` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the orbit type to which this orbital coordinate is related
        
        
        """
        ...
    def getStateVectorIndex(self) -> int:
        """
            Gets the index of the coordinate in the state vector array.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getStateVectorIndex` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the index of the coordinate in the state vector array.
        
        
        """
        ...
    _valueOf_2__T = typing.TypeVar('_valueOf_2__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(int: int, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> 'CircularCoordinate':
        """
            Gets the coordinate type associated with a given state vector index.
        
            Parameters:
                stateVectorIndex (int): the state vector index
                positionAngle (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the position angle type (only used for the latitude argument)
        
            Returns:
                the coordinate type associated with the provided state vector index
        
            Raises:
                : if the provided state vector index is not between 0 and 5 (included)
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'CircularCoordinate':
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
    def valueOf(class_: typing.Type[_valueOf_2__T], string: str) -> _valueOf_2__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['CircularCoordinate']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (CircularCoordinate c : CircularCoordinate.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class EquatorialCoordinate(java.lang.Enum['EquatorialCoordinate'], OrbitalCoordinate):
    """
    public enum EquatorialCoordinate extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialCoordinate`> implements :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
    
        Enumerates the different types of coordinate associated with the equatorial parameters.
    """
    SEMI_MAJOR_AXIS: typing.ClassVar['EquatorialCoordinate'] = ...
    ECCENTRICITY: typing.ClassVar['EquatorialCoordinate'] = ...
    PERIAPSIS_LONGITUDE: typing.ClassVar['EquatorialCoordinate'] = ...
    I_X: typing.ClassVar['EquatorialCoordinate'] = ...
    I_Y: typing.ClassVar['EquatorialCoordinate'] = ...
    TRUE_ANOMALY: typing.ClassVar['EquatorialCoordinate'] = ...
    MEAN_ANOMALY: typing.ClassVar['EquatorialCoordinate'] = ...
    ECCENTRIC_ANOMALY: typing.ClassVar['EquatorialCoordinate'] = ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Gets the orbit type to which this orbital coordinate is related.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getOrbitType` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the orbit type to which this orbital coordinate is related
        
        
        """
        ...
    def getStateVectorIndex(self) -> int:
        """
            Gets the index of the coordinate in the state vector array.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getStateVectorIndex` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the index of the coordinate in the state vector array.
        
        
        """
        ...
    _valueOf_2__T = typing.TypeVar('_valueOf_2__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(int: int, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> 'EquatorialCoordinate':
        """
            Gets the coordinate type associated with a given state vector index.
        
            Parameters:
                stateVectorIndex (int): the state vector index
                positionAngle (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the position angle type (only used for the anomaly)
        
            Returns:
                the coordinate type associated with the provided state vector index
        
            Raises:
                : if the provided state vector index is not between 0 and 5 (included)
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'EquatorialCoordinate':
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
    def valueOf(class_: typing.Type[_valueOf_2__T], string: str) -> _valueOf_2__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['EquatorialCoordinate']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (EquatorialCoordinate c : EquatorialCoordinate.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class EquinoctialCoordinate(java.lang.Enum['EquinoctialCoordinate'], OrbitalCoordinate):
    """
    public enum EquinoctialCoordinate extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialCoordinate`> implements :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
    
        Enumerates the different types of coordinate associated with the equinoctial parameters.
    """
    SEMI_MAJOR_AXIS: typing.ClassVar['EquinoctialCoordinate'] = ...
    E_X: typing.ClassVar['EquinoctialCoordinate'] = ...
    E_Y: typing.ClassVar['EquinoctialCoordinate'] = ...
    H_X: typing.ClassVar['EquinoctialCoordinate'] = ...
    H_Y: typing.ClassVar['EquinoctialCoordinate'] = ...
    TRUE_LONGITUDE_ARGUMENT: typing.ClassVar['EquinoctialCoordinate'] = ...
    MEAN_LONGITUDE_ARGUMENT: typing.ClassVar['EquinoctialCoordinate'] = ...
    ECCENTRIC_LONGITUDE_ARGUMENT: typing.ClassVar['EquinoctialCoordinate'] = ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Gets the orbit type to which this orbital coordinate is related.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getOrbitType` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the orbit type to which this orbital coordinate is related
        
        
        """
        ...
    def getStateVectorIndex(self) -> int:
        """
            Gets the index of the coordinate in the state vector array.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getStateVectorIndex` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the index of the coordinate in the state vector array.
        
        
        """
        ...
    _valueOf_2__T = typing.TypeVar('_valueOf_2__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(int: int, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> 'EquinoctialCoordinate':
        """
            Gets the coordinate type associated with a given state vector index.
        
            Parameters:
                stateVectorIndex (int): the state vector index
                positionAngle (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the position angle type (only used for the longitude argument)
        
            Returns:
                the coordinate type associated with the provided state vector index
        
            Raises:
                : if the provided state vector index is not between 0 and 5 (included)
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'EquinoctialCoordinate':
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
    def valueOf(class_: typing.Type[_valueOf_2__T], string: str) -> _valueOf_2__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['EquinoctialCoordinate']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (EquinoctialCoordinate c : EquinoctialCoordinate.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class KeplerianCoordinate(java.lang.Enum['KeplerianCoordinate'], OrbitalCoordinate):
    """
    public enum KeplerianCoordinate extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianCoordinate`> implements :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
    
        Enumerates the different types of coordinate associated with the keplerian parameters.
    """
    SEMI_MAJOR_AXIS: typing.ClassVar['KeplerianCoordinate'] = ...
    ECCENTRICITY: typing.ClassVar['KeplerianCoordinate'] = ...
    INCLINATION: typing.ClassVar['KeplerianCoordinate'] = ...
    PERIGEE_ARGUMENT: typing.ClassVar['KeplerianCoordinate'] = ...
    RIGHT_ASCENSION_OF_ASCENDING_NODE: typing.ClassVar['KeplerianCoordinate'] = ...
    TRUE_ANOMALY: typing.ClassVar['KeplerianCoordinate'] = ...
    MEAN_ANOMALY: typing.ClassVar['KeplerianCoordinate'] = ...
    ECCENTRIC_ANOMALY: typing.ClassVar['KeplerianCoordinate'] = ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Gets the orbit type to which this orbital coordinate is related.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getOrbitType` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the orbit type to which this orbital coordinate is related
        
        
        """
        ...
    def getStateVectorIndex(self) -> int:
        """
            Gets the index of the coordinate in the state vector array.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate.getStateVectorIndex` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`
        
            Returns:
                the index of the coordinate in the state vector array.
        
        
        """
        ...
    _valueOf_2__T = typing.TypeVar('_valueOf_2__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(int: int, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> 'KeplerianCoordinate':
        """
            Gets the coordinate type associated with a given state vector index.
        
            Parameters:
                stateVectorIndex (int): the state vector index
                positionAngle (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): the position angle type (only used for the anomaly)
        
            Returns:
                the coordinate type associated with the provided state vector index
        
            Raises:
                : if the provided state vector index is not between 0 and 5 (included)
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'KeplerianCoordinate':
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
    def valueOf(class_: typing.Type[_valueOf_2__T], string: str) -> _valueOf_2__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['KeplerianCoordinate']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (KeplerianCoordinate c : KeplerianCoordinate.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class AlternateEquinoctialParameters(AbstractOrbitalParameters):
    """
    public class AlternateEquinoctialParameters extends :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AbstractOrbitalParameters`
    
        This class handles alternate equinoctial orbital parameters, which can support both circular and equatorial orbits.
    
        The parameters used internally are the alternate equinoctial elements which can be related to keplerian elements as
        follows:
    
        .. code-block: java
        
        
             n
             ex = e cos(ω + Ω)
             ey = e sin(ω + Ω)
             hx = tan(i/2) cos(Ω)
             hy = tan(i/2) sin(Ω)
             lM = M + ω + Ω
         
        where ω stands for the Perigee Argument and Ω stands for the Right Ascension of the Ascending Node.
    
        Alternate equinoctial parameters are derived from equinoctial parameter (see
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters` for more information) and they are
        particularly interesting for uncertainty propagation.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, double7: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.equals` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getAlternateEquinoctialParameters(self) -> 'AlternateEquinoctialParameters':
        """
            Convert current orbital parameters into alternate equinoctial parameters.
        
            Returns:
                current orbital parameters converted into alternate equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters`
        
        
        """
        ...
    def getApsisAltitudeParameters(self, double: float) -> 'ApsisAltitudeParameters':
        """
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
        
        """
        ...
    def getApsisRadiusParameters(self) -> 'ApsisRadiusParameters':
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        
        """
        ...
    def getCartesianParameters(self) -> 'CartesianParameters':
        """
            Convert current orbital parameters into cartesian parameters.
        
            Returns:
                current orbital parameters converted into cartesian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters`
        
        
        """
        ...
    def getCircularParameters(self) -> 'CircularParameters':
        """
            Convert current orbital parameters into circular parameters.
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    def getEquatorialParameters(self) -> 'EquatorialParameters':
        """
            Convert current orbital parameters into equatorial parameters.
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        
        """
        ...
    def getEquinoctialEx(self) -> float:
        """
            Get the first component of the eccentricity vector.
        
            Returns:
                e cos(ω + Ω), first component of the eccentricity vector
        
        
        """
        ...
    def getEquinoctialEy(self) -> float:
        """
            Get the second component of the eccentricity vector.
        
            Returns:
                e sin(ω + Ω), second component of the eccentricity vector
        
        
        """
        ...
    def getEquinoctialParameters(self) -> 'EquinoctialParameters':
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        
        """
        ...
    def getHx(self) -> float:
        """
            Get the first component of the inclination vector.
        
            Returns:
                tan(i/2) cos(Ω), first component of the inclination vector
        
        
        """
        ...
    def getHy(self) -> float:
        """
            Get the second component of the inclination vector.
        
            Returns:
                tan(i/2) sin(Ω), second component of the inclination vector
        
        
        """
        ...
    def getKeplerianParameters(self) -> 'KeplerianParameters':
        """
            Convert current orbital parameters into Keplerian parameters.
        
            Returns:
                current orbital parameters converted into Keplerian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters`
        
        
        """
        ...
    def getL(self, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> float:
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
        
            Returns:
                E + ω + Ω eccentric longitude argument (rad)
        
        
        """
        ...
    def getLM(self) -> float:
        """
            Get the mean longitude argument.
        
            Returns:
                M + ω + Ω true longitude argument (rad)
        
        
        """
        ...
    def getLv(self) -> float:
        """
            Get the true longitude argument.
        
            Returns:
                v + ω + Ω true longitude argument (rad)
        
        
        """
        ...
    def getN(self) -> float:
        """
            Get the mean motion.
        
            Returns:
                mean motion (1/s)
        
        
        """
        ...
    def getReentryParameters(self, double: float, double2: float) -> 'ReentryParameters':
        """
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
                f (double): flattening (f = (a-b)/a)
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
        
        """
        ...
    def getStelaEquinoctialParameters(self) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.hashCode` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of this orbit parameters object.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this object
        
        
        """
        ...

class ApsisAltitudeParameters(AbstractOrbitalParameters):
    """
    public class ApsisAltitudeParameters extends :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AbstractOrbitalParameters`
    
        This class handles periapsis altitude/apoapsis altitude parameters.
    
        The parameters used internally are the apsis elements which can be related to keplerian elements as follows:
    
          - periapsis altitude = a (1 - e) - req
          - apoapsis altitude = a (1 + e) - req
          - i
          - ω
          - Ω
          - v
    
        where Ω stands for the Right Ascension of the Ascending Node, v stands for true anomaly and req for central body radius
        (m)
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, double7: float, double8: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.equals` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getAe(self) -> float:
        """
            Getter for equatorial radius.
        
            Returns:
                equatorial radius (m)
        
        
        """
        ...
    def getAlternateEquinoctialParameters(self) -> AlternateEquinoctialParameters:
        """
            Convert current orbital parameters into alternate equinoctial parameters.
        
            Returns:
                current orbital parameters converted into alternate equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters`
        
        
        """
        ...
    def getAnomaly(self, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> float:
        """
            Get the anomaly.
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the angle
        
            Returns:
                anomaly (rad)
        
        
        """
        ...
    def getApoapsisAltitude(self) -> float:
        """
            Get the apoapsis altitude.
        
            Returns:
                apoapsis altitude (m)
        
        
        """
        ...
    def getApsisAltitudeParameters(self, double: float) -> 'ApsisAltitudeParameters':
        """
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                req (double): equatorial radius (m)
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
        
        """
        ...
    def getApsisRadiusParameters(self) -> 'ApsisRadiusParameters':
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        
        """
        ...
    def getCartesianParameters(self) -> 'CartesianParameters':
        """
            Convert current orbital parameters into cartesian parameters.
        
            Returns:
                current orbital parameters converted into cartesian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters`
        
        
        """
        ...
    def getCircularParameters(self) -> 'CircularParameters':
        """
            Convert current orbital parameters into circular parameters.
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    def getEquatorialParameters(self) -> 'EquatorialParameters':
        """
            Convert current orbital parameters into equatorial parameters.
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        
        """
        ...
    def getEquinoctialParameters(self) -> 'EquinoctialParameters':
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    def getKeplerianParameters(self) -> 'KeplerianParameters':
        """
            Convert current orbital parameters into Keplerian parameters.
        
            Returns:
                current orbital parameters converted into Keplerian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters`
        
        
        """
        ...
    def getPeriapsisAltitude(self) -> float:
        """
            Get the periapsis altitude.
        
            Returns:
                periapsis altitude (m)
        
        
        """
        ...
    def getPerigeeArgument(self) -> float:
        """
            Get the perigee argument.
        
            Returns:
                perigee argument (rad)
        
        
        """
        ...
    def getReentryParameters(self, double: float, double2: float) -> 'ReentryParameters':
        """
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                req (double): equatorial radius (m)
                f (double): flattening (f = (a-b)/a)
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
        
        """
        ...
    def getRightAscensionOfAscendingNode(self) -> float:
        """
            Get the right ascension of the ascending node.
        
            Returns:
                right ascension of the ascending node (rad)
        
        
        """
        ...
    def getStelaEquinoctialParameters(self) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.hashCode` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of this Orbit object.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this object
        
        
        """
        ...

class ApsisRadiusParameters(AbstractOrbitalParameters):
    """
    public class ApsisRadiusParameters extends :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AbstractOrbitalParameters`
    
        This class handles periapsis/apoapsis parameters.
    
        The parameters used internally are the apsis elements which can be related to keplerian elements as follows:
    
          - periapsis = a (1 - e)
          - apoapsis = a (1 + e)
          - i
          - ω
          - Ω
          - v
    
        where Ω stands for the Right Ascension of the Ascending Node and v stands for true anomaly
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, double7: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.equals` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getAlternateEquinoctialParameters(self) -> AlternateEquinoctialParameters:
        """
            Convert current orbital parameters into alternate equinoctial parameters.
        
            Returns:
                current orbital parameters converted into alternate equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters`
        
        
        """
        ...
    def getAnomaly(self, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> float:
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
    def getApsisAltitudeParameters(self, double: float) -> ApsisAltitudeParameters:
        """
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
        
        """
        ...
    def getApsisRadiusParameters(self) -> 'ApsisRadiusParameters':
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        
        """
        ...
    def getCartesianParameters(self) -> 'CartesianParameters':
        """
            Convert current orbital parameters into cartesian parameters.
        
            Returns:
                current orbital parameters converted into cartesian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters`
        
        
        """
        ...
    def getCircularParameters(self) -> 'CircularParameters':
        """
            Convert current orbital parameters into circular parameters.
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    def getEquatorialParameters(self) -> 'EquatorialParameters':
        """
            Convert current orbital parameters into equatorial parameters.
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        
        """
        ...
    def getEquinoctialParameters(self) -> 'EquinoctialParameters':
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    def getKeplerianParameters(self) -> 'KeplerianParameters':
        """
            Convert current orbital parameters into Keplerian parameters.
        
            Returns:
                current orbital parameters converted into Keplerian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters`
        
        
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
    def getReentryParameters(self, double: float, double2: float) -> 'ReentryParameters':
        """
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
                f (double): flattening (f = (a-b)/a)
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
        
        """
        ...
    def getRightAscensionOfAscendingNode(self) -> float:
        """
            Get the right ascension of the ascending node.
        
            Returns:
                right ascension of the ascending node (rad)
        
        
        """
        ...
    def getStelaEquinoctialParameters(self) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.hashCode` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of this Orbit object.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this object
        
        
        """
        ...

class CartesianParameters(AbstractOrbitalParameters):
    """
    public class CartesianParameters extends :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AbstractOrbitalParameters`
    
        This class holds cartesian orbital parameters.
    
        The parameters used internally are the cartesian coordinates:
    
          - x
          - y
          - z
          - xDot
          - yDot
          - zDot
    
        contained in :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    @typing.overload
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.equals` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getAlternateEquinoctialParameters(self) -> AlternateEquinoctialParameters:
        """
            Convert current orbital parameters into alternate equinoctial parameters.
        
            Returns:
                current orbital parameters converted into alternate equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters`
        
        
        """
        ...
    @typing.overload
    def getApsisAltitudeParameters(self, double: float) -> ApsisAltitudeParameters:
        """
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
                mu (double): central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
        
        """
        ...
    @typing.overload
    def getApsisAltitudeParameters(self, double: float, double2: float) -> ApsisAltitudeParameters: ...
    @typing.overload
    def getApsisRadiusParameters(self) -> ApsisRadiusParameters:
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        """
        ...
    @typing.overload
    def getApsisRadiusParameters(self, double: float) -> ApsisRadiusParameters:
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Parameters:
                mu (double): central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        
        """
        ...
    def getCartesianParameters(self) -> 'CartesianParameters':
        """
            Convert current orbital parameters into cartesian parameters.
        
            Returns:
                current orbital parameters converted into cartesian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters`
        
        
        """
        ...
    @typing.overload
    def getCircularParameters(self) -> 'CircularParameters':
        """
            Convert current orbital parameters into circular parameters.
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        """
        ...
    @typing.overload
    def getCircularParameters(self, double: float) -> 'CircularParameters':
        """
            Convert current orbital parameters into circular parameters.
        
            Parameters:
                mu (double): central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    @typing.overload
    def getEquatorialParameters(self) -> 'EquatorialParameters':
        """
            Convert current orbital parameters into equatorial parameters.
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        """
        ...
    @typing.overload
    def getEquatorialParameters(self, double: float) -> 'EquatorialParameters':
        """
            Convert current orbital parameters into equatorial parameters.
        
            Parameters:
                mu (double): central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        
        """
        ...
    @typing.overload
    def getEquinoctialParameters(self) -> 'EquinoctialParameters':
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        """
        ...
    @typing.overload
    def getEquinoctialParameters(self, double: float) -> 'EquinoctialParameters':
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Parameters:
                mu (double): central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        
        """
        ...
    @typing.overload
    def getKeplerianParameters(self) -> 'KeplerianParameters':
        """
            Convert current orbital parameters into Keplerian parameters.
        
            Returns:
                current orbital parameters converted into Keplerian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters`
        
        """
        ...
    @typing.overload
    def getKeplerianParameters(self, double: float) -> 'KeplerianParameters':
        """
            Convert current orbital parameters into circular parameters.
        
            Parameters:
                mu (double): central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    def getPVCoordinates(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates:
        """
            Get the PV coordinates.
        
            Returns:
                pvCoordinates
        
        
        """
        ...
    def getPosition(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the position.
        
            Returns:
                position
        
        
        """
        ...
    @typing.overload
    def getReentryParameters(self, double: float, double2: float) -> 'ReentryParameters':
        """
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
                f (double): flattening (f = (a-b)/a)
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
                f (double): flattening (f = (a-b)/a)
                mu (double): central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
        
        """
        ...
    @typing.overload
    def getReentryParameters(self, double: float, double2: float, double3: float) -> 'ReentryParameters': ...
    @typing.overload
    def getStelaEquinoctialParameters(self) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        """
        ...
    @typing.overload
    def getStelaEquinoctialParameters(self, double: float) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Parameters:
                mu (double): central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        
        """
        ...
    def getVelocity(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the velocity.
        
            Returns:
                velocity
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.hashCode` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of this Orbit object.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this object
        
        
        """
        ...

class CircularParameters(AbstractOrbitalParameters):
    """
    public class CircularParameters extends :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AbstractOrbitalParameters`
    
        This class handles circular orbital parameters.
    
        The parameters used internally are the circular elements which can be related to keplerian elements as follows:
    
          - a
          - e :sub:`x` = e cos(ω)
          - e :sub:`y` = e sin(ω)
          - i
          - Ω
          - α :sub:`v` = v + ω
    
        where Ω stands for the Right Ascension of the Ascending Node and α :sub:`v` stands for the true latitude argument
    
        The conversion equations from and to keplerian elements given above hold only when both sides are unambiguously defined,
        i.e. when orbit is neither equatorial nor circular. When orbit is circular (but not equatorial), the circular parameters
        are still unambiguously defined whereas some keplerian elements (more precisely ω and Ω) become ambiguous. When orbit
        is equatorial, neither the keplerian nor the circular parameters can be defined unambiguously.
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters` is the recommended way to represent
        orbits.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, double7: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.equals` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
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
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getAlpha(self, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> float:
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
    def getAlternateEquinoctialParameters(self) -> AlternateEquinoctialParameters:
        """
            Convert current orbital parameters into alternate equinoctial parameters.
        
            Returns:
                current orbital parameters converted into alternate equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters`
        
        
        """
        ...
    def getApsisAltitudeParameters(self, double: float) -> ApsisAltitudeParameters:
        """
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
        
        """
        ...
    def getApsisRadiusParameters(self) -> ApsisRadiusParameters:
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        
        """
        ...
    def getCartesianParameters(self) -> CartesianParameters:
        """
            Convert current orbital parameters into cartesian parameters.
        
            Returns:
                current orbital parameters converted into cartesian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters`
        
        
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
    def getCircularParameters(self) -> 'CircularParameters':
        """
            Convert current orbital parameters into circular parameters.
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    def getEquatorialParameters(self) -> 'EquatorialParameters':
        """
            Convert current orbital parameters into equatorial parameters.
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        
        """
        ...
    def getEquinoctialParameters(self) -> 'EquinoctialParameters':
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    def getKeplerianParameters(self) -> 'KeplerianParameters':
        """
            Convert current orbital parameters into Keplerian parameters.
        
            Returns:
                current orbital parameters converted into Keplerian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters`
        
        
        """
        ...
    def getReentryParameters(self, double: float, double2: float) -> 'ReentryParameters':
        """
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
                f (double): flattening (f = (a-b)/a)
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
        
        """
        ...
    def getRightAscensionOfAscendingNode(self) -> float:
        """
            Get the right ascension of the ascending node.
        
            Returns:
                right ascension of the ascending node (rad)
        
        
        """
        ...
    def getStelaEquinoctialParameters(self) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.hashCode` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of this Orbit object.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this object
        
        
        """
        ...

class EquatorialParameters(AbstractOrbitalParameters):
    """
    public class EquatorialParameters extends :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AbstractOrbitalParameters`
    
        This class handles non circular equatorial orbital parameters.
    
        The parameters used internally are the following elements:
    
        .. code-block: java
        
        
             a semi-major axis (m)
             e eccentricity
             pomega = ω + Ω , longitude of the periapsis;
             ix = 2 sin(i/2) cos(Ω), first component of inclination vector
             iy = 2 sin(i/2) sin(Ω), second component of inclination vector
             anomaly (M or E or v);, mean, eccentric or true anomaly (rad)
         
        where ω stands for the Periapsis Argument, Ω stands for the Right Ascension of the Ascending Node.
    
        When orbit is either equatorial or circular, some keplerian elements (more precisely ω and Ω) become ambiguous so this
        class should not be used for such orbits. For this reason,
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters` is the recommended way to represent
        orbits.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, double7: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.equals` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
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
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getAlternateEquinoctialParameters(self) -> AlternateEquinoctialParameters:
        """
            Convert current orbital parameters into alternate equinoctial parameters.
        
            Returns:
                current orbital parameters converted into alternate equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters`
        
        
        """
        ...
    def getAnomaly(self, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> float:
        """
            Get the anomaly.
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the angle
        
            Returns:
                anomaly (rad)
        
        
        """
        ...
    def getApsisAltitudeParameters(self, double: float) -> ApsisAltitudeParameters:
        """
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
        
        """
        ...
    def getApsisRadiusParameters(self) -> ApsisRadiusParameters:
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        
        """
        ...
    def getCartesianParameters(self) -> CartesianParameters:
        """
            Convert current orbital parameters into cartesian parameters.
        
            Returns:
                current orbital parameters converted into cartesian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters`
        
        
        """
        ...
    def getCircularParameters(self) -> CircularParameters:
        """
            Convert current orbital parameters into circular parameters.
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    def getE(self) -> float:
        """
            Get the eccentricity.
        
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
    def getEquatorialParameters(self) -> 'EquatorialParameters':
        """
            Convert current orbital parameters into equatorial parameters.
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        
        """
        ...
    def getEquinoctialParameters(self) -> 'EquinoctialParameters':
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        
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
    def getKeplerianParameters(self) -> 'KeplerianParameters':
        """
            Convert current orbital parameters into Keplerian parameters.
        
            Returns:
                current orbital parameters converted into Keplerian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters`
        
        
        """
        ...
    def getMeanAnomaly(self) -> float:
        """
            Get the mean anomaly.
        
            Returns:
                mean anomaly (rad)
        
        
        """
        ...
    def getPomega(self) -> float:
        """
            Get the longitude of the periapsis (ω + Ω).
        
            Returns:
                longitude of the periapsis (rad)
        
        
        """
        ...
    def getReentryParameters(self, double: float, double2: float) -> 'ReentryParameters':
        """
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
                f (double): flattening (f = (a-b)/a)
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
        
        """
        ...
    def getStelaEquinoctialParameters(self) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        
        """
        ...
    def getTrueAnomaly(self) -> float:
        """
            Get the true anomaly.
        
            Returns:
                true anomaly (rad)
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.hashCode` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of this non circular equatorial orbital parameters object.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this object
        
        
        """
        ...

class EquinoctialParameters(AbstractOrbitalParameters):
    """
    public class EquinoctialParameters extends :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AbstractOrbitalParameters`
    
        This class handles equinoctial orbital parameters, which can support both circular and equatorial orbits.
    
        The parameters used internally are the equinoctial elements which can be related to keplerian elements as follows:
    
        .. code-block: java
        
        
             a
             ex = e cos(ω + Ω)
             ey = e sin(ω + Ω)
             hx = tan(i/2) cos(Ω)
             hy = tan(i/2) sin(Ω)
             lv = v + ω + Ω
         
        where ω stands for the Perigee Argument and Ω stands for the Right Ascension of the Ascending Node.
    
        The conversion equations from and to keplerian elements given above hold only when both sides are unambiguously defined,
        i.e. when orbit is neither equatorial nor circular. When orbit is either equatorial or circular, the equinoctial
        parameters are still unambiguously defined whereas some keplerian elements (more precisely ω and Ω) become ambiguous.
        For this reason, equinoctial parameters are the recommended way to represent orbits.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, double7: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.equals` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
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
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getAlternateEquinoctialParameters(self) -> AlternateEquinoctialParameters:
        """
            Convert current orbital parameters into alternate equinoctial parameters.
        
            Returns:
                current orbital parameters converted into alternate equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters`
        
        
        """
        ...
    def getApsisAltitudeParameters(self, double: float) -> ApsisAltitudeParameters:
        """
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
        
        """
        ...
    def getApsisRadiusParameters(self) -> ApsisRadiusParameters:
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        
        """
        ...
    def getCartesianParameters(self) -> CartesianParameters:
        """
            Convert current orbital parameters into cartesian parameters.
        
            Returns:
                current orbital parameters converted into cartesian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters`
        
        
        """
        ...
    def getCircularParameters(self) -> CircularParameters:
        """
            Convert current orbital parameters into circular parameters.
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    def getEquatorialParameters(self) -> EquatorialParameters:
        """
            Convert current orbital parameters into equatorial parameters.
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        
        """
        ...
    def getEquinoctialEx(self) -> float:
        """
            Get the first component of the eccentricity vector.
        
            Returns:
                e cos(ω + Ω), first component of the eccentricity vector
        
        
        """
        ...
    def getEquinoctialEy(self) -> float:
        """
            Get the second component of the eccentricity vector.
        
            Returns:
                e sin(ω + Ω), second component of the eccentricity vector
        
        
        """
        ...
    def getEquinoctialParameters(self) -> 'EquinoctialParameters':
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        
        """
        ...
    def getHx(self) -> float:
        """
            Get the first component of the inclination vector.
        
            Returns:
                tan(i/2) cos(Ω), first component of the inclination vector
        
        
        """
        ...
    def getHy(self) -> float:
        """
            Get the second component of the inclination vector.
        
            Returns:
                tan(i/2) sin(Ω), second component of the inclination vector
        
        
        """
        ...
    def getKeplerianParameters(self) -> 'KeplerianParameters':
        """
            Convert current orbital parameters into Keplerian parameters.
        
            Returns:
                current orbital parameters converted into Keplerian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters`
        
        
        """
        ...
    def getL(self, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> float:
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
        
            Returns:
                E + ω + Ω eccentric longitude argument (rad)
        
        
        """
        ...
    def getLM(self) -> float:
        """
            Get the mean longitude argument.
        
            Returns:
                M + ω + Ω mean longitude argument (rad)
        
        
        """
        ...
    def getLv(self) -> float:
        """
            Get the true longitude argument.
        
            Returns:
                v + ω + Ω true longitude argument (rad)
        
        
        """
        ...
    def getReentryParameters(self, double: float, double2: float) -> 'ReentryParameters':
        """
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
                f (double): flattening (f = (a-b)/a)
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
        
        """
        ...
    def getStelaEquinoctialParameters(self) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.hashCode` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of this orbit parameters object.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this object
        
        
        """
        ...

class KeplerianParameters(AbstractOrbitalParameters):
    """
    public class KeplerianParameters extends :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AbstractOrbitalParameters`
    
        This class handles traditional keplerian orbital parameters.
    
        The parameters used internally are the classical keplerian elements:
    
        .. code-block: java
        
        
             a
             e
             i
             ω
             Ω
             v
         
        where ω stands for the Perigee Argument, Ω stands for the Right Ascension of the Ascending Node and v stands for the
        true anomaly.
    
        The eccentricity must be greater than or equal to zero.
    
        This class supports hyperbolic orbits, using the convention that semi major axis is negative for such orbits (and of
        course eccentricity is greater than 1).
    
        When orbit is either equatorial or circular, some keplerian elements (more precisely ω and Ω) become ambiguous so this
        class should not be used for such orbits. For this reason,
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters` is the recommended way to represent
        orbits.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, double7: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.equals` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
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
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getAlternateEquinoctialParameters(self) -> AlternateEquinoctialParameters:
        """
            Convert current orbital parameters into alternate equinoctial parameters.
        
            Returns:
                current orbital parameters converted into alternate equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters`
        
        
        """
        ...
    def getAnomaly(self, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> float:
        """
            Get the anomaly.
        
            Parameters:
                type (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): type of the angle
        
            Returns:
                anomaly (rad)
        
        
        """
        ...
    def getApsisAltitudeParameters(self, double: float) -> ApsisAltitudeParameters:
        """
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
        
        """
        ...
    def getApsisRadiusParameters(self) -> ApsisRadiusParameters:
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        
        """
        ...
    def getCartesianParameters(self) -> CartesianParameters:
        """
            Convert current orbital parameters into cartesian parameters.
        
            Returns:
                current orbital parameters converted into cartesian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters`
        
        
        """
        ...
    def getCircularParameters(self) -> CircularParameters:
        """
            Convert current orbital parameters into circular parameters.
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    def getE(self) -> float:
        """
            Get the eccentricity.
        
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
    def getEquatorialParameters(self) -> EquatorialParameters:
        """
            Convert current orbital parameters into equatorial parameters.
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        
        """
        ...
    def getEquinoctialParameters(self) -> EquinoctialParameters:
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination.
        
            Returns:
                inclination (rad)
        
        
        """
        ...
    def getKeplerianParameters(self) -> 'KeplerianParameters':
        """
            Convert current orbital parameters into Keplerian parameters.
        
            Returns:
                current orbital parameters converted into Keplerian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters`
        
        
        """
        ...
    def getMeanAnomaly(self) -> float:
        """
            Get the mean anomaly.
        
            Returns:
                mean anomaly (rad)
        
        
        """
        ...
    def getPerigeeArgument(self) -> float:
        """
            Get the perigee argument.
        
            Returns:
                perigee argument (rad)
        
        
        """
        ...
    def getReentryParameters(self, double: float, double2: float) -> 'ReentryParameters':
        """
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
                f (double): flattening (f = (a-b)/a)
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
        
        """
        ...
    def getRightAscensionOfAscendingNode(self) -> float:
        """
            Get the right ascension of the ascending node.
        
            Returns:
                right ascension of the ascending node (rad)
        
        
        """
        ...
    def getStelaEquinoctialParameters(self) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        
        """
        ...
    def getTrueAnomaly(self) -> float:
        """
            Get the true anomaly.
        
            Returns:
                true anomaly (rad)
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.hashCode` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    @staticmethod
    def solveKeplerEquationEccentricAnomaly(double: float, double2: float) -> float:
        """
            Solve the Kepler equation to get the eccentric anomaly : E - e*sin(E)= M
        
            Parameters:
                meanAnomaly (double): the mean anomaly (rad)
                eccentricity (double): the eccentricity of the orbit
        
            Returns:
                the eccentric anomaly (rad)
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of this keplerian parameters object.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this object
        
        
        """
        ...

class ReentryParameters(AbstractOrbitalParameters):
    """
    public class ReentryParameters extends :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AbstractOrbitalParameters`
    
        This class handles reentry parameters.
    
        The parameters used internally are the following elements:
    
        .. code-block: java
        
        
             altitude (m)
             latitude (m)
             longitude (m)
             velocity (m/s)
             slope of velocity (rad)
             azimuth of velocity (rad)
         
    
        2 more parameters defining the central body are added:
    
        .. code-block: java
        
        
              equatorial radius (m)
              flattening
         
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    EPS: typing.ClassVar[float] = ...
    """
    public static final double EPS
    
        Epsilon for specific cases.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.equals` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two orbits are equal
        
        
        """
        ...
    def getAe(self) -> float:
        """
            Getter for the equatorial radius.
        
            Returns:
                equatorial radius (m)
        
        
        """
        ...
    def getAlternateEquinoctialParameters(self) -> AlternateEquinoctialParameters:
        """
            Convert current orbital parameters into alternate equinoctial parameters.
        
            Returns:
                current orbital parameters converted into alternate equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters`
        
        
        """
        ...
    def getAltitude(self) -> float:
        """
            Getter for the altitude.
        
            Returns:
                altitude (m)
        
        
        """
        ...
    def getApsisAltitudeParameters(self, double: float) -> ApsisAltitudeParameters:
        """
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                req (double): equatorial radius (m)
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
        
        """
        ...
    def getApsisRadiusParameters(self) -> ApsisRadiusParameters:
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        
        """
        ...
    def getAzimuth(self) -> float:
        """
            Getter for the azimuth of velocity.
        
            Returns:
                azimuth of velocity (rad)
        
        
        """
        ...
    def getCartesianParameters(self) -> CartesianParameters:
        """
            Convert current orbital parameters into cartesian parameters.
        
            Returns:
                current orbital parameters converted into cartesian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters`
        
        
        """
        ...
    def getCircularParameters(self) -> CircularParameters:
        """
            Convert current orbital parameters into circular parameters.
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    def getEquatorialParameters(self) -> EquatorialParameters:
        """
            Convert current orbital parameters into equatorial parameters.
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        
        """
        ...
    def getEquinoctialParameters(self) -> EquinoctialParameters:
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        
        """
        ...
    def getF(self) -> float:
        """
            Getter for the flattening.
        
            Returns:
                flattening
        
        
        """
        ...
    def getKeplerianParameters(self) -> KeplerianParameters:
        """
            Convert current orbital parameters into Keplerian parameters.
        
            Returns:
                current orbital parameters converted into Keplerian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters`
        
        
        """
        ...
    def getLatitude(self) -> float:
        """
            Getter for the latitude.
        
            Returns:
                latitude (rad)
        
        
        """
        ...
    def getLongitude(self) -> float:
        """
            Getter for the longitude.
        
            Returns:
                longitude (rad)
        
        
        """
        ...
    def getReentryParameters(self, double: float, double2: float) -> 'ReentryParameters':
        """
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                req (double): equatorial radius (m)
                flat (double): flattening (f = (a-b)/a)
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
        
        """
        ...
    def getSlope(self) -> float:
        """
            Getter for the slope of velocity.
        
            Returns:
                slope of velocity (rad)
        
        
        """
        ...
    def getStelaEquinoctialParameters(self) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        
        """
        ...
    def getVelocity(self) -> float:
        """
            Getter for the velocity.
        
            Returns:
                velocity (m/s)
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.hashCode` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of the reentry parameters.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this reentry parameters
        
        
        """
        ...

class StelaEquinoctialParameters(AbstractOrbitalParameters):
    """
    public class StelaEquinoctialParameters extends :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AbstractOrbitalParameters`
    
        This class handles the equinoctial orbital parameters used in Stela; it has been created because the equinoctial
        parameters associated to Stela differ from the
        :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters` parameters.
    
        The parameters used internally are the equinoctial elements which can be related to keplerian elements as follows:
    
        .. code-block: java
        
        
             a
             ex = e cos(ω + Ω)
             ey = e sin(ω + Ω)
             ix = sin(i/2) cos(Ω)
             iy = sin(i/2) sin(Ω)
             lM = M + ω + Ω
         
        where ω stands for the Perigee Argument and Ω stands for the Right Ascension of the Ascending Node.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    I_LIM: typing.ClassVar[float] = ...
    """
    public static final double I_LIM
    
        Inclination upper limit.
    
    """
    SIN_I_LIM: typing.ClassVar[float] = ...
    """
    public static final double SIN_I_LIM
    
        Sinus of half limit inclination in type 8.
    
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, boolean: bool): ...
    def correctInclination(self, double: float, double2: float) -> typing.MutableSequence[float]:
        """
            Inclination correction because of inclination singularity in StelaEquinoctial parameters around 180deg.
        
            Parameters:
                ixIn (double): first component of inclination vector
                iyIn (double): second component of inclination vector
        
            Returns:
                corrected inclination components
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two orbits.
        
            Orbits are considered equals if they have the same type and all their attributes are equals. In particular, the orbits
            frame are considered equals if they represent the same instance. If they have the same attributes but are not the same
            instance, the method will return false.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.equals` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
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
        
            Returns:
                semi-major axis (m)
        
        
        """
        ...
    def getAlternateEquinoctialParameters(self) -> AlternateEquinoctialParameters:
        """
            Convert current orbital parameters into alternate equinoctial parameters.
        
            Returns:
                current orbital parameters converted into alternate equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.AlternateEquinoctialParameters`
        
        
        """
        ...
    def getApsisAltitudeParameters(self, double: float) -> ApsisAltitudeParameters:
        """
            Convert current orbital parameters into apsis (using altitude) parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
        
            Returns:
                current orbital parameters converted into apsis (using altitude) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisAltitudeParameters`
        
        
        """
        ...
    def getApsisRadiusParameters(self) -> ApsisRadiusParameters:
        """
            Convert current orbital parameters into apsis (using radius) parameters.
        
            Returns:
                current orbital parameters converted into apsis (using radius) parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ApsisRadiusParameters`
        
        
        """
        ...
    def getCartesianParameters(self) -> CartesianParameters:
        """
            Convert current orbital parameters into cartesian parameters.
        
            Returns:
                current orbital parameters converted into cartesian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CartesianParameters`
        
        
        """
        ...
    def getCircularParameters(self) -> CircularParameters:
        """
            Convert current orbital parameters into circular parameters.
        
            Returns:
                current orbital parameters converted into circular parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.CircularParameters`
        
        
        """
        ...
    def getEquatorialParameters(self) -> EquatorialParameters:
        """
            Convert current orbital parameters into equatorial parameters.
        
            Returns:
                current orbital parameters converted into equatorial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquatorialParameters`
        
        
        """
        ...
    def getEquinoctialEx(self) -> float:
        """
            Get the first component of the eccentricity vector.
        
            Returns:
                e cos(ω + Ω), first component of the eccentricity vector
        
        
        """
        ...
    def getEquinoctialEy(self) -> float:
        """
            Get the second component of the eccentricity vector.
        
            Returns:
                e sin(ω + Ω), second component of the eccentricity vector
        
        
        """
        ...
    def getEquinoctialParameters(self) -> EquinoctialParameters:
        """
            Convert current orbital parameters into equinoctial parameters.
        
            Returns:
                current orbital parameters converted into equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.EquinoctialParameters`
        
        
        """
        ...
    def getIx(self) -> float:
        """
            Get the first component of the inclination vector.
        
            Returns:
                sin(i/2) cos(Ω), first component of the inclination vector
        
        
        """
        ...
    def getIy(self) -> float:
        """
            Get the second component of the inclination vector.
        
            Returns:
                sin(i/2) sin(Ω), second component of the inclination vector
        
        
        """
        ...
    def getKeplerianParameters(self) -> KeplerianParameters:
        """
            Convert current orbital parameters into Keplerian parameters.
        
            Returns:
                current orbital parameters converted into Keplerian parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.KeplerianParameters`
        
        
        """
        ...
    def getLM(self) -> float:
        """
            Get the mean longitude argument.
        
            Returns:
                M + ω + Ω mean longitude argument (rad)
        
        
        """
        ...
    def getReentryParameters(self, double: float, double2: float) -> ReentryParameters:
        """
            Convert current orbital parameters into reentry parameters.
        
            Parameters:
                ae (double): equatorial radius (m)
                f (double): flattening (f = (a-b)/a)
        
            Returns:
                current orbital parameters converted into reentry parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.ReentryParameters`
        
        
        """
        ...
    def getStelaEquinoctialParameters(self) -> 'StelaEquinoctialParameters':
        """
            Convert current orbital parameters into Stela equinoctial parameters.
        
            Returns:
                current orbital parameters converted into Stela equinoctial parameters
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters`
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the orbit.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters.hashCode` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters`
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of this orbit parameters object.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this object
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.orbits.orbitalparameters")``.

    AbstractOrbitalParameters: typing.Type[AbstractOrbitalParameters]
    AlternateEquinoctialCoordinate: typing.Type[AlternateEquinoctialCoordinate]
    AlternateEquinoctialParameters: typing.Type[AlternateEquinoctialParameters]
    ApsisAltitudeCoordinate: typing.Type[ApsisAltitudeCoordinate]
    ApsisAltitudeParameters: typing.Type[ApsisAltitudeParameters]
    ApsisRadiusCoordinate: typing.Type[ApsisRadiusCoordinate]
    ApsisRadiusParameters: typing.Type[ApsisRadiusParameters]
    CartesianCoordinate: typing.Type[CartesianCoordinate]
    CartesianParameters: typing.Type[CartesianParameters]
    CircularCoordinate: typing.Type[CircularCoordinate]
    CircularParameters: typing.Type[CircularParameters]
    EquatorialCoordinate: typing.Type[EquatorialCoordinate]
    EquatorialParameters: typing.Type[EquatorialParameters]
    EquinoctialCoordinate: typing.Type[EquinoctialCoordinate]
    EquinoctialParameters: typing.Type[EquinoctialParameters]
    IOrbitalParameters: typing.Type[IOrbitalParameters]
    KeplerianCoordinate: typing.Type[KeplerianCoordinate]
    KeplerianParameters: typing.Type[KeplerianParameters]
    OrbitalCoordinate: typing.Type[OrbitalCoordinate]
    ReentryParameters: typing.Type[ReentryParameters]
    StelaEquinoctialParameters: typing.Type[StelaEquinoctialParameters]
