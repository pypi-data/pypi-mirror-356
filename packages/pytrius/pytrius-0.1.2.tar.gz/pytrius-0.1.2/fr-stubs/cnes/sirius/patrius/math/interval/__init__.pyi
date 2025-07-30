
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.geometry.euclidean.twod
import java.io
import java.lang
import java.util
import typing



class AbstractInterval:
    """
    public abstract class AbstractInterval extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
    
        - very simple class to represent an interval only by its ending point nature : this is what all intervals have in
        common.
    
        - This class is abstract : it can't be instanced.
    
        - It contains no method.
        See DV-MATHS_50, DV-DATES_150
    
        Since:
            1.0
    """
    def __init__(self): ...
    def getLowerEndPoint(self) -> 'IntervalEndpointType':
        """
        
            Returns:
                the lowerEndPoint
        
        
        """
        ...
    def getUpperEndPoint(self) -> 'IntervalEndpointType':
        """
        
            Returns:
                the upperEndPoint
        
        
        """
        ...

class AngleTools:
    """
    public final class AngleTools extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
    
        This class provides static methods for angles :
    
        - angles computation,
    
        - comparison,
    
        - arithmetic and trigonometric operations.
    
        Since:
            1.0
    """
    @staticmethod
    def angleInInterval(double: float, angleInterval: 'AngleInterval') -> float:
        """
            Computes the angle in the given interval modulo 2pi. There are particular cases : numerical quality issue solving in the
            following cases : - the interval is of the form [a, a + 2PI[ If angle is lower than lower bound and angle + 2Pi larger
            than higher bound : lower bound is returned - the interval is of the form ]a, a + 2PI] If angle is larger than larger
            bound and angle - 2Pi lower than lower bound : larger bound is returned These cases occur because of the non-identical
            repartition of doubles around the two interval boundaries.
        
            Parameters:
                angle (double): angle to be expressed inside the given interval
                interval (:class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval`): interval of expression
        
            Returns:
                the angle expressed in the interval
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: the angle is'nt in the interval modulo 2PI
        
            Since:
                1.0
        
        
        """
        ...
    @staticmethod
    def complementaryAngle(double: float, angleInterval: 'AngleInterval') -> float:
        """
            Computes the complementary (PI/2 - angle) of the input angle, and then tries to express it in the input interval.
        
            Parameters:
                angle (double): the angle to get the complementary
                interval (:class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval`): the interval to express the result
        
            Returns:
                double : complementary angle
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the resulting angle is'nt in the interval, modulo 2PI See DV-MATHS_80 .
        
            Since:
                1.0
        
        
        """
        ...
    @staticmethod
    def equal(double: float, double2: float, angleInterval: 'AngleInterval') -> bool:
        """
            Tests the equality of two angles after expressing them in the same interval.
        
            Parameters:
                alpha (double): one angle
                beta (double): one angle
                interval (:class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval`): the interval to express the angles
        
            Returns:
                boolean : true if equal
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if one angle is'nt in the interval, modulo 2PI
        
            Since:
                1.0
        
        
        """
        ...
    @staticmethod
    def getAngleBewteen2Vector3D(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the angle between 2 vectors 3D. To do so, we use the method angle(Vector3D, Vector3D) of
            :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D` .
        
            Parameters:
                vector1 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the first vector
                vector2 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the second vector
        
            Returns:
                double angle = the positive value of the angle between the two vectors, the angle is defined between :code:`0` and
                :code:`PI`. See DV-MATHS_100
        
            Since:
                1.0
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D.angle`
        
        
        """
        ...
    @staticmethod
    def getAngleFromCosineAndSine(double: float, double2: float) -> float:
        """
            Computes an angle from the sine and the cosine
        
            Parameters:
                cos (double): : the cosine of the angle we want to know the value
                sin (double): : the sine of the angle we want to know the value
        
            Returns:
                double angle = the angle given by sine and cosine between :code:`-PI` and :code:`PI` See DV-MATHS_100 .
        
            Since:
                1.0
        
        
        """
        ...
    @staticmethod
    def getOrientedAngleBetween2Vector2D(vector2D: fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D, vector2D2: fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D) -> float:
        """
            Computes the oriented angle between 2 vectors 2D.
        
            Parameters:
                vector1 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): the first vector
                vector2 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.twod.Vector2D`): the second vector
        
            Returns:
                double angle = the value of the oriented angle between the two vectors, the angle is defined between :code:`-2 PI` and
                :code:`2 PI`. See DV-MATHS_100 .
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if at least one norm is zero
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if at least one norm is infinity
        
            Since:
                1.0
        
        
        """
        ...
    @staticmethod
    def getOrientedAngleBewteen2Vector3D(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the oriented angle between 2 vectors 3D.
        
            Parameters:
                vector1 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the first vector
                vector2 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the second vector
                vector3 (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the third vector which defines the orientation
        
            Returns:
                double angle = the value of the oriented angle between the two vectors, the angle is defined between :code:`-PI` and
                :code:`PI`. See DV-MATHS_100 .
        
            Raises:
                : if the cross product is wrong
        
            Since:
                1.0
        
        
        """
        ...
    @staticmethod
    def greaterOrEqual(double: float, double2: float, angleInterval: 'AngleInterval') -> bool:
        """
            Tests if one angle is greater or equal to another after expressing them in the same interval.
        
            Parameters:
                alpha (double): : one angle
                beta (double): : one angle
                interval (:class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval`): the interval to express the angles
        
            Returns:
                boolean : true is greater or equal
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if one angle is'nt in the interval, modulo 2PI
        
            Since:
                1.0
        
        
        """
        ...
    @staticmethod
    def greaterStrict(double: float, double2: float, angleInterval: 'AngleInterval') -> bool:
        """
            Tests if one angle is strictly greater than another after expressing them in the same interval.
        
            Parameters:
                alpha (double): : one angle
                beta (double): : one angle
                interval (:class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval`): the interval to express the angles
        
            Returns:
                boolean : true is greater
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if one angle is'nt in the interval, modulo 2PI
        
            Since:
                1.0
        
        
        """
        ...
    @staticmethod
    def lowerOrEqual(double: float, double2: float, angleInterval: 'AngleInterval') -> bool:
        """
            Tests if one angle is lower or equal to another after expressing them in the same interval.
        
            Parameters:
                alpha (double): one angle
                beta (double): one angle
                interval (:class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval`): the interval to express the angles
        
            Returns:
                boolean : true if lower or equal
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if one angle is'nt in the interval, modulo 2PI
        
            Since:
                1.0
        
        
        """
        ...
    @staticmethod
    def lowerStrict(double: float, double2: float, angleInterval: 'AngleInterval') -> bool:
        """
            Tests if one angle is strictly lower than another after expressing them in the same interval.
        
            Parameters:
                alpha (double): : one angle
                beta (double): : one angle
                interval (:class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval`): the interval to express the angles
        
            Returns:
                boolean : true if lower
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if one angle is'nt in the interval, modulo 2PI
        
            Since:
                1.0
        
        
        """
        ...
    @staticmethod
    def meanAngle(*double: float) -> float:
        """
            Computes the mean of two circular quantities or angles. Returned value is in [0 ; 2*PI[.
        
            For the case of more than two input angles, since the arithmetic mean is not appropriate for circular quantities due to
            angular wrapping, the angles are converted to their corresponding points on the unit circle, i.e. converting its polar
            coordinates to cartesian, and then computing the arithmetic mean of those two points.
        
            **Note:** Results produced by this computation may seem counterintuitive since they are different from what would be
            obtained using a standard arithmetic mean of the values, with this difference being greater when the angles are widely
            distributed.
        
            Parameters:
                angles (double...): set of input angles [rad]
        
            Returns:
                mean angular value
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def modulo(double: float, double2: float) -> float:
        """
            Compute the modulo value
        
            Parameters:
                value (double): input value
                moduloMax (double): maximum value
        
            Returns:
                the modulo value in [0 ; moduloMax[
        
        public static `List <http://docs.oracle.com/javase/8/docs/api/java/util/List.html?is-external=true>`<`Double <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>`> modulo(`List <http://docs.oracle.com/javase/8/docs/api/java/util/List.html?is-external=true>`<`Double <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>`> values, double moduloMax)
        
            Compute the modulo for all elements of a list
        
            Parameters:
                values (`List <http://docs.oracle.com/javase/8/docs/api/java/util/List.html?is-external=true>`<`Double <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>`> values): input list
                moduloMax (double): maximum value
        
            Returns:
                the list of modulo values in [0 ; moduloMax[
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def modulo(list: java.util.List[float], double: float) -> java.util.List[float]: ...
    @staticmethod
    def moduloTwoPi(double: float) -> float:
        """
            Compute the modulo 2PI value
        
            Parameters:
                value (double): input value
        
            Returns:
                the modulo value in [0 ; 2PI[
        
        
        """
        ...
    @staticmethod
    def oppositeAngle(double: float, angleInterval: 'AngleInterval') -> float:
        """
            Computes the opposite of the input angle, and then tries to express it in the input interval.
        
            Parameters:
                angle (double): the angle to get the complementary
                interval (:class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval`): the interval to express the result
        
            Returns:
                double : opposite angle
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the resulting angle is'nt in the interval, modulo 2PI See DV-MATHS_80 .
        
            Since:
                1.0
        
        
        """
        ...
    @staticmethod
    def supplementaryAngle(double: float, angleInterval: 'AngleInterval') -> float:
        """
            Computes the supplementary (PI - angle) of the input angle, and then tries to express it in the input interval.
        
            Parameters:
                angle (double): the angle to get the supplementary
                interval (:class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval`): the interval to express the result
        
            Returns:
                double : supplementary angle
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the resulting angle is'nt in the interval, modulo 2PI See DV-MATHS_80 .
        
            Since:
                1.0
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def unMod(list: java.util.List[float]) -> None: ...
    @typing.overload
    @staticmethod
    def unMod(list: java.util.List[float], double: float) -> None: ...
    @typing.overload
    @staticmethod
    def unMod(list: java.util.List[float], list2: java.util.List[float], double: float, double2: float) -> None: ...

_ComparableIntervalsList__T = typing.TypeVar('_ComparableIntervalsList__T', bound=java.lang.Comparable)  # <T>
class ComparableIntervalsList(java.util.TreeSet['ComparableInterval'[_ComparableIntervalsList__T]], typing.Generic[_ComparableIntervalsList__T]):
    """
    public class ComparableIntervalsList<T extends `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<T>> extends `TreeSet <http://docs.oracle.com/javase/8/docs/api/java/util/TreeSet.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.interval.ComparableInterval`<T>>
    
        This class represents a list of objects :class:`~fr.cnes.sirius.patrius.math.interval.ComparableInterval`.
    
        It extends a TreeSet of :class:`~fr.cnes.sirius.patrius.math.interval.ComparableInterval` instances. Since the objects
        of the list implement the :class:`~fr.cnes.sirius.patrius.math.interval.ComparableInterval` class, the list is an
        ordered collection.
    
        The generic class must implement :code:`java.lang.Comparable`
    
    
        It is HIGHLY recommended this class be immutable!
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.interval.ComparableInterval`, `null
            <http://docs.oracle.com/javase/8/docs/api/java/util/TreeSet.html?is-external=true>`, :meth:`~serialized`
    """
    def __init__(self): ...
    def getInclusiveInterval(self) -> 'ComparableInterval'[_ComparableIntervalsList__T]: ...
    def getIntersectionWith(self, comparableInterval: 'ComparableInterval'[_ComparableIntervalsList__T]) -> 'ComparableIntervalsList'[_ComparableIntervalsList__T]: ...
    def getIntervalsContaining(self, t: _ComparableIntervalsList__T) -> 'ComparableIntervalsList'[_ComparableIntervalsList__T]: ...
    def getMergedIntervals(self) -> 'ComparableIntervalsList'[_ComparableIntervalsList__T]: ...
    def includes(self, comparableInterval: 'ComparableInterval'[_ComparableIntervalsList__T]) -> bool: ...
    def overlaps(self, comparableInterval: 'ComparableInterval'[_ComparableIntervalsList__T]) -> bool: ...

_GenericInterval__T = typing.TypeVar('_GenericInterval__T')  # <T>
class GenericInterval(java.io.Serializable, typing.Generic[_GenericInterval__T]):
    """
    public class GenericInterval<T> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        - Generic class to describe an interval.
    
        - The generic element is the nature of the data defining the upper and lower boundaries.
    
        - This class can be extended ; toString may be overriden.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, intervalEndpointType: 'IntervalEndpointType', t: _GenericInterval__T, t2: _GenericInterval__T, intervalEndpointType2: 'IntervalEndpointType'): ...
    def getLowerData(self) -> _GenericInterval__T:
        """
        
            Returns:
                the lowerData
        
        
        """
        ...
    def getLowerEndpoint(self) -> 'IntervalEndpointType':
        """
        
            Returns:
                the lowerEndpoint
        
        
        """
        ...
    def getUpperData(self) -> _GenericInterval__T:
        """
        
            Returns:
                the upperData
        
        
        """
        ...
    def getUpperEndpoint(self) -> 'IntervalEndpointType':
        """
        
            Returns:
                the upperEndpoint
        
        
        """
        ...
    def toString(self) -> str:
        """
            This method returns a String representing the interval, with boundaries as brackets and the lower/upper values.
        
        
            Example : "] 0.0 , 1.2534 [" for an open interval with doubles.
        
        
            toString is called on the values.
        
        
            Warning : this representation is subject to change.
        
        
            This method may be overriden if convenient.
        
            Overrides:
                 in class 
        
            Returns:
                a String with boundary brackets and values.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#toString-->`
        
        
        """
        ...

class IntervalEndpointType(java.lang.Enum['IntervalEndpointType']):
    """
    public enum IntervalEndpointType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.interval.IntervalEndpointType`>
    
    
        - Describes the type of an interval endpoint : OPENED or CLOSED.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.interval.GenericInterval`
    """
    OPEN: typing.ClassVar['IntervalEndpointType'] = ...
    CLOSED: typing.ClassVar['IntervalEndpointType'] = ...
    def computeHashCode(self) -> int:
        """
            Computes hash code for the instance (13 if the instance is OPEN and 37 if the instance is CLOSED)
        
            Returns:
                the hashcode
        
        
        """
        ...
    def getOpposite(self) -> 'IntervalEndpointType':
        """
            Returns OPEN if the instance is CLOSED and CLOSED if the instance is OPEN.
        
            Returns:
                an :class:`~fr.cnes.sirius.patrius.math.interval.IntervalEndpointType`
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'IntervalEndpointType':
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
    def values() -> typing.MutableSequence['IntervalEndpointType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (IntervalEndpointType c : IntervalEndpointType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class AngleInterval(AbstractInterval, java.io.Serializable):
    """
    public final class AngleInterval extends :class:`~fr.cnes.sirius.patrius.math.interval.AbstractInterval` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        - This class describes an angle interval.
    
        - It contains no method other than getters and setters : the operations on angles are available in the AngleTools class
        See DV-MATHS_50.
    
        Since:
            1.0
    
        Also see:
            :meth:`~serialized`
    """
    ZERO_2PI: typing.ClassVar['AngleInterval'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval` ZERO_2PI
    
        Interval [ 0 ; 2pi [.
    
    """
    MINUS2PI_ZERO: typing.ClassVar['AngleInterval'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval` MINUS2PI_ZERO
    
        Interval ] -2pi ; 0 ].
    
    """
    MINUSPI_PI: typing.ClassVar['AngleInterval'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.interval.AngleInterval` MINUSPI_PI
    
        Interval [ -pi ; pi [.
    
    """
    @typing.overload
    def __init__(self, double: float, double2: float, intervalEndpointType: IntervalEndpointType, intervalEndpointType2: IntervalEndpointType): ...
    @typing.overload
    def __init__(self, intervalEndpointType: IntervalEndpointType, double: float, double2: float, intervalEndpointType2: IntervalEndpointType): ...
    def contains(self, double: float) -> bool:
        """
            Returns true if the angle is contained in this interval, false otherwise. Boundaries OPEN/CLOSED are taken into account.
            No modulo is performed (i.e. -Pi is not included in [0, 2Pi]).
        
            Parameters:
                angle (double): an angle
        
            Returns:
                true if the angle is contained in this interval, false otherwise
        
        
        """
        ...
    def getLength(self) -> float:
        """
        
            Returns:
                the length
        
        
        """
        ...
    def getLowerAngle(self) -> float:
        """
        
            Returns:
                the lowerAngle
        
        
        """
        ...
    def getReference(self) -> float:
        """
        
            Returns:
                the reference
        
        
        """
        ...
    def getUpperAngle(self) -> float:
        """
        
            Returns:
                the upperAngle
        
        
        """
        ...
    def toString(self) -> str:
        """
            This method returns a String representing the interval, with boundaries as brackets and the lower/upper values.
        
        
            Example : "] 0.0 rad , 1.2534 rad [" for an open interval.
        
        
            Warning : this representation is subject to change.
        
            Overrides:
                 in class 
        
            Returns:
                a String representation
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#toString-->`
        
        
        """
        ...

_ComparableInterval__T = typing.TypeVar('_ComparableInterval__T', bound=java.lang.Comparable)  # <T>
class ComparableInterval(GenericInterval[_ComparableInterval__T], java.lang.Comparable['ComparableInterval'[_ComparableInterval__T]], typing.Generic[_ComparableInterval__T]):
    @typing.overload
    def __init__(self, intervalEndpointType: IntervalEndpointType, t: _ComparableInterval__T, t2: _ComparableInterval__T, intervalEndpointType2: IntervalEndpointType): ...
    @typing.overload
    def __init__(self, t: _ComparableInterval__T, t2: _ComparableInterval__T): ...
    def compare(self, comparable: typing.Union[java.lang.Comparable[_ComparableInterval__T], typing.Callable[[_ComparableInterval__T], int]]) -> int: ...
    def compareLowerEndTo(self, comparableInterval: 'ComparableInterval'[_ComparableInterval__T]) -> int: ...
    def compareTo(self, comparableInterval: 'ComparableInterval'[_ComparableInterval__T]) -> int: ...
    def compareUpperEndTo(self, comparableInterval: 'ComparableInterval'[_ComparableInterval__T]) -> int: ...
    def contains(self, comparable: typing.Union[java.lang.Comparable[_ComparableInterval__T], typing.Callable[[_ComparableInterval__T], int]]) -> bool: ...
    def equals(self, object: typing.Any) -> bool: ...
    def extendTo(self, t: _ComparableInterval__T) -> 'ComparableInterval'[_ComparableInterval__T]: ...
    def getIntersectionWith(self, comparableInterval: 'ComparableInterval'[_ComparableInterval__T]) -> 'ComparableInterval'[_ComparableInterval__T]: ...
    def hashCode(self) -> int: ...
    def includes(self, comparableInterval: 'ComparableInterval'[_ComparableInterval__T]) -> bool: ...
    def isConnectedTo(self, comparableInterval: 'ComparableInterval'[_ComparableInterval__T]) -> bool: ...
    def mergeTo(self, comparableInterval: 'ComparableInterval'[_ComparableInterval__T]) -> 'ComparableInterval'[_ComparableInterval__T]: ...
    def overlaps(self, comparableInterval: 'ComparableInterval'[_ComparableInterval__T]) -> bool: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.interval")``.

    AbstractInterval: typing.Type[AbstractInterval]
    AngleInterval: typing.Type[AngleInterval]
    AngleTools: typing.Type[AngleTools]
    ComparableInterval: typing.Type[ComparableInterval]
    ComparableIntervalsList: typing.Type[ComparableIntervalsList]
    GenericInterval: typing.Type[GenericInterval]
    IntervalEndpointType: typing.Type[IntervalEndpointType]
