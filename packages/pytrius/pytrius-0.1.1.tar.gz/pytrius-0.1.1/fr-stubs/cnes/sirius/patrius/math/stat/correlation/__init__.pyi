
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.stat.ranking
import jpype
import typing



class Covariance:
    """
    public class Covariance extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Computes covariances for pairs of arrays or columns of a matrix.
    
        The constructors that take :code:`RealMatrix` or :code:`double[][]` arguments generate covariance matrices. The columns
        of the input matrices are assumed to represent variable values.
    
        The constructor argument :code:`biasCorrected` determines whether or not computed covariances are bias-corrected.
    
        Unbiased covariances are given by the formula
        :code:`cov(X, Y) = Σ[(x :sub:`i` - E(X))(y :sub:`i` - E(Y))] / (n - 1)` where :code:`E(X)` is the mean of :code:`X` and
        :code:`E(Y)` is the mean of the :code:`Y` values.
    
        Non-bias-corrected estimates use :code:`n` in place of :code:`n - 1`
    
        Since:
            2.0
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], boolean: bool): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, boolean: bool): ...
    @typing.overload
    def covariance(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Computes the covariance between the two arrays, using the bias-corrected formula.
        
            Array lengths must match and the common length must be at least 2.
        
            Parameters:
                xArray (double[]): first data array
                yArray (double[]): second data array
        
            Returns:
                returns the covariance for the two arrays
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the arrays lengths do not match or there is insufficient data
        
        
        """
        ...
    @typing.overload
    def covariance(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool) -> float:
        """
            Computes the covariance between the two arrays.
        
            Array lengths must match and the common length must be at least 2.
        
            Parameters:
                xArray (double[]): first data array
                yArray (double[]): second data array
                biasCorrected (boolean): if true, returned value will be bias-corrected
        
            Returns:
                returns the covariance for the two arrays
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the arrays lengths do not match or there is insufficient data
        
        """
        ...
    def getCovarianceMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the covariance matrix
        
            Returns:
                covariance matrix
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of observations (length of covariate vectors)
        
            Returns:
                number of observations
        
        
        """
        ...

class PearsonsCorrelation:
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, int: int): ...
    @typing.overload
    def __init__(self, covariance: Covariance): ...
    @typing.overload
    def computeCorrelationMatrix(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    @typing.overload
    def computeCorrelationMatrix(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def correlation(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    def covarianceToCorrelation(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def getCorrelationMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def getCorrelationPValues(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def getCorrelationStandardErrors(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...

class SpearmansCorrelation:
    """
    public class SpearmansCorrelation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
    
        Spearman's rank correlation. This implementation performs a rank transformation on the input data and then computes
        :class:`~fr.cnes.sirius.patrius.math.stat.correlation.PearsonsCorrelation` on the ranked data.
    
        By default, ranks are computed using :class:`~fr.cnes.sirius.patrius.math.stat.ranking.NaturalRanking` with default
        strategies for handling NaNs and ties in the data (NaNs maximal, ties averaged). The ranking algorithm can be set using
        a constructor argument.
    
        Since:
            2.0
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, rankingAlgorithm: typing.Union[fr.cnes.sirius.patrius.math.stat.ranking.RankingAlgorithm, typing.Callable]): ...
    @typing.overload
    def __init__(self, rankingAlgorithm: typing.Union[fr.cnes.sirius.patrius.math.stat.ranking.RankingAlgorithm, typing.Callable]): ...
    @typing.overload
    def computeCorrelationMatrix(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Computes the Spearman's rank correlation matrix for the columns of the input matrix.
        
            Parameters:
                matrix (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix with columns representing variables to correlate
        
            Returns:
                correlation matrix
        
            Computes the Spearman's rank correlation matrix for the columns of the input rectangular array. The columns of the array
            represent values of variables to be correlated.
        
            Parameters:
                matrix (double[][]): matrix with columns representing variables to correlate
        
            Returns:
                correlation matrix
        
        
        """
        ...
    @typing.overload
    def computeCorrelationMatrix(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def correlation(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Computes the Spearman's rank correlation coefficient between the two arrays.
        
            Parameters:
                xArray (double[]): first data array
                yArray (double[]): second data array
        
            Returns:
                Returns Spearman's rank correlation coefficient for the two arrays
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the arrays lengths do not match
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array length is less than 2
        
        
        """
        ...
    def getCorrelationMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Calculate the Spearman Rank Correlation Matrix.
        
            Returns:
                Spearman Rank Correlation Matrix
        
        
        """
        ...
    def getRankCorrelation(self) -> PearsonsCorrelation:
        """
            Returns a :class:`~fr.cnes.sirius.patrius.math.stat.correlation.PearsonsCorrelation` instance constructed from the
            ranked input data. That is, :code:`new SpearmansCorrelation(matrix).getRankCorrelation()` is equivalent to :code:`new
            PearsonsCorrelation(rankTransform(matrix))` where :code:`rankTransform(matrix)` is the result of applying the configured
            :code:`RankingAlgorithm` to each of the columns of :code:`matrix.`
        
            Returns:
                PearsonsCorrelation among ranked column data
        
        
        """
        ...

class StorelessCovariance(Covariance):
    """
    public class StorelessCovariance extends :class:`~fr.cnes.sirius.patrius.math.stat.correlation.Covariance`
    
        Covariance implementation that does not require input data to be stored in memory. The size of the covariance matrix is
        specified in the constructor. Specific elements of the matrix are incrementally updated with calls to incrementRow() or
        increment Covariance().
    
        This class is based on a paper written by Philippe Pébay: ` Formulas for Robust, One-Pass Parallel Computation of
        Covariances and Arbitrary-Order Statistical Moments
        <http://prod.sandia.gov/techlib/access-control.cgi/2008/086212.pdf>`, 2008, Technical Report SAND2008-6212, Sandia
        National Laboratories.
    
        Note: the underlying covariance matrix is symmetric, thus only the upper triangular part of the matrix is stored and
        updated each increment.
    
        Since:
            3.0
    """
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, boolean: bool): ...
    def getCovariance(self, int: int, int2: int) -> float:
        """
            Get the covariance for an individual element of the covariance matrix.
        
            Parameters:
                xIndex (int): row index in the covariance matrix
                yIndex (int): column index in the covariance matrix
        
            Returns:
                the covariance of the given element
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the number of observations in the cell is < 2
        
        
        """
        ...
    def getCovarianceMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the covariance matrix
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.correlation.Covariance.getCovarianceMatrix` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.correlation.Covariance`
        
            Returns:
                covariance matrix
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the number of observations in a cell is < 2
        
        
        """
        ...
    def getData(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Return the covariance matrix as two-dimensional array.
        
            Returns:
                a two-dimensional double array of covariance values
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the number of observations for a cell is < 2
        
        
        """
        ...
    def getN(self) -> int:
        """
            This :class:`~fr.cnes.sirius.patrius.math.stat.correlation.Covariance` method is not supported by a
            :class:`~fr.cnes.sirius.patrius.math.stat.correlation.StorelessCovariance`, since the number of bivariate observations
            does not have to be the same for different pairs of covariates - i.e., N as defined in
            :meth:`~fr.cnes.sirius.patrius.math.stat.correlation.Covariance.getN` is undefined.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.stat.correlation.Covariance.getN` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.correlation.Covariance`
        
            Returns:
                nothing as this implementation always throws a
                :class:`~fr.cnes.sirius.patrius.math.exception.MathUnsupportedOperationException`
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathUnsupportedOperationException`: in all cases
        
        
        """
        ...
    def increment(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Increment the covariance matrix with one row of data.
        
            Parameters:
                data (double[]): array representing one row of data.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the length of :code:`rowData` does not match with the covariance matrix
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.stat.correlation")``.

    Covariance: typing.Type[Covariance]
    PearsonsCorrelation: typing.Type[PearsonsCorrelation]
    SpearmansCorrelation: typing.Type[SpearmansCorrelation]
    StorelessCovariance: typing.Type[StorelessCovariance]
