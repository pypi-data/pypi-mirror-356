
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.util
import jpype
import typing



class ArgUtils:
    """
    public final class ArgUtils extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Utility class for transforming the list of arguments passed to constructors of exceptions.
    """
    @staticmethod
    def flatten(objectArray: typing.Union[typing.List[typing.Any], jpype.JArray]) -> typing.MutableSequence[typing.Any]:
        """
            Transform a multidimensional array into a one-dimensional list.
        
            Parameters:
                array (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`[]): Array (possibly multidimensional).
        
            Returns:
                a list of all the :code:`Object` instances contained in :code:`array`.
        
        
        """
        ...

class ExceptionContext(java.io.Serializable):
    """
    public class ExceptionContext extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class that contains the actual implementation of the functionality mandated by the
        :class:`~fr.cnes.sirius.patrius.math.exception.util.ExceptionContext` interface. All Commons Math exceptions delegate
        the interface's methods to this class.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, throwable: java.lang.Throwable): ...
    def addMessage(self, localizable: 'Localizable', *object: typing.Any) -> None: ...
    def getKeys(self) -> java.util.Set[str]: ...
    def getLocalizedMessage(self) -> str:
        """
            Gets the message in the default locale.
        
            Returns:
                the localized message.
        
        
        """
        ...
    @typing.overload
    def getMessage(self) -> str:
        """
            Gets the default message.
        
            Returns:
                the message.
        
        """
        ...
    @typing.overload
    def getMessage(self, locale: java.util.Locale) -> str:
        """
            Gets the message in a specified locale.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): Locale in which the message should be translated.
        
            Returns:
                the localized message.
        
        """
        ...
    @typing.overload
    def getMessage(self, locale: java.util.Locale, string: str) -> str:
        """
            Gets the message in a specified locale.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): Locale in which the message should be translated.
                separator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): Separator inserted between the message parts.
        
            Returns:
                the localized message.
        
        
        """
        ...
    def getThrowable(self) -> java.lang.Throwable:
        """
            Get a reference to the exception to which the context relates.
        
            Returns:
                a reference to the exception to which the context relates
        
        
        """
        ...
    def getValue(self, string: str) -> typing.Any:
        """
            Gets the value associated to the given context key.
        
            Parameters:
                key (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): Context key.
        
            Returns:
                the context value or :code:`null` if the key does not exist.
        
        
        """
        ...
    def setValue(self, string: str, object: typing.Any) -> None:
        """
            Sets the context (key, value) pair. Keys are assumed to be unique within an instance. If the same key is assigned a new
            value, the previous one will be lost.
        
            Parameters:
                key (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): Context key (not null).
                value (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Context value.
        
        
        """
        ...

class ExceptionContextProvider:
    """
    public interface ExceptionContextProvider
    
        Interface for accessing the context data structure stored in Commons Math exceptions.
    """
    def getContext(self) -> ExceptionContext:
        """
            Gets a reference to the "rich context" data structure that allows to customize error messages and store key, value pairs
            in exceptions.
        
            Returns:
                a reference to the exception context.
        
        
        """
        ...

class Localizable(java.io.Serializable):
    """
    public interface Localizable extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for localizable strings.
    
        Since:
            2.2
    """
    def getLocalizedString(self, locale: java.util.Locale) -> str:
        """
            Gets the localized string.
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): locale into which to get the string.
        
            Returns:
                the localized string or the source string if no localized version is available.
        
        
        """
        ...
    def getSourceString(self) -> str:
        """
            Gets the source (non-localized) string.
        
            Returns:
                the source string.
        
        
        """
        ...

class DummyLocalizable(Localizable):
    """
    public class DummyLocalizable extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.exception.util.Localizable`
    
        Dummy implementation of the :class:`~fr.cnes.sirius.patrius.math.exception.util.Localizable` interface, without
        localization.
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str): ...
    def getLocalizedString(self, locale: java.util.Locale) -> str:
        """
            Gets the localized string.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.exception.util.Localizable.getLocalizedString` in
                interface :class:`~fr.cnes.sirius.patrius.math.exception.util.Localizable`
        
            Parameters:
                locale (`Locale <http://docs.oracle.com/javase/8/docs/api/java/util/Locale.html?is-external=true>`): locale into which to get the string.
        
            Returns:
                the localized string or the source string if no localized version is available.
        
        
        """
        ...
    def getSourceString(self) -> str:
        """
            Gets the source (non-localized) string.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.exception.util.Localizable.getSourceString` in
                interface :class:`~fr.cnes.sirius.patrius.math.exception.util.Localizable`
        
            Returns:
                the source string.
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.exception.util")``.

    ArgUtils: typing.Type[ArgUtils]
    DummyLocalizable: typing.Type[DummyLocalizable]
    ExceptionContext: typing.Type[ExceptionContext]
    ExceptionContextProvider: typing.Type[ExceptionContextProvider]
    Localizable: typing.Type[Localizable]
