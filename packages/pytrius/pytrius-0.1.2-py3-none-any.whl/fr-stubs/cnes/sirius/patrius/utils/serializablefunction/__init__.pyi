
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util.function
import typing



_SerializableFunction__T = typing.TypeVar('_SerializableFunction__T')  # <T>
_SerializableFunction__R = typing.TypeVar('_SerializableFunction__R')  # <R>
class SerializableFunction(java.io.Serializable, java.util.function.Function[_SerializableFunction__T, _SerializableFunction__R], typing.Generic[_SerializableFunction__T, _SerializableFunction__R]):
    """
    `@FunctionalInterface <http://docs.oracle.com/javase/8/docs/api/java/lang/FunctionalInterface.html?is-external=true>` public interface SerializableFunction<T,R> extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, `Function <http://docs.oracle.com/javase/8/docs/api/java/util/function/Function.html?is-external=true>`<T,R>
    
        Extension of the `null <http://docs.oracle.com/javase/8/docs/api/java/util/function/Function.html?is-external=true>`
        interface to specify that these implementations must be serializable.
    
        Since:
            4.13
    """
    ...

_SerializablePredicate__T = typing.TypeVar('_SerializablePredicate__T')  # <T>
class SerializablePredicate(java.io.Serializable, java.util.function.Predicate[_SerializablePredicate__T], typing.Generic[_SerializablePredicate__T]):
    """
    `@FunctionalInterface <http://docs.oracle.com/javase/8/docs/api/java/lang/FunctionalInterface.html?is-external=true>` public interface SerializablePredicate<T> extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, `Predicate <http://docs.oracle.com/javase/8/docs/api/java/util/function/Predicate.html?is-external=true>`<T>
    
        Extension of the `null <http://docs.oracle.com/javase/8/docs/api/java/util/function/Predicate.html?is-external=true>` to
        specify that these implementations must be serializable.
    
        Since:
            4.14
    """
    ...

_SerializableToDoubleFunction__T = typing.TypeVar('_SerializableToDoubleFunction__T')  # <T>
class SerializableToDoubleFunction(java.io.Serializable, java.util.function.ToDoubleFunction[_SerializableToDoubleFunction__T], typing.Generic[_SerializableToDoubleFunction__T]):
    """
    `@FunctionalInterface <http://docs.oracle.com/javase/8/docs/api/java/lang/FunctionalInterface.html?is-external=true>` public interface SerializableToDoubleFunction<T> extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, `ToDoubleFunction <http://docs.oracle.com/javase/8/docs/api/java/util/function/ToDoubleFunction.html?is-external=true>`<T>
    
        Extension of the `null
        <http://docs.oracle.com/javase/8/docs/api/java/util/function/ToDoubleFunction.html?is-external=true>` to specify that
        these implementations must be serializable.
    
        Since:
            4.13
    """
    ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.utils.serializablefunction")``.

    SerializableFunction: typing.Type[SerializableFunction]
    SerializablePredicate: typing.Type[SerializablePredicate]
    SerializableToDoubleFunction: typing.Type[SerializableToDoubleFunction]
