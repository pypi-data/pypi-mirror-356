
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.complex
import fr.cnes.sirius.patrius.math.dfp
import fr.cnes.sirius.patrius.math.distribution
import fr.cnes.sirius.patrius.math.exception
import fr.cnes.sirius.patrius.math.filter
import fr.cnes.sirius.patrius.math.fitting
import fr.cnes.sirius.patrius.math.fraction
import fr.cnes.sirius.patrius.math.framework
import fr.cnes.sirius.patrius.math.genetics
import fr.cnes.sirius.patrius.math.geometry
import fr.cnes.sirius.patrius.math.interval
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.ode
import fr.cnes.sirius.patrius.math.optim
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.math.random
import fr.cnes.sirius.patrius.math.special
import fr.cnes.sirius.patrius.math.stat
import fr.cnes.sirius.patrius.math.transform
import fr.cnes.sirius.patrius.math.util
import fr.cnes.sirius.patrius.math.utils
import jpype
import typing



class Comparators:
    """
    public final class Comparators extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
    
        - Static comparison methods for real numbers
    
        - Classical methods to compare doubles using an epsilon, as an input or with a default value
        See DV-MATHS_30.
    
        Since:
            1.0
    """
    DOUBLE_COMPARISON_EPSILON: typing.ClassVar[float] = ...
    """
    public static final double DOUBLE_COMPARISON_EPSILON
    
        The epsilon used for doubles relative comparison
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def equals(self, object: typing.Any) -> bool:
        """
            Tests the equality between doubles with a relative comparison using a default epsilon.
        
            Parameters:
                x (double): first double to be compared
                y (double): second double to be compared
        
            Returns:
                a boolean : "true" if the doubles are found equals.
        
                The value "Nan" as input always imply the return "false"
        
            Since:
                1.0
        
            Tests the equality between doubles with a relative comparison using an input epsilon.
        
            Parameters:
                x (double): first double to be compared
                y (double): second double to be compared
                eps (double): epsilon used in the relative comparison
        
            Returns:
                a boolean : "true" if the doubles are found equals.
        
                The value "Nan" as input always imply the return "false"
        
            Since:
                1.0
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def equals(double: float, double2: float) -> bool: ...
    @typing.overload
    @staticmethod
    def equals(double: float, double2: float, double3: float) -> bool: ...
    @staticmethod
    def equalsWithRelativeTolerance(double: float, double2: float, double3: float) -> bool:
        """
            Copied from commons math :meth:`~fr.cnes.sirius.patrius.math.util.Precision.equalsWithRelativeTolerance`. Returns
            :code:`true` if the difference between the number is smaller or equal to the given tolerance. The difference is the call
            to the :meth:`~fr.cnes.sirius.patrius.math.util.Precision.equals`. The ulp is 0 instead of 1. This means that two
            adjacent numbers are not considered equal.
        
            Parameters:
                x (double): First value.
                y (double): Second value.
                eps (double): Amount of allowed relative error.
        
            Returns:
                :code:`true` if the values are two adjacent floating point numbers or they are within range of each other.
        
            Since:
                2.1
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def greaterOrEqual(double: float, double2: float) -> bool:
        """
            Tests if a double is greater or equal to another with a relative comparison using a default epsilon.
        
            Parameters:
                x (double): first double to be compared
                y (double): second double to be compared
        
            Returns:
                a boolean : "true" if x is found greater or equal to y.
        
                The value "Nan" as input always imply the return "false"
        
            Since:
                1.0
        
            Tests if a double is greater or equal to another with a relative comparison using an input epsilon.
        
            Parameters:
                x (double): first double to be compared
                y (double): second double to be compared
                eps (double): epsilon used in the relative comparison
        
            Returns:
                a boolean : "true" if x is found greater or equal to y.
        
                The value "Nan" as input always imply the return "false"
        
            Since:
                1.0
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def greaterOrEqual(double: float, double2: float, double3: float) -> bool: ...
    @typing.overload
    @staticmethod
    def greaterStrict(double: float, double2: float) -> bool:
        """
            Tests if a double is strictly greater than another with a relative comparison using a default epsilon.
        
            Parameters:
                x (double): first double to be compared
                y (double): second double to be compared
        
            Returns:
                a boolean : "true" if x is found greater than y.
        
                The value "Nan" as input always imply the return "false"
        
            Since:
                1.0
        
            Tests if a double is strictly greater than another with a relative comparison using an input epsilon.
        
            Parameters:
                x (double): first double to be compared
                y (double): second double to be compared
                eps (double): epsilon used in the relative comparison
        
            Returns:
                a boolean : "true" if x is found greater than y.
        
                The value "Nan" as input always imply the return "false"
        
            Since:
                1.0
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def greaterStrict(double: float, double2: float, double3: float) -> bool: ...
    @typing.overload
    @staticmethod
    def lowerOrEqual(double: float, double2: float) -> bool:
        """
            Tests if a double is lower or equal to another with a relative comparison using a default epsilon.
        
            Parameters:
                x (double): first double to be compared
                y (double): second double to be compared
        
            Returns:
                a boolean : "true" if x is found lower or equal to y.
        
                The value "Nan" as input always imply the return "false"
        
            Since:
                1.0
        
            Tests if a double is lower or equal to another with a relative comparison using an input epsilon.
        
            Parameters:
                x (double): first double to be compared
                y (double): second double to be compared
                eps (double): epsilon used in the relative comparison
        
            Returns:
                a boolean : "true" if x is found lower or equal to y.
        
                The value "Nan" as input always imply the return "false"
        
            Since:
                1.0
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def lowerOrEqual(double: float, double2: float, double3: float) -> bool: ...
    @typing.overload
    @staticmethod
    def lowerStrict(double: float, double2: float) -> bool:
        """
            Tests if a double is strictly lower than another with a relative comparison using a default epsilon.
        
            Parameters:
                x (double): first double to be compared
                y (double): second double to be compared
        
            Returns:
                a boolean : "true" if x is found lower than y.
        
                The value "Nan" as input always imply the return "false"
        
            Since:
                1.0
        
            Tests if a double is strictly lower than another with a relative comparison using an input epsilon.
        
            Parameters:
                x (double): first double to be compared
                y (double): second double to be compared
                eps (double): epsilon used in the relative comparison
        
            Returns:
                a boolean : "true" if x is found lower than y.
        
                The value "Nan" as input always imply the return "false"
        
            Since:
                1.0
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def lowerStrict(double: float, double2: float, double3: float) -> bool: ...

_Field__T = typing.TypeVar('_Field__T')  # <T>
class Field(typing.Generic[_Field__T]):
    """
    public interface Field<T>
    
        Interface representing a `field <http://mathworld.wolfram.com/Field.html>`.
    
        Classes implementing this interface will often be singletons.
    
        Since:
            2.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.FieldElement`
    """
    def getOne(self) -> _Field__T:
        """
            Get the multiplicative identity of the field.
        
            The multiplicative identity is the element e :sub:`1` of the field such that for all elements a of the field, the
            equalities a × e :sub:`1` = e :sub:`1` × a = a hold.
        
            Returns:
                multiplicative identity of the field
        
        
        """
        ...
    def getRuntimeClass(self) -> typing.Type['FieldElement'[_Field__T]]: ...
    def getZero(self) -> _Field__T:
        """
            Get the additive identity of the field.
        
            The additive identity is the element e :sub:`0` of the field such that for all elements a of the field, the equalities a
            + e :sub:`0` = e :sub:`0` + a = a hold.
        
            Returns:
                additive identity of the field
        
        
        """
        ...

_FieldElement__T = typing.TypeVar('_FieldElement__T')  # <T>
class FieldElement(typing.Generic[_FieldElement__T]):
    """
    public interface FieldElement<T>
    
        Interface representing `field <http://mathworld.wolfram.com/Field.html>` elements.
    
        Since:
            2.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.Field`
    """
    def add(self, t: _FieldElement__T) -> _FieldElement__T:
        """
            Compute this + a.
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.FieldElement`): element to add
        
            Returns:
                a new element representing this + a
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`addend` is :code:`null`.
        
        
        """
        ...
    def divide(self, t: _FieldElement__T) -> _FieldElement__T:
        """
            Compute this ÷ a.
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.FieldElement`): element to add
        
            Returns:
                a new element representing this ÷ a
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`a` is :code:`null`.
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if :code:`a` is zero
        
        
        """
        ...
    def getField(self) -> Field[_FieldElement__T]: ...
    @typing.overload
    def multiply(self, int: int) -> _FieldElement__T:
        """
            Compute n × this. Multiplication by an integer number is defined as the following sum
            n × this = ∑ :sub:`i=1` :sup:`n` this.
        
            Parameters:
                n (int): Number of times :code:`this` must be added to itself.
        
            Returns:
                A new element representing n × this.
        
            Compute this × a.
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.FieldElement`): element to multiply
        
            Returns:
                a new element representing this × a
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`a` is :code:`null`.
        
        
        """
        ...
    @typing.overload
    def multiply(self, t: _FieldElement__T) -> _FieldElement__T: ...
    def negate(self) -> _FieldElement__T:
        """
            Returns the additive inverse of :code:`this` element.
        
            Returns:
                the opposite of :code:`this`.
        
        
        """
        ...
    def reciprocal(self) -> _FieldElement__T:
        """
            Returns the multiplicative inverse of :code:`this` element.
        
            Returns:
                the inverse of :code:`this`.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if :code:`this` is zero
        
        
        """
        ...
    def subtract(self, t: _FieldElement__T) -> _FieldElement__T:
        """
            Compute this - a.
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.FieldElement`): element to subtract
        
            Returns:
                a new element representing this - a
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`a` is :code:`null`.
        
        
        """
        ...

_RealFieldElement__T = typing.TypeVar('_RealFieldElement__T')  # <T>
class RealFieldElement(FieldElement[_RealFieldElement__T], typing.Generic[_RealFieldElement__T]):
    def abs(self) -> _RealFieldElement__T: ...
    def acos(self) -> _RealFieldElement__T: ...
    def acosh(self) -> _RealFieldElement__T: ...
    @typing.overload
    def add(self, t: _RealFieldElement__T) -> _RealFieldElement__T: ...
    @typing.overload
    def add(self, double: float) -> _RealFieldElement__T: ...
    def asin(self) -> _RealFieldElement__T: ...
    def asinh(self) -> _RealFieldElement__T: ...
    def atan(self) -> _RealFieldElement__T: ...
    def atan2(self, t: _RealFieldElement__T) -> _RealFieldElement__T: ...
    def atanh(self) -> _RealFieldElement__T: ...
    def cbrt(self) -> _RealFieldElement__T: ...
    def ceil(self) -> _RealFieldElement__T: ...
    @typing.overload
    def copySign(self, double: float) -> _RealFieldElement__T: ...
    @typing.overload
    def copySign(self, t: _RealFieldElement__T) -> _RealFieldElement__T: ...
    def cos(self) -> _RealFieldElement__T: ...
    def cosh(self) -> _RealFieldElement__T: ...
    @typing.overload
    def divide(self, t: _RealFieldElement__T) -> _RealFieldElement__T: ...
    @typing.overload
    def divide(self, double: float) -> _RealFieldElement__T: ...
    def exp(self) -> _RealFieldElement__T: ...
    def expm1(self) -> _RealFieldElement__T: ...
    def floor(self) -> _RealFieldElement__T: ...
    def getReal(self) -> float: ...
    def hypot(self, t: _RealFieldElement__T) -> _RealFieldElement__T: ...
    @typing.overload
    def linearCombination(self, double: float, t: _RealFieldElement__T, double2: float, t2: _RealFieldElement__T) -> _RealFieldElement__T: ...
    @typing.overload
    def linearCombination(self, double: float, t: _RealFieldElement__T, double2: float, t2: _RealFieldElement__T, double3: float, t3: _RealFieldElement__T) -> _RealFieldElement__T: ...
    @typing.overload
    def linearCombination(self, double: float, t: _RealFieldElement__T, double2: float, t2: _RealFieldElement__T, double3: float, t3: _RealFieldElement__T, double4: float, t4: _RealFieldElement__T) -> _RealFieldElement__T: ...
    @typing.overload
    def linearCombination(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], tArray: typing.Union[typing.List[_RealFieldElement__T], jpype.JArray]) -> _RealFieldElement__T: ...
    @typing.overload
    def linearCombination(self, t: _RealFieldElement__T, t2: _RealFieldElement__T, t3: _RealFieldElement__T, t4: _RealFieldElement__T) -> _RealFieldElement__T: ...
    @typing.overload
    def linearCombination(self, t: _RealFieldElement__T, t2: _RealFieldElement__T, t3: _RealFieldElement__T, t4: _RealFieldElement__T, t5: _RealFieldElement__T, t6: _RealFieldElement__T) -> _RealFieldElement__T: ...
    @typing.overload
    def linearCombination(self, t: _RealFieldElement__T, t2: _RealFieldElement__T, t3: _RealFieldElement__T, t4: _RealFieldElement__T, t5: _RealFieldElement__T, t6: _RealFieldElement__T, t7: _RealFieldElement__T, t8: _RealFieldElement__T) -> _RealFieldElement__T: ...
    @typing.overload
    def linearCombination(self, tArray: typing.Union[typing.List[_RealFieldElement__T], jpype.JArray], tArray2: typing.Union[typing.List[_RealFieldElement__T], jpype.JArray]) -> _RealFieldElement__T: ...
    def log(self) -> _RealFieldElement__T: ...
    def log1p(self) -> _RealFieldElement__T: ...
    @typing.overload
    def multiply(self, int: int) -> _RealFieldElement__T: ...
    @typing.overload
    def multiply(self, t: _RealFieldElement__T) -> _RealFieldElement__T: ...
    @typing.overload
    def multiply(self, double: float) -> _RealFieldElement__T: ...
    @typing.overload
    def pow(self, double: float) -> _RealFieldElement__T: ...
    @typing.overload
    def pow(self, int: int) -> _RealFieldElement__T: ...
    @typing.overload
    def pow(self, t: _RealFieldElement__T) -> _RealFieldElement__T: ...
    def reciprocal(self) -> _RealFieldElement__T: ...
    @typing.overload
    def remainder(self, double: float) -> _RealFieldElement__T: ...
    @typing.overload
    def remainder(self, t: _RealFieldElement__T) -> _RealFieldElement__T: ...
    def rint(self) -> _RealFieldElement__T: ...
    def rootN(self, int: int) -> _RealFieldElement__T: ...
    def round(self) -> int: ...
    def scalb(self, int: int) -> _RealFieldElement__T: ...
    def signum(self) -> _RealFieldElement__T: ...
    def sin(self) -> _RealFieldElement__T: ...
    def sinh(self) -> _RealFieldElement__T: ...
    def sqrt(self) -> _RealFieldElement__T: ...
    @typing.overload
    def subtract(self, t: _RealFieldElement__T) -> _RealFieldElement__T: ...
    @typing.overload
    def subtract(self, double: float) -> _RealFieldElement__T: ...
    def tan(self) -> _RealFieldElement__T: ...
    def tanh(self) -> _RealFieldElement__T: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math")``.

    Comparators: typing.Type[Comparators]
    Field: typing.Type[Field]
    FieldElement: typing.Type[FieldElement]
    RealFieldElement: typing.Type[RealFieldElement]
    analysis: fr.cnes.sirius.patrius.math.analysis.__module_protocol__
    complex: fr.cnes.sirius.patrius.math.complex.__module_protocol__
    dfp: fr.cnes.sirius.patrius.math.dfp.__module_protocol__
    distribution: fr.cnes.sirius.patrius.math.distribution.__module_protocol__
    exception: fr.cnes.sirius.patrius.math.exception.__module_protocol__
    filter: fr.cnes.sirius.patrius.math.filter.__module_protocol__
    fitting: fr.cnes.sirius.patrius.math.fitting.__module_protocol__
    fraction: fr.cnes.sirius.patrius.math.fraction.__module_protocol__
    framework: fr.cnes.sirius.patrius.math.framework.__module_protocol__
    genetics: fr.cnes.sirius.patrius.math.genetics.__module_protocol__
    geometry: fr.cnes.sirius.patrius.math.geometry.__module_protocol__
    interval: fr.cnes.sirius.patrius.math.interval.__module_protocol__
    linear: fr.cnes.sirius.patrius.math.linear.__module_protocol__
    ode: fr.cnes.sirius.patrius.math.ode.__module_protocol__
    optim: fr.cnes.sirius.patrius.math.optim.__module_protocol__
    parameter: fr.cnes.sirius.patrius.math.parameter.__module_protocol__
    random: fr.cnes.sirius.patrius.math.random.__module_protocol__
    special: fr.cnes.sirius.patrius.math.special.__module_protocol__
    stat: fr.cnes.sirius.patrius.math.stat.__module_protocol__
    transform: fr.cnes.sirius.patrius.math.transform.__module_protocol__
    util: fr.cnes.sirius.patrius.math.util.__module_protocol__
    utils: fr.cnes.sirius.patrius.math.utils.__module_protocol__
