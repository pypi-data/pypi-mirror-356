
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math
import java.io
import java.lang
import java.text
import java.util
import jpype
import typing



class Complex(fr.cnes.sirius.patrius.math.FieldElement['Complex'], java.io.Serializable):
    I: typing.ClassVar['Complex'] = ...
    NaN: typing.ClassVar['Complex'] = ...
    INF: typing.ClassVar['Complex'] = ...
    ONE: typing.ClassVar['Complex'] = ...
    ZERO: typing.ClassVar['Complex'] = ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    def abs(self) -> float: ...
    def acos(self) -> 'Complex': ...
    @typing.overload
    def add(self, double: float) -> 'Complex': ...
    @typing.overload
    def add(self, complex: 'Complex') -> 'Complex': ...
    def asin(self) -> 'Complex': ...
    def atan(self) -> 'Complex': ...
    def conjugate(self) -> 'Complex': ...
    def cos(self) -> 'Complex': ...
    def cosh(self) -> 'Complex': ...
    @typing.overload
    def divide(self, double: float) -> 'Complex': ...
    @typing.overload
    def divide(self, complex: 'Complex') -> 'Complex': ...
    def equals(self, object: typing.Any) -> bool: ...
    def exp(self) -> 'Complex': ...
    def getArgument(self) -> float: ...
    def getField(self) -> 'ComplexField': ...
    def getImaginary(self) -> float: ...
    def getReal(self) -> float: ...
    def hashCode(self) -> int: ...
    def isInfinite(self) -> bool: ...
    def isNaN(self) -> bool: ...
    def log(self) -> 'Complex': ...
    @typing.overload
    def multiply(self, double: float) -> 'Complex': ...
    @typing.overload
    def multiply(self, complex: 'Complex') -> 'Complex': ...
    @typing.overload
    def multiply(self, int: int) -> 'Complex': ...
    def negate(self) -> 'Complex': ...
    def nthRoot(self, int: int) -> java.util.List['Complex']: ...
    @typing.overload
    def pow(self, double: float) -> 'Complex': ...
    @typing.overload
    def pow(self, complex: 'Complex') -> 'Complex': ...
    def reciprocal(self) -> 'Complex': ...
    def sin(self) -> 'Complex': ...
    def sinh(self) -> 'Complex': ...
    def sqrt(self) -> 'Complex': ...
    def sqrt1z(self) -> 'Complex': ...
    @typing.overload
    def subtract(self, double: float) -> 'Complex': ...
    @typing.overload
    def subtract(self, complex: 'Complex') -> 'Complex': ...
    def tan(self) -> 'Complex': ...
    def tanh(self) -> 'Complex': ...
    def toString(self) -> str: ...
    @typing.overload
    @staticmethod
    def valueOf(double: float) -> 'Complex': ...
    @typing.overload
    @staticmethod
    def valueOf(double: float, double2: float) -> 'Complex': ...

class ComplexField(fr.cnes.sirius.patrius.math.Field[Complex], java.io.Serializable):
    """
    public final class ComplexField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.Field`<:class:`~fr.cnes.sirius.patrius.math.complex.Complex`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Representation of the complex numbers field.
    
        This class is a singleton.
    
        Since:
            2.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.complex.Complex`, :meth:`~serialized`
    """
    @staticmethod
    def getInstance() -> 'ComplexField':
        """
            Get the unique instance.
        
            Returns:
                the unique instance
        
        
        """
        ...
    def getOne(self) -> Complex:
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
    def getRuntimeClass(self) -> typing.Type[fr.cnes.sirius.patrius.math.FieldElement[Complex]]: ...
    def getZero(self) -> Complex:
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

