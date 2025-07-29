
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis.differentiation
import fr.cnes.sirius.patrius.math.analysis.function
import fr.cnes.sirius.patrius.math.analysis.integration
import fr.cnes.sirius.patrius.math.analysis.interpolation
import fr.cnes.sirius.patrius.math.analysis.polynomials
import fr.cnes.sirius.patrius.math.analysis.solver
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import java.io
import jpype
import typing



class BivariateFunction(java.io.Serializable):
    """
    public interface BivariateFunction extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        An interface representing a bivariate real function.
    
        Since:
            2.1
    """
    def value(self, double: float, double2: float) -> float:
        """
            Compute the value for the function.
        
            Parameters:
                x (double): Abscissa for which the function value should be computed.
                y (double): Ordinate for which the function value should be computed.
        
            Returns:
                the value.
        
        
        """
        ...

class ErrorEvaluationFunctionUtils:
    """
    public final class ErrorEvaluationFunctionUtils extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        A collection of static methods that evaluate :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction` functions
        errors.
    """
    @typing.overload
    @staticmethod
    def getNormInf(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], univariateFunction: typing.Union['UnivariateFunction', typing.Callable]) -> float:
        """
            Compute the L :sub:`∞` norm (worst value) between the function to evaluate and the approximated function at the
            considered abscissas.
        
            Note: the L :sub:`∞` norm isn't computed (return `null
            <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NaN>`) if the function or the
            approximated function have `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NaN>`
            values.
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Function to evaluate
                approximatedFunction (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Approximated function
                abscissas (double[]): Abscissas to considered
        
            Returns:
                L :sub:`∞` norm
        
            Compute the L :sub:`∞` norm (worst value) between the function to evaluate and the approximated function at the
            considered abscissas.
        
            Note: the L :sub:`∞` norm isn't computed (return `null
            <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NaN>`) if the function or the
            approximated function have `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NaN>`
            values.
        
            Parameters:
                abscissas (double[]): Abscissas to considered
                functionValues (double[]): Function values at the specified abscissas
                approximatedFunction (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Approximated function
        
            Returns:
                L :sub:`∞` norm
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if :code:`abscissas` and :code:`functionValues` do not have the same length
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getNormInf(univariateFunction: typing.Union['UnivariateFunction', typing.Callable], univariateFunction2: typing.Union['UnivariateFunction', typing.Callable], doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def getStandardDeviation(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], univariateFunction: typing.Union['UnivariateFunction', typing.Callable]) -> float:
        """
            Compute the standard deviation σ between the function to evaluate and the approximated function at the considered
            abscissas.
        
            Note: the standard deviation isn't computed (return `null
            <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NaN>`) if the function or the
            approximated function have `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NaN>`
            values.
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Function to evaluate
                approximatedFunction (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Approximated function
                abscissas (double[]): Abscissas to considered
        
            Returns:
                the standard deviation σ
        
            Compute the standard deviation σ between the function to evaluate and the approximated function at the considered
            abscissas.
        
            Note: the standard deviation isn't computed (return `null
            <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NaN>`) if the function or the
            approximated function have `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NaN>`
            values.
        
            Parameters:
                abscissas (double[]): Abscissas to considered
                functionValues (double[]): Function values at the specified abscissas
                approximatedFunction (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Approximated function
        
            Returns:
                the standard deviation σ
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if :code:`abscissas` and :code:`functionValues` do not have the same length
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getStandardDeviation(univariateFunction: typing.Union['UnivariateFunction', typing.Callable], univariateFunction2: typing.Union['UnivariateFunction', typing.Callable], doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...

class FunctionUtils:
    @typing.overload
    @staticmethod
    def add(*univariateFunction: typing.Union['UnivariateFunction', typing.Callable]) -> 'UnivariateFunction': ...
    @typing.overload
    @staticmethod
    def add(*univariateDifferentiableFunction: fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction) -> fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction: ...
    @typing.overload
    @staticmethod
    def collector(bivariateFunction: typing.Union[BivariateFunction, typing.Callable], double: float) -> 'MultivariateFunction': ...
    @typing.overload
    @staticmethod
    def collector(bivariateFunction: typing.Union[BivariateFunction, typing.Callable], univariateFunction: typing.Union['UnivariateFunction', typing.Callable], double: float) -> 'MultivariateFunction': ...
    @staticmethod
    def combine(bivariateFunction: typing.Union[BivariateFunction, typing.Callable], univariateFunction: typing.Union['UnivariateFunction', typing.Callable], univariateFunction2: typing.Union['UnivariateFunction', typing.Callable]) -> 'UnivariateFunction': ...
    @typing.overload
    @staticmethod
    def compose(*univariateFunction: typing.Union['UnivariateFunction', typing.Callable]) -> 'UnivariateFunction': ...
    @typing.overload
    @staticmethod
    def compose(*univariateDifferentiableFunction: fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction) -> fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction: ...
    @staticmethod
    def fix1stArgument(bivariateFunction: typing.Union[BivariateFunction, typing.Callable], double: float) -> 'UnivariateFunction': ...
    @staticmethod
    def fix2ndArgument(bivariateFunction: typing.Union[BivariateFunction, typing.Callable], double: float) -> 'UnivariateFunction': ...
    @typing.overload
    @staticmethod
    def multiply(*univariateFunction: typing.Union['UnivariateFunction', typing.Callable]) -> 'UnivariateFunction': ...
    @typing.overload
    @staticmethod
    def multiply(*univariateDifferentiableFunction: fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction) -> fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction: ...
    @staticmethod
    def sample(univariateFunction: typing.Union['UnivariateFunction', typing.Callable], double: float, double2: float, int: int) -> typing.MutableSequence[float]: ...

_IDependentVariable__T = typing.TypeVar('_IDependentVariable__T')  # <T>
class IDependentVariable(java.io.Serializable, typing.Generic[_IDependentVariable__T]):
    """
    public interface IDependentVariable<T> extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        Generic interface to describe a T-dependent variable.
        The generic parameter T represents the nature of the independent variable.
    
        Since:
            1.2
    """
    def value(self, t: _IDependentVariable__T) -> float:
        """
            Compute the value of the T-dependent variable.
        
            Parameters:
                x (:class:`~fr.cnes.sirius.patrius.math.analysis.IDependentVariable`): value of T for which the variable should be computed.
        
            Returns:
                the value of the dependent variable.
        
        
        """
        ...

_IDependentVectorVariable__T = typing.TypeVar('_IDependentVectorVariable__T')  # <T>
class IDependentVectorVariable(java.io.Serializable, typing.Generic[_IDependentVectorVariable__T]):
    """
    public interface IDependentVectorVariable<T> extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        Generic interface to describe a T-dependent 3D vector.
        The generic parameter T represents the nature of the independent variable.
    
        Since:
            1.2
    """
    def value(self, t: _IDependentVectorVariable__T) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Compute the value of the T-dependent 3D vector.
        
            Parameters:
                x (:class:`~fr.cnes.sirius.patrius.math.analysis.IDependentVectorVariable`): value of T for which the variable should be computed.
        
            Returns:
                the value of the dependent vector.
        
        
        """
        ...

class MultivariateFunction:
    """
    public interface MultivariateFunction
    
        An interface representing a multivariate real function.
    
        Since:
            2.0
    """
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Compute the value for the function at the given point.
        
            Parameters:
                point (double[]): Point at which the function must be evaluated.
        
            Returns:
                the function value for the given point.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the parameter's dimension is wrong for the function being evaluated.
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: when the activated method itself can ascertain that preconditions, specified in the API expressed at the level of the
                    activated method, have been violated. In the vast majority of cases where Commons Math throws this exception, it is the
                    result of argument checking of actual parameters immediately passed to a method.
        
        
        """
        ...

class MultivariateMatrixFunction:
    """
    public interface MultivariateMatrixFunction
    
        An interface representing a multivariate matrix function.
    
        Since:
            2.0
    """
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Compute the value for the function at the given point.
        
            Parameters:
                point (double[]): point at which the function must be evaluated
        
            Returns:
                function value for the given point
        
            Raises:
                : if points dimension is wrong
        
        
        """
        ...

class MultivariateVectorFunction:
    """
    public interface MultivariateVectorFunction
    
        An interface representing a multivariate vectorial function.
    
        Since:
            2.0
    """
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Compute the value for the function at the given point.
        
            Parameters:
                point (double[]): point at which the function must be evaluated
        
            Returns:
                function value for the given point
        
            Raises:
                : if points dimension is wrong
        
        
        """
        ...

class ParametricUnivariateFunction:
    """
    public interface ParametricUnivariateFunction
    
        An interface representing a real function that depends on one independent variable plus some extra parameters.
    
        Since:
            3.0
    """
    def gradient(self, double: float, *double2: float) -> typing.MutableSequence[float]:
        """
            Compute the gradient of the function with respect to its parameters.
        
            Parameters:
                x (double): Point for which the function value should be computed.
                parameters (double...): Function parameters.
        
            Returns:
                the value.
        
        
        """
        ...
    def value(self, double: float, *double2: float) -> float:
        """
            Compute the value of the function.
        
            Parameters:
                x (double): Point for which the function value should be computed.
                parameters (double...): Function parameters.
        
            Returns:
                the value.
        
        
        """
        ...

class TrivariateFunction(java.io.Serializable):
    """
    public interface TrivariateFunction extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        An interface representing a trivariate real function.
    
        Since:
            2.2
    """
    def value(self, double: float, double2: float, double3: float) -> float:
        """
            Compute the value for the function.
        
            Parameters:
                x (double): x-coordinate for which the function value should be computed.
                y (double): y-coordinate for which the function value should be computed.
                z (double): z-coordinate for which the function value should be computed.
        
            Returns:
                the value.
        
        
        """
        ...

class UnivariateFunction(java.io.Serializable):
    def value(self, double: float) -> float: ...

class UnivariateMatrixFunction:
    """
    public interface UnivariateMatrixFunction
    
        An interface representing a univariate matrix function.
    
        Since:
            2.0
    """
    def value(self, double: float) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Compute the value for the function.
        
            Parameters:
                x (double): the point for which the function value should be computed
        
            Returns:
                the value
        
        
        """
        ...

class UnivariateVectorFunction:
    """
    public interface UnivariateVectorFunction
    
        An interface representing a univariate vectorial function.
    
        Since:
            2.0
    """
    def getSize(self) -> int:
        """
            Compute the size of the list of values of the function as created by the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction.value` method
        
            Returns:
                the size of the values array
        
        
        """
        ...
    def value(self, double: float) -> typing.MutableSequence[float]:
        """
            Compute the value for the function.
        
            Parameters:
                x (double): the point for which the function value should be computed
        
            Returns:
                the value
        
        
        """
        ...

class IntegrableUnivariateFunction(UnivariateFunction):
    """
    public interface IntegrableUnivariateFunction extends :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
    
        Extension of :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction` representing an integrable univariate
        real function.
    
        Since:
            1.1
    """
    def primitive(self) -> UnivariateFunction:
        """
            Returns the primitive of the function
        
            Returns:
                the primitive function
        
        
        """
        ...

class DifferentiableIntegrableUnivariateFunction(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction, IntegrableUnivariateFunction):
    """
    public interface DifferentiableIntegrableUnivariateFunction extends :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`, :class:`~fr.cnes.sirius.patrius.math.analysis.IntegrableUnivariateFunction`
    
        Extension of :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction` representing a differentiable and
        integrable univariate real function.
    
        Since:
            1.2
    """
    ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.analysis")``.

    BivariateFunction: typing.Type[BivariateFunction]
    DifferentiableIntegrableUnivariateFunction: typing.Type[DifferentiableIntegrableUnivariateFunction]
    ErrorEvaluationFunctionUtils: typing.Type[ErrorEvaluationFunctionUtils]
    FunctionUtils: typing.Type[FunctionUtils]
    IDependentVariable: typing.Type[IDependentVariable]
    IDependentVectorVariable: typing.Type[IDependentVectorVariable]
    IntegrableUnivariateFunction: typing.Type[IntegrableUnivariateFunction]
    MultivariateFunction: typing.Type[MultivariateFunction]
    MultivariateMatrixFunction: typing.Type[MultivariateMatrixFunction]
    MultivariateVectorFunction: typing.Type[MultivariateVectorFunction]
    ParametricUnivariateFunction: typing.Type[ParametricUnivariateFunction]
    TrivariateFunction: typing.Type[TrivariateFunction]
    UnivariateFunction: typing.Type[UnivariateFunction]
    UnivariateMatrixFunction: typing.Type[UnivariateMatrixFunction]
    UnivariateVectorFunction: typing.Type[UnivariateVectorFunction]
    differentiation: fr.cnes.sirius.patrius.math.analysis.differentiation.__module_protocol__
    function: fr.cnes.sirius.patrius.math.analysis.function.__module_protocol__
    integration: fr.cnes.sirius.patrius.math.analysis.integration.__module_protocol__
    interpolation: fr.cnes.sirius.patrius.math.analysis.interpolation.__module_protocol__
    polynomials: fr.cnes.sirius.patrius.math.analysis.polynomials.__module_protocol__
    solver: fr.cnes.sirius.patrius.math.analysis.solver.__module_protocol__
