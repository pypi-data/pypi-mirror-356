
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.optim
import fr.cnes.sirius.patrius.math.optim.nonlinear.vector
import jpype
import typing



class AbstractLeastSquaresOptimizer(fr.cnes.sirius.patrius.math.optim.nonlinear.vector.JacobianMultivariateVectorOptimizer):
    def computeCovariances(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computeSigma(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> typing.MutableSequence[float]: ...
    def getChiSquare(self) -> float: ...
    def getRMS(self) -> float: ...
    def getWeightSquareRoot(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def optimize(self, *optimizationData: fr.cnes.sirius.patrius.math.optim.OptimizationData) -> fr.cnes.sirius.patrius.math.optim.PointVectorValuePair: ...

class GaussNewtonOptimizer(AbstractLeastSquaresOptimizer):
    """
    public class GaussNewtonOptimizer extends :class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.vector.jacobian.AbstractLeastSquaresOptimizer`
    
        Gauss-Newton least-squares solver.
    
        This class solve a least-square problem by solving the normal equations of the linearized problem at each iteration.
        Either LU decomposition or QR decomposition can be used to solve the normal equations. LU decomposition is faster but QR
        decomposition is more robust for difficult problems.
    
        Since:
            2.0
    """
    @typing.overload
    def __init__(self, boolean: bool, convergenceChecker: typing.Union[fr.cnes.sirius.patrius.math.optim.ConvergenceChecker[fr.cnes.sirius.patrius.math.optim.PointVectorValuePair], typing.Callable[[int, fr.cnes.sirius.patrius.math.optim.PointVectorValuePair, fr.cnes.sirius.patrius.math.optim.PointVectorValuePair], bool]]): ...
    @typing.overload
    def __init__(self, convergenceChecker: typing.Union[fr.cnes.sirius.patrius.math.optim.ConvergenceChecker[fr.cnes.sirius.patrius.math.optim.PointVectorValuePair], typing.Callable[[int, fr.cnes.sirius.patrius.math.optim.PointVectorValuePair, fr.cnes.sirius.patrius.math.optim.PointVectorValuePair], bool]]): ...
    def doOptimize(self) -> fr.cnes.sirius.patrius.math.optim.PointVectorValuePair:
        """
            Performs the bulk of the optimization algorithm.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.optim.BaseOptimizer.doOptimize` in
                class :class:`~fr.cnes.sirius.patrius.math.optim.BaseOptimizer`
        
            Returns:
                the point/value pair giving the optimal value of the objective function.
        
        
        """
        ...

class LevenbergMarquardtOptimizer(AbstractLeastSquaresOptimizer):
    """
    public class LevenbergMarquardtOptimizer extends :class:`~fr.cnes.sirius.patrius.math.optim.nonlinear.vector.jacobian.AbstractLeastSquaresOptimizer`
    
        This class solves a least-squares problem using the Levenberg-Marquardt algorithm.
    
        This implementation *should* work even for over-determined systems (i.e. systems having more point than equations).
        Over-determined systems are solved by ignoring the point which have the smallest impact according to their jacobian
        column norm. Only the rank of the matrix and some loop bounds are changed to implement this.
    
        The resolution engine is a simple translation of the MINPACK `lmder <http://www.netlib.org/minpack/lmder.f>` routine
        with minor changes. The changes include the over-determined resolution, the use of inherited convergence checker and the
        Q.R. decomposition which has been rewritten following the algorithm described in the P. Lascaux and R. Theodor book
        *Analyse numérique matricielle appliquée à l'art de l'ingénieur*, Masson 1986.
    
        The authors of the original fortran version are:
    
          - Argonne National Laboratory. MINPACK project. March 1980
          - Burton S. Garbow
          - Kenneth E. Hillstrom
          - Jorge J. More
    
        The redistribution policy for MINPACK is available `here <http://www.netlib.org/minpack/disclaimer>`, for convenience,
        it is reproduced below.
    
        Since:
            2.0
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float): ...
    @typing.overload
    def __init__(self, double: float, convergenceChecker: typing.Union[fr.cnes.sirius.patrius.math.optim.ConvergenceChecker[fr.cnes.sirius.patrius.math.optim.PointVectorValuePair], typing.Callable[[int, fr.cnes.sirius.patrius.math.optim.PointVectorValuePair, fr.cnes.sirius.patrius.math.optim.PointVectorValuePair], bool]], double2: float, double3: float, double4: float, double5: float): ...
    @typing.overload
    def __init__(self, convergenceChecker: typing.Union[fr.cnes.sirius.patrius.math.optim.ConvergenceChecker[fr.cnes.sirius.patrius.math.optim.PointVectorValuePair], typing.Callable[[int, fr.cnes.sirius.patrius.math.optim.PointVectorValuePair, fr.cnes.sirius.patrius.math.optim.PointVectorValuePair], bool]]): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.nonlinear.vector.jacobian")``.

    AbstractLeastSquaresOptimizer: typing.Type[AbstractLeastSquaresOptimizer]
    GaussNewtonOptimizer: typing.Type[GaussNewtonOptimizer]
    LevenbergMarquardtOptimizer: typing.Type[LevenbergMarquardtOptimizer]
