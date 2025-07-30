
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.stat.descriptive
import java.io
import jpype
import typing



class Max(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable):
    """
    public class Max extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Returns the maximum of the available values.
    
    
          - The result is :code:`NaN` iff all values are :code:`NaN` (i.e. :code:`NaN` values have no impact on the value of the
            statistic).
          - If any of the values equals :code:`Double.POSITIVE_INFINITY`, the result is :code:`Double.POSITIVE_INFINITY.`
    
    
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, max: 'Max'): ...
    def clear(self) -> None:
        """
            Clears the internal state of the Statistic
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.clear` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.clear` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
        
        """
        ...
    @typing.overload
    def copy(self) -> 'Max':
        """
            Returns a copy of the statistic with the same internal state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.copy` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                a copy of the statistic
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(max: 'Max', max2: 'Max') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.rank.Max`): Max to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.rank.Max`): Max to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float:
        """
            Returns the maximum of the entries in the specified portion of the input array, or :code:`Double.NaN` if the designated
            subarray is empty.
        
            Throws :code:`MathIllegalArgumentException` if the array is null or the array index parameters are not valid.
        
        
              - The result is :code:`NaN` iff all values are :code:`NaN` (i.e. :code:`NaN` values have no impact on the value of the
                statistic).
              - If any of the values equals :code:`Double.POSITIVE_INFINITY`, the result is :code:`Double.POSITIVE_INFINITY.`
        
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                values (double[]): the input array
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the maximum of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the array index parameters are not valid
        
            Also see:
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of values that have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Returns:
                the number of values.
        
        
        """
        ...
    def getResult(self) -> float:
        """
            Returns the current value of the Statistic.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getResult` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.getResult` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                value of the statistic, :code:`Double.NaN` if it has been cleared or just instantiated.
        
        
        """
        ...
    def increment(self, double: float) -> None:
        """
            Updates the internal state of the statistic to reflect the addition of the new value.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.increment` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.increment` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                d (double): the new value.
        
        
        """
        ...

class Min(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable):
    """
    public class Min extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Returns the minimum of the available values.
    
    
          - The result is :code:`NaN` iff all values are :code:`NaN` (i.e. :code:`NaN` values have no impact on the value of the
            statistic).
          - If any of the values equals :code:`Double.NEGATIVE_INFINITY`, the result is :code:`Double.NEGATIVE_INFINITY.`
    
    
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, min: 'Min'): ...
    def clear(self) -> None:
        """
            Clears the internal state of the Statistic
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.clear` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.clear` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
        
        """
        ...
    @typing.overload
    def copy(self) -> 'Min':
        """
            Returns a copy of the statistic with the same internal state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.copy` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                a copy of the statistic
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(min: 'Min', min2: 'Min') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.rank.Min`): Min to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.rank.Min`): Min to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float:
        """
            Returns the minimum of the entries in the specified portion of the input array, or :code:`Double.NaN` if the designated
            subarray is empty.
        
            Throws :code:`MathIllegalArgumentException` if the array is null or the array index parameters are not valid.
        
        
              - The result is :code:`NaN` iff all values are :code:`NaN` (i.e. :code:`NaN` values have no impact on the value of the
                statistic).
              - If any of the values equals :code:`Double.NEGATIVE_INFINITY`, the result is :code:`Double.NEGATIVE_INFINITY.`
        
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                values (double[]): the input array
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the minimum of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the array index parameters are not valid
        
            Also see:
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of values that have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Returns:
                the number of values.
        
        
        """
        ...
    def getResult(self) -> float:
        """
            Returns the current value of the Statistic.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getResult` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.getResult` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                value of the statistic, :code:`Double.NaN` if it has been cleared or just instantiated.
        
        
        """
        ...
    def increment(self, double: float) -> None:
        """
            Updates the internal state of the statistic to reflect the addition of the new value.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.increment` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.increment` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                d (double): the new value.
        
        
        """
        ...

class Percentile(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractUnivariateStatistic, java.io.Serializable):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, percentile: 'Percentile'): ...
    @typing.overload
    def copy(self) -> 'Percentile': ...
    @typing.overload
    @staticmethod
    def copy(percentile: 'Percentile', percentile2: 'Percentile') -> None: ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, double: float) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int, double2: float) -> float: ...
    def getQuantile(self) -> float: ...
    def medianOf3(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> int: ...
    @typing.overload
    def setData(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    def setData(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> None: ...
    def setQuantile(self, double: float) -> None: ...

class Median(Percentile):
    """
    public class Median extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.rank.Percentile`
    
        Returns the median of the available values. This is the same as the 50th percentile. See
        :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.rank.Percentile` for a description of the algorithm used.
    
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, median: 'Median'): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.stat.descriptive.rank")``.

    Max: typing.Type[Max]
    Median: typing.Type[Median]
    Min: typing.Type[Min]
    Percentile: typing.Type[Percentile]
