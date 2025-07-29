
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.optim
import fr.cnes.sirius.patrius.math.optim.nonlinear.scalar
import fr.cnes.sirius.patrius.math.random
import java.io
import typing



class BracketFinder(java.io.Serializable):
    """
    public class BracketFinder extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Provide an interval that brackets a local optimum of a function. This code is based on a Python implementation (from
        *SciPy*, module :code:`optimize.py` v0.5).
    
        Since:
            2.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, int: int): ...
    def getEvaluations(self) -> int:
        """
        
            Returns:
                the number of evalutations.
        
        
        """
        ...
    def getFHi(self) -> float:
        """
            Get function value at :meth:`~fr.cnes.sirius.patrius.math.optim.univariate.BracketFinder.getHi`.
        
            Returns:
                function value at :meth:`~fr.cnes.sirius.patrius.math.optim.univariate.BracketFinder.getHi`
        
        
        """
        ...
    def getFLo(self) -> float:
        """
            Get function value at :meth:`~fr.cnes.sirius.patrius.math.optim.univariate.BracketFinder.getLo`.
        
            Returns:
                function value at :meth:`~fr.cnes.sirius.patrius.math.optim.univariate.BracketFinder.getLo`
        
        
        """
        ...
    def getFMid(self) -> float:
        """
            Get function value at :meth:`~fr.cnes.sirius.patrius.math.optim.univariate.BracketFinder.getMid`.
        
            Returns:
                function value at :meth:`~fr.cnes.sirius.patrius.math.optim.univariate.BracketFinder.getMid`
        
        
        """
        ...
    def getHi(self) -> float:
        """
        
            Returns:
                the higher bound of the bracket.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.optim.univariate.BracketFinder.getFHi`
        
        
        """
        ...
    def getLo(self) -> float:
        """
        
            Returns:
                the lower bound of the bracket.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.optim.univariate.BracketFinder.getFLo`
        
        
        """
        ...
    def getMaxEvaluations(self) -> int:
        """
        
            Returns:
                the number of evalutations.
        
        
        """
        ...
    def getMid(self) -> float:
        """
        
            Returns:
                a point in the middle of the bracket.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.optim.univariate.BracketFinder.getFMid`
        
        
        """
        ...
    def search(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], goalType: fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.GoalType, double: float, double2: float) -> None:
        """
            Search new points that bracket a local optimum of the function.
        
            Parameters:
                func (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Function whose optimum should be bracketed.
                goal (:class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.GoalType`): :class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.GoalType`.
                xAIn (double): Initial point.
                xBIn (double): Initial point.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the maximum number of evaluations is exceeded.
        
        
        """
        ...

class SearchInterval(fr.cnes.sirius.patrius.math.optim.OptimizationData):
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...
    def getMax(self) -> float: ...
    def getMin(self) -> float: ...
    def getStartValue(self) -> float: ...

class SimpleUnivariateValueChecker(fr.cnes.sirius.patrius.math.optim.AbstractConvergenceChecker['UnivariatePointValuePair']):
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, int: int): ...
    def converged(self, int: int, univariatePointValuePair: 'UnivariatePointValuePair', univariatePointValuePair2: 'UnivariatePointValuePair') -> bool: ...

class UnivariateObjectiveFunction(fr.cnes.sirius.patrius.math.optim.OptimizationData):
    """
    public class UnivariateObjectiveFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.OptimizationData`
    
        Scalar function to be optimized.
    
        Since:
            3.1
    """
    def __init__(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable]): ...
    def getObjectiveFunction(self) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction:
        """
            Gets the function to be optimized.
        
            Returns:
                the objective function.
        
        
        """
        ...

class UnivariateOptimizer(fr.cnes.sirius.patrius.math.optim.BaseOptimizer['UnivariatePointValuePair']):
    def getGoalType(self) -> fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.GoalType: ...
    def getMax(self) -> float: ...
    def getMin(self) -> float: ...
    def getStartValue(self) -> float: ...
    def optimize(self, *optimizationData: fr.cnes.sirius.patrius.math.optim.OptimizationData) -> 'UnivariatePointValuePair': ...

class UnivariatePointValuePair(java.io.Serializable):
    """
    public class UnivariatePointValuePair extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class holds a point and the value of an objective function at this point. This is a simple immutable container.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float): ...
    def getPoint(self) -> float:
        """
            Get the point.
        
            Returns:
                the point.
        
        
        """
        ...
    def getValue(self) -> float:
        """
            Get the value of the objective function.
        
            Returns:
                the stored value of the objective function.
        
        
        """
        ...

class BrentOptimizer(UnivariateOptimizer):
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, convergenceChecker: typing.Union[fr.cnes.sirius.patrius.math.optim.ConvergenceChecker[UnivariatePointValuePair], typing.Callable[[int, UnivariatePointValuePair, UnivariatePointValuePair], bool]]): ...

class MultiStartUnivariateOptimizer(UnivariateOptimizer):
    def __init__(self, univariateOptimizer: UnivariateOptimizer, int: int, randomGenerator: fr.cnes.sirius.patrius.math.random.RandomGenerator): ...
    def getEvaluations(self) -> int: ...
    def getOptima(self) -> typing.MutableSequence[UnivariatePointValuePair]: ...
    def optimize(self, *optimizationData: fr.cnes.sirius.patrius.math.optim.OptimizationData) -> UnivariatePointValuePair: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.univariate")``.

    BracketFinder: typing.Type[BracketFinder]
    BrentOptimizer: typing.Type[BrentOptimizer]
    MultiStartUnivariateOptimizer: typing.Type[MultiStartUnivariateOptimizer]
    SearchInterval: typing.Type[SearchInterval]
    SimpleUnivariateValueChecker: typing.Type[SimpleUnivariateValueChecker]
    UnivariateObjectiveFunction: typing.Type[UnivariateObjectiveFunction]
    UnivariateOptimizer: typing.Type[UnivariateOptimizer]
    UnivariatePointValuePair: typing.Type[UnivariatePointValuePair]
