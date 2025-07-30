
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import _jpype
import fr.cnes.sirius.patrius.math.exception.util
import fr.cnes.sirius.patrius.math.util
import java.lang
import jpype
import typing



class MathArithmeticException(java.lang.ArithmeticException, fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider):
    """
    public class MathArithmeticException extends `ArithmeticException <http://docs.oracle.com/javase/8/docs/api/java/lang/ArithmeticException.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`
    
        Base class for arithmetic exceptions. It is used for all the exceptions that have the semantics of the standard `null
        <http://docs.oracle.com/javase/8/docs/api/java/lang/ArithmeticException.html?is-external=true>`, but must also provide a
        localized message.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    def getContext(self) -> fr.cnes.sirius.patrius.math.exception.util.ExceptionContext:
        """
            Gets a reference to the "rich context" data structure that allows to customize error messages and store key, value pairs
            in exceptions.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider.getContext` in
                interface :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`
        
            Returns:
                a reference to the exception context.
        
        
        """
        ...
    def getLocalizedMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class MathIllegalArgumentException(java.lang.IllegalArgumentException, fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider):
    """
    public class MathIllegalArgumentException extends `IllegalArgumentException <http://docs.oracle.com/javase/8/docs/api/java/lang/IllegalArgumentException.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`
    
        Base class for all preconditions violation exceptions. In most cases, this class should not be instantiated directly: it
        should serve as a base class to create all the exceptions that have the semantics of the standard `null
        <http://docs.oracle.com/javase/8/docs/api/java/lang/IllegalArgumentException.html?is-external=true>`.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    def getContext(self) -> fr.cnes.sirius.patrius.math.exception.util.ExceptionContext:
        """
            Gets a reference to the "rich context" data structure that allows to customize error messages and store key, value pairs
            in exceptions.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider.getContext` in
                interface :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`
        
            Returns:
                a reference to the exception context.
        
        
        """
        ...
    def getLocalizedMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class MathIllegalStateException(java.lang.IllegalStateException, fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider):
    """
    public class MathIllegalStateException extends `IllegalStateException <http://docs.oracle.com/javase/8/docs/api/java/lang/IllegalStateException.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`
    
        Base class for all exceptions that signal a mismatch between the current state and the user's expectations.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    @typing.overload
    def __init__(self, throwable: java.lang.Throwable, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    def getContext(self) -> fr.cnes.sirius.patrius.math.exception.util.ExceptionContext:
        """
            Gets a reference to the "rich context" data structure that allows to customize error messages and store key, value pairs
            in exceptions.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider.getContext` in
                interface :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`
        
            Returns:
                a reference to the exception context.
        
        
        """
        ...
    def getLocalizedMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class MathRuntimeException(java.lang.RuntimeException, fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider):
    """
    public class MathRuntimeException extends `RuntimeException <http://docs.oracle.com/javase/8/docs/api/java/lang/RuntimeException.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`
    
        As of release 4.0, all exceptions thrown by the Commons Math code (except
        :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`) inherit from this class. In most cases, this
        class should not be instantiated directly: it should serve as a base class for implementing exception classes that
        describe a specific "problem".
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    def getContext(self) -> fr.cnes.sirius.patrius.math.exception.util.ExceptionContext:
        """
            Gets a reference to the "rich context" data structure that allows to customize error messages and store key, value pairs
            in exceptions.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider.getContext` in
                interface :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`
        
            Returns:
                a reference to the exception context.
        
        
        """
        ...
    def getLocalizedMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class MathUnsupportedOperationException(java.lang.UnsupportedOperationException, fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider):
    """
    public class MathUnsupportedOperationException extends `UnsupportedOperationException <http://docs.oracle.com/javase/8/docs/api/java/lang/UnsupportedOperationException.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`
    
        Base class for all unsupported features. It is used for all the exceptions that have the semantics of the standard `null
        <http://docs.oracle.com/javase/8/docs/api/java/lang/UnsupportedOperationException.html?is-external=true>`, but must also
        provide a localized message.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    def getContext(self) -> fr.cnes.sirius.patrius.math.exception.util.ExceptionContext:
        """
            Gets a reference to the "rich context" data structure that allows to customize error messages and store key, value pairs
            in exceptions.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider.getContext` in
                interface :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`
        
            Returns:
                a reference to the exception context.
        
        
        """
        ...
    def getLocalizedMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class ConvergenceException(MathIllegalStateException):
    """
    public class ConvergenceException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`
    
        Error thrown when a numerical computation can not be performed because the numerical result failed to converge to a
        finite value.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...

class MathIllegalNumberException(MathIllegalArgumentException):
    """
    public class MathIllegalNumberException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`
    
        Base class for exceptions raised by a wrong number. This class is not intended to be instantiated directly: it should
        serve as a base class to create all the exceptions that are raised because some precondition is violated by a number
        argument.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    def getArgument(self) -> java.lang.Number:
        """
        
            Returns:
                the requested value.
        
        
        """
        ...

class MathInternalError(MathIllegalStateException):
    """
    public class MathInternalError extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`
    
        Exception triggered when something that shouldn't happen does happen.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    @typing.overload
    def __init__(self, throwable: java.lang.Throwable): ...

class MathParseException(MathIllegalStateException):
    """
    public class MathParseException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`
    
        Class to signal parse failures.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, string: str, int: int): ...
    @typing.overload
    def __init__(self, string: str, int: int, class_: typing.Type[typing.Any]): ...

class MaxCountExceededException(MathIllegalStateException):
    """
    public class MaxCountExceededException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`
    
        Exception to be thrown when some counter maximum value is exceeded.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], *object: typing.Any): ...
    @typing.overload
    def __init__(self, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat]): ...
    def getMax(self) -> java.lang.Number:
        """
        
            Returns:
                the maximum number of evaluations.
        
        
        """
        ...

class MultiDimensionMismatchException(MathIllegalArgumentException):
    """
    public class MultiDimensionMismatchException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`
    
        Exception to be thrown when two sets of dimensions differ.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, integerArray: typing.Union[typing.List[int], jpype.JArray], integerArray2: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, integerArray: typing.Union[typing.List[int], jpype.JArray], integerArray2: typing.Union[typing.List[int], jpype.JArray]): ...
    def getExpectedDimension(self, int: int) -> int:
        """
        
            Parameters:
                index (int): Dimension index.
        
            Returns:
                the expected dimension stored at :code:`index`.
        
        
        """
        ...
    def getExpectedDimensions(self) -> typing.MutableSequence[int]:
        """
        
            Returns:
                an array containing the expected dimensions.
        
        
        """
        ...
    def getWrongDimension(self, int: int) -> int:
        """
        
            Parameters:
                index (int): Dimension index.
        
            Returns:
                the wrong dimension stored at :code:`index`.
        
        
        """
        ...
    def getWrongDimensions(self) -> typing.MutableSequence[int]:
        """
        
            Returns:
                an array containing the wrong dimensions.
        
        
        """
        ...

