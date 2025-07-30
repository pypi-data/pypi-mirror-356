
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.optim.joptimizer.functions
import fr.cnes.sirius.patrius.math.optim.joptimizer.solvers
import jpype
import typing



class BasicPhaseIBM:
    """
    public class BasicPhaseIBM extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Basic Phase I Method (implemented as a Barried Method).
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, p. 579"
    """
    def __init__(self, barrierMethod: 'BarrierMethod'): ...
    def findFeasibleInitialPoint(self) -> typing.MutableSequence[float]: ...

class BasicPhaseILPPDM:
    """
    public class BasicPhaseILPPDM extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Basic Phase I Method form LP problems (implemented as a Primal-Dual Method).
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, p. 579"
    """
    def __init__(self, lPPrimalDualMethod: 'LPPrimalDualMethod'): ...
    def findFeasibleInitialPoint(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...

class BasicPhaseIPDM:
    """
    public class BasicPhaseIPDM extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Basic Phase I Method (implemented as a Primal-Dual Method).
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, p. 579"
    """
    def __init__(self, primalDualMethod: 'PrimalDualMethod'): ...
    def findFeasibleInitialPoint(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...

class JOptimizer:
    """
    public final class JOptimizer extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Convex Optimizer. The algorithm selection is implemented as a Chain of Responsibility pattern, and this class is the
        client of the chain.
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization"
    """
    DEFAULT_MAX_ITERATION: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_MAX_ITERATION
    
        Default max number of iterations
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_FEASIBILITY_TOLERANCE: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_FEASIBILITY_TOLERANCE
    
        Default feasibility tolerance
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_TOLERANCE: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_TOLERANCE
    
        Default tolerance
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_TOLERANCE_INNER_STEP: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_TOLERANCE_INNER_STEP
    
        Default tolerance for inner step
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_KKT_TOLERANCE: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_KKT_TOLERANCE
    
        Default ktt tolerance
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_ALPHA: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_ALPHA
    
        Default alpha
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_BETA: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_BETA
    
        Default beta
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_MU: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_MU
    
        Default mu
    
        Also see:
            :meth:`~constant`
    
    
    """
    BARRIER_METHOD: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` BARRIER_METHOD
    
        Barrier method string
    
        Also see:
            :meth:`~constant`
    
    
    """
    PRIMAL_DUAL_METHOD: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` PRIMAL_DUAL_METHOD
    
        Primal dual method string
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_INTERIOR_POINT_METHOD: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_INTERIOR_POINT_METHOD
    
        Default interior point method string
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def getOptimizationResponse(self) -> 'OptimizationResponse':
        """
            Get the optimization request
        
            Returns:
                optimization request
        
        
        """
        ...
    def optimize(self) -> int: ...
    def setOptimizationRequest(self, optimizationRequest: 'OptimizationRequest') -> None:
        """
            Set the optimization request
        
            Parameters:
                or (:class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequest`): optimization request
        
        
        """
        ...

class LPPresolver:
    DEFAULT_UNBOUNDED_LOWER_BOUND: typing.ClassVar[float] = ...
    DEFAULT_UNBOUNDED_UPPER_BOUND: typing.ClassVar[float] = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    def getMaxRescaledUB(self) -> float: ...
    def getMinRescaledLB(self) -> float: ...
    def getOriginalMeq(self) -> int: ...
    def getOriginalN(self) -> int: ...
    def getPresolvedA(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def getPresolvedB(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getPresolvedC(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getPresolvedLB(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getPresolvedMeq(self) -> int: ...
    def getPresolvedN(self) -> int: ...
    def getPresolvedUB(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getPresolvedYlb(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getPresolvedYub(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getPresolvedZlb(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getPresolvedZub(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def isAvoidIncreaseSparsity(self) -> bool: ...
    def isLBUnbounded(self, double: float) -> bool: ...
    def isUBUnbounded(self, double: float) -> bool: ...
    def postsolve(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def presolve(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def presolve(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray], doubleArray4: typing.Union[typing.List[float], jpype.JArray], doubleArray5: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    def presolve(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realVector2: fr.cnes.sirius.patrius.math.linear.RealVector, realVector3: fr.cnes.sirius.patrius.math.linear.RealVector, realVector4: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def setAvoidFillIn(self, boolean: bool) -> None: ...
    def setAvoidIncreaseSparsity(self, boolean: bool) -> None: ...
    def setAvoidScaling(self, boolean: bool) -> None: ...
    def setExpectedSolution(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def setNOfSlackVariables(self, int: int) -> None: ...
    def setZeroTolerance(self, double: float) -> None: ...

class LPStandardConverter:
    DEFAULT_UNBOUNDED_LOWER_BOUND: typing.ClassVar[float] = ...
    DEFAULT_UNBOUNDED_UPPER_BOUND: typing.ClassVar[float] = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...
    @typing.overload
    def __init__(self, boolean: bool, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    def getOriginalN(self) -> int: ...
    def getStandardA(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def getStandardB(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getStandardC(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getStandardComponents(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    def getStandardLB(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getStandardN(self) -> int: ...
    def getStandardS(self) -> int: ...
    def getStandardUB(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getUnboundedLBValue(self) -> float: ...
    def getUnboundedUBValue(self) -> float: ...
    def isLbUnbounded(self, double: float) -> bool: ...
    def isUbUnbounded(self, double: float) -> bool: ...
    def postConvert(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def toStandardForm(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray], doubleArray4: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray5: typing.Union[typing.List[float], jpype.JArray], doubleArray6: typing.Union[typing.List[float], jpype.JArray], doubleArray7: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    def toStandardForm(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realVector2: fr.cnes.sirius.patrius.math.linear.RealVector, realMatrix2: fr.cnes.sirius.patrius.math.linear.RealMatrix, realVector3: fr.cnes.sirius.patrius.math.linear.RealVector, realVector4: fr.cnes.sirius.patrius.math.linear.RealVector, realVector5: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...

class OptimizationRequest:
    """
    public class OptimizationRequest extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Optimization problem. Setting the field's values you define an optimization problem.
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization"
    """
    def __init__(self): ...
    def getA(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Get the equalities constraints matrix
        
            Returns:
                equalities constraints matrix
        
        
        """
        ...
    def getAlpha(self) -> float:
        """
            Get the calibration parameter for line search
        
            Returns:
                alpha
        
        
        """
        ...
    def getB(self) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Get the equalities constraints vector
        
            Returns:
                equalities constraints vector
        
        
        """
        ...
    def getBeta(self) -> float:
        """
            Get the calibration parameter for line search
        
            Returns:
                beta
        
        
        """
        ...
    def getF0(self) -> fr.cnes.sirius.patrius.math.optim.joptimizer.functions.ConvexMultivariateRealFunction:
        """
            Get the objective function to minimize
        
            Returns:
                objective function
        
        
        """
        ...
    def getFi(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.optim.joptimizer.functions.ConvexMultivariateRealFunction]:
        """
            Get the inequalities constraints array
        
            Returns:
                inequalities constraints array
        
        
        """
        ...
    def getInitialLagrangian(self) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Get a starting point for the Lagrangian multipliers
        
            Returns:
                initial point
        
        
        """
        ...
    def getInitialPoint(self) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Get the feasible starting point for the minimum search
        
            Returns:
                initial point
        
        
        """
        ...
    def getInteriorPointMethod(self) -> str:
        """
            Get the chosen interior-point method
        
            Returns:
                chosen interior-point method
        
        
        """
        ...
    def getMaxIteration(self) -> int:
        """
            Get the maximum number of iteration in the search algorithm.
        
            Returns:
                maximum number of iteration
        
        
        """
        ...
    def getMu(self) -> float:
        """
            Get the calibration parameter for line search
        
            Returns:
                mu
        
        
        """
        ...
    def getNotFeasibleInitialPoint(self) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Get a not-feasible starting point for the minimum search
        
            Returns:
                not-feasible initial point
        
        
        """
        ...
    def getTolerance(self) -> float:
        """
            Get the tolerance for the minimum value.
        
            Returns:
                tolerance
        
        
        """
        ...
    def getToleranceFeas(self) -> float:
        """
            Get the tolerance for the constraints satisfaction.
        
            Returns:
                tolerance
        
        
        """
        ...
    def getToleranceInnerStep(self) -> float:
        """
            Get the tolerance for inner iterations in the barrier-method.
        
            Returns:
                tolerance
        
        
        """
        ...
    def getToleranceKKT(self) -> float:
        """
            Get the acceptable tolerance for KKT system resolution
        
            Returns:
                tolerance
        
        
        """
        ...
    def isCheckKKTSolutionAccuracy(self) -> bool:
        """
            Check the accuracy of the solution of KKT system during iterations. If true, every inversion of the system must have an
            accuracy that satisfy the given toleranceKKT
        
            Returns:
                true/false
        
        
        """
        ...
    def isCheckProgressConditions(self) -> bool:
        """
            If true, a progress in the relevant algorithm norms is required during iterations, otherwise the iteration will be
            exited with a warning
        
            Returns:
                true/false
        
        
        """
        ...
    def isRescalingDisabled(self) -> bool:
        """
            Is the matrix rescaling disabled?
        
            Returns:
                true/false
        
        
        """
        ...
    @typing.overload
    def setA(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None:
        """
            Set the equalities constraints matrix
        
            Parameters:
                a (double[][]): equalities constraints double[][]
        
            Set the equalities constraints matrix
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): equalities constraints matrix
        
        
        """
        ...
    @typing.overload
    def setA(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> None: ...
    def setAlpha(self, double: float) -> None:
        """
            Set the calibration parameter for line search
        
            Parameters:
                a (double): calibration parameter
        
        
        """
        ...
    @typing.overload
    def setB(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set the equalities constraints vector
        
            Parameters:
                vecB (double[]): equalities constraints double[]
        
            Set the equalities constraints vector
        
            Parameters:
                vecB (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): equalities constraints vector
        
        
        """
        ...
    @typing.overload
    def setB(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def setBeta(self, double: float) -> None:
        """
            Set the calibration parameter for line search
        
            Parameters:
                be (double): calibration parameter
        
        
        """
        ...
    def setCheckKKTSolutionAccuracy(self, boolean: bool) -> None:
        """
            Set true if every inversion of the system must have an accuracy that satisfy the given toleranceKKT, false otherwise.
        
            Parameters:
                checkKKTSolutionAcc (boolean): true/false
        
        
        """
        ...
    def setCheckProgressConditions(self, boolean: bool) -> None:
        """
            Set true if a progress in the relevant algorithm norms is required during iterations, or false if the iteration will be
            exited with a warning
        
            Parameters:
                checkProgressCondition (boolean): true/false
        
        
        """
        ...
    def setF0(self, convexMultivariateRealFunction: fr.cnes.sirius.patrius.math.optim.joptimizer.functions.ConvexMultivariateRealFunction) -> None:
        """
            Set the objective function to minimize
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.ConvexMultivariateRealFunction`): objective function
        
        
        """
        ...
    def setFi(self, convexMultivariateRealFunctionArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.optim.joptimizer.functions.ConvexMultivariateRealFunction], jpype.JArray]) -> None:
        """
            Set the inequalities constraints array
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.functions.ConvexMultivariateRealFunction`[]): inequalities constraints array
        
        
        """
        ...
    def setInitialLagrangian(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set a starting point for the Lagrangian multipliers
        
            Parameters:
                initialL (double[]): initial point
        
        
        """
        ...
    def setInitialPoint(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set the feasible starting point for the minimum search
        
            Parameters:
                initialP (double[]): feasible starting point
        
        
        """
        ...
    def setInteriorPointMethod(self, string: str) -> None:
        """
            Set the chosen interior-point method
        
            Parameters:
                interiorPM (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): chosen interior-point method (string)
        
        
        """
        ...
    def setMaxIteration(self, int: int) -> None:
        """
            Set the maximum number of iteration in the search algorithm.
        
            Parameters:
                maxIterations (int): maximum number of iteration
        
        
        """
        ...
    def setMu(self, double: float) -> None:
        """
            Set the calibration parameter for line search
        
            Parameters:
                m (double): calibration parameter
        
        
        """
        ...
    def setNotFeasibleInitialPoint(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set a not-feasible starting point for the minimum search
        
            Parameters:
                notFeasibleInitialP (double[]): not-feasible initial point
        
        
        """
        ...
    def setRescalingDisabled(self, boolean: bool) -> None:
        """
            Set if the matrix rescaling should be disabled (true) or not (false) Rescaling is involved in LP presolving and in the
            solution of the KKT systems associated with the problem.
        
            Parameters:
                rescalingDis (boolean): true/false
        
        
        """
        ...
    def setTolerance(self, double: float) -> None:
        """
            Set the tolerance for the minimum value.
        
            Parameters:
                toleranceMV (double): tolerance
        
        
        """
        ...
    def setToleranceFeas(self, double: float) -> None:
        """
            Set the tolerance for the constraints satisfaction.
        
            Parameters:
                toleranceF (double): tolerance
        
        
        """
        ...
    def setToleranceInnerStep(self, double: float) -> None:
        """
            Set the tolerance for inner iterations in the barrier-method.
        
            Parameters:
                toleranceIS (double): tolerance
        
        
        """
        ...
    def setToleranceKKT(self, double: float) -> None:
        """
            Set the acceptable tolerance for KKT system resolution
        
            Parameters:
                toleranceK (double): tolerance
        
        
        """
        ...

class OptimizationRequestHandler:
    SCALAR: typing.ClassVar[float] = ...
    MAX_ITERATIONS: typing.ClassVar[float] = ...
    def getOptimizationResponse(self) -> 'OptimizationResponse': ...
    def optimize(self) -> int: ...
    def setOptimizationRequest(self, optimizationRequest: OptimizationRequest) -> None: ...

class OptimizationResponse:
    """
    public class OptimizationResponse extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Optimization process output: stores the solution as well as an exit code.
    
        Since:
            4.6
    """
    SUCCESS: typing.ClassVar[int] = ...
    """
    public static final int SUCCESS
    
        Succes variable
    
        Also see:
            :meth:`~constant`
    
    
    """
    WARN: typing.ClassVar[int] = ...
    """
    public static final int WARN
    
        Warn variable
    
        Also see:
            :meth:`~constant`
    
    
    """
    FAILED: typing.ClassVar[int] = ...
    """
    public static final int FAILED
    
        Failed variable
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def getMultiplicators(self) -> typing.MutableSequence[float]:
        """
            Returns the Lagrangian multipliers.
        
            Returns:
                the Lagrangian multipliers
        
        
        """
        ...
    def getReturnCode(self) -> int:
        """
            Get the return code
        
            Returns:
                0, 1 or 2
        
        
        """
        ...
    def getSolution(self) -> typing.MutableSequence[float]:
        """
            Get the solution
        
            Returns:
                solution
        
        
        """
        ...
    def setMultiplicators(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set the Lagrangian multipliers.
        
            Parameters:
                multiplicators (double[]): Lagrangian multipliers
        
        
        """
        ...
    def setReturnCode(self, int: int) -> None:
        """
            Set the return code (succes, warn or failed)
        
            Parameters:
                code (int): return code
        
        
        """
        ...
    def setSolution(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set the solution
        
            Parameters:
                sol (double[]): solution
        
        
        """
        ...

class AbstractLPOptimizationRequestHandler(OptimizationRequestHandler):
    """
    public abstract class AbstractLPOptimizationRequestHandler extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequestHandler`
    
        Class Linear Problem Optimization Request Handler.
    
        Since:
            4.6
    """
    def __init__(self): ...
    def getLPOptimizationResponse(self) -> 'LPOptimizationResponse':
        """
            Get the linear problem optimization response
        
            Returns:
                response
        
        
        """
        ...
    def setLPOptimizationRequest(self, lPOptimizationRequest: 'LPOptimizationRequest') -> None:
        """
            Set the linear problem optimization request
        
            Parameters:
                lpReq (:class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.LPOptimizationRequest`): request
        
        
        """
        ...
    def setOptimizationRequest(self, optimizationRequest: OptimizationRequest) -> None:
        """
            Set optimization request
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequestHandler.setOptimizationRequest` in
                class :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequestHandler`
        
            Parameters:
                request (:class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequest`): 
        
        """
        ...

class BarrierMethod(OptimizationRequestHandler):
    """
    public class BarrierMethod extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequestHandler`
    
        Barrier method.
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, p. 568"
    """
    def __init__(self, barrierFunction: fr.cnes.sirius.patrius.math.optim.joptimizer.functions.BarrierFunction): ...
    def getHessFi(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.linear.RealMatrix]:
        """
            Use the barrier function instead.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequestHandler.getHessFi` in
                class :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequestHandler`
        
            Parameters:
                x (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): hessians X
        
            Returns:
                inequality function
        
        
        """
        ...
    def optimize(self) -> int: ...

class LPOptimizationRequest(OptimizationRequest):
    def __init__(self): ...
    def cloneMe(self) -> 'LPOptimizationRequest': ...
    def getC(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getG(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def getH(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getLb(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getUb(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getYlb(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getYub(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getZlb(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def getZub(self) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    def isAvoidPresolvingFillIn(self) -> bool: ...
    def isAvoidPresolvingIncreaseSparsity(self) -> bool: ...
    def isCheckOptimalLagrangianBounds(self) -> bool: ...
    def isPresolvingDisabled(self) -> bool: ...
    def setAvoidPresolvingFillIn(self, boolean: bool) -> None: ...
    def setAvoidPresolvingIncreaseSparsity(self, boolean: bool) -> None: ...
    @typing.overload
    def setC(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    def setC(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def setCheckOptimalLagrangianBounds(self, boolean: bool) -> None: ...
    def setF0(self, convexMultivariateRealFunction: fr.cnes.sirius.patrius.math.optim.joptimizer.functions.ConvexMultivariateRealFunction) -> None: ...
    def setFi(self, convexMultivariateRealFunctionArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.optim.joptimizer.functions.ConvexMultivariateRealFunction], jpype.JArray]) -> None: ...
    @typing.overload
    def setG(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    @typing.overload
    def setG(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> None: ...
    @typing.overload
    def setH(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    def setH(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    @typing.overload
    def setLb(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    def setLb(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def setPresolvingDisabled(self, boolean: bool) -> None: ...
    @typing.overload
    def setUb(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    def setUb(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def setYlb(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def setYub(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def setZlb(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def setZub(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def toString(self) -> str: ...

class LPOptimizationResponse(OptimizationResponse):
    """
    public class LPOptimizationResponse extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationResponse`
    
    
        Since:
            4.6
    """
    def __init__(self): ...

class NewtonLEConstrainedFSP(OptimizationRequestHandler):
    """
    public class NewtonLEConstrainedFSP extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequestHandler`
    
        Linear equality constrained newton optimizer, with feasible starting point.
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, p. 521"
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...
    def optimize(self) -> int: ...
    def setKKTSolver(self, abstractKKTSolver: fr.cnes.sirius.patrius.math.optim.joptimizer.solvers.AbstractKKTSolver) -> None:
        """
            Set the ktt solver
        
            Parameters:
                kktSol (:class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.solvers.AbstractKKTSolver`): ktt solver
        
        
        """
        ...

class NewtonLEConstrainedISP(OptimizationRequestHandler):
    """
    public class NewtonLEConstrainedISP extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequestHandler`
    
        Linear equality constrained newton optimizer, with infeasible starting point.
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, p. 521"
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...
    def optimize(self) -> int: ...
    def setKKTSolver(self, abstractKKTSolver: fr.cnes.sirius.patrius.math.optim.joptimizer.solvers.AbstractKKTSolver) -> None:
        """
            Set the ktt solver
        
            Parameters:
                kktSol (:class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.solvers.AbstractKKTSolver`): solver
        
        
        """
        ...

class NewtonUnconstrained(OptimizationRequestHandler):
    """
    public class NewtonUnconstrained extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequestHandler`
    
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, p. 487"
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...
    def optimize(self) -> int: ...

class PrimalDualMethod(OptimizationRequestHandler):
    """
    public class PrimalDualMethod extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.OptimizationRequestHandler`
    
        Primal-dual interior-point method.
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, p. 609"
    """
    def __init__(self): ...
    def optimize(self) -> int: ...

class LPPrimalDualMethod(AbstractLPOptimizationRequestHandler):
    DEFAULT_MIN_LOWER_BOUND: typing.ClassVar[float] = ...
    DEFAULT_MAX_UPPER_BOUND: typing.ClassVar[float] = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    def getHessFi(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.linear.RealMatrix]: ...
    def optimize(self) -> int: ...
    def setKKTSolver(self, abstractKKTSolver: fr.cnes.sirius.patrius.math.optim.joptimizer.solvers.AbstractKKTSolver) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers")``.

    AbstractLPOptimizationRequestHandler: typing.Type[AbstractLPOptimizationRequestHandler]
    BarrierMethod: typing.Type[BarrierMethod]
    BasicPhaseIBM: typing.Type[BasicPhaseIBM]
    BasicPhaseILPPDM: typing.Type[BasicPhaseILPPDM]
    BasicPhaseIPDM: typing.Type[BasicPhaseIPDM]
    JOptimizer: typing.Type[JOptimizer]
    LPOptimizationRequest: typing.Type[LPOptimizationRequest]
    LPOptimizationResponse: typing.Type[LPOptimizationResponse]
    LPPresolver: typing.Type[LPPresolver]
    LPPrimalDualMethod: typing.Type[LPPrimalDualMethod]
    LPStandardConverter: typing.Type[LPStandardConverter]
    NewtonLEConstrainedFSP: typing.Type[NewtonLEConstrainedFSP]
    NewtonLEConstrainedISP: typing.Type[NewtonLEConstrainedISP]
    NewtonUnconstrained: typing.Type[NewtonUnconstrained]
    OptimizationRequest: typing.Type[OptimizationRequest]
    OptimizationRequestHandler: typing.Type[OptimizationRequestHandler]
    OptimizationResponse: typing.Type[OptimizationResponse]
    PrimalDualMethod: typing.Type[PrimalDualMethod]
