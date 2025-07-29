
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.optim
import fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.gradient
import fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.noderiv
import fr.cnes.sirius.patrius.math.random
import java.lang
import jpype
import typing



class GoalType(java.lang.Enum['GoalType'], fr.cnes.sirius.patrius.math.optim.OptimizationData):
    """
    public enum GoalType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.GoalType`> implements :class:`~fr.cnes.sirius.patrius.math.optim.OptimizationData`
    
        Goal type for an optimization problem (minimization or maximization of a scalar function.
    
        Since:
            2.0
    """
    MAXIMIZE: typing.ClassVar['GoalType'] = ...
    MINIMIZE: typing.ClassVar['GoalType'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'GoalType':
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
    def values() -> typing.MutableSequence['GoalType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (GoalType c : GoalType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class LeastSquaresConverter(fr.cnes.sirius.patrius.math.analysis.MultivariateFunction):
    @typing.overload
    def __init__(self, multivariateVectorFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction, typing.Callable], doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, multivariateVectorFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction, typing.Callable], doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, multivariateVectorFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction, typing.Callable], doubleArray: typing.Union[typing.List[float], jpype.JArray], realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix): ...
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...

class MultiStartMultivariateOptimizer(fr.cnes.sirius.patrius.math.optim.BaseMultiStartMultivariateOptimizer[fr.cnes.sirius.patrius.math.optim.PointValuePair]):
    def __init__(self, multivariateOptimizer: 'MultivariateOptimizer', int: int, randomVectorGenerator: typing.Union[fr.cnes.sirius.patrius.math.random.RandomVectorGenerator, typing.Callable]): ...
    def getOptima(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.optim.PointValuePair]: ...