class NoBracketingException(MathIllegalArgumentException):
    """
    public class NoBracketingException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`
    
        Exception to be thrown when function values have the same sign at both ends of an interval.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, double: float, double2: float, double3: float, double4: float, *object: typing.Any): ...
    def getFHi(self) -> float:
        """
            Get the value at the higher end of the interval.
        
            Returns:
                the value at the higher end.
        
        
        """
        ...
    def getFLo(self) -> float:
        """
            Get the value at the lower end of the interval.
        
            Returns:
                the value at the lower end.
        
        
        """
        ...
    def getHi(self) -> float:
        """
            Get the higher end of the interval.
        
            Returns:
                the higher end.
        
        
        """
        ...
    def getLo(self) -> float:
        """
            Get the lower end of the interval.
        
            Returns:
                the lower end.
        
        
        """
        ...

class NoDataException(MathIllegalArgumentException):
    """
    public class NoDataException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`
    
        Exception to be thrown when the required data is missing.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable): ...

class NullArgumentException(MathIllegalArgumentException):
    """
    public class NullArgumentException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`
    
        All conditions checks that fail due to a :code:`null` argument must throw this exception. This class is meant to signal
        a precondition violation ("null is an illegal argument") and so does not extend the standard
        :code:`NullPointerException`. Propagation of :code:`NullPointerException` from within Commons-Math is construed to be a
        bug.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...

class DimensionMismatchException(MathIllegalNumberException):
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, int: int, int2: int): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, string: str, int: int, string2: str, int2: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    @typing.overload
    def __init__(self, string: str, int: int, int2: int): ...
    def getDimension(self) -> int: ...

class NonMonotonicSequenceException(MathIllegalNumberException):
    """
    public class NonMonotonicSequenceException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalNumberException`
    
        Exception to be thrown when the a sequence of values is not monotonically increasing or decreasing.
    
        Since:
            2.2 (name changed to "NonMonotonicSequenceException" in 3.0)
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], number2: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], int: int): ...
    @typing.overload
    def __init__(self, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], number2: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], int: int, orderDirection: fr.cnes.sirius.patrius.math.util.MathArrays.OrderDirection, boolean: bool): ...
    def getDirection(self) -> fr.cnes.sirius.patrius.math.util.MathArrays.OrderDirection:
        """
        
            Returns:
                the order direction.
        
        
        """
        ...
    def getIndex(self) -> int:
        """
            Get the index of the wrong value.
        
            Returns:
                the current index.
        
        
        """
        ...
    def getPrevious(self) -> java.lang.Number:
        """
        
            Returns:
                the previous value.
        
        
        """
        ...
    def getStrict(self) -> bool:
        """
        
            Returns:
                :code:`true` is the sequence should be strictly monotonic.
        
        
        """
        ...

class NotANumberException(MathIllegalNumberException):
    """
    public class NotANumberException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalNumberException`
    
        Exception to be thrown when a number is not a number.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...

class NotFiniteNumberException(MathIllegalNumberException):
    """
    public class NotFiniteNumberException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalNumberException`
    
        Exception to be thrown when a number is not finite.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], *object: typing.Any): ...
    @typing.overload
    def __init__(self, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], *object: typing.Any): ...

