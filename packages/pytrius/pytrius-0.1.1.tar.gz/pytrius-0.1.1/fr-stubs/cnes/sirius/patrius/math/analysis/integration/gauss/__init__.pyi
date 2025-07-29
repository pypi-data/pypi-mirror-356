
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.util
import java.lang
import java.math
import jpype
import typing



_BaseRuleFactory__T = typing.TypeVar('_BaseRuleFactory__T', bound=java.lang.Number)  # <T>
class BaseRuleFactory(typing.Generic[_BaseRuleFactory__T]):
    """
    public abstract class BaseRuleFactory<T extends `Number <http://docs.oracle.com/javase/8/docs/api/java/lang/Number.html?is-external=true>`> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Base class for rules that determines the integration nodes and their weights. Subclasses must implement the
        :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.gauss.BaseRuleFactory.computeRule` method.
    
        Since:
            3.1
    """
    def __init__(self): ...
    def getRule(self, int: int) -> fr.cnes.sirius.patrius.math.util.Pair[typing.MutableSequence[float], typing.MutableSequence[float]]:
        """
            Gets a copy of the quadrature rule with the given number of integration points.
        
            Parameters:
                numberOfPoints (int): Number of integration points.
        
            Returns:
                a copy of the integration rule.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NotStrictlyPositiveException`: if :code:`numberOfPoints < 1`.
        
        
        """
        ...

class GaussIntegrator:
    """
    public class GaussIntegrator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class that implements the Gaussian rule for
        :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.gauss.GaussIntegrator.integrate` a weighted function.
    
        Since:
            3.1
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, pair: fr.cnes.sirius.patrius.math.util.Pair[typing.Union[typing.List[float], jpype.JArray], typing.Union[typing.List[float], jpype.JArray]]): ...
    def getNumberOfPoints(self) -> int:
        """
        
            Returns:
                the order of the integration rule (the number of integration points).
        
        
        """
        ...
    def integrate(self, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable]) -> float:
        """
            Returns an estimate of the integral of :code:`f(x) * w(x)`, where :code:`w` is a weight function that depends on the
            actual flavor of the Gauss integration scheme. The algorithm uses the points and associated weights, as passed to the
            null.
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Function to integrate.
        
            Returns:
                the integral of the weighted function.
        
        
        """
        ...

class GaussIntegratorFactory:
    """
    public class GaussIntegratorFactory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class that provides different ways to compute the nodes and weights to be used by the
        :class:`~fr.cnes.sirius.patrius.math.analysis.integration.gauss.GaussIntegrator`.
    
        Since:
            3.1
    """
    def __init__(self): ...
    @typing.overload
    def legendre(self, int: int) -> GaussIntegrator:
        """
            Creates an integrator of the given order, and whose call to the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.gauss.GaussIntegrator.integrate` method will perform an
            integration on the natural interval :code:`[-1 , 1]`.
        
            Parameters:
                numberOfPoints (int): Order of the integration rule.
        
            Returns:
                a Gauss-Legendre integrator.
        
            Creates an integrator of the given order, and whose call to the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.gauss.GaussIntegrator.integrate` method will perform an
            integration on the given interval.
        
            Parameters:
                numberOfPoints (int): Order of the integration rule.
                lowerBound (double): Lower bound of the integration interval.
                upperBound (double): Upper bound of the integration interval.
        
            Returns:
                a Gauss-Legendre integrator.
        
        
        """
        ...
    @typing.overload
    def legendre(self, int: int, double: float, double2: float) -> GaussIntegrator: ...
    @typing.overload
    def legendreHighPrecision(self, int: int) -> GaussIntegrator:
        """
            Creates an integrator of the given order, and whose call to the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.gauss.GaussIntegrator.integrate` method will perform an
            integration on the natural interval :code:`[-1 , 1]`.
        
            Parameters:
                numberOfPoints (int): Order of the integration rule.
        
            Returns:
                a Gauss-Legendre integrator.
        
            Creates an integrator of the given order, and whose call to the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.gauss.GaussIntegrator.integrate` method will perform an
            integration on the given interval.
        
            Parameters:
                numberOfPoints (int): Order of the integration rule.
                lowerBound (double): Lower bound of the integration interval.
                upperBound (double): Upper bound of the integration interval.
        
            Returns:
                a Gauss-Legendre integrator.
        
        
        """
        ...
    @typing.overload
    def legendreHighPrecision(self, int: int, double: float, double2: float) -> GaussIntegrator: ...

class LegendreHighPrecisionRuleFactory(BaseRuleFactory[java.math.BigDecimal]):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, mathContext: java.math.MathContext): ...

class LegendreRuleFactory(BaseRuleFactory[float]):
    def __init__(self): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.analysis.integration.gauss")``.

    BaseRuleFactory: typing.Type[BaseRuleFactory]
    GaussIntegrator: typing.Type[GaussIntegrator]
    GaussIntegratorFactory: typing.Type[GaussIntegratorFactory]
    LegendreHighPrecisionRuleFactory: typing.Type[LegendreHighPrecisionRuleFactory]
    LegendreRuleFactory: typing.Type[LegendreRuleFactory]
