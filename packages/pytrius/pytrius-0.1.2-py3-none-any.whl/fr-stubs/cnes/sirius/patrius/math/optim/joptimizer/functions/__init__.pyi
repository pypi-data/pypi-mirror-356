
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jpype
import typing



class FunctionsUtils:
    """
    public final class FunctionsUtils extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Utility class for optimization function building.
    
        Since:
            4.6
    """
    @typing.overload
    @staticmethod
    def createCircle(int: int, double: float) -> 'ConvexMultivariateRealFunction':
        """
            Create a circle
        
            Parameters:
                dim (int): dimension of the circle
                radius (double): radius of the circle
        
            Returns:
                ConvexMultivariateRealFunction
        
            Create a circle
        
            Parameters:
                dim (int): dimension of the circle
                radius (double): radius of the circle
                center (double[]): the position of the center of the circle
        
            Returns:
                ConvexMultivariateRealFunction
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def createCircle(int: int, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> 'ConvexMultivariateRealFunction': ...

class TwiceDifferentiableMultivariateRealFunction:
    """
    public interface TwiceDifferentiableMultivariateRealFunction
    
        Interface for multi-variate functions that are twice differentiable., i.e. for which a gradient and a hessian can be
        provided.
    
        Since:
            4.6
    """
    def getDim(self) -> int:
        """
            Get dimension of the function argument.
        
            Returns:
                dimension
        
        
        """
        ...
    def gradient(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Function gradient at point X.
        
            Parameters:
                x (double[]): point
        
            Returns:
                gradient
        
        
        """
        ...
    def hessian(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Function hessian at point X.
        
            Parameters:
                x (double[]): point
        
            Returns:
                hessian
        
        
        """
        ...
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Evaluation of the function at point X.
        
            Parameters:
                x (double[]): point
        
            Returns:
                evaluation
        
        
        """
        ...

class BarrierFunction(TwiceDifferentiableMultivariateRealFunction):
    """
    public interface BarrierFunction extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.TwiceDifferentiableMultivariateRealFunction`
    
        Interface for the barrier function used by a given barrier optimization method.
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, 11.2"
    """
    def calculatePhase1InitialFeasiblePoint(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> float:
        """
            Calculates the initial value for the additional variable s in basic Phase I method.
        
            Parameters:
                originalNotFeasiblePoint (double[]): initial point (not-feasible)
                tolerance (double): tolerance
        
            Returns:
                phase 1 initial feasible point
        
            Also see:
                "S.Boyd and L.Vandenberghe, Convex Optimization, 11.4.1"
        
        
        """
        ...
    def createPhase1BarrierFunction(self) -> 'BarrierFunction':
        """
            Create the barrier function for the basic Phase I method.
        
            Returns:
                phase 1 barrier function
        
            Also see:
                "S.Boyd and L.Vandenberghe, Convex Optimization, 11.4.1"
        
        
        """
        ...
    def getDualityGap(self, double: float) -> float:
        """
            Calculates the duality gap for a barrier method build with this barrier function.
        
            Parameters:
                t (double): value
        
            Returns:
                duality gap
        
        
        """
        ...

class ConvexMultivariateRealFunction(TwiceDifferentiableMultivariateRealFunction):
    """
    public interface ConvexMultivariateRealFunction extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.TwiceDifferentiableMultivariateRealFunction`
    
        Interface for convex multi-variate real functions.
    
        Use this whenever possible, because the algorithm will check that.
    
        Since:
            4.6
    """
    ...

class QuadraticMultivariateRealFunction(TwiceDifferentiableMultivariateRealFunction):
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float, boolean: bool): ...
    def getDim(self) -> int: ...
    def gradient(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    def hessian(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...

class LinearMultivariateRealFunction(QuadraticMultivariateRealFunction, ConvexMultivariateRealFunction):
    """
    public class LinearMultivariateRealFunction extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.QuadraticMultivariateRealFunction` implements :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.ConvexMultivariateRealFunction`
    
        Represents a function f(x) = q.x + r.
    
        Since:
            4.6
    """
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float): ...

class LogarithmicBarrier(BarrierFunction):
    """
    public class LogarithmicBarrier extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.BarrierFunction`
    
        Default barrier function for the barrier method algorithm.
    
    
        If f_i(x) are the inequalities of the problem, theh we have:
    
    
        *Φ* = - Sum_i[log(-f_i(x))]
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, 11.2.1"
    """
    def __init__(self, convexMultivariateRealFunctionArray: typing.Union[typing.List[ConvexMultivariateRealFunction], jpype.JArray], int: int): ...
    def calculatePhase1InitialFeasiblePoint(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> float:
        """
            Calculates the initial value for the s parameter in Phase I. Return s = max(fi(x))
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.BarrierFunction`
        
            Parameters:
                originalNotFeasiblePoint (double[]): initial point (not-feasible)
                tolerance (double): tolerance
        
            Returns:
                phase 1 initial feasible point
        
            Also see:
                "S.Boyd and L.Vandenberghe, Convex Optimization, 11.6.2"
        
        
        """
        ...
    def createPhase1BarrierFunction(self) -> BarrierFunction:
        """
            Create the barrier function for the Phase I. It is a LogarithmicBarrier for the constraints:
        
        
            fi(X)-s, i=1,...,n
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.BarrierFunction.createPhase1BarrierFunction` in
                interface :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.BarrierFunction`
        
            Returns:
                phase 1 barrier function
        
            Also see:
                "S.Boyd and L.Vandenberghe, Convex Optimization, 11.4.1"
        
        
        """
        ...
    def getDim(self) -> int:
        """
            Get dimension
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.TwiceDifferentiableMultivariateRealFunction.getDim` in
                interface :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.TwiceDifferentiableMultivariateRealFunction`
        
            Returns:
                dimension
        
        
        """
        ...
    def getDualityGap(self, double: float) -> float:
        """
            Calculates the duality gap for a barrier method build with this barrier function
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.BarrierFunction.getDualityGap` in
                interface :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.BarrierFunction`
        
            Parameters:
                t (double): value
        
            Returns:
                duality gap
        
        
        """
        ...
    def gradient(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Function gradient at point X
        
            Specified by:
                 in
                interface :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.TwiceDifferentiableMultivariateRealFunction`
        
            Parameters:
                value (double[]): point
        
            Returns:
                gradient
        
        
        """
        ...
    def hessian(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Function hessian at point X.
        
            Specified by:
                 in
                interface :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.TwiceDifferentiableMultivariateRealFunction`
        
            Parameters:
                value (double[]): point
        
            Returns:
                hessian
        
        
        """
        ...
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Evaluation of the function at point X.
        
            Specified by:
                 in
                interface :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.TwiceDifferentiableMultivariateRealFunction`
        
            Parameters:
                val (double[]): point
        
            Returns:
                evaluation
        
        
        """
        ...

class PSDQuadraticMultivariateRealFunction(QuadraticMultivariateRealFunction, ConvexMultivariateRealFunction):
    """
    public class PSDQuadraticMultivariateRealFunction extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.QuadraticMultivariateRealFunction` implements :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.ConvexMultivariateRealFunction`
    
        Function 1/2 * x.P.x + q.x + r, P symmetric and positive semi-definite
    
        Since:
            4.6
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float, boolean: bool): ...

class StrictlyConvexMultivariateRealFunction(ConvexMultivariateRealFunction):
    """
    public interface StrictlyConvexMultivariateRealFunction extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.ConvexMultivariateRealFunction`
    
        Interface for strictly convex multi-variate real functions.
    
        Use children classes whenever possible, because the algorithm will check that.
    
        Since:
            4.6
    """
    ...

class PDQuadraticMultivariateRealFunction(PSDQuadraticMultivariateRealFunction, StrictlyConvexMultivariateRealFunction):
    """
    public class PDQuadraticMultivariateRealFunction extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.PSDQuadraticMultivariateRealFunction` implements :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.StrictlyConvexMultivariateRealFunction`
    
        Function 1/2 * x.P.x + q.x + r, P symmetric and positive definite
    
        Since:
            4.6
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double3: float, boolean: bool): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.joptimizer.functions")``.

    BarrierFunction: typing.Type[BarrierFunction]
    ConvexMultivariateRealFunction: typing.Type[ConvexMultivariateRealFunction]
    FunctionsUtils: typing.Type[FunctionsUtils]
    LinearMultivariateRealFunction: typing.Type[LinearMultivariateRealFunction]
    LogarithmicBarrier: typing.Type[LogarithmicBarrier]
    PDQuadraticMultivariateRealFunction: typing.Type[PDQuadraticMultivariateRealFunction]
    PSDQuadraticMultivariateRealFunction: typing.Type[PSDQuadraticMultivariateRealFunction]
    QuadraticMultivariateRealFunction: typing.Type[QuadraticMultivariateRealFunction]
    StrictlyConvexMultivariateRealFunction: typing.Type[StrictlyConvexMultivariateRealFunction]
    TwiceDifferentiableMultivariateRealFunction: typing.Type[TwiceDifferentiableMultivariateRealFunction]