class NumberIsTooLargeException(MathIllegalNumberException):
    """
    public class NumberIsTooLargeException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalNumberException`
    
        Exception to be thrown when a number is too large.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], number2: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], boolean: bool): ...
    @typing.overload
    def __init__(self, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], number2: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], boolean: bool): ...
    def getBoundIsAllowed(self) -> bool:
        """
        
            Returns:
                :code:`true` if the maximum is included in the allowed range.
        
        
        """
        ...
    def getMax(self) -> java.lang.Number:
        """
        
            Returns:
                the maximum.
        
        
        """
        ...

class NumberIsTooSmallException(MathIllegalNumberException):
    """
    public class NumberIsTooSmallException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalNumberException`
    
        Exception to be thrown when a number is too small.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], number2: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], boolean: bool): ...
    @typing.overload
    def __init__(self, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], number2: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], boolean: bool): ...
    def getBoundIsAllowed(self) -> bool:
        """
        
            Returns:
                :code:`true` if the minimum is included in the allowed range.
        
        
        """
        ...
    def getMin(self) -> java.lang.Number:
        """
        
            Returns:
                the minimum.
        
        
        """
        ...

class OutOfRangeException(MathIllegalNumberException):
    """
    public class OutOfRangeException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalNumberException`
    
        Exception to be thrown when some argument is out of range.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], number2: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], number3: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat]): ...
    @typing.overload
    def __init__(self, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], number2: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat], number3: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat]): ...
    def getHi(self) -> java.lang.Number:
        """
        
            Returns:
                the higher bound.
        
        
        """
        ...
    def getLo(self) -> java.lang.Number:
        """
        
            Returns:
                the lower bound.
        
        
        """
        ...

class TooManyEvaluationsException(MaxCountExceededException):
    """
    public class TooManyEvaluationsException extends :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`
    
        Exception to be thrown when the maximal number of evaluations is exceeded.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat]): ...

class TooManyIterationsException(MaxCountExceededException):
    """
    public class TooManyIterationsException extends :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`
    
        Exception to be thrown when the maximal number of iterations is exceeded.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat]): ...

class ZeroException(MathIllegalNumberException):
    """
    public class ZeroException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalNumberException`
    
        Exception to be thrown when zero is provided where it is not allowed.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...

class NotPositiveException(NumberIsTooSmallException):
    """
    public class NotPositiveException extends :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`
    
        Exception to be thrown when the argument is negative.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat]): ...
    @typing.overload
    def __init__(self, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat]): ...

class NotStrictlyPositiveException(NumberIsTooSmallException):
    """
    public class NotStrictlyPositiveException extends :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`
    
        Exception to be thrown when the argument is negative.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat]): ...
    @typing.overload
    def __init__(self, number: typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat]): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.exception")``.

    ConvergenceException: typing.Type[ConvergenceException]
    DimensionMismatchException: typing.Type[DimensionMismatchException]
    MathArithmeticException: typing.Type[MathArithmeticException]
    MathIllegalArgumentException: typing.Type[MathIllegalArgumentException]
    MathIllegalNumberException: typing.Type[MathIllegalNumberException]
    MathIllegalStateException: typing.Type[MathIllegalStateException]
    MathInternalError: typing.Type[MathInternalError]
    MathParseException: typing.Type[MathParseException]
    MathRuntimeException: typing.Type[MathRuntimeException]
    MathUnsupportedOperationException: typing.Type[MathUnsupportedOperationException]
    MaxCountExceededException: typing.Type[MaxCountExceededException]
    MultiDimensionMismatchException: typing.Type[MultiDimensionMismatchException]
    NoBracketingException: typing.Type[NoBracketingException]
    NoDataException: typing.Type[NoDataException]
    NonMonotonicSequenceException: typing.Type[NonMonotonicSequenceException]
    NotANumberException: typing.Type[NotANumberException]
    NotFiniteNumberException: typing.Type[NotFiniteNumberException]
    NotPositiveException: typing.Type[NotPositiveException]
    NotStrictlyPositiveException: typing.Type[NotStrictlyPositiveException]
    NullArgumentException: typing.Type[NullArgumentException]
    NumberIsTooLargeException: typing.Type[NumberIsTooLargeException]
    NumberIsTooSmallException: typing.Type[NumberIsTooSmallException]
    OutOfRangeException: typing.Type[OutOfRangeException]
    TooManyEvaluationsException: typing.Type[TooManyEvaluationsException]
    TooManyIterationsException: typing.Type[TooManyIterationsException]
    ZeroException: typing.Type[ZeroException]
    util: fr.cnes.sirius.patrius.math.exception.util.__module_protocol__
