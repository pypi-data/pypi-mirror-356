
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.analysis.function
import fr.cnes.sirius.patrius.math.analysis.polynomials
import fr.cnes.sirius.patrius.math.optim.nonlinear.vector
import fr.cnes.sirius.patrius.time
import java.io
import jpype
import typing



_CurveFitter__T = typing.TypeVar('_CurveFitter__T', bound=fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction)  # <T>
class CurveFitter(typing.Generic[_CurveFitter__T]):
    def __init__(self, multivariateVectorOptimizer: fr.cnes.sirius.patrius.math.optim.nonlinear.vector.MultivariateVectorOptimizer): ...
    @typing.overload
    def addObservedPoint(self, double: float, double2: float) -> None: ...
    @typing.overload
    def addObservedPoint(self, double: float, double2: float, double3: float) -> None: ...
    @typing.overload
    def addObservedPoint(self, weightedObservedPoint: 'WeightedObservedPoint') -> None: ...
    def clearObservations(self) -> None: ...
    @typing.overload
    def fit(self, t: _CurveFitter__T, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def fit(self, int: int, t: _CurveFitter__T, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    def getObservations(self) -> typing.MutableSequence['WeightedObservedPoint']: ...

class LinearRegression:
    """
    public final class LinearRegression extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class enables to perform linear regression.
    """
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    def getOrigin(self) -> float:
        """
            Get the origin A of the linear model y = A + B*x
        
            Returns:
                the origin of the linear model
        
        
        """
        ...
    def getSlope(self) -> float:
        """
            Get the slope B of the linear model y = A + B*x
        
            Returns:
                the slope of the linear model
        
        
        """
        ...

class SecularAndHarmonic:
    """
    public class SecularAndHarmonic extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class for fitting evolution of osculating orbital parameters.
    
        This class allows conversion from osculating parameters to mean parameters.
    """
    def __init__(self, int: int, *double: float): ...
    def addPoint(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> None:
        """
            Add a fitting point.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date of the point
                osculatingValue (double): osculating value
        
        
        """
        ...
    def approximateAsPolynomialOnly(self, int: int, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, int2: int, int3: int, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate3: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> typing.MutableSequence[float]:
        """
            Approximate an already fitted model to polynomial only terms.
        
            This method is mainly used in order to combine the large amplitude long periods with the secular part as a new
            approximate polynomial model over some time range. This should be used rather than simply extracting the polynomial
            coefficients from :meth:`~fr.cnes.sirius.patrius.math.fitting.SecularAndHarmonic.getFittedParameters` when some periodic
            terms amplitudes are large (for example Sun resonance effects on local solar time in sun synchronous orbits). In theses
            cases, the pure polynomial secular part in the coefficients may be far from the mean model.
        
            Parameters:
                combinedDegree (int): desired degree for the combined polynomial
                combinedReference (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): desired reference date for the combined polynomial
                meanDegree (int): degree of polynomial secular part to consider
                meanHarmonics (int): number of harmonics terms to consider
                start (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): start date of the approximation time range
                end (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): end date of the approximation time range
                step (double): sampling step
        
            Returns:
                coefficients of the approximate polynomial (in increasing degree order), using the user provided reference date
        
        
        """
        ...
    def fit(self) -> None:
        """
            Fit parameters.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.fitting.SecularAndHarmonic.getFittedParameters`
        
        
        """
        ...
    def getFittedParameters(self) -> typing.MutableSequence[float]:
        """
            Get a copy of the last fitted parameters.
        
            Returns:
                copy of the last fitted parameters.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.fitting.SecularAndHarmonic.fit`
        
        
        """
        ...
    def getHarmonicAmplitude(self) -> float:
        """
            Get an upper bound of the fitted harmonic amplitude.
        
            Returns:
                upper bound of the fitted harmonic amplitude
        
        
        """
        ...
    def getReferenceDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the reference date.
        
            Returns:
                reference date
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.fitting.SecularAndHarmonic.resetFitting`
        
        
        """
        ...
    def meanDerivative(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, int: int, int2: int) -> float:
        """
            Get mean derivative, truncated to first components.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                degree (int): degree of polynomial secular part to consider
                harmonics (int): number of harmonics terms to consider
        
            Returns:
                mean derivative at current date
        
        
        """
        ...
    def meanSecondDerivative(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, int: int, int2: int) -> float:
        """
            Get mean second derivative, truncated to first components.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                degree (int): degree of polynomial secular part
                harmonics (int): number of harmonics terms to consider
        
            Returns:
                mean second derivative at current date
        
        
        """
        ...
    def meanValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, int: int, int2: int) -> float:
        """
            Get mean value, truncated to first components.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                degree (int): degree of polynomial secular part to consider
                harmonics (int): number of harmonics terms to consider
        
            Returns:
                mean value at current date
        
        
        """
        ...
    def osculatingDerivative(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get fitted osculating derivative.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
        
            Returns:
                osculating derivative at current date
        
        
        """
        ...
    def osculatingSecondDerivative(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get fitted osculating second derivative.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
        
            Returns:
                osculating second derivative at current date
        
        
        """
        ...
    def osculatingValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get fitted osculating value.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
        
            Returns:
                osculating value at current date
        
        
        """
        ...
    def resetFitting(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, *double: float) -> None:
        """
            Reset fitting.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): reference date
                initialGuess (double...): initial guess for the parameters
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.fitting.SecularAndHarmonic.getReferenceDate`
        
        
        """
        ...

class WeightedObservedPoint(java.io.Serializable):
    """
    public class WeightedObservedPoint extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class is a simple container for weighted observed point in
        :class:`~fr.cnes.sirius.patrius.math.fitting.CurveFitter`.
    
        Instances of this class are guaranteed to be immutable.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float): ...
    def getWeight(self) -> float:
        """
            Gets the weight of the measurement in the fitting process.
        
            Returns:
                the weight of the measurement in the fitting process.
        
        
        """
        ...
    def getX(self) -> float:
        """
            Gets the abscissa of the point.
        
            Returns:
                the abscissa of the point.
        
        
        """
        ...
    def getY(self) -> float:
        """
            Gets the observed value of the function at x.
        
            Returns:
                the observed value of the function at x.
        
        
        """
        ...

class GaussianFitter(CurveFitter[fr.cnes.sirius.patrius.math.analysis.function.Gaussian.Parametric]):
    """
    public class GaussianFitter extends :class:`~fr.cnes.sirius.patrius.math.fitting.CurveFitter`<:class:`~fr.cnes.sirius.patrius.math.analysis.function.Gaussian.Parametric`>
    
        Fits points to a :class:`~fr.cnes.sirius.patrius.math.analysis.function.Gaussian.Parametric` function.
    
        Usage example:
    
        .. code-block: java
        
        
         GaussianFitter fitter = new GaussianFitter(
             new LevenbergMarquardtOptimizer());
         fitter.addObservedPoint(4.0254623, 531026.0);
         fitter.addObservedPoint(4.03128248, 984167.0);
         fitter.addObservedPoint(4.03839603, 1887233.0);
         fitter.addObservedPoint(4.04421621, 2687152.0);
         fitter.addObservedPoint(4.05132976, 3461228.0);
         fitter.addObservedPoint(4.05326982, 3580526.0);
         fitter.addObservedPoint(4.05779662, 3439750.0);
         fitter.addObservedPoint(4.0636168, 2877648.0);
         fitter.addObservedPoint(4.06943698, 2175960.0);
         fitter.addObservedPoint(4.07525716, 1447024.0);
         fitter.addObservedPoint(4.08237071, 717104.0);
         fitter.addObservedPoint(4.08366408, 620014.0);
         double[] parameters = fitter.fit();
         
    
        Since:
            2.2
    """
    def __init__(self, multivariateVectorOptimizer: fr.cnes.sirius.patrius.math.optim.nonlinear.vector.MultivariateVectorOptimizer): ...
    @typing.overload
    def fit(self, t: fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def fit(self, int: int, t: fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def fit(self) -> typing.MutableSequence[float]:
        """
            Fits a Gaussian function to the observed points.
        
            Returns:
                the parameters of the Gaussian function that best fits the observed points (in the same order as above).
        
        
        """
        ...
    @typing.overload
    def fit(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Fits a Gaussian function to the observed points.
        
            Parameters:
                initialGuess (double[]): First guess values in the following order:
        
                      - Norm
                      - Mean
                      - Sigma
        
        
            Returns:
                the parameters of the Gaussian function that best fits the observed points (in the same order as above).
        
            Since:
                3.0
        
        """
        ...
    class ParameterGuesser:
        def __init__(self, weightedObservedPointArray: typing.Union[typing.List[WeightedObservedPoint], jpype.JArray]): ...
        def guess(self) -> typing.MutableSequence[float]: ...

class HarmonicFitter(CurveFitter[fr.cnes.sirius.patrius.math.analysis.function.HarmonicOscillator.Parametric]):
    """
    public class HarmonicFitter extends :class:`~fr.cnes.sirius.patrius.math.fitting.CurveFitter`<:class:`~fr.cnes.sirius.patrius.math.analysis.function.HarmonicOscillator.Parametric`>
    
        Class that implements a curve fitting specialized for sinusoids. Harmonic fitting is a very simple case of curve
        fitting. The estimated coefficients are the amplitude a, the pulsation ω and the phase φ: :code:`f (t) = a cos (ω t +
        φ)`. They are searched by a least square estimator initialized with a rough guess based on integrals.
    
        Since:
            2.0
    """
    def __init__(self, multivariateVectorOptimizer: fr.cnes.sirius.patrius.math.optim.nonlinear.vector.MultivariateVectorOptimizer): ...
    @typing.overload
    def fit(self, t: fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def fit(self, int: int, t: fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def fit(self) -> typing.MutableSequence[float]:
        """
            Fit an harmonic function to the observed points. An initial guess will be automatically computed.
        
            Returns:
                the parameters of the harmonic function that best fits the observed points (see the other null method.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the sample is too short for the the first guess to be computed.
                :class:`~fr.cnes.sirius.patrius.math.exception.ZeroException`: if the first guess cannot be computed because the abscissa range is zero.
        
        
        """
        ...
    @typing.overload
    def fit(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Fit an harmonic function to the observed points.
        
            Parameters:
                initialGuess (double[]): First guess values in the following order:
        
                      - Amplitude
                      - Angular frequency
                      - Phase
        
        
            Returns:
                the parameters of the harmonic function that best fits the observed points (in the same order as above).
        
        """
        ...
    class ParameterGuesser:
        def __init__(self, weightedObservedPointArray: typing.Union[typing.List[WeightedObservedPoint], jpype.JArray]): ...
        def guess(self) -> typing.MutableSequence[float]: ...

class PolynomialChebyshevFitter(CurveFitter[fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialChebyshevFunction]):
    """
    public class PolynomialChebyshevFitter extends :class:`~fr.cnes.sirius.patrius.math.fitting.CurveFitter`<:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialChebyshevFunction`>
    
        Chebyshev polynomial fitting is a very simple case of :class:`~fr.cnes.sirius.patrius.math.fitting.CurveFitter`. The
        estimated coefficients are the Chebyshev polynomial coefficients (see the null method).
    """
    def __init__(self, double: float, double2: float, multivariateVectorOptimizer: fr.cnes.sirius.patrius.math.optim.nonlinear.vector.MultivariateVectorOptimizer): ...
    @typing.overload
    def fit(self, t: fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Get the coefficients of the Chebyshev polynomial fitting the weighted data points. The degree of the fitting polynomial
            is :code:`guess.length - 1`.
        
            Parameters:
                guess (int): First guess for the coefficients. They must be sorted in increasing order of the polynomial's degree.
                maxEval (double[]): Maximum number of evaluations of the polynomial
        
            Returns:
                the coefficients of the Chebyshev polynomial that best fits the observed points
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the number of evaluations exceeds :code:`maxEval`
                :class:`~fr.cnes.sirius.patrius.math.exception.ConvergenceException`: if the algorithm failed to converge
        
        """
        ...
    @typing.overload
    def fit(self, int: int, t: fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def fit(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Get the coefficients of the Chebyshev polynomial fitting the weighted data points. The degree of the fitting polynomial
            is :code:`guess.length - 1`.
        
            Parameters:
                guess (double[]): First guess for the coefficients. They must be sorted in increasing order of the polynomial's degree.
        
            Returns:
                the coefficients of the Chebyshev polynomial that best fits the observed points
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.ConvergenceException`: if the algorithm failed to converge.
        
        
        """
        ...
    @typing.overload
    def fit(self, int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...

class PolynomialFitter(CurveFitter[fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction.Parametric]):
    """
    public class PolynomialFitter extends :class:`~fr.cnes.sirius.patrius.math.fitting.CurveFitter`<:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction.Parametric`>
    
        Polynomial fitting is a very simple case of :class:`~fr.cnes.sirius.patrius.math.fitting.CurveFitter`. The estimated
        coefficients are the polynomial coefficients (see the null method).
    
        Since:
            2.0
    """
    def __init__(self, multivariateVectorOptimizer: fr.cnes.sirius.patrius.math.optim.nonlinear.vector.MultivariateVectorOptimizer): ...
    @typing.overload
    def fit(self, t: fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Get the coefficients of the polynomial fitting the weighted data points. The degree of the fitting polynomial is
            :code:`guess.length - 1`.
        
            Parameters:
                guess (int): First guess for the coefficients. They must be sorted in increasing order of the polynomial's degree.
                maxEval (double[]): Maximum number of evaluations of the polynomial.
        
            Returns:
                the coefficients of the polynomial that best fits the observed points.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the number of evaluations exceeds :code:`maxEval`.
                :class:`~fr.cnes.sirius.patrius.math.exception.ConvergenceException`: if the algorithm failed to converge.
        
        """
        ...
    @typing.overload
    def fit(self, int: int, t: fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def fit(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Get the coefficients of the polynomial fitting the weighted data points. The degree of the fitting polynomial is
            :code:`guess.length - 1`.
        
            Parameters:
                guess (double[]): First guess for the coefficients. They must be sorted in increasing order of the polynomial's degree.
        
            Returns:
                the coefficients of the polynomial that best fits the observed points.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.ConvergenceException`: if the algorithm failed to converge.
        
        
        """
        ...
    @typing.overload
    def fit(self, int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.fitting")``.

    CurveFitter: typing.Type[CurveFitter]
    GaussianFitter: typing.Type[GaussianFitter]
    HarmonicFitter: typing.Type[HarmonicFitter]
    LinearRegression: typing.Type[LinearRegression]
    PolynomialChebyshevFitter: typing.Type[PolynomialChebyshevFitter]
    PolynomialFitter: typing.Type[PolynomialFitter]
    SecularAndHarmonic: typing.Type[SecularAndHarmonic]
    WeightedObservedPoint: typing.Type[WeightedObservedPoint]
