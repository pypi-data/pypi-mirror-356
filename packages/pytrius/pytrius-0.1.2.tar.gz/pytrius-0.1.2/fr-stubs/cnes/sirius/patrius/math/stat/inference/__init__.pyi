
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.stat.descriptive
import fr.cnes.sirius.patrius.math.stat.ranking
import java.util
import jpype
import typing



class ChiSquareTest:
    def __init__(self): ...
    @typing.overload
    def chiSquare(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray]) -> float: ...
    @typing.overload
    def chiSquare(self, longArray: typing.Union[typing.List[typing.MutableSequence[int]], jpype.JArray]) -> float: ...
    def chiSquareDataSetsComparison(self, longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray]) -> float: ...
    @typing.overload
    def chiSquareTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray], double2: float) -> bool: ...
    @typing.overload
    def chiSquareTest(self, longArray: typing.Union[typing.List[typing.MutableSequence[int]], jpype.JArray], double: float) -> bool: ...
    @typing.overload
    def chiSquareTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray]) -> float: ...
    @typing.overload
    def chiSquareTest(self, longArray: typing.Union[typing.List[typing.MutableSequence[int]], jpype.JArray]) -> float: ...
    @typing.overload
    def chiSquareTestDataSetsComparison(self, longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray], double: float) -> bool: ...
    @typing.overload
    def chiSquareTestDataSetsComparison(self, longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray]) -> float: ...

class GTest:
    def __init__(self): ...
    def g(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray]) -> float: ...
    def gDataSetsComparison(self, longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray]) -> float: ...
    @typing.overload
    def gTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray], double2: float) -> bool: ...
    @typing.overload
    def gTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray]) -> float: ...
    @typing.overload
    def gTestDataSetsComparison(self, longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray], double: float) -> bool: ...
    @typing.overload
    def gTestDataSetsComparison(self, longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray]) -> float: ...
    def gTestIntrinsic(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray]) -> float: ...
    def rootLogLikelihoodRatio(self, long: int, long2: int, long3: int, long4: int) -> float: ...

