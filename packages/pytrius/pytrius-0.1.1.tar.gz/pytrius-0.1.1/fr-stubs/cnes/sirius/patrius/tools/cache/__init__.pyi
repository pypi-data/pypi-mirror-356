
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.util.function
import typing



_CacheEntry__K = typing.TypeVar('_CacheEntry__K')  # <K>
_CacheEntry__V = typing.TypeVar('_CacheEntry__V')  # <V>
class CacheEntry(java.io.Serializable, typing.Generic[_CacheEntry__K, _CacheEntry__V]):
    """
    public class CacheEntry<K,V> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Immutable class representing an entry of the cache :class:`~fr.cnes.sirius.patrius.tools.cache.FIFOThreadSafeCache`.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, k: _CacheEntry__K, v: _CacheEntry__V): ...
    def getKey(self) -> _CacheEntry__K:
        """
            Getter for the key of the entry.
        
            Returns:
                the key of the entry
        
        
        """
        ...
    def getValue(self) -> _CacheEntry__V:
        """
            Getter for the value of the entry.
        
            Returns:
                the value of the entry
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of the cache entry.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of the cache entry
        
        
        """
        ...

_FIFOThreadSafeCache__K = typing.TypeVar('_FIFOThreadSafeCache__K')  # <K>
_FIFOThreadSafeCache__V = typing.TypeVar('_FIFOThreadSafeCache__V')  # <V>
class FIFOThreadSafeCache(java.io.Serializable, typing.Generic[_FIFOThreadSafeCache__K, _FIFOThreadSafeCache__V]):
    """
    public class FIFOThreadSafeCache<K,V> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class implements a thread safe cache.
    
    
        It is based on a FirstInFirstOut (FIFO) structure. As soon as the structure reaches it's maximum size, adding a new
        entry removes the oldest entry.
    
        The tread-safety is handled by the use of the `null
        <http://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ConcurrentLinkedDeque.html?is-external=true>`
        implementation (which is a lock-free implementation).
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_MAX_SIZE: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_MAX_SIZE
    
        Default max size for the cache: trade-off between the duration for look-up in the cache versus reuse of already computed
        values.
    
        Also see:
            :meth:`~constant`
    
    
    """
    PERCENT: typing.ClassVar[int] = ...
    """
    public static final int PERCENT
    
        Percent conversion value.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    def clear(self) -> None:
        """
            Clears the cache.
        
        
            Note that this method might have non desired effects if it is called in concurrency with
            :meth:`~fr.cnes.sirius.patrius.tools.cache.FIFOThreadSafeCache.computeIf` (more precisely with addEntry internal
            method).
        
        """
        ...
    def computeIf(self, predicate: typing.Union[java.util.function.Predicate[CacheEntry[_FIFOThreadSafeCache__K, _FIFOThreadSafeCache__V]], typing.Callable[[CacheEntry[_FIFOThreadSafeCache__K, _FIFOThreadSafeCache__V]], bool]], supplier: typing.Union[java.util.function.Supplier[CacheEntry[_FIFOThreadSafeCache__K, _FIFOThreadSafeCache__V]], typing.Callable[[], CacheEntry[_FIFOThreadSafeCache__K, _FIFOThreadSafeCache__V]]]) -> CacheEntry[_FIFOThreadSafeCache__K, _FIFOThreadSafeCache__V]: ...
    def computeIfAbsent(self, k: _FIFOThreadSafeCache__K, supplier: typing.Union[java.util.function.Supplier[CacheEntry[_FIFOThreadSafeCache__K, _FIFOThreadSafeCache__V]], typing.Callable[[], CacheEntry[_FIFOThreadSafeCache__K, _FIFOThreadSafeCache__V]]]) -> CacheEntry[_FIFOThreadSafeCache__K, _FIFOThreadSafeCache__V]: ...
    def getMaxSize(self) -> int:
        """
            Getter for the maximum size of the cache.
        
            Returns:
                the maximum size of the cache
        
        
        """
        ...
    def getReusabilityRatio(self) -> float:
        """
            Provides the ratio of reusability of this cache.
        
            This method can help to chose the size of the cache.
        
            Returns:
                the reusability ratio (0 means no reusability at all, 0.5 means that the supplier is called only half time compared to
                the :meth:`~fr.cnes.sirius.patrius.tools.cache.FIFOThreadSafeCache.computeIf` method)
        
        
        """
        ...
    def toString(self) -> str:
        """
            Returns a string representation of the cache structure.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of the cache structure
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.tools.cache")``.

    CacheEntry: typing.Type[CacheEntry]
    FIFOThreadSafeCache: typing.Type[FIFOThreadSafeCache]
