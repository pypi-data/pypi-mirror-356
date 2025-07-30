
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.exception
import fr.cnes.sirius.patrius.math.exception.util
import fr.cnes.sirius.patrius.math.linear
import java.io
import jpype
import typing



class ModelSpecificationException(fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException):
    """
    public class ModelSpecificationException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`
    
        Exception thrown when a regression model is not correctly specified.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...

class MultipleLinearRegression:
    """
    public interface MultipleLinearRegression
    
        The multiple linear regression can be represented in matrix-notation.
    
        .. code-block: java
        
        
         y = X * b + u
         
        where y is an :code:`n-vector` **regressand**, X is a :code:`[n,k]` matrix whose :code:`k` columns are called
        **regressors**, b is :code:`k-vector` of **regression parameters** and :code:`u` is an :code:`n-vector` of **error
        terms** or **residuals**. The notation is quite standard in literature, cf eg `Davidson and MacKinnon, Econometrics
        Theory and Methods, 2004 <http://www.econ.queensu.ca/ETM>`.
    
        Since:
            2.0
    """
    def estimateRegressandVariance(self) -> float:
        """
            Returns the variance of the regressand, ie Var(y).
        
            Returns:
                The double representing the variance of y
        
        
        """
        ...
    def estimateRegressionParameters(self) -> typing.MutableSequence[float]:
        """
            Estimates the regression parameters b.
        
            Returns:
                The [k,1] array representing b
        
        
        """
        ...
    def estimateRegressionParametersStandardErrors(self) -> typing.MutableSequence[float]:
        """
            Returns the standard errors of the regression parameters.
        
            Returns:
                standard errors of estimated regression parameters
        
        
        """
        ...
    def estimateRegressionParametersVariance(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Estimates the variance of the regression parameters, ie Var(b).
        
            Returns:
                The [k,k] array representing the variance of b
        
        
        """
        ...
    def estimateResiduals(self) -> typing.MutableSequence[float]:
        """
            Estimates the residuals, ie u = y - X*b.
        
            Returns:
                The [n,1] array representing the residuals
        
        
        """
        ...