class MultivariateFunctionMappingAdapter(fr.cnes.sirius.patrius.math.analysis.MultivariateFunction):
    """
    public class MultivariateFunctionMappingAdapter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction`
    
    
        Adapter for mapping bounded :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction` to unbounded ones.
    
        This adapter can be used to wrap functions subject to simple bounds on parameters so they can be used by optimizers that
        do *not* directly support simple bounds.
    
        The principle is that the user function that will be wrapped will see its parameters bounded as required, i.e when its
        :code:`value` method is called with argument array :code:`point`, the elements array will fulfill requirement
        :code:`lower[i] <= point[i] <= upper[i]` for all i. Some of the components may be unbounded or bounded only on one side
        if the corresponding bound is set to an infinite value. The optimizer will not manage the user function by itself, but
        it will handle this adapter and it is this adapter that will take care the bounds are fulfilled. The adapter null method
        will be called by the optimizer with unbound parameters, and the adapter will map the unbounded value to the bounded
        range using appropriate functions like :class:`~fr.cnes.sirius.patrius.math.analysis.function.Sigmoid` for double
        bounded elements for example.
    
        As the optimizer sees only unbounded parameters, it should be noted that the start point or simplex expected by the
        optimizer should be unbounded, so the user is responsible for converting his bounded point to unbounded by calling null
        before providing them to the optimizer.
    
        This adapter is only a poor man solution to simple bounds optimization constraints that can be used with simple
        optimizers like :class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.noderiv.SimplexOptimizer`. A better solution
        is to use an optimizer that directly supports simple bounds like
        :class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.noderiv.CMAESOptimizer` or
        :class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.noderiv.BOBYQAOptimizer`. One caveat of this poor-man's
        solution is that behavior near the bounds may be numerically unstable as bounds are mapped from infinite values. Another
        caveat is that convergence values are evaluated by the optimizer with respect to unbounded variables, so there will be
        scales differences when converted to bounded variables.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.MultivariateFunctionPenaltyAdapter`
    """
    def __init__(self, multivariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.MultivariateFunction, typing.Callable], doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    def boundedToUnbounded(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Maps an array from bounded to unbounded.
        
            Parameters:
                point (double[]): Bounded values.
        
            Returns:
                the unbounded values.
        
        
        """
        ...
    def unboundedToBounded(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Maps an array from unbounded to bounded.
        
            Parameters:
                point (double[]): Unbounded values.
        
            Returns:
                the bounded values.
        
        
        """
        ...
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Compute the underlying function value from an unbounded point.
        
            This method simply bounds the unbounded point using the mappings set up at construction and calls the underlying
            function using the bounded point.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction`
        
            Parameters:
                point (double[]): unbounded value
        
            Returns:
                underlying function value
        
            Also see:
        
        
        """
        ...

class MultivariateFunctionPenaltyAdapter(fr.cnes.sirius.patrius.math.analysis.MultivariateFunction):
    """
    public class MultivariateFunctionPenaltyAdapter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction`
    
    
        Adapter extending bounded :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction` to an unbouded domain
        using a penalty function.
    
        This adapter can be used to wrap functions subject to simple bounds on parameters so they can be used by optimizers that
        do *not* directly support simple bounds.
    
        The principle is that the user function that will be wrapped will see its parameters bounded as required, i.e when its
        :code:`value` method is called with argument array :code:`point`, the elements array will fulfill requirement
        :code:`lower[i] <= point[i] <= upper[i]` for all i. Some of the components may be unbounded or bounded only on one side
        if the corresponding bound is set to an infinite value. The optimizer will not manage the user function by itself, but
        it will handle this adapter and it is this adapter that will take care the bounds are fulfilled. The adapter null method
        will be called by the optimizer with unbound parameters, and the adapter will check if the parameters is within range or
        not. If it is in range, then the underlying user function will be called, and if it is not the value of a penalty
        function will be returned instead.
    
        This adapter is only a poor-man's solution to simple bounds optimization constraints that can be used with simple
        optimizers like :class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.noderiv.SimplexOptimizer`. A better solution
        is to use an optimizer that directly supports simple bounds like
        :class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.noderiv.CMAESOptimizer` or
        :class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.noderiv.BOBYQAOptimizer`. One caveat of this poor-man's
        solution is that if start point or start simplex is completely outside of the allowed range, only the penalty function
        is used, and the optimizer may converge without ever entering the range.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.MultivariateFunctionMappingAdapter`
    """
    def __init__(self, multivariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.MultivariateFunction, typing.Callable], doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float, doubleArray3: typing.Union[typing.List[float], jpype.JArray]): ...
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Computes the underlying function value from an unbounded point.
        
            This method simply returns the value of the underlying function if the unbounded point already fulfills the bounds, and
            compute a replacement value using the offset and scale if bounds are violated, without calling the function at all.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction`
        
            Parameters:
                point (double[]): unbounded point
        
            Returns:
                either underlying function value or penalty function value
        
        
        """
        ...

class MultivariateOptimizer(fr.cnes.sirius.patrius.math.optim.BaseMultivariateOptimizer[fr.cnes.sirius.patrius.math.optim.PointValuePair]):
    def getGoalType(self) -> GoalType: ...
    def optimize(self, *optimizationData: fr.cnes.sirius.patrius.math.optim.OptimizationData) -> fr.cnes.sirius.patrius.math.optim.PointValuePair: ...

class ObjectiveFunction(fr.cnes.sirius.patrius.math.optim.OptimizationData):
    """
    public class ObjectiveFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.OptimizationData`
    
        Scalar function to be optimized.
    
        Since:
            3.1
    """
    def __init__(self, multivariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.MultivariateFunction, typing.Callable]): ...
    def getObjectiveFunction(self) -> fr.cnes.sirius.patrius.math.analysis.MultivariateFunction:
        """
            Gets the function to be optimized.
        
            Returns:
                the objective function.
        
        
        """
        ...

class ObjectiveFunctionGradient(fr.cnes.sirius.patrius.math.optim.OptimizationData):
    """
    public class ObjectiveFunctionGradient extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.OptimizationData`
    
        Gradient of the scalar function to be optimized.
    
        Since:
            3.1
    """
    def __init__(self, multivariateVectorFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction, typing.Callable]): ...
    def getObjectiveFunctionGradient(self) -> fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction:
        """
            Gets the gradient of the function to be optimized.
        
            Returns:
                the objective function gradient.
        
        
        """
        ...

class GradientMultivariateOptimizer(MultivariateOptimizer):
    def optimize(self, *optimizationData: fr.cnes.sirius.patrius.math.optim.OptimizationData) -> fr.cnes.sirius.patrius.math.optim.PointValuePair: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.nonlinear.scalar")``.

    GoalType: typing.Type[GoalType]
    GradientMultivariateOptimizer: typing.Type[GradientMultivariateOptimizer]
    LeastSquaresConverter: typing.Type[LeastSquaresConverter]
    MultiStartMultivariateOptimizer: typing.Type[MultiStartMultivariateOptimizer]
    MultivariateFunctionMappingAdapter: typing.Type[MultivariateFunctionMappingAdapter]
    MultivariateFunctionPenaltyAdapter: typing.Type[MultivariateFunctionPenaltyAdapter]
    MultivariateOptimizer: typing.Type[MultivariateOptimizer]
    ObjectiveFunction: typing.Type[ObjectiveFunction]
    ObjectiveFunctionGradient: typing.Type[ObjectiveFunctionGradient]
    gradient: fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.gradient.__module_protocol__
    noderiv: fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.noderiv.__module_protocol__
