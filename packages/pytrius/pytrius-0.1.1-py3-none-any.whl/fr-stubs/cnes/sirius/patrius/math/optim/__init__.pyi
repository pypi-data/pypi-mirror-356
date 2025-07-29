
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.optim.joptimizer
import fr.cnes.sirius.patrius.math.optim.linear
import fr.cnes.sirius.patrius.math.optim.nonlinear
import fr.cnes.sirius.patrius.math.optim.univariate
import fr.cnes.sirius.patrius.math.random
import fr.cnes.sirius.patrius.math.util
import jpype
import typing



_BaseOptimizer__T = typing.TypeVar('_BaseOptimizer__T')  # <T>
class BaseOptimizer(typing.Generic[_BaseOptimizer__T]):
    def getConvergenceChecker(self) -> 'ConvergenceChecker'[_BaseOptimizer__T]: ...
    def getEvaluations(self) -> int: ...
    def getIterations(self) -> int: ...
    def getMaxEvaluations(self) -> int: ...
    def getMaxIterations(self) -> int: ...
    def optimize(self, *optimizationData: 'OptimizationData') -> _BaseOptimizer__T: ...

_ConvergenceChecker__PAIR = typing.TypeVar('_ConvergenceChecker__PAIR')  # <PAIR>
class ConvergenceChecker(typing.Generic[_ConvergenceChecker__PAIR]):
    def converged(self, int: int, pAIR: _ConvergenceChecker__PAIR, pAIR2: _ConvergenceChecker__PAIR) -> bool: ...

class OptimizationData:
    """
    public interface OptimizationData
    
        Marker interface. Implementations will provide functionality (optional or required) needed by the optimizers, and those
        will need to check the actual type of the arguments and perform the appropriate cast in order to access the data they
        need.
    
        Since:
            3.1
    """
    ...

