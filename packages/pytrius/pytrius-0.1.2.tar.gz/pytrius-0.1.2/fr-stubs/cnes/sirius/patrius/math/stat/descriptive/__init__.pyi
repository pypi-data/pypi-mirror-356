
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.stat.descriptive.moment
import fr.cnes.sirius.patrius.math.stat.descriptive.rank
import fr.cnes.sirius.patrius.math.stat.descriptive.summary
import fr.cnes.sirius.patrius.math.util
import java.io
import java.util
import jpype
import typing



class StatisticalMultivariateSummary:
    """
    public interface StatisticalMultivariateSummary
    
        Reporting interface for basic multivariate statistics.
    
        Since:
            1.2
    """
    def getCovariance(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the covariance of the available values.
        
            Returns:
                The covariance, null if no multivariate sample have been added or a zeroed matrix for a single value set.
        
        
        """
        ...
    def getDimension(self) -> int:
        """
            Returns the dimension of the data
        
            Returns:
                The dimension of the data
        
        
        """
        ...
    def getGeometricMean(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the geometric mean of the i :sup:`th` entries of the arrays that correspond
            to each multivariate sample
        
            Returns:
                the array of component geometric means
        
        
        """
        ...
    def getMax(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the maximum of the i :sup:`th` entries of the arrays that correspond to each
            multivariate sample
        
            Returns:
                the array of component maxima
        
        
        """
        ...
    def getMean(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the mean of the i :sup:`th` entries of the arrays that correspond to each
            multivariate sample
        
            Returns:
                the array of component means
        
        
        """
        ...
    def getMin(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the minimum of the i :sup:`th` entries of the arrays that correspond to each
            multivariate sample
        
            Returns:
                the array of component minima
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of available values
        
            Returns:
                The number of available values
        
        
        """
        ...
    def getStandardDeviation(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the standard deviation of the i :sup:`th` entries of the arrays that
            correspond to each multivariate sample
        
            Returns:
                the array of component standard deviations
        
        
        """
        ...
    def getSum(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the sum of the i :sup:`th` entries of the arrays that correspond to each
            multivariate sample
        
            Returns:
                the array of component sums
        
        
        """
        ...
    def getSumLog(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the sum of logs of the i :sup:`th` entries of the arrays that correspond to
            each multivariate sample
        
            Returns:
                the array of component log sums
        
        
        """
        ...
    def getSumSq(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the sum of squares of the i :sup:`th` entries of the arrays that correspond
            to each multivariate sample
        
            Returns:
                the array of component sums of squares
        
        
        """
        ...

class StatisticalSummary:
    """
    public interface StatisticalSummary
    
        Reporting interface for basic univariate statistics.
    """
    def getMax(self) -> float:
        """
            Returns the maximum of the available values
        
            Returns:
                The max or Double.NaN if no values have been added.
        
        
        """
        ...
    def getMean(self) -> float:
        """
            Returns the ` arithmetic mean <http://www.xycoon.com/arithmetic_mean.htm>` of the available values
        
            Returns:
                The mean or Double.NaN if no values have been added.
        
        
        """
        ...
    def getMin(self) -> float:
        """
            Returns the minimum of the available values
        
            Returns:
                The min or Double.NaN if no values have been added.
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of available values
        
            Returns:
                The number of available values
        
        
        """
        ...
    def getStandardDeviation(self) -> float:
        """
            Returns the standard deviation of the available values.
        
            Returns:
                The standard deviation, Double.NaN if no values have been added or 0.0 for a single value set.
        
        
        """
        ...
    def getSum(self) -> float:
        """
            Returns the sum of the values that have been added to Univariate.
        
            Returns:
                The sum or Double.NaN if no values have been added
        
        
        """
        ...
    def getVariance(self) -> float:
        """
            Returns the variance of the available values.
        
            Returns:
                The variance, Double.NaN if no values have been added or 0.0 for a single value set.
        
        
        """
        ...

class UnivariateStatistic(fr.cnes.sirius.patrius.math.util.MathArrays.Function):
    """
    public interface UnivariateStatistic extends :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
    
        Base interface implemented by all statistics.
    """
    def copy(self) -> 'UnivariateStatistic':
        """
            Returns a copy of the statistic with the same internal state.
        
            Returns:
                a copy of the statistic
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Returns the result of evaluating the statistic over the input array.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Parameters:
                values (double[]): input array
        
            Returns:
                the value of the statistic applied to the input array
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if values is null
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float:
        """
            Returns the result of evaluating the statistic over the specified entries in the input array.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Parameters:
                values (double[]): the input array
                begin (int): the index of the first element to include
                length (int): the number of elements to include
        
            Returns:
                the value of the statistic applied to the included array entries
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if values is null or the indices are invalid
        
        
        """
        ...

class WeightedEvaluation:
    """
    public interface WeightedEvaluation
    
        Weighted evaluation for statistics.
    
        Since:
            2.1
    """
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Returns the result of evaluating the statistic over the input array, using the supplied weights.
        
            Parameters:
                values (double[]): input array
                weights (double[]): array of weights
        
            Returns:
                the value of the weighted statistic applied to the input array
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if either array is null, lengths do not match, weights contain NaN, negative or infinite values, or weights does not
                    include at least on positive value
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float:
        """
            Returns the result of evaluating the statistic over the specified entries in the input array, using corresponding
            entries in the supplied weights array.
        
            Parameters:
                values (double[]): the input array
                weights (double[]): array of weights
                begin (int): the index of the first element to include
                length (int): the number of elements to include
        
            Returns:
                the value of the weighted statistic applied to the included array entries
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if either array is null, lengths do not match, indices are invalid, weights contain NaN, negative or infinite values, or
                    weights does not include at least on positive value
        
        
        """
        ...

class AbstractUnivariateStatistic(UnivariateStatistic):
    """
    public abstract class AbstractUnivariateStatistic extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
    
        Abstract base class for all implementations of the
        :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic` interface.
    
        Provides a default implementation of :code:`evaluate(double[]),` delegating to :code:`evaluate(double[], int, int)` in
        the natural way.
    
        Also includes a :code:`test` method that performs generic parameter validation for the :code:`evaluate` methods.
    """
    def __init__(self): ...
    def copy(self) -> UnivariateStatistic:
        """
            Returns a copy of the statistic with the same internal state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Returns:
                a copy of the statistic
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float:
        """
            Returns the result of evaluating the statistic over the specified entries in the input array.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Parameters:
                values (double[]): the input array
                begin (int): the index of the first element to include
                length (int): the number of elements to include
        
            Returns:
                the value of the statistic applied to the included array entries
        
        
        """
        ...
    @typing.overload
    def evaluate(self) -> float:
        """
            Returns the result of evaluating the statistic over the stored data.
        
            The stored array is the one which was set by previous calls to null.
        
            Returns:
                the value of the statistic applied to the stored data
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the stored data array is null
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Returns the result of evaluating the statistic over the input array.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Parameters:
                values (double[]): input array
        
            Returns:
                the value of the statistic applied to the input array
        
        """
        ...
    def getData(self) -> typing.MutableSequence[float]:
        """
            Get a copy of the stored data array.
        
            Returns:
                copy of the stored data array (may be null)
        
        
        """
        ...
    @typing.overload
    def setData(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set the data array.
        
            The stored value is a copy of the parameter array, not the array itself.
        
            Parameters:
                values (double[]): data array to store (may be null to remove stored data)
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractUnivariateStatistic.evaluate`
        
        """
        ...
    @typing.overload
    def setData(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> None:
        """
            Set the data array. The input array is copied, not referenced.
        
            Parameters:
                values (double[]): data array to store
                begin (int): the index of the first element to include
                length (int): the number of elements to include
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if values is null or the indices are not valid
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractUnivariateStatistic.evaluate`
        
        
        """
        ...

class AggregateSummaryStatistics(StatisticalSummary, java.io.Serializable):
    """
    public class AggregateSummaryStatistics extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        An aggregator for :code:`SummaryStatistics` from several data sets or data set partitions. In its simplest usage mode,
        the client creates an instance via the zero-argument constructor, then uses
        :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AggregateSummaryStatistics.createContributingStatistics` to obtain
        a :code:`SummaryStatistics` for each individual data set / partition. The per-set statistics objects are used as normal,
        and at any time the aggregate statistics for all the contributors can be obtained from this object.
    
        Clients with specialized requirements can use alternative constructors to control the statistics implementations and
        initial values used by the contributing and the internal aggregate :code:`SummaryStatistics` objects.
    
        A static :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AggregateSummaryStatistics.aggregate` method is also
        included that computes aggregate statistics directly from a Collection of SummaryStatistics instances.
    
        When :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AggregateSummaryStatistics.createContributingStatistics` is
        used to create SummaryStatistics instances to be aggregated concurrently, the created instances'
        :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` methods must synchronize on the
        aggregating instance maintained by this class. In multithreaded environments, if the functionality provided by
        :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AggregateSummaryStatistics.aggregate` is adequate, that method
        should be used to avoid unnecessary computation and synchronization delays.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, summaryStatistics: 'SummaryStatistics'): ...
    @typing.overload
    def __init__(self, summaryStatistics: 'SummaryStatistics', summaryStatistics2: 'SummaryStatistics'): ...
    @staticmethod
    def aggregate(collection: typing.Union[java.util.Collection['SummaryStatistics'], typing.Sequence['SummaryStatistics'], typing.Set['SummaryStatistics']]) -> 'StatisticalSummaryValues': ...
    def createContributingStatistics(self) -> 'SummaryStatistics':
        """
            Creates and returns a :code:`SummaryStatistics` whose data will be aggregated with those of this
            :code:`AggregateSummaryStatistics`.
        
            Returns:
                a :code:`SummaryStatistics` whose data will be aggregated with those of this :code:`AggregateSummaryStatistics`. The
                initial state is a copy of the configured prototype statistics.
        
        
        """
        ...
    def getGeometricMean(self) -> float:
        """
            Returns the geometric mean of all the aggregated data.
        
            Returns:
                the geometric mean
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getGeometricMean`
        
        
        """
        ...
    def getMax(self) -> float:
        """
            Returns the maximum of the available values. This version returns the maximum over all the aggregated data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMax` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The max or Double.NaN if no values have been added.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMax`
        
        
        """
        ...
    def getMean(self) -> float:
        """
            Returns the ` arithmetic mean <http://www.xycoon.com/arithmetic_mean.htm>` of the available values. This version returns
            the mean of all the aggregated data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMean` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The mean or Double.NaN if no values have been added.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMean`
        
        
        """
        ...
    def getMin(self) -> float:
        """
            Returns the minimum of the available values. This version returns the minimum over all the aggregated data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMin` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The min or Double.NaN if no values have been added.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMin`
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of available values. This version returns a count of all the aggregated data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The number of available values
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getN`
        
        
        """
        ...
    def getSecondMoment(self) -> float:
        """
            Returns a statistic related to the Second Central Moment. Specifically, what is returned is the sum of squared
            deviations from the sample mean among the all of the aggregated data.
        
            Returns:
                second central moment statistic
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getSecondMoment`
        
        
        """
        ...
    def getStandardDeviation(self) -> float:
        """
            Returns the standard deviation of the available values.. This version returns the standard deviation of all the
            aggregated data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getStandardDeviation` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The standard deviation, Double.NaN if no values have been added or 0.0 for a single value set.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getStandardDeviation`
        
        
        """
        ...
    def getSum(self) -> float:
        """
            Returns the sum of the values that have been added to Univariate.. This version returns a sum of all the aggregated
            data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getSum` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The sum or Double.NaN if no values have been added
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getSum`
        
        
        """
        ...
    def getSumOfLogs(self) -> float:
        """
            Returns the sum of the logs of all the aggregated data.
        
            Returns:
                the sum of logs
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getSumOfLogs`
        
        
        """
        ...
    def getSummary(self) -> StatisticalSummary:
        """
            Return a :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummaryValues` instance reporting current
            aggregate statistics.
        
            Returns:
                Current values of aggregate statistics
        
        
        """
        ...
    def getSumsq(self) -> float:
        """
            Returns the sum of the squares of all the aggregated data.
        
            Returns:
                The sum of squares
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getSumsq`
        
        
        """
        ...
    def getVariance(self) -> float:
        """
            Returns the variance of the available values.. This version returns the variance of all the aggregated data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getVariance` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The variance, Double.NaN if no values have been added or 0.0 for a single value set.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getVariance`
        
        
        """
        ...

class DescriptiveStatistics(StatisticalSummary, java.io.Serializable):
    """
    public class DescriptiveStatistics extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Maintains a dataset of values of a single variable and computes descriptive statistics based on stored data. The
        :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.getWindowSize` property sets a limit on the
        number of values that can be stored in the dataset. The default value, INFINITE_WINDOW, puts no limit on the size of the
        dataset. This value should be used with caution, as the backing store will grow without bound in this case. For very
        large datasets, :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`, which does not store the
        dataset, should be used instead of this class. If :code:`windowSize` is not INFINITE_WINDOW and more values are added
        than can be stored in the dataset, new values are added in a "rolling" manner, with new values replacing the "oldest"
        values in the dataset.
    
        Note: this class is not threadsafe. Use
        :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SynchronizedDescriptiveStatistics` if concurrent access from
        multiple threads is required.
    
        Also see:
            :meth:`~serialized`
    """
    INFINITE_WINDOW: typing.ClassVar[int] = ...
    """
    public static final int INFINITE_WINDOW
    
        Represents an infinite window size. When the
        :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.getWindowSize` returns this value, there is
        no limit to the number of data values that can be stored in the dataset.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, descriptiveStatistics: 'DescriptiveStatistics'): ...
    @typing.overload
    def __init__(self, int: int): ...
    def addValue(self, double: float) -> None:
        """
            Adds the value to the dataset. If the dataset is at the maximum size (i.e., the number of stored elements equals the
            currently configured windowSize), the first (oldest) element in the dataset is discarded to make room for the new value.
        
            Parameters:
                v (double): the value to be added
        
        
        """
        ...
    def apply(self, univariateStatistic: UnivariateStatistic) -> float:
        """
            Apply the given statistic to the data associated with this set of statistics.
        
            Parameters:
                stat (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the statistic to apply
        
            Returns:
                the computed value of the statistic.
        
        
        """
        ...
    def clear(self) -> None:
        """
            Resets all statistics and storage
        
        """
        ...
    @typing.overload
    def copy(self) -> 'DescriptiveStatistics':
        """
            Returns a copy of this DescriptiveStatistics instance with the same internal state.
        
            Returns:
                a copy of this
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(descriptiveStatistics: 'DescriptiveStatistics', descriptiveStatistics2: 'DescriptiveStatistics') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`): DescriptiveStatistics to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`): DescriptiveStatistics to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    def getElement(self, int: int) -> float:
        """
            Returns the element at the specified index
        
            Parameters:
                index (int): The Index of the element
        
            Returns:
                return the element at the specified index
        
        
        """
        ...
    def getGeometricMean(self) -> float:
        """
            Returns the ` geometric mean <http://www.xycoon.com/geometric_mean.htm>` of the available values
        
            Returns:
                The geometricMean, Double.NaN if no values have been added, or if the product of the available values is less than or
                equal to 0.
        
        
        """
        ...
    def getGeometricMeanImpl(self) -> UnivariateStatistic:
        """
            Returns the currently configured geometric mean implementation.
        
            Returns:
                the UnivariateStatistic implementing the geometric mean
        
            Since:
                1.2
        
        
        """
        ...
    def getKurtosis(self) -> float:
        """
            Returns the Kurtosis of the available values. Kurtosis is a measure of the "peakedness" of a distribution
        
            Returns:
                The kurtosis, Double.NaN if no values have been added, or 0.0 for a value set <=3.
        
        
        """
        ...
    def getKurtosisImpl(self) -> UnivariateStatistic:
        """
            Returns the currently configured kurtosis implementation.
        
            Returns:
                the UnivariateStatistic implementing the kurtosis
        
            Since:
                1.2
        
        
        """
        ...
    def getMax(self) -> float:
        """
            Returns the maximum of the available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMax` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The max or Double.NaN if no values have been added.
        
        
        """
        ...
    def getMaxImpl(self) -> UnivariateStatistic:
        """
            Returns the currently configured maximum implementation.
        
            Returns:
                the UnivariateStatistic implementing the maximum
        
            Since:
                1.2
        
        
        """
        ...
    def getMean(self) -> float:
        """
            Returns the ` arithmetic mean <http://www.xycoon.com/arithmetic_mean.htm>` of the available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMean` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The mean or Double.NaN if no values have been added.
        
        
        """
        ...
    def getMeanImpl(self) -> UnivariateStatistic:
        """
            Returns the currently configured mean implementation.
        
            Returns:
                the UnivariateStatistic implementing the mean
        
            Since:
                1.2
        
        
        """
        ...
    def getMin(self) -> float:
        """
            Returns the minimum of the available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMin` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The min or Double.NaN if no values have been added.
        
        
        """
        ...
    def getMinImpl(self) -> UnivariateStatistic:
        """
            Returns the currently configured minimum implementation.
        
            Returns:
                the UnivariateStatistic implementing the minimum
        
            Since:
                1.2
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The number of available values
        
        
        """
        ...
    def getPercentile(self, double: float) -> float:
        """
            Returns an estimate for the pth percentile of the stored values.
        
            The implementation provided here follows the first estimation procedure presented `here.
            <http://www.itl.nist.gov/div898/handbook/prc/section2/prc252.htm>`
        
            **Preconditions**:
        
              - :code:`0 < p ≤ 100` (otherwise an :code:`MathIllegalArgumentException` is thrown)
              - at least one value must be stored (returns :code:`Double.NaN` otherwise)
        
        
            Parameters:
                p (double): the requested percentile (scaled from 0 - 100)
        
            Returns:
                An estimate for the pth percentile of the stored data
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if percentile implementation has been overridden and the supplied implementation does not support setQuantile
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if p is not a valid quantile
        
        
        """
        ...
    def getPercentileImpl(self) -> UnivariateStatistic:
        """
            Returns the currently configured percentile implementation.
        
            Returns:
                the UnivariateStatistic implementing the percentile
        
            Since:
                1.2
        
        
        """
        ...
    def getPopulationVariance(self) -> float:
        """
            Returns the ` population variance <http://en.wikibooks.org/wiki/Statistics/Summary/Variance>` of the available values.
        
            Returns:
                The population variance, Double.NaN if no values have been added, or 0.0 for a single value set.
        
        
        """
        ...
    def getSkewness(self) -> float:
        """
            Returns the skewness of the available values. Skewness is a measure of the asymmetry of a given distribution.
        
            Returns:
                The skewness, Double.NaN if no values have been added or 0.0 for a value set <=2.
        
        
        """
        ...
    def getSkewnessImpl(self) -> UnivariateStatistic:
        """
            Returns the currently configured skewness implementation.
        
            Returns:
                the UnivariateStatistic implementing the skewness
        
            Since:
                1.2
        
        
        """
        ...
    def getSortedValues(self) -> typing.MutableSequence[float]:
        """
            Returns the current set of values in an array of double primitives, sorted in ascending order. The returned array is a
            fresh copy of the underlying data -- i.e., it is not a reference to the stored data.
        
            Returns:
                returns the current set of numbers sorted in ascending order
        
        
        """
        ...
    def getStandardDeviation(self) -> float:
        """
            Returns the standard deviation of the available values.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getStandardDeviation` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The standard deviation, Double.NaN if no values have been added or 0.0 for a single value set.
        
        
        """
        ...
    def getSum(self) -> float:
        """
            Returns the sum of the values that have been added to Univariate.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getSum` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The sum or Double.NaN if no values have been added
        
        
        """
        ...
    def getSumImpl(self) -> UnivariateStatistic:
        """
            Returns the currently configured sum implementation.
        
            Returns:
                the UnivariateStatistic implementing the sum
        
            Since:
                1.2
        
        
        """
        ...
    def getSumsq(self) -> float:
        """
            Returns the sum of the squares of the available values.
        
            Returns:
                The sum of the squares or Double.NaN if no values have been added.
        
        
        """
        ...
    def getSumsqImpl(self) -> UnivariateStatistic:
        """
            Returns the currently configured sum of squares implementation.
        
            Returns:
                the UnivariateStatistic implementing the sum of squares
        
            Since:
                1.2
        
        
        """
        ...
    def getValues(self) -> typing.MutableSequence[float]:
        """
            Returns the current set of values in an array of double primitives. The order of addition is preserved. The returned
            array is a fresh copy of the underlying data -- i.e., it is not a reference to the stored data.
        
            Returns:
                returns the current set of numbers in the order in which they were added to this set
        
        
        """
        ...
    def getVariance(self) -> float:
        """
            Returns the (sample) variance of the available values.
        
            This method returns the bias-corrected sample variance (using :code:`n - 1` in the denominator). Use
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.getPopulationVariance` for the
            non-bias-corrected population variance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getVariance` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The variance, Double.NaN if no values have been added or 0.0 for a single value set.
        
        
        """
        ...
    def getVarianceImpl(self) -> UnivariateStatistic:
        """
            Returns the currently configured variance implementation.
        
            Returns:
                the UnivariateStatistic implementing the variance
        
            Since:
                1.2
        
        
        """
        ...
    def getWindowSize(self) -> int:
        """
            Returns the maximum number of values that can be stored in the dataset, or INFINITE_WINDOW (-1) if there is no limit.
        
            Returns:
                The current window size or -1 if its Infinite.
        
        
        """
        ...
    def removeMostRecentValue(self) -> None:
        """
            Removes the most recent value from the dataset.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if there are no elements stored
        
        
        """
        ...
    def replaceMostRecentValue(self, double: float) -> float:
        """
            Replaces the most recently stored value with the given value. There must be at least one element stored to call this
            method.
        
            Parameters:
                v (double): the value to replace the most recent stored value
        
            Returns:
                replaced value
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if there are no elements stored
        
        
        """
        ...
    def setGeometricMeanImpl(self, univariateStatistic: UnivariateStatistic) -> None:
        """
        
            Sets the implementation for the gemoetric mean.
        
            Parameters:
                geometricMeanImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the UnivariateStatistic instance to use for computing the geometric mean
        
            Since:
                1.2
        
        
        """
        ...
    def setKurtosisImpl(self, univariateStatistic: UnivariateStatistic) -> None:
        """
        
            Sets the implementation for the kurtosis.
        
            Parameters:
                kurtosisImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the UnivariateStatistic instance to use for computing the kurtosis
        
            Since:
                1.2
        
        
        """
        ...
    def setMaxImpl(self, univariateStatistic: UnivariateStatistic) -> None:
        """
        
            Sets the implementation for the maximum.
        
            Parameters:
                maxImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the UnivariateStatistic instance to use for computing the maximum
        
            Since:
                1.2
        
        
        """
        ...
    def setMeanImpl(self, univariateStatistic: UnivariateStatistic) -> None:
        """
        
            Sets the implementation for the mean.
        
            Parameters:
                meanImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the UnivariateStatistic instance to use for computing the mean
        
            Since:
                1.2
        
        
        """
        ...
    def setMinImpl(self, univariateStatistic: UnivariateStatistic) -> None:
        """
        
            Sets the implementation for the minimum.
        
            Parameters:
                minImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the UnivariateStatistic instance to use for computing the minimum
        
            Since:
                1.2
        
        
        """
        ...
    def setPercentileImpl(self, univariateStatistic: UnivariateStatistic) -> None:
        """
            Sets the implementation to be used by
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.getPercentile`. The supplied
            :code:`UnivariateStatistic` must provide a :code:`setQuantile(double)` method; otherwise
            :code:`IllegalArgumentException` is thrown.
        
            Parameters:
                percentileImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the percentileImpl to set
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the supplied implementation does not provide a :code:`setQuantile` method
        
            Since:
                1.2
        
        
        """
        ...
    def setSkewnessImpl(self, univariateStatistic: UnivariateStatistic) -> None:
        """
        
            Sets the implementation for the skewness.
        
            Parameters:
                skewnessImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the UnivariateStatistic instance to use for computing the skewness
        
            Since:
                1.2
        
        
        """
        ...
    def setSumImpl(self, univariateStatistic: UnivariateStatistic) -> None:
        """
        
            Sets the implementation for the sum.
        
            Parameters:
                sumImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the UnivariateStatistic instance to use for computing the sum
        
            Since:
                1.2
        
        
        """
        ...
    def setSumsqImpl(self, univariateStatistic: UnivariateStatistic) -> None:
        """
        
            Sets the implementation for the sum of squares.
        
            Parameters:
                sumsqImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the UnivariateStatistic instance to use for computing the sum of squares
        
            Since:
                1.2
        
        
        """
        ...
    def setVarianceImpl(self, univariateStatistic: UnivariateStatistic) -> None:
        """
        
            Sets the implementation for the variance.
        
            Parameters:
                varianceImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the UnivariateStatistic instance to use for computing the variance
        
            Since:
                1.2
        
        
        """
        ...
    def setWindowSize(self, int: int) -> None:
        """
            WindowSize controls the number of values that contribute to the reported statistics. For example, if windowSize is set
            to 3 and the values {1,2,3,4,5} have been added **in that order** then the *available values* are {3,4,5} and all
            reported statistics will be based on these values. If :code:`windowSize` is decreased as a result of this call and there
            are more than the new value of elements in the current dataset, values from the front of the array are discarded to
            reduce the dataset to :code:`windowSize` elements.
        
            Parameters:
                windowSizeIn (int): sets the size of the window.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if window size is less than 1 but not equal to
                    :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.INFINITE_WINDOW`
        
        
        """
        ...
    def toString(self) -> str:
        """
            Generates a text report displaying univariate statistics from values that have been added. Each statistic is displayed
            on a separate line.
        
            Overrides:
                 in class 
        
            Returns:
                String with line feeds displaying statistics
        
        
        """
        ...

class MultivariateSummaryStatistics(StatisticalMultivariateSummary, java.io.Serializable):
    """
    public class MultivariateSummaryStatistics extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        Computes summary statistics for a stream of n-tuples added using the null method. The data values are not stored in
        memory, so this class can be used to compute statistics for very large n-tuple streams.
    
        The :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic` instances used to maintain
        summary state and compute statistics are configurable via setters. For example, the default implementation for the mean
        can be overridden by calling null. Actual parameters to these methods must implement the
        :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic` interface and configuration must be
        completed before :code:`addValue` is called. No configuration is necessary to use the default, commons-math provided
        implementations.
    
        To compute statistics for a stream of n-tuples, construct a MultivariateStatistics instance with dimension n and then
        use null to add n-tuples. The :code:`getXxx` methods where Xxx is a statistic return an array of :code:`double` values,
        where for :code:`i = 0,...,n-1` the i :sup:`th` array element is the value of the given statistic for data range
        consisting of the i :sup:`th` element of each of the input n-tuples. For example, if :code:`addValue` is called with
        actual parameters {0, 1, 2}, then {3, 4, 5} and finally {6, 7, 8}, :code:`getSum` will return a three-element array with
        values {0+3+6, 1+4+7, 2+5+8}
    
        Note: This class is not thread-safe. Use
        :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SynchronizedMultivariateSummaryStatistics` if concurrent access
        from multiple threads is required.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int, boolean: bool): ...
    def addValue(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Add an n-tuple to the data
        
            Parameters:
                value (double[]): the n-tuple to add
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the length of the array does not match the one used at construction
        
        
        """
        ...
    def clear(self) -> None:
        """
            Resets all statistics and storage
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
            Returns true iff :code:`object` is a :code:`MultivariateSummaryStatistics` instance and all statistics have the same
            values as this.
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the object to test equality against.
        
            Returns:
                true if object equals this
        
        
        """
        ...
    def getCovariance(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the covariance matrix of the values that have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getCovariance` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Returns:
                the covariance matrix
        
        
        """
        ...
    def getDimension(self) -> int:
        """
            Returns the dimension of the data
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getDimension` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Returns:
                The dimension of the data
        
        
        """
        ...
    def getGeoMeanImpl(self) -> typing.MutableSequence['StorelessUnivariateStatistic']:
        """
            Returns the currently configured geometric mean implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the geometric mean
        
        
        """
        ...
    def getGeometricMean(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the geometric mean of the i :sup:`th` entries of the arrays that have been
            added using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getGeometricMean` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Returns:
                the array of component geometric means
        
        
        """
        ...
    def getMax(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the maximum of the i :sup:`th` entries of the arrays that have been added
            using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getMax` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Returns:
                the array of component maxima
        
        
        """
        ...
    def getMaxImpl(self) -> typing.MutableSequence['StorelessUnivariateStatistic']:
        """
            Returns the currently configured maximum implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the maximum
        
        
        """
        ...
    def getMean(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the mean of the i :sup:`th` entries of the arrays that have been added using
            null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getMean` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Returns:
                the array of component means
        
        
        """
        ...
    def getMeanImpl(self) -> typing.MutableSequence['StorelessUnivariateStatistic']:
        """
            Returns the currently configured mean implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the mean
        
        
        """
        ...
    def getMin(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the minimum of the i :sup:`th` entries of the arrays that have been added
            using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getMin` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Returns:
                the array of component minima
        
        
        """
        ...
    def getMinImpl(self) -> typing.MutableSequence['StorelessUnivariateStatistic']:
        """
            Returns the currently configured minimum implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the minimum
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Returns:
                The number of available values
        
        
        """
        ...
    def getStandardDeviation(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the standard deviation of the i :sup:`th` entries of the arrays that have
            been added using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getStandardDeviation` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Returns:
                the array of component standard deviations
        
        
        """
        ...
    def getSum(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the sum of the i :sup:`th` entries of the arrays that have been added using
            null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getSum` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Returns:
                the array of component sums
        
        
        """
        ...
    def getSumImpl(self) -> typing.MutableSequence['StorelessUnivariateStatistic']:
        """
            Returns the currently configured Sum implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the sum
        
        
        """
        ...
    def getSumLog(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the sum of logs of the i :sup:`th` entries of the arrays that have been
            added using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getSumLog` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Returns:
                the array of component log sums
        
        
        """
        ...
    def getSumLogImpl(self) -> typing.MutableSequence['StorelessUnivariateStatistic']:
        """
            Returns the currently configured sum of logs implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the log sum
        
        
        """
        ...
    def getSumSq(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the sum of squares of the i :sup:`th` entries of the arrays that have been
            added using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getSumSq` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Returns:
                the array of component sums of squares
        
        
        """
        ...
    def getSumsqImpl(self) -> typing.MutableSequence['StorelessUnivariateStatistic']:
        """
            Returns the currently configured sum of squares implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the sum of squares
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Returns hash code based on values of statistics
        
            Overrides:
                 in class 
        
            Returns:
                hash code
        
        
        """
        ...
    def setGeoMeanImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List['StorelessUnivariateStatistic'], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the geometric mean.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                geoMeanImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the geometric mean
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array dimension does not match the one used at construction
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
        
        """
        ...
    def setMaxImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List['StorelessUnivariateStatistic'], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the maximum.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                maxImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the maximum
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array dimension does not match the one used at construction
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
        
        """
        ...
    def setMeanImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List['StorelessUnivariateStatistic'], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the mean.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                meanImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the mean
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array dimension does not match the one used at construction
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
        
        """
        ...
    def setMinImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List['StorelessUnivariateStatistic'], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the minimum.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                minImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the minimum
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array dimension does not match the one used at construction
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
        
        """
        ...
    def setSumImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List['StorelessUnivariateStatistic'], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the Sum.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                sumImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the Sum
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array dimension does not match the one used at construction
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
        
        """
        ...
    def setSumLogImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List['StorelessUnivariateStatistic'], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the sum of logs.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                sumLogImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the log sum
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array dimension does not match the one used at construction
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
        
        """
        ...
    def setSumsqImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List['StorelessUnivariateStatistic'], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the sum of squares.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                sumsqImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the sum of squares
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array dimension does not match the one used at construction
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
        
        """
        ...
    def toString(self) -> str:
        """
            Generates a text report displaying summary statistics from values that have been added.
        
            Overrides:
                 in class 
        
            Returns:
                String with line feeds displaying statistics
        
        
        """
        ...

class StatisticalSummaryValues(java.io.Serializable, StatisticalSummary):
    """
    public class StatisticalSummaryValues extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
    
        Value object representing the results of a univariate statistical summary.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, long: int, double3: float, double4: float, double5: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Returns true iff :code:`object` is a :code:`StatisticalSummaryValues` instance and all statistics have the same values
            as this.
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the object to test equality against.
        
            Returns:
                true if object equals this
        
        
        """
        ...
    def getMax(self) -> float:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMax`
            Returns the maximum of the available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMax` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                Returns the max.
        
        
        """
        ...
    def getMean(self) -> float:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMean`
            Returns the ` arithmetic mean <http://www.xycoon.com/arithmetic_mean.htm>` of the available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMean` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                Returns the mean.
        
        
        """
        ...
    def getMin(self) -> float:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMin`
            Returns the minimum of the available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMin` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                Returns the min.
        
        
        """
        ...
    def getN(self) -> int:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getN`
            Returns the number of available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                Returns the number of values.
        
        
        """
        ...
    def getStandardDeviation(self) -> float:
        """
            Description copied from
            interface: :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getStandardDeviation`
            Returns the standard deviation of the available values.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getStandardDeviation` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                Returns the standard deviation
        
        
        """
        ...
    def getSum(self) -> float:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getSum`
            Returns the sum of the values that have been added to Univariate.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getSum` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                Returns the sum.
        
        
        """
        ...
    def getVariance(self) -> float:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getVariance`
            Returns the variance of the available values.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getVariance` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                Returns the variance.
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Returns hash code based on values of statistics
        
            Overrides:
                 in class 
        
            Returns:
                hash code
        
        
        """
        ...
    def toString(self) -> str:
        """
            Generates a text report displaying values of statistics. Each statistic is displayed on a separate line.
        
            Overrides:
                 in class 
        
            Returns:
                String with line feeds displaying statistics
        
        
        """
        ...

class StorelessUnivariateStatistic(UnivariateStatistic):
    """
    public interface StorelessUnivariateStatistic extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
    
        Extends the definition of :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic` with
        :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.increment` and null methods for adding
        values and updating internal state.
    
        This interface is designed to be used for calculating statistics that can be computed in one pass through the data
        without storing the full array of sample values.
    """
    def clear(self) -> None:
        """
            Clears the internal state of the Statistic
        
        """
        ...
    def copy(self) -> 'StorelessUnivariateStatistic':
        """
            Returns a copy of the statistic with the same internal state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Returns:
                a copy of the statistic
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of values that have been added.
        
            Returns:
                the number of values.
        
        
        """
        ...
    def getResult(self) -> float:
        """
            Returns the current value of the Statistic.
        
            Returns:
                value of the statistic, :code:`Double.NaN` if it has been cleared or just instantiated.
        
        
        """
        ...
    def increment(self, double: float) -> None:
        """
            Updates the internal state of the statistic to reflect the addition of the new value.
        
            Parameters:
                d (double): the new value.
        
        
        """
        ...
    @typing.overload
    def incrementAll(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Updates the internal state of the statistic to reflect addition of all values in the values array. Does not clear the
            statistic first -- i.e., the values are added **incrementally** to the dataset.
        
            Parameters:
                values (double[]): array holding the new values to add
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null
        
        """
        ...
    @typing.overload
    def incrementAll(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> None:
        """
            Updates the internal state of the statistic to reflect addition of the values in the designated portion of the values
            array. Does not clear the statistic first -- i.e., the values are added **incrementally** to the dataset.
        
            Parameters:
                values (double[]): array holding the new values to add
                start (int): the array index of the first value to add
                length (int): the number of elements to add
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the index
        
        
        """
        ...

class SummaryStatistics(StatisticalSummary, java.io.Serializable):
    """
    public class SummaryStatistics extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        Computes summary statistics for a stream of data values added using the
        :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` method. The data values are not stored
        in memory, so this class can be used to compute statistics for very large data streams.
    
        The :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic` instances used to maintain
        summary state and compute statistics are configurable via setters. For example, the default implementation for the
        variance can be overridden by calling
        :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.setVarianceImpl`. Actual parameters to these
        methods must implement the :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic` interface
        and configuration must be completed before :code:`addValue` is called. No configuration is necessary to use the default,
        commons-math provided implementations.
    
        Note: This class is not thread-safe. Use
        :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SynchronizedSummaryStatistics` if concurrent access from multiple
        threads is required.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, summaryStatistics: 'SummaryStatistics'): ...
    def addValue(self, double: float) -> None:
        """
            Add a value to the data
        
            Parameters:
                value (double): the value to add
        
        
        """
        ...
    def clear(self) -> None:
        """
            Resets all statistics and storage
        
        """
        ...
    @typing.overload
    def copy(self) -> 'SummaryStatistics':
        """
            Returns a copy of this SummaryStatistics instance with the same internal state.
        
            Returns:
                a copy of this
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(summaryStatistics: 'SummaryStatistics', summaryStatistics2: 'SummaryStatistics') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                sourceIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`): SummaryStatistics to copy
                destIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`): SummaryStatistics to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
            Returns true iff :code:`object` is a :code:`SummaryStatistics` instance and all statistics have the same values as this.
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the object to test equality against.
        
            Returns:
                true if object equals this
        
        
        """
        ...
    def getGeoMeanImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured geometric mean implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the geometric mean
        
            Since:
                1.2
        
        
        """
        ...
    def getGeometricMean(self) -> float:
        """
            Returns the geometric mean of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Returns:
                the geometric mean
        
        
        """
        ...
    def getMax(self) -> float:
        """
            Returns the maximum of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMax` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                the maximum
        
        
        """
        ...
    def getMaxImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured maximum implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the maximum
        
            Since:
                1.2
        
        
        """
        ...
    def getMean(self) -> float:
        """
            Returns the mean of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMean` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                the mean
        
        
        """
        ...
    def getMeanImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured mean implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the mean
        
            Since:
                1.2
        
        
        """
        ...
    def getMin(self) -> float:
        """
            Returns the minimum of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMin` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                the minimum
        
        
        """
        ...
    def getMinImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured minimum implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the minimum
        
            Since:
                1.2
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The number of available values
        
        
        """
        ...
    def getPopulationVariance(self) -> float:
        """
            Returns the ` population variance <http://en.wikibooks.org/wiki/Statistics/Summary/Variance>` of the values that have
            been added.
        
            Double.NaN is returned if no values have been added.
        
            Returns:
                the population variance
        
        
        """
        ...
    def getSecondMoment(self) -> float:
        """
            Returns a statistic related to the Second Central Moment. Specifically, what is returned is the sum of squared
            deviations from the sample mean among the values that have been added.
        
            Returns :code:`Double.NaN` if no data values have been added and returns :code:`0` if there is just one value in the
            data set.
        
        
            Returns:
                second central moment statistic
        
            Since:
                2.0
        
        
        """
        ...
    def getStandardDeviation(self) -> float:
        """
            Returns the standard deviation of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getStandardDeviation` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                the standard deviation
        
        
        """
        ...
    def getSum(self) -> float:
        """
            Returns the sum of the values that have been added
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getSum` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                The sum or :code:`Double.NaN` if no values have been added
        
        
        """
        ...
    def getSumImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured Sum implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the sum
        
            Since:
                1.2
        
        
        """
        ...
    def getSumLogImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured sum of logs implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the log sum
        
            Since:
                1.2
        
        
        """
        ...
    def getSumOfLogs(self) -> float:
        """
            Returns the sum of the logs of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Returns:
                the sum of logs
        
            Since:
                1.2
        
        
        """
        ...
    def getSummary(self) -> StatisticalSummary:
        """
            Return a :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummaryValues` instance reporting current
            statistics.
        
            Returns:
                Current values of statistics
        
        
        """
        ...
    def getSumsq(self) -> float:
        """
            Returns the sum of the squares of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Returns:
                The sum of squares
        
        
        """
        ...
    def getSumsqImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured sum of squares implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the sum of squares
        
            Since:
                1.2
        
        
        """
        ...
    def getVariance(self) -> float:
        """
            Returns the (sample) variance of the available values.
        
            This method returns the bias-corrected sample variance (using :code:`n - 1` in the denominator). Use
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getPopulationVariance` for the non-bias-corrected
            population variance.
        
            Double.NaN is returned if no values have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getVariance` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Returns:
                the variance
        
        
        """
        ...
    def getVarianceImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured variance implementation
        
            Returns:
                the StorelessUnivariateStatistic implementing the variance
        
            Since:
                1.2
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Returns hash code based on values of statistics
        
            Overrides:
                 in class 
        
            Returns:
                hash code
        
        
        """
        ...
    def setGeoMeanImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the geometric mean.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                geoMeanImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the geometric mean
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
            Since:
                1.2
        
        
        """
        ...
    def setMaxImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the maximum.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                maxImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the maximum
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
            Since:
                1.2
        
        
        """
        ...
    def setMeanImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the mean.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                meanImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the mean
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
            Since:
                1.2
        
        
        """
        ...
    def setMinImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the minimum.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                minImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the minimum
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
            Since:
                1.2
        
        
        """
        ...
    def setSumImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the Sum.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                sumImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the Sum
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n >0)
        
            Since:
                1.2
        
        
        """
        ...
    def setSumLogImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the sum of logs.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                sumLogImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the log sum
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
            Since:
                1.2
        
        
        """
        ...
    def setSumsqImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the sum of squares.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                sumsqImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the sum of squares
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
            Since:
                1.2
        
        
        """
        ...
    def setVarianceImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the variance.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Parameters:
                varianceImplIn (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the variance
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if data has already been added (i.e if n > 0)
        
            Since:
                1.2
        
        
        """
        ...
    def toString(self) -> str:
        """
            Generates a text report displaying summary statistics from values that have been added.
        
            Overrides:
                 in class 
        
            Returns:
                String with line feeds displaying statistics
        
            Since:
                1.2
        
        
        """
        ...

class AbstractStorelessUnivariateStatistic(AbstractUnivariateStatistic, StorelessUnivariateStatistic):
    """
    public abstract class AbstractStorelessUnivariateStatistic extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractUnivariateStatistic` implements :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
    
        Abstract implementation of the :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        interface.
    
        Provides default :code:`evaluate()` and :code:`incrementAll(double[])` implementations.
    
        **Note that these implementations are not synchronized.**
    """
    def __init__(self): ...
    def clear(self) -> None:
        """
            Clears the internal state of the Statistic
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.clear` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
        
        """
        ...
    def copy(self) -> StorelessUnivariateStatistic:
        """
            Returns a copy of the statistic with the same internal state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractUnivariateStatistic.copy` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractUnivariateStatistic`
        
            Returns:
                a copy of the statistic
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
            Returns true iff :code:`object` is an :code:`AbstractStorelessUnivariateStatistic` returning the same values as this for
            :code:`getResult()` and :code:`getN()`
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): object to test equality against.
        
            Returns:
                true if object returns the same value as this
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            This default implementation calls
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.clear`, then invokes
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.increment` in a loop over the
            the input array, and then uses
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.getResult` to compute the
            return value.
        
            Note that this implementation changes the internal state of the statistic. Its side effects are the same as invoking
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.clear` and then null.
        
            Implementations may override this method with a more efficient and possibly more accurate implementation that works
            directly with the input array.
        
            If the array is null, a MathIllegalArgumentException is thrown.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractUnivariateStatistic`
        
            Parameters:
                values (double[]): input array
        
            Returns:
                the value of the statistic applied to the input array
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if values is null
        
            Also see:
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float:
        """
            This default implementation calls
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.clear`, then invokes
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.increment` in a loop over the
            specified portion of the input array, and then uses
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.getResult` to compute the
            return value.
        
            Note that this implementation changes the internal state of the statistic. Its side effects are the same as invoking
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.clear` and then null.
        
            Implementations may override this method with a more efficient and possibly more accurate implementation that works
            directly with the input array.
        
            If the array is null or the index parameters are not valid, an MathIllegalArgumentException is thrown.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Specified by:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractUnivariateStatistic`
        
            Parameters:
                values (double[]): the input array
                begin (int): the index of the first element to include
                length (int): the number of elements to include
        
            Returns:
                the value of the statistic applied to the included array entries
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the indices are not valid
        
            Also see:
        
        
        """
        ...
    @typing.overload
    def evaluate(self) -> float: ...
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
    def hashCode(self) -> int:
        """
            Returns hash code based on getResult() and getN()
        
            Overrides:
                 in class 
        
            Returns:
                hash code
        
        
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
    @typing.overload
    def incrementAll(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            This default implementation just calls
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.increment` in a loop over the
            input array.
        
            Throws IllegalArgumentException if the input values array is null.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Parameters:
                values (double[]): values to add
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if values is null
        
            Also see:
        
        """
        ...
    @typing.overload
    def incrementAll(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> None:
        """
            This default implementation just calls
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.increment` in a loop over the
            specified portion of the input array.
        
            Throws IllegalArgumentException if the input values array is null.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Parameters:
                values (double[]): array holding values to add
                begin (int): index of the first array element to add
                length (int): number of array elements to add
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if values is null
        
            Also see:
        
        
        """
        ...

class SynchronizedDescriptiveStatistics(DescriptiveStatistics):
    """
    public class SynchronizedDescriptiveStatistics extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
    
        Implementation of :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics` that is safe to use in a
        multithreaded environment. Multiple threads can safely operate on a single instance without causing runtime exceptions
        due to race conditions. In effect, this implementation makes modification and access methods atomic operations for a
        single instance. That is to say, as one thread is computing a statistic from the instance, no other thread can modify
        the instance nor compute another statistic.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, synchronizedDescriptiveStatistics: 'SynchronizedDescriptiveStatistics'): ...
    @typing.overload
    def __init__(self, int: int): ...
    def addValue(self, double: float) -> None:
        """
            Adds the value to the dataset. If the dataset is at the maximum size (i.e., the number of stored elements equals the
            currently configured windowSize), the first (oldest) element in the dataset is discarded to make room for the new value.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.addValue` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
        
            Parameters:
                v (double): the value to be added
        
        
        """
        ...
    def apply(self, univariateStatistic: UnivariateStatistic) -> float:
        """
            Apply the given statistic to the data associated with this set of statistics.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.apply` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
        
            Parameters:
                stat (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`): the statistic to apply
        
            Returns:
                the computed value of the statistic.
        
        
        """
        ...
    def clear(self) -> None:
        """
            Resets all statistics and storage
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.clear` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(descriptiveStatistics: DescriptiveStatistics, descriptiveStatistics2: DescriptiveStatistics) -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Acquires synchronization lock on source, then dest before copying.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SynchronizedDescriptiveStatistics`): SynchronizedDescriptiveStatistics to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SynchronizedDescriptiveStatistics`): SynchronizedDescriptiveStatistics to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(synchronizedDescriptiveStatistics: 'SynchronizedDescriptiveStatistics', synchronizedDescriptiveStatistics2: 'SynchronizedDescriptiveStatistics') -> None: ...
    @typing.overload
    def copy(self) -> 'SynchronizedDescriptiveStatistics':
        """
            Returns a copy of this SynchronizedDescriptiveStatistics instance with the same internal state.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.copy` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
        
            Returns:
                a copy of this
        
        """
        ...
    def getElement(self, int: int) -> float:
        """
            Returns the element at the specified index
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.getElement` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
        
            Parameters:
                index (int): The Index of the element
        
            Returns:
                return the element at the specified index
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.getN` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
        
            Returns:
                The number of available values
        
        
        """
        ...
    def getStandardDeviation(self) -> float:
        """
            Returns the standard deviation of the available values.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getStandardDeviation` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.getStandardDeviation` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
        
            Returns:
                The standard deviation, Double.NaN if no values have been added or 0.0 for a single value set.
        
        
        """
        ...
    def getValues(self) -> typing.MutableSequence[float]:
        """
            Returns the current set of values in an array of double primitives. The order of addition is preserved. The returned
            array is a fresh copy of the underlying data -- i.e., it is not a reference to the stored data.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.getValues` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
        
            Returns:
                returns the current set of numbers in the order in which they were added to this set
        
        
        """
        ...
    def getWindowSize(self) -> int:
        """
            Returns the maximum number of values that can be stored in the dataset, or INFINITE_WINDOW (-1) if there is no limit.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.getWindowSize` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
        
            Returns:
                The current window size or -1 if its Infinite.
        
        
        """
        ...
    def setWindowSize(self, int: int) -> None:
        """
            WindowSize controls the number of values that contribute to the reported statistics. For example, if windowSize is set
            to 3 and the values {1,2,3,4,5} have been added **in that order** then the *available values* are {3,4,5} and all
            reported statistics will be based on these values. If :code:`windowSize` is decreased as a result of this call and there
            are more than the new value of elements in the current dataset, values from the front of the array are discarded to
            reduce the dataset to :code:`windowSize` elements.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.setWindowSize` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
        
            Parameters:
                windowSize (int): sets the size of the window.
        
        
        """
        ...
    def toString(self) -> str:
        """
            Generates a text report displaying univariate statistics from values that have been added. Each statistic is displayed
            on a separate line.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics.toString` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.DescriptiveStatistics`
        
            Returns:
                String with line feeds displaying statistics
        
        
        """
        ...

class SynchronizedMultivariateSummaryStatistics(MultivariateSummaryStatistics):
    """
    public class SynchronizedMultivariateSummaryStatistics extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
    
        Implementation of :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics` that is safe to
        use in a multithreaded environment. Multiple threads can safely operate on a single instance without causing runtime
        exceptions due to race conditions. In effect, this implementation makes modification and access methods atomic
        operations for a single instance. That is to say, as one thread is computing a statistic from the instance, no other
        thread can modify the instance nor compute another statistic.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int, boolean: bool): ...
    def addValue(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Add an n-tuple to the data
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Parameters:
                value (double[]): the n-tuple to add
        
        
        """
        ...
    def clear(self) -> None:
        """
            Resets all statistics and storage
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.clear` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
            Returns true iff :code:`object` is a :code:`MultivariateSummaryStatistics` instance and all statistics have the same
            values as this.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.equals` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the object to test equality against.
        
            Returns:
                true if object equals this
        
        
        """
        ...
    def getCovariance(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the covariance matrix of the values that have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getCovariance` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getCovariance` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the covariance matrix
        
        
        """
        ...
    def getDimension(self) -> int:
        """
            Returns the dimension of the data
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getDimension` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getDimension` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                The dimension of the data
        
        
        """
        ...
    def getGeoMeanImpl(self) -> typing.MutableSequence[StorelessUnivariateStatistic]:
        """
            Returns the currently configured geometric mean implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getGeoMeanImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the geometric mean
        
        
        """
        ...
    def getGeometricMean(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the geometric mean of the i :sup:`th` entries of the arrays that have been
            added using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getGeometricMean` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getGeometricMean` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the array of component geometric means
        
        
        """
        ...
    def getMax(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the maximum of the i :sup:`th` entries of the arrays that have been added
            using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getMax` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getMax` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the array of component maxima
        
        
        """
        ...
    def getMaxImpl(self) -> typing.MutableSequence[StorelessUnivariateStatistic]:
        """
            Returns the currently configured maximum implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getMaxImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the maximum
        
        
        """
        ...
    def getMean(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the mean of the i :sup:`th` entries of the arrays that have been added using
            null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getMean` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getMean` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the array of component means
        
        
        """
        ...
    def getMeanImpl(self) -> typing.MutableSequence[StorelessUnivariateStatistic]:
        """
            Returns the currently configured mean implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getMeanImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the mean
        
        
        """
        ...
    def getMin(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the minimum of the i :sup:`th` entries of the arrays that have been added
            using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getMin` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getMin` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the array of component minima
        
        
        """
        ...
    def getMinImpl(self) -> typing.MutableSequence[StorelessUnivariateStatistic]:
        """
            Returns the currently configured minimum implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getMinImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the minimum
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getN` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                The number of available values
        
        
        """
        ...
    def getStandardDeviation(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the standard deviation of the i :sup:`th` entries of the arrays that have
            been added using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getStandardDeviation` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getStandardDeviation` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the array of component standard deviations
        
        
        """
        ...
    def getSum(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the sum of the i :sup:`th` entries of the arrays that have been added using
            null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getSum` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getSum` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the array of component sums
        
        
        """
        ...
    def getSumImpl(self) -> typing.MutableSequence[StorelessUnivariateStatistic]:
        """
            Returns the currently configured Sum implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getSumImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the sum
        
        
        """
        ...
    def getSumLog(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the sum of logs of the i :sup:`th` entries of the arrays that have been
            added using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getSumLog` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getSumLog` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the array of component log sums
        
        
        """
        ...
    def getSumLogImpl(self) -> typing.MutableSequence[StorelessUnivariateStatistic]:
        """
            Returns the currently configured sum of logs implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getSumLogImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the log sum
        
        
        """
        ...
    def getSumSq(self) -> typing.MutableSequence[float]:
        """
            Returns an array whose i :sup:`th` entry is the sum of squares of the i :sup:`th` entries of the arrays that have been
            added using null
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary.getSumSq` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalMultivariateSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getSumSq` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the array of component sums of squares
        
        
        """
        ...
    def getSumsqImpl(self) -> typing.MutableSequence[StorelessUnivariateStatistic]:
        """
            Returns the currently configured sum of squares implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.getSumsqImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the sum of squares
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Returns hash code based on values of statistics
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.hashCode` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                hash code
        
        
        """
        ...
    def setGeoMeanImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List[StorelessUnivariateStatistic], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the geometric mean.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Parameters:
                geoMeanImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the geometric mean
        
        
        """
        ...
    def setMaxImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List[StorelessUnivariateStatistic], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the maximum.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Parameters:
                maxImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the maximum
        
        
        """
        ...
    def setMeanImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List[StorelessUnivariateStatistic], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the mean.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Parameters:
                meanImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the mean
        
        
        """
        ...
    def setMinImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List[StorelessUnivariateStatistic], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the minimum.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Parameters:
                minImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the minimum
        
        
        """
        ...
    def setSumImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List[StorelessUnivariateStatistic], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the Sum.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Parameters:
                sumImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the Sum
        
        
        """
        ...
    def setSumLogImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List[StorelessUnivariateStatistic], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the sum of logs.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Parameters:
                sumLogImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the log sum
        
        
        """
        ...
    def setSumsqImpl(self, storelessUnivariateStatisticArray: typing.Union[typing.List[StorelessUnivariateStatistic], jpype.JArray]) -> None:
        """
        
            Sets the implementation for the sum of squares.
        
            This method must be activated before any data has been added - i.e., before null has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Parameters:
                sumsqImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`[]): the StorelessUnivariateStatistic instance to use for computing the sum of squares
        
        
        """
        ...
    def toString(self) -> str:
        """
            Generates a text report displaying summary statistics from values that have been added.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics.toString` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.MultivariateSummaryStatistics`
        
            Returns:
                String with line feeds displaying statistics
        
        
        """
        ...

class SynchronizedSummaryStatistics(SummaryStatistics):
    """
    public class SynchronizedSummaryStatistics extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
    
        Implementation of :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics` that is safe to use in a
        multithreaded environment. Multiple threads can safely operate on a single instance without causing runtime exceptions
        due to race conditions. In effect, this implementation makes modification and access methods atomic operations for a
        single instance. That is to say, as one thread is computing a statistic from the instance, no other thread can modify
        the instance nor compute another statistic.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, synchronizedSummaryStatistics: 'SynchronizedSummaryStatistics'): ...
    def addValue(self, double: float) -> None:
        """
            Add a value to the data
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Parameters:
                value (double): the value to add
        
        
        """
        ...
    def clear(self) -> None:
        """
            Resets all statistics and storage
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.clear` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(summaryStatistics: SummaryStatistics, summaryStatistics2: SummaryStatistics) -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Acquires synchronization lock on source, then dest before copying.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SynchronizedSummaryStatistics`): SynchronizedSummaryStatistics to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SynchronizedSummaryStatistics`): SynchronizedSummaryStatistics to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(synchronizedSummaryStatistics: 'SynchronizedSummaryStatistics', synchronizedSummaryStatistics2: 'SynchronizedSummaryStatistics') -> None: ...
    @typing.overload
    def copy(self) -> 'SynchronizedSummaryStatistics':
        """
            Returns a copy of this SynchronizedSummaryStatistics instance with the same internal state.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.copy` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                a copy of this
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
            Returns true iff :code:`object` is a :code:`SummaryStatistics` instance and all statistics have the same values as this.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.equals` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the object to test equality against.
        
            Returns:
                true if object equals this
        
        
        """
        ...
    def getGeoMeanImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured geometric mean implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getGeoMeanImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the geometric mean
        
        
        """
        ...
    def getGeometricMean(self) -> float:
        """
            Returns the geometric mean of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getGeometricMean` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the geometric mean
        
        
        """
        ...
    def getMax(self) -> float:
        """
            Returns the maximum of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMax` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getMax` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the maximum
        
        
        """
        ...
    def getMaxImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured maximum implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getMaxImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the maximum
        
        
        """
        ...
    def getMean(self) -> float:
        """
            Returns the mean of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMean` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getMean` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the mean
        
        
        """
        ...
    def getMeanImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured mean implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getMeanImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the mean
        
        
        """
        ...
    def getMin(self) -> float:
        """
            Returns the minimum of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getMin` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getMin` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the minimum
        
        
        """
        ...
    def getMinImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured minimum implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getMinImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the minimum
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of available values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getN` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                The number of available values
        
        
        """
        ...
    def getPopulationVariance(self) -> float:
        """
            Returns the ` population variance <http://en.wikibooks.org/wiki/Statistics/Summary/Variance>` of the values that have
            been added.
        
            Double.NaN is returned if no values have been added.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getPopulationVariance` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the population variance
        
        
        """
        ...
    def getStandardDeviation(self) -> float:
        """
            Returns the standard deviation of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getStandardDeviation` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getStandardDeviation` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the standard deviation
        
        
        """
        ...
    def getSum(self) -> float:
        """
            Returns the sum of the values that have been added
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getSum` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getSum` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                The sum or :code:`Double.NaN` if no values have been added
        
        
        """
        ...
    def getSumImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured Sum implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getSumImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the sum
        
        
        """
        ...
    def getSumLogImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured sum of logs implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getSumLogImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the log sum
        
        
        """
        ...
    def getSummary(self) -> StatisticalSummary:
        """
            Return a :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummaryValues` instance reporting current
            statistics.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getSummary` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                Current values of statistics
        
        
        """
        ...
    def getSumsq(self) -> float:
        """
            Returns the sum of the squares of the values that have been added.
        
            Double.NaN is returned if no values have been added.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getSumsq` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                The sum of squares
        
        
        """
        ...
    def getSumsqImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured sum of squares implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getSumsqImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the sum of squares
        
        
        """
        ...
    def getVariance(self) -> float:
        """
            Returns the (sample) variance of the available values.
        
            This method returns the bias-corrected sample variance (using :code:`n - 1` in the denominator). Use
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getPopulationVariance` for the non-bias-corrected
            population variance.
        
            Double.NaN is returned if no values have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary.getVariance` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getVariance` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the variance
        
        
        """
        ...
    def getVarianceImpl(self) -> StorelessUnivariateStatistic:
        """
            Returns the currently configured variance implementation
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.getVarianceImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                the StorelessUnivariateStatistic implementing the variance
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Returns hash code based on values of statistics
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.hashCode` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                hash code
        
        
        """
        ...
    def setGeoMeanImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the geometric mean.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.setGeoMeanImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Parameters:
                geoMeanImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the geometric mean
        
        
        """
        ...
    def setMaxImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the maximum.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.setMaxImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Parameters:
                maxImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the maximum
        
        
        """
        ...
    def setMeanImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the mean.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.setMeanImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Parameters:
                meanImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the mean
        
        
        """
        ...
    def setMinImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the minimum.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.setMinImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Parameters:
                minImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the minimum
        
        
        """
        ...
    def setSumImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the Sum.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.setSumImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Parameters:
                sumImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the Sum
        
        
        """
        ...
    def setSumLogImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the sum of logs.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.setSumLogImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Parameters:
                sumLogImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the log sum
        
        
        """
        ...
    def setSumsqImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the sum of squares.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.setSumsqImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Parameters:
                sumsqImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the sum of squares
        
        
        """
        ...
    def setVarianceImpl(self, storelessUnivariateStatistic: StorelessUnivariateStatistic) -> None:
        """
        
            Sets the implementation for the variance.
        
            This method must be activated before any data has been added - i.e., before
            :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.addValue` has been used to add data; otherwise an
            IllegalStateException will be thrown.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.setVarianceImpl` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Parameters:
                varianceImpl (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`): the StorelessUnivariateStatistic instance to use for computing the variance
        
        
        """
        ...
    def toString(self) -> str:
        """
            Generates a text report displaying summary statistics from values that have been added.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics.toString` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics`
        
            Returns:
                String with line feeds displaying statistics
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.stat.descriptive")``.

    AbstractStorelessUnivariateStatistic: typing.Type[AbstractStorelessUnivariateStatistic]
    AbstractUnivariateStatistic: typing.Type[AbstractUnivariateStatistic]
    AggregateSummaryStatistics: typing.Type[AggregateSummaryStatistics]
    DescriptiveStatistics: typing.Type[DescriptiveStatistics]
    MultivariateSummaryStatistics: typing.Type[MultivariateSummaryStatistics]
    StatisticalMultivariateSummary: typing.Type[StatisticalMultivariateSummary]
    StatisticalSummary: typing.Type[StatisticalSummary]
    StatisticalSummaryValues: typing.Type[StatisticalSummaryValues]
    StorelessUnivariateStatistic: typing.Type[StorelessUnivariateStatistic]
    SummaryStatistics: typing.Type[SummaryStatistics]
    SynchronizedDescriptiveStatistics: typing.Type[SynchronizedDescriptiveStatistics]
    SynchronizedMultivariateSummaryStatistics: typing.Type[SynchronizedMultivariateSummaryStatistics]
    SynchronizedSummaryStatistics: typing.Type[SynchronizedSummaryStatistics]
    UnivariateStatistic: typing.Type[UnivariateStatistic]
    WeightedEvaluation: typing.Type[WeightedEvaluation]
    moment: fr.cnes.sirius.patrius.math.stat.descriptive.moment.__module_protocol__
    rank: fr.cnes.sirius.patrius.math.stat.descriptive.rank.__module_protocol__
    summary: fr.cnes.sirius.patrius.math.stat.descriptive.summary.__module_protocol__
