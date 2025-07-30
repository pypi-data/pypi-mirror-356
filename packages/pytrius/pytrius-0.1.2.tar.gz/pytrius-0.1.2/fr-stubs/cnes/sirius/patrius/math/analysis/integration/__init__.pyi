
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.analysis.integration.bivariate
import fr.cnes.sirius.patrius.math.analysis.integration.gauss
import fr.cnes.sirius.patrius.math.analysis.integration.sphere
import java.io
import java.util
import typing



class UnivariateIntegrator(java.io.Serializable):
    """
    public interface UnivariateIntegrator extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for univariate real integration algorithms.
    
        Since:
            1.2
    """
    def getAbsoluteAccuracy(self) -> float:
        """
            Get the actual absolute accuracy.
        
            Returns:
                the accuracy
        
        
        """
        ...
    def getEvaluations(self) -> int:
        """
            Get the number of function evaluations of the last run of the integrator.
        
            Returns:
                number of function evaluations
        
        
        """
        ...
    def getIterations(self) -> int:
        """
            Get the number of iterations of the last run of the integrator.
        
            Returns:
                number of iterations
        
        
        """
        ...
    def getMaximalIterationCount(self) -> int:
        """
            Get the upper limit for the number of iterations.
        
            Returns:
                the actual upper limit
        
        
        """
        ...
    def getMinimalIterationCount(self) -> int:
        """
            Get the min limit for the number of iterations.
        
            Returns:
                the actual min limit
        
        
        """
        ...
    def getRelativeAccuracy(self) -> float:
        """
            Get the actual relative accuracy.
        
            Returns:
                the accuracy
        
        
        """
        ...
    def integrate(self, int: int, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float) -> float:
        """
            Integrate the function in the given interval.
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): the integrand function
                min (double): the min bound for the interval
                max (double): the upper bound for the interval
        
            Returns:
                the value of integral
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the maximum number of function evaluations is exceeded.
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the maximum iteration count is exceeded or the integrator detects convergence problems otherwise
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if min > max or the endpoints do not satisfy the requirements specified by the integrator
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`f` is :code:`null`.
        
        
        """
        ...

class BaseAbstractUnivariateIntegrator(UnivariateIntegrator):
    """
    public abstract class BaseAbstractUnivariateIntegrator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator`
    
        Provide a default implementation for several generic functions.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_ABSOLUTE_ACCURACY: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_ABSOLUTE_ACCURACY
    
        Default absolute accuracy.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_RELATIVE_ACCURACY: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_RELATIVE_ACCURACY
    
        Default relative accuracy.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_MIN_ITERATIONS_COUNT: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_MIN_ITERATIONS_COUNT
    
        Default minimal iteration count.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_MAX_ITERATIONS_COUNT: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_MAX_ITERATIONS_COUNT
    
        Default maximal iteration count.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def getAbsoluteAccuracy(self) -> float:
        """
            Get the actual absolute accuracy.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator.getAbsoluteAccuracy` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator`
        
            Returns:
                the accuracy
        
        
        """
        ...
    def getEvaluations(self) -> int:
        """
            Get the number of function evaluations of the last run of the integrator.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator.getEvaluations` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator`
        
            Returns:
                number of function evaluations
        
        
        """
        ...
    def getIterations(self) -> int:
        """
            Get the number of iterations of the last run of the integrator.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator.getIterations` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator`
        
            Returns:
                number of iterations
        
        
        """
        ...
    def getMaximalIterationCount(self) -> int:
        """
            Get the upper limit for the number of iterations.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator.getMaximalIterationCount` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator`
        
            Returns:
                the actual upper limit
        
        
        """
        ...
    def getMinimalIterationCount(self) -> int:
        """
            Get the min limit for the number of iterations.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator.getMinimalIterationCount` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator`
        
            Returns:
                the actual min limit
        
        
        """
        ...
    def getRelativeAccuracy(self) -> float:
        """
            Get the actual relative accuracy.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator.getRelativeAccuracy` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator`
        
            Returns:
                the accuracy
        
        
        """
        ...
    def integrate(self, int: int, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float) -> float:
        """
            Integrate the function in the given interval.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator.integrate` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator`
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): the integrand function
                lower (double): the min bound for the interval
                upper (double): the upper bound for the interval
        
            Returns:
                the value of integral
        
        
        """
        ...

class AdaptiveSimpsonIntegrator(BaseAbstractUnivariateIntegrator):
    """
    public class AdaptiveSimpsonIntegrator extends :class:`~fr.cnes.sirius.patrius.math.analysis.integration.BaseAbstractUnivariateIntegrator`
    
        Implements ` Simpson's Rule <http://mathworld.wolfram.com/SimpsonsRule.html>` for the integration of real univariate
        functions.
    
        This method splits the integration interval into two equal parts and computes the value of the integral on each of these
        parts using a 3 point Simpson's rule. The same method is then applied again on each sub-interval, until the required
        accuracy is reached or the maximal number of iterations is reached.
    
        For reference, see **Introduction to Numerical Analysis**, ISBN 038795452X, chapter 3.
    
        Also see:
            :meth:`~serialized`
    """
    MAX_ITERATIONS_COUNT: typing.ClassVar[int] = ...
    """
    public static final int MAX_ITERATIONS_COUNT
    
        Maximal number of iterations allowed for this method.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float, int: int, int2: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...

