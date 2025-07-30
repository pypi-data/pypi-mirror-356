
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.stat.descriptive
import fr.cnes.sirius.patrius.math.stat.descriptive.summary
import java.io
import java.lang
import jpype
import typing



class GeometricMean(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, geometricMean: 'GeometricMean'): ...
    @typing.overload
    def __init__(self, sumOfLogs: fr.cnes.sirius.patrius.math.stat.descriptive.summary.SumOfLogs): ...
    def clear(self) -> None: ...
    @typing.overload
    def copy(self) -> 'GeometricMean': ...
    @typing.overload
    @staticmethod
    def copy(geometricMean: 'GeometricMean', geometricMean2: 'GeometricMean') -> None: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    def getN(self) -> int: ...
    def getResult(self) -> float: ...
    def getSumLogImpl(self) -> fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic: ...
    def increment(self, double: float) -> None: ...
    def setSumLogImpl(self, storelessUnivariateStatistic: fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic) -> None: ...

class Kurtosis(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, fourthMoment: 'FourthMoment'): ...
    @typing.overload
    def __init__(self, kurtosis: 'Kurtosis'): ...
    def clear(self) -> None: ...
    @typing.overload
    def copy(self) -> 'Kurtosis': ...
    @typing.overload
    @staticmethod
    def copy(kurtosis: 'Kurtosis', kurtosis2: 'Kurtosis') -> None: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    def getN(self) -> int: ...
    def getResult(self) -> float: ...
    def increment(self, double: float) -> None: ...