class ComplexFormat:
    """
    public class ComplexFormat extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Formats a Complex number in cartesian format "Re(c) + Im(c)i". 'i' can be replaced with 'j' (or anything else), and the
        number format for both real and imaginary parts can be configured.
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, string: str, numberFormat: java.text.NumberFormat): ...
    @typing.overload
    def __init__(self, string: str, numberFormat: java.text.NumberFormat, numberFormat2: java.text.NumberFormat): ...
    @typing.overload
    def __init__(self, numberFormat: java.text.NumberFormat): ...
    @typing.overload
    def __init__(self, numberFormat: java.text.NumberFormat, numberFormat2: java.text.NumberFormat): ...
    @typing.overload
    def format(self, complex: Complex) -> str:
        """
            This method calls :meth:`~fr.cnes.sirius.patrius.math.complex.ComplexFormat.format`.
        
            Parameters:
                c (:class:`~fr.cnes.sirius.patrius.math.complex.Complex`): Complex object to format.
        
            Returns:
                A formatted number in the form "Re(c) + Im(c)i".
        
            This method calls :meth:`~fr.cnes.sirius.patrius.math.complex.ComplexFormat.format`.
        
            Parameters:
                c (`Double <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>`): Double object to format.
        
            Returns:
                A formatted number.
        
        """
        ...
    @typing.overload
    def format(self, double: float) -> str: ...
    @typing.overload
    def format(self, complex: Complex, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer:
        """
            Formats a :class:`~fr.cnes.sirius.patrius.math.complex.Complex` object to produce a string.
        
            Parameters:
                complex (:class:`~fr.cnes.sirius.patrius.math.complex.Complex`): the object to format.
                toAppendTo (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): where the text is to be appended
                pos (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
        
            Returns:
                the value passed in as toAppendTo.
        
            Formats a object to produce a string. :code:`obj` must be either a :class:`~fr.cnes.sirius.patrius.math.complex.Complex`
            object or a `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Number.html?is-external=true>` object. Any other
            type of object will result in an `null
            <http://docs.oracle.com/javase/8/docs/api/java/lang/IllegalArgumentException.html?is-external=true>` being thrown.
        
            Parameters:
                obj (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the object to format.
                toAppendTo (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): where the text is to be appended
                pos (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
        
            Returns:
                the value passed in as toAppendTo.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: is :code:`obj` is not a valid type.
        
            Also see:
                `null
                <http://docs.oracle.com/javase/8/docs/api/java/text/Format.html?is-external=true#format-java.lang.Object-java.lang.StringBuffer-java.text.FieldPosition->`
        
        
        """
        ...
    @typing.overload
    def format(self, object: typing.Any, stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer: ...
    @staticmethod
    def getAvailableLocales() -> typing.MutableSequence[java.util.Locale]:
        """
            Get the set of locales for which complex formats are available.
        
            This is the same set as the `null
            <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>` set.
        
            Returns:
                available complex format locales.
        
        
        """
        ...
    def getImaginaryCharacter(self) -> str:
        """
            Access the imaginaryCharacter.
        
            Returns:
                the imaginaryCharacter.
        
        
        """
        ...
    def getImaginaryFormat(self) -> java.text.NumberFormat:
        """
            Access the imaginaryFormat.
        
            Returns:
                the imaginaryFormat.
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getInstance() -> 'ComplexFormat':
        """
            Returns the default complex format for the current locale.
        
            Returns:
                the default complex format.
        
        """
        ...
    @typing.overload
    @staticmethod
    def getInstance(string: str, locale: java.util.Locale) -> 'ComplexFormat':
        """
            Returns the default complex format for the given locale.
        
            Parameters:
                locale (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the specific locale used by the format.
                imaginaryCharacter (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): Imaginary character.
        
            Returns:
                the complex format specific to the given locale.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`imaginaryCharacter` is :code:`null`.
                :class:`~fr.cnes.sirius.patrius.math.exception.NoDataException`: if :code:`imaginaryCharacter` is an empty string.
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getInstance(locale: java.util.Locale) -> 'ComplexFormat':
        """
            Returns the default complex format for the given locale.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): the specific locale used by the format.
        
            Returns:
                the complex format specific to the given locale.
        
        """
        ...
    def getRealFormat(self) -> java.text.NumberFormat:
        """
            Access the realFormat.
        
            Returns:
                the realFormat.
        
        
        """
        ...
    @typing.overload
    def parse(self, string: str) -> Complex:
        """
            Parses a string to produce a :class:`~fr.cnes.sirius.patrius.math.complex.Complex` object.
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse.
        
            Returns:
                the parsed :class:`~fr.cnes.sirius.patrius.math.complex.Complex` object.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathParseException`: if the beginning of the specified string cannot be parsed.
        
        """
        ...
    @typing.overload
    def parse(self, string: str, parsePosition: java.text.ParsePosition) -> Complex:
        """
            Parses a string to produce a :class:`~fr.cnes.sirius.patrius.math.complex.Complex` object.
        
            Parameters:
                source (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to parse
                pos (`ParsePosition <http://docs.oracle.com/javase/8/docs/api/java/text/ParsePosition.html?is-external=true>`): input/ouput parsing parameter.
        
            Returns:
                the parsed :class:`~fr.cnes.sirius.patrius.math.complex.Complex` object.
        
        
        """
        ...

class ComplexUtils:
    """
    public final class ComplexUtils extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Static implementations of common :class:`~fr.cnes.sirius.patrius.math.complex.Complex` utilities functions.
    """
    @staticmethod
    def convertToComplex(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[Complex]:
        """
            Convert an array of primitive doubles to an array of :code:`Complex` objects.
        
            Parameters:
                real (double[]): Array of numbers to be converted to their :code:`Complex` equivalent.
        
            Returns:
                an array of :code:`Complex` objects.
        
            Since:
                3.1
        
        
        """
        ...
    @staticmethod
    def polar2Complex(double: float, double2: float) -> Complex:
        """
            Creates a complex number from the given polar representation.
        
            The value returned is :code:`r·e :sup:`i·theta``, computed as :code:`r·cos(theta) + r·sin(theta)i`
        
            If either :code:`r` or :code:`theta` is NaN, or :code:`theta` is infinite,
            :meth:`~fr.cnes.sirius.patrius.math.complex.Complex.NaN` is returned.
        
            If :code:`r` is infinite and :code:`theta` is finite, infinite or NaN values may be returned in parts of the result,
            following the rules for double arithmetic.
        
            .. code-block: java
            
            
             Examples:
             
             polar2Complex(INFINITY, π/4) = INFINITY + INFINITY i
             polar2Complex(INFINITY, 0) = INFINITY + NaN i
             polar2Complex(INFINITY, -π/4) = INFINITY - INFINITY i
             polar2Complex(INFINITY, 5π/4) = -INFINITY - INFINITY i 
             
        
            Parameters:
                r (double): the modulus of the complex number to create
                theta (double): the argument of the complex number to create
        
            Returns:
                :code:`r·e :sup:`i·theta``
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if :code:`r` is negative.
        
            Since:
                1.1
        
        
        """
        ...

class Quaternion(java.io.Serializable):
    IDENTITY: typing.ClassVar['Quaternion'] = ...
    ZERO: typing.ClassVar['Quaternion'] = ...
    I: typing.ClassVar['Quaternion'] = ...
    J: typing.ClassVar['Quaternion'] = ...
    K: typing.ClassVar['Quaternion'] = ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def add(self, quaternion: 'Quaternion') -> 'Quaternion': ...
    @typing.overload
    @staticmethod
    def add(quaternion: 'Quaternion', quaternion2: 'Quaternion') -> 'Quaternion': ...
    @typing.overload
    def dotProduct(self, quaternion: 'Quaternion') -> float: ...
    @typing.overload
    @staticmethod
    def dotProduct(quaternion: 'Quaternion', quaternion2: 'Quaternion') -> float: ...
    @typing.overload
    def equals(self, quaternion: 'Quaternion', double: float) -> bool: ...
    @typing.overload
    def equals(self, object: typing.Any) -> bool: ...
    def getConjugate(self) -> 'Quaternion': ...
    def getInverse(self) -> 'Quaternion': ...
    def getNorm(self) -> float: ...
    def getPositivePolarForm(self) -> 'Quaternion': ...
    def getQ0(self) -> float: ...
    def getQ1(self) -> float: ...
    def getQ2(self) -> float: ...
    def getQ3(self) -> float: ...
    def getScalarPart(self) -> float: ...
    def getVectorPart(self) -> typing.MutableSequence[float]: ...
    def hashCode(self) -> int: ...
    def isPureQuaternion(self, double: float) -> bool: ...
    def isUnitQuaternion(self, double: float) -> bool: ...
    @typing.overload
    def multiply(self, double: float) -> 'Quaternion': ...
    @typing.overload
    def multiply(self, quaternion: 'Quaternion') -> 'Quaternion': ...
    @typing.overload
    @staticmethod
    def multiply(quaternion: 'Quaternion', quaternion2: 'Quaternion') -> 'Quaternion': ...
    def normalize(self) -> 'Quaternion': ...
    @typing.overload
    def subtract(self, quaternion: 'Quaternion') -> 'Quaternion': ...
    @typing.overload
    @staticmethod
    def subtract(quaternion: 'Quaternion', quaternion2: 'Quaternion') -> 'Quaternion': ...
    def toString(self) -> str: ...

class RootsOfUnity(java.io.Serializable):
    def __init__(self): ...
    def computeRoots(self, int: int) -> None: ...
    def getImaginary(self, int: int) -> float: ...
    def getNumberOfRoots(self) -> int: ...
    def getReal(self, int: int) -> float: ...
    def isCounterClockWise(self) -> bool: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.complex")``.

    Complex: typing.Type[Complex]
    ComplexField: typing.Type[ComplexField]
    ComplexFormat: typing.Type[ComplexFormat]
    ComplexUtils: typing.Type[ComplexUtils]
    Quaternion: typing.Type[Quaternion]
    RootsOfUnity: typing.Type[RootsOfUnity]
