
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math
import fr.cnes.sirius.patrius.math.analysis
import java.io
import jpype
import typing



class DSCompiler:
    """
    public final class DSCompiler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class holding "compiled" computation rules for derivative structures.
    
        This class implements the computation rules described in Dan Kalman's paper `Doubly Recursive Multivariate Automatic
        Differentiation <http://www.math.american.edu/People/kalman/pdffiles/mmgautodiff.pdf>`, Mathematics Magazine, vol. 75,
        no. 3, June 2002. However, in order to avoid performances bottlenecks, the recursive rules are "compiled" once in an
        unfold form. This class does this recursion unrolling and stores the computation rules as simple loops with pre-computed
        indirection arrays.
    
        This class maps all derivative computation into single dimension arrays that hold the value and partial derivatives. The
        class does not hold these arrays, which remains under the responsibility of the caller. For each combination of number
        of free parameters and derivation order, only one compiler is necessary, and this compiler will be used to perform
        computations on all arrays provided to it, which can represent hundreds or thousands of different parameters kept
        together with all theur partial derivatives.
    
        The arrays on which compilers operate contain only the partial derivatives together with the 0 :sup:`th` derivative,
        i.e. the value. The partial derivatives are stored in a compiler-specific order, which can be retrieved using methods
        :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DSCompiler.getPartialDerivativeIndex` and
        :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DSCompiler.getPartialDerivativeOrders`. The value is
        guaranteed to be stored as the first element (i.e. the
        :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DSCompiler.getPartialDerivativeIndex` method returns 0 when
        called with 0 for all derivation orders and
        :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DSCompiler.getPartialDerivativeOrders` returns an array
        filled with 0 when called with 0 as the index).
    
        Note that the ordering changes with number of parameters and derivation order. For example given 2 parameters x and y,
        df/dy is stored at index 2 when derivation order is set to 1 (in this case the array has three elements: f, df/dx and
        df/dy). If derivation order is set to 2, then df/dy will be stored at index 3 (in this case the array has six elements:
        f, df/dx, df/dxdx, df/dy, df/dxdy and df/dydy).
    
        Given this structure, users can perform some simple operations like adding, subtracting or multiplying constants and
        negating the elements by themselves, knowing if they want to mutate their array or create a new array. These simple
        operations are not provided by the compiler. The compiler provides only the more complex operations between several
        arrays.
    
        This class is mainly used as the engine for scalar variable
        :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`. It can also be used directly to hold
        several variables in arrays for more complex data structures. User can for example store a vector of n variables
        depending on three x, y and z free parameters in one array as follows:
    
        .. code-block: java
        
        
           // parameter 0 is x, parameter 1 is y, parameter 2 is z
           int parameters = 3;
           DSCompiler compiler = DSCompiler.getCompiler(parameters, order);
           int size = compiler.getSize();
         
           // pack all elements in a single array
           double[] array = new double[n * size];
           for (int i = 0; i
    """
    def acos(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def acosh(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def add(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int, doubleArray3: typing.Union[typing.List[float], jpype.JArray], int3: int) -> None: ...
    def asin(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def asinh(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def atan(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def atan2(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int, doubleArray3: typing.Union[typing.List[float], jpype.JArray], int3: int) -> None: ...
    def atanh(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def checkCompatibility(self, dSCompiler: 'DSCompiler') -> None: ...
    def compose(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def cos(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def cosh(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def divide(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int, doubleArray3: typing.Union[typing.List[float], jpype.JArray], int3: int) -> None: ...
    def exp(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def expm1(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    @staticmethod
    def getCompiler(int: int, int2: int) -> 'DSCompiler': ...
    def getFreeParameters(self) -> int: ...
    def getOrder(self) -> int: ...
    def getPartialDerivativeIndex(self, *int: int) -> int: ...
    def getPartialDerivativeOrders(self, int: int) -> typing.MutableSequence[int]: ...
    def getSize(self) -> int: ...
    @typing.overload
    def linearCombination(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int, double5: float, doubleArray3: typing.Union[typing.List[float], jpype.JArray], int3: int, double7: float, doubleArray4: typing.Union[typing.List[float], jpype.JArray], int4: int, doubleArray5: typing.Union[typing.List[float], jpype.JArray], int5: int) -> None: ...
    @typing.overload
    def linearCombination(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int, double5: float, doubleArray3: typing.Union[typing.List[float], jpype.JArray], int3: int, doubleArray4: typing.Union[typing.List[float], jpype.JArray], int4: int) -> None: ...
    @typing.overload
    def linearCombination(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int, doubleArray3: typing.Union[typing.List[float], jpype.JArray], int3: int) -> None: ...
    def log(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def log10(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def log1p(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def multiply(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int, doubleArray3: typing.Union[typing.List[float], jpype.JArray], int3: int) -> None: ...
    @typing.overload
    def pow(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    @typing.overload
    def pow(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, double2: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    @typing.overload
    def pow(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int, doubleArray3: typing.Union[typing.List[float], jpype.JArray], int3: int) -> None: ...
    @typing.overload
    def pow(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int3: int) -> None: ...
    def remainder(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int, doubleArray3: typing.Union[typing.List[float], jpype.JArray], int3: int) -> None: ...
    def rootN(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int3: int) -> None: ...
    def sin(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def sinh(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def subtract(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int, doubleArray3: typing.Union[typing.List[float], jpype.JArray], int3: int) -> None: ...
    def tan(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def tanh(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], int2: int) -> None: ...
    def taylor(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, *double2: float) -> float: ...

class DerivativeStructure(fr.cnes.sirius.patrius.math.RealFieldElement['DerivativeStructure'], java.io.Serializable):
    @typing.overload
    def __init__(self, double: float, derivativeStructure: 'DerivativeStructure', double2: float, derivativeStructure2: 'DerivativeStructure'): ...
    @typing.overload
    def __init__(self, double: float, derivativeStructure: 'DerivativeStructure', double2: float, derivativeStructure2: 'DerivativeStructure', double3: float, derivativeStructure3: 'DerivativeStructure'): ...
    @typing.overload
    def __init__(self, double: float, derivativeStructure: 'DerivativeStructure', double2: float, derivativeStructure2: 'DerivativeStructure', double3: float, derivativeStructure3: 'DerivativeStructure', double4: float, derivativeStructure4: 'DerivativeStructure'): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int, double: float): ...
    @typing.overload
    def __init__(self, int: int, int2: int, *double: float): ...
    @typing.overload
    def __init__(self, int: int, int2: int, int3: int, double: float): ...
    def abs(self) -> 'DerivativeStructure': ...
    def acos(self) -> 'DerivativeStructure': ...
    def acosh(self) -> 'DerivativeStructure': ...
    @typing.overload
    def add(self, double: float) -> 'DerivativeStructure': ...
    @typing.overload
    def add(self, derivativeStructure: 'DerivativeStructure') -> 'DerivativeStructure': ...
    def asin(self) -> 'DerivativeStructure': ...
    def asinh(self) -> 'DerivativeStructure': ...
    def atan(self) -> 'DerivativeStructure': ...
    @typing.overload
    def atan2(self, derivativeStructure: 'DerivativeStructure') -> 'DerivativeStructure': ...
    @typing.overload
    @staticmethod
    def atan2(derivativeStructure: 'DerivativeStructure', derivativeStructure2: 'DerivativeStructure') -> 'DerivativeStructure': ...
    def atanh(self) -> 'DerivativeStructure': ...
    def cbrt(self) -> 'DerivativeStructure': ...
    def ceil(self) -> 'DerivativeStructure': ...
    def compose(self, *double: float) -> 'DerivativeStructure': ...
    @typing.overload
    def copySign(self, double: float) -> 'DerivativeStructure': ...
    @typing.overload
    def copySign(self, derivativeStructure: 'DerivativeStructure') -> 'DerivativeStructure': ...
    def cos(self) -> 'DerivativeStructure': ...
    def cosh(self) -> 'DerivativeStructure': ...
    def createConstant(self, double: float) -> 'DerivativeStructure': ...
    @typing.overload
    def divide(self, double: float) -> 'DerivativeStructure': ...
    @typing.overload
    def divide(self, derivativeStructure: 'DerivativeStructure') -> 'DerivativeStructure': ...
    def equals(self, object: typing.Any) -> bool: ...
    def exp(self) -> 'DerivativeStructure': ...
    def expm1(self) -> 'DerivativeStructure': ...
    def floor(self) -> 'DerivativeStructure': ...
    def getAllDerivatives(self) -> typing.MutableSequence[float]: ...
    def getExponent(self) -> int: ...
    def getField(self) -> fr.cnes.sirius.patrius.math.Field['DerivativeStructure']: ...
    def getFreeParameters(self) -> int: ...
    def getOrder(self) -> int: ...
    def getPartialDerivative(self, *int: int) -> float: ...
    def getReal(self) -> float: ...
    def getValue(self) -> float: ...
    def hashCode(self) -> int: ...
    @typing.overload
    def hypot(self, derivativeStructure: 'DerivativeStructure') -> 'DerivativeStructure': ...
    @typing.overload
    @staticmethod
    def hypot(derivativeStructure: 'DerivativeStructure', derivativeStructure2: 'DerivativeStructure') -> 'DerivativeStructure': ...
    @typing.overload
    def linearCombination(self, double: float, derivativeStructure: 'DerivativeStructure', double2: float, derivativeStructure2: 'DerivativeStructure') -> 'DerivativeStructure': ...
    @typing.overload
    def linearCombination(self, double: float, derivativeStructure: 'DerivativeStructure', double2: float, derivativeStructure2: 'DerivativeStructure', double3: float, derivativeStructure3: 'DerivativeStructure') -> 'DerivativeStructure': ...
    @typing.overload
    def linearCombination(self, double: float, derivativeStructure: 'DerivativeStructure', double2: float, derivativeStructure2: 'DerivativeStructure', double3: float, derivativeStructure3: 'DerivativeStructure', double4: float, derivativeStructure4: 'DerivativeStructure') -> 'DerivativeStructure': ...
    @typing.overload
    def linearCombination(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], derivativeStructureArray: typing.Union[typing.List['DerivativeStructure'], jpype.JArray]) -> 'DerivativeStructure': ...
    @typing.overload
    def linearCombination(self, derivativeStructure: 'DerivativeStructure', derivativeStructure2: 'DerivativeStructure', derivativeStructure3: 'DerivativeStructure', derivativeStructure4: 'DerivativeStructure') -> 'DerivativeStructure': ...
    @typing.overload
    def linearCombination(self, derivativeStructure: 'DerivativeStructure', derivativeStructure2: 'DerivativeStructure', derivativeStructure3: 'DerivativeStructure', derivativeStructure4: 'DerivativeStructure', derivativeStructure5: 'DerivativeStructure', derivativeStructure6: 'DerivativeStructure') -> 'DerivativeStructure': ...
    @typing.overload
    def linearCombination(self, derivativeStructure: 'DerivativeStructure', derivativeStructure2: 'DerivativeStructure', derivativeStructure3: 'DerivativeStructure', derivativeStructure4: 'DerivativeStructure', derivativeStructure5: 'DerivativeStructure', derivativeStructure6: 'DerivativeStructure', derivativeStructure7: 'DerivativeStructure', derivativeStructure8: 'DerivativeStructure') -> 'DerivativeStructure': ...
    @typing.overload
    def linearCombination(self, derivativeStructureArray: typing.Union[typing.List['DerivativeStructure'], jpype.JArray], derivativeStructureArray2: typing.Union[typing.List['DerivativeStructure'], jpype.JArray]) -> 'DerivativeStructure': ...
    def log(self) -> 'DerivativeStructure': ...
    def log10(self) -> 'DerivativeStructure': ...
    def log1p(self) -> 'DerivativeStructure': ...
    @typing.overload
    def multiply(self, double: float) -> 'DerivativeStructure': ...
    @typing.overload
    def multiply(self, derivativeStructure: 'DerivativeStructure') -> 'DerivativeStructure': ...
    @typing.overload
    def multiply(self, int: int) -> 'DerivativeStructure': ...
    def negate(self) -> 'DerivativeStructure': ...
    @typing.overload
    def pow(self, double: float) -> 'DerivativeStructure': ...
    @typing.overload
    def pow(self, derivativeStructure: 'DerivativeStructure') -> 'DerivativeStructure': ...
    @typing.overload
    def pow(self, int: int) -> 'DerivativeStructure': ...
    @typing.overload
    @staticmethod
    def pow(double: float, derivativeStructure: 'DerivativeStructure') -> 'DerivativeStructure': ...
    def reciprocal(self) -> 'DerivativeStructure': ...
    @typing.overload
    def remainder(self, double: float) -> 'DerivativeStructure': ...
    @typing.overload
    def remainder(self, derivativeStructure: 'DerivativeStructure') -> 'DerivativeStructure': ...
    def rint(self) -> 'DerivativeStructure': ...
    def rootN(self, int: int) -> 'DerivativeStructure': ...
    def round(self) -> int: ...
    def scalb(self, int: int) -> 'DerivativeStructure': ...
    def signum(self) -> 'DerivativeStructure': ...
    def sin(self) -> 'DerivativeStructure': ...
    def sinh(self) -> 'DerivativeStructure': ...
    def sqrt(self) -> 'DerivativeStructure': ...
    @typing.overload
    def subtract(self, double: float) -> 'DerivativeStructure': ...
    @typing.overload
    def subtract(self, derivativeStructure: 'DerivativeStructure') -> 'DerivativeStructure': ...
    def tan(self) -> 'DerivativeStructure': ...
    def tanh(self) -> 'DerivativeStructure': ...
    def taylor(self, *double: float) -> float: ...
    def toDegrees(self) -> 'DerivativeStructure': ...
    def toRadians(self) -> 'DerivativeStructure': ...

class GradientFunction(fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction):
    """
    public class GradientFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction`
    
        Class representing the gradient of a multivariate function.
    
        The vectorial components of the function represent the derivatives with respect to each function parameters.
    
        Since:
            3.1
    """
    def __init__(self, multivariateDifferentiableFunction: 'MultivariateDifferentiableFunction'): ...
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Compute the value for the function at the given point.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction`
        
            Parameters:
                point (double[]): point at which the function must be evaluated
        
            Returns:
                function value for the given point
        
        
        """
        ...

class JacobianFunction(fr.cnes.sirius.patrius.math.analysis.MultivariateMatrixFunction):
    """
    public class JacobianFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateMatrixFunction`
    
        Class representing the Jacobian of a multivariate vector function.
    
        The rows iterate on the model functions while the columns iterate on the parameters; thus, the numbers of rows is equal
        to the dimension of the underlying function vector value and the number of columns is equal to the number of free
        parameters of the underlying function.
    
        Since:
            3.1
    """
    def __init__(self, multivariateDifferentiableVectorFunction: 'MultivariateDifferentiableVectorFunction'): ...
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Compute the value for the function at the given point.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateMatrixFunction`
        
            Parameters:
                point (double[]): point at which the function must be evaluated
        
            Returns:
                function value for the given point
        
        
        """
        ...

class MultivariateDifferentiableFunction(fr.cnes.sirius.patrius.math.analysis.MultivariateFunction):
    """
    public interface MultivariateDifferentiableFunction extends :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction`
    
        Extension of :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction` representing a multivariate
        differentiable real function.
    
        Since:
            3.1
    """
    @typing.overload
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Compute the value for the function at the given point.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`[]): Point at which the function must be evaluated.
        
            Returns:
                the function value for the given point.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if :code:`point` does not fulfill functions constraints (wrong dimension, argument out of bound, or unsupported
                    derivative order for example)
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructureArray: typing.Union[typing.List[DerivativeStructure], jpype.JArray]) -> DerivativeStructure: ...

class MultivariateDifferentiableVectorFunction(fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction):
    """
    public interface MultivariateDifferentiableVectorFunction extends :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction`
    
        Extension of :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction` representing a multivariate
        differentiable vectorial function.
    
        Since:
            3.1
    """
    @typing.overload
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Compute the value for the function at the given point.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`[]): point at which the function must be evaluated
        
            Returns:
                function value for the given point
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if :code:`point` does not fulfill functions constraints (wrong dimension, argument out of bound, or unsupported
                    derivative order for example)
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructureArray: typing.Union[typing.List[DerivativeStructure], jpype.JArray]) -> typing.MutableSequence[DerivativeStructure]: ...

class UnivariateDifferentiableFunction(fr.cnes.sirius.patrius.math.analysis.UnivariateFunction):
    """
    public interface UnivariateDifferentiableFunction extends :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
    
        Interface for univariate functions derivatives.
    
        This interface represents a simple function which computes both the value and the first derivative of a mathematical
        function. The derivative is computed with respect to the input variable.
    
        Since:
            3.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`,
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateFunctionDifferentiator`
    """
    @typing.overload
    def value(self, double: float) -> float:
        """
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`:             if :code:`t` does not fulfill functions constraints (argument out of bound, or unsupported derivative order for example)
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: DerivativeStructure) -> DerivativeStructure: ...

class UnivariateDifferentiableMatrixFunction(fr.cnes.sirius.patrius.math.analysis.UnivariateMatrixFunction):
    """
    public interface UnivariateDifferentiableMatrixFunction extends :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateMatrixFunction`
    
        Extension of :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateMatrixFunction` representing a univariate
        differentiable matrix function.
    
        Since:
            3.1
    """
    @typing.overload
    def value(self, double: float) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Compute the value for the function.
        
            Parameters:
                x (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): the point for which the function value should be computed
        
            Returns:
                the value
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`:             if :code:`x` does not fulfill functions constraints (argument out of bound, or unsupported derivative order for example)
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: DerivativeStructure) -> typing.MutableSequence[typing.MutableSequence[DerivativeStructure]]: ...

class UnivariateDifferentiableVectorFunction(fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction):
    """
    public interface UnivariateDifferentiableVectorFunction extends :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction`
    
        Extension of :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction` representing a univariate
        differentiable vectorial function.
    
        Since:
            3.1
    """
    @typing.overload
    def value(self, double: float) -> typing.MutableSequence[float]:
        """
            Compute the value for the function.
        
            Parameters:
                x (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): the point for which the function value should be computed
        
            Returns:
                the value
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`:             if :code:`x` does not fulfill functions constraints (argument out of bound, or unsupported derivative order for example)
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: DerivativeStructure) -> typing.MutableSequence[DerivativeStructure]: ...

class UnivariateFunctionDifferentiator(java.io.Serializable):
    """
    public interface UnivariateFunctionDifferentiator extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface defining the function differentiation operation.
    
        Since:
            3.1
    """
    def differentiate(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable]) -> UnivariateDifferentiableFunction:
        """
            Create an implementation of a
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` from a regular
            :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`.
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): function to differentiate
        
            Returns:
                differential function
        
        
        """
        ...

class UnivariateMatrixFunctionDifferentiator:
    """
    public interface UnivariateMatrixFunctionDifferentiator
    
        Interface defining the function differentiation operation.
    
        Since:
            3.1
    """
    def differentiate(self, univariateMatrixFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateMatrixFunction, typing.Callable]) -> UnivariateDifferentiableMatrixFunction:
        """
            Create an implementation of a
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableMatrixFunction` from a regular
            :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateMatrixFunction`.
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateMatrixFunction`): function to differentiate
        
            Returns:
                differential function
        
        
        """
        ...

class UnivariateVectorFunctionDifferentiator:
    """
    public interface UnivariateVectorFunctionDifferentiator
    
        Interface defining the function differentiation operation.
    
        Since:
            3.1
    """
    def differentiate(self, univariateVectorFunction: fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction) -> UnivariateDifferentiableVectorFunction:
        """
            Create an implementation of a
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableVectorFunction` from a regular
            :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction`.
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction`): function to differentiate
        
            Returns:
                differential function
        
        
        """
        ...

class FiniteDifferencesDifferentiator(UnivariateFunctionDifferentiator, UnivariateVectorFunctionDifferentiator, UnivariateMatrixFunctionDifferentiator):
    """
    public class FiniteDifferencesDifferentiator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateFunctionDifferentiator`, :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateVectorFunctionDifferentiator`, :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateMatrixFunctionDifferentiator`
    
        Univariate functions differentiator using finite differences.
    
        This class creates some wrapper objects around regular :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        (or :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction` or
        :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateMatrixFunction`). These wrapper objects compute derivatives in
        addition to function value.
    
        The wrapper objects work by calling the underlying function on a sampling grid around the current point and performing
        polynomial interpolation. A finite differences scheme with n points is theoretically able to compute derivatives up to
        order n-1, but it is generally better to have a slight margin. The step size must also be small enough in order for the
        polynomial approximation to be good in the current point neighborhood, but it should not be too small because numerical
        instability appears quickly (there are several differences of close points). Choosing the number of points and the step
        size is highly problem dependent.
    
        As an example of good and bad settings, lets consider the quintic polynomial function :code:`f(x) =
        (x-1)*(x-0.5)*x*(x+0.5)*(x+1)`. Since it is a polynomial, finite differences with at least 6 points should theoretically
        recover the exact same polynomial and hence compute accurate derivatives for any order. However, due to numerical
        errors, we get the following results for a 7 points finite differences for abscissae in the [-10, 10] range:
    
          - step size = 0.25, second order derivative error about 9.97e-10
          - step size = 0.25, fourth order derivative error about 5.43e-8
          - step size = 1.0e-6, second order derivative error about 148
          - step size = 1.0e-6, fourth order derivative error about 6.35e+14
    
        This example shows that the small step size is really bad, even simply for second order derivative!
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, int: int, double: float): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, double3: float): ...
    @typing.overload
    def differentiate(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable]) -> UnivariateDifferentiableFunction:
        """
        
            The returned object cannot compute derivatives to arbitrary orders. The value function will throw a
            :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooLargeException` if the requested derivation order is larger or
            equal to the number of points.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateFunctionDifferentiator.differentiate` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateFunctionDifferentiator`
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): function to differentiate
        
            Returns:
                differential function
        
            Create an implementation of a
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableVectorFunction` from a regular
            :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction`.
        
            The returned object cannot compute derivatives to arbitrary orders. The value function will throw a
            :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooLargeException` if the requested derivation order is larger or
            equal to the number of points.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateVectorFunctionDifferentiator.differentiate` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateVectorFunctionDifferentiator`
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction`): function to differentiate
        
            Returns:
                differential function
        
            Create an implementation of a
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableMatrixFunction` from a regular
            :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateMatrixFunction`.
        
            The returned object cannot compute derivatives to arbitrary orders. The value function will throw a
            :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooLargeException` if the requested derivation order is larger or
            equal to the number of points.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateMatrixFunctionDifferentiator.differentiate` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateMatrixFunctionDifferentiator`
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateMatrixFunction`): function to differentiate
        
            Returns:
                differential function
        
        
        """
        ...
    @typing.overload
    def differentiate(self, univariateMatrixFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateMatrixFunction, typing.Callable]) -> UnivariateDifferentiableMatrixFunction: ...
    @typing.overload
    def differentiate(self, univariateVectorFunction: fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction) -> UnivariateDifferentiableVectorFunction: ...
    def getNbPoints(self) -> int:
        """
            Get the number of points to use.
        
            Returns:
                number of points to use
        
        
        """
        ...
    def getStepSize(self) -> float:
        """
            Get the step size.
        
            Returns:
                step size
        
        
        """
        ...

class RiddersDifferentiator(UnivariateFunctionDifferentiator):
    """
    public final class RiddersDifferentiator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateFunctionDifferentiator`
    
        Implements Ridders method of polynomial extrapolation for differentiation of real univariate functions.
    
    
        The algorithm implemented in this class comes from *Numerical Recipes in Fortran 77 : the art of scientific computing.*
    
    
        With respect to the :code:`UnivariateDifferentiableFunction` implementation, since this class uses a specific
        differentiation algorithm, the returned :code:`DerivativeStructure` instances are constant ( they cannot provide
        derivatives other than the first order already computed when they are created).
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float): ...
    @typing.overload
    def differentiate(self, double: float, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable]) -> float:
        """
            Differentiates a :code:`UnivariateFunction` on a single point using the Ridders method.
        
            Parameters:
                x (double): value for the computation
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): function to be derivated
        
            Returns:
                the derivative value f'(x)
        
        """
        ...
    @typing.overload
    def differentiate(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable]) -> UnivariateDifferentiableFunction:
        """
            Create an implementation of a
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` from a regular
            :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateFunctionDifferentiator.differentiate` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateFunctionDifferentiator`
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): function to differentiate
        
            Returns:
                differential function
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.analysis.differentiation")``.

    DSCompiler: typing.Type[DSCompiler]
    DerivativeStructure: typing.Type[DerivativeStructure]
    FiniteDifferencesDifferentiator: typing.Type[FiniteDifferencesDifferentiator]
    GradientFunction: typing.Type[GradientFunction]
    JacobianFunction: typing.Type[JacobianFunction]
    MultivariateDifferentiableFunction: typing.Type[MultivariateDifferentiableFunction]
    MultivariateDifferentiableVectorFunction: typing.Type[MultivariateDifferentiableVectorFunction]
    RiddersDifferentiator: typing.Type[RiddersDifferentiator]
    UnivariateDifferentiableFunction: typing.Type[UnivariateDifferentiableFunction]
    UnivariateDifferentiableMatrixFunction: typing.Type[UnivariateDifferentiableMatrixFunction]
    UnivariateDifferentiableVectorFunction: typing.Type[UnivariateDifferentiableVectorFunction]
    UnivariateFunctionDifferentiator: typing.Type[UnivariateFunctionDifferentiator]
    UnivariateMatrixFunctionDifferentiator: typing.Type[UnivariateMatrixFunctionDifferentiator]
    UnivariateVectorFunctionDifferentiator: typing.Type[UnivariateVectorFunctionDifferentiator]
