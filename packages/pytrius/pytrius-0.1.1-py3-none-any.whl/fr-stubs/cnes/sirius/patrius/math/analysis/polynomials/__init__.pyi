
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.analysis.differentiation
import fr.cnes.sirius.patrius.math.analysis.integration
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.math.util
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import jpype
import typing



class ChebyshevDecompositionEngine:
    @staticmethod
    def approximateChebyshevFunction(univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], int: int, double: float, double2: float, int2: int) -> 'PolynomialChebyshevFunction': ...
    @typing.overload
    @staticmethod
    def interpolateChebyshevFunction(double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> 'PolynomialChebyshevFunction': ...
    @typing.overload
    @staticmethod
    def interpolateChebyshevFunction(univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], int: int, double: float, double2: float) -> 'PolynomialChebyshevFunction': ...

class ElementaryMultiplicationTypes:
    """
    public final class ElementaryMultiplicationTypes extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class is used to represent elementary trigonometric polynomials cos and sin.
    
        Since:
            1.2
    """
    @staticmethod
    def componentProvider(elementaryType: 'ElementaryMultiplicationTypes.ElementaryType', int: int, double: float) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction:
        """
            This method provides the :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction` cos(intermediateOrder * omega
            * x) or sin
        
            Parameters:
                intermediateType (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.ElementaryMultiplicationTypes.ElementaryType`): cos or sin
                intermediateOrder (int): order of elementary function
                period (double): period such as :code:`omega = 2 * pi / period`
        
            Returns:
                function as a :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.FourierDecompositionEngine`
        
        
        """
        ...
    class ElementaryType(java.lang.Enum['ElementaryMultiplicationTypes.ElementaryType']):
        COS: typing.ClassVar['ElementaryMultiplicationTypes.ElementaryType'] = ...
        SIN: typing.ClassVar['ElementaryMultiplicationTypes.ElementaryType'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'ElementaryMultiplicationTypes.ElementaryType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['ElementaryMultiplicationTypes.ElementaryType']: ...

class FourierDecompositionEngine:
    """
    public final class FourierDecompositionEngine extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Decompose a :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction` as a Fourier Series using
        :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction` representation.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`
    """
    def __init__(self, univariateIntegrator: fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator): ...
    def decompose(self) -> 'FourierSeriesApproximation':
        """
            Decompose function :code:`f`, using user given period :code:`t` and :code:`integrator`, into a Fourier Series of order
            :code:`order`. **Warning :** the user must make sure the given period :code:`t` is coherent with the function :code:`f`.
        
            Returns:
                A :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeriesApproximation` instance containing the Fourier
                Series approximation of the user function and the latter.
        
        
        """
        ...
    def getMaxEvals(self) -> int:
        """
        
            Returns:
                the maximum evaluations for the integrator
        
        
        """
        ...
    def getOrder(self) -> int:
        """
        
            Returns:
                the order
        
        
        """
        ...
    def getPeriod(self) -> float:
        """
        
            Returns:
                the period of function f
        
        
        """
        ...
    def setFunction(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float) -> None:
        """
            Set the :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction` to decompose and its period.
        
        
            **Warning :** The user should make sure the period specified is coherent with the function.
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): to decompose
                period (double): period of function
        
        
        """
        ...
    def setIntegrator(self, univariateIntegrator: fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator) -> None:
        """
            Set the :class:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator` to use for the serires
            coefficient computation.
        
            Parameters:
                newIntegrator (:class:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator`): to use
        
        
        """
        ...
    def setMaxEvals(self, int: int) -> None:
        """
            Set the maximum evaluations allowed for the integrator. Default is 100
        
            Parameters:
                maxEvaluations (int): the maximum evaluations for the integrator
        
        
        """
        ...
    def setOrder(self, int: int) -> None:
        """
        
            Parameters:
                newOrder (int): the order to set
        
        
        """
        ...

class FourierSeries(fr.cnes.sirius.patrius.math.analysis.DifferentiableIntegrableUnivariateFunction):
    def __init__(self, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def derivative(self) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction: ...
    @typing.overload
    def derivative(self, int: int) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction: ...
    def derivativeValue(self, int: int, double: float) -> float: ...
    def getAngularFrequency(self) -> float: ...
    def getConstant(self) -> float: ...
    def getCosArray(self) -> typing.MutableSequence[float]: ...
    def getOrder(self) -> int: ...
    def getPeriod(self) -> float: ...
    def getSinArray(self) -> typing.MutableSequence[float]: ...
    def negate(self) -> 'FourierSeries': ...
    @typing.overload
    def polynomialDerivative(self) -> 'FourierSeries': ...
    @typing.overload
    def polynomialDerivative(self, int: int) -> 'FourierSeries': ...
    def polynomialPrimitive(self) -> 'FourierSeries': ...
    def primitive(self) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction: ...
    def primitiveValue(self, double: float) -> float: ...
    def scalarAdd(self, double: float) -> 'FourierSeries': ...
    def scalarDivide(self, double: float) -> 'FourierSeries': ...
    def scalarMultiply(self, double: float) -> 'FourierSeries': ...
    def scalarSubtract(self, double: float) -> 'FourierSeries': ...
    def toString(self) -> str: ...
    @typing.overload
    def value(self, double: float) -> float: ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class FourierSeriesApproximation(java.io.Serializable):
    """
    public class FourierSeriesApproximation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Holder for a :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction` and its
        :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries` approximation
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.FourierDecompositionEngine`, :meth:`~serialized`
    """
    def getFourier(self) -> FourierSeries:
        """
        
            Returns:
                the fourier series approximation
        
        
        """
        ...
    def getFunction(self) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction:
        """
        
            Returns:
                the function
        
        
        """
        ...
    def getPeriod(self) -> float:
        """
        
            Returns:
                period of functions
        
        
        """
        ...
    def toString(self) -> str:
        """
            Get String representation of Fourier Series
        
            Overrides:
                 in class 
        
            Returns:
                string
        
        
        """
        ...

class HelmholtzPolynomial(java.io.Serializable):
    """
    public final class HelmholtzPolynomial extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class represents Helmholtz polynomial.
    
        Since:
            3.1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int, int2: int): ...
    def computeHelmholtzPolynomial(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Calculate the value of the polynomial in a given point.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the given point
        
            Returns:
                value of polynomial
        
        
        """
        ...
    def getDpph(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Get the H'lm coefficients
        
            Returns:
                the H'lm coefficients
        
        
        """
        ...
    def getDsph(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Get the H''lm coefficients
        
            Returns:
                the H''lm coefficients
        
        
        """
        ...
    def getPh(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Get the Hlm coefficients
        
            Returns:
                the Hlm coefficients
        
        
        """
        ...

class PolynomialFunctionInterface(fr.cnes.sirius.patrius.math.analysis.UnivariateFunction):
    """
    public interface PolynomialFunctionInterface extends :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
    
        Represents an interface for polynomial functions.
    
        Since:
            4.11
    """
    def derivative(self) -> 'PolynomialFunctionInterface':
        """
            Return the derivative date polynomial function.
        
            Returns:
                the derivative date polynomial function
        
        
        """
        ...
    def getCoefficients(self) -> typing.MutableSequence[float]:
        """
            Get the polynomial coefficients.
        
            Returns:
                the polynomial coefficients
        
        
        """
        ...
    def getDegree(self) -> int:
        """
            Return the polynomial degree.
        
            Returns:
                the polynomial degree
        
        
        """
        ...
    def getPolynomialType(self) -> 'PolynomialType':
        """
            Return the type of this polynomial function.
        
            Returns:
                the type of this polynomial function
        
        
        """
        ...
    def primitive(self, double: float, double2: float) -> 'PolynomialFunctionInterface':
        """
            Return the primitive polynomial function.
        
            Parameters:
                abscissa0 (double): the abscissa of interest
                ordinate0 (double): the function value at abscissa0
        
            Returns:
                the primitive polynomial function
        
        
        """
        ...

class PolynomialFunctionLagrangeForm(fr.cnes.sirius.patrius.math.analysis.UnivariateFunction):
    """
    public class PolynomialFunctionLagrangeForm extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
    
        Implements the representation of a real polynomial function in ` Lagrange Form
        <http://mathworld.wolfram.com/LagrangeInterpolatingPolynomial.html>`. For reference, see **Introduction to Numerical
        Analysis**, ISBN 038795452X, chapter 2.
    
        The approximated function should be smooth enough for Lagrange polynomial to work well. Otherwise, consider using
        splines instead.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    def degree(self) -> int:
        """
            Returns the degree of the polynomial.
        
            Returns:
                the degree of the polynomial
        
        
        """
        ...
    @staticmethod
    def evaluate(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float) -> float:
        """
            Evaluate the Lagrange polynomial using ` Neville's Algorithm <http://mathworld.wolfram.com/NevillesAlgorithm.html>`. It
            takes O(n^2) time.
        
            Parameters:
                x (double[]): Interpolating points array.
                y (double[]): Interpolating values array.
                z (double): Point at which the function value is to be computed.
        
            Returns:
                the function value.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if :code:`x` and :code:`y` have different lengths.
                :class:`~fr.cnes.sirius.patrius.math.exception.NonMonotonicSequenceException`: if :code:`x` is not sorted in strictly increasing order.
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the size of :code:`x` is less than 2.
        
        
        """
        ...
    def getCoefficients(self) -> typing.MutableSequence[float]:
        """
            Returns a copy of the coefficients array.
        
            Changes made to the returned copy will not affect the polynomial.
        
            Note that coefficients computation can be ill-conditioned. Use with caution and only when it is necessary.
        
            Returns:
                a fresh copy of the coefficients array
        
        
        """
        ...
    def getInterpolatingPoints(self) -> typing.MutableSequence[float]:
        """
            Returns a copy of the interpolating points array.
        
            Changes made to the returned copy will not affect the polynomial.
        
            Returns:
                a fresh copy of the interpolating points array
        
        
        """
        ...
    def getInterpolatingTabValues(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Returns a copy of the interpolating values matrix.
        
            Changes made to the returned copy will not affect the polynomial.
        
            Returns:
                a fresh copy of the interpolating values matrix
        
        
        """
        ...
    def getInterpolatingValues(self) -> typing.MutableSequence[float]:
        """
            Returns a copy of the interpolating values array.
        
            Changes made to the returned copy will not affect the polynomial.
        
            Returns:
                a fresh copy of the interpolating values array
        
        
        """
        ...
    def value(self, double: float) -> float:
        """
            Calculate the function value at the given point.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                z (double): Point at which the function value is to be computed.
        
            Returns:
                the function value.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if :code:`x` and :code:`y` have different lengths.
                :class:`~fr.cnes.sirius.patrius.math.exception.NonMonotonicSequenceException`: if :code:`x` is not sorted in strictly increasing order.
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the size of :code:`x` is less than 2.
        
        
        """
        ...
    def valueIndex(self, int: int, double: float) -> float:
        """
            Calculate the function value at the given point.
        
            Parameters:
                index (int): : the function to be interpolated, ie btw 0 and yTab.length-1
                z (double): Point at which the function value is to be computed.
        
            Returns:
                the function value.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if :code:`x` and :code:`y` have different lengths.
                :class:`~fr.cnes.sirius.patrius.math.exception.NonMonotonicSequenceException`: if :code:`x` is not sorted in strictly increasing order.
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the size of :code:`x` is less than 2.
        
        
        """
        ...
    @staticmethod
    def verifyInterpolationArray(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool) -> bool:
        """
            Check that the interpolation arrays are valid. The arrays features checked by this method are that both arrays have the
            same length and this length is at least 2.
        
            Parameters:
                x (double[]): Interpolating points array.
                y (double[]): Interpolating values array.
                abort (boolean): Whether to throw an exception if :code:`x` is not sorted.
        
            Returns:
                :code:`false` if the :code:`x` is not sorted in increasing order, :code:`true` otherwise.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array lengths are different.
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the number of points is less than 2.
                :class:`~fr.cnes.sirius.patrius.math.exception.NonMonotonicSequenceException`: if :code:`x` is not sorted in strictly increasing order and :code:`abort` is :code:`true`.
        
            Also see:
                null, :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunctionLagrangeForm.computeCoefficients`
        
        
        """
        ...

class PolynomialFunctionNewtonForm(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class PolynomialFunctionNewtonForm extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Implements the representation of a real polynomial function in Newton Form. For reference, see **Elementary Numerical
        Analysis**, ISBN 0070124477, chapter 2.
    
        The formula of polynomial in Newton form is p(x) = a[0] + a[1](x-c[0]) + a[2](x-c[0])(x-c[1]) + ... +
        a[n](x-c[0])(x-c[1])...(x-c[n-1]) Note that the length of a[] is one more than the length of c[]
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    def degree(self) -> int:
        """
            Returns the degree of the polynomial.
        
            Returns:
                the degree of the polynomial
        
        
        """
        ...
    @staticmethod
    def evaluate(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float) -> float:
        """
            Evaluate the Newton polynomial using nested multiplication. It is also called ` Horner's Rule
            <http://mathworld.wolfram.com/HornersRule.html>` and takes O(N) time.
        
            Parameters:
                a (double[]): Coefficients in Newton form formula.
                c (double[]): Centers.
                z (double): Point at which the function value is to be computed.
        
            Returns:
                the function value.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if any argument is :code:`null`.
                :class:`~fr.cnes.sirius.patrius.math.exception.NoDataException`: if any array has zero length.
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the size difference between :code:`a` and :code:`c` is not equal to 1.
        
        
        """
        ...
    def getCenters(self) -> typing.MutableSequence[float]:
        """
            Returns a copy of the centers array.
        
            Changes made to the returned copy will not affect the polynomial.
        
            Returns:
                a fresh copy of the centers array.
        
        
        """
        ...
    def getCoefficients(self) -> typing.MutableSequence[float]:
        """
            Returns a copy of the coefficients array.
        
            Changes made to the returned copy will not affect the polynomial.
        
            Returns:
                a fresh copy of the coefficients array.
        
        
        """
        ...
    def getNewtonCoefficients(self) -> typing.MutableSequence[float]:
        """
            Returns a copy of coefficients in Newton form formula.
        
            Changes made to the returned copy will not affect the polynomial.
        
            Returns:
                a fresh copy of coefficients in Newton form formula
        
        
        """
        ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Calculate the function value at the given point.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                z (double): Point at which the function value is to be computed.
        
            Returns:
                the function value.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class PolynomialSplineFunction(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class PolynomialSplineFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Represents a polynomial spline function.
    
        A **polynomial spline function** consists of a set of *interpolating polynomials* and an ascending array of domain *knot
        points*, determining the intervals over which the spline function is defined by the constituent polynomials. The
        polynomials are assumed to have been computed to match the values of another function at the knot points. The value
        consistency constraints are not currently enforced by :code:`PolynomialSplineFunction` itself, but are assumed to hold
        among the polynomials and knot points passed to the constructor.
    
        N.B.: The polynomials in the :code:`polynomials` property must be centered on the knot points to compute the spline
        function values. See below.
    
        The domain of the polynomial spline function is :code:`[smallest knot, largest knot]`. Attempts to evaluate the function
        at values outside of this range generate IllegalArgumentExceptions.
    
        The value of the polynomial spline function for an argument :code:`x` is computed as follows:
    
          1.  The knot array is searched to find the segment to which :code:`x` belongs. If :code:`x` is less than the smallest knot
            point or greater than the largest one, an :code:`IllegalArgumentException` is thrown.
          2.  Let :code:`j` be the index of the largest knot point that is less than or equal to :code:`x`. The value returned is
    
    
    :code:`polynomials[j](x - knot[j])`
    
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], polynomialFunctionArray: typing.Union[typing.List['PolynomialFunction'], jpype.JArray]): ...
    def derivative(self) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction:
        """
            Get the derivative of the polynomial spline function.
        
            Returns:
                the derivative function.
        
        
        """
        ...
    def getKnots(self) -> typing.MutableSequence[float]:
        """
            Get an array copy of the knot points. It returns a fresh copy of the array. Changes made to the copy will not affect the
            knots property.
        
            Returns:
                the knot points.
        
        
        """
        ...
    def getN(self) -> int:
        """
            Get the number of spline segments. It is also the number of polynomials and the number of knot points - 1.
        
            Returns:
                the number of spline segments.
        
        
        """
        ...
    def getPolynomials(self) -> typing.MutableSequence['PolynomialFunction']:
        """
            Get a copy of the interpolating polynomials array. It returns a fresh copy of the array. Changes made to the copy will
            not affect the polynomials property.
        
            Returns:
                the interpolating polynomials.
        
        
        """
        ...
    def polynomialSplineDerivative(self) -> 'PolynomialSplineFunction':
        """
            Get the derivative of the polynomial spline function.
        
            Returns:
                the derivative function.
        
        
        """
        ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value for the function. See
            :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialSplineFunction` for details on the algorithm for
            computing the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                v (double): Point for which the function value should be computed.
        
            Returns:
                the value.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if :code:`v` is outside of the domain of the spline function (smaller than the smallest knot point or larger than the
                    largest knot point).
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class PolynomialType(java.lang.Enum['PolynomialType']):
    """
    public enum PolynomialType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialType`>
    
        Describe the polynomial function type.
    
        Since:
            4.11
    """
    CLASSICAL: typing.ClassVar['PolynomialType'] = ...
    CHEBYSHEV: typing.ClassVar['PolynomialType'] = ...
    def getNature(self) -> str:
        """
            Getter for the nature of the polynomial function.
        
            Returns:
                the nature of the polynomial function
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'PolynomialType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                : if this enum type has no constant with the specified name
                : if the argument is null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['PolynomialType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (PolynomialType c : PolynomialType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class PolynomialsUtils:
    """
    public final class PolynomialsUtils extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        A collection of static methods that operate on or return polynomials.
    
        Since:
            2.0
    """
    @staticmethod
    def createChebyshevPolynomial(int: int) -> 'PolynomialFunction':
        """
            Create a Chebyshev polynomial of the first kind.
        
            `Chebyshev polynomials of the first kind <http://mathworld.wolfram.com/ChebyshevPolynomialoftheFirstKind.html>` are
            orthogonal polynomials. They can be defined by the following recurrence relations:
        
            .. code-block: java
            
            
              T :sub:`0` (X)   = 1
              T :sub:`1` (X)   = X
              T :sub:`k+1` (X) = 2X T :sub:`k` (X) - T :sub:`k-1` (X)
             
        
            Parameters:
                degree (int): degree of the polynomial
        
            Returns:
                Chebyshev polynomial of specified degree
        
        
        """
        ...
    @staticmethod
    def createHermitePolynomial(int: int) -> 'PolynomialFunction':
        """
            Create a Hermite polynomial.
        
            `Hermite polynomials <http://mathworld.wolfram.com/HermitePolynomial.html>` are orthogonal polynomials. They can be
            defined by the following recurrence relations:
        
            .. code-block: java
            
            
              H :sub:`0` (X)   = 1
              H :sub:`1` (X)   = 2X
              H :sub:`k+1` (X) = 2X H :sub:`k` (X) - 2k H :sub:`k-1` (X)
             
        
            Parameters:
                degree (int): degree of the polynomial
        
            Returns:
                Hermite polynomial of specified degree
        
        
        """
        ...
    @staticmethod
    def createJacobiPolynomial(int: int, int2: int, int3: int) -> 'PolynomialFunction':
        """
            Create a Jacobi polynomial.
        
            `Jacobi polynomials <http://mathworld.wolfram.com/JacobiPolynomial.html>` are orthogonal polynomials. They can be
            defined by the following recurrence relations:
        
            .. code-block: java
            
            
                    P :sub:`0`  :sup:`vw` (X)   = 1
                    P :sub:`-1`  :sup:`vw` (X)  = 0
              2k(k + v + w)(2k + v + w - 2) P :sub:`k`  :sup:`vw` (X) =
              (2k + v + w - 1)[(2k + v + w)(2k + v + w - 2) X + v :sup:`2`  - w :sup:`2` ] P :sub:`k-1`  :sup:`vw` (X)
              - 2(k + v - 1)(k + w - 1)(2k + v + w) P :sub:`k-2`  :sup:`vw` (X)
             
        
            Parameters:
                degree (int): degree of the polynomial
                v (int): first exponent
                w (int): second exponent
        
            Returns:
                Jacobi polynomial of specified degree
        
        
        """
        ...
    @staticmethod
    def createLaguerrePolynomial(int: int) -> 'PolynomialFunction':
        """
            Create a Laguerre polynomial.
        
            `Laguerre polynomials <http://mathworld.wolfram.com/LaguerrePolynomial.html>` are orthogonal polynomials. They can be
            defined by the following recurrence relations:
        
            .. code-block: java
            
            
                    L :sub:`0` (X)   = 1
                    L :sub:`1` (X)   = 1 - X
              (k+1) L :sub:`k+1` (X) = (2k + 1 - X) L :sub:`k` (X) - k L :sub:`k-1` (X)
             
        
            Parameters:
                degree (int): degree of the polynomial
        
            Returns:
                Laguerre polynomial of specified degree
        
        
        """
        ...
    @staticmethod
    def createLegendrePolynomial(int: int) -> 'PolynomialFunction':
        """
            Create a Legendre polynomial.
        
            `Legendre polynomials <http://mathworld.wolfram.com/LegendrePolynomial.html>` are orthogonal polynomials. They can be
            defined by the following recurrence relations:
        
            .. code-block: java
            
            
                    P :sub:`0` (X)   = 1
                    P :sub:`1` (X)   = X
              (k+1) P :sub:`k+1` (X) = (2k+1) X P :sub:`k` (X) - k P :sub:`k-1` (X)
             
        
            Parameters:
                degree (int): degree of the polynomial
        
            Returns:
                Legendre polynomial of specified degree
        
        
        """
        ...
    @staticmethod
    def getChebyshevAbscissas(double: float, double2: float, int: int) -> typing.MutableSequence[float]:
        """
            Compute the N Chebyshev abscissas on the range [start ; end] in a chronological (increasing) order.
        
            Parameters:
                start (double): Start range
                end (double): End range
                n (int): Number of points (coefficients) to evaluate
        
            Returns:
                the N Chebyshev abscissas
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NotStrictlyPositiveException`: if :code:`n <= 0`
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if :code:`start >= end`
        
        
        """
        ...
    @staticmethod
    def shift(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> typing.MutableSequence[float]:
        """
            Compute the coefficients of the polynomial :code:`P :sub:`s` (x)` whose values at point :code:`x` will be the same as
            the those from the original polynomial :code:`P(x)` when computed at :code:`x + shift`. Thus, if :code:`P(x) = Σ
            :sub:`i` a :sub:`i` x :sup:`i``, then
        
            .. code-block: java
            
            
              
               
                :code:`P :sub:`s` (x)`
                :code:`= Σ :sub:`i`  b :sub:`i`  x :sup:`i``
               
               
                
                :code:`= Σ :sub:`i`  a :sub:`i`  (x + shift) :sup:`i``
               
              
             
        
            Parameters:
                coefficients (double[]): Coefficients of the original polynomial.
                shift (double): Shift value.
        
            Returns:
                the coefficients :code:`b :sub:`i`` of the shifted polynomial.
        
        
        """
        ...

class TrigonometricPolynomialFunction(fr.cnes.sirius.patrius.math.analysis.DifferentiableIntegrableUnivariateFunction):
    """
    public final class TrigonometricPolynomialFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.DifferentiableIntegrableUnivariateFunction`
    
        This class is the Trigonometric Polynomial Function class. Given a constant :code:`a0`, and two arrays of same lengths
        :code:`a` and :code:`b`, the corresponding trigonometric polynomial function :code:`p` is given by the following
        expression :
    
    
        :code:`p(x) = a0 + sum( a(k) * cos(k*x) + b(k) * sin(k*x) , k, 1, n )`
    
    
        where :code:`a(k)` (resp . :code:`b(k)`) is the k :sup:`th` coefficient of the array :code:`a` (resp. :code:`b`).
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    def add(self, trigonometricPolynomialFunction: 'TrigonometricPolynomialFunction') -> 'TrigonometricPolynomialFunction':
        """
            Add two :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`
        
            Parameters:
                newPol (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`): polynomial to add to current
        
            Returns:
                resulting TrigonometricPolynomialFunction
        
        
        """
        ...
    @typing.overload
    def derivative(self) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction:
        """
            Compute and return derivative of polynomial
        
            Returns:
                derivative of polynomial function
        
        """
        ...
    @typing.overload
    def derivative(self, int: int) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction:
        """
            Compute and return n :sup:`th` derivative of polynomial
        
            Parameters:
                n (int): order of derivative
        
            Returns:
                n :sup:`th` derivative of polynomial function
        
        
        """
        ...
    def getA(self) -> typing.MutableSequence[float]:
        """
            Get array of cosine coefficients
        
            Returns:
                a
        
        
        """
        ...
    def getA0(self) -> float:
        """
            Get value of order zero coefficient
        
            Returns:
                a0
        
        
        """
        ...
    def getB(self) -> typing.MutableSequence[float]:
        """
            Get array of sine coefficients
        
            Returns:
                b
        
        
        """
        ...
    def getDegree(self) -> int:
        """
            Get polynomial degree
        
            Returns:
                n
        
        
        """
        ...
    def multiply(self, trigonometricPolynomialFunction: 'TrigonometricPolynomialFunction') -> 'TrigonometricPolynomialFunction':
        """
            Multiply this polynomial by another polynomial
        
            Parameters:
                polynomial (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`): polynomial to multiply instance by
        
            Returns:
                multiplied polynomials in a new instance
        
        
        """
        ...
    def negate(self) -> 'TrigonometricPolynomialFunction':
        """
            Negate polynomial
        
            Returns:
                negated polynomial
        
        
        """
        ...
    @typing.overload
    def polynomialDerivative(self) -> 'TrigonometricPolynomialFunction':
        """
            Returns the first order derivative as a
            :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`.
        
            Returns:
                the derivative polynomial.
        
        """
        ...
    @typing.overload
    def polynomialDerivative(self, int: int) -> 'TrigonometricPolynomialFunction':
        """
            Returns the n :sup:`th` order derivative as a
            :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`.
        
            Parameters:
                order (int): order of derivative (must be > 0)
        
            Returns:
                the derivative polynomial.
        
        
        """
        ...
    def polynomialPrimitive(self, double: float) -> 'TrigonometricPolynomialPrimitive':
        """
            Get primitive of :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`
        
            Parameters:
                constant (double): integration constant
        
            Returns:
                the primitive as a :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
        
        """
        ...
    def primitive(self) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction:
        """
            Get primitive of :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.IntegrableUnivariateFunction.primitive` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.IntegrableUnivariateFunction`
        
            Returns:
                the primitive as a :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
        
        """
        ...
    def scalarAdd(self, double: float) -> 'TrigonometricPolynomialFunction':
        """
            Add a scalar
        
            Parameters:
                scalar (double): to add
        
            Returns:
                new :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`
        
        
        """
        ...
    def scalarDivide(self, double: float) -> 'TrigonometricPolynomialFunction':
        """
            Divide by a scalar
        
            Parameters:
                scalar (double): to divide polynomial by
        
            Returns:
                polynomial divide by scalar
        
        
        """
        ...
    def scalarMultiply(self, double: float) -> 'TrigonometricPolynomialFunction':
        """
            Multiply by a scalar
        
            Parameters:
                scalar (double): to multiply polynomial by
        
            Returns:
                polynomial multiplied by scalar
        
        
        """
        ...
    def scalarSubtract(self, double: float) -> 'TrigonometricPolynomialFunction':
        """
            Subtract a scalar
        
            Parameters:
                scalar (double): to subtract
        
            Returns:
                new :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`
        
        
        """
        ...
    def subtract(self, trigonometricPolynomialFunction: 'TrigonometricPolynomialFunction') -> 'TrigonometricPolynomialFunction':
        """
            Subtract a polynomial to the current polynomial :
        
            Parameters:
                polynomial (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`): to perform subtraction
        
            Returns:
                :code:`this - polynomial`
        
        
        """
        ...
    def toString(self) -> str:
        """
            Get String representation of polynomial
        
            Overrides:
                 in class 
        
            Returns:
                string
        
        
        """
        ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Return value at x of polynomial
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): desired abscissa
        
            Returns:
                value of polynomial function
        
            Return value at x of n :sup:`th` order derivative
        
            Parameters:
                n (int): order of derivative
                x (double): desired abscissa
        
            Returns:
                value of derivative
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
        
        """
        ...
    @typing.overload
    def value(self, int: int, double: float) -> float: ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class TrigonometricPolynomialPrimitive(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public final class TrigonometricPolynomialPrimitive extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        This class represents a trigonometric polynomial primitive. Such a function is defined as being the sum of a {link
        TrigonometricPolynomialFunction} and a :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction` :
        :code:`P(x) = a0 + a1 x + sum( bk cos(kt) + ck sin(kt) )`
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, polynomialFunction: 'PolynomialFunction', trigonometricPolynomialFunction: TrigonometricPolynomialFunction): ...
    @typing.overload
    def add(self, polynomialFunction: 'PolynomialFunction') -> 'TrigonometricPolynomialPrimitive':
        """
            Add two :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
            Parameters:
                poly (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`): to add
        
            Returns:
                resulting :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
            Add a :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction`
        
            Parameters:
                poly (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction`): to add
        
            Returns:
                resulting :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
            Add a :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`
        
            Parameters:
                poly (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`): to add
        
            Returns:
                resulting :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
        
        """
        ...
    @typing.overload
    def add(self, trigonometricPolynomialFunction: TrigonometricPolynomialFunction) -> 'TrigonometricPolynomialPrimitive': ...
    @typing.overload
    def add(self, trigonometricPolynomialPrimitive: 'TrigonometricPolynomialPrimitive') -> 'TrigonometricPolynomialPrimitive': ...
    @typing.overload
    def derivative(self) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction:
        """
            Get first order derivative
        
            Returns:
                derivative as a :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
        """
        ...
    @typing.overload
    def derivative(self, int: int) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction:
        """
            Get n :sup:`th` order derivative
        
            Parameters:
                n (int): order of derivative
        
            Returns:
                derivative as a :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
        
        """
        ...
    def getLinearPolynomial(self) -> 'PolynomialFunction':
        """
            Get the Linear Polynomial Part
        
            Returns:
                the polynomial as a :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction`
        
        
        """
        ...
    def getTrigonometricPolynomial(self) -> TrigonometricPolynomialFunction:
        """
            Get the Trigonometric Polynomial Part
        
            Returns:
                the polynomial as a :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`
        
        
        """
        ...
    def negate(self) -> 'TrigonometricPolynomialPrimitive':
        """
            Get opposite of current polynomial
        
            Returns:
                opposite
        
        
        """
        ...
    @typing.overload
    def polynomialDerivative(self) -> 'TrigonometricPolynomialPrimitive':
        """
            Get first order derivative
        
            Returns:
                derivative as an :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
        """
        ...
    @typing.overload
    def polynomialDerivative(self, int: int) -> 'TrigonometricPolynomialPrimitive':
        """
            Get n :sup:`th` order derivative
        
            Parameters:
                n (int): order of derivative (n > 0)
        
            Returns:
                n :sup:`th` order polynomial derivative as a
                :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`
        
        
        """
        ...
    def scalarAdd(self, double: float) -> 'TrigonometricPolynomialPrimitive':
        """
            Add a scalar to a :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
            Parameters:
                scalar (double): for addition
        
            Returns:
                resulting :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
        
        """
        ...
    def scalarDivide(self, double: float) -> 'TrigonometricPolynomialPrimitive':
        """
            Divide by a scalar
        
            Parameters:
                scalar (double): to divide polynomial by
        
            Returns:
                polynomial divide by scalar
        
        
        """
        ...
    def scalarMultiply(self, double: float) -> 'TrigonometricPolynomialPrimitive':
        """
            Multiply :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive` by a scalar
        
            Parameters:
                scalar (double): for multiplication
        
            Returns:
                resulting :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
        
        """
        ...
    def scalarSubtract(self, double: float) -> 'TrigonometricPolynomialPrimitive':
        """
            Subtract a scalar
        
            Parameters:
                scalar (double): to subtract
        
            Returns:
                new :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`
        
        
        """
        ...
    @typing.overload
    def subtract(self, polynomialFunction: 'PolynomialFunction') -> 'TrigonometricPolynomialPrimitive':
        """
            Subtract two :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
            Parameters:
                poly (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`): to Subtract
        
            Returns:
                resulting :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
            Subtract a :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction`
        
            Parameters:
                poly (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction`): to Subtract
        
            Returns:
                resulting :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
            Subtract a :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`
        
            Parameters:
                poly (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialFunction`): to Subtract
        
            Returns:
                resulting :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.TrigonometricPolynomialPrimitive`
        
        
        """
        ...
    @typing.overload
    def subtract(self, trigonometricPolynomialFunction: TrigonometricPolynomialFunction) -> 'TrigonometricPolynomialPrimitive': ...
    @typing.overload
    def subtract(self, trigonometricPolynomialPrimitive: 'TrigonometricPolynomialPrimitive') -> 'TrigonometricPolynomialPrimitive': ...
    def toString(self) -> str:
        """
            Get String representation of polynomial
        
            Overrides:
                 in class 
        
            Returns:
                string
        
        
        """
        ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Get value at given abscissa
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): abscissa
        
            Returns:
                value a given abscissa
        
            Get value of derivative
        
            Parameters:
                n (int): order of derivative
                x (double): abscissa
        
            Returns:
                value of derivative at abscissa
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
        
        """
        ...
    @typing.overload
    def value(self, int: int, double: float) -> float: ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class UnivariateDateFunction(java.io.Serializable):
    """
    public interface UnivariateDateFunction extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This handles univariate functions. It is the space mechanics counter part of
        :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`.
    
        Since:
            3.0
    """
    def value(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Returns value of function at provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                value of function at provided date
        
        
        """
        ...

class ZernikePolynomial(fr.cnes.sirius.patrius.math.parameter.IParameterizable):
    """
    public class ZernikePolynomial extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
    
        Class representing a Zernike polynomial.
    
        Since:
            4.13
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, parameterArray: typing.Union[typing.List[typing.MutableSequence[fr.cnes.sirius.patrius.math.parameter.Parameter]], jpype.JArray]): ...
    @staticmethod
    def arrayIndexToAzimuthalDegree(int: int, int2: int) -> int:
        """
            Utility function to convert an array index of the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.ZernikePolynomial.computeZernikeMonomials` to an azimuthal
            degree.
        
            Parameters:
                radialDegree (int): The radial degree
                arrayIndex (int): The array index
        
            Returns:
                the azimuthal degree
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NotPositiveException`: if :code:`radialDegree < 0`
        
        
        if :code:`arrayIndex < 0`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if :code:`arrayIndex > radialDegree + 1`
        
        
        """
        ...
    @staticmethod
    def azimuthalDegreeToArrayIndex(int: int, int2: int) -> int:
        """
            Utility function to convert an azimuthal degree to the array index of the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.ZernikePolynomial.computeZernikeMonomials`.
        
            Parameters:
                radialDegree (int): The radial degree
                azimuthalDegree (int): The azimuthal degree
        
            Returns:
                the array index of :code:`zernikeMonomials[radialDegree]` corresponding to the azimuthalDegree
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NotPositiveException`: if :code:`radialDegree < 0`
                : if the azimuthal degree is greater in absolute value to the radial degree if the difference of the two degrees is not an
                    even number
        
        
        """
        ...
    def computeDerivatives(self, double: float, double2: float, collection: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.math.parameter.Parameter], typing.Sequence[fr.cnes.sirius.patrius.math.parameter.Parameter], typing.Set[fr.cnes.sirius.patrius.math.parameter.Parameter]]) -> typing.MutableSequence[float]: ...
    @staticmethod
    def computeRadialZernikeMonomials(int: int, double: float) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Compute the radial zernike monomials.
        
            The radial zernike monomials are 0 when radialDegree-azimuthalDegree is odd. The returned array does not contain these
            values.
        
        
            The row n corresponds to the radial degree n, while each column j corresponds to the azimuthal degree n%2+2j:
        
              - For even radial degrees 2n: R_(2n)^0, R_(2n)^2, R_(2n)^4, etc...
              - For odd radial degrees 2n+1: R_(2n+1)^1, R_(2n+1)^3, R_(2n+1)^5, etc...
        
        
            Parameters:
                radialDegree (int): The radial degree
                rho (double): The distance variable
        
            Returns:
                the radial zernike monomials
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NotPositiveException`: if :code:`radialDegree < 0`
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if rho is outside [0, 1]
        
        
        """
        ...
    def computeValue(self, double: float, double2: float) -> float:
        """
            Compute the value of this zernike polynomial.
        
            Parameters:
                rho (double): The distance variable
                azimuth (double): The angular variable [rad]
        
            Returns:
                The polynomial value
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if rho is outside [0, 1]
        
        
        """
        ...
    def computeValueAndDerivatives(self, double: float, double2: float, collection: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.math.parameter.Parameter], typing.Sequence[fr.cnes.sirius.patrius.math.parameter.Parameter], typing.Set[fr.cnes.sirius.patrius.math.parameter.Parameter]]) -> fr.cnes.sirius.patrius.math.util.Pair[float, typing.MutableSequence[float]]: ...
    @staticmethod
    def computeZernikeMonomials(int: int, double: float, double2: float) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Compute the zernike monomials.
        
            The monomials are stored in a 2D array. The row i corresponds to the radial degree i and contains an array of size i+1,
            containing the different azimuthal degrees. Use
            :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.ZernikePolynomial.azimuthalDegreeToArrayIndex` and
            :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.ZernikePolynomial.arrayIndexToAzimuthalDegree` to switch
            between azimuthal degrees and array index.
        
            Parameters:
                radialDegree (int): The radial degree
                rho (double): The distance variable
                azimuth (double): The angular variable [rad]
        
            Returns:
                the zernike monomials
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NotPositiveException`: if :code:`radialDegree < 0`
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if rho is outside [0, 1]
        
        
        """
        ...
    def getCoefficient(self, int: int, int2: int) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Getter for the required coefficient of the zernike polynomial.
        
            Parameters:
                radialDegreeIn (int): The coefficient radial degree
                azimuthalDegree (int): the coefficient azimuthal degree
        
            Returns:
                the coefficient parameter
        
        
        """
        ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def supportsParameter(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Check if a parameter is supported.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable.supportsParameter` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
        
            Parameters:
                param (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to check
        
            Returns:
                true if the parameter is supported
        
        
        """
        ...

class DatePolynomialFunctionInterface(UnivariateDateFunction):
    """
    public interface DatePolynomialFunctionInterface extends :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction`
    
        Represents an interface for polynomial functions of date.
    
        Since:
            4.11
    """
    def copy(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'DatePolynomialFunctionInterface':
        """
            Build a new date polynomial function whose value over time is the same as this (same degree), only the origin date is
            different what may modify the time factor and/or the polynomial coefficients (pending the polynomial type).
        
            Parameters:
                newOriginDate (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The new origin date
        
            Returns:
                a new date polynomial function
        
        
        """
        ...
    def dateToDouble(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Getter for the time as double corresponding to the given :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the given :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`
        
            Returns:
                the corresponding time as double
        
        
        """
        ...
    def derivative(self) -> 'DatePolynomialFunctionInterface':
        """
            Getter for the derivative date polynomial function.
        
            Returns:
                the derivative date polynomial function
        
        
        """
        ...
    def doubleToDate(self, double: float) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` corresponding to the given time as double.
        
            Parameters:
                time (double): the given time as double with respect to time origin
        
            Returns:
                the corresponding :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`
        
        
        """
        ...
    def getCoefficients(self) -> typing.MutableSequence[float]:
        """
            Getter for the polynomial coefficients.
        
            Returns:
                the polynomial coefficients
        
        
        """
        ...
    def getDegree(self) -> int:
        """
            Getter for the polynomial degree.
        
            Returns:
                the polynomial degree
        
        
        """
        ...
    def getPolynomialType(self) -> PolynomialType:
        """
            Getter for the type of this polynomial function.
        
            Returns:
                the type of this polynomial function
        
        
        """
        ...
    def getT0(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the origin date.
        
            Returns:
                the origin date
        
        
        """
        ...
    def getTimeFactor(self) -> float:
        """
            Getter for the time factor.
        
            Returns:
                the time factor (a :code:`null` value corresponds to a unit time factor)
        
        
        """
        ...
    def primitive(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> 'DatePolynomialFunctionInterface':
        """
            Getter for the primitive date polynomial function at the given date and for the given function value at abscissa0.
        
            Parameters:
                date0 (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the date of interest
                ordinate0 (double): the function value at abscissa0
        
            Returns:
                the primitive date polynomial function at the given date and for the given function value at abscissa0
        
        
        """
        ...

class PolynomialChebyshevFunction(fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction, PolynomialFunctionInterface):
    def __init__(self, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    def add(self, polynomialChebyshevFunction: 'PolynomialChebyshevFunction') -> 'PolynomialChebyshevFunction': ...
    def derivative(self) -> 'PolynomialChebyshevFunction': ...
    def equals(self, object: typing.Any) -> bool: ...
    def getChebyshevAbscissas(self, int: int) -> typing.MutableSequence[float]: ...
    def getCoefficients(self) -> typing.MutableSequence[float]: ...
    def getDegree(self) -> int: ...
    def getEnd(self) -> float: ...
    def getPolynomialType(self) -> PolynomialType: ...
    def getStart(self) -> float: ...
    def gradient(self, double: float, *double2: float) -> typing.MutableSequence[float]: ...
    def hashCode(self) -> int: ...
    def negate(self) -> 'PolynomialChebyshevFunction': ...
    def primitive(self, double: float, double2: float) -> 'PolynomialChebyshevFunction': ...
    def subtract(self, polynomialChebyshevFunction: 'PolynomialChebyshevFunction') -> 'PolynomialChebyshevFunction': ...
    def toString(self) -> str: ...
    def univariateDerivative(self) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction: ...
    @typing.overload
    def value(self, double: float) -> float: ...
    @typing.overload
    def value(self, double: float, *double2: float) -> float: ...

class PolynomialFunction(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction, PolynomialFunctionInterface):
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    def add(self, polynomialFunction: 'PolynomialFunction') -> 'PolynomialFunction': ...
    def derivative(self) -> 'PolynomialFunction': ...
    def equals(self, object: typing.Any) -> bool: ...
    def getCoefficients(self) -> typing.MutableSequence[float]: ...
    def getDegree(self) -> int: ...
    def getPolynomialType(self) -> PolynomialType: ...
    def hashCode(self) -> int: ...
    def multiply(self, polynomialFunction: 'PolynomialFunction') -> 'PolynomialFunction': ...
    def negate(self) -> 'PolynomialFunction': ...
    def primitive(self, double: float, double2: float) -> 'PolynomialFunction': ...
    def subtract(self, polynomialFunction: 'PolynomialFunction') -> 'PolynomialFunction': ...
    def toString(self) -> str: ...
    def univariateDerivative(self) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction: ...
    @typing.overload
    def value(self, double: float) -> float: ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...
    class Parametric(fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction):
        def __init__(self): ...
        def gradient(self, double: float, *double2: float) -> typing.MutableSequence[float]: ...
        def value(self, double: float, *double2: float) -> float: ...

class DatePolynomialChebyshevFunction(DatePolynomialFunctionInterface):
    """
    public class DatePolynomialChebyshevFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
    
        This class represents a Chebyshev polynomial function of date.
    
        The real time (unreduced time) is used.
    
        Since:
            4.10
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, polynomialChebyshevFunction: PolynomialChebyshevFunction): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate3: fr.cnes.sirius.patrius.time.AbsoluteDate, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def copy(self) -> 'DatePolynomialChebyshevFunction':
        """
            Copies this function and returns a new one identical to this.
        
            Returns:
                new DatePolynomialChebyshevFunction identical to this
        
        """
        ...
    @typing.overload
    def copy(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'DatePolynomialChebyshevFunction':
        """
            Build a new date polynomial function whose value over time is the same as this (same degree), only the origin date is
            different what may modify the time factor and/or the polynomial coefficients (pending the polynomial type).
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Parameters:
                newOriginDate (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The new origin date
        
            Returns:
                a new date polynomial function
        
        
        """
        ...
    def dateToDouble(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Getter for the time as double corresponding to the given :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.dateToDouble` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the given :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`
        
            Returns:
                the corresponding time as double
        
        
        """
        ...
    def derivative(self) -> 'DatePolynomialChebyshevFunction':
        """
            Getter for the derivative date polynomial function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.derivative` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the derivative date polynomial function
        
        
        """
        ...
    def doubleToDate(self, double: float) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` corresponding to the given time as double.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.doubleToDate` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Parameters:
                time (double): the given time as double with respect to time origin
        
            Returns:
                the corresponding :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`
        
        
        """
        ...
    def getChebyshevAbscissas(self, int: int) -> typing.MutableSequence[fr.cnes.sirius.patrius.time.AbsoluteDate]:
        """
            Compute the N Chebyshev abscissas on the range [start ; end] in a chronological (increasing) order.
        
            Parameters:
                n (int): Number of points to evaluate
        
            Returns:
                the N Chebyshev abscissas
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NotStrictlyPositiveException`: if :code:`n <= 0`
        
        
        """
        ...
    def getCoefficients(self) -> typing.MutableSequence[float]:
        """
            Getter for the polynomial coefficients.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.getCoefficients` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the polynomial coefficients
        
        
        """
        ...
    def getDegree(self) -> int:
        """
            Getter for the polynomial degree.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.getDegree` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the polynomial degree
        
        
        """
        ...
    def getEnd(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the Chebyshev polynomial range end date.
        
            Returns:
                the Chebyshev polynomial range end date
        
        
        """
        ...
    def getEndAsDouble(self) -> float:
        """
            Getter for the end range of the underlying polynomial Chebyshev function.
        
            Returns:
                the end range of the underlying polynomial Chebyshev function
        
        
        """
        ...
    def getOrder(self) -> int:
        """
            Getter for polynomial order.
        
            Returns:
                the polynomial order
        
        
        """
        ...
    def getPolynomialType(self) -> PolynomialType:
        """
            Getter for the type of this polynomial function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.getPolynomialType` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the type of this polynomial function
        
        
        """
        ...
    def getRange(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Getter for the Chebyshev polynomial range.
        
            Returns:
                the Chebyshev polynomial range
        
        
        """
        ...
    def getStart(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the Chebyshev polynomial range start date.
        
            Returns:
                the Chebyshev polynomial range start date
        
        
        """
        ...
    def getStartAsDouble(self) -> float:
        """
            Getter for the start range of the underlying polynomial Chebyshev function.
        
            Returns:
                the start range of the underlying polynomial Chebyshev function
        
        
        """
        ...
    def getT0(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the Chebyshev polynomial origin date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.getT0` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the Chebyshev polynomial origin date
        
        
        """
        ...
    def getTimeFactor(self) -> float:
        """
            Getter for the time factor.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.getTimeFactor` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the time factor (a :code:`null` value corresponds to a unit time factor)
        
        
        """
        ...
    def primitive(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> 'DatePolynomialChebyshevFunction':
        """
            Getter for the primitive date polynomial function at the given date and for the given function value at abscissa0.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.primitive` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Parameters:
                date0 (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the date of interest
                value0 (double): the function value at abscissa0
        
            Returns:
                the primitive date polynomial function at the given date and for the given function value at abscissa0
        
        
        """
        ...
    def value(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Returns value of function at provided date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                value of function at provided date
        
        
        """
        ...

class DatePolynomialFunction(DatePolynomialFunctionInterface):
    """
    public class DatePolynomialFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
    
        This class represents a polynomial function of date.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, polynomialFunction: PolynomialFunction): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, polynomialFunction: PolynomialFunction): ...
    def copy(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'DatePolynomialFunction':
        """
            Build a new date polynomial function whose value over time is the same as this (same degree), only the origin date is
            different what may modify the time factor and/or the polynomial coefficients (pending the polynomial type).
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Parameters:
                newOriginDate (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The new origin date
        
            Returns:
                a new date polynomial function
        
            Raises:
                : if the time factor is enabled and the new origin date is not strictly anterior to the current origin date shifted by the
                    timeFactor
        
        
        """
        ...
    def derivative(self) -> 'DatePolynomialFunction':
        """
            Getter for the derivative date polynomial function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.derivative` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the derivative date polynomial function
        
        
        """
        ...
    def getCoefficients(self) -> typing.MutableSequence[float]:
        """
            Getter for the polynomial coefficients.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.getCoefficients` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the polynomial coefficients
        
        
        """
        ...
    def getDegree(self) -> int:
        """
            Getter for the polynomial degree.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.getDegree` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the polynomial degree
        
        
        """
        ...
    def getPolynomialType(self) -> PolynomialType:
        """
            Getter for the type of this polynomial function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.getPolynomialType` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the type of this polynomial function
        
        
        """
        ...
    def getT0(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Returns the model origin date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.getT0` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the model origin date
        
        
        """
        ...
    def getTimeFactor(self) -> float:
        """
            Getter for the time factor.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.getTimeFactor` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Returns:
                the time factor (a :code:`null` value corresponds to a unit time factor)
        
        
        """
        ...
    def primitive(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> 'DatePolynomialFunction':
        """
            Getter for the primitive date polynomial function at the given date and for the given function value at abscissa0.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface.primitive` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface`
        
            Parameters:
                date0 (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the date of interest
                value0 (double): the function value at abscissa0
        
            Returns:
                the primitive date polynomial function at the given date and for the given function value at abscissa0
        
        
        """
        ...
    def value(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Returns value of function at provided date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                value of function at provided date
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.analysis.polynomials")``.

    ChebyshevDecompositionEngine: typing.Type[ChebyshevDecompositionEngine]
    DatePolynomialChebyshevFunction: typing.Type[DatePolynomialChebyshevFunction]
    DatePolynomialFunction: typing.Type[DatePolynomialFunction]
    DatePolynomialFunctionInterface: typing.Type[DatePolynomialFunctionInterface]
    ElementaryMultiplicationTypes: typing.Type[ElementaryMultiplicationTypes]
    FourierDecompositionEngine: typing.Type[FourierDecompositionEngine]
    FourierSeries: typing.Type[FourierSeries]
    FourierSeriesApproximation: typing.Type[FourierSeriesApproximation]
    HelmholtzPolynomial: typing.Type[HelmholtzPolynomial]
    PolynomialChebyshevFunction: typing.Type[PolynomialChebyshevFunction]
    PolynomialFunction: typing.Type[PolynomialFunction]
    PolynomialFunctionInterface: typing.Type[PolynomialFunctionInterface]
    PolynomialFunctionLagrangeForm: typing.Type[PolynomialFunctionLagrangeForm]
    PolynomialFunctionNewtonForm: typing.Type[PolynomialFunctionNewtonForm]
    PolynomialSplineFunction: typing.Type[PolynomialSplineFunction]
    PolynomialType: typing.Type[PolynomialType]
    PolynomialsUtils: typing.Type[PolynomialsUtils]
    TrigonometricPolynomialFunction: typing.Type[TrigonometricPolynomialFunction]
    TrigonometricPolynomialPrimitive: typing.Type[TrigonometricPolynomialPrimitive]
    UnivariateDateFunction: typing.Type[UnivariateDateFunction]
    ZernikePolynomial: typing.Type[ZernikePolynomial]