class PointValuePair(fr.cnes.sirius.patrius.math.util.Pair[typing.MutableSequence[float], float]):
    """
    public class PointValuePair extends :class:`~fr.cnes.sirius.patrius.math.util.Pair`<double[],`Double <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>`>
    
        This class holds a point and the value of an objective function at that point.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.optim.PointVectorValuePair`,
            :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, boolean: bool): ...
    def getPoint(self) -> typing.MutableSequence[float]:
        """
            Getter for the point.
        
            Returns:
                a copy of the stored point
        
        
        """
        ...
    def getPointRef(self) -> typing.MutableSequence[float]:
        """
            Getter for the reference to the point.
        
            Returns:
                the reference to the internal array storing the point
        
        
        """
        ...

class PointVectorValuePair(fr.cnes.sirius.patrius.math.util.Pair[typing.MutableSequence[float], typing.MutableSequence[float]]):
    """
    public class PointVectorValuePair extends :class:`~fr.cnes.sirius.patrius.math.util.Pair`<double[],double[]>
    
        This class holds a point and the vectorial value of an objective function at that point.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.optim.PointValuePair`,
            :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool): ...
    def getPoint(self) -> typing.MutableSequence[float]:
        """
            Gets the point.
        
            Returns:
                a copy of the stored point
        
        
        """
        ...
    def getPointRef(self) -> typing.MutableSequence[float]:
        """
            Getter for a reference to the point.
        
            Returns:
                a reference to the internal array storing the point
        
        
        """
        ...
    def getValue(self) -> typing.MutableSequence[float]:
        """
            Getter for the value of the objective function.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.util.Pair.getValue` in class :class:`~fr.cnes.sirius.patrius.math.util.Pair`
        
            Returns:
                a copy of the stored value of the objective function
        
        
        """
        ...
    def getValueRef(self) -> typing.MutableSequence[float]:
        """
            Gets a reference to the value of the objective function.
        
            Returns:
                a reference to the internal array storing the value of the objective function
        
        
        """
        ...

_AbstractConvergenceChecker__T = typing.TypeVar('_AbstractConvergenceChecker__T')  # <T>
class AbstractConvergenceChecker(ConvergenceChecker[_AbstractConvergenceChecker__T], typing.Generic[_AbstractConvergenceChecker__T]):
    """
    public abstract class AbstractConvergenceChecker<T> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.ConvergenceChecker`<T>
    
        Base class for all convergence checker implementations.
    
        Since:
            3.0
    """
    def __init__(self, double: float, double2: float): ...
    def converged(self, int: int, t: _AbstractConvergenceChecker__T, t2: _AbstractConvergenceChecker__T) -> bool:
        """
            Check if the optimization algorithm has converged.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.optim.ConvergenceChecker.converged` in
                interface :class:`~fr.cnes.sirius.patrius.math.optim.ConvergenceChecker`
        
            Parameters:
                iteration (int): Current iteration.
                previous (:class:`~fr.cnes.sirius.patrius.math.optim.AbstractConvergenceChecker`): Best point in the previous iteration.
                current (:class:`~fr.cnes.sirius.patrius.math.optim.AbstractConvergenceChecker`): Best point in the current iteration.
        
            Returns:
                :code:`true` if the algorithm is considered to have converged.
        
        
        """
        ...
    def getAbsoluteThreshold(self) -> float:
        """
        
            Returns:
                the absolute threshold.
        
        
        """
        ...
    def getRelativeThreshold(self) -> float:
        """
        
            Returns:
                the relative threshold.
        
        
        """
        ...

_BaseMultivariateOptimizer__T = typing.TypeVar('_BaseMultivariateOptimizer__T')  # <T>
class BaseMultivariateOptimizer(BaseOptimizer[_BaseMultivariateOptimizer__T], typing.Generic[_BaseMultivariateOptimizer__T]):
    def getLowerBound(self) -> typing.MutableSequence[float]: ...
    def getStartPoint(self) -> typing.MutableSequence[float]: ...
    def getUpperBound(self) -> typing.MutableSequence[float]: ...
    def optimize(self, *optimizationData: OptimizationData) -> _BaseMultivariateOptimizer__T: ...

class InitialGuess(OptimizationData):
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    def getInitialGuess(self) -> typing.MutableSequence[float]: ...

class MaxEval(OptimizationData):
    """
    public class MaxEval extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.OptimizationData`
    
        Maximum number of evaluations of the function to be optimized.
    
        Since:
            3.1
    """
    def __init__(self, int: int): ...
    def getMaxEval(self) -> int:
        """
            Gets the maximum number of evaluations.
        
            Returns:
                the allowed number of evaluations.
        
        
        """
        ...
    @staticmethod
    def unlimited() -> 'MaxEval':
        """
            Factory method that creates instance of this class that represents a virtually unlimited number of evaluations.
        
            Returns:
                a new instance suitable for allowing `null
                <http://docs.oracle.com/javase/8/docs/api/java/lang/Integer.html?is-external=true#MAX_VALUE>` evaluations.
        
        
        """
        ...

class MaxIter(OptimizationData):
    """
    public class MaxIter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.OptimizationData`
    
        Maximum number of iterations performed by an (iterative) algorithm.
    
        Since:
            3.1
    """
    def __init__(self, int: int): ...
    def getMaxIter(self) -> int:
        """
            Gets the maximum number of evaluations.
        
            Returns:
                the allowed number of evaluations.
        
        
        """
        ...
    @staticmethod
    def unlimited() -> 'MaxIter':
        """
            Factory method that creates instance of this class that represents a virtually unlimited number of iterations.
        
            Returns:
                a new instance suitable for allowing `null
                <http://docs.oracle.com/javase/8/docs/api/java/lang/Integer.html?is-external=true#MAX_VALUE>` evaluations.
        
        
        """
        ...

class SimpleBounds(OptimizationData):
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    def getLower(self) -> typing.MutableSequence[float]: ...
    def getUpper(self) -> typing.MutableSequence[float]: ...
    @staticmethod
    def unbounded(int: int) -> 'SimpleBounds': ...

_BaseMultiStartMultivariateOptimizer__T = typing.TypeVar('_BaseMultiStartMultivariateOptimizer__T')  # <T>
class BaseMultiStartMultivariateOptimizer(BaseMultivariateOptimizer[_BaseMultiStartMultivariateOptimizer__T], typing.Generic[_BaseMultiStartMultivariateOptimizer__T]):
    def __init__(self, baseMultivariateOptimizer: BaseMultivariateOptimizer[_BaseMultiStartMultivariateOptimizer__T], int: int, randomVectorGenerator: typing.Union[fr.cnes.sirius.patrius.math.random.RandomVectorGenerator, typing.Callable]): ...
    def getEvaluations(self) -> int: ...
    def getOptima(self) -> typing.MutableSequence[_BaseMultiStartMultivariateOptimizer__T]: ...
    def optimize(self, *optimizationData: OptimizationData) -> _BaseMultiStartMultivariateOptimizer__T: ...

_SimplePointChecker__T = typing.TypeVar('_SimplePointChecker__T', bound=fr.cnes.sirius.patrius.math.util.Pair)  # <T>
class SimplePointChecker(AbstractConvergenceChecker[_SimplePointChecker__T], typing.Generic[_SimplePointChecker__T]):
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, int: int): ...
    def converged(self, int: int, t: _SimplePointChecker__T, t2: _SimplePointChecker__T) -> bool: ...

class SimpleValueChecker(AbstractConvergenceChecker[PointValuePair]):
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, int: int): ...
    def converged(self, int: int, pointValuePair: PointValuePair, pointValuePair2: PointValuePair) -> bool: ...

class SimpleVectorValueChecker(AbstractConvergenceChecker[PointVectorValuePair]):
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, int: int): ...
    def converged(self, int: int, pointVectorValuePair: PointVectorValuePair, pointVectorValuePair2: PointVectorValuePair) -> bool: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim")``.

    AbstractConvergenceChecker: typing.Type[AbstractConvergenceChecker]
    BaseMultiStartMultivariateOptimizer: typing.Type[BaseMultiStartMultivariateOptimizer]
    BaseMultivariateOptimizer: typing.Type[BaseMultivariateOptimizer]
    BaseOptimizer: typing.Type[BaseOptimizer]
    ConvergenceChecker: typing.Type[ConvergenceChecker]
    InitialGuess: typing.Type[InitialGuess]
    MaxEval: typing.Type[MaxEval]
    MaxIter: typing.Type[MaxIter]
    OptimizationData: typing.Type[OptimizationData]
    PointValuePair: typing.Type[PointValuePair]
    PointVectorValuePair: typing.Type[PointVectorValuePair]
    SimpleBounds: typing.Type[SimpleBounds]
    SimplePointChecker: typing.Type[SimplePointChecker]
    SimpleValueChecker: typing.Type[SimpleValueChecker]
    SimpleVectorValueChecker: typing.Type[SimpleVectorValueChecker]
    joptimizer: fr.cnes.sirius.patrius.math.optim.joptimizer.__module_protocol__
    linear: fr.cnes.sirius.patrius.math.optim.linear.__module_protocol__
    nonlinear: fr.cnes.sirius.patrius.math.optim.nonlinear.__module_protocol__
    univariate: fr.cnes.sirius.patrius.math.optim.univariate.__module_protocol__