class Mean(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable, fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation):
    """
    public class Mean extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation`
    
    
        Computes the arithmetic mean of a set of values. Uses the definitional formula:
    
        mean = sum(x_i) / n
    
        where :code:`n` is the number of observations.
    
        When :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Mean.increment` is used to add data incrementally from
        a stream of (unstored) values, the value of the statistic that
        :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Mean.getResult` returns is computed using the following
        recursive updating algorithm:
    
          1.  Initialize :code:`m =` the first value
          2.  For each additional value, update using
    
    
    :code:`m = m + (new value - m) / (number of observations)`
    
    
        If null is used to compute the mean of an array of stored values, a two-pass, corrected algorithm is used, starting with
        the definitional formula computed using the array of stored values and then correcting this by adding the mean deviation
        of the data values from the arithmetic mean. See, e.g. "Comparison of Several Algorithms for Computing Sample Means and
        Variances," Robert F. Ling, Journal of the American Statistical Association, Vol. 69, No. 348 (Dec., 1974), pp. 859-866.
    
        Returns :code:`Double.NaN` if the dataset is empty.
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, firstMoment: 'FirstMoment'): ...
    @typing.overload
    def __init__(self, mean: 'Mean'): ...
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
    def copy(self) -> 'Mean':
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
    def copy(mean: 'Mean', mean2: 'Mean') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Mean`): Mean to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Mean`): Mean to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Returns the arithmetic mean of the entries in the specified portion of the input array, or :code:`Double.NaN` if the
            designated subarray is empty.
        
            Throws :code:`IllegalArgumentException` if the array is null.
        
            See :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Mean` for details on the computing algorithm.
        
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
                the mean of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the array index parameters are not valid
        
            Also see:
        
            Returns the weighted arithmetic mean of the entries in the input array.
        
            Throws :code:`MathIllegalArgumentException` if either array is null.
        
            See :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Mean` for details on the computing algorithm. The
            two-pass algorithm described above is used here, with weights applied in computing both the original estimate and the
            correction factor.
        
            Throws :code:`MathIllegalArgumentException` if any of the following are true:
        
              - the values array is null
              - the weights array is null
              - the weights array does not have the same length as the values array
              - the weights array contains one or more infinite values
              - the weights array contains one or more NaN values
              - the weights array contains negative values
        
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation`
        
            Parameters:
                values (double[]): the input array
                weights (double[]): the weights array
        
            Returns:
                the mean of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the parameters are not valid
        
            Since:
                2.1
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float:
        """
            Returns the weighted arithmetic mean of the entries in the specified portion of the input array, or :code:`Double.NaN`
            if the designated subarray is empty.
        
            Throws :code:`IllegalArgumentException` if either array is null.
        
            See :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Mean` for details on the computing algorithm. The
            two-pass algorithm described above is used here, with weights applied in computing both the original estimate and the
            correction factor.
        
            Throws :code:`IllegalArgumentException` if any of the following are true:
        
              - the values array is null
              - the weights array is null
              - the weights array does not have the same length as the values array
              - the weights array contains one or more infinite values
              - the weights array contains one or more NaN values
              - the weights array contains negative values
              - the start and length arguments do not determine a valid array
        
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation`
        
            Parameters:
                values (double[]): the input array
                weights (double[]): the weights array
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the mean of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the parameters are not valid
        
            Since:
                2.1
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
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
        
            Note that when :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Mean.Mean` is used to create a Mean, this
            method does nothing. In that case, the FirstMoment should be incremented directly.
        
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

class SemiVariance(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractUnivariateStatistic, java.io.Serializable):
    UPSIDE_VARIANCE: typing.ClassVar['SemiVariance.Direction'] = ...
    DOWNSIDE_VARIANCE: typing.ClassVar['SemiVariance.Direction'] = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...
    @typing.overload
    def __init__(self, boolean: bool, direction: 'SemiVariance.Direction'): ...
    @typing.overload
    def __init__(self, direction: 'SemiVariance.Direction'): ...
    @typing.overload
    def __init__(self, semiVariance: 'SemiVariance'): ...
    @typing.overload
    def copy(self) -> 'SemiVariance': ...
    @typing.overload
    @staticmethod
    def copy(semiVariance: 'SemiVariance', semiVariance2: 'SemiVariance') -> None: ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, direction: 'SemiVariance.Direction') -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, direction: 'SemiVariance.Direction', boolean: bool, int: int, int2: int) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], direction: 'SemiVariance.Direction') -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    def getVarianceDirection(self) -> 'SemiVariance.Direction': ...
    def isBiasCorrected(self) -> bool: ...
    def setBiasCorrected(self, boolean: bool) -> None: ...
    def setVarianceDirection(self, direction: 'SemiVariance.Direction') -> None: ...
    class Direction(java.lang.Enum['SemiVariance.Direction']):
        UPSIDE: typing.ClassVar['SemiVariance.Direction'] = ...
        DOWNSIDE: typing.ClassVar['SemiVariance.Direction'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'SemiVariance.Direction': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['SemiVariance.Direction']: ...

class Skewness(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable):
    """
    public class Skewness extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Computes the skewness of the available values.
    
        We use the following (unbiased) formula to define skewness:
    
        skewness = [n / (n -1) (n - 2)] sum[(x_i - mean)^3] / std^3
    
        where n is the number of values, mean is the :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Mean` and std
        is the :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.StandardDeviation`
    
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, skewness: 'Skewness'): ...
    @typing.overload
    def __init__(self, thirdMoment: 'ThirdMoment'): ...
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
    def copy(self) -> 'Skewness':
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
    def copy(skewness: 'Skewness', skewness2: 'Skewness') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Skewness`): Skewness to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Skewness`): Skewness to copy to
        
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
            Returns the Skewness of the entries in the specifed portion of the input array.
        
            See :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Skewness` for the definition used in the computation.
        
            Throws :code:`IllegalArgumentException` if the array is null.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                values (double[]): the input array
                begin (int): the index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the skewness of the values or Double.NaN if length is less than 3
        
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
            Returns the value of the statistic based on the values that have been added.
        
            See :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Skewness` for the definition used in the computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getResult` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.getResult` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                the skewness of the available values.
        
        
        """
        ...
    def increment(self, double: float) -> None:
        """
            Updates the internal state of the statistic to reflect the addition of the new value.
        
            Note that when :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Skewness.Skewness` is used to create a
            Skewness, this method does nothing. In that case, the ThirdMoment should be incremented directly.
        
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

