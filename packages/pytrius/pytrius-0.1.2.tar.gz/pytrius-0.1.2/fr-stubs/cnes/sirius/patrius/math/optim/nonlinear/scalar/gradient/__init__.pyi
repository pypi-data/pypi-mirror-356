
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis.solver
import fr.cnes.sirius.patrius.math.optim
import fr.cnes.sirius.patrius.math.optim.nonlinear.scalar
import java.lang
import jpype
import typing



class Preconditioner:
    """
    public interface Preconditioner
    
        This interface represents a preconditioner for differentiable scalar objective function optimizers.
    
        Since:
            2.0
    """
    def precondition(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Precondition a search direction.
        
            The returned preconditioned search direction must be computed fast or the algorithm performances will drop drastically.
            A classical approach is to compute only the diagonal elements of the hessian and to divide the raw search direction by
            these elements if they are all positive. If at least one of them is negative, it is safer to return a clone of the raw
            search direction as if the hessian was the identity matrix. The rationale for this simplified choice is that a negative
            diagonal element means the current point is far from the optimum and preconditioning will not be efficient anyway in
            this case.
        
            Parameters:
                point (double[]): current point at which the search direction was computed
                r (double[]): raw search direction (i.e. opposite of the gradient)
        
            Returns:
                approximation of H :sup:`-1` r where H is the objective function hessian
        
        
        """
        ...

class NonLinearConjugateGradientOptimizer(fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.GradientMultivariateOptimizer):
    @typing.overload
    def __init__(self, formula: 'NonLinearConjugateGradientOptimizer.Formula', convergenceChecker: typing.Union[fr.cnes.sirius.patrius.math.optim.ConvergenceChecker[fr.cnes.sirius.patrius.math.optim.PointValuePair], typing.Callable[[int, fr.cnes.sirius.patrius.math.optim.PointValuePair, fr.cnes.sirius.patrius.math.optim.PointValuePair], bool]]): ...
    @typing.overload
    def __init__(self, formula: 'NonLinearConjugateGradientOptimizer.Formula', convergenceChecker: typing.Union[fr.cnes.sirius.patrius.math.optim.ConvergenceChecker[fr.cnes.sirius.patrius.math.optim.PointValuePair], typing.Callable[[int, fr.cnes.sirius.patrius.math.optim.PointValuePair, fr.cnes.sirius.patrius.math.optim.PointValuePair], bool]], univariateSolver: fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver): ...
    @typing.overload
    def __init__(self, formula: 'NonLinearConjugateGradientOptimizer.Formula', convergenceChecker: typing.Union[fr.cnes.sirius.patrius.math.optim.ConvergenceChecker[fr.cnes.sirius.patrius.math.optim.PointValuePair], typing.Callable[[int, fr.cnes.sirius.patrius.math.optim.PointValuePair, fr.cnes.sirius.patrius.math.optim.PointValuePair], bool]], univariateSolver: fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver, preconditioner: typing.Union[Preconditioner, typing.Callable]): ...
    def optimize(self, *optimizationData: fr.cnes.sirius.patrius.math.optim.OptimizationData) -> fr.cnes.sirius.patrius.math.optim.PointValuePair: ...
    class BracketingStep(fr.cnes.sirius.patrius.math.optim.OptimizationData):
        def __init__(self, double: float): ...
        def getBracketingStep(self) -> float: ...
    class Formula(java.lang.Enum['NonLinearConjugateGradientOptimizer.Formula']):
        FLETCHER_REEVES: typing.ClassVar['NonLinearConjugateGradientOptimizer.Formula'] = ...
        POLAK_RIBIERE: typing.ClassVar['NonLinearConjugateGradientOptimizer.Formula'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'NonLinearConjugateGradientOptimizer.Formula': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['NonLinearConjugateGradientOptimizer.Formula']: ...
    class IdentityPreconditioner(Preconditioner):
        def __init__(self): ...
        def precondition(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.gradient")``.

    NonLinearConjugateGradientOptimizer: typing.Type[NonLinearConjugateGradientOptimizer]
    Preconditioner: typing.Type[Preconditioner]
