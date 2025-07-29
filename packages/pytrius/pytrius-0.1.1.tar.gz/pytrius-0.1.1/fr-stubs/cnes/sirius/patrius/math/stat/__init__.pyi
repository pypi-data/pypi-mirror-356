
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.stat.clustering
import fr.cnes.sirius.patrius.math.stat.correlation
import fr.cnes.sirius.patrius.math.stat.descriptive
import fr.cnes.sirius.patrius.math.stat.inference
import fr.cnes.sirius.patrius.math.stat.ranking
import fr.cnes.sirius.patrius.math.stat.regression
import java.io
import java.lang
import java.util
import jpype
import typing



class Frequency(java.io.Serializable):
    """
    public class Frequency extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Maintains a frequency distribution.
    
        Accepts int, long, char or Comparable values. New values added must be comparable to those that have been added,
        otherwise the add method will throw an IllegalArgumentException.
    
        Integer values (int, long, Integer, Long) are not distinguished by type -- i.e. :code:`addValue(Long.valueOf(2)),
        addValue(2), addValue(2l)` all have the same effect (similarly for arguments to :code:`getCount,` etc.).
    
        char values are converted by :code:`addValue` to Character instances. As such, these values are not comparable to
        integral values, so attempts to combine integral types with chars in a frequency distribution will fail.
    
        The values are ordered using the default (natural order), unless a :code:`Comparator` is supplied in the constructor.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, comparator: typing.Union[java.util.Comparator[typing.Any], typing.Callable[[typing.Any, typing.Any], int]]): ...
    @typing.overload
    def addValue(self, char: str) -> None:
        """
            Adds 1 to the frequency count for v.
        
            Parameters:
                v (int): the value to add.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the table contains entries not comparable to Integer
        
            Adds 1 to the frequency count for v.
        
            Parameters:
                v (long): the value to add.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the table contains entries not comparable to Long
        
            Adds 1 to the frequency count for v.
        
            Parameters:
                v (char): the value to add.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the table contains entries not comparable to Char
        
        
        """
        ...
    @typing.overload
    def addValue(self, int: int) -> None: ...
    @typing.overload
    def addValue(self, comparable: typing.Union[java.lang.Comparable[typing.Any], typing.Callable[[typing.Any], int]]) -> None: ...
    @typing.overload
    def addValue(self, long: int) -> None: ...
    def clear(self) -> None:
        """
            Clears the frequency table
        
        """
        ...
    def entrySetIterator(self) -> java.util.Iterator[java.util.Map.Entry[java.lang.Comparable[typing.Any], int]]: ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @typing.overload
    def getCount(self, char: str) -> int:
        """
            Returns the number of values = v.
        
            Parameters:
                v (int): the value to lookup.
        
            Returns:
                the frequency of v.
        
            Returns the number of values = v.
        
            Parameters:
                v (long): the value to lookup.
        
            Returns:
                the frequency of v.
        
            Returns the number of values = v.
        
            Parameters:
                v (char): the value to lookup.
        
            Returns:
                the frequency of v.
        
        
        """
        ...
    @typing.overload
    def getCount(self, int: int) -> int: ...
    @typing.overload
    def getCount(self, comparable: typing.Union[java.lang.Comparable[typing.Any], typing.Callable[[typing.Any], int]]) -> int: ...
    @typing.overload
    def getCount(self, long: int) -> int: ...
    @typing.overload
    def getCumFreq(self, char: str) -> int:
        """
            Returns the cumulative frequency of values less than or equal to v.
        
            Returns 0 if v is not comparable to the values set.
        
            Parameters:
                v (int): the value to lookup
        
            Returns:
                the proportion of values equal to v
        
            Returns the cumulative frequency of values less than or equal to v.
        
            Returns 0 if v is not comparable to the values set.
        
            Parameters:
                v (long): the value to lookup
        
            Returns:
                the proportion of values equal to v
        
            Returns the cumulative frequency of values less than or equal to v.
        
            Returns 0 if v is not comparable to the values set.
        
            Parameters:
                v (char): the value to lookup
        
            Returns:
                the proportion of values equal to v
        
        
        """
        ...
    @typing.overload
    def getCumFreq(self, int: int) -> int: ...
    @typing.overload
    def getCumFreq(self, comparable: typing.Union[java.lang.Comparable[typing.Any], typing.Callable[[typing.Any], int]]) -> int: ...
    @typing.overload
    def getCumFreq(self, long: int) -> int: ...
    @typing.overload
    def getCumPct(self, char: str) -> float:
        """
            Returns the cumulative percentage of values less than or equal to v (as a proportion between 0 and 1).
        
            Returns 0 if v is not comparable to the values set.
        
            Parameters:
                v (int): the value to lookup
        
            Returns:
                the proportion of values less than or equal to v
        
            Returns the cumulative percentage of values less than or equal to v (as a proportion between 0 and 1).
        
            Returns 0 if v is not comparable to the values set.
        
            Parameters:
                v (long): the value to lookup
        
            Returns:
                the proportion of values less than or equal to v
        
            Returns the cumulative percentage of values less than or equal to v (as a proportion between 0 and 1).
        
            Returns 0 if v is not comparable to the values set.
        
            Parameters:
                v (char): the value to lookup
        
            Returns:
                the proportion of values less than or equal to v
        
        
        """
        ...
    @typing.overload
    def getCumPct(self, int: int) -> float: ...
    @typing.overload
    def getCumPct(self, comparable: typing.Union[java.lang.Comparable[typing.Any], typing.Callable[[typing.Any], int]]) -> float: ...
    @typing.overload
    def getCumPct(self, long: int) -> float: ...
    @typing.overload
    def getPct(self, char: str) -> float:
        """
            Returns the percentage of values that are equal to v (as a proportion between 0 and 1).
        
            Parameters:
                v (int): the value to lookup
        
            Returns:
                the proportion of values equal to v
        
            Returns the percentage of values that are equal to v (as a proportion between 0 and 1).
        
            Parameters:
                v (long): the value to lookup
        
            Returns:
                the proportion of values equal to v
        
            Returns the percentage of values that are equal to v (as a proportion between 0 and 1).
        
            Parameters:
                v (char): the value to lookup
        
            Returns:
                the proportion of values equal to v
        
        
        """
        ...
    @typing.overload
    def getPct(self, int: int) -> float: ...
    @typing.overload
    def getPct(self, comparable: typing.Union[java.lang.Comparable[typing.Any], typing.Callable[[typing.Any], int]]) -> float: ...
    @typing.overload
    def getPct(self, long: int) -> float: ...
    def getSumFreq(self) -> int:
        """
            Returns the sum of all frequencies.
        
            Returns:
                the total frequency count.
        
        
        """
        ...
    def getUniqueCount(self) -> int:
        """
            Returns the number of values in the frequency table.
        
            Returns:
                the number of unique values that have been added to the frequency table.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.Frequency.valuesIterator`
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def incrementValue(self, comparable: typing.Union[java.lang.Comparable[typing.Any], typing.Callable[[typing.Any], int]], long: int) -> None: ...
    @typing.overload
    def merge(self, frequency: 'Frequency') -> None:
        """
            Merge another Frequency object's counts into this instance. This Frequency's counts will be incremented (or set when not
            already set) by the counts represented by other.
        
            Parameters:
                other (:class:`~fr.cnes.sirius.patrius.math.stat.Frequency`): the other :class:`~fr.cnes.sirius.patrius.math.stat.Frequency` object to be merged
        
            Since:
                3.1
        
        public void merge(`Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.stat.Frequency`> others)
        
            Merge a `null <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>` of
            :class:`~fr.cnes.sirius.patrius.math.stat.Frequency` objects into this instance. This Frequency's counts will be
            incremented (or set when not already set) by the counts represented by each of the others.
        
            Parameters:
                others (`Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.stat.Frequency`> others): the other :class:`~fr.cnes.sirius.patrius.math.stat.Frequency` objects to be merged
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def merge(self, collection: typing.Union[java.util.Collection['Frequency'], typing.Sequence['Frequency'], typing.Set['Frequency']]) -> None: ...
    def toString(self) -> str:
        """
            Return a string representation of this frequency distribution.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation.
        
        
        """
        ...
    def valuesIterator(self) -> java.util.Iterator[java.lang.Comparable[typing.Any]]: ...

class StatUtils:
    @typing.overload
    @staticmethod
    def geometricMean(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def geometricMean(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def max(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def max(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @staticmethod
    def maxAbs(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def mean(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def mean(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @staticmethod
    def meanDifference(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def median(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def median(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def min(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def min(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @staticmethod
    def normalize(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    @staticmethod
    def percentile(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def percentile(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def populationVariance(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def populationVariance(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def populationVariance(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def populationVariance(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def product(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def product(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def quadraticMean(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def quadraticMean(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def standardDeviation(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def standardDeviation(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def standardDeviation(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def standardDeviation(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def sum(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def sum(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @staticmethod
    def sumDifference(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def sumLog(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def sumLog(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def sumSq(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def sumSq(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def variance(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def variance(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def variance(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, int: int, int2: int) -> float: ...
    @typing.overload
    @staticmethod
    def variance(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @staticmethod
    def varianceDifference(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.stat")``.

    Frequency: typing.Type[Frequency]
    StatUtils: typing.Type[StatUtils]
    clustering: fr.cnes.sirius.patrius.math.stat.clustering.__module_protocol__
    correlation: fr.cnes.sirius.patrius.math.stat.correlation.__module_protocol__
    descriptive: fr.cnes.sirius.patrius.math.stat.descriptive.__module_protocol__
    inference: fr.cnes.sirius.patrius.math.stat.inference.__module_protocol__
    ranking: fr.cnes.sirius.patrius.math.stat.ranking.__module_protocol__
    regression: fr.cnes.sirius.patrius.math.stat.regression.__module_protocol__
