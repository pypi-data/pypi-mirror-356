
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.analysis.integration
import typing



class BivariateIntegrator:
    """
    public interface BivariateIntegrator
    
        Interface for bivariate real integration algorithms.
    
        Since:
            4.1
    """
    def getEvaluations(self) -> int:
        """
            Returns the number of function evaluations made during the last run of the integrator.
        
            Returns:
                the number of function evaluations
        
        
        """
        ...
    def getFunction(self) -> fr.cnes.sirius.patrius.math.analysis.BivariateFunction:
        """
            Returns the function used during the last run of the integrator.
        
            Returns:
                the last function integrated
        
        
        """
        ...
    def getMaxEvaluations(self) -> int:
        """
            Returns the maximal number of function evaluations authorized during the last run of the integrator.
        
            Returns:
                the maximal number of function evaluations
        
        
        """
        ...
    def getXMax(self) -> float:
        """
            Returns the upper bounds on x used during the last call to this integrator.
        
            Returns:
                the dimension of the integration domain
        
        
        """
        ...
    def getXMin(self) -> float:
        """
            Returns the lower bounds on x used during the last call to this integrator.
        
            Returns:
                the dimension of the integration domain
        
        
        """
        ...
    def getYMax(self) -> float:
        """
            Returns the upper bounds on y used during the last call to this integrator.
        
            Returns:
                the dimension of the integration domain
        
        
        """
        ...
    def getYMin(self) -> float:
        """
            Returns the lower bounds on y used during the last call to this integrator.
        
            Returns:
                the dimension of the integration domain
        
        
        """
        ...
    def integrate(self, int: int, bivariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.BivariateFunction, typing.Callable], double: float, double2: float, double3: float, double4: float) -> float:
        """
            Integrates the function on the specified domain.
        
            Parameters:
                maxEval (int): the maximum number of evaluations
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`): the integrand function
                xmin (double): the lower bound of the interval for the 1st axis
                xmax (double): the upper bound of the interval for the 1st axis
                ymin (double): the lower bound of the interval for the 2nd axis
                ymax (double): the upper bound of the interval for the 2nd axis
        
            Returns:
                the value of integral
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the maximum number of function evaluations is exceeded
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the maximum iteration count is exceeded or a convergence problem is detected
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if min > max or the endpoints do not satisfy the requirements specified by the integrator
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`f` is :code:`null`.
        
        
        """
        ...

class DelegatedBivariateIntegrator(BivariateIntegrator):
    """
    public class DelegatedBivariateIntegrator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator`
    
        Bivariate integrator based on two univariate integrators.
    
        Since:
            4.1
    """
    def __init__(self, univariateIntegrator: fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator, univariateIntegrator2: fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator): ...
    def getEvaluations(self) -> int:
        """
            Returns the number of function evaluations made during the last run of the integrator.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator.getEvaluations` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator`
        
            Returns:
                the number of function evaluations
        
        
        """
        ...
    def getFunction(self) -> fr.cnes.sirius.patrius.math.analysis.BivariateFunction:
        """
            Returns the function used during the last run of the integrator.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator.getFunction` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator`
        
            Returns:
                the last function integrated
        
        
        """
        ...
    def getIntegratorX(self) -> fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator:
        """
            Gets the univariate integrator associated to the 1st axis.
        
            Returns:
                the univariate integrator associated to the 1st axis
        
        
        """
        ...
    def getIntegratorY(self) -> fr.cnes.sirius.patrius.math.analysis.integration.UnivariateIntegrator:
        """
            Gets the univariate integrator associated to the 2nd axis.
        
            Returns:
                the univariate integrator associated to the 2nd axis
        
        
        """
        ...
    def getMaxEvaluations(self) -> int:
        """
            Returns the maximal number of function evaluations authorized during the last run of the integrator.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator.getMaxEvaluations` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator`
        
            Returns:
                the maximal number of function evaluations
        
        
        """
        ...
    def getXMax(self) -> float:
        """
            Returns the upper bounds on x used during the last call to this integrator.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator.getXMax` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator`
        
            Returns:
                the dimension of the integration domain
        
        
        """
        ...
    def getXMin(self) -> float:
        """
            Returns the lower bounds on x used during the last call to this integrator.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator.getXMin` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator`
        
            Returns:
                the dimension of the integration domain
        
        
        """
        ...
    def getYMax(self) -> float:
        """
            Returns the upper bounds on y used during the last call to this integrator.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator.getYMax` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator`
        
            Returns:
                the dimension of the integration domain
        
        
        """
        ...
    def getYMin(self) -> float:
        """
            Returns the lower bounds on y used during the last call to this integrator.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator.getYMin` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator`
        
            Returns:
                the dimension of the integration domain
        
        
        """
        ...
    def integrate(self, int: int, bivariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.BivariateFunction, typing.Callable], double: float, double2: float, double3: float, double4: float) -> float:
        """
            Integrates the function on the specified domain.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator.integrate` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.integration.bivariate.BivariateIntegrator`
        
            Parameters:
                maxEval (int): the maximum number of evaluations
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`): the integrand function
                xminIn (double): the lower bound of the interval for the 1st axis
                xmaxIn (double): the upper bound of the interval for the 1st axis
                yminIn (double): the lower bound of the interval for the 2nd axis
                ymaxIn (double): the upper bound of the interval for the 2nd axis
        
            Returns:
                the value of integral
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.analysis.integration.bivariate")``.

    BivariateIntegrator: typing.Type[BivariateIntegrator]
    DelegatedBivariateIntegrator: typing.Type[DelegatedBivariateIntegrator]
