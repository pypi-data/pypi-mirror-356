
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util.function
import jpype
import typing



_TimeStampedInterpolableEphemeris__IN = typing.TypeVar('_TimeStampedInterpolableEphemeris__IN', bound=fr.cnes.sirius.patrius.time.TimeStamped)  # <IN>
_TimeStampedInterpolableEphemeris__OUT = typing.TypeVar('_TimeStampedInterpolableEphemeris__OUT')  # <OUT>
class TimeStampedInterpolableEphemeris(java.io.Serializable, typing.Generic[_TimeStampedInterpolableEphemeris__IN, _TimeStampedInterpolableEphemeris__OUT]):
    """
    public class TimeStampedInterpolableEphemeris<IN extends :class:`~fr.cnes.sirius.patrius.time.TimeStamped`,OUT> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class representing an interpolable ephemeris for any time stamped data. It is thread-safe.
    
        This class makes a difference between 3 interval types:
    
          - The samples interval corresponds to the first and last date of the provided samples.
          - The optimal interval is related to the order of interpolation. Indeed, interpolation is of best quality when it is
            performed between the 2 central points of the interpolation (if interpolation is of order 8, then interpolation quality
            is best if there are 4 points before and 4 points after).
          - The usable interval corresponds, depending on
            :meth:`~fr.cnes.sirius.patrius.time.interpolation.TimeStampedInterpolableEphemeris.isAcceptOutOfOptimalRange`, either to
            the samples interval or to the optimal interval
    
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, iNArray: typing.Union[typing.List[_TimeStampedInterpolableEphemeris__IN], jpype.JArray], int: int, timeStampedInterpolationFunctionBuilder: typing.Union['TimeStampedInterpolationFunctionBuilder'[_TimeStampedInterpolableEphemeris__IN, _TimeStampedInterpolableEphemeris__OUT], typing.Callable[[typing.MutableSequence[fr.cnes.sirius.patrius.time.TimeStamped], int, int], java.util.function.Function[fr.cnes.sirius.patrius.time.AbsoluteDate, typing.Any]]], boolean: bool): ...
    @typing.overload
    def __init__(self, iNArray: typing.Union[typing.List[_TimeStampedInterpolableEphemeris__IN], jpype.JArray], int: int, timeStampedInterpolationFunctionBuilder: typing.Union['TimeStampedInterpolationFunctionBuilder'[_TimeStampedInterpolableEphemeris__IN, _TimeStampedInterpolableEphemeris__OUT], typing.Callable[[typing.MutableSequence[fr.cnes.sirius.patrius.time.TimeStamped], int, int], java.util.function.Function[fr.cnes.sirius.patrius.time.AbsoluteDate, typing.Any]]], boolean: bool, boolean2: bool, boolean3: bool, int2: int): ...
    def extendInterpolableEphemeris(self, iNArray: typing.Union[typing.List[_TimeStampedInterpolableEphemeris__IN], jpype.JArray], boolean: bool, boolean2: bool) -> 'TimeStampedInterpolableEphemeris'[_TimeStampedInterpolableEphemeris__IN, _TimeStampedInterpolableEphemeris__OUT]: ...
    def getCacheReusabilityRatio(self) -> float:
        """
            Provides the ratio of reusability of the internal cache. This method can help to chose the size of the cache.
        
            Returns:
                the reusability ratio (0 means no reusability at all, 0.5 means that the supplier is called only half time compared to
                computeIf method)
        
        
        """
        ...
    def getCeilingIndex(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> int:
        """
            Getter for the ceiling index for the given date.
        
        
            If the provided date is after the last sample, -1 is returned.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date to look for
        
            Returns:
                the ceiling index
        
        
        """
        ...
    def getCeilingSample(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> _TimeStampedInterpolableEphemeris__IN:
        """
            Getter for the ceiling sample for the given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date to look for
        
            Returns:
                the ceiling index
        
            Raises:
                : if the provided date is after the last sample
        
        
        """
        ...
    def getFirstDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the first date.
        
            Returns:
                the first date
        
        
        """
        ...
    def getFirstOptimalDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the first optimal date.
        
            Returns:
                the first optimal date
        
        
        """
        ...
    def getFirstSample(self) -> _TimeStampedInterpolableEphemeris__IN:
        """
            Getter for the first sample.
        
            Returns:
                the first sample
        
        
        """
        ...
    def getFirstUsableDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the first usable date.
        
            Returns:
                the first usable date
        
        
        """
        ...
    def getFloorIndex(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> int:
        """
            Getter for the floor index for the given date.
        
        
            If the provided date is before the first sample, -1 is returned.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date to look for
        
            Returns:
                the floor index
        
        
        """
        ...
    def getFloorSample(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> _TimeStampedInterpolableEphemeris__IN:
        """
            Getter for the floor sample for the given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date to look for
        
            Returns:
                the ceiling index
        
            Raises:
                : if the provided date is before the first sample
        
        
        """
        ...
    def getLastDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the last date.
        
            Returns:
                the last date
        
        
        """
        ...
    def getLastOptimalDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the last optimal date.
        
            Returns:
                the last date
        
        
        """
        ...
    def getLastSample(self) -> _TimeStampedInterpolableEphemeris__IN:
        """
            Getter for the last sample.
        
            Returns:
                the last sample
        
        
        """
        ...
    def getLastUsableDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the last usable date.
        
            Returns:
                the last usable date
        
        
        """
        ...
    def getSampleSize(self) -> int:
        """
            Getter for the sample size.
        
            Returns:
                the sample size
        
        
        """
        ...
    def getSamples(self, boolean: bool) -> typing.MutableSequence[_TimeStampedInterpolableEphemeris__IN]:
        """
            Getter for the samples array.
        
            Parameters:
                copy (boolean): if :code:`true` return a copy of the samples array, otherwise return the stored array
        
            Returns:
                the samples array
        
        
        """
        ...
    def getSearchMethod(self) -> 'TimeStampedInterpolableEphemeris.SearchMethod':
        """
            Getter for the search method.
        
            Returns:
                the search method
        
        
        """
        ...
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> _TimeStampedInterpolableEphemeris__OUT:
        """
            Returns an interpolated instance at the required date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date of the interpolation
        
            Returns:
                the interpolated instance
        
            Raises:
                : if the date is outside the supported interval or if the instance has the setting :code:`acceptOutOfRange = false` and
                    the date is outside the optimal interval which is a sub-interval from the full interval interval required for
                    interpolation with respect to the interpolation order
        
        
        """
        ...
    def isAcceptOutOfOptimalRange(self) -> bool:
        """
            Indicates whether accept dates outside of the optimal interval which is a sub-interval from the full interval interval
            required for interpolation with respect to the interpolation order.
        
            Returns:
                :code:`true` if the dates outside of the optimal interval are accepted, :code:`false` otherwise
        
        
        """
        ...
    def setSearchMethod(self, searchMethod: 'TimeStampedInterpolableEphemeris.SearchMethod') -> None:
        """
            Setter for the search method.
        
            Parameters:
                searchMethod (:class:`~fr.cnes.sirius.patrius.time.interpolation.TimeStampedInterpolableEphemeris.SearchMethod`): the search method to set
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`searchMethod` is null
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    class SearchMethod(java.lang.Enum['TimeStampedInterpolableEphemeris.SearchMethod']):
        DICHOTOMY: typing.ClassVar['TimeStampedInterpolableEphemeris.SearchMethod'] = ...
        PROPORTIONAL: typing.ClassVar['TimeStampedInterpolableEphemeris.SearchMethod'] = ...
        def midPoint(self, int: int, int2: int, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate3: fr.cnes.sirius.patrius.time.AbsoluteDate) -> int: ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'TimeStampedInterpolableEphemeris.SearchMethod': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['TimeStampedInterpolableEphemeris.SearchMethod']: ...

_TimeStampedInterpolationFunctionBuilder__IN = typing.TypeVar('_TimeStampedInterpolationFunctionBuilder__IN', bound=fr.cnes.sirius.patrius.time.TimeStamped)  # <IN>
_TimeStampedInterpolationFunctionBuilder__OUT = typing.TypeVar('_TimeStampedInterpolationFunctionBuilder__OUT')  # <OUT>
class TimeStampedInterpolationFunctionBuilder(java.io.Serializable, typing.Generic[_TimeStampedInterpolationFunctionBuilder__IN, _TimeStampedInterpolationFunctionBuilder__OUT]):
    """
    `@FunctionalInterface <http://docs.oracle.com/javase/8/docs/api/java/lang/FunctionalInterface.html?is-external=true>` public interface TimeStampedInterpolationFunctionBuilder<IN extends :class:`~fr.cnes.sirius.patrius.time.TimeStamped`,OUT> extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface representing a class that can build an interpolation function from an array of Time stamped samples.
    """
    def buildInterpolationFunction(self, iNArray: typing.Union[typing.List[_TimeStampedInterpolationFunctionBuilder__IN], jpype.JArray], int: int, int2: int) -> java.util.function.Function[fr.cnes.sirius.patrius.time.AbsoluteDate, _TimeStampedInterpolationFunctionBuilder__OUT]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.time.interpolation")``.

    TimeStampedInterpolableEphemeris: typing.Type[TimeStampedInterpolableEphemeris]
    TimeStampedInterpolationFunctionBuilder: typing.Type[TimeStampedInterpolationFunctionBuilder]
