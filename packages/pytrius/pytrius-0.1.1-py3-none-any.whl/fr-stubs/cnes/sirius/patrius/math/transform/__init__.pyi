
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.complex
import java.io
import java.lang
import jpype
import typing



class DctNormalization(java.lang.Enum['DctNormalization']):
    """
    public enum DctNormalization extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.transform.DctNormalization`>
    
        This enumeration defines the various types of normalizations that can be applied to discrete cosine transforms (DCT).
        The exact definition of these normalizations is detailed below.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.transform.FastCosineTransformer`
    """
    STANDARD_DCT_I: typing.ClassVar['DctNormalization'] = ...
    ORTHOGONAL_DCT_I: typing.ClassVar['DctNormalization'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'DctNormalization':
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
    def values() -> typing.MutableSequence['DctNormalization']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (DctNormalization c : DctNormalization.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class DftNormalization(java.lang.Enum['DftNormalization']):
    """
    public enum DftNormalization extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.transform.DftNormalization`>
    
        This enumeration defines the various types of normalizations that can be applied to discrete Fourier transforms (DFT).
        The exact definition of these normalizations is detailed below.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.transform.FastFourierTransformer`
    """
    STANDARD: typing.ClassVar['DftNormalization'] = ...
    UNITARY: typing.ClassVar['DftNormalization'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'DftNormalization':
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
    def values() -> typing.MutableSequence['DftNormalization']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (DftNormalization c : DftNormalization.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class DstNormalization(java.lang.Enum['DstNormalization']):
    """
    public enum DstNormalization extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.transform.DstNormalization`>
    
        This enumeration defines the various types of normalizations that can be applied to discrete sine transforms (DST). The
        exact definition of these normalizations is detailed below.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.transform.FastSineTransformer`
    """
    STANDARD_DST_I: typing.ClassVar['DstNormalization'] = ...
    ORTHOGONAL_DST_I: typing.ClassVar['DstNormalization'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'DstNormalization':
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
    def values() -> typing.MutableSequence['DstNormalization']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (DstNormalization c : DstNormalization.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class IFastFourierTransformer:
    """
    public interface IFastFourierTransformer
    
        This interface gathers all the FFT algorithms of this library.
    
        Since:
            2.3
    """
    @typing.overload
    def transform(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], transformType: 'TransformType') -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]:
        """
            Returns the (forward, inverse) transform of the specified real data set.
        
            Parameters:
                f (double[]): the real data array to be transformed
                type (:class:`~fr.cnes.sirius.patrius.math.transform.TransformType`): the type of transform (forward, inverse) to be performed
        
            Returns:
                the complex transformed array
        
            Returns the (forward, inverse) transform of the specified complex data set.
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.complex.Complex`[]): the complex data array to be transformed
                type (:class:`~fr.cnes.sirius.patrius.math.transform.TransformType`): the type of transform (forward, inverse) to be performed
        
            Returns:
                the complex transformed array
        
            Returns the (forward, inverse) transform of the specified real function, sampled on the specified interval.
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): the function to be sampled and transformed
                min (double): the (inclusive) lower bound for the interval
                max (double): the (exclusive) upper bound for the interval
                n (int): the number of sample points
                type (:class:`~fr.cnes.sirius.patrius.math.transform.TransformType`): the type of transform (forward, inverse) to be performed
        
            Returns:
                the complex transformed array
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooLargeException`: if the lower bound is greater than, or equal to the upper bound
                :class:`~fr.cnes.sirius.patrius.math.exception.NotStrictlyPositiveException`: if the number of sample points :code:`n` is negative
        
        
        """
        ...
    @typing.overload
    def transform(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, int: int, transformType: 'TransformType') -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]: ...
    @typing.overload
    def transform(self, complexArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.complex.Complex], jpype.JArray], transformType: 'TransformType') -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]: ...

