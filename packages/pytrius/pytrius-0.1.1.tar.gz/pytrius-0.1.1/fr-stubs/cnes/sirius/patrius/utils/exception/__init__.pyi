
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.exception.util
import java.lang
import java.text
import java.util
import typing



class PatriusException(java.lang.Exception):
    """
    public class PatriusException extends `Exception <http://docs.oracle.com/javase/8/docs/api/java/lang/Exception.html?is-external=true>`
    
        This class is the base class for all specific exceptions thrown by the Patrius classes.
    
        When the Patrius classes throw exceptions that are specific to the package, these exceptions are always subclasses of
        OrekitException. When exceptions that are already covered by the standard java API should be thrown, like
        ArrayIndexOutOfBoundsException or InvalidParameterException, these standard exceptions are thrown rather than the
        commons-math specific ones.
    
        This class also provides utility methods to throw some standard java exceptions with localized messages.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, exceptionContextProvider: typing.Union[fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider, typing.Callable]): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, throwable: java.lang.Throwable): ...
    @typing.overload
    def __init__(self, patriusException: 'PatriusException'): ...
    @typing.overload
    def __init__(self, throwable: java.lang.Throwable, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    @staticmethod
    def createIllegalArgumentException(localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any) -> java.lang.IllegalArgumentException: ...
    @staticmethod
    def createIllegalStateException(localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any) -> java.lang.IllegalStateException: ...
    @staticmethod
    def createInternalError(throwable: java.lang.Throwable) -> java.lang.RuntimeException:
        """
            Create an `null <http://docs.oracle.com/javase/8/docs/api/java/lang/RuntimeException.html?is-external=true>` for an
            internal error.
        
            Parameters:
                cause (`Throwable <http://docs.oracle.com/javase/8/docs/api/java/lang/Throwable.html?is-external=true>`): underlying cause
        
            Returns:
                an `null <http://docs.oracle.com/javase/8/docs/api/java/lang/RuntimeException.html?is-external=true>` for an internal
                error
        
        
        """
        ...
    @staticmethod
    def createParseException(localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any) -> java.text.ParseException: ...
    def getLocalizedMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @typing.overload
    def getMessage(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @typing.overload
    def getMessage(self, locale: java.util.Locale) -> str:
        """
            Gets the message in a specified locale.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): Locale in which the message should be translated
        
            Returns:
                localized message
        
            Since:
                5.0
        
        """
        ...
    def getParts(self) -> typing.MutableSequence[typing.Any]:
        """
            Get the variable parts of the error message.
        
            Returns:
                a copy of the variable parts of the error message
        
            Since:
                5.1
        
        
        """
        ...
    def getSpecifier(self) -> fr.cnes.sirius.patrius.math.exception.util.Localizable:
        """
            Get the localizable specifier of the error message.
        
            Returns:
                localizable specifier of the error message
        
            Since:
                5.1
        
        
        """
        ...

class PatriusExceptionWrapper(java.lang.RuntimeException):
    """
    public class PatriusExceptionWrapper extends `RuntimeException <http://docs.oracle.com/javase/8/docs/api/java/lang/RuntimeException.html?is-external=true>`
    
        This class allows to wrap :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException` instances in
        :code:`RuntimeException`.
    
        Wrapping :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException` instances is useful when a low level method
        throws one such exception and this method must be called from another one which does not allow this exception. Typical
        examples are propagation methods that are used inside Apache Commons optimizers, integrators or solvers.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, patriusException: PatriusException): ...
    def getException(self) -> PatriusException:
        """
            Get the wrapped exception.
        
            Returns:
                wrapped exception
        
        
        """
        ...

class PatriusRuntimeException(java.lang.RuntimeException):
    """
    public class PatriusRuntimeException extends `RuntimeException <http://docs.oracle.com/javase/8/docs/api/java/lang/RuntimeException.html?is-external=true>`
    
        Orekit Runtime Exception.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, throwable: java.lang.Throwable): ...
    @typing.overload
    def __init__(self, string: str, throwable: java.lang.Throwable): ...

class FrameAncestorException(PatriusException):
    """
    public class FrameAncestorException extends :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
    
        This class is the base class for exception thrown by the
        :meth:`~fr.cnes.sirius.patrius.frames.UpdatableFrame.updateTransform` method.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...

class PropagationException(PatriusException):
    """
    public class PropagationException extends :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
    
        This class is the base class for all specific exceptions thrown by during the propagation computation.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, exceptionContextProvider: typing.Union[fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider, typing.Callable]): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    @typing.overload
    def __init__(self, patriusException: PatriusException): ...
    @typing.overload
    def __init__(self, throwable: java.lang.Throwable, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    @typing.overload
    @staticmethod
    def unwrap(exceptionContextProvider: typing.Union[fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider, typing.Callable]) -> 'PropagationException':
        """
            Recover a PropagationException, possibly embedded in a
            :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`.
        
            If the :code:`OrekitException` does not embed a PropagationException, a new one will be created.
        
            Parameters:
                oe (:class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`): OrekitException to analyze
        
            Returns:
                a (possibly embedded) PropagationException
        
            Recover a PropagationException, possibly embedded in an
            :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`.
        
            If the :code:`ExceptionContextProvider` does not embed a PropagationException, a new one will be created.
        
            Parameters:
                provider (:class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`): ExceptionContextProvider to analyze
        
            Returns:
                a (possibly embedded) PropagationException
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def unwrap(patriusException: PatriusException) -> 'PropagationException': ...

class TimeStampedCacheException(PatriusException):
    """
    public class TimeStampedCacheException extends :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
    
        This class is the base class for all specific exceptions thrown by during the
        :class:`~fr.cnes.sirius.patrius.time.TimeStampedCache`.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, exceptionContextProvider: typing.Union[fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider, typing.Callable]): ...
    @typing.overload
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    @typing.overload
    def __init__(self, patriusException: PatriusException): ...
    @typing.overload
    def __init__(self, throwable: java.lang.Throwable, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...
    @typing.overload
    @staticmethod
    def unwrap(exceptionContextProvider: typing.Union[fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider, typing.Callable]) -> 'TimeStampedCacheException':
        """
            Recover a PropagationException, possibly embedded in a
            :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`.
        
            If the :code:`OrekitException` does not embed a PropagationException, a new one will be created.
        
            Parameters:
                oe (:class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`): OrekitException to analyze
        
            Returns:
                a (possibly embedded) PropagationException
        
            Recover a PropagationException, possibly embedded in an
            :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`.
        
            If the :code:`ExceptionContextProvider` does not embed a PropagationException, a new one will be created.
        
            Parameters:
                provider (:class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContextProvider`): ExceptionContextProvider to analyze
        
            Returns:
                a (possibly embedded) PropagationException
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def unwrap(patriusException: PatriusException) -> 'TimeStampedCacheException': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.utils.exception")``.

    FrameAncestorException: typing.Type[FrameAncestorException]
    PatriusException: typing.Type[PatriusException]
    PatriusExceptionWrapper: typing.Type[PatriusExceptionWrapper]
    PatriusRuntimeException: typing.Type[PatriusRuntimeException]
    PropagationException: typing.Type[PropagationException]
    TimeStampedCacheException: typing.Type[TimeStampedCacheException]
