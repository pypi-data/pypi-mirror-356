
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math
import fr.cnes.sirius.patrius.math.exception
import java.io
import java.lang
import java.math
import java.text
import java.util
import typing



class AbstractFormat(java.text.NumberFormat):
    """
    public abstract class AbstractFormat extends `NumberFormat <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>`
    
        Common part shared by both :class:`~fr.cnes.sirius.patrius.math.fraction.FractionFormat` and
        :class:`~fr.cnes.sirius.patrius.math.fraction.BigFractionFormat`.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def format(self, object: typing.Any) -> str: ...
    @typing.overload
    def format(self, double: float) -> str: ...
    @typing.overload
    def format(self, long: int) -> str: ...
    @typing.overload
    def format(self, double: float, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer:
        """
            Formats a double value as a fraction and appends the result to a StringBuffer.
        
            Specified by:
                 in class 
        
            Parameters:
                value (double): the double value to format
                buffer (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): StringBuffer to append to
                position (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
        
            Returns:
                a reference to the appended buffer
        
            Also see:
                `null
                <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true#format-java.lang.Object-java.lang.StringBuffer-java.text.FieldPosition->`
        
            Formats a long value as a fraction and appends the result to a StringBuffer.
        
            Specified by:
                 in class 
        
            Parameters:
                value (long): the long value to format
                buffer (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): StringBuffer to append to
                position (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
        
            Returns:
                a reference to the appended buffer
        
            Also see:
                `null
                <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true#format-java.lang.Object-java.lang.StringBuffer-java.text.FieldPosition->`
        
        
        """
        ...
    @typing.overload
    def format(self, long: int, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @typing.overload
    def format(self, object: typing.Any, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    def getDenominatorFormat(self) -> java.text.NumberFormat:
        """
            Access the denominator format.
        
            Returns:
                the denominator format.
        
        
        """
        ...
    def getNumeratorFormat(self) -> java.text.NumberFormat:
        """
            Access the numerator format.
        
            Returns:
                the numerator format.
        
        
        """
        ...
    def setDenominatorFormat(self, numberFormat: java.text.NumberFormat) -> None:
        """
            Modify the denominator format.
        
            Parameters:
                format (`NumberFormat <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>`): the new denominator format value.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`format` is :code:`null`.
        
        
        """
        ...
    def setNumeratorFormat(self, numberFormat: java.text.NumberFormat) -> None:
        """
            Modify the numerator format.
        
            Parameters:
                format (`NumberFormat <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>`): the new numerator format value.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`format` is :code:`null`.
        
        
        """
        ...

class BigFraction(java.lang.Number, fr.cnes.sirius.patrius.math.FieldElement['BigFraction'], java.lang.Comparable['BigFraction']):
    """
    public class BigFraction extends `Number <http://docs.oracle.com/javase/8/docs/api/java/lang/Number.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.FieldElement`<:class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`>, `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`>
    
        Representation of a rational number without any overflow. This class is immutable.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    TWO: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` TWO
    
        A fraction representing "2 / 1".
    
    """
    ONE: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` ONE
    
        A fraction representing "1".
    
    """
    ZERO: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` ZERO
    
        A fraction representing "0".
    
    """
    MINUS_ONE: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` MINUS_ONE
    
        A fraction representing "-1 / 1".
    
    """
    FOUR_FIFTHS: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` FOUR_FIFTHS
    
        A fraction representing "4/5".
    
    """
    ONE_FIFTH: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` ONE_FIFTH
    
        A fraction representing "1/5".
    
    """
    ONE_HALF: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` ONE_HALF
    
        A fraction representing "1/2".
    
    """
    ONE_QUARTER: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` ONE_QUARTER
    
        A fraction representing "1/4".
    
    """
    ONE_THIRD: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` ONE_THIRD
    
        A fraction representing "1/3".
    
    """
    THREE_FIFTHS: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` THREE_FIFTHS
    
        A fraction representing "3/5".
    
    """
    THREE_QUARTERS: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` THREE_QUARTERS
    
        A fraction representing "3/4".
    
    """
    TWO_FIFTHS: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` TWO_FIFTHS
    
        A fraction representing "2/5".
    
    """
    TWO_QUARTERS: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` TWO_QUARTERS
    
        A fraction representing "2/4".
    
    """
    TWO_THIRDS: typing.ClassVar['BigFraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` TWO_THIRDS
    
        A fraction representing "2/3".
    
    """
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, int: int): ...
    @typing.overload
    def __init__(self, double: float, int: int): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    @typing.overload
    def __init__(self, bigInteger: java.math.BigInteger): ...
    @typing.overload
    def __init__(self, bigInteger: java.math.BigInteger, bigInteger2: java.math.BigInteger): ...
    @typing.overload
    def __init__(self, long: int): ...
    @typing.overload
    def __init__(self, long: int, long2: int): ...
    def abs(self) -> 'BigFraction':
        """
        
            Returns the absolute value of this :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`.
        
            Returns:
                the absolute value as a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`.
        
        
        """
        ...
    @typing.overload
    def add(self, bigFraction: 'BigFraction') -> 'BigFraction':
        """
        
            Adds the value of this fraction to the passed `null
            <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>`, returning the result in reduced
            form.
        
            Parameters:
                bg (`BigInteger <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>`): the `null <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>` to add, must'nt be
                    :code:`null`.
        
            Returns:
                a :code:`BigFraction` instance with the resulting values.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the `null <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>` is :code:`null`.
        
        
            Adds the value of this fraction to the passed ``integer``, returning the result in reduced form.
        
            Parameters:
                i (int): the ``integer`` to add.
        
            Returns:
                a :code:`BigFraction` instance with the resulting values.
        
        
            Adds the value of this fraction to the passed ``long``, returning the result in reduced form.
        
            Parameters:
                l (long): the ``long`` to add.
        
            Returns:
                a :code:`BigFraction` instance with the resulting values.
        
        
            Adds the value of this fraction to another, returning the result in reduced form.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.add` in interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                fraction (:class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`): the :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` to add, must not be :code:`null`.
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` instance with the resulting values.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` is :code:`null`.
        
        
        """
        ...
    @typing.overload
    def add(self, int: int) -> 'BigFraction': ...
    @typing.overload
    def add(self, bigInteger: java.math.BigInteger) -> 'BigFraction': ...
    @typing.overload
    def add(self, long: int) -> 'BigFraction': ...
    @typing.overload
    def bigDecimalValue(self) -> java.math.BigDecimal:
        """
        
            Gets the fraction as a :code:`BigDecimal`. This calculates the fraction as the numerator divided by denominator.
        
            Returns:
                the fraction as a :code:`BigDecimal`.
        
            Raises:
                : if the exact quotient does not have a terminating decimal expansion.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html?is-external=true>`
        
        """
        ...
    @typing.overload
    def bigDecimalValue(self, int: int) -> java.math.BigDecimal:
        """
        
            Gets the fraction as a :code:`BigDecimal` following the passed rounding mode. This calculates the fraction as the
            numerator divided by denominator.
        
            Parameters:
                roundingMode (int): rounding mode to apply. see `null <http://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html?is-external=true>`
                    constants.
        
            Returns:
                the fraction as a :code:`BigDecimal`.
        
            Raises:
                : if ``roundingMode`` does not represent a valid rounding mode.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html?is-external=true>`
        
        
            Gets the fraction as a :code:`BigDecimal` following the passed scale and rounding mode. This calculates the fraction as
            the numerator divided by denominator.
        
            Parameters:
                scale (int): scale of the :code:`BigDecimal` quotient to be returned. see `null
                    <http://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html?is-external=true>` for more information.
                roundingMode (int): rounding mode to apply. see `null <http://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html?is-external=true>`
                    constants.
        
            Returns:
                the fraction as a :code:`BigDecimal`.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html?is-external=true>`
        
        
        """
        ...
    @typing.overload
    def bigDecimalValue(self, int: int, int2: int) -> java.math.BigDecimal: ...
    def compareTo(self, bigFraction: 'BigFraction') -> int:
        """
        
            Compares this object to another based on size.
        
            Specified by:
                 in interface 
        
            Parameters:
                object (:class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`): the object to compare to, must not be :code:`null`.
        
            Returns:
                -1 if this is less than ``object``, +1 if this is greater than ``object``, 0 if they are equal.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true#compareTo-T->`
        
        
        """
        ...
    @typing.overload
    def divide(self, bigFraction: 'BigFraction') -> 'BigFraction':
        """
        
            Divide the value of this fraction by the passed :code:`BigInteger`, ie :code:`this * 1 / bg`, returning the result in
            reduced form.
        
            Parameters:
                bg (`BigInteger <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>`): the :code:`BigInteger` to divide by, must not be :code:`null`
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` instance with the resulting values
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the :code:`BigInteger` is :code:`null`
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the fraction to divide by is zero
        
        
            Divide the value of this fraction by the passed :code:`int`, ie :code:`this * 1 / i`, returning the result in reduced
            form.
        
            Parameters:
                i (int): the :code:`int` to divide by
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` instance with the resulting values
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the fraction to divide by is zero
        
        
            Divide the value of this fraction by the passed :code:`long`, ie :code:`this * 1 / l`, returning the result in reduced
            form.
        
            Parameters:
                l (long): the :code:`long` to divide by
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` instance with the resulting values
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the fraction to divide by is zero
        
        
            Divide the value of this fraction by another, returning the result in reduced form.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.divide` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                fraction (:class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`): Fraction to divide by, must not be :code:`null`.
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` instance with the resulting values.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the :code:`fraction` is :code:`null`.
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the fraction to divide by is zero
        
        
        """
        ...
    @typing.overload
    def divide(self, int: int) -> 'BigFraction': ...
    @typing.overload
    def divide(self, bigInteger: java.math.BigInteger) -> 'BigFraction': ...
    @typing.overload
    def divide(self, long: int) -> 'BigFraction': ...
    def doubleValue(self) -> float:
        """
        
            Gets the fraction as a ``double``. This calculates the fraction as the numerator divided by denominator.
        
            Specified by:
                 in class 
        
            Returns:
                the fraction as a ``double``
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Number.html?is-external=true#doubleValue-->`
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Test for the equality of two fractions. If the lowest term numerator and denominators are the same for both fractions,
            the two fractions are considered to be equal.
        
            Overrides:
                 in class 
        
            Parameters:
                other (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): fraction to test for equality to this fraction, can be :code:`null`.
        
            Returns:
                true if two fractions are equal, false if object is :code:`null`, not an instance of
                :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`, or not equal to this fraction instance.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#equals-java.lang.Object->`
        
        
        """
        ...
    def floatValue(self) -> float:
        """
        
            Gets the fraction as a ``float``. This calculates the fraction as the numerator divided by denominator.
        
            Specified by:
                 in class 
        
            Returns:
                the fraction as a ``float``.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Number.html?is-external=true#floatValue-->`
        
        
        """
        ...
    def getDenominator(self) -> java.math.BigInteger:
        """
        
            Access the denominator as a :code:`BigInteger`.
        
            Returns:
                the denominator as a :code:`BigInteger`.
        
        
        """
        ...
    def getDenominatorAsInt(self) -> int:
        """
        
            Access the denominator as a ``int``.
        
            Returns:
                the denominator as a ``int``.
        
        
        """
        ...
    def getDenominatorAsLong(self) -> int:
        """
        
            Access the denominator as a ``long``.
        
            Returns:
                the denominator as a ``long``.
        
        
        """
        ...
    def getField(self) -> 'BigFractionField':
        """
            Get the :class:`~fr.cnes.sirius.patrius.math.Field` to which the instance belongs.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.getField` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Returns:
                :class:`~fr.cnes.sirius.patrius.math.Field` to which the instance belongs
        
        
        """
        ...
    def getNumerator(self) -> java.math.BigInteger:
        """
        
            Access the numerator as a :code:`BigInteger`.
        
            Returns:
                the numerator as a :code:`BigInteger`.
        
        
        """
        ...
    def getNumeratorAsInt(self) -> int:
        """
        
            Access the numerator as a ``int``.
        
            Returns:
                the numerator as a ``int``.
        
        
        """
        ...
    def getNumeratorAsLong(self) -> int:
        """
        
            Access the numerator as a ``long``.
        
            Returns:
                the numerator as a ``long``.
        
        
        """
        ...
    @staticmethod
    def getReducedFraction(int: int, int2: int) -> 'BigFraction':
        """
        
            Creates a :code:`BigFraction` instance with the 2 parts of a fraction Y/Z.
        
            Any negative signs are resolved to be on the numerator.
        
            Parameters:
                numerator (int): the numerator, for example the three in 'three sevenths'.
                denominator (int): the denominator, for example the seven in 'three sevenths'.
        
            Returns:
                a new fraction instance, with the numerator and denominator reduced.
        
            Raises:
                : if the denominator is :code:`zero`.
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Gets a hashCode for the fraction.
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#hashCode-->`
        
        
        """
        ...
    def intValue(self) -> int:
        """
        
            Gets the fraction as an ``int``. This returns the whole number part of the fraction.
        
            Specified by:
                 in class 
        
            Returns:
                the whole number fraction part.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Number.html?is-external=true#intValue-->`
        
        
        """
        ...
    def longValue(self) -> int:
        """
        
            Gets the fraction as a ``long``. This returns the whole number part of the fraction.
        
            Specified by:
                 in class 
        
            Returns:
                the whole number fraction part.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Number.html?is-external=true#longValue-->`
        
        
        """
        ...
    @typing.overload
    def multiply(self, bigFraction: 'BigFraction') -> 'BigFraction':
        """
        
            Multiplies the value of this fraction by the passed :code:`BigInteger`, returning the result in reduced form.
        
            Parameters:
                bg (`BigInteger <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>`): the :code:`BigInteger` to multiply by.
        
            Returns:
                a :code:`BigFraction` instance with the resulting values.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`bg` is :code:`null`.
        
        
            Multiply the value of this fraction by the passed ``int``, returning the result in reduced form.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.multiply` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                i (int): the ``int`` to multiply by.
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` instance with the resulting values.
        
        
            Multiply the value of this fraction by the passed ``long``, returning the result in reduced form.
        
            Parameters:
                l (long): the ``long`` to multiply by.
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` instance with the resulting values.
        
        
            Multiplies the value of this fraction by another, returning the result in reduced form.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.multiply` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                fraction (:class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`): Fraction to multiply by, must not be :code:`null`.
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` instance with the resulting values.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`fraction` is :code:`null`.
        
        
        """
        ...
    @typing.overload
    def multiply(self, int: int) -> 'BigFraction': ...
    @typing.overload
    def multiply(self, bigInteger: java.math.BigInteger) -> 'BigFraction': ...
    @typing.overload
    def multiply(self, long: int) -> 'BigFraction': ...
    def negate(self) -> 'BigFraction':
        """
        
            Return the additive inverse of this fraction, returning the result in reduced form.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.negate` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Returns:
                the negation of this fraction.
        
        
        """
        ...
    def percentageValue(self) -> float:
        """
        
            Gets the fraction percentage as a ``double``. This calculates the fraction as the numerator divided by denominator
            multiplied by 100.
        
            Returns:
                the fraction percentage as a ``double``.
        
        
        """
        ...
    @typing.overload
    def pow(self, double: float) -> float:
        """
        
            Returns a :code:`BigFraction` whose value is :code:`(this<sup>exponent</sup>)`, returning the result in reduced form.
        
            Parameters:
                exponent (int): exponent to which this :code:`BigFraction` is to be raised.
        
            Returns:
                ``this :sup:`exponent```.
        
        
            Returns a :code:`BigFraction` whose value is ``(this :sup:`exponent` )``, returning the result in reduced form.
        
            Parameters:
                exponent (long): exponent to which this :code:`BigFraction` is to be raised.
        
            Returns:
                ``this :sup:`exponent``` as a :code:`BigFraction`.
        
        
            Returns a :code:`BigFraction` whose value is ``(this :sup:`exponent` )``, returning the result in reduced form.
        
            Parameters:
                exponent (`BigInteger <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>`): exponent to which this :code:`BigFraction` is to be raised.
        
            Returns:
                ``this :sup:`exponent``` as a :code:`BigFraction`.
        
        
            Returns a :code:`double` whose value is ``(this :sup:`exponent` )``, returning the result in reduced form.
        
            Parameters:
                exponent (double): exponent to which this :code:`BigFraction` is to be raised.
        
            Returns:
                ``this :sup:`exponent```.
        
        
        """
        ...
    @typing.overload
    def pow(self, int: int) -> 'BigFraction': ...
    @typing.overload
    def pow(self, bigInteger: java.math.BigInteger) -> 'BigFraction': ...
    @typing.overload
    def pow(self, long: int) -> 'BigFraction': ...
    def reciprocal(self) -> 'BigFraction':
        """
        
            Return the multiplicative inverse of this fraction.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.reciprocal` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Returns:
                the reciprocal fraction.
        
        
        """
        ...
    def reduce(self) -> 'BigFraction':
        """
        
            Reduce this :code:`BigFraction` to its lowest terms.
        
            Returns:
                the reduced :code:`BigFraction`. It doesn't change anything if the fraction can be reduced.
        
        
        """
        ...
    @typing.overload
    def subtract(self, bigFraction: 'BigFraction') -> 'BigFraction':
        """
        
            Subtracts the value of an `null <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>`
            from the value of this :code:`BigFraction`, returning the result in reduced form.
        
            Parameters:
                bg (`BigInteger <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>`): the `null <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>` to subtract, cannot be
                    :code:`null`.
        
            Returns:
                a :code:`BigFraction` instance with the resulting values.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the `null <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>` is :code:`null`.
        
        
            Subtracts the value of an :code:`integer` from the value of this :code:`BigFraction`, returning the result in reduced
            form.
        
            Parameters:
                i (int): the :code:`integer` to subtract.
        
            Returns:
                a :code:`BigFraction` instance with the resulting values.
        
        
            Subtracts the value of a :code:`long` from the value of this :code:`BigFraction`, returning the result in reduced form.
        
            Parameters:
                l (long): the :code:`long` to subtract.
        
            Returns:
                a :code:`BigFraction` instance with the resulting values.
        
        
            Subtracts the value of another fraction from the value of this one, returning the result in reduced form.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.subtract` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                fraction (:class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`): :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` to subtract, must not be :code:`null`.
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` instance with the resulting values
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the :code:`fraction` is :code:`null`.
        
        
        """
        ...
    @typing.overload
    def subtract(self, int: int) -> 'BigFraction': ...
    @typing.overload
    def subtract(self, bigInteger: java.math.BigInteger) -> 'BigFraction': ...
    @typing.overload
    def subtract(self, long: int) -> 'BigFraction': ...
    def toString(self) -> str:
        """
        
            Returns the :code:`String` representing this fraction, ie "num / dem" or just "num" if the denominator is one.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of the fraction.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#toString-->`
        
        
        """
        ...

class BigFractionField(fr.cnes.sirius.patrius.math.Field[BigFraction], java.io.Serializable):
    """
    public final class BigFractionField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.Field`<:class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Representation of the fractional numbers without any overflow field.
    
        This class is a singleton.
    
        Since:
            2.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`, :meth:`~serialized`
    """
    @staticmethod
    def getInstance() -> 'BigFractionField':
        """
            Get the unique instance.
        
            Returns:
                the unique instance
        
        
        """
        ...
    def getOne(self) -> BigFraction:
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
    def getRuntimeClass(self) -> typing.Type[fr.cnes.sirius.patrius.math.FieldElement[BigFraction]]: ...
    def getZero(self) -> BigFraction:
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

class Fraction(java.lang.Number, fr.cnes.sirius.patrius.math.FieldElement['Fraction'], java.lang.Comparable['Fraction']):
    """
    public class Fraction extends `Number <http://docs.oracle.com/javase/8/docs/api/java/lang/Number.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.FieldElement`<:class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`>, `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`>
    
        Representation of a rational number. implements Serializable since 2.0
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    TWO: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` TWO
    
        A fraction representing "2 / 1".
    
    """
    ONE: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` ONE
    
        A fraction representing "1".
    
    """
    ZERO: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` ZERO
    
        A fraction representing "0".
    
    """
    FOUR_FIFTHS: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` FOUR_FIFTHS
    
        A fraction representing "4/5".
    
    """
    ONE_FIFTH: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` ONE_FIFTH
    
        A fraction representing "1/5".
    
    """
    ONE_HALF: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` ONE_HALF
    
        A fraction representing "1/2".
    
    """
    ONE_QUARTER: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` ONE_QUARTER
    
        A fraction representing "1/4".
    
    """
    ONE_THIRD: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` ONE_THIRD
    
        A fraction representing "1/3".
    
    """
    THREE_FIFTHS: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` THREE_FIFTHS
    
        A fraction representing "3/5".
    
    """
    THREE_QUARTERS: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` THREE_QUARTERS
    
        A fraction representing "3/4".
    
    """
    TWO_FIFTHS: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` TWO_FIFTHS
    
        A fraction representing "2/5".
    
    """
    TWO_QUARTERS: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` TWO_QUARTERS
    
        A fraction representing "2/4".
    
    """
    TWO_THIRDS: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` TWO_THIRDS
    
        A fraction representing "2/3".
    
    """
    MINUS_ONE: typing.ClassVar['Fraction'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` MINUS_ONE
    
        A fraction representing "-1 / 1".
    
    """
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, int: int): ...
    @typing.overload
    def __init__(self, double: float, int: int): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    def abs(self) -> 'Fraction':
        """
            Returns the absolute value of this fraction.
        
            Returns:
                the absolute value.
        
        
        """
        ...
    @typing.overload
    def add(self, fraction: 'Fraction') -> 'Fraction':
        """
        
            Adds the value of this fraction to another, returning the result in reduced form. The algorithm follows Knuth, 4.5.1.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.add` in interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                fraction (:class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`): the fraction to add, must not be :code:`null`
        
            Returns:
                a :code:`Fraction` instance with the resulting values
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the fraction is :code:`null`
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the resulting numerator or denominator exceeds :code:`Integer.MAX_VALUE`
        
            Add an integer to the fraction.
        
            Parameters:
                i (int): the ``integer`` to add.
        
            Returns:
                this + i
        
        
        """
        ...
    @typing.overload
    def add(self, int: int) -> 'Fraction': ...
    def compareTo(self, fraction: 'Fraction') -> int:
        """
            Compares this object to another based on size.
        
            Specified by:
                 in interface 
        
            Parameters:
                object (:class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`): the object to compare to
        
            Returns:
                -1 if this is less than ``object``, +1 if this is greater than ``object``, 0 if they are equal.
        
        
        """
        ...
    @typing.overload
    def divide(self, fraction: 'Fraction') -> 'Fraction':
        """
        
            Divide the value of this fraction by another.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.divide` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                fraction (:class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`): the fraction to divide by, must not be :code:`null`
        
            Returns:
                a :code:`Fraction` instance with the resulting values
        
            Raises:
                : if the fraction is :code:`null`
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the fraction to divide by is zero
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the resulting numerator or denominator exceeds :code:`Integer.MAX_VALUE`
        
            Divide the fraction by an integer.
        
            Parameters:
                i (int): the ``integer`` to divide by.
        
            Returns:
                this * i
        
        
        """
        ...
    @typing.overload
    def divide(self, int: int) -> 'Fraction': ...
    def doubleValue(self) -> float:
        """
            Gets the fraction as a ``double``. This calculates the fraction as the numerator divided by denominator.
        
            Specified by:
                 in class 
        
            Returns:
                the fraction as a ``double``
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two fractions. If the lowest term numerator and denominators are the same for both fractions,
            the two fractions are considered to be equal.
        
            Overrides:
                 in class 
        
            Parameters:
                other (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): fraction to test for equality to this fraction
        
            Returns:
                true if two fractions are equal, false if object is ``null``, not an instance of
                :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`, or not equal to this fraction instance.
        
        
        """
        ...
    def floatValue(self) -> float:
        """
            Gets the fraction as a ``float``. This calculates the fraction as the numerator divided by denominator.
        
            Specified by:
                 in class 
        
            Returns:
                the fraction as a ``float``
        
        
        """
        ...
    def getDenominator(self) -> int:
        """
            Access the denominator.
        
            Returns:
                the denominator.
        
        
        """
        ...
    def getField(self) -> 'FractionField':
        """
            Get the :class:`~fr.cnes.sirius.patrius.math.Field` to which the instance belongs.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.getField` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Returns:
                :class:`~fr.cnes.sirius.patrius.math.Field` to which the instance belongs
        
        
        """
        ...
    def getNumerator(self) -> int:
        """
            Access the numerator.
        
            Returns:
                the numerator.
        
        
        """
        ...
    @staticmethod
    def getReducedFraction(int: int, int2: int) -> 'Fraction':
        """
        
            Creates a :code:`Fraction` instance with the 2 parts of a fraction Y/Z.
        
            Any negative signs are resolved to be on the numerator.
        
            Parameters:
                numeratorIn (int): the numerator, for example the three in 'three sevenths'
                denominatorIn (int): the denominator, for example the seven in 'three sevenths'
        
            Returns:
                a new fraction instance, with the numerator and denominator reduced
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the denominator is :code:`zero`
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Gets a hashCode for the fraction.
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    def intValue(self) -> int:
        """
            Gets the fraction as an ``int``. This returns the whole number part of the fraction.
        
            Specified by:
                 in class 
        
            Returns:
                the whole number fraction part
        
        
        """
        ...
    def longValue(self) -> int:
        """
            Gets the fraction as a ``long``. This returns the whole number part of the fraction.
        
            Specified by:
                 in class 
        
            Returns:
                the whole number fraction part
        
        
        """
        ...
    @typing.overload
    def multiply(self, fraction: 'Fraction') -> 'Fraction':
        """
        
            Multiplies the value of this fraction by another, returning the result in reduced form.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.multiply` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                fraction (:class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`): the fraction to multiply by, must not be :code:`null`
        
            Returns:
                a :code:`Fraction` instance with the resulting values
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the fraction is :code:`null`
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the resulting numerator or denominator exceeds :code:`Integer.MAX_VALUE`
        
            Multiply the fraction by an integer.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.multiply` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                i (int): the ``integer`` to multiply by.
        
            Returns:
                this * i
        
        
        """
        ...
    @typing.overload
    def multiply(self, int: int) -> 'Fraction': ...
    def negate(self) -> 'Fraction':
        """
            Return the additive inverse of this fraction.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.negate` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Returns:
                the negation of this fraction.
        
        
        """
        ...
    def percentageValue(self) -> float:
        """
        
            Gets the fraction percentage as a ``double``. This calculates the fraction as the numerator divided by denominator
            multiplied by 100.
        
            Returns:
                the fraction percentage as a ``double``.
        
        
        """
        ...
    def reciprocal(self) -> 'Fraction':
        """
            Return the multiplicative inverse of this fraction.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.reciprocal` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Returns:
                the reciprocal fraction
        
        
        """
        ...
    @typing.overload
    def subtract(self, fraction: 'Fraction') -> 'Fraction':
        """
        
            Subtracts the value of another fraction from the value of this one, returning the result in reduced form.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.FieldElement.subtract` in
                interface :class:`~fr.cnes.sirius.patrius.math.FieldElement`
        
            Parameters:
                fraction (:class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`): the fraction to subtract, must not be :code:`null`
        
            Returns:
                a :code:`Fraction` instance with the resulting values
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the fraction is :code:`null`
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the resulting numerator or denominator cannot be represented in an :code:`int`.
        
            Subtract an integer from the fraction.
        
            Parameters:
                i (int): the ``integer`` to subtract.
        
            Returns:
                this - i
        
        
        """
        ...
    @typing.overload
    def subtract(self, int: int) -> 'Fraction': ...
    def toString(self) -> str:
        """
        
            Returns the :code:`String` representing this fraction, ie "num / dem" or just "num" if the denominator is one.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of the fraction.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#toString-->`
        
        
        """
        ...

class FractionConversionException(fr.cnes.sirius.patrius.math.exception.ConvergenceException):
    """
    public class FractionConversionException extends :class:`~fr.cnes.sirius.patrius.math.exception.ConvergenceException`
    
        Error thrown when a double value cannot be converted to a fraction in the allowed number of iterations.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, int: int): ...
    @typing.overload
    def __init__(self, double: float, long: int, long2: int): ...

class FractionField(fr.cnes.sirius.patrius.math.Field[Fraction], java.io.Serializable):
    """
    public final class FractionField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.Field`<:class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Representation of the fractional numbers field.
    
        This class is a singleton.
    
        Since:
            2.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`, :meth:`~serialized`
    """
    @staticmethod
    def getInstance() -> 'FractionField':
        """
            Get the unique instance.
        
            Returns:
                the unique instance
        
        
        """
        ...
    def getOne(self) -> Fraction:
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
    def getRuntimeClass(self) -> typing.Type[fr.cnes.sirius.patrius.math.FieldElement[Fraction]]: ...
    def getZero(self) -> Fraction:
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

class BigFractionFormat(AbstractFormat):
    """
    public class BigFractionFormat extends :class:`~fr.cnes.sirius.patrius.math.fraction.AbstractFormat`
    
        Formats a BigFraction number in proper format or improper format.
    
        The number format for each of the whole number, numerator and, denominator can be configured.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, numberFormat: java.text.NumberFormat): ...
    @typing.overload
    def __init__(self, numberFormat: java.text.NumberFormat, numberFormat2: java.text.NumberFormat): ...
    @typing.overload
    def format(self, object: typing.Any) -> str: ...
    @typing.overload
    def format(self, double: float) -> str: ...
    @typing.overload
    def format(self, long: int) -> str: ...
    @typing.overload
    def format(self, double: float, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer:
        """
            Formats a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` object to produce a string. The BigFraction is
            output in improper format.
        
            Parameters:
                bigFraction (:class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`): the object to format.
                toAppendTo (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): where the text is to be appended
                pos (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
        
            Returns:
                the value passed in as toAppendTo.
        
            Formats an object and appends the result to a StringBuffer. :code:`obj` must be either a
            :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` object or a `null
            <http://docs.oracle.com/javase/8/docs/api/java/math/BigInteger.html?is-external=true>` object or a `null
            <http://docs.oracle.com/javase/8/docs/api/java/lang/Number.html?is-external=true>` object. Any other type of object will
            result in an `null <http://docs.oracle.com/javase/8/docs/api/java/lang/IllegalArgumentException.html?is-external=true>`
            being thrown.
        
            Overrides:
                 in class 
        
            Parameters:
                obj (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the object to format.
                toAppendTo (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): where the text is to be appended
                pos (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
        
            Returns:
                the value passed in as toAppendTo.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if :code:`obj` is not a valid type.
        
            Also see:
                `null
                <http://docs.oracle.com/javase/8/docs/api/java/text/Format.html?is-external=true#format-java.lang.Object-java.lang.StringBuffer-java.text.FieldPosition->`
        
        
        """
        ...
    @typing.overload
    def format(self, long: int, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @typing.overload
    def format(self, bigFraction: BigFraction, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @typing.overload
    def format(self, object: typing.Any, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @staticmethod
    def formatBigFraction(bigFraction: BigFraction) -> str:
        """
            This static method calls formatBigFraction() on a default instance of BigFractionFormat.
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`): BigFraction object to format
        
            Returns:
                A formatted BigFraction in proper form.
        
        
        """
        ...
    @staticmethod
    def getAvailableLocales() -> typing.MutableSequence[java.util.Locale]:
        """
            Get the set of locales for which complex formats are available. This is the same set as the `null
            <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>` set.
        
            Returns:
                available complex format locales.
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getImproperInstance() -> 'BigFractionFormat':
        """
            Returns the default complex format for the current locale.
        
            Returns:
                the default complex format.
        
        """
        ...
    @typing.overload
    @staticmethod
    def getImproperInstance(locale: java.util.Locale) -> 'BigFractionFormat':
        """
            Returns the default complex format for the given locale.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): the specific locale used by the format.
        
            Returns:
                the complex format specific to the given locale.
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getProperInstance() -> 'BigFractionFormat':
        """
            Returns the default complex format for the current locale.
        
            Returns:
                the default complex format.
        
        """
        ...
    @typing.overload
    @staticmethod
    def getProperInstance(locale: java.util.Locale) -> 'BigFractionFormat':
        """
            Returns the default complex format for the given locale.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): the specific locale used by the format.
        
            Returns:
                the complex format specific to the given locale.
        
        
        """
        ...
    @typing.overload
    def parse(self, string: str) -> BigFraction:
        """
            Parses a string to produce a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` object.
        
            Overrides:
                 in class 
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
        
            Returns:
                the parsed :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` object.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathParseException`: if the beginning of the specified string cannot be parsed.
        
        """
        ...
    @typing.overload
    def parse(self, string: str, parsePosition: java.text.ParsePosition) -> BigFraction:
        """
            Parses a string to produce a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` object. This method expects the
            string to be formatted as an improper BigFraction.
        
            Specified by:
                 in class 
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
                pos (`ParsePosition <http://docs.oracle.com/javase/8/docs/api/java/text/ParsePosition.html?is-external=true>`): input/output parsing parameter.
        
            Returns:
                the parsed :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` object.
        
        
        """
        ...

class FractionFormat(AbstractFormat):
    """
    public class FractionFormat extends :class:`~fr.cnes.sirius.patrius.math.fraction.AbstractFormat`
    
        Formats a Fraction number in proper format or improper format. The number format for each of the whole number, numerator
        and, denominator can be configured.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, numberFormat: java.text.NumberFormat): ...
    @typing.overload
    def __init__(self, numberFormat: java.text.NumberFormat, numberFormat2: java.text.NumberFormat): ...
    @typing.overload
    def format(self, object: typing.Any) -> str: ...
    @typing.overload
    def format(self, double: float) -> str: ...
    @typing.overload
    def format(self, long: int) -> str: ...
    @typing.overload
    def format(self, double: float, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer:
        """
            Formats a :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` object to produce a string. The fraction is output in
            improper format.
        
            Parameters:
                fraction (:class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`): the object to format.
                toAppendTo (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): where the text is to be appended
                pos (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
        
            Returns:
                the value passed in as toAppendTo.
        
            Formats an object and appends the result to a StringBuffer. :code:`obj` must be either a
            :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` object or a `null
            <http://docs.oracle.com/javase/8/docs/api/java/lang/Number.html?is-external=true>` object. Any other type of object will
            result in an `null <http://docs.oracle.com/javase/8/docs/api/java/lang/IllegalArgumentException.html?is-external=true>`
            being thrown.
        
            Overrides:
                 in class 
        
            Parameters:
                obj (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the object to format.
                toAppendTo (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): where the text is to be appended
                pos (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
        
            Returns:
                the value passed in as toAppendTo.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.fraction.FractionConversionException`: if the number cannot be converted to a fraction
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if :code:`obj` is not a valid type.
        
            Also see:
                `null
                <http://docs.oracle.com/javase/8/docs/api/java/text/Format.html?is-external=true#format-java.lang.Object-java.lang.StringBuffer-java.text.FieldPosition->`
        
        
        """
        ...
    @typing.overload
    def format(self, long: int, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @typing.overload
    def format(self, fraction: Fraction, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @typing.overload
    def format(self, object: typing.Any, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @staticmethod
    def formatFraction(fraction: Fraction) -> str:
        """
            This static method calls formatFraction() on a default instance of FractionFormat.
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`): Fraction object to format
        
            Returns:
                a formatted fraction in proper form.
        
        
        """
        ...
    @staticmethod
    def getAvailableLocales() -> typing.MutableSequence[java.util.Locale]:
        """
            Get the set of locales for which complex formats are available. This is the same set as the `null
            <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>` set.
        
            Returns:
                available complex format locales.
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getImproperInstance() -> 'FractionFormat':
        """
            Returns the default complex format for the current locale.
        
            Returns:
                the default complex format.
        
        """
        ...
    @typing.overload
    @staticmethod
    def getImproperInstance(locale: java.util.Locale) -> 'FractionFormat':
        """
            Returns the default complex format for the given locale.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): the specific locale used by the format.
        
            Returns:
                the complex format specific to the given locale.
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getProperInstance() -> 'FractionFormat':
        """
            Returns the default complex format for the current locale.
        
            Returns:
                the default complex format.
        
        """
        ...
    @typing.overload
    @staticmethod
    def getProperInstance(locale: java.util.Locale) -> 'FractionFormat':
        """
            Returns the default complex format for the given locale.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): the specific locale used by the format.
        
            Returns:
                the complex format specific to the given locale.
        
        
        """
        ...
    @typing.overload
    def parse(self, string: str) -> Fraction:
        """
            Parses a string to produce a :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` object.
        
            Overrides:
                 in class 
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
        
            Returns:
                the parsed :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` object.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathParseException`: if the beginning of the specified string cannot be parsed.
        
        """
        ...
    @typing.overload
    def parse(self, string: str, parsePosition: java.text.ParsePosition) -> Fraction:
        """
            Parses a string to produce a :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` object. This method expects the
            string to be formatted as an improper fraction.
        
            Specified by:
                 in class 
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
                pos (`ParsePosition <http://docs.oracle.com/javase/8/docs/api/java/text/ParsePosition.html?is-external=true>`): input/output parsing parameter.
        
            Returns:
                the parsed :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` object.
        
        
        """
        ...

class ProperBigFractionFormat(BigFractionFormat):
    """
    public class ProperBigFractionFormat extends :class:`~fr.cnes.sirius.patrius.math.fraction.BigFractionFormat`
    
        Formats a BigFraction number in proper format. The number format for each of the whole number, numerator and,
        denominator can be configured.
    
        Minus signs are only allowed in the whole number part - i.e., "-3 1/2" is legitimate and denotes -7/2, but "-3 -1/2" is
        invalid and will result in a :code:`ParseException`.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, numberFormat: java.text.NumberFormat): ...
    @typing.overload
    def __init__(self, numberFormat: java.text.NumberFormat, numberFormat2: java.text.NumberFormat, numberFormat3: java.text.NumberFormat): ...
    @typing.overload
    def format(self, object: typing.Any) -> str: ...
    @typing.overload
    def format(self, double: float) -> str: ...
    @typing.overload
    def format(self, long: int) -> str: ...
    @typing.overload
    def format(self, double: float, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer:
        """
            Formats a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` object to produce a string. The BigFraction is
            output in proper format.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.fraction.BigFractionFormat.format` in
                class :class:`~fr.cnes.sirius.patrius.math.fraction.BigFractionFormat`
        
            Parameters:
                fraction (:class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction`): the object to format.
                toAppendTo (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): where the text is to be appended
                pos (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
        
            Returns:
                the value passed in as toAppendTo.
        
        
        """
        ...
    @typing.overload
    def format(self, long: int, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @typing.overload
    def format(self, object: typing.Any, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @typing.overload
    def format(self, bigFraction: BigFraction, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    def getWholeFormat(self) -> java.text.NumberFormat:
        """
            Access the whole format.
        
            Returns:
                the whole format.
        
        
        """
        ...
    @typing.overload
    def parse(self, string: str) -> BigFraction: ...
    @typing.overload
    def parse(self, string: str, parsePosition: java.text.ParsePosition) -> BigFraction:
        """
            Parses a string to produce a :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` object. This method expects the
            string to be formatted as a proper BigFraction.
        
            Minus signs are only allowed in the whole number part - i.e., "-3 1/2" is legitimate and denotes -7/2, but "-3 -1/2" is
            invalid and will result in a :code:`ParseException`.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.fraction.BigFractionFormat.parse` in
                class :class:`~fr.cnes.sirius.patrius.math.fraction.BigFractionFormat`
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
                pos (`ParsePosition <http://docs.oracle.com/javase/8/docs/api/java/text/ParsePosition.html?is-external=true>`): input/ouput parsing parameter.
        
            Returns:
                the parsed :class:`~fr.cnes.sirius.patrius.math.fraction.BigFraction` object.
        
        
        """
        ...
    def setWholeFormat(self, numberFormat: java.text.NumberFormat) -> None:
        """
            Modify the whole format.
        
            Parameters:
                format (`NumberFormat <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>`): The new whole format value.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`format` is :code:`null`.
        
        
        """
        ...

class ProperFractionFormat(FractionFormat):
    """
    public class ProperFractionFormat extends :class:`~fr.cnes.sirius.patrius.math.fraction.FractionFormat`
    
        Formats a Fraction number in proper format. The number format for each of the whole number, numerator and, denominator
        can be configured.
    
        Minus signs are only allowed in the whole number part - i.e., "-3 1/2" is legitimate and denotes -7/2, but "-3 -1/2" is
        invalid and will result in a :code:`ParseException`.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, numberFormat: java.text.NumberFormat): ...
    @typing.overload
    def __init__(self, numberFormat: java.text.NumberFormat, numberFormat2: java.text.NumberFormat, numberFormat3: java.text.NumberFormat): ...
    @typing.overload
    def format(self, object: typing.Any) -> str: ...
    @typing.overload
    def format(self, double: float) -> str: ...
    @typing.overload
    def format(self, long: int) -> str: ...
    @typing.overload
    def format(self, double: float, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer:
        """
            Formats a :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` object to produce a string. The fraction is output in
            proper format.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.fraction.FractionFormat.format` in
                class :class:`~fr.cnes.sirius.patrius.math.fraction.FractionFormat`
        
            Parameters:
                fraction (:class:`~fr.cnes.sirius.patrius.math.fraction.Fraction`): the object to format.
                toAppendTo (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): where the text is to be appended
                pos (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
        
            Returns:
                the value passed in as toAppendTo.
        
        
        """
        ...
    @typing.overload
    def format(self, long: int, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @typing.overload
    def format(self, object: typing.Any, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @typing.overload
    def format(self, fraction: Fraction, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    def getWholeFormat(self) -> java.text.NumberFormat:
        """
            Access the whole format.
        
            Returns:
                the whole format.
        
        
        """
        ...
    @typing.overload
    def parse(self, string: str) -> Fraction: ...
    @typing.overload
    def parse(self, string: str, parsePosition: java.text.ParsePosition) -> Fraction:
        """
            Parses a string to produce a :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` object. This method expects the
            string to be formatted as a proper fraction.
        
            Minus signs are only allowed in the whole number part - i.e., "-3 1/2" is legitimate and denotes -7/2, but "-3 -1/2" is
            invalid and will result in a :code:`ParseException`.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.fraction.FractionFormat.parse` in
                class :class:`~fr.cnes.sirius.patrius.math.fraction.FractionFormat`
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
                pos (`ParsePosition <http://docs.oracle.com/javase/8/docs/api/java/text/ParsePosition.html?is-external=true>`): input/ouput parsing parameter.
        
            Returns:
                the parsed :class:`~fr.cnes.sirius.patrius.math.fraction.Fraction` object.
        
        
        """
        ...
    def setWholeFormat(self, numberFormat: java.text.NumberFormat) -> None:
        """
            Modify the whole format.
        
            Parameters:
                format (`NumberFormat <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>`): The new whole format value.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`format` is :code:`null`.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.fraction")``.

    AbstractFormat: typing.Type[AbstractFormat]
    BigFraction: typing.Type[BigFraction]
    BigFractionField: typing.Type[BigFractionField]
    BigFractionFormat: typing.Type[BigFractionFormat]
    Fraction: typing.Type[Fraction]
    FractionConversionException: typing.Type[FractionConversionException]
    FractionField: typing.Type[FractionField]
    FractionFormat: typing.Type[FractionFormat]
    ProperBigFractionFormat: typing.Type[ProperBigFractionFormat]
    ProperFractionFormat: typing.Type[ProperFractionFormat]
