
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.linear
import typing



class AbstractKKTSolver:
    DEFAULT_SCALAR: typing.ClassVar[float] = ...
    def __init__(self): ...
    def setAMatrix(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> None: ...
    def setCheckKKTSolutionAccuracy(self, boolean: bool) -> None: ...
    def setGVector(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def setHMatrix(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> None: ...
    def setHVector(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def setToleranceKKT(self, double: float) -> None: ...
    def solve(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.linear.RealVector]: ...

class AugmentedKKTSolver(AbstractKKTSolver):
    """
    public class AugmentedKKTSolver extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.solvers.AbstractKKTSolver`
    
        Solves the KKT system H.v + [A]T.w = -g,
    
    
        A.v = -h with singular H. The KKT matrix is nonsingular if and only if H + ATQA > 0 for some Q > 0, 0, in which case, H
        + ATQA > 0 for all Q > 0. This class uses the diagonal matrix Q = s.Id with scalar s > 0 to try finding the solution.
        NOTE: matrix A can not be null for this solver
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, p. 547"
    """
    def __init__(self): ...
    def setS(self, double: float) -> None:
        """
            Set a value to s
        
            Parameters:
                constant (double): value to assign to the variable s
        
        
        """
        ...
    def solve(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.linear.RealVector]: ...

class BasicKKTSolver(AbstractKKTSolver):
    """
    public final class BasicKKTSolver extends :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.solvers.AbstractKKTSolver`
    
        H.v + [A]T.w = -g,
    
    
        A.v = -h
    
        Since:
            4.6
    
        Also see:
            "S.Boyd and L.Vandenberghe, Convex Optimization, p. 542"
    """
    def __init__(self): ...
    def solve(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.linear.RealVector]: ...

class UpperDiagonalHKKTSolver(AbstractKKTSolver):
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, boolean: bool): ...
    def getDiagonalLength(self) -> int: ...
    def setDiagonalLength(self, int: int) -> None: ...
    def solve(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.linear.RealVector]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.joptimizer.solvers")``.

    AbstractKKTSolver: typing.Type[AbstractKKTSolver]
    AugmentedKKTSolver: typing.Type[AugmentedKKTSolver]
    BasicKKTSolver: typing.Type[BasicKKTSolver]
    UpperDiagonalHKKTSolver: typing.Type[UpperDiagonalHKKTSolver]