class StandardDeviation(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable):
    """
    public class StandardDeviation extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Computes the sample standard deviation. The standard deviation is the positive square root of the variance. This
        implementation wraps a :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Variance` instance. The
        :code:`isBiasCorrected` property of the wrapped Variance instance is exposed, so that this class can be used to compute
        both the "sample standard deviation" (the square root of the bias-corrected "sample variance") or the "population
        standard deviation" (the square root of the non-bias-corrected "population variance"). See
        :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Variance` for more information.
    
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...
    @typing.overload
    def __init__(self, boolean: bool, secondMoment: 'SecondMoment'): ...
    @typing.overload
    def __init__(self, secondMoment: 'SecondMoment'): ...
    @typing.overload
    def __init__(self, standardDeviation: 'StandardDeviation'): ...
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
    def copy(self) -> 'StandardDeviation':
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
    def copy(standardDeviation: 'StandardDeviation', standardDeviation2: 'StandardDeviation') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.StandardDeviation`): StandardDeviation to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.StandardDeviation`): StandardDeviation to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Returns the Standard Deviation of the entries in the input array, or :code:`Double.NaN` if the array is empty.
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            Throws :code:`MathIllegalArgumentException` if the array is null.
        
            Does not change the internal state of the statistic.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                values (double[]): the input array
        
            Returns:
                the standard deviation of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null
        
            Also see:
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> float:
        """
            Returns the Standard Deviation of the entries in the specified portion of the input array, or :code:`Double.NaN` if the
            designated subarray is empty.
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            Throws :code:`MathIllegalArgumentException` if the array is null.
        
            Does not change the internal state of the statistic.
        
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
                the standard deviation of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the array index parameters are not valid
        
            Also see:
        
            Returns the Standard Deviation of the entries in the specified portion of the input array, using the precomputed mean
            value. Returns :code:`Double.NaN` if the designated subarray is empty.
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            The formula used assumes that the supplied mean value is the arithmetic mean of the sample data, not a known population
            parameter. This method is supplied only to save computation when the mean has already been computed.
        
            Throws :code:`IllegalArgumentException` if the array is null.
        
            Does not change the internal state of the statistic.
        
            Parameters:
                values (double[]): the input array
                mean (double): the precomputed mean value
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the standard deviation of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the array index parameters are not valid
        
            Returns the Standard Deviation of the entries in the input array, using the precomputed mean value. Returns
            :code:`Double.NaN` if the designated subarray is empty.
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            The formula used assumes that the supplied mean value is the arithmetic mean of the sample data, not a known population
            parameter. This method is supplied only to save computation when the mean has already been computed.
        
            Throws :code:`MathIllegalArgumentException` if the array is null.
        
            Does not change the internal state of the statistic.
        
            Parameters:
                values (double[]): the input array
                mean (double): the precomputed mean value
        
            Returns:
                the standard deviation of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, int: int, int2: int) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
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
    def isBiasCorrected(self) -> bool:
        """
        
            Returns:
                Returns the isBiasCorrected.
        
        
        """
        ...
    def setBiasCorrected(self, boolean: bool) -> None:
        """
        
            Parameters:
                isBiasCorrected (boolean): The isBiasCorrected to set.
        
        
        """
        ...