class FixedStepSimpsonIntegrator(BaseAbstractUnivariateIntegrator):
    """
    public class FixedStepSimpsonIntegrator extends :class:`~fr.cnes.sirius.patrius.math.analysis.integration.BaseAbstractUnivariateIntegrator`
    
        Implements ` Simpson's Rule <http://mathworld.wolfram.com/SimpsonsRule.html>` for integration of real univariate
        functions. This integrator uses a fixed step to perform integration unlike
        :class:`~fr.cnes.sirius.patrius.math.analysis.integration.SimpsonIntegrator`.
    
        Since:
            4.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int): ...
    def getCumulatedIntegration(self) -> java.util.List[float]: ...

class IterativeLegendreGaussIntegrator(BaseAbstractUnivariateIntegrator):
    """
    public class IterativeLegendreGaussIntegrator extends :class:`~fr.cnes.sirius.patrius.math.analysis.integration.BaseAbstractUnivariateIntegrator`
    
        This algorithm divides the integration interval into equally-sized sub-interval and on each of them performs a `
        Legendre-Gauss <http://mathworld.wolfram.com/Legendre-GaussQuadrature.html>` quadrature.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, int: int, double: float, double2: float): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, int2: int, int3: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int, int3: int): ...

class RombergIntegrator(BaseAbstractUnivariateIntegrator):
    """
    public class RombergIntegrator extends :class:`~fr.cnes.sirius.patrius.math.analysis.integration.BaseAbstractUnivariateIntegrator`
    
        Implements the ` Romberg Algorithm <http://mathworld.wolfram.com/RombergIntegration.html>` for integration of real
        univariate functions. For reference, see **Introduction to Numerical Analysis**, ISBN 038795452X, chapter 3.
    
        Romberg integration employs k successive refinements of the trapezoid rule to remove error terms less than order
        O(N^(-2k)). Simpson's rule is a special case of k = 2.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    ROMBERG_MAX_ITERATIONS_COUNT: typing.ClassVar[int] = ...
    """
    public static final int ROMBERG_MAX_ITERATIONS_COUNT
    
        Maximal number of iterations for Romberg.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float, int: int, int2: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...

class SimpsonIntegrator(BaseAbstractUnivariateIntegrator):
    """
    public class SimpsonIntegrator extends :class:`~fr.cnes.sirius.patrius.math.analysis.integration.BaseAbstractUnivariateIntegrator`
    
        Implements ` Simpson's Rule <http://mathworld.wolfram.com/SimpsonsRule.html>` for integration of real univariate
        functions. For reference, see **Introduction to Numerical Analysis**, ISBN 038795452X, chapter 3.
    
        This implementation employs the basic trapezoid rule to calculate Simpson's rule.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    SIMPSON_MAX_ITERATIONS_COUNT: typing.ClassVar[int] = ...
    """
    public static final int SIMPSON_MAX_ITERATIONS_COUNT
    
        Maximal number of iterations for Simpson.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float, int: int, int2: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...

class TrapezoidIntegrator(BaseAbstractUnivariateIntegrator):
    """
    public class TrapezoidIntegrator extends :class:`~fr.cnes.sirius.patrius.math.analysis.integration.BaseAbstractUnivariateIntegrator`
    
        Implements the ` Trapezoid Rule <http://mathworld.wolfram.com/TrapezoidalRule.html>` for integration of real univariate
        functions. For reference, see **Introduction to Numerical Analysis**, ISBN 038795452X, chapter 3.
    
        The function should be integrable.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    TRAPEZOID_MAX_ITERATIONS_COUNT: typing.ClassVar[int] = ...
    """
    public static final int TRAPEZOID_MAX_ITERATIONS_COUNT
    
        Maximum number of iterations for trapezoid.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float, int: int, int2: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    def stage(self, baseAbstractUnivariateIntegrator: BaseAbstractUnivariateIntegrator, int: int) -> float:
        """
            Compute the n-th stage integral of trapezoid rule. This function should only be called by API :code:`integrate()` in the
            package. To save time it does not verify arguments - caller does.
        
            The interval is divided equally into 2^n sections rather than an arbitrary m sections because this configuration can
            best utilize the already computed values.
        
            Parameters:
                baseIntegrator (:class:`~fr.cnes.sirius.patrius.math.analysis.integration.BaseAbstractUnivariateIntegrator`): integrator holding integration parameters
                n (int): the stage of 1/2 refinement, n = 0 is no refinement
        
            Returns:
                the value of n-th stage integral
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the maximal number of evaluations is exceeded.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.analysis.integration")``.

    AdaptiveSimpsonIntegrator: typing.Type[AdaptiveSimpsonIntegrator]
    BaseAbstractUnivariateIntegrator: typing.Type[BaseAbstractUnivariateIntegrator]
    FixedStepSimpsonIntegrator: typing.Type[FixedStepSimpsonIntegrator]
    IterativeLegendreGaussIntegrator: typing.Type[IterativeLegendreGaussIntegrator]
    RombergIntegrator: typing.Type[RombergIntegrator]
    SimpsonIntegrator: typing.Type[SimpsonIntegrator]
    TrapezoidIntegrator: typing.Type[TrapezoidIntegrator]
    UnivariateIntegrator: typing.Type[UnivariateIntegrator]
    bivariate: fr.cnes.sirius.patrius.math.analysis.integration.bivariate.__module_protocol__
    gauss: fr.cnes.sirius.patrius.math.analysis.integration.gauss.__module_protocol__
    sphere: fr.cnes.sirius.patrius.math.analysis.integration.sphere.__module_protocol__
