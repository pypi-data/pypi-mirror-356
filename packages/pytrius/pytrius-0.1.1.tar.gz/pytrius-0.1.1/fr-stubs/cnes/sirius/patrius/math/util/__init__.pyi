
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import decimal
import fr.cnes.sirius.patrius.math
import fr.cnes.sirius.patrius.math.exception.util
import fr.cnes.sirius.patrius.math.framework
import java.io
import java.lang
import java.math
import java.text
import java.util
import jpype
import typing



class ArithmeticUtils:
    @typing.overload
    @staticmethod
    def addAndCheck(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def addAndCheck(long: int, long2: int) -> int: ...
    @staticmethod
    def binomialCoefficient(int: int, int2: int) -> int: ...
    @staticmethod
    def binomialCoefficientDouble(int: int, int2: int) -> float: ...
    @staticmethod
    def binomialCoefficientLog(int: int, int2: int) -> float: ...
    _binomialCombinations__T = typing.TypeVar('_binomialCombinations__T')  # <T>
    @staticmethod
    def binomialCombinations(list: java.util.List[_binomialCombinations__T], int: int) -> java.util.List[java.util.List[_binomialCombinations__T]]: ...
    @staticmethod
    def factorial(int: int) -> int: ...
    @staticmethod
    def factorialDouble(int: int) -> float: ...
    @staticmethod
    def factorialLog(int: int) -> float: ...
    @typing.overload
    @staticmethod
    def gcd(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def gcd(long: int, long2: int) -> int: ...
    @staticmethod
    def isPowerOfTwo(long: int) -> bool: ...
    @typing.overload
    @staticmethod
    def lcm(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def lcm(long: int, long2: int) -> int: ...
    @typing.overload
    @staticmethod
    def mulAndCheck(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def mulAndCheck(long: int, long2: int) -> int: ...
    @typing.overload
    @staticmethod
    def pow(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def pow(int: int, long: int) -> int: ...
    @typing.overload
    @staticmethod
    def pow(bigInteger: java.math.BigInteger, int: int) -> java.math.BigInteger: ...
    @typing.overload
    @staticmethod
    def pow(bigInteger: java.math.BigInteger, bigInteger2: java.math.BigInteger) -> java.math.BigInteger: ...
    @typing.overload
    @staticmethod
    def pow(bigInteger: java.math.BigInteger, long: int) -> java.math.BigInteger: ...
    @typing.overload
    @staticmethod
    def pow(long: int, int: int) -> int: ...
    @typing.overload
    @staticmethod
    def pow(long: int, long2: int) -> int: ...
    @staticmethod
    def stirlingS2(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def subAndCheck(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def subAndCheck(long: int, long2: int) -> int: ...

class BigReal(fr.cnes.sirius.patrius.math.FieldElement['BigReal'], java.lang.Comparable['BigReal'], java.io.Serializable):
    """
    public class BigReal extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.FieldElement`<:class:`~fr.cnes.sirius.patrius.math.util.BigReal`>, `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.util.BigReal`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Arbitrary precision decimal number.
    
        This class is a simple wrapper around the standard :code:`BigDecimal` in order to implement the
        :class:`~fr.cnes.sirius.patrius.math.FieldElement` interface.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    ZERO: typing.ClassVar['BigReal'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.util.BigReal` ZERO
    
        A big real representing 0.
    
    """
    ONE: typing.ClassVar['BigReal'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.util.BigReal` ONE
    
        A big real representing 1.
    
    """
    @typing.overload
    def __init__(self, charArray: typing.Union[typing.List[str], jpype.JArray]): ...
    @typing.overload
    def __init__(self, charArray: typing.Union[typing.List[str], jpype.JArray], int: int, int2: int): ...
    @typing.overload
    def __init__(self, charArray: typing.Union[typing.List[str], jpype.JArray], int: int, int2: int, mathContext: java.math.MathContext): ...
    @typing.overload
    def __init__(self, charArray: typing.Union[typing.List[str], jpype.JArray], mathContext: java.math.MathContext): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, mathContext: java.math.MathContext): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, mathContext: java.math.MathContext): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, string: str, mathContext: java.math.MathContext): ...
    @typing.overload
    def __init__(self, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]): ...
    @typing.overload
    def __init__(self, bigInteger: java.math.BigInteger): ...
    @typing.overload
    def __init__(self, bigInteger: java.math.BigInteger, int: int): ...
    @typing.overload
    def __init__(self, bigInteger: java.math.BigInteger, int: int, mathContext: java.math.MathContext): ...
    @typing.overload
    def __init__(self, bigInteger: java.math.BigInteger, mathContext: java.math.MathContext): ...
    @typing.overload
    def __init__(self, long: int): ...
    @typing.overload
    def __init__(self, long: int, mathContext: java.math.MathContext): ...
    def add(self, bigReal: 'BigReal') -> 'BigReal':
        """
            Compute this + a.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.add` in interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.util.BigReal`): element to add
        
            Returns:
                a new element representing this + a
        
        
        """
        ...
    def bigDecimalValue(self) -> java.math.BigDecimal:
        """
            Get the BigDecimal value corresponding to the instance.
        
            Returns:
                BigDecimal value corresponding to the instance
        
        
        """
        ...
    def compareTo(self, bigReal: 'BigReal') -> int:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    def divide(self, bigReal: 'BigReal') -> 'BigReal':
        """
            Compute this ÷ a.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.divide` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.util.BigReal`): element to add
        
            Returns:
                a new element representing this ÷ a
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if :code:`a` is zero
        
        
        """
        ...
    def doubleValue(self) -> float:
        """
            Get the double value corresponding to the instance.
        
            Returns:
                double value corresponding to the instance
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getField(self) -> fr.cnes.sirius.patrius.math.Field['BigReal']: ...
    def getRoundingMode(self) -> java.math.RoundingMode:
        """
            Gets the rounding mode for division operations The default is :code:`RoundingMode.HALF_UP`
        
            Returns:
                the rounding mode.
        
            Since:
                2.1
        
        
        """
        ...
    def getScale(self) -> int:
        """
            Sets the scale for division operations. The default is 64
        
            Returns:
                the scale
        
            Since:
                2.1
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @typing.overload
    def multiply(self, bigReal: 'BigReal') -> 'BigReal':
        """
            Compute this × a.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.multiply` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.util.BigReal`): element to multiply
        
            Returns:
                a new element representing this × a
        
            Compute n × this. Multiplication by an integer number is defined as the following sum
            n × this = ∑ :sub:`i=1` :sup:`n` this.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.multiply` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                n (int): Number of times :code:`this` must be added to itself.
        
            Returns:
                A new element representing n × this.
        
        
        """
        ...
    @typing.overload
    def multiply(self, int: int) -> 'BigReal': ...
    def negate(self) -> 'BigReal':
        """
            Returns the additive inverse of :code:`this` element.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.negate` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Returns:
                the opposite of :code:`this`.
        
        
        """
        ...
    def reciprocal(self) -> 'BigReal':
        """
            Returns the multiplicative inverse of :code:`this` element.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.reciprocal` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Returns:
                the inverse of :code:`this`.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if :code:`this` is zero
        
        
        """
        ...
    def setRoundingMode(self, roundingMode: java.math.RoundingMode) -> None:
        """
            Sets the rounding mode for decimal divisions.
        
            Parameters:
                roundingModeIn (`RoundingMode <http://docs.oracle.com/javase/8/docs/api/java/math/RoundingMode.html?is-external=true>`): rounding mode for decimal divisions
        
            Since:
                2.1
        
        
        """
        ...
    def setScale(self, int: int) -> None:
        """
            Sets the scale for division operations.
        
            Parameters:
                scaleIn (int): scale for division operations
        
            Since:
                2.1
        
        
        """
        ...
    def subtract(self, bigReal: 'BigReal') -> 'BigReal':
        """
            Compute this - a.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.subtract` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.util.BigReal`): element to subtract
        
            Returns:
                a new element representing this - a
        
        
        """
        ...

class BigRealField(fr.cnes.sirius.patrius.math.Field[BigReal], java.io.Serializable):
    """
    public final class BigRealField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.Field`<:class:`~fr.cnes.sirius.patrius.math.util.BigReal`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Representation of real numbers with arbitrary precision field.
    
        This class is a singleton.
    
        Since:
            2.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.util.BigReal`, :meth:`~serialized`
    """
    @staticmethod
    def getInstance() -> 'BigRealField':
        """
            Get the unique instance.
        
            Returns:
                the unique instance
        
        
        """
        ...
    def getOne(self) -> BigReal:
        """
            Get the multiplicative identity of the field.
        
            The multiplicative identity is the element e :sub:`1` of the field such that for all elements a of the field, the
            equalities a × e :sub:`1` = e :sub:`1` × a = a hold.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.Field.getOne` in interface :class:`~fr.cnes.sirius.patrius.math.Field`
        
            Returns:
                multiplicative identity of the field
        
        
        """
        ...
    def getRuntimeClass(self) -> typing.Type[fr.cnes.sirius.patrius.math.FieldElement[BigReal]]: ...
    def getZero(self) -> BigReal:
        """
            Get the additive identity of the field.
        
            The additive identity is the element e :sub:`0` of the field such that for all elements a of the field, the equalities a
            + e :sub:`0` = e :sub:`0` + a = a hold.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.Field.getZero` in interface :class:`~fr.cnes.sirius.patrius.math.Field`
        
            Returns:
                additive identity of the field
        
        
        """
        ...

class Combinations(java.lang.Iterable[typing.MutableSequence[int]]):
    def __init__(self, int: int, int2: int): ...
    def comparator(self) -> java.util.Comparator[typing.MutableSequence[int]]: ...
    def getK(self) -> int: ...
    def getN(self) -> int: ...
    def iterator(self) -> java.util.Iterator[typing.MutableSequence[int]]: ...

class CombinatoricsUtils:
    @staticmethod
    def binomialCoefficient(int: int, int2: int) -> int: ...
    @staticmethod
    def binomialCoefficientDouble(int: int, int2: int) -> float: ...
    @staticmethod
    def binomialCoefficientLog(int: int, int2: int) -> float: ...
    @staticmethod
    def checkBinomial(int: int, int2: int) -> None: ...
    @staticmethod
    def factorial(int: int) -> int: ...
    @staticmethod
    def factorialDouble(int: int) -> float: ...
    @staticmethod
    def factorialLog(int: int) -> float: ...

class CompositeFormat:
    """
    public final class CompositeFormat extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Base class for formatters of composite objects (complex numbers, vectors ...).
    """
    @staticmethod
    def formatDouble(double: float, numberFormat: java.text.NumberFormat, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer:
        """
            Formats a double value to produce a string. In general, the value is formatted using the formatting rules of
            :code:`format`.
        
        
            There are three exceptions to this:
        
              1.  NaN is formatted as '(NaN)'
              2.  Positive infinity is formatted as '(Infinity)'
              3.  Negative infinity is formatted as '(-Infinity)'
        
        
            Parameters:
                value (double): the double to format
                format (`NumberFormat <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>`): the format used
                toAppendTo (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): where the text is to be appended
                pos (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
        
            Returns:
                the value passed in as toAppendTo
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getDefaultNumberFormat() -> java.text.NumberFormat:
        """
            Create a default number format. The default number format is based on `null
            <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true#getInstance-->` with the only
            customizing that the maximum number of fraction digits is set to 10.
        
            Returns:
                the default number format
        
        """
        ...
    @typing.overload
    @staticmethod
    def getDefaultNumberFormat(locale: java.util.Locale) -> java.text.NumberFormat:
        """
            Create a default number format. The default number format is based on `null
            <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true#getInstance-java.util.Locale->`
            with the only customizing that the maximum number of fraction digits is set to 10.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): the specific locale used by the format
        
            Returns:
                the default number format specific to the given locale
        
        """
        ...
    @typing.overload
    @staticmethod
    def getDefaultNumberFormat(locale: java.util.Locale, int: int) -> java.text.NumberFormat:
        """
            Create a default number format. The default number format is based on `null
            <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true#getInstance-java.util.Locale->`.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): the specific locale used by the format
                maximumFractionDigits (int): the maximum number of fraction digits to be shown; if less than zero, then zero is used.
        
            Returns:
                the default number format specific to the given locale
        
        
        """
        ...
    @staticmethod
    def parseAndIgnoreWhitespace(string: str, parsePosition: java.text.ParsePosition) -> None:
        """
            Parses :code:`source` until a non-whitespace character is found.
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
                pos (`ParsePosition <http://docs.oracle.com/javase/8/docs/api/java/text/ParsePosition.html?is-external=true>`): input/output parsing parameter. On output, :code:`pos` holds the index of the next non-whitespace character.
        
        
        """
        ...
    @staticmethod
    def parseFixedstring(string: str, string2: str, parsePosition: java.text.ParsePosition) -> bool:
        """
            Parse :code:`source` for an expected fixed string.
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
                expected (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): expected string
                pos (`ParsePosition <http://docs.oracle.com/javase/8/docs/api/java/text/ParsePosition.html?is-external=true>`): input/output parsing parameter
        
            Returns:
                true if the expected string was there
        
        
        """
        ...
    @staticmethod
    def parseNextCharacter(string: str, parsePosition: java.text.ParsePosition) -> str:
        """
            Parses :code:`source` until a non-whitespace character is found.
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
                pos (`ParsePosition <http://docs.oracle.com/javase/8/docs/api/java/text/ParsePosition.html?is-external=true>`): input/output parsing parameter
        
            Returns:
                the first non-whitespace character
        
        
        """
        ...
    @staticmethod
    def parseNumber(string: str, numberFormat: java.text.NumberFormat, parsePosition: java.text.ParsePosition) -> java.lang.Number:
        """
            Parses :code:`source` for a number. This method can parse normal, numeric values as well as special values. These
            special values include `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NaN>`,
            `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#POSITIVE_INFINITY>`, `null
            <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NEGATIVE_INFINITY>`.
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
                format (`NumberFormat <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>`): the number format used to parse normal, numeric values
                pos (`ParsePosition <http://docs.oracle.com/javase/8/docs/api/java/text/ParsePosition.html?is-external=true>`): input/output parsing parameter
        
            Returns:
                the parsed number
        
        
        """
        ...

class ContinuedFraction:
    """
    public abstract class ContinuedFraction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Provides a generic means to evaluate continued fractions. Subclasses simply provided the a and b coefficients to
        evaluate the continued fraction.
    
        References:
    
          - ` Continued Fraction <http://mathworld.wolfram.com/ContinuedFraction.html>`
    """
    @typing.overload
    def evaluate(self, double: float) -> float:
        """
            Evaluates the continued fraction at the value x.
        
            Parameters:
                x (double): the evaluation point.
        
            Returns:
                the value of the continued fraction evaluated at x.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.ConvergenceException`: if the algorithm fails to converge.
        
            Evaluates the continued fraction at the value x.
        
            Parameters:
                x (double): the evaluation point.
                epsilon (double): maximum error allowed.
        
            Returns:
                the value of the continued fraction evaluated at x.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.ConvergenceException`: if the algorithm fails to converge.
        
            Evaluates the continued fraction at the value x.
        
            Parameters:
                x (double): the evaluation point.
                maxIterations (int): maximum number of convergents
        
            Returns:
                the value of the continued fraction evaluated at x.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.ConvergenceException`: if the algorithm fails to converge.
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if maximal number of iterations is reached
        
            Evaluates the continued fraction at the value x.
        
            The implementation of this method is based on the modified Lentz algorithm as described on page 18 ff. in:
        
              - I. J. Thompson, A. R. Barnett. "Coulomb and Bessel Functions of Complex Arguments and Order." `
                http://www.fresco.org.uk/papers/Thompson-JCP64p490.pdf <http://www.fresco.org.uk/papers/Thompson-JCP64p490.pdf>`
        
            **Note:** the implementation uses the terms a :sub:`i` and b :sub:`i` as defined in `Continued Fraction @ MathWorld
            <http://mathworld.wolfram.com/ContinuedFraction.html>`.
        
            Parameters:
                x (double): the evaluation point.
                epsilon (double): maximum error allowed.
                maxIterations (int): maximum number of convergents
        
            Returns:
                the value of the continued fraction evaluated at x.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.ConvergenceException`: if the algorithm fails to converge.
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if maximal number of iterations is reached
        
        
        """
        ...
    @typing.overload
    def evaluate(self, double: float, double2: float) -> float: ...
    @typing.overload
    def evaluate(self, double: float, double2: float, int: int) -> float: ...
    @typing.overload
    def evaluate(self, double: float, int: int) -> float: ...

class Decimal64(java.lang.Number, fr.cnes.sirius.patrius.math.FieldElement['Decimal64'], java.lang.Comparable['Decimal64']):
    """
    public class Decimal64 extends `Number <http://docs.oracle.com/javase/8/docs/api/java/lang/Number.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.FieldElement`<:class:`~fr.cnes.sirius.patrius.math.util.Decimal64`>, `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.util.Decimal64`>
    
        This class wraps a :code:`double` value in an object. It is similar to the standard class `null
        <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>`, while also implementing the
        :class:`~fr.cnes.sirius.patrius.math.FieldElement` interface.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    ZERO: typing.ClassVar['Decimal64'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.util.Decimal64` ZERO
    
        The constant value of :code:`0d` as a :code:`Decimal64`.
    
    """
    ONE: typing.ClassVar['Decimal64'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.util.Decimal64` ONE
    
        The constant value of :code:`1d` as a :code:`Decimal64`.
    
    """
    NEGATIVE_INFINITY: typing.ClassVar['Decimal64'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.util.Decimal64` NEGATIVE_INFINITY
    
        The constant value of `null
        <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NEGATIVE_INFINITY>` as a
        :code:`Decimal64`.
    
    """
    POSITIVE_INFINITY: typing.ClassVar['Decimal64'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.util.Decimal64` POSITIVE_INFINITY
    
        The constant value of `null
        <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#POSITIVE_INFINITY>` as a
        :code:`Decimal64`.
    
    """
    NAN: typing.ClassVar['Decimal64'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.util.Decimal64` NAN
    
        The constant value of `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NaN>` as a
        :code:`Decimal64`.
    
    """
    def __init__(self, double: float): ...
    def add(self, decimal64: 'Decimal64') -> 'Decimal64':
        """
            Compute this + a. The current implementation strictly enforces :code:`this.add(a).equals(new
            Decimal64(this.doubleValue() + a.doubleValue()))`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.add` in interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.util.Decimal64`): element to add
        
            Returns:
                a new element representing this + a
        
        
        """
        ...
    def byteValue(self) -> int:
        """
            The current implementation performs casting to a :code:`byte`.
        
            Overrides:
                 in class 
        
        
        """
        ...
    def compareTo(self, decimal64: 'Decimal64') -> int:
        """
            The current implementation returns the same value as
            :code:`new Double(this.doubleValue()).compareTo(new Double(o.doubleValue()))`
        
            Specified by:
                 in interface 
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#compareTo-java.lang.Double->`
        
        
        """
        ...
    def divide(self, decimal64: 'Decimal64') -> 'Decimal64':
        """
            Compute this ÷ a. The current implementation strictly enforces :code:`this.divide(a).equals(new
            Decimal64(this.doubleValue() / a.doubleValue()))`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.divide` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.util.Decimal64`): element to add
        
            Returns:
                a new element representing this ÷ a
        
        
        """
        ...
    def doubleValue(self) -> float:
        """
        
            Specified by:
                 in class 
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def floatValue(self) -> float:
        """
            The current implementation performs casting to a :code:`float`.
        
            Specified by:
                 in class 
        
        
        """
        ...
    def getField(self) -> fr.cnes.sirius.patrius.math.Field['Decimal64']: ...
    def hashCode(self) -> int:
        """
            The current implementation returns the same value as :code:`new Double(this.doubleValue()).hashCode()`
        
            Overrides:
                 in class 
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#hashCode-->`
        
        
        """
        ...
    def intValue(self) -> int:
        """
            The current implementation performs casting to a :code:`int`.
        
            Specified by:
                 in class 
        
        
        """
        ...
    def isInfinite(self) -> bool:
        """
            Returns :code:`true` if :code:`this` double precision number is infinite (`null
            <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#POSITIVE_INFINITY>` or `null
            <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NEGATIVE_INFINITY>`).
        
            Returns:
                :code:`true` if :code:`this` number is infinite
        
        
        """
        ...
    def isNaN(self) -> bool:
        """
            Returns :code:`true` if :code:`this` double precision number is Not-a-Number (:code:`NaN`), false otherwise.
        
            Returns:
                :code:`true` if :code:`this` is :code:`NaN`
        
        
        """
        ...
    def longValue(self) -> int:
        """
            The current implementation performs casting to a :code:`long`.
        
            Specified by:
                 in class 
        
        
        """
        ...
    @typing.overload
    def multiply(self, decimal64: 'Decimal64') -> 'Decimal64':
        """
            Compute this × a. The current implementation strictly enforces :code:`this.multiply(a).equals(new
            Decimal64(this.doubleValue() * a.doubleValue()))`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.multiply` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.util.Decimal64`): element to multiply
        
            Returns:
                a new element representing this × a
        
            Compute n × this. Multiplication by an integer number is defined as the following sum
            n × this = ∑ :sub:`i=1` :sup:`n` this.
            The current implementation strictly enforces :code:`this.multiply(n).equals(new Decimal64(n * this.doubleValue()))`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.multiply` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                n (int): Number of times :code:`this` must be added to itself.
        
            Returns:
                A new element representing n × this.
        
        
        """
        ...
    @typing.overload
    def multiply(self, int: int) -> 'Decimal64': ...
    def negate(self) -> 'Decimal64':
        """
            Returns the additive inverse of :code:`this` element. The current implementation strictly enforces
            :code:`this.negate().equals(new Decimal64(-this.doubleValue()))`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.negate` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Returns:
                the opposite of :code:`this`.
        
        
        """
        ...
    def reciprocal(self) -> 'Decimal64':
        """
            Returns the multiplicative inverse of :code:`this` element. The current implementation strictly enforces
            :code:`this.reciprocal().equals(new Decimal64(1.0 / this.doubleValue()))`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.reciprocal` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Returns:
                the inverse of :code:`this`.
        
        
        """
        ...
    def subtract(self, decimal64: 'Decimal64') -> 'Decimal64':
        """
            Compute this - a. The current implementation strictly enforces :code:`this.subtract(a).equals(new
            Decimal64(this.doubleValue() - a.doubleValue()))`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.subtract` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.util.Decimal64`): element to subtract
        
            Returns:
                a new element representing this - a
        
        
        """
        ...
    def toString(self) -> str:
        """
            The returned :code:`String` is equal to :code:`Double.toString(this.doubleValue())`
        
            Overrides:
                 in class 
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#toString-double->`
        
        
        """
        ...

class Decimal64Field(fr.cnes.sirius.patrius.math.Field[Decimal64]):
    """
    public final class Decimal64Field extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.Field`<:class:`~fr.cnes.sirius.patrius.math.util.Decimal64`>
    
        The field of double precision floating-point numbers.
    
        Since:
            3.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.util.Decimal64`
    """
    @staticmethod
    def getInstance() -> 'Decimal64Field':
        """
            Returns the unique instance of this class.
        
            Returns:
                the unique instance of this class
        
        
        """
        ...
    def getOne(self) -> Decimal64:
        """
            Get the multiplicative identity of the field.
        
            The multiplicative identity is the element e :sub:`1` of the field such that for all elements a of the field, the
            equalities a × e :sub:`1` = e :sub:`1` × a = a hold.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.Field.getOne` in interface :class:`~fr.cnes.sirius.patrius.math.Field`
        
            Returns:
                multiplicative identity of the field
        
        
        """
        ...
    def getRuntimeClass(self) -> typing.Type[fr.cnes.sirius.patrius.math.FieldElement[Decimal64]]: ...
    def getZero(self) -> Decimal64:
        """
            Get the additive identity of the field.
        
            The additive identity is the element e :sub:`0` of the field such that for all elements a of the field, the equalities a
            + e :sub:`0` = e :sub:`0` + a = a hold.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.Field.getZero` in interface :class:`~fr.cnes.sirius.patrius.math.Field`
        
            Returns:
                additive identity of the field
        
        
        """
        ...

class DoubleArray:
    """
    public interface DoubleArray
    
        Provides a standard interface for double arrays. Allows different array implementations to support various storage
        mechanisms such as automatic expansion, contraction, and array "rolling".
    """
    def addElement(self, double: float) -> None:
        """
            Adds an element to the end of this expandable array
        
            Parameters:
                value (double): to be added to end of array
        
        
        """
        ...
    def addElementRolling(self, double: float) -> float:
        """
        
            Adds an element to the end of the array and removes the first element in the array. Returns the discarded first element.
            The effect is similar to a push operation in a FIFO queue.
        
            Example: If the array contains the elements 1, 2, 3, 4 (in that order) and addElementRolling(5) is invoked, the result
            is an array containing the entries 2, 3, 4, 5 and the value returned is 1.
        
            Parameters:
                value (double): the value to be added to the array
        
            Returns:
                the value which has been discarded or "pushed" out of the array by this rolling insert
        
        
        """
        ...
    def addElements(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Adds elements to the end of this expandable array
        
            Parameters:
                values (double[]): to be added to end of array
        
        
        """
        ...
    def clear(self) -> None:
        """
            Clear the double array
        
        """
        ...
    def getElement(self, int: int) -> float:
        """
            Returns the element at the specified index. Note that if an out of bounds index is supplied a
            ArrayIndexOutOfBoundsException will be thrown.
        
            Parameters:
                index (int): index to fetch a value from
        
            Returns:
                value stored at the specified index
        
            Raises:
                : if :code:`index` is less than zero or is greater than :code:`getNumElements() - 1`.
        
        
        """
        ...
    def getElements(self) -> typing.MutableSequence[float]:
        """
            Returns a double[] array containing the elements of this :code:`DoubleArray`. If the underlying implementation is
            array-based, this method should always return a copy, rather than a reference to the underlying array so that changes
            made to the returned array have no effect on the :code:`DoubleArray.`
        
            Returns:
                all elements added to the array
        
        
        """
        ...
    def getNumElements(self) -> int:
        """
            Returns the number of elements currently in the array. Please note that this may be different from the length of the
            internal storage array.
        
            Returns:
                number of elements
        
        
        """
        ...
    def setElement(self, int: int, double: float) -> None:
        """
            Sets the element at the specified index. If the specified index is greater than :code:`getNumElements() - 1` , the
            :code:`numElements` property is increased to :code:`index +1` and additional storage is allocated (if necessary) for the
            new element and all (uninitialized) elements between the new element and the previous end of the array).
        
            Parameters:
                index (int): index to store a value in
                value (double): value to store at the specified index
        
            Raises:
                : if :code:`index` is less than zero.
        
        
        """
        ...

class FastMath:
    PI: typing.ClassVar[float] = ...
    E: typing.ClassVar[float] = ...
    @staticmethod
    def IEEEremainder(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def abs(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def abs(float: float) -> float: ...
    @typing.overload
    @staticmethod
    def abs(int: int) -> int: ...
    @typing.overload
    @staticmethod
    def abs(long: int) -> int: ...
    @staticmethod
    def acos(double: float) -> float: ...
    @staticmethod
    def acosh(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def addExact(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def addExact(long: int, long2: int) -> int: ...
    @staticmethod
    def asin(double: float) -> float: ...
    @staticmethod
    def asinh(double: float) -> float: ...
    @staticmethod
    def atan(double: float) -> float: ...
    @staticmethod
    def atan2(double: float, double2: float) -> float: ...
    @staticmethod
    def atanh(double: float) -> float: ...
    @staticmethod
    def cbrt(double: float) -> float: ...
    @staticmethod
    def ceil(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def copySign(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def copySign(float: float, float2: float) -> float: ...
    @staticmethod
    def cos(double: float) -> float: ...
    @staticmethod
    def cosh(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def decrementExact(int: int) -> int: ...
    @typing.overload
    @staticmethod
    def decrementExact(long: int) -> int: ...
    @staticmethod
    def exp(double: float) -> float: ...
    @staticmethod
    def expm1(double: float) -> float: ...
    @staticmethod
    def floor(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def floorDiv(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def floorDiv(long: int, long2: int) -> int: ...
    @typing.overload
    @staticmethod
    def floorMod(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def floorMod(long: int, long2: int) -> int: ...
    @typing.overload
    @staticmethod
    def getExponent(double: float) -> int: ...
    @typing.overload
    @staticmethod
    def getExponent(float: float) -> int: ...
    @staticmethod
    def hypot(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def incrementExact(int: int) -> int: ...
    @typing.overload
    @staticmethod
    def incrementExact(long: int) -> int: ...
    @typing.overload
    @staticmethod
    def log(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def log(double: float, double2: float) -> float: ...
    @staticmethod
    def log10(double: float) -> float: ...
    @staticmethod
    def log1p(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def max(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def max(float: float, float2: float) -> float: ...
    @typing.overload
    @staticmethod
    def max(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def max(long: int, long2: int) -> int: ...
    @typing.overload
    @staticmethod
    def min(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def min(float: float, float2: float) -> float: ...
    @typing.overload
    @staticmethod
    def min(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def min(long: int, long2: int) -> int: ...
    @typing.overload
    @staticmethod
    def multiplyExact(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def multiplyExact(long: int, long2: int) -> int: ...
    @typing.overload
    @staticmethod
    def nextAfter(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def nextAfter(float: float, double: float) -> float: ...
    @typing.overload
    @staticmethod
    def nextDown(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def nextDown(float: float) -> float: ...
    @typing.overload
    @staticmethod
    def nextUp(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def nextUp(float: float) -> float: ...
    @typing.overload
    @staticmethod
    def pow(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def pow(double: float, int: int) -> float: ...
    @typing.overload
    @staticmethod
    def pow(double: float, long: int) -> float: ...
    @staticmethod
    def random() -> float: ...
    @staticmethod
    def rint(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def round(float: float) -> int: ...
    @typing.overload
    @staticmethod
    def round(double: float) -> int: ...
    @typing.overload
    @staticmethod
    def scalb(double: float, int: int) -> float: ...
    @typing.overload
    @staticmethod
    def scalb(float: float, int: int) -> float: ...
    @typing.overload
    @staticmethod
    def signum(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def signum(float: float) -> float: ...
    @staticmethod
    def sin(double: float) -> float: ...
    @staticmethod
    def sinh(double: float) -> float: ...
    @staticmethod
    def sqrt(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def subtractExact(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def subtractExact(long: int, long2: int) -> int: ...
    @staticmethod
    def tan(double: float) -> float: ...
    @staticmethod
    def tanh(double: float) -> float: ...
    @staticmethod
    def toDegrees(double: float) -> float: ...
    @staticmethod
    def toIntExact(long: int) -> int: ...
    @staticmethod
    def toRadians(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def ulp(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def ulp(float: float) -> float: ...

class Incrementor(java.io.Serializable):
    """
    public class Incrementor extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Utility that increments a counter until a maximum is reached, at which point, the instance will by default throw a
        :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`. However, the user is able to override this
        behaviour by defining a custom :class:`~fr.cnes.sirius.patrius.math.util.Incrementor.MaxCountExceededCallback`, in order
        to e.g. select which exception must be thrown.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, maxCountExceededCallback: typing.Union['Incrementor.MaxCountExceededCallback', typing.Callable]): ...
    def canIncrement(self) -> bool:
        """
            Checks whether a single increment is allowed.
        
            Returns:
                :code:`false` if the next call to :meth:`~fr.cnes.sirius.patrius.math.util.Incrementor.incrementCount` will trigger a
                :code:`MaxCountExceededException`, :code:`true` otherwise.
        
        
        """
        ...
    def getCount(self) -> int:
        """
            Gets the current count.
        
            Returns:
                the current count.
        
        
        """
        ...
    def getMaximalCount(self) -> int:
        """
            Gets the upper limit of the counter.
        
            Returns:
                the counter upper limit.
        
        
        """
        ...
    @typing.overload
    def incrementCount(self) -> None:
        """
            Adds one to the current iteration count. At counter exhaustion, this method will call the
            :meth:`~fr.cnes.sirius.patrius.math.util.Incrementor.MaxCountExceededCallback.trigger` method of the callback object
            passed to the :meth:`~fr.cnes.sirius.patrius.math.util.Incrementor.Incrementor`. If not explictly set, a default
            callback is used that will throw a :code:`MaxCountExceededException`.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: at counter exhaustion, unless a custom :class:`~fr.cnes.sirius.patrius.math.util.Incrementor.MaxCountExceededCallback`
                    has been set at construction.
        
        
        """
        ...
    @typing.overload
    def incrementCount(self, int: int) -> None:
        """
            Performs multiple increments. See the other :meth:`~fr.cnes.sirius.patrius.math.util.Incrementor.incrementCount`
            method).
        
            Parameters:
                value (int): Number of increments.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: at counter exhaustion.
        
        """
        ...
    def resetCount(self) -> None:
        """
            Resets the counter to 0.
        
        """
        ...
    def setMaximalCount(self, int: int) -> None:
        """
            Sets the upper limit for the counter. This does not automatically reset the current count to zero (see
            :meth:`~fr.cnes.sirius.patrius.math.util.Incrementor.resetCount`).
        
            Parameters:
                max (int): Upper limit of the counter.
        
        
        """
        ...
    class MaxCountExceededCallback(java.io.Serializable):
        def trigger(self, int: int) -> None: ...

class IterationEvent(java.util.EventObject):
    """
    public class IterationEvent extends `EventObject <http://docs.oracle.com/javase/8/docs/api/java/util/EventObject.html?is-external=true>`
    
        The root class from which all events occurring while running an
        :class:`~fr.cnes.sirius.patrius.math.util.IterationManager` should be derived.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, object: typing.Any, int: int): ...
    def getIterations(self) -> int:
        """
            Returns the number of iterations performed at the time :code:`this` event is created.
        
            Returns:
                the number of iterations performed
        
        
        """
        ...

class IterationListener(java.util.EventListener):
    """
    public interface IterationListener extends `EventListener <http://docs.oracle.com/javase/8/docs/api/java/util/EventListener.html?is-external=true>`
    
        The listener interface for receiving events occurring in an iterative algorithm.
    """
    def initializationPerformed(self, iterationEvent: IterationEvent) -> None:
        """
            Invoked after completion of the initial phase of the iterative algorithm (prior to the main iteration loop).
        
            Parameters:
                e (:class:`~fr.cnes.sirius.patrius.math.util.IterationEvent`): The :class:`~fr.cnes.sirius.patrius.math.util.IterationEvent` object.
        
        
        """
        ...
    def iterationPerformed(self, iterationEvent: IterationEvent) -> None:
        """
            Invoked each time an iteration is completed (in the main iteration loop).
        
            Parameters:
                e (:class:`~fr.cnes.sirius.patrius.math.util.IterationEvent`): The :class:`~fr.cnes.sirius.patrius.math.util.IterationEvent` object.
        
        
        """
        ...
    def iterationStarted(self, iterationEvent: IterationEvent) -> None:
        """
            Invoked each time a new iteration is completed (in the main iteration loop).
        
            Parameters:
                e (:class:`~fr.cnes.sirius.patrius.math.util.IterationEvent`): The :class:`~fr.cnes.sirius.patrius.math.util.IterationEvent` object.
        
        
        """
        ...
    def terminationPerformed(self, iterationEvent: IterationEvent) -> None:
        """
            Invoked after completion of the operations which occur after breaking out of the main iteration loop.
        
            Parameters:
                e (:class:`~fr.cnes.sirius.patrius.math.util.IterationEvent`): The :class:`~fr.cnes.sirius.patrius.math.util.IterationEvent` object.
        
        
        """
        ...

class IterationManager:
    """
    public class IterationManager extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This abstract class provides a general framework for managing iterative algorithms. The maximum number of iterations can
        be set, and methods are provided to monitor the current iteration count. A lightweight event framework is also provided.
    """
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, maxCountExceededCallback: typing.Union[Incrementor.MaxCountExceededCallback, typing.Callable]): ...
    def addIterationListener(self, iterationListener: IterationListener) -> None:
        """
            Attaches a listener to this manager.
        
            Parameters:
                listener (:class:`~fr.cnes.sirius.patrius.math.util.IterationListener`): A :code:`IterationListener` object.
        
        
        """
        ...
    def fireInitializationEvent(self, iterationEvent: IterationEvent) -> None:
        """
            Informs all registered listeners that the initial phase (prior to the main iteration loop) has been completed.
        
            Parameters:
                e (:class:`~fr.cnes.sirius.patrius.math.util.IterationEvent`): The :class:`~fr.cnes.sirius.patrius.math.util.IterationEvent` object.
        
        
        """
        ...
    def fireIterationPerformedEvent(self, iterationEvent: IterationEvent) -> None:
        """
            Informs all registered listeners that a new iteration (in the main iteration loop) has been performed.
        
            Parameters:
                e (:class:`~fr.cnes.sirius.patrius.math.util.IterationEvent`): The :class:`~fr.cnes.sirius.patrius.math.util.IterationEvent` object.
        
        
        """
        ...
    def fireIterationStartedEvent(self, iterationEvent: IterationEvent) -> None:
        """
            Informs all registered listeners that a new iteration (in the main iteration loop) has been started.
        
            Parameters:
                e (:class:`~fr.cnes.sirius.patrius.math.util.IterationEvent`): The :class:`~fr.cnes.sirius.patrius.math.util.IterationEvent` object.
        
        
        """
        ...
    def fireTerminationEvent(self, iterationEvent: IterationEvent) -> None:
        """
            Informs all registered listeners that the final phase (post-iterations) has been completed.
        
            Parameters:
                e (:class:`~fr.cnes.sirius.patrius.math.util.IterationEvent`): The :class:`~fr.cnes.sirius.patrius.math.util.IterationEvent` object.
        
        
        """
        ...
    def getIterations(self) -> int:
        """
            Returns the number of iterations of this solver, 0 if no iterations has been performed yet.
        
            Returns:
                the number of iterations.
        
        
        """
        ...
    def getMaxIterations(self) -> int:
        """
            Returns the maximum number of iterations.
        
            Returns:
                the maximum number of iterations.
        
        
        """
        ...
    def incrementIterationCount(self) -> None:
        """
            Increments the iteration count by one, and throws an exception if the maximum number of iterations is reached. This
            method should be called at the beginning of a new iteration.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the maximum number of iterations is reached.
        
        
        """
        ...
    def removeIterationListener(self, iterationListener: IterationListener) -> None:
        """
            Removes the specified iteration listener from the list of listeners currently attached to :code:`this` object.
            Attempting to remove a listener which was *not* previously registered does not cause any error.
        
            Parameters:
                listener (:class:`~fr.cnes.sirius.patrius.math.util.IterationListener`): The :class:`~fr.cnes.sirius.patrius.math.util.IterationListener` to be removed.
        
        
        """
        ...
    def resetIterationCount(self) -> None:
        """
            Sets the iteration count to 0. This method must be called during the initial phase.
        
        """
        ...

class MathArrays:
    _buildArray_0__T = typing.TypeVar('_buildArray_0__T')  # <T>
    _buildArray_1__T = typing.TypeVar('_buildArray_1__T')  # <T>
    @typing.overload
    @staticmethod
    def buildArray(field: fr.cnes.sirius.patrius.math.Field[_buildArray_0__T], int: int) -> typing.MutableSequence[_buildArray_0__T]: ...
    @typing.overload
    @staticmethod
    def buildArray(field: fr.cnes.sirius.patrius.math.Field[_buildArray_1__T], int: int, int2: int) -> typing.MutableSequence[typing.MutableSequence[_buildArray_1__T]]: ...
    @typing.overload
    @staticmethod
    def checkNonNegative(longArray: typing.Union[typing.List[int], jpype.JArray]) -> None: ...
    @typing.overload
    @staticmethod
    def checkNonNegative(longArray: typing.Union[typing.List[typing.MutableSequence[int]], jpype.JArray]) -> None: ...
    @typing.overload
    @staticmethod
    def checkOrder(doubleArray: typing.Union[typing.List[float], jpype.JArray], orderDirection: 'MathArrays.OrderDirection', boolean: bool, boolean2: bool) -> bool: ...
    @typing.overload
    @staticmethod
    def checkOrder(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    @staticmethod
    def checkOrder(doubleArray: typing.Union[typing.List[float], jpype.JArray], orderDirection: 'MathArrays.OrderDirection', boolean: bool) -> None: ...
    @staticmethod
    def checkPositive(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @staticmethod
    def checkRectangular(longArray: typing.Union[typing.List[typing.MutableSequence[int]], jpype.JArray]) -> None: ...
    @typing.overload
    @staticmethod
    def copyOf(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    @staticmethod
    def copyOf(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int) -> typing.MutableSequence[float]: ...
    @typing.overload
    @staticmethod
    def copyOf(intArray: typing.Union[typing.List[int], jpype.JArray]) -> typing.MutableSequence[int]: ...
    @typing.overload
    @staticmethod
    def copyOf(intArray: typing.Union[typing.List[int], jpype.JArray], int2: int) -> typing.MutableSequence[int]: ...
    @typing.overload
    @staticmethod
    def distance(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def distance(intArray: typing.Union[typing.List[int], jpype.JArray], intArray2: typing.Union[typing.List[int], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def distance1(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def distance1(intArray: typing.Union[typing.List[int], jpype.JArray], intArray2: typing.Union[typing.List[int], jpype.JArray]) -> int: ...
    @typing.overload
    @staticmethod
    def distanceInf(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def distanceInf(intArray: typing.Union[typing.List[int], jpype.JArray], intArray2: typing.Union[typing.List[int], jpype.JArray]) -> int: ...
    @staticmethod
    def ebeAdd(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @staticmethod
    def ebeDivide(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @staticmethod
    def ebeMultiply(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @staticmethod
    def ebeSubtract(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def equals(self, object: typing.Any) -> bool: ...
    @typing.overload
    @staticmethod
    def equals(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> bool: ...
    @typing.overload
    @staticmethod
    def equals(floatArray: typing.Union[typing.List[float], jpype.JArray], floatArray2: typing.Union[typing.List[float], jpype.JArray]) -> bool: ...
    @typing.overload
    @staticmethod
    def equalsIncludingNaN(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> bool: ...
    @typing.overload
    @staticmethod
    def equalsIncludingNaN(floatArray: typing.Union[typing.List[float], jpype.JArray], floatArray2: typing.Union[typing.List[float], jpype.JArray]) -> bool: ...
    _isMonotonic_1__T = typing.TypeVar('_isMonotonic_1__T', bound=java.lang.Comparable)  # <T>
    @typing.overload
    @staticmethod
    def isMonotonic(doubleArray: typing.Union[typing.List[float], jpype.JArray], orderDirection: 'MathArrays.OrderDirection', boolean: bool) -> bool: ...
    @typing.overload
    @staticmethod
    def isMonotonic(tArray: typing.Union[typing.List[_isMonotonic_1__T], jpype.JArray], orderDirection: 'MathArrays.OrderDirection', boolean: bool) -> bool: ...
    @typing.overload
    @staticmethod
    def linearCombination(double: float, double2: float, double3: float, double4: float) -> float: ...
    @typing.overload
    @staticmethod
    def linearCombination(double: float, double2: float, double3: float, double4: float, double5: float, double6: float) -> float: ...
    @typing.overload
    @staticmethod
    def linearCombination(double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float) -> float: ...
    @typing.overload
    @staticmethod
    def linearCombination(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @staticmethod
    def natural(int: int) -> typing.MutableSequence[int]: ...
    @staticmethod
    def normalizeArray(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> typing.MutableSequence[float]: ...
    @staticmethod
    def preciseSum(*double: float) -> float: ...
    @staticmethod
    def safeNorm(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @staticmethod
    def sequence(int: int, int2: int, int3: int) -> typing.MutableSequence[int]: ...
    @typing.overload
    @staticmethod
    def sortInPlace(doubleArray: typing.Union[typing.List[float], jpype.JArray], *doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    @staticmethod
    def sortInPlace(doubleArray: typing.Union[typing.List[float], jpype.JArray], orderDirection: 'MathArrays.OrderDirection', *doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    class Function:
        @typing.overload
        def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
        @typing.overload
        def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    class OrderDirection(java.lang.Enum['MathArrays.OrderDirection']):
        INCREASING: typing.ClassVar['MathArrays.OrderDirection'] = ...
        DECREASING: typing.ClassVar['MathArrays.OrderDirection'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'MathArrays.OrderDirection': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['MathArrays.OrderDirection']: ...

class MathLib:
    PI: typing.ClassVar[float] = ...
    E: typing.ClassVar[float] = ...
    @staticmethod
    def IEEEremainder(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def abs(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def abs(float: float) -> float: ...
    @typing.overload
    @staticmethod
    def abs(int: int) -> int: ...
    @typing.overload
    @staticmethod
    def abs(long: int) -> int: ...
    @staticmethod
    def acos(double: float) -> float: ...
    @staticmethod
    def acosh(double: float) -> float: ...
    @staticmethod
    def asin(double: float) -> float: ...
    @staticmethod
    def asinh(double: float) -> float: ...
    @staticmethod
    def atan(double: float) -> float: ...
    @staticmethod
    def atan2(double: float, double2: float) -> float: ...
    @staticmethod
    def atanh(double: float) -> float: ...
    @staticmethod
    def cbrt(double: float) -> float: ...
    @staticmethod
    def ceil(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def copySign(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def copySign(float: float, float2: float) -> float: ...
    @staticmethod
    def cos(double: float) -> float: ...
    @staticmethod
    def cosh(double: float) -> float: ...
    @staticmethod
    def divide(double: float, double2: float) -> float: ...
    @staticmethod
    def exp(double: float) -> float: ...
    @staticmethod
    def expm1(double: float) -> float: ...
    @staticmethod
    def floor(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def getExponent(double: float) -> int: ...
    @typing.overload
    @staticmethod
    def getExponent(float: float) -> int: ...
    @staticmethod
    def hypot(double: float, double2: float) -> float: ...
    @staticmethod
    def log(double: float) -> float: ...
    @staticmethod
    def log10(double: float) -> float: ...
    @staticmethod
    def log1p(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def max(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def max(float: float, float2: float) -> float: ...
    @typing.overload
    @staticmethod
    def max(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def max(long: int, long2: int) -> int: ...
    @typing.overload
    @staticmethod
    def min(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def min(float: float, float2: float) -> float: ...
    @typing.overload
    @staticmethod
    def min(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def min(long: int, long2: int) -> int: ...
    @typing.overload
    @staticmethod
    def nextAfter(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def nextAfter(float: float, double: float) -> float: ...
    @typing.overload
    @staticmethod
    def nextUp(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def nextUp(float: float) -> float: ...
    @typing.overload
    @staticmethod
    def pow(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def pow(double: float, int: int) -> float: ...
    @staticmethod
    def random() -> float: ...
    @staticmethod
    def rint(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def round(float: float) -> int: ...
    @typing.overload
    @staticmethod
    def round(double: float) -> int: ...
    @typing.overload
    @staticmethod
    def scalb(double: float, int: int) -> float: ...
    @typing.overload
    @staticmethod
    def scalb(float: float, int: int) -> float: ...
    @typing.overload
    @staticmethod
    def setMathLibrary(mathLibrary: fr.cnes.sirius.patrius.math.framework.MathLibrary) -> None: ...
    @typing.overload
    @staticmethod
    def setMathLibrary(mathLibraryType: fr.cnes.sirius.patrius.math.framework.MathLibraryType) -> None: ...
    @typing.overload
    @staticmethod
    def signum(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def signum(float: float) -> float: ...
    @staticmethod
    def sin(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def sinAndCos(double: float) -> typing.MutableSequence[float]: ...
    @typing.overload
    @staticmethod
    def sinAndCos(double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @staticmethod
    def sinh(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def sinhAndCosh(double: float) -> typing.MutableSequence[float]: ...
    @typing.overload
    @staticmethod
    def sinhAndCosh(double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @staticmethod
    def sqrt(double: float) -> float: ...
    @staticmethod
    def tan(double: float) -> float: ...
    @staticmethod
    def tanh(double: float) -> float: ...
    @staticmethod
    def toDegrees(double: float) -> float: ...
    @staticmethod
    def toRadians(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def ulp(double: float) -> float: ...
    @typing.overload
    @staticmethod
    def ulp(float: float) -> float: ...

class MathUtils:
    TWO_PI: typing.ClassVar[float] = ...
    HALF_PI: typing.ClassVar[float] = ...
    HALF_CIRCLE: typing.ClassVar[float] = ...
    DEG_TO_RAD: typing.ClassVar[float] = ...
    RAD_TO_DEG: typing.ClassVar[float] = ...
    @typing.overload
    @staticmethod
    def checkFinite(double: float) -> None: ...
    @typing.overload
    @staticmethod
    def checkFinite(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    @staticmethod
    def checkNotNull(object: typing.Any) -> None: ...
    @typing.overload
    @staticmethod
    def checkNotNull(object: typing.Any, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object2: typing.Any) -> None: ...
    @staticmethod
    def containsNaN(*double: float) -> bool: ...
    @typing.overload
    @staticmethod
    def copySign(byte: int, byte2: int) -> int: ...
    @typing.overload
    @staticmethod
    def copySign(int: int, int2: int) -> int: ...
    @typing.overload
    @staticmethod
    def copySign(long: int, long2: int) -> int: ...
    @staticmethod
    def findSmallestOffset(double: float, double2: float, double3: float) -> float: ...
    @typing.overload
    @staticmethod
    def hash(double: float) -> int: ...
    @typing.overload
    @staticmethod
    def hash(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> int: ...
    @staticmethod
    def normalizeAngle(double: float, double2: float) -> float: ...
    @staticmethod
    def reduce(double: float, double2: float, double3: float) -> float: ...
    @staticmethod
    def solveQuadraticEquation(double: float, double2: float, double3: float) -> typing.MutableSequence[float]: ...
    @staticmethod
    def solveQuadraticEquationMaxRoot(double: float, double2: float, double3: float) -> float: ...
    @staticmethod
    def solveQuadraticEquationMinRoot(double: float, double2: float, double3: float) -> float: ...

class MultidimensionalCounter(java.lang.Iterable[int]):
    """
    public class MultidimensionalCounter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Iterable <http://docs.oracle.com/javase/8/docs/api/java/lang/Iterable.html?is-external=true>`<`Integer <http://docs.oracle.com/javase/8/docs/api/java/lang/Integer.html?is-external=true>`>
    
        Converter between unidimensional storage structure and multidimensional conceptual structure. This utility will convert
        from indices in a multidimensional structure to the corresponding index in a one-dimensional array. For example,
        assuming that the ranges (in 3 dimensions) of indices are 2, 4 and 3, the following correspondences, between 3-tuples
        indices and unidimensional indices, will hold:
    
          - (0, 0, 0) corresponds to 0
          - (0, 0, 1) corresponds to 1
          - (0, 0, 2) corresponds to 2
          - (0, 1, 0) corresponds to 3
          - ...
          - (1, 0, 0) corresponds to 12
          - ...
          - (1, 3, 2) corresponds to 23
    
    
        Since:
            2.2
    """
    def __init__(self, *int: int): ...
    def getCount(self, *int: int) -> int:
        """
            Convert to unidimensional counter.
        
            Parameters:
                c (int...): Indices in multidimensional counter.
        
            Returns:
                the index within the unidimensionl counter.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the size of :code:`c` does not match the size of the array given in the constructor.
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if a value of :code:`c` is not in the range of the corresponding dimension, as defined in the
                    :meth:`~fr.cnes.sirius.patrius.math.util.MultidimensionalCounter.MultidimensionalCounter`.
        
        
        """
        ...
    def getCounts(self, int: int) -> typing.MutableSequence[int]:
        """
            Convert to multidimensional counter.
        
            Parameters:
                index (int): Index in unidimensional counter.
        
            Returns:
                the multidimensional counts.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if :code:`index` is not between :code:`0` and the value returned by
                    :meth:`~fr.cnes.sirius.patrius.math.util.MultidimensionalCounter.getSize` (excluded).
        
        
        """
        ...
    def getDimension(self) -> int:
        """
            Get the number of dimensions of the multidimensional counter.
        
            Returns:
                the number of dimensions.
        
        
        """
        ...
    def getSize(self) -> int:
        """
            Get the total number of elements.
        
            Returns:
                the total size of the unidimensional counter.
        
        
        """
        ...
    def getSizes(self) -> typing.MutableSequence[int]:
        """
            Get the number of multidimensional counter slots in each dimension.
        
            Returns:
                the sizes of the multidimensional counter in each dimension.
        
        
        """
        ...
    def iterator(self) -> 'MultidimensionalCounter.Iterator':
        """
            Create an iterator over this counter.
        
            Specified by:
                 in interface 
        
            Returns:
                the iterator.
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    class Iterator(java.util.Iterator[int]):
        @typing.overload
        def getCount(self) -> int: ...
        @typing.overload
        def getCount(self, int: int) -> int: ...
        def getCounts(self) -> typing.MutableSequence[int]: ...
        def hasNext(self) -> bool: ...
        def next(self) -> int: ...
        def remove(self) -> None: ...

class NumberTransformer:
    """
    public interface NumberTransformer
    
        Subclasses implementing this interface can transform Objects to doubles.
    """
    def transform(self, object: typing.Any) -> float:
        """
            Implementing this interface provides a facility to transform from Object to Double.
        
            Parameters:
                o (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the Object to be transformed.
        
            Returns:
                the double value of the Object.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the Object can not be transformed into a Double.
        
        
        """
        ...

class OpenIntToDoubleHashMap(java.io.Serializable):
    """
    public class OpenIntToDoubleHashMap extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Open addressed map from int to double.
    
        This class provides a dedicated map from integers to doubles with a much smaller memory overhead than standard
        :code:`java.util.Map`.
    
        This class is not synchronized. The specialized iterators returned by
        :meth:`~fr.cnes.sirius.patrius.math.util.OpenIntToDoubleHashMap.iterator` are fail-fast: they throw a
        :code:`ConcurrentModificationException` when they detect the map has been modified during iteration.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, openIntToDoubleHashMap: 'OpenIntToDoubleHashMap'): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, double: float): ...
    def containsKey(self, int: int) -> bool:
        """
            Check if a value is associated with a key.
        
            Parameters:
                key (int): key to check
        
            Returns:
                true if a value is associated with key
        
        
        """
        ...
    def get(self, int: int) -> float:
        """
            Get the stored value associated with the given key
        
            Parameters:
                key (int): key associated with the data
        
            Returns:
                data associated with the key
        
        
        """
        ...
    def iterator(self) -> 'OpenIntToDoubleHashMap.Iterator':
        """
            Get an iterator over map elements.
        
            The specialized iterators returned are fail-fast: they throw a :code:`ConcurrentModificationException` when they detect
            the map has been modified during iteration.
        
            Returns:
                iterator over the map elements
        
        
        """
        ...
    def put(self, int: int, double: float) -> float:
        """
            Put a value associated with a key in the map.
        
            Parameters:
                key (int): key to which value is associated
                value (double): value to put in the map
        
            Returns:
                previous value associated with the key
        
        
        """
        ...
    def remove(self, int: int) -> float:
        """
            Remove the value associated with a key.
        
            Parameters:
                key (int): key to which the value is associated
        
            Returns:
                removed value
        
        
        """
        ...
    def size(self) -> int:
        """
            Get the number of elements stored in the map.
        
            Returns:
                number of elements stored in the map
        
        
        """
        ...
    class Iterator:
        def advance(self) -> None: ...
        def hasNext(self) -> bool: ...
        def key(self) -> int: ...
        def value(self) -> float: ...

_OpenIntToFieldHashMap__T = typing.TypeVar('_OpenIntToFieldHashMap__T', bound=fr.cnes.sirius.patrius.math.FieldElement)  # <T>
class OpenIntToFieldHashMap(java.io.Serializable, typing.Generic[_OpenIntToFieldHashMap__T]):
    """
    public class OpenIntToFieldHashMap<T extends :class:`~fr.cnes.sirius.patrius.math.FieldElement`<T>> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Open addressed map from int to FieldElement.
    
        This class provides a dedicated map from integers to FieldElements with a much smaller memory overhead than standard
        :code:`java.util.Map`.
    
        This class is not synchronized. The specialized iterators returned by
        :meth:`~fr.cnes.sirius.patrius.math.util.OpenIntToFieldHashMap.iterator` are fail-fast: they throw a
        :code:`ConcurrentModificationException` when they detect the map has been modified during iteration.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, field: fr.cnes.sirius.patrius.math.Field[_OpenIntToFieldHashMap__T]): ...
    @typing.overload
    def __init__(self, field: fr.cnes.sirius.patrius.math.Field[_OpenIntToFieldHashMap__T], t: _OpenIntToFieldHashMap__T): ...
    @typing.overload
    def __init__(self, field: fr.cnes.sirius.patrius.math.Field[_OpenIntToFieldHashMap__T], int: int): ...
    @typing.overload
    def __init__(self, field: fr.cnes.sirius.patrius.math.Field[_OpenIntToFieldHashMap__T], int: int, t: _OpenIntToFieldHashMap__T): ...
    @typing.overload
    def __init__(self, openIntToFieldHashMap: 'OpenIntToFieldHashMap'[_OpenIntToFieldHashMap__T]): ...
    def containsKey(self, int: int) -> bool:
        """
            Check if a value is associated with a key.
        
            Parameters:
                key (int): key to check
        
            Returns:
                true if a value is associated with key
        
        
        """
        ...
    def get(self, int: int) -> _OpenIntToFieldHashMap__T:
        """
            Get the stored value associated with the given key
        
            Parameters:
                key (int): key associated with the data
        
            Returns:
                data associated with the key
        
        
        """
        ...
    def iterator(self) -> 'OpenIntToFieldHashMap.Iterator':
        """
            Get an iterator over map elements.
        
            The specialized iterators returned are fail-fast: they throw a :code:`ConcurrentModificationException` when they detect
            the map has been modified during iteration.
        
            Returns:
                iterator over the map elements
        
        
        """
        ...
    def put(self, int: int, t: _OpenIntToFieldHashMap__T) -> _OpenIntToFieldHashMap__T:
        """
            Put a value associated with a key in the map.
        
            Parameters:
                key (int): key to which value is associated
                value (:class:`~fr.cnes.sirius.patrius.math.util.OpenIntToFieldHashMap`): value to put in the map
        
            Returns:
                previous value associated with the key
        
        
        """
        ...
    def remove(self, int: int) -> _OpenIntToFieldHashMap__T:
        """
            Remove the value associated with a key.
        
            Parameters:
                key (int): key to which the value is associated
        
            Returns:
                removed value
        
        
        """
        ...
    def size(self) -> int:
        """
            Get the number of elements stored in the map.
        
            Returns:
                number of elements stored in the map
        
        
        """
        ...
    class Iterator:
        def advance(self) -> None: ...
        def hasNext(self) -> bool: ...
        def key(self) -> int: ...
        def value(self) -> _OpenIntToFieldHashMap__T: ...

_Pair__K = typing.TypeVar('_Pair__K')  # <K>
_Pair__V = typing.TypeVar('_Pair__V')  # <V>
class Pair(java.io.Serializable, typing.Generic[_Pair__K, _Pair__V]):
    @typing.overload
    def __init__(self, pair: 'Pair'[_Pair__K, _Pair__V]): ...
    @typing.overload
    def __init__(self, k: _Pair__K, v: _Pair__V): ...
    def equals(self, object: typing.Any) -> bool: ...
    def getFirst(self) -> _Pair__K: ...
    def getKey(self) -> _Pair__K: ...
    def getSecond(self) -> _Pair__V: ...
    def getValue(self) -> _Pair__V: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...

class Precision:
    EPSILON: typing.ClassVar[float] = ...
    DOUBLE_COMPARISON_EPSILON: typing.ClassVar[float] = ...
    SAFE_MIN: typing.ClassVar[float] = ...
    @typing.overload
    @staticmethod
    def compareTo(double: float, double2: float, double3: float) -> int: ...
    @typing.overload
    @staticmethod
    def compareTo(double: float, double2: float, int: int) -> int: ...
    @typing.overload
    def equals(self, object: typing.Any) -> bool: ...
    @typing.overload
    @staticmethod
    def equals(double: float, double2: float) -> bool: ...
    @typing.overload
    @staticmethod
    def equals(double: float, double2: float, double3: float) -> bool: ...
    @typing.overload
    @staticmethod
    def equals(double: float, double2: float, int: int) -> bool: ...
    @typing.overload
    @staticmethod
    def equals(float: float, float2: float) -> bool: ...
    @typing.overload
    @staticmethod
    def equals(float: float, float2: float, float3: float) -> bool: ...
    @typing.overload
    @staticmethod
    def equals(float: float, float2: float, int: int) -> bool: ...
    @typing.overload
    @staticmethod
    def equalsIncludingNaN(double: float, double2: float) -> bool: ...
    @typing.overload
    @staticmethod
    def equalsIncludingNaN(double: float, double2: float, double3: float) -> bool: ...
    @typing.overload
    @staticmethod
    def equalsIncludingNaN(double: float, double2: float, int: int) -> bool: ...
    @typing.overload
    @staticmethod
    def equalsIncludingNaN(float: float, float2: float) -> bool: ...
    @typing.overload
    @staticmethod
    def equalsIncludingNaN(float: float, float2: float, float3: float) -> bool: ...
    @typing.overload
    @staticmethod
    def equalsIncludingNaN(float: float, float2: float, int: int) -> bool: ...
    @staticmethod
    def equalsWithAbsoluteAndRelativeTolerances(double: float, double2: float, double3: float, double4: float) -> bool: ...
    @staticmethod
    def equalsWithAbsoluteOrRelativeTolerances(double: float, double2: float, double3: float, double4: float) -> bool: ...
    @typing.overload
    @staticmethod
    def equalsWithRelativeTolerance(double: float, double2: float) -> bool: ...
    @typing.overload
    @staticmethod
    def equalsWithRelativeTolerance(double: float, double2: float, double3: float) -> bool: ...
    @staticmethod
    def representableDelta(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def round(double: float, int: int) -> float: ...
    @typing.overload
    @staticmethod
    def round(double: float, int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def round(float: float, int: int) -> float: ...
    @typing.overload
    @staticmethod
    def round(float: float, int: int, int2: int) -> float: ...
    @staticmethod
    def twoProductError(double: float, double2: float, double3: float) -> float: ...
    @staticmethod
    def twoSumError(double: float, double2: float, double3: float) -> float: ...

class DefaultTransformer(NumberTransformer, java.io.Serializable):
    """
    public class DefaultTransformer extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.util.NumberTransformer`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        A Default NumberTransformer for java.lang.Numbers and Numeric Strings. This provides some simple conversion capabilities
        to turn any java.lang.Number into a primitive double or to turn a String representation of a Number into a double.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def transform(self, object: typing.Any) -> float:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.math.util.NumberTransformer.transform`
            Implementing this interface provides a facility to transform from Object to Double.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.util.NumberTransformer.transform` in
                interface :class:`~fr.cnes.sirius.patrius.math.util.NumberTransformer`
        
            Parameters:
                o (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the object that gets transformed.
        
            Returns:
                a double primitive representation of the Object o.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if Object :code:`o` is :code:`null`.
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if Object :code:`o` cannot successfully be transformed
        
            Also see:
                `Commons Collections Transformer <http://commons.apache.org/collections/api-release/org/apache/
                commons/collections/Transformer.html>`
        
        
        """
        ...

class ResizableDoubleArray(DoubleArray, java.io.Serializable):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, resizableDoubleArray: 'ResizableDoubleArray'): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, double: float): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, expansionMode: 'ResizableDoubleArray.ExpansionMode', *double3: float): ...
    def addElement(self, double: float) -> None: ...
    def addElementRolling(self, double: float) -> float: ...
    def addElements(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def clear(self) -> None: ...
    def compute(self, function: MathArrays.Function) -> float: ...
    def contract(self) -> None: ...
    @typing.overload
    @staticmethod
    def copy(resizableDoubleArray: 'ResizableDoubleArray', resizableDoubleArray2: 'ResizableDoubleArray') -> None: ...
    @typing.overload
    def copy(self) -> 'ResizableDoubleArray': ...
    def discardFrontElements(self, int: int) -> None: ...
    def discardMostRecentElements(self, int: int) -> None: ...
    def equals(self, object: typing.Any) -> bool: ...
    def getCapacity(self) -> int: ...
    def getContractionCriterion(self) -> float: ...
    def getElement(self, int: int) -> float: ...
    def getElements(self) -> typing.MutableSequence[float]: ...
    def getNumElements(self) -> int: ...
    def hashCode(self) -> int: ...
    def setElement(self, int: int, double: float) -> None: ...
    def setNumElements(self, int: int) -> None: ...
    def substituteMostRecentElement(self, double: float) -> float: ...
    class ExpansionMode(java.lang.Enum['ResizableDoubleArray.ExpansionMode']):
        MULTIPLICATIVE: typing.ClassVar['ResizableDoubleArray.ExpansionMode'] = ...
        ADDITIVE: typing.ClassVar['ResizableDoubleArray.ExpansionMode'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'ResizableDoubleArray.ExpansionMode': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['ResizableDoubleArray.ExpansionMode']: ...

class TransformerMap(NumberTransformer, java.io.Serializable):
    """
    public class TransformerMap extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.util.NumberTransformer`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This TansformerMap automates the transformation of mixed object types. It provides a means to set NumberTransformers
        that will be selected based on the Class of the object handed to the Maps :code:`double transform(Object o)` method.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def classes(self) -> java.util.Set[typing.Type[typing.Any]]: ...
    def clear(self) -> None:
        """
            Clears all the Class to Transformer mappings.
        
        """
        ...
    def containsClass(self, class_: typing.Type[typing.Any]) -> bool: ...
    def containsTransformer(self, numberTransformer: typing.Union[NumberTransformer, typing.Callable]) -> bool:
        """
            Tests if a NumberTransformer is present in the TransformerMap.
        
            Parameters:
                value (:class:`~fr.cnes.sirius.patrius.math.util.NumberTransformer`): NumberTransformer to check
        
            Returns:
                true|false
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getTransformer(self, class_: typing.Type[typing.Any]) -> NumberTransformer: ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def putTransformer(self, class_: typing.Type[typing.Any], numberTransformer: typing.Union[NumberTransformer, typing.Callable]) -> NumberTransformer: ...
    def removeTransformer(self, class_: typing.Type[typing.Any]) -> NumberTransformer: ...
    def transform(self, object: typing.Any) -> float:
        """
            Attempts to transform the Object against the map of NumberTransformers. Otherwise it returns Double.NaN.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.util.NumberTransformer.transform` in
                interface :class:`~fr.cnes.sirius.patrius.math.util.NumberTransformer`
        
            Parameters:
                o (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the Object to be transformed.
        
            Returns:
                the double value of the Object.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the Object can not be transformed into a Double.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.util.NumberTransformer.transform`
        
        
        """
        ...
    def transformers(self) -> java.util.Collection[NumberTransformer]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.util")``.

    ArithmeticUtils: typing.Type[ArithmeticUtils]
    BigReal: typing.Type[BigReal]
    BigRealField: typing.Type[BigRealField]
    Combinations: typing.Type[Combinations]
    CombinatoricsUtils: typing.Type[CombinatoricsUtils]
    CompositeFormat: typing.Type[CompositeFormat]
    ContinuedFraction: typing.Type[ContinuedFraction]
    Decimal64: typing.Type[Decimal64]
    Decimal64Field: typing.Type[Decimal64Field]
    DefaultTransformer: typing.Type[DefaultTransformer]
    DoubleArray: typing.Type[DoubleArray]
    FastMath: typing.Type[FastMath]
    Incrementor: typing.Type[Incrementor]
    IterationEvent: typing.Type[IterationEvent]
    IterationListener: typing.Type[IterationListener]
    IterationManager: typing.Type[IterationManager]
    MathArrays: typing.Type[MathArrays]
    MathLib: typing.Type[MathLib]
    MathUtils: typing.Type[MathUtils]
    MultidimensionalCounter: typing.Type[MultidimensionalCounter]
    NumberTransformer: typing.Type[NumberTransformer]
    OpenIntToDoubleHashMap: typing.Type[OpenIntToDoubleHashMap]
    OpenIntToFieldHashMap: typing.Type[OpenIntToFieldHashMap]
    Pair: typing.Type[Pair]
    Precision: typing.Type[Precision]
    ResizableDoubleArray: typing.Type[ResizableDoubleArray]
    TransformerMap: typing.Type[TransformerMap]