class RegressionResults(java.io.Serializable):
    """
    public class RegressionResults extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Results of a Multiple Linear Regression model fit.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], boolean: bool, long: int, int: int, double3: float, double4: float, double5: float, boolean2: bool, boolean3: bool): ...
    def getAdjustedRSquared(self) -> float:
        """
        
            Returns the adjusted R-squared statistic, defined by the formula
        
            .. code-block: java
            
            
             R :sup:`2`  :sub:`adj`  = 1 - [SSR (n - 1)] / [SSTO (n - p)]
             
            where SSR is the sum of squared residuals}, SSTO is the total sum of squares}, n is the number of observations and p is
            the number of parameters estimated (including the intercept).
        
            If the regression is estimated without an intercept term, what is returned is
        
            .. code-block: java
            
            
             :meth:`~fr.cnes.sirius.patrius.math.stat.regression.RegressionResults.getRSquared`
             
        
            Returns:
                adjusted R-Squared statistic
        
        
        """
        ...
    def getCovarianceOfParameters(self, int: int, int2: int) -> float:
        """
        
            Returns the covariance between regression parameters i and j.
        
            If there are problems with an ill conditioned design matrix then the covariance which involves redundant columns will be
            assigned :code:`Double.NaN`.
        
            Parameters:
                i (int): :code:`i`th regression parameter.
                j (int): :code:`j`th regression parameter.
        
            Returns:
                the covariance of the parameter estimates.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if :code:`i` or :code:`j` is not in the interval :code:`[0, number of parameters)`.
        
        
        """
        ...
    def getErrorSumSquares(self) -> float:
        """
        
            Returns the ` sum of squared errors <http://www.xycoon.com/SumOfSquares.htm>` (SSE) associated with the regression
            model.
        
            The return value is constrained to be non-negative - i.e., if due to rounding errors the computational formula returns a
            negative result, 0 is returned.
        
            **Preconditions**:
        
              - numberOfParameters data pairs must have been added before invoking this method. If this method is invoked before a model
                can be estimated, :code:`Double,NaN` is returned.
        
        
            Returns:
                sum of squared errors associated with the regression model
        
        
        """
        ...
    def getMeanSquareError(self) -> float:
        """
        
            Returns the sum of squared errors divided by the degrees of freedom, usually abbreviated MSE.
        
            If there are fewer than **numberOfParameters + 1** data pairs in the model, or if there is no variation in :code:`x`,
            this returns :code:`Double.NaN`.
        
            Returns:
                sum of squared deviations of y values
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of observations added to the regression model.
        
            Returns:
                Number of observations, -1 if an error condition prevents estimation
        
        
        """
        ...
    def getNumberOfParameters(self) -> int:
        """
        
            Returns the number of parameters estimated in the model.
        
            This is the maximum number of regressors, some techniques may drop redundant parameters
        
            Returns:
                number of regressors, -1 if not estimated
        
        
        """
        ...
    def getParameterEstimate(self, int: int) -> float:
        """
        
            Returns the parameter estimate for the regressor at the given index.
        
            A redundant regressor will have its redundancy flag set, as well as a parameters estimated equal to :code:`Double.NaN`
        
            Parameters:
                index (int): Index.
        
            Returns:
                the parameters estimated for regressor at index.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if :code:`index` is not in the interval :code:`[0, number of parameters)`.
        
        
        """
        ...
    def getParameterEstimates(self) -> typing.MutableSequence[float]:
        """
        
            Returns a copy of the regression parameters estimates.
        
            The parameter estimates are returned in the natural order of the data.
        
            A redundant regressor will have its redundancy flag set, as will a parameter estimate equal to :code:`Double.NaN` .
        
            Returns:
                array of parameter estimates, null if no estimation occurred
        
        
        """
        ...
    def getRSquared(self) -> float:
        """
        
            Returns the ` coefficient of multiple determination <http://www.xycoon.com/coefficient1.htm>`, usually denoted r-square.
        
            **Preconditions**:
        
              - At least numberOfParameters observations (with at least numberOfParameters different x values) must have been added
                before invoking this method. If this method is invoked before a model can be estimated, :code:`Double,NaN` is returned.
        
        
            Returns:
                r-square, a double in the interval [0, 1]
        
        
        """
        ...
    def getRegressionSumSquares(self) -> float:
        """
        
            Returns the sum of squared deviations of the predicted y values about their mean (which equals the mean of y).
        
            This is usually abbreviated SSR or SSM. It is defined as SSM `here <http://www.xycoon.com/SumOfSquares.htm>`
        
            **Preconditions**:
        
              - At least two observations (with at least two different x values) must have been added before invoking this method. If
                this method is invoked before a model can be estimated, :code:`Double.NaN` is returned.
        
        
            Returns:
                sum of squared deviations of predicted y values
        
        
        """
        ...
    def getStdErrorOfEstimate(self, int: int) -> float:
        """
            Returns the `standard error of the parameter estimate at index <http://www.xycoon.com/standerrorb(1).htm>`, usually
            denoted s(b :sub:`index` ).
        
            Parameters:
                index (int): Index.
        
            Returns:
                the standard errors associated with parameters estimated at index.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if :code:`index` is not in the interval :code:`[0, number of parameters)`.
        
        
        """
        ...
    def getStdErrorOfEstimates(self) -> typing.MutableSequence[float]:
        """
        
            Returns the `standard error of the parameter estimates <http://www.xycoon.com/standerrorb(1).htm>`, usually denoted s(b
            :sub:`i` ).
        
            If there are problems with an ill conditioned design matrix then the regressor which is redundant will be assigned
            :code:`Double.NaN`.
        
            Returns:
                an array standard errors associated with parameters estimates, null if no estimation occurred
        
        
        """
        ...
    def getTotalSumSquares(self) -> float:
        """
        
            Returns the sum of squared deviations of the y values about their mean.
        
            This is defined as SSTO `here <http://www.xycoon.com/SumOfSquares.htm>`.
        
            If :code:`n < 2`, this returns :code:`Double.NaN`.
        
            Returns:
                sum of squared deviations of y values
        
        
        """
        ...
    def hasIntercept(self) -> bool:
        """
            Returns true if the regression model has been computed including an intercept. In this case, the coefficient of the
            intercept is the first element of the
            :meth:`~fr.cnes.sirius.patrius.math.stat.regression.RegressionResults.getParameterEstimates`.
        
            Returns:
                true if the model has an intercept term
        
        
        """
        ...

class UpdatingMultipleLinearRegression:
    """
    public interface UpdatingMultipleLinearRegression
    
        An interface for regression models allowing for dynamic updating of the data. That is, the entire data set need not be
        loaded into memory. As observations become available, they can be added to the regression model and an updated estimate
        regression statistics can be calculated.
    
        Since:
            3.0
    """
    def addObservation(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> None:
        """
            Adds one observation to the regression model.
        
            Parameters:
                x (double[]): the independent variables which form the design matrix
                y (double): the dependent or response variable
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.stat.regression.ModelSpecificationException`: if the length of :code:`x` does not equal the number of independent variables in the model
        
        
        """
        ...
    def addObservations(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Adds a series of observations to the regression model. The lengths of x and y must be the same and x must be
            rectangular.
        
            Parameters:
                x (double[][]): a series of observations on the independent variables
                y (double[]): a series of observations on the dependent variable The length of x and y must be the same
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.stat.regression.ModelSpecificationException`: if :code:`x` is not rectangular, does not match the length of :code:`y` or does not contain sufficient data to estimate
                    the model
        
        
        """
        ...
    def clear(self) -> None:
        """
            Clears internal buffers and resets the regression model. This means all data and derived values are initialized
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of observations added to the regression model.
        
            Returns:
                Number of observations
        
        
        """
        ...
    def hasIntercept(self) -> bool:
        """
            Returns true if a constant has been included false otherwise.
        
            Returns:
                true if constant exists, false otherwise
        
        
        """
        ...
    @typing.overload
    def regress(self) -> RegressionResults:
        """
            Performs a regression on data present in buffers and outputs a RegressionResults object
        
            Returns:
                RegressionResults acts as a container of regression output
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.stat.regression.ModelSpecificationException`: if the model is not correctly specified
                :class:`~fr.cnes.sirius.patrius.math.exception.NoDataException`: if there is not sufficient data in the model to estimate the regression parameters
        
        """
        ...
    @typing.overload
    def regress(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> RegressionResults:
        """
            Performs a regression on data present in buffers including only regressors indexed in variablesToInclude and outputs a
            RegressionResults object
        
            Parameters:
                variablesToInclude (int[]): an array of indices of regressors to include
        
            Returns:
                RegressionResults acts as a container of regression output
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.stat.regression.ModelSpecificationException`: if the model is not correctly specified
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the variablesToInclude array is null or zero length
        
        
        """
        ...

class AbstractMultipleLinearRegression(MultipleLinearRegression):
    def __init__(self): ...
    def estimateErrorVariance(self) -> float: ...
    def estimateRegressandVariance(self) -> float: ...
    def estimateRegressionParameters(self) -> typing.MutableSequence[float]: ...
    def estimateRegressionParametersStandardErrors(self) -> typing.MutableSequence[float]: ...
    def estimateRegressionParametersVariance(self) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def estimateRegressionStandardError(self) -> float: ...
    def estimateResiduals(self) -> typing.MutableSequence[float]: ...
    def isNoIntercept(self) -> bool: ...
    def newSampleData(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> None: ...
    def setNoIntercept(self, boolean: bool) -> None: ...

class MillerUpdatingRegression(UpdatingMultipleLinearRegression):
    @typing.overload
    def __init__(self, int: int, boolean: bool): ...
    @typing.overload
    def __init__(self, int: int, boolean: bool, double: float): ...
    def addObservation(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> None: ...
    def addObservations(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def clear(self) -> None: ...
    def getDiagonalOfHatMatrix(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    def getN(self) -> int: ...
    def getOrderOfRegressors(self) -> typing.MutableSequence[int]: ...
    def getPartialCorrelations(self, int: int) -> typing.MutableSequence[float]: ...
    def hasIntercept(self) -> bool: ...
    @typing.overload
    def regress(self) -> RegressionResults: ...
    @typing.overload
    def regress(self, int: int) -> RegressionResults: ...
    @typing.overload
    def regress(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> RegressionResults: ...

class SimpleRegression(java.io.Serializable, UpdatingMultipleLinearRegression):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...
    @typing.overload
    def addData(self, double: float, double2: float) -> None: ...
    @typing.overload
    def addData(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def addObservation(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> None: ...
    def addObservations(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def clear(self) -> None: ...
    def getIntercept(self) -> float: ...
    def getInterceptStdErr(self) -> float: ...
    def getMeanSquareError(self) -> float: ...
    def getN(self) -> int: ...
    def getR(self) -> float: ...
    def getRSquare(self) -> float: ...
    def getRegressionSumSquares(self) -> float: ...
    def getSignificance(self) -> float: ...
    def getSlope(self) -> float: ...
    @typing.overload
    def getSlopeConfidenceInterval(self) -> float: ...
    @typing.overload
    def getSlopeConfidenceInterval(self, double: float) -> float: ...
    def getSlopeStdErr(self) -> float: ...
    def getSumOfCrossProducts(self) -> float: ...
    def getSumSquaredErrors(self) -> float: ...
    def getTotalSumSquares(self) -> float: ...
    def getXSumSquares(self) -> float: ...
    def hasIntercept(self) -> bool: ...
    def predict(self, double: float) -> float: ...
    @typing.overload
    def regress(self) -> RegressionResults: ...
    @typing.overload
    def regress(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> RegressionResults: ...
    @typing.overload
    def removeData(self, double: float, double2: float) -> None: ...
    @typing.overload
    def removeData(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...

class GLSMultipleLinearRegression(AbstractMultipleLinearRegression):
    """
    public class GLSMultipleLinearRegression extends :class:`~fr.cnes.sirius.patrius.math.stat.regression.AbstractMultipleLinearRegression`
    
        The GLS implementation of the multiple linear regression. GLS assumes a general covariance matrix Omega of the error
    
        .. code-block: java
        
        
         u ~ N(0, Omega)
         
        Estimated by GLS,
    
        .. code-block: java
        
        
         b=(X' Omega^-1 X)^-1X'Omega^-1 y
         
        whose variance is
    
        .. code-block: java
        
        
         Var(b)=(X' Omega^-1 X)^-1
         
    
        Since:
            2.0
    """
    def __init__(self): ...
    @typing.overload
    def newSampleData(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> None:
        """
            Replace sample data, overriding any previous sample.
        
            Parameters:
                y (double[]): y values of the sample
                x (double[][]): x values of the sample
                covariance (double[][]): array representing the covariance matrix
        
        
        """
        ...
    @typing.overload
    def newSampleData(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...

class OLSMultipleLinearRegression(AbstractMultipleLinearRegression):
    def __init__(self): ...
    def calculateAdjustedRSquared(self) -> float: ...
    def calculateHat(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def calculateRSquared(self) -> float: ...
    def calculateResidualSumOfSquares(self) -> float: ...
    def calculateTotalSumOfSquares(self) -> float: ...
    @typing.overload
    def newSampleData(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    @typing.overload
    def newSampleData(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.stat.regression")``.

    AbstractMultipleLinearRegression: typing.Type[AbstractMultipleLinearRegression]
    GLSMultipleLinearRegression: typing.Type[GLSMultipleLinearRegression]
    MillerUpdatingRegression: typing.Type[MillerUpdatingRegression]
    ModelSpecificationException: typing.Type[ModelSpecificationException]
    MultipleLinearRegression: typing.Type[MultipleLinearRegression]
    OLSMultipleLinearRegression: typing.Type[OLSMultipleLinearRegression]
    RegressionResults: typing.Type[RegressionResults]
    SimpleRegression: typing.Type[SimpleRegression]
    UpdatingMultipleLinearRegression: typing.Type[UpdatingMultipleLinearRegression]