class MannWhitneyUTest:
    """
    public class MannWhitneyUTest extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        An implementation of the Mann-Whitney U test (also called Wilcoxon rank-sum test).
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, naNStrategy: fr.cnes.sirius.patrius.math.stat.ranking.NaNStrategy, tiesStrategy: fr.cnes.sirius.patrius.math.stat.ranking.TiesStrategy): ...
    def mannWhitneyU(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Computes the ` Mann-Whitney U statistic <http://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U>` comparing mean for two
            independent samples possibly of different length.
        
            This statistic can be used to perform a Mann-Whitney U test evaluating the null hypothesis that the two independent
            samples has equal mean.
        
            Let X :sub:`i` denote the i'th individual of the first sample and Y :sub:`j` the j'th individual in the second sample.
            Note that the samples would often have different length.
        
            **Preconditions**:
        
              - All observations in the two samples are independent.
              - The observations are at least ordinal (continuous are also ordinal).
        
        
            Parameters:
                x (double[]): the first sample
                y (double[]): the second sample
        
            Returns:
                Mann-Whitney U statistic (maximum of U :sup:`x` and U :sup:`y` )
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`x` or :code:`y` are :code:`null`.
                :class:`~fr.cnes.sirius.patrius.math.exception.NoDataException`: if :code:`x` or :code:`y` are zero-length.
        
        
        """
        ...
    def mannWhitneyUTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Returns the asymptotic *observed significance level*, or ` p-value
            <http://www.cas.lancs.ac.uk/glossary_v1.1/hyptest.html#pvalue>`, associated with a ` Mann-Whitney U statistic
            <http://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U>` comparing mean for two independent samples.
        
            Let X :sub:`i` denote the i'th individual of the first sample and Y :sub:`j` the j'th individual in the second sample.
            Note that the samples would often have different length.
        
            **Preconditions**:
        
              - All observations in the two samples are independent.
              - The observations are at least ordinal (continuous are also ordinal).
        
        
            Ties give rise to biased variance at the moment. See e.g. `http://mlsc.lboro.ac.uk/resources/statistics/Mannwhitney.pdf
            <http://mlsc.lboro.ac.uk/resources/statistics/Mannwhitney.pdf>`.
        
            Parameters:
                x (double[]): the first sample
                y (double[]): the second sample
        
            Returns:
                asymptotic p-value
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`x` or :code:`y` are :code:`null`.
                :class:`~fr.cnes.sirius.patrius.math.exception.NoDataException`: if :code:`x` or :code:`y` are zero-length.
                :class:`~fr.cnes.sirius.patrius.math.exception.ConvergenceException`: if the p-value can not be computed due to a convergence error
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the maximum number of iterations is exceeded
        
        
        """
        ...

class OneWayAnova:
    """
    public class OneWayAnova extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Implements one-way ANOVA (analysis of variance) statistics.
    
        Tests for differences between two or more categories of univariate data (for example, the body mass index of
        accountants, lawyers, doctors and computer programmers). When two categories are given, this is equivalent to the
        :class:`~fr.cnes.sirius.patrius.math.stat.inference.TTest`.
    
        Uses the :class:`~fr.cnes.sirius.patrius.math.distribution.FDistribution` to estimate exact p-values.
    
        This implementation is based on a description at http://faculty.vassar.edu/lowry/ch13pt1.html
    
        .. code-block: java
        
        
         Abbreviations: bg = between groups,
                        wg = within groups,
                        ss = sum squared deviations
         
    
        Since:
            1.2
    """
    def __init__(self): ...
    def anovaFValue(self, collection: typing.Union[java.util.Collection[typing.Union[typing.List[float], jpype.JArray]], typing.Sequence[typing.Union[typing.List[float], jpype.JArray]], typing.Set[typing.Union[typing.List[float], jpype.JArray]]]) -> float: ...
    def anovaPValue(self, collection: typing.Union[java.util.Collection[typing.Union[typing.List[float], jpype.JArray]], typing.Sequence[typing.Union[typing.List[float], jpype.JArray]], typing.Set[typing.Union[typing.List[float], jpype.JArray]]]) -> float: ...
    def anovaTest(self, collection: typing.Union[java.util.Collection[typing.Union[typing.List[float], jpype.JArray]], typing.Sequence[typing.Union[typing.List[float], jpype.JArray]], typing.Set[typing.Union[typing.List[float], jpype.JArray]]], double: float) -> bool: ...

class TTest:
    def __init__(self): ...
    @typing.overload
    def homoscedasticT(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def homoscedasticT(self, statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, statisticalSummary2: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...
    @typing.overload
    def homoscedasticTTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float) -> bool: ...
    @typing.overload
    def homoscedasticTTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def homoscedasticTTest(self, statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, statisticalSummary2: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...
    def pairedT(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def pairedTTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float) -> bool: ...
    @typing.overload
    def pairedTTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def t(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def t(self, double: float, statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...
    @typing.overload
    def t(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def t(self, statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, statisticalSummary2: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...
    @typing.overload
    def tTest(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float) -> bool: ...
    @typing.overload
    def tTest(self, double: float, statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, double2: float) -> bool: ...
    @typing.overload
    def tTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float) -> bool: ...
    @typing.overload
    def tTest(self, statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, statisticalSummary2: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, double: float) -> bool: ...
    @typing.overload
    def tTest(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def tTest(self, double: float, statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...
    @typing.overload
    def tTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def tTest(self, statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, statisticalSummary2: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...

class TestUtils:
    """
    public final class TestUtils extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        A collection of static methods to create inference test instances or to perform inference tests.
    
        Since:
            1.1
    """
    @typing.overload
    @staticmethod
    def chiSquare(doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray]) -> float:
        """
        
            Parameters:
                observed (double[]): array of observed frequency counts
                expected (long[]): array of expected frequency counts
        
            Returns:
                chiSquare test statistic
        
            Also see:
        
        """
        ...
    @typing.overload
    @staticmethod
    def chiSquare(longArray: typing.Union[typing.List[typing.MutableSequence[int]], jpype.JArray]) -> float:
        """
        
            Parameters:
                counts (long[][]): array representation of 2-way table
        
            Returns:
                chiSquare test statistic
        
            Also see:
        
        
        """
        ...
    @staticmethod
    def chiSquareDataSetsComparison(longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray]) -> float:
        """
        
            Parameters:
                observed1 (long[]): array of observed frequency counts of the first data set
                observed2 (long[]): array of observed frequency counts of the second data set
        
            Returns:
                chiSquare test statistic
        
            Since:
                1.2
        
            Also see:
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def chiSquareTest(doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray], double2: float) -> bool:
        """
        
            Parameters:
                observed (double[]): array of observed frequency counts
                expected (long[]): array of expected frequency counts
                alpha (double): significance level of the test
        
            Returns:
                true iff null hypothesis can be rejected with confidence 1 - alpha
        
            Also see:
        
        """
        ...
    @typing.overload
    @staticmethod
    def chiSquareTest(longArray: typing.Union[typing.List[typing.MutableSequence[int]], jpype.JArray], double: float) -> bool:
        """
        
            Parameters:
                observed (double[]): array of observed frequency counts
                expected (long[]): array of expected frequency counts
        
            Returns:
                p-value
        
            Also see:
        
        
            Parameters:
                counts (long[][]): array representation of 2-way table
                alpha (double): significance level of the test
        
            Returns:
                true iff null hypothesis can be rejected with confidence 1 - alpha
        
            Also see:
        
        """
        ...
    @typing.overload
    @staticmethod
    def chiSquareTest(doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def chiSquareTest(longArray: typing.Union[typing.List[typing.MutableSequence[int]], jpype.JArray]) -> float:
        """
        
            Parameters:
                counts (long[][]): array representation of 2-way table
        
            Returns:
                p-value
        
            Also see:
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def chiSquareTestDataSetsComparison(longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray], double: float) -> bool:
        """
        
            Parameters:
                observed1 (long[]): array of observed frequency counts of the first data set
                observed2 (long[]): array of observed frequency counts of the second data set
                alpha (double): significance level of the test
        
            Returns:
                true iff null hypothesis can be rejected with confidence 1 - alpha
        
            Since:
                1.2
        
            Also see:
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def chiSquareTestDataSetsComparison(longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray]) -> float:
        """
        
            Parameters:
                observed1 (long[]): array of observed frequency counts of the first data set
                observed2 (long[]): array of observed frequency counts of the second data set
        
            Returns:
                p-value
        
            Since:
                1.2
        
            Also see:
        
        """
        ...
    @staticmethod
    def g(doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray]) -> float:
        """
        
            Parameters:
                observed (double[]): array of observed frequency counts
                expected (long[]): array of expected frequency counts
        
            Returns:
                G-Test statistic
        
            Since:
                3.1
        
            Also see:
        
        
        """
        ...
    @staticmethod
    def gDataSetsComparison(longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray]) -> float:
        """
        
            Parameters:
                observed1 (long[]): array of observed frequency counts of the first data set
                observed2 (long[]): array of observed frequency counts of the second data set
        
            Returns:
                G-Test statistic
        
            Since:
                3.1
        
            Also see:
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def gTest(doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray], double2: float) -> bool:
        """
        
            Parameters:
                observed (double[]): array of observed frequency counts
                expected (long[]): array of expected frequency counts
                alpha (double): significance level of the test
        
            Returns:
                true iff null hypothesis can be rejected with confidence 1 - alpha
        
            Since:
                3.1
        
            Also see:
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def gTest(doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray]) -> float:
        """
        
            Parameters:
                observed (double[]): array of observed frequency counts
                expected (long[]): array of expected frequency counts
        
            Returns:
                p-value
        
            Since:
                3.1
        
            Also see:
        
        """
        ...
    @typing.overload
    @staticmethod
    def gTestDataSetsComparison(longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray], double: float) -> bool:
        """
        
            Parameters:
                observed1 (long[]): array of observed frequency counts of the first data set
                observed2 (long[]): array of observed frequency counts of the second data set
                alpha (double): significance level of the test
        
            Returns:
                true iff null hypothesis can be rejected with confidence 1 - alpha
        
            Since:
                3.1
        
            Also see:
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def gTestDataSetsComparison(longArray: typing.Union[typing.List[int], jpype.JArray], longArray2: typing.Union[typing.List[int], jpype.JArray]) -> float:
        """
        
            Parameters:
                observed1 (long[]): array of observed frequency counts of the first data set
                observed2 (long[]): array of observed frequency counts of the second data set
        
            Returns:
                p-value
        
            Since:
                3.1
        
            Also see:
        
        """
        ...
    @staticmethod
    def gTestIntrinsic(doubleArray: typing.Union[typing.List[float], jpype.JArray], longArray: typing.Union[typing.List[int], jpype.JArray]) -> float:
        """
        
            Parameters:
                observed (double[]): array of observed frequency counts
                expected (long[]): array of expected frequency counts
        
            Returns:
                p-value
        
            Since:
                3.1
        
            Also see:
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def homoscedasticT(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
        
            Parameters:
                sample1 (double[]): array of sample data values
                sample2 (double[]): array of sample data values
        
            Returns:
                t statistic
        
            Also see:
        
            See TTest# homoscedasticT(fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary,
            fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary)
        
            Parameters:
                sampleStats1 (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing data from the first sample
                sampleStats2 (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing data from the second sample
        
            Returns:
                t statistic
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def homoscedasticT(statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, statisticalSummary2: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...
    @typing.overload
    @staticmethod
    def homoscedasticTTest(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float) -> bool:
        """
        
            Parameters:
                sample1 (double[]): array of sample data values
                sample2 (double[]): array of sample data values
                alpha (double): significance level of the test
        
            Returns:
                true if the null hypothesis can be rejected with confidence 1 - alpha
        
            Also see:
        
        """
        ...
    @typing.overload
    @staticmethod
    def homoscedasticTTest(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
        
            Parameters:
                sample1 (double[]): array of sample data values
                sample2 (double[]): array of sample data values
        
            Returns:
                t statistic
        
            Also see:
        
            See TTest# homoscedasticTTest(fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary,
            fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary)
        
            Parameters:
                sampleStats1 (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing data from the first sample
                sampleStats2 (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing data from the second sample
        
            Returns:
                t statistic
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def homoscedasticTTest(statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, statisticalSummary2: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...
    @staticmethod
    def oneWayAnovaFValue(collection: typing.Union[java.util.Collection[typing.Union[typing.List[float], jpype.JArray]], typing.Sequence[typing.Union[typing.List[float], jpype.JArray]], typing.Set[typing.Union[typing.List[float], jpype.JArray]]]) -> float: ...
    @staticmethod
    def oneWayAnovaPValue(collection: typing.Union[java.util.Collection[typing.Union[typing.List[float], jpype.JArray]], typing.Sequence[typing.Union[typing.List[float], jpype.JArray]], typing.Set[typing.Union[typing.List[float], jpype.JArray]]]) -> float: ...
    @staticmethod
    def oneWayAnovaTest(collection: typing.Union[java.util.Collection[typing.Union[typing.List[float], jpype.JArray]], typing.Sequence[typing.Union[typing.List[float], jpype.JArray]], typing.Set[typing.Union[typing.List[float], jpype.JArray]]], double: float) -> bool: ...
    @staticmethod
    def pairedT(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
        
            Parameters:
                sample1 (double[]): array of sample data values
                sample2 (double[]): array of sample data values
        
            Returns:
                t statistic
        
            Also see:
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def pairedTTest(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float) -> bool:
        """
        
            Parameters:
                sample1 (double[]): array of sample data values
                sample2 (double[]): array of sample data values
                alpha (double): significance level of the test
        
            Returns:
                true if the null hypothesis can be rejected with confidence 1 - alpha
        
            Also see:
        
        """
        ...
    @typing.overload
    @staticmethod
    def pairedTTest(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
        
            Parameters:
                sample1 (double[]): array of sample data values
                sample2 (double[]): array of sample data values
        
            Returns:
                t statistic
        
            Also see:
        
        
        """
        ...
    @staticmethod
    def rootLogLikelihoodRatio(long: int, long2: int, long3: int, long4: int) -> float:
        """
        
            Parameters:
                k11 (long): number of times the two events occurred together (AB)
                k12 (long): number of times the second event occurred WITHOUT the first event (notA,B)
                k21 (long): number of times the first event occurred WITHOUT the second event (A, notB)
                k22 (long): number of times something else occurred (i.e. was neither of these events (notA, notB)
        
            Returns:
                root log-likelihood ratio
        
            Since:
                3.1
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.inference.GTest.rootLogLikelihoodRatio`
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def t(double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
        
            Parameters:
                mu (double): comparison constant
                observed (double[]): array of values
        
            Returns:
                t statistic
        
            Also see:
        
        
            Parameters:
                mu (double): comparison constant
                sampleStats (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): DescriptiveStatistics holding sample summary statitstics
        
            Returns:
                t statistic
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.inference.TTest.t`
        
        
            Parameters:
                sample1 (double[]): array of sample data values
                sample2 (double[]): array of sample data values
        
            Returns:
                t statistic
        
            Also see:
        
            See TTest# t(fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary,
            fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary)
        
            Parameters:
                sampleStats1 (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing data from the first sample
                sampleStats2 (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing data from the second sample
        
            Returns:
                t statistic
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def t(double: float, statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...
    @typing.overload
    @staticmethod
    def t(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def t(statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, statisticalSummary2: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...
    @typing.overload
    @staticmethod
    def tTest(double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float) -> bool:
        """
        
            Parameters:
                mu (double): constant value to compare sample mean against
                sample (double[]): array of sample data values
                alpha (double): significance level of the test
        
            Returns:
                p-value
        
            Also see:
        
        
            Parameters:
                mu (double): constant value to compare sample mean against
                sampleStats (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing sample data values
                alpha (double): significance level of the test
        
            Returns:
                p-value
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.inference.TTest.tTest`
        
        
            Parameters:
                sample1 (double[]): array of sample data values
                sample2 (double[]): array of sample data values
                alpha (double): significance level of the test
        
            Returns:
                true if the null hypothesis can be rejected with confidence 1 - alpha
        
            Also see:
        
            See fr.cnes.sirius.patrius.math.stat.inference.TTest#
            tTest(fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary,
            fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, double)
        
            Parameters:
                sampleStats1 (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing data from the first sample
                sampleStats2 (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing data from the second sample
                alpha (double): significance level of the test
        
            Returns:
                true if the null hypothesis can be rejected with confidence 1 - alpha
        
        """
        ...
    @typing.overload
    @staticmethod
    def tTest(double: float, statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, double2: float) -> bool: ...
    @typing.overload
    @staticmethod
    def tTest(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float) -> bool: ...
    @typing.overload
    @staticmethod
    def tTest(statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, statisticalSummary2: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, double: float) -> bool: ...
    @typing.overload
    @staticmethod
    def tTest(double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
        
            Parameters:
                mu (double): constant value to compare sample mean against
                sample (double[]): array of sample data values
        
            Returns:
                p-value
        
            Also see:
        
        
            Parameters:
                mu (double): constant value to compare sample mean against
                sampleStats (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing sample data
        
            Returns:
                p-value
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.stat.inference.TTest.tTest`
        
        
            Parameters:
                sample1 (double[]): array of sample data values
                sample2 (double[]): array of sample data values
        
            Returns:
                t statistic
        
            Also see:
        
            See fr.cnes.sirius.patrius.math.stat.inference.TTest#
            tTest(fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary,
            fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary)
        
            Parameters:
                sampleStats1 (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing data from the first sample
                sampleStats2 (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary`): StatisticalSummary describing data from the second sample
        
            Returns:
                t statistic
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def tTest(double: float, statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...
    @typing.overload
    @staticmethod
    def tTest(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def tTest(statisticalSummary: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary, statisticalSummary2: fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary) -> float: ...

class WilcoxonSignedRankTest:
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, naNStrategy: fr.cnes.sirius.patrius.math.stat.ranking.NaNStrategy, tiesStrategy: fr.cnes.sirius.patrius.math.stat.ranking.TiesStrategy): ...
    def wilcoxonSignedRank(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    def wilcoxonSignedRankTest(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.stat.inference")``.

    ChiSquareTest: typing.Type[ChiSquareTest]
    GTest: typing.Type[GTest]
    MannWhitneyUTest: typing.Type[MannWhitneyUTest]
    OneWayAnova: typing.Type[OneWayAnova]
    TTest: typing.Type[TTest]
    TestUtils: typing.Type[TestUtils]
    WilcoxonSignedRankTest: typing.Type[WilcoxonSignedRankTest]