class Variance(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable, fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation):
    """
    public class Variance extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation`
    
        Computes the variance of the available values. By default, the unbiased "sample variance" definitional formula is used:
    
        variance = sum((x_i - mean)^2) / (n - 1)
    
        where mean is the :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Mean` and :code:`n` is the number of
        sample observations.
    
        The definitional formula does not have good numerical properties, so this implementation does not compute the statistic
        using the definitional formula.
    
          - The :code:`getResult` method computes the variance using updating formulas based on West's algorithm, as described in `
            Chan, T. F. and J. G. Lewis 1979, *Communications of the ACM*, vol. 22 no. 9, pp. 526-531.
            <http://doi.acm.org/10.1145/359146.359152>`
          - The :code:`evaluate` methods leverage the fact that they have the full array of values in memory to execute a two-pass
            algorithm. Specifically, these methods use the "corrected two-pass algorithm" from Chan, Golub, Levesque, *Algorithms
            for Computing the Sample Variance*, American Statistician, vol. 37, no. 3 (1983) pp. 242-247.
    
        Note that adding values using :code:`increment` or :code:`incrementAll` and then executing :code:`getResult` will
        sometimes give a different, less accurate, result than executing :code:`evaluate` with the full array of values. The
        former approach should only be used when the full array of values is not available.
    
        The "population variance" ( sum((x_i - mean)^2) / n ) can also be computed using this statistic. The
        :code:`isBiasCorrected` property determines whether the "population" or "sample" value is returned by the
        :code:`evaluate` and :code:`getResult` methods. To compute population variances, set this property to :code:`false.`
    
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...
    @typing.overload
    def __init__(self, boolean: bool, secondMoment: 'SecondMoment'): ...
    @typing.overload
    def __init__(self, secondMoment: 'SecondMoment'): ...
    @typing.overload
    def __init__(self, variance: 'Variance'): ...
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
    def copy(self) -> 'Variance':
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
    def copy(variance: 'Variance', variance2: 'Variance') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Variance`): Variance to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Variance`): Variance to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Returns the variance of the entries in the input array, or :code:`Double.NaN` if the array is empty.
        
            See :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Variance` for details on the computing algorithm.
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            Throws :code:`MathIllegalArgumentException` if the array is null.
        
            Does not change the internal state of the statistic.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                values (double[]): the input array
        
            Returns:
                the variance of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null
        
            Also see:
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> float:
        """
            Returns the variance of the entries in the specified portion of the input array, or :code:`Double.NaN` if the designated
            subarray is empty.
        
            See :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Variance` for details on the computing algorithm.
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            Does not change the internal state of the statistic.
        
            Throws :code:`MathIllegalArgumentException` if the array is null.
        
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
                the variance of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the array index parameters are not valid
        
            Also see:
        
        
            Returns the weighted variance of the entries in the the input array.
        
            Uses the formula
        
            .. code-block: java
            
            
               Σ(weights[i]*(values[i] - weightedMean) :sup:`2` )/(Σ(weights[i]) - 1)
             
            where weightedMean is the weighted mean
        
            This formula will not return the same result as the unweighted variance when all weights are equal, unless all weights
            are equal to 1. The formula assumes that weights are to be treated as "expansion values," as will be the case if for
            example the weights represent frequency counts. To normalize weights so that the denominator in the variance computation
            equals the length of the input vector minus one, use
        
            .. code-block: java
            
            
               evaluate(values, MathArrays.normalizeArray(weights, values.length)); 
             
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            Throws :code:`MathIllegalArgumentException` if any of the following are true:
        
              - the values array is null
              - the weights array is null
              - the weights array does not have the same length as the values array
              - the weights array contains one or more infinite values
              - the weights array contains one or more NaN values
              - the weights array contains negative values
        
        
            Does not change the internal state of the statistic.
        
            Throws :code:`MathIllegalArgumentException` if either array is null.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation`
        
            Parameters:
                values (double[]): the input array
                weights (double[]): the weights array
        
            Returns:
                the weighted variance of the values
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the parameters are not valid
        
            Since:
                2.1
        
            Returns the variance of the entries in the specified portion of the input array, using the precomputed mean value.
            Returns :code:`Double.NaN` if the designated subarray is empty.
        
            See :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Variance` for details on the computing algorithm.
        
            The formula used assumes that the supplied mean value is the arithmetic mean of the sample data, not a known population
            parameter. This method is supplied only to save computation when the mean has already been computed.
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            Throws :code:`MathIllegalArgumentException` if the array is null.
        
            Does not change the internal state of the statistic.
        
            Parameters:
                values (double[]): the input array
                mean (double): the precomputed mean value
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the variance of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the array index parameters are not valid
        
            Returns the variance of the entries in the input array, using the precomputed mean value. Returns :code:`Double.NaN` if
            the array is empty.
        
            See :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Variance` for details on the computing algorithm.
        
            If :code:`isBiasCorrected` is :code:`true` the formula used assumes that the supplied mean value is the arithmetic mean
            of the sample data, not a known population parameter. If the mean is a known population parameter, or if the
            "population" version of the variance is desired, set :code:`isBiasCorrected` to :code:`false` before invoking this
            method.
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            Throws :code:`MathIllegalArgumentException` if the array is null.
        
            Does not change the internal state of the statistic.
        
            Parameters:
                values (double[]): the input array
                mean (double): the precomputed mean value
        
            Returns:
                the variance of the values or Double.NaN if the array is empty
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, int: int, int2: int) -> float:
        """
        
            Returns the weighted variance of the entries in the specified portion of the input array, or :code:`Double.NaN` if the
            designated subarray is empty.
        
            Uses the formula
        
            .. code-block: java
            
            
               Σ(weights[i]*(values[i] - weightedMean) :sup:`2` )/(Σ(weights[i]) - 1)
             
            where weightedMean is the weighted mean
        
            This formula will not return the same result as the unweighted variance when all weights are equal, unless all weights
            are equal to 1. The formula assumes that weights are to be treated as "expansion values," as will be the case if for
            example the weights represent frequency counts. To normalize weights so that the denominator in the variance computation
            equals the length of the input vector minus one, use
        
            .. code-block: java
            
            
               evaluate(values, MathArrays.normalizeArray(weights, values.length)); 
             
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            Throws :code:`IllegalArgumentException` if any of the following are true:
        
              - the values array is null
              - the weights array is null
              - the weights array does not have the same length as the values array
              - the weights array contains one or more infinite values
              - the weights array contains one or more NaN values
              - the weights array contains negative values
              - the start and length arguments do not determine a valid array
        
        
            Does not change the internal state of the statistic.
        
            Throws :code:`MathIllegalArgumentException` if either array is null.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation`
        
            Parameters:
                values (double[]): the input array
                weights (double[]): the weights array
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the weighted variance of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the parameters are not valid
        
            Since:
                2.1
        
            Returns the weighted variance of the entries in the specified portion of the input array, using the precomputed weighted
            mean value. Returns :code:`Double.NaN` if the designated subarray is empty.
        
            Uses the formula
        
            .. code-block: java
            
            
               Σ(weights[i]*(values[i] - mean) :sup:`2` )/(Σ(weights[i]) - 1)
             
        
            The formula used assumes that the supplied mean value is the weighted arithmetic mean of the sample data, not a known
            population parameter. This method is supplied only to save computation when the mean has already been computed.
        
            This formula will not return the same result as the unweighted variance when all weights are equal, unless all weights
            are equal to 1. The formula assumes that weights are to be treated as "expansion values," as will be the case if for
            example the weights represent frequency counts. To normalize weights so that the denominator in the variance computation
            equals the length of the input vector minus one, use
        
            .. code-block: java
            
            
               evaluate(values, MathArrays.normalizeArray(weights, values.length), mean); 
             
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            Throws :code:`MathIllegalArgumentException` if any of the following are true:
        
              - the values array is null
              - the weights array is null
              - the weights array does not have the same length as the values array
              - the weights array contains one or more infinite values
              - the weights array contains one or more NaN values
              - the weights array contains negative values
              - the start and length arguments do not determine a valid array
        
        
            Does not change the internal state of the statistic.
        
            Parameters:
                values (double[]): the input array
                weights (double[]): the weights array
                mean (double): the precomputed weighted mean value
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the variance of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the parameters are not valid
        
            Since:
                2.1
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float) -> float:
        """
        
            Returns the weighted variance of the values in the input array, using the precomputed weighted mean value.
        
            Uses the formula
        
            .. code-block: java
            
            
               Σ(weights[i]*(values[i] - mean) :sup:`2` )/(Σ(weights[i]) - 1)
             
        
            The formula used assumes that the supplied mean value is the weighted arithmetic mean of the sample data, not a known
            population parameter. This method is supplied only to save computation when the mean has already been computed.
        
            This formula will not return the same result as the unweighted variance when all weights are equal, unless all weights
            are equal to 1. The formula assumes that weights are to be treated as "expansion values," as will be the case if for
            example the weights represent frequency counts. To normalize weights so that the denominator in the variance computation
            equals the length of the input vector minus one, use
        
            .. code-block: java
            
            
               evaluate(values, MathArrays.normalizeArray(weights, values.length), mean); 
             
        
            Returns 0 for a single-value (i.e. length = 1) sample.
        
            Throws :code:`MathIllegalArgumentException` if any of the following are true:
        
              - the values array is null
              - the weights array is null
              - the weights array does not have the same length as the values array
              - the weights array contains one or more infinite values
              - the weights array contains one or more NaN values
              - the weights array contains negative values
        
        
            Does not change the internal state of the statistic.
        
            Parameters:
                values (double[]): the input array
                weights (double[]): the weights array
                mean (double): the precomputed weighted mean value
        
            Returns:
                the variance of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the parameters are not valid
        
            Since:
                2.1
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float, int: int, int2: int) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
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
        
            If all values are available, it is more accurate to use null rather than adding values one at a time using this method
            and then executing :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Variance.getResult`, since
            :code:`evaluate` leverages the fact that is has the full list of values together to execute a two-pass algorithm. See
            :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Variance`.
        
            Note also that when :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.Variance.Variance` is used to create a
            Variance, this method does nothing. In that case, the SecondMoment should be incremented directly.
        
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
    def isBiasCorrected(self) -> bool:
        """
        
            Returns:
                Returns the isBiasCorrected.
        
        
        """
        ...
    def setBiasCorrected(self, boolean: bool) -> None:
        """
        
            Parameters:
                biasCorrected (boolean): The isBiasCorrected to set.
        
        
        """
        ...

class VectorialCovariance(java.io.Serializable):
    """
    public class VectorialCovariance extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Returns the covariance matrix of the available vectors.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int, boolean: bool): ...
    def clear(self) -> None:
        """
            Clears the internal state of the Statistic
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getN(self) -> int:
        """
            Get the number of vectors in the sample.
        
            Returns:
                number of vectors in the sample
        
        
        """
        ...
    def getResult(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Get the covariance matrix.
        
            Returns:
                covariance matrix
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def increment(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Add a new vector to the sample.
        
            Parameters:
                v (double[]): vector to add
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the vector does not have the right dimension
        
        
        """
        ...

class VectorialMean(java.io.Serializable):
    """
    public class VectorialMean extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Returns the arithmetic mean of the available vectors.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getN(self) -> int:
        """
            Get the number of vectors in the sample.
        
            Returns:
                number of vectors in the sample
        
        
        """
        ...
    def getResult(self) -> typing.MutableSequence[float]:
        """
            Get the mean vector.
        
            Returns:
                mean vector
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def increment(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Add a new vector to the sample.
        
            Parameters:
                v (double[]): vector to add
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the vector does not have the right dimension
        
        
        """
        ...

class FirstMoment: ...

class FourthMoment: ...

class ThirdMoment: ...

class SecondMoment(FirstMoment):
    """
    public class SecondMoment extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
    
        Computes a statistic related to the Second Central Moment. Specifically, what is computed is the sum of squared
        deviations from the sample mean.
    
        The following recursive updating formula is used:
    
        Let
    
          - dev = (current obs - previous mean)
          - n = number of observations (including current obs)
    
        Then
    
        new value = old value + dev^2 * (n -1) / n.
    
        Returns :code:`Double.NaN` if no data values have been added and returns :code:`0` if there is just one value in the
        data set.
    
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, secondMoment: 'SecondMoment'): ...
    def clear(self) -> None:
        """
            Clears the internal state of the Statistic
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.clear` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
        
        """
        ...
    @typing.overload
    def copy(self) -> 'SecondMoment':
        """
            Returns a copy of the statistic with the same internal state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Returns:
                a copy of the statistic
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(firstMoment: FirstMoment, firstMoment2: FirstMoment) -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.SecondMoment`): SecondMoment to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.moment.SecondMoment`): SecondMoment to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (fr.cnes.sirius.patrius.math.stat.descriptive.moment.FirstMoment): FirstMoment to copy
                dest (fr.cnes.sirius.patrius.math.stat.descriptive.moment.FirstMoment): FirstMoment to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(secondMoment: 'SecondMoment', secondMoment2: 'SecondMoment') -> None: ...
    def getResult(self) -> float:
        """
            Returns the current value of the Statistic.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getResult` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
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
        
            Parameters:
                d (double): the new value.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.stat.descriptive.moment")``.

    FirstMoment: typing.Type[FirstMoment]
    FourthMoment: typing.Type[FourthMoment]
    GeometricMean: typing.Type[GeometricMean]
    Kurtosis: typing.Type[Kurtosis]
    Mean: typing.Type[Mean]
    SecondMoment: typing.Type[SecondMoment]
    SemiVariance: typing.Type[SemiVariance]
    Skewness: typing.Type[Skewness]
    StandardDeviation: typing.Type[StandardDeviation]
    ThirdMoment: typing.Type[ThirdMoment]
    Variance: typing.Type[Variance]
    VectorialCovariance: typing.Type[VectorialCovariance]
    VectorialMean: typing.Type[VectorialMean]