class RealTransformer:
    """
    public interface RealTransformer
    
        Interface for one-dimensional data sets transformations producing real results.
    
        Such transforms include :class:`~fr.cnes.sirius.patrius.math.transform.FastSineTransformer`,
        :class:`~fr.cnes.sirius.patrius.math.transform.FastCosineTransformer` or
        :class:`~fr.cnes.sirius.patrius.math.transform.FastHadamardTransformer`.
        :class:`~fr.cnes.sirius.patrius.math.transform.FastFourierTransformer` is of a different kind and does not implement
        this interface since it produces :class:`~fr.cnes.sirius.patrius.math.complex.Complex` results instead of real ones.
    
        Since:
            2.0
    """
    @typing.overload
    def transform(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], transformType: 'TransformType') -> typing.MutableSequence[float]:
        """
            Returns the (forward, inverse) transform of the specified real data set.
        
            Parameters:
                f (double[]): the real data array to be transformed (signal)
                type (:class:`~fr.cnes.sirius.patrius.math.transform.TransformType`): the type of transform (forward, inverse) to be performed
        
            Returns:
                the real transformed array (spectrum)
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array cannot be transformed with the given type (this may be for example due to array size, which is constrained
                    in some transforms)
        
            Returns the (forward, inverse) transform of the specified real function, sampled on the specified interval.
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): the function to be sampled and transformed
                min (double): the (inclusive) lower bound for the interval
                max (double): the (exclusive) upper bound for the interval
                n (int): the number of sample points
                type (:class:`~fr.cnes.sirius.patrius.math.transform.TransformType`): the type of transform (forward, inverse) to be performed
        
            Returns:
                the real transformed array
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NonMonotonicSequenceException`: if the lower bound is greater than, or equal to the upper bound
                :class:`~fr.cnes.sirius.patrius.math.exception.NotStrictlyPositiveException`: if the number of sample points is negative
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the sample cannot be transformed with the given type (this may be for example due to sample size, which is
                    constrained in some transforms)
        
        
        """
        ...
    @typing.overload
    def transform(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, int: int, transformType: 'TransformType') -> typing.MutableSequence[float]: ...

class TransformType(java.lang.Enum['TransformType']):
    """
    public enum TransformType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.transform.TransformType`>
    
        This enumeration defines the type of transform which is to be computed.
    
        Since:
            3.0
    """
    FORWARD: typing.ClassVar['TransformType'] = ...
    INVERSE: typing.ClassVar['TransformType'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'TransformType':
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
    def values() -> typing.MutableSequence['TransformType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (TransformType c : TransformType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class TransformUtils:
    """
    public final class TransformUtils extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Useful functions for the implementation of various transforms.
    
        Since:
            3.0
    """
    @staticmethod
    def createComplexArray(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]:
        """
            Builds a new array of :class:`~fr.cnes.sirius.patrius.math.complex.Complex` from the specified two dimensional array of
            real and imaginary parts. In the returned array :code:`dataC`, the data is laid out as follows
        
              - :code:`dataC[i].getReal() = dataRI[0][i]`,
              - :code:`dataC[i].getImaginary() = dataRI[1][i]`.
        
        
            Parameters:
                dataRI (double[][]): the array of real and imaginary parts to be transformed
        
            Returns:
                an array of :class:`~fr.cnes.sirius.patrius.math.complex.Complex` with specified real and imaginary parts.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the number of rows of the specified array is not two, or the array is not rectangular
        
        
        """
        ...
    @staticmethod
    def createRealImaginaryArray(complexArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.complex.Complex], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Builds a new two dimensional array of :code:`double` filled with the real and imaginary parts of the specified
            :class:`~fr.cnes.sirius.patrius.math.complex.Complex` numbers. In the returned array :code:`dataRI`, the data is laid
            out as follows
        
              - :code:`dataRI[0][i] = dataC[i].getReal()`,
              - :code:`dataRI[1][i] = dataC[i].getImaginary()`.
        
        
            Parameters:
                dataC (:class:`~fr.cnes.sirius.patrius.math.complex.Complex`[]): the array of :class:`~fr.cnes.sirius.patrius.math.complex.Complex` data to be transformed
        
            Returns:
                a two dimensional array filled with the real and imaginary parts of the specified complex input
        
        
        """
        ...
    @staticmethod
    def exactLog2(int: int) -> int:
        """
            Returns the base-2 logarithm of the specified :code:`int`. Throws an exception if :code:`n` is not a power of two.
        
            Parameters:
                n (int): the :code:`int` whose base-2 logarithm is to be evaluated
        
            Returns:
                the base-2 logarithm of :code:`n`
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if :code:`n` is not a power of two
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def scaleArray(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> typing.MutableSequence[float]:
        """
            Multiply every component in the given real array by the given real number. The change is made in place.
        
            Parameters:
                f (double[]): the real array to be scaled
                d (double): the real scaling coefficient
        
            Returns:
                a reference to the scaled array
        
            Multiply every component in the given complex array by the given real number. The change is made in place.
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.complex.Complex`[]): the complex array to be scaled
                d (double): the real scaling coefficient
        
            Returns:
                a reference to the scaled array
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def scaleArray(complexArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.complex.Complex], jpype.JArray], double: float) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]: ...

class AbstractFastFourierTransformer(IFastFourierTransformer):
    """
    public abstract class AbstractFastFourierTransformer extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.transform.IFastFourierTransformer`
    
        This abstract class is common to all FFT algorithms of this library.
    
        Since:
            2.3
    """
    def __init__(self, dftNormalization: DftNormalization): ...
    def getNormalization(self) -> DftNormalization:
        """
            Gets the private attribute normalization.
        
            Returns:
                normalization : an enum DftNormalization equal to STANDARD or UNITARY
        
        
        """
        ...
    @typing.overload
    def transform(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], transformType: TransformType) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]:
        """
            Returns the (forward, inverse) transform of the specified real function, sampled on the specified interval.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.transform.IFastFourierTransformer.transform` in
                interface :class:`~fr.cnes.sirius.patrius.math.transform.IFastFourierTransformer`
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): the function to be sampled and transformed
                min (double): the (inclusive) lower bound for the interval
                max (double): the (exclusive) upper bound for the interval
                n (int): the number of sample points
                type (:class:`~fr.cnes.sirius.patrius.math.transform.TransformType`): the type of transform (forward, inverse) to be performed
        
            Returns:
                the complex transformed array
        
        
        """
        ...
    @typing.overload
    def transform(self, complexArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.complex.Complex], jpype.JArray], transformType: TransformType) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]: ...
    @typing.overload
    def transform(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, int: int, transformType: TransformType) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]: ...

class FastCosineTransformer(RealTransformer, java.io.Serializable):
    def __init__(self, dctNormalization: DctNormalization): ...
    @typing.overload
    def transform(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], transformType: TransformType) -> typing.MutableSequence[float]: ...
    @typing.overload
    def transform(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, int: int, transformType: TransformType) -> typing.MutableSequence[float]: ...

class FastHadamardTransformer(RealTransformer, java.io.Serializable):
    def __init__(self): ...
    @typing.overload
    def transform(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], transformType: TransformType) -> typing.MutableSequence[float]: ...
    @typing.overload
    def transform(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, int: int, transformType: TransformType) -> typing.MutableSequence[float]: ...
    @typing.overload
    def transform(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> typing.MutableSequence[int]: ...

class FastSineTransformer(RealTransformer, java.io.Serializable):
    def __init__(self, dstNormalization: DstNormalization): ...
    @typing.overload
    def transform(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], transformType: TransformType) -> typing.MutableSequence[float]: ...
    @typing.overload
    def transform(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, int: int, transformType: TransformType) -> typing.MutableSequence[float]: ...

class FastFourierTransformer(AbstractFastFourierTransformer):
    """
    public class FastFourierTransformer extends :class:`~fr.cnes.sirius.patrius.math.transform.AbstractFastFourierTransformer`
    
        This class allows the computation of a Fast Fourier Transform for all kind (odd or powers of two) orders.
    
        Since:
            2.3
    """
    def __init__(self, dftNormalization: DftNormalization): ...
    @typing.overload
    def transform(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, int: int, transformType: TransformType) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]: ...
    @typing.overload
    def transform(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], transformType: TransformType) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]:
        """
            Returns the (forward, inverse) transform of the specified real data set.
        
            Parameters:
                f (double[]): the real data array to be transformed
                type (:class:`~fr.cnes.sirius.patrius.math.transform.TransformType`): the type of transform (forward, inverse) to be performed
        
            Returns:
                the complex transformed array
        
            Returns the (forward, inverse) transform of the specified complex data set.
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.complex.Complex`[]): the complex data array to be transformed
                type (:class:`~fr.cnes.sirius.patrius.math.transform.TransformType`): the type of transform (forward, inverse) to be performed
        
            Returns:
                the complex transformed array
        
        
        """
        ...
    @typing.overload
    def transform(self, complexArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.complex.Complex], jpype.JArray], transformType: TransformType) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.transform")``.

    AbstractFastFourierTransformer: typing.Type[AbstractFastFourierTransformer]
    DctNormalization: typing.Type[DctNormalization]
    DftNormalization: typing.Type[DftNormalization]
    DstNormalization: typing.Type[DstNormalization]
    FastCosineTransformer: typing.Type[FastCosineTransformer]
    FastFourierTransformer: typing.Type[FastFourierTransformer]
    FastHadamardTransformer: typing.Type[FastHadamardTransformer]
    FastSineTransformer: typing.Type[FastSineTransformer]
    IFastFourierTransformer: typing.Type[IFastFourierTransformer]
    RealTransformer: typing.Type[RealTransformer]
    TransformType: typing.Type[TransformType]
    TransformUtils: typing.Type[TransformUtils]
