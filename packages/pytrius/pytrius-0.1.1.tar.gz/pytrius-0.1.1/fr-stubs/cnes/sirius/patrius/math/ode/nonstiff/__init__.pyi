
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr
import fr.cnes.sirius.patrius.math.analysis.solver
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.ode
import fr.cnes.sirius.patrius.math.ode.events
import fr.cnes.sirius.patrius.math.ode.nonstiff.cowell
import fr.cnes.sirius.patrius.math.ode.sampling
import jpype
import typing



class AdamsIntegrator(fr.cnes.sirius.patrius.math.ode.MultistepIntegrator):
    """
    public abstract class AdamsIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.MultistepIntegrator`
    
        Base class for :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsBashforthIntegrator` and
        :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsMoultonIntegrator` integrators.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, string: str, int: int, int2: int, double: float, double2: float, double3: float, double4: float, boolean: bool): ...
    @typing.overload
    def __init__(self, string: str, int: int, int2: int, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool): ...
    @typing.overload
    def integrate(self, expandableStatefulODE: fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE, double: float) -> None:
        """
            Integrate a set of differential equations up to the given time.
        
            This method solves an Initial Value Problem (IVP).
        
            The set of differential equations is composed of a main set, which can be extended by some sets of secondary equations.
            The set of equations must be already set up with initial time and partial states. At integration completion, the final
            time and partial states will be available in the same object.
        
            Since this method stores some internal state variables made available in its public interface during integration
            (:meth:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator.getCurrentSignedStepsize`), it is *not* thread-safe.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdaptiveStepsizeIntegrator.integrate` in
                class :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdaptiveStepsizeIntegrator`
        
            Parameters:
                equations (:class:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE`): complete set of differential equations to integrate
                t (double): target time for the integration (can be set to a value smaller than :code:`t0` for backward integration)
        
        
        """
        ...
    @typing.overload
    def integrate(self, firstOrderDifferentialEquations: fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    def updateHighOrderDerivativesPhase1(self, array2DRowRealMatrix: fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix) -> fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix:
        """
            Update the high order scaled derivatives for Adams integrators (phase 1).
        
            The complete update of high order derivatives has a form similar to:
        
            .. code-block: java
            
            
             r :sub:`n+1`  = (s :sub:`1` (n) - s :sub:`1` (n+1)) P :sup:`-1`  u + P :sup:`-1`  A P r :sub:`n` 
             
            this method computes the P :sup:`-1` A P r :sub:`n` part.
        
            Parameters:
                highOrder (:class:`~fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix`): high order scaled derivatives (h :sup:`2` /2 y'', ... h :sup:`k` /k! y(k))
        
            Returns:
                updated high order derivatives
        
            Also see:
        
        
        """
        ...
    def updateHighOrderDerivativesPhase2(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], array2DRowRealMatrix: fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix) -> None:
        """
            Update the high order scaled derivatives Adams integrators (phase 2).
        
            The complete update of high order derivatives has a form similar to:
        
            .. code-block: java
            
            
             r :sub:`n+1`  = (s :sub:`1` (n) - s :sub:`1` (n+1)) P :sup:`-1`  u + P :sup:`-1`  A P r :sub:`n` 
             
            this method computes the (s :sub:`1` (n) - s :sub:`1` (n+1)) P :sup:`-1` u part.
        
            Phase 1 of the update must already have been performed.
        
            Parameters:
                start (double[]): first order scaled derivatives at step start
                end (double[]): first order scaled derivatives at step end
                highOrder (:class:`~fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix`): high order scaled derivatives, will be modified (h :sup:`2` /2 y'', ... h :sup:`k` /k! y(k))
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsIntegrator.updateHighOrderDerivativesPhase1`
        
        
        """
        ...

class AdamsNordsieckTransformer:
    """
    public final class AdamsNordsieckTransformer extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Transformer to Nordsieck vectors for Adams integrators.
    
        This class is used by :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsBashforthIntegrator` and
        :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsMoultonIntegrator` integrators to convert between classical
        representation with several previous first derivatives and Nordsieck representation with higher order scaled
        derivatives.
    
        We define scaled derivatives s :sub:`i` (n) at step n as:
    
        .. code-block: java
        
        
         s :sub:`1` (n) = h y' :sub:`n`  for first derivative
         s :sub:`2` (n) = h :sup:`2` /2 y'' :sub:`n`  for second derivative
         s :sub:`3` (n) = h :sup:`3` /6 y''' :sub:`n`  for third derivative
         ...
         s :sub:`k` (n) = h :sup:`k` /k! y :sup:`(k)`  :sub:`n`  for k :sup:`th`  derivative
         
    
        With the previous definition, the classical representation of multistep methods uses first derivatives only, i.e. it
        handles y :sub:`n` , s :sub:`1` (n) and q :sub:`n` where q :sub:`n` is defined as:
    
        .. code-block: java
        
        
           q :sub:`n`  = [ s :sub:`1` (n-1) s :sub:`1` (n-2) ... s :sub:`1` (n-(k-1)) ] :sup:`T` 
         
        (we omit the k index in the notation for clarity).
    
        Another possible representation uses the Nordsieck vector with higher degrees scaled derivatives all taken at the same
        step, i.e it handles y :sub:`n` , s :sub:`1` (n) and r :sub:`n` ) where r :sub:`n` is defined as:
    
        .. code-block: java
        
        
         r :sub:`n`  = [ s :sub:`2` (n), s :sub:`3` (n) ... s :sub:`k` (n) ] :sup:`T` 
         
        (here again we omit the k index in the notation for clarity)
    
        Taylor series formulas show that for any index offset i, s :sub:`1` (n-i) can be computed from s :sub:`1` (n), s
        :sub:`2` (n) ... s :sub:`k` (n), the formula being exact for degree k polynomials.
    
        .. code-block: java
        
        
         s :sub:`1` (n-i) = s :sub:`1` (n) + ∑ :sub:`j>1`  j (-i) :sup:`j-1`  s :sub:`j` (n)
         
        The previous formula can be used with several values for i to compute the transform between classical representation and
        Nordsieck vector at step end. The transform between r :sub:`n` and q :sub:`n` resulting from the Taylor series formulas
        above is:
    
        .. code-block: java
        
        
         q :sub:`n`  = s :sub:`1` (n) u + P r :sub:`n` 
         
        where u is the [ 1 1 ... 1 ] :sup:`T` vector and P is the (k-1)×(k-1) matrix built with the j (-i) :sup:`j-1` terms:
    
        .. code-block: java
        
        
                [  -2   3   -4    5  ... ]
                [  -4  12  -32   80  ... ]
           P =  [  -6  27 -108  405  ... ]
                [  -8  48 -256 1280  ... ]
                [          ...           ]
         
    
        Changing -i into +i in the formula above can be used to compute a similar transform between classical representation and
        Nordsieck vector at step start. The resulting matrix is simply the absolute value of matrix P.
    
        For :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsBashforthIntegrator` method, the Nordsieck vector at step n+1
        is computed from the Nordsieck vector at step n as follows:
    
          - y :sub:`n+1` = y :sub:`n` + s :sub:`1` (n) + u :sup:`T` r :sub:`n`
          - s :sub:`1` (n+1) = h f(t :sub:`n+1` , y :sub:`n+1` )
          - r :sub:`n+1` = (s :sub:`1` (n) - s :sub:`1` (n+1)) P :sup:`-1` u + P :sup:`-1` A P r :sub:`n`
    
        where A is a rows shifting matrix (the lower left part is an identity matrix):
    
        .. code-block: java
        
        
                [ 0 0   ...  0 0 | 0 ]
                [ ---------------+---]
                [ 1 0   ...  0 0 | 0 ]
            A = [ 0 1   ...  0 0 | 0 ]
                [       ...      | 0 ]
                [ 0 0   ...  1 0 | 0 ]
                [ 0 0   ...  0 1 | 0 ]
         
    
        For :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsMoultonIntegrator` method, the predicted Nordsieck vector at
        step n+1 is computed from the Nordsieck vector at step n as follows:
    
          - Y :sub:`n+1` = y :sub:`n` + s :sub:`1` (n) + u :sup:`T` r :sub:`n`
          - S :sub:`1` (n+1) = h f(t :sub:`n+1` , Y :sub:`n+1` )
          - R :sub:`n+1` = (s :sub:`1` (n) - s :sub:`1` (n+1)) P :sup:`-1` u + P :sup:`-1` A P r :sub:`n`
    
        From this predicted vector, the corrected vector is computed as follows:
    
          - y :sub:`n+1` = y :sub:`n` + S :sub:`1` (n+1) + [ -1 +1 -1 +1 ... ±1 ] r :sub:`n+1`
          - s :sub:`1` (n+1) = h f(t :sub:`n+1` , y :sub:`n+1` )
          - r :sub:`n+1` = R :sub:`n+1` + (s :sub:`1` (n+1) - S :sub:`1` (n+1)) P :sup:`-1` u
    
        where the upper case Y :sub:`n+1` , S :sub:`1` (n+1) and R :sub:`n+1` represent the predicted states whereas the lower
        case y :sub:`n+1` , s :sub:`n+1` and r :sub:`n+1` represent the corrected states.
    
        We observe that both methods use similar update formulas. In both cases a P :sup:`-1` u vector and a P :sup:`-1` A P
        matrix are used that do not depend on the state, they only depend on k. This class handles these transformations.
    
        Since:
            2.0
    """
    @staticmethod
    def getInstance(int: int) -> 'AdamsNordsieckTransformer':
        """
            Get the Nordsieck transformer for a given number of steps.
        
            Parameters:
                nSteps (int): number of steps of the multistep method (excluding the one being computed)
        
            Returns:
                Nordsieck transformer for the specified number of steps
        
        
        """
        ...
    def getNSteps(self) -> int:
        """
            Get the number of steps of the method (excluding the one being computed).
        
            Returns:
                number of steps of the method (excluding the one being computed)
        
        
        """
        ...
    def initializeHighOrderDerivatives(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix:
        """
            Initialize the high order scaled derivatives at step start.
        
            Parameters:
                h (double): step size to use for scaling
                t (double[]): first steps times
                y (double[][]): first steps states
                yDot (double[][]): first steps derivatives
        
            Returns:
                Nordieck vector at first step (h :sup:`2` /2 y'' :sub:`n` , h :sup:`3` /6 y''' :sub:`n` ... h :sup:`k` /k! y :sup:`(k)`
                :sub:`n` )
        
        
        """
        ...
    def updateHighOrderDerivativesPhase1(self, array2DRowRealMatrix: fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix) -> fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix:
        """
            Update the high order scaled derivatives for Adams integrators (phase 1).
        
            The complete update of high order derivatives has a form similar to:
        
            .. code-block: java
            
            
             r :sub:`n+1`  = (s :sub:`1` (n) - s :sub:`1` (n+1)) P :sup:`-1`  u + P :sup:`-1`  A P r :sub:`n` 
             
            this method computes the P :sup:`-1` A P r :sub:`n` part.
        
            Parameters:
                highOrder (:class:`~fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix`): high order scaled derivatives (h :sup:`2` /2 y'', ... h :sup:`k` /k! y(k))
        
            Returns:
                updated high order derivatives
        
            Also see:
        
        
        """
        ...
    def updateHighOrderDerivativesPhase2(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], array2DRowRealMatrix: fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix) -> None:
        """
            Update the high order scaled derivatives Adams integrators (phase 2).
        
            The complete update of high order derivatives has a form similar to:
        
            .. code-block: java
            
            
             r :sub:`n+1`  = (s :sub:`1` (n) - s :sub:`1` (n+1)) P :sup:`-1`  u + P :sup:`-1`  A P r :sub:`n` 
             
            this method computes the (s :sub:`1` (n) - s :sub:`1` (n+1)) P :sup:`-1` u part.
        
            Phase 1 of the update must already have been performed.
        
            Parameters:
                start (double[]): first order scaled derivatives at step start
                end (double[]): first order scaled derivatives at step end
                highOrder (:class:`~fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix`): high order scaled derivatives, will be modified (h :sup:`2` /2 y'', ... h :sup:`k` /k! y(k))
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsNordsieckTransformer.updateHighOrderDerivativesPhase1`
        
        
        """
        ...

class AdaptiveStepsizeIntegrator(fr.cnes.sirius.patrius.math.ode.AbstractIntegrator):
    """
    public abstract class AdaptiveStepsizeIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator`
    
        This abstract class holds the common part of all adaptive stepsize integrators for Ordinary Differential Equations.
    
        These algorithms perform integration with stepsize control, which means the user does not specify the integration step
        but rather a tolerance on error. The error threshold is computed as
    
        .. code-block: java
        
        
         threshold_i = absTol_i + relTol_i * max(abs(ym), abs(ym + 1))
         
        where absTol_i is the absolute tolerance for component i of the state vector and relTol_i is the relative tolerance for
        the same component. The user can also use only two scalar values absTol and relTol which will be used for all
        components.
    
        If the Ordinary Differential Equations is an :class:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE` rather than
        a :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`, then *only* the
        :meth:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE.getPrimaryState` of the state vector is used for stepsize
        control, not the complete state vector.
    
        If the estimated error for ym+1 is such that
    
        .. code-block: java
        
        
         sqrt((sum(errEst_i / threshold_i) ˆ 2) / n) < 1
         
        (where n is the main set dimension) then the step is accepted, otherwise the step is rejected and a new attempt is made
        with a new stepsize.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, string: str, double: float, double2: float, double3: float, double4: float, boolean: bool): ...
    @typing.overload
    def __init__(self, string: str, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool): ...
    def getCurrentStepStart(self) -> float:
        """
            Get the current value of the step start time t :sub:`i` .
        
            This method can be called during integration (typically by the object implementing the
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations` problem) if the value of the current step that
            is attempted is needed.
        
            The result is undefined if the method is called outside of calls to :code:`integrate`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.getCurrentStepStart` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator.getCurrentStepStart` in
                class :class:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator`
        
            Returns:
                current value of the step start time t :sub:`i`
        
        
        """
        ...
    def getMaxStep(self) -> float:
        """
            Get the maximal step.
        
            Returns:
                maximal step
        
        
        """
        ...
    def getMinStep(self) -> float:
        """
            Get the minimal step.
        
            Returns:
                minimal step
        
        
        """
        ...
    def getScalAbsoluteTolerance(self) -> float:
        """
            Returns the scalar absolute tolerances.
        
            Returns:
                the scalar absolute tolerances, if defined by a scalar, zero otherwise
        
        
        """
        ...
    def getScalRelativeTolerance(self) -> float:
        """
            Returns the scalar relative tolerances.
        
            Returns:
                the scalar relative tolerances, if defined by a scalar, zero otherwise
        
        
        """
        ...
    def getVecAbsoluteTolerance(self) -> typing.MutableSequence[float]:
        """
            Returns the vector of absolute tolerances.
        
            Returns:
                the vector of absolute tolerances, if defined by a vector, null otherwise
        
        
        """
        ...
    def getVecRelativeTolerance(self) -> typing.MutableSequence[float]:
        """
            Returns the vector of relative tolerances.
        
            Returns:
                the vector of relative tolerances, if defined by a vector, null otherwise
        
        
        """
        ...
    def initializeStep(self, boolean: bool, int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray], doubleArray4: typing.Union[typing.List[float], jpype.JArray], doubleArray5: typing.Union[typing.List[float], jpype.JArray], double7: float) -> float:
        """
            Initialize the integration step.
        
            Parameters:
                forward (boolean): forward integration indicator
                order (int): order of the method
                scale (double[]): scaling vector for the state vector (can be shorter than state vector)
                t0 (double): start time
                y0 (double[]): state vector at t0
                yDot0 (double[]): first time derivative of y0
                y1 (double[]): work array for a state vector
                yDot1 (double[]): work array for the first time derivative of y1
                t (double): final integration time
        
            Returns:
                first integration step
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if arrays dimensions do not match equations settings
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the step is too small and acceptSmall is false
        
        
        """
        ...
    @typing.overload
    def integrate(self, expandableStatefulODE: fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE, double: float) -> None:
        """
            Integrate a set of differential equations up to the given time.
        
            This method solves an Initial Value Problem (IVP).
        
            The set of differential equations is composed of a main set, which can be extended by some sets of secondary equations.
            The set of equations must be already set up with initial time and partial states. At integration completion, the final
            time and partial states will be available in the same object.
        
            Since this method stores some internal state variables made available in its public interface during integration
            (:meth:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator.getCurrentSignedStepsize`), it is *not* thread-safe.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator.integrate` in
                class :class:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator`
        
            Parameters:
                equations (:class:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE`): complete set of differential equations to integrate
                t (double): target time for the integration (can be set to a value smaller than :code:`t0` for backward integration)
        
        
        """
        ...
    @typing.overload
    def integrate(self, firstOrderDifferentialEquations: fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    def setInitialStepSize(self, double: float) -> None:
        """
            Set the initial step size.
        
            This method allows the user to specify an initial positive step size instead of letting the integrator guess it by
            itself. If this method is not called before integration is started, the initial step size will be estimated by the
            integrator.
        
            Parameters:
                initialStepSize (double): initial step size to use (must be positive even for backward integration ; providing a negative value or a value outside
                    of the min/max step interval will lead the integrator to ignore the value and compute the initial step size by itself)
        
        
        """
        ...
    @typing.overload
    def setStepSizeControl(self, double: float, double2: float, double3: float, double4: float, boolean: bool) -> None:
        """
            Set the adaptive step size control parameters.
        
            A side effect of this method is to also reset the initial step so it will be automatically computed by the integrator if
            :meth:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdaptiveStepsizeIntegrator.setInitialStepSize` is not called by the
            user.
        
            Parameters:
                minimalStep (double): minimal step (must be positive even for backward integration), the last step can be smaller than this
                maximalStep (double): maximal step (must be positive even for backward integration)
                absoluteTolerance (double): allowed absolute error
                relativeTolerance (double): allowed relative error
                acceptSmallIn (boolean): if true, steps smaller than the minimal value are silently increased up to this value, if false such small steps
                    generate an exception
        
            Set the adaptive step size control parameters.
        
            A side effect of this method is to also reset the initial step so it will be automatically computed by the integrator if
            :meth:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdaptiveStepsizeIntegrator.setInitialStepSize` is not called by the
            user.
        
            Parameters:
                minimalStep (double): minimal step (must be positive even for backward integration), the last step can be smaller than this
                maximalStep (double): maximal step (must be positive even for backward integration)
                absoluteTolerance (double[]): allowed absolute error
                relativeTolerance (double[]): allowed relative error
                acceptSmallIn (boolean): if true, steps smaller than the minimal value are silently increased up to this value, if false such small steps
                    generate an exception
        
        
        """
        ...
    @typing.overload
    def setStepSizeControl(self, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool) -> None: ...
    def setVecAbsoluteTolerance(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set the vector of absolute tolerances.
        
            Parameters:
                vecAbsoluteTolerance (double[]): the vector of absolute tolerances to set
        
        
        """
        ...
    def setVecRelativeTolerance(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set the vector of relative tolerances.
        
            Parameters:
                vecRelativeTolerance (double[]): the vector of relative tolerances to set
        
        
        """
        ...

class RungeKuttaIntegrator(fr.cnes.sirius.patrius.math.ode.AbstractIntegrator):
    """
    public abstract class RungeKuttaIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator`
    
        This class implements the common part of all fixed step Runge-Kutta integrators for Ordinary Differential Equations.
    
        These methods are explicit Runge-Kutta methods, their Butcher arrays are as follows :
    
        .. code-block: java
        
        
            0  |
           c2  | a21
           c3  | a31  a32
           ... |        ...
           cs  | as1  as2  ...  ass-1
               |--------------------------
               |  b1   b2  ...   bs-1  bs
         
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EulerIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.ClassicalRungeKuttaIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.GillIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.MidpointIntegrator`, :meth:`~serialized`
    """
    @typing.overload
    def integrate(self, firstOrderDifferentialEquations: fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def integrate(self, expandableStatefulODE: fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE, double: float) -> None:
        """
            Integrate a set of differential equations up to the given time.
        
            This method solves an Initial Value Problem (IVP).
        
            The set of differential equations is composed of a main set, which can be extended by some sets of secondary equations.
            The set of equations must be already set up with initial time and partial states. At integration completion, the final
            time and partial states will be available in the same object.
        
            Since this method stores some internal state variables made available in its public interface during integration
            (:meth:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator.getCurrentSignedStepsize`), it is *not* thread-safe.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator.integrate` in
                class :class:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator`
        
            Parameters:
                equations (:class:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE`): complete set of differential equations to integrate
                t (double): target time for the integration (can be set to a value smaller than :code:`t0` for backward integration)
        
        
        """
        ...

class AdamsBashforthIntegrator(AdamsIntegrator):
    """
    public class AdamsBashforthIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsIntegrator`
    
        This class implements explicit Adams-Bashforth integrators for Ordinary Differential Equations.
    
        Adams-Bashforth methods (in fact due to Adams alone) are explicit multistep ODE solvers. This implementation is a
        variation of the classical one: it uses adaptive stepsize to implement error control, whereas classical implementations
        are fixed step size. The value of state vector at step n+1 is a simple combination of the value at step n and of the
        derivatives at steps n, n-1, n-2 ... Depending on the number k of previous steps one wants to use for computing the next
        value, different formulas are available:
    
          - k = 1: y :sub:`n+1` = y :sub:`n` + h y' :sub:`n`
          - k = 2: y :sub:`n+1` = y :sub:`n` + h (3y' :sub:`n` -y' :sub:`n-1` )/2
          - k = 3: y :sub:`n+1` = y :sub:`n` + h (23y' :sub:`n` -16y' :sub:`n-1` +5y' :sub:`n-2` )/12
          - k = 4: y :sub:`n+1` = y :sub:`n` + h (55y' :sub:`n` -59y' :sub:`n-1` +37y' :sub:`n-2` -9y' :sub:`n-3` )/24
          - ...
    
    
        A k-steps Adams-Bashforth method is of order k.
    
        Implementation details
    ----------------------
    
    
        We define scaled derivatives s :sub:`i` (n) at step n as:
    
        .. code-block: java
        
        
         s :sub:`1` (n) = h y' :sub:`n`  for first derivative
         s :sub:`2` (n) = h :sup:`2` /2 y'' :sub:`n`  for second derivative
         s :sub:`3` (n) = h :sup:`3` /6 y''' :sub:`n`  for third derivative
         ...
         s :sub:`k` (n) = h :sup:`k` /k! y :sup:`(k)`  :sub:`n`  for k :sup:`th`  derivative
         
    
        The definitions above use the classical representation with several previous first derivatives. Lets define
    
        .. code-block: java
        
        
           q :sub:`n`  = [ s :sub:`1` (n-1) s :sub:`1` (n-2) ... s :sub:`1` (n-(k-1)) ] :sup:`T` 
         
        (we omit the k index in the notation for clarity). With these definitions, Adams-Bashforth methods can be written:
    
          - k = 1: y :sub:`n+1` = y :sub:`n` + s :sub:`1` (n)
          - k = 2: y :sub:`n+1` = y :sub:`n` + 3/2 s :sub:`1` (n) + [ -1/2 ] q :sub:`n`
          - k = 3: y :sub:`n+1` = y :sub:`n` + 23/12 s :sub:`1` (n) + [ -16/12 5/12 ] q :sub:`n`
          - k = 4: y :sub:`n+1` = y :sub:`n` + 55/24 s :sub:`1` (n) + [ -59/24 37/24 -9/24 ] q :sub:`n`
          - ...
    
    
        Instead of using the classical representation with first derivatives only (y :sub:`n` , s :sub:`1` (n) and q :sub:`n` ),
        our implementation uses the Nordsieck vector with higher degrees scaled derivatives all taken at the same step (y
        :sub:`n` , s :sub:`1` (n) and r :sub:`n` ) where r :sub:`n` is defined as:
    
        .. code-block: java
        
        
         r :sub:`n`  = [ s :sub:`2` (n), s :sub:`3` (n) ... s :sub:`k` (n) ] :sup:`T` 
         
        (here again we omit the k index in the notation for clarity)
    
        Taylor series formulas show that for any index offset i, s :sub:`1` (n-i) can be computed from s :sub:`1` (n), s
        :sub:`2` (n) ... s :sub:`k` (n), the formula being exact for degree k polynomials.
    
        .. code-block: java
        
        
         s :sub:`1` (n-i) = s :sub:`1` (n) + ∑ :sub:`j`  j (-i) :sup:`j-1`  s :sub:`j` (n)
         
        The previous formula can be used with several values for i to compute the transform between classical representation and
        Nordsieck vector. The transform between r :sub:`n` and q :sub:`n` resulting from the Taylor series formulas above is:
    
        .. code-block: java
        
        
         q :sub:`n`  = s :sub:`1` (n) u + P r :sub:`n` 
         
        where u is the [ 1 1 ... 1 ] :sup:`T` vector and P is the (k-1)×(k-1) matrix built with the j (-i) :sup:`j-1` terms:
    
        .. code-block: java
        
        
                [  -2   3   -4    5  ... ]
                [  -4  12  -32   80  ... ]
           P =  [  -6  27 -108  405  ... ]
                [  -8  48 -256 1280  ... ]
                [          ...           ]
         
    
        Using the Nordsieck vector has several advantages:
    
          - it greatly simplifies step interpolation as the interpolator mainly applies Taylor series formulas,
          - it simplifies step changes that occur when discrete events that truncate the step are triggered,
          - it allows to extend the methods in order to support adaptive stepsize.
    
    
        The Nordsieck vector at step n+1 is computed from the Nordsieck vector at step n as follows:
    
          - y :sub:`n+1` = y :sub:`n` + s :sub:`1` (n) + u :sup:`T` r :sub:`n`
          - s :sub:`1` (n+1) = h f(t :sub:`n+1` , y :sub:`n+1` )
          - r :sub:`n+1` = (s :sub:`1` (n) - s :sub:`1` (n+1)) P :sup:`-1` u+P :sup:`-1` A P r :sub:`n`
    
        where A is a rows shifting matrix (the lower left part is an identity matrix):
    
        .. code-block: java
        
        
                [ 0 0   ...  0 0 | 0 ]
                [ ---------------+---]
                [ 1 0   ...  0 0 | 0 ]
            A = [ 0 1   ...  0 0 | 0 ]
                [       ...      | 0 ]
                [ 0 0   ...  1 0 | 0 ]
                [ 0 0   ...  0 1 | 0 ]
         
    
        The P :sup:`-1` u vector and the P :sup:`-1` A P matrix do not depend on the state, they only depend on k and therefore
        are precomputed once for all.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, double3: float, double4: float, boolean: bool): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool): ...
    @typing.overload
    def integrate(self, firstOrderDifferentialEquations: fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def integrate(self, expandableStatefulODE: fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE, double: float) -> None:
        """
            Integrate a set of differential equations up to the given time.
        
            This method solves an Initial Value Problem (IVP).
        
            The set of differential equations is composed of a main set, which can be extended by some sets of secondary equations.
            The set of equations must be already set up with initial time and partial states. At integration completion, the final
            time and partial states will be available in the same object.
        
            Since this method stores some internal state variables made available in its public interface during integration
            (:meth:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator.getCurrentSignedStepsize`), it is *not* thread-safe.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsIntegrator.integrate` in
                class :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsIntegrator`
        
            Parameters:
                equations (:class:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE`): complete set of differential equations to integrate
                t (double): target time for the integration (can be set to a value smaller than :code:`t0` for backward integration)
        
        
        """
        ...

class AdamsMoultonIntegrator(AdamsIntegrator):
    """
    public class AdamsMoultonIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsIntegrator`
    
        This class implements implicit Adams-Moulton integrators for Ordinary Differential Equations.
    
        Adams-Moulton methods (in fact due to Adams alone) are implicit multistep ODE solvers. This implementation is a
        variation of the classical one: it uses adaptive stepsize to implement error control, whereas classical implementations
        are fixed step size. The value of state vector at step n+1 is a simple combination of the value at step n and of the
        derivatives at steps n+1, n, n-1 ... Since y' :sub:`n+1` is needed to compute y :sub:`n+1` , another method must be used
        to compute a first estimate of y :sub:`n+1` , then compute y' :sub:`n+1` , then compute a final estimate of y :sub:`n+1`
        using the following formulas. Depending on the number k of previous steps one wants to use for computing the next value,
        different formulas are available for the final estimate:
    
          - k = 1: y :sub:`n+1` = y :sub:`n` + h y' :sub:`n+1`
          - k = 2: y :sub:`n+1` = y :sub:`n` + h (y' :sub:`n+1` +y' :sub:`n` )/2
          - k = 3: y :sub:`n+1` = y :sub:`n` + h (5y' :sub:`n+1` +8y' :sub:`n` -y' :sub:`n-1` )/12
          - k = 4: y :sub:`n+1` = y :sub:`n` + h (9y' :sub:`n+1` +19y' :sub:`n` -5y' :sub:`n-1` +y' :sub:`n-2` )/24
          - ...
    
    
        A k-steps Adams-Moulton method is of order k+1.
    
        Implementation details
    ----------------------
    
    
        We define scaled derivatives s :sub:`i` (n) at step n as:
    
        .. code-block: java
        
        
         s :sub:`1` (n) = h y' :sub:`n`  for first derivative
         s :sub:`2` (n) = h :sup:`2` /2 y'' :sub:`n`  for second derivative
         s :sub:`3` (n) = h :sup:`3` /6 y''' :sub:`n`  for third derivative
         ...
         s :sub:`k` (n) = h :sup:`k` /k! y :sup:`(k)`  :sub:`n`  for k :sup:`th`  derivative
         
    
        The definitions above use the classical representation with several previous first derivatives. Lets define
    
        .. code-block: java
        
        
           q :sub:`n`  = [ s :sub:`1` (n-1) s :sub:`1` (n-2) ... s :sub:`1` (n-(k-1)) ] :sup:`T` 
         
        (we omit the k index in the notation for clarity). With these definitions, Adams-Moulton methods can be written:
    
          - k = 1: y :sub:`n+1` = y :sub:`n` + s :sub:`1` (n+1)
          - k = 2: y :sub:`n+1` = y :sub:`n` + 1/2 s :sub:`1` (n+1) + [ 1/2 ] q :sub:`n+1`
          - k = 3: y :sub:`n+1` = y :sub:`n` + 5/12 s :sub:`1` (n+1) + [ 8/12 -1/12 ] q :sub:`n+1`
          - k = 4: y :sub:`n+1` = y :sub:`n` + 9/24 s :sub:`1` (n+1) + [ 19/24 -5/24 1/24 ] q :sub:`n+1`
          - ...
    
    
        Instead of using the classical representation with first derivatives only (y :sub:`n` , s :sub:`1` (n+1) and q
        :sub:`n+1` ), our implementation uses the Nordsieck vector with higher degrees scaled derivatives all taken at the same
        step (y :sub:`n` , s :sub:`1` (n) and r :sub:`n` ) where r :sub:`n` is defined as:
    
        .. code-block: java
        
        
         r :sub:`n`  = [ s :sub:`2` (n), s :sub:`3` (n) ... s :sub:`k` (n) ] :sup:`T` 
         
        (here again we omit the k index in the notation for clarity)
    
        Taylor series formulas show that for any index offset i, s :sub:`1` (n-i) can be computed from s :sub:`1` (n), s
        :sub:`2` (n) ... s :sub:`k` (n), the formula being exact for degree k polynomials.
    
        .. code-block: java
        
        
         s :sub:`1` (n-i) = s :sub:`1` (n) + ∑ :sub:`j`  j (-i) :sup:`j-1`  s :sub:`j` (n)
         
        The previous formula can be used with several values for i to compute the transform between classical representation and
        Nordsieck vector. The transform between r :sub:`n` and q :sub:`n` resulting from the Taylor series formulas above is:
    
        .. code-block: java
        
        
         q :sub:`n`  = s :sub:`1` (n) u + P r :sub:`n` 
         
        where u is the [ 1 1 ... 1 ] :sup:`T` vector and P is the (k-1)×(k-1) matrix built with the j (-i) :sup:`j-1` terms:
    
        .. code-block: java
        
        
                [  -2   3   -4    5  ... ]
                [  -4  12  -32   80  ... ]
           P =  [  -6  27 -108  405  ... ]
                [  -8  48 -256 1280  ... ]
                [          ...           ]
         
    
        Using the Nordsieck vector has several advantages:
    
          - it greatly simplifies step interpolation as the interpolator mainly applies Taylor series formulas,
          - it simplifies step changes that occur when discrete events that truncate the step are triggered,
          - it allows to extend the methods in order to support adaptive stepsize.
    
    
        The predicted Nordsieck vector at step n+1 is computed from the Nordsieck vector at step n as follows:
    
          - Y :sub:`n+1` = y :sub:`n` + s :sub:`1` (n) + u :sup:`T` r :sub:`n`
          - S :sub:`1` (n+1) = h f(t :sub:`n+1` , Y :sub:`n+1` )
          - R :sub:`n+1` = (s :sub:`1` (n) - S :sub:`1` (n+1)) P :sup:`-1` u+P :sup:`-1` A P r :sub:`n`
    
        where A is a rows shifting matrix (the lower left part is an identity matrix):
    
        .. code-block: java
        
        
                [ 0 0   ...  0 0 | 0 ]
                [ ---------------+---]
                [ 1 0   ...  0 0 | 0 ]
            A = [ 0 1   ...  0 0 | 0 ]
                [       ...      | 0 ]
                [ 0 0   ...  1 0 | 0 ]
                [ 0 0   ...  0 1 | 0 ]
         
        From this predicted vector, the corrected vector is computed as follows:
    
          - y :sub:`n+1` = y :sub:`n` + S :sub:`1` (n+1) + [ -1 +1 -1 +1 ... ±1 ] r :sub:`n+1`
          - s :sub:`1` (n+1) = h f(t :sub:`n+1` , y :sub:`n+1` )
          - r :sub:`n+1` = R :sub:`n+1` + (s :sub:`1` (n+1) - S :sub:`1` (n+1)) P :sup:`-1` u
    
        where the upper case Y :sub:`n+1` , S :sub:`1` (n+1) and R :sub:`n+1` represent the predicted states whereas the lower
        case y :sub:`n+1` , s :sub:`n+1` and r :sub:`n+1` represent the corrected states.
    
        The P :sup:`-1` u vector and the P :sup:`-1` A P matrix do not depend on the state, they only depend on k and therefore
        are precomputed once for all.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, double3: float, double4: float, boolean: bool): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool): ...
    @typing.overload
    def integrate(self, firstOrderDifferentialEquations: fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def integrate(self, expandableStatefulODE: fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE, double: float) -> None:
        """
            Integrate a set of differential equations up to the given time.
        
            This method solves an Initial Value Problem (IVP).
        
            The set of differential equations is composed of a main set, which can be extended by some sets of secondary equations.
            The set of equations must be already set up with initial time and partial states. At integration completion, the final
            time and partial states will be available in the same object.
        
            Since this method stores some internal state variables made available in its public interface during integration
            (:meth:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator.getCurrentSignedStepsize`), it is *not* thread-safe.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsIntegrator.integrate` in
                class :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsIntegrator`
        
            Parameters:
                equations (:class:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE`): complete set of differential equations to integrate
                t (double): target time for the integration (can be set to a value smaller than :code:`t0` for backward integration)
        
        
        """
        ...

class ClassicalRungeKuttaIntegrator(RungeKuttaIntegrator):
    """
    public class ClassicalRungeKuttaIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.RungeKuttaIntegrator`
    
        This class implements the classical 4th order Runge-Kutta integrator for Ordinary Differential Equations (it is the most
        often used Runge-Kutta method).
    
        This method is an explicit Runge-Kutta method, its Butcher-array is the following one :
    
        .. code-block: java
        
        
            0  |  0    0    0    0
           1/2 | 1/2   0    0    0
           1/2 |  0   1/2   0    0
            1  |  0    0    1    0
               |--------------------
               | 1/6  1/3  1/3  1/6
         
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EulerIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.GillIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.MidpointIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.ThreeEighthesIntegrator`, :meth:`~serialized`
    """
    def __init__(self, double: float): ...

class EmbeddedRungeKuttaIntegrator(AdaptiveStepsizeIntegrator):
    """
    public abstract class EmbeddedRungeKuttaIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdaptiveStepsizeIntegrator`
    
        This class implements the common part of all embedded Runge-Kutta integrators for Ordinary Differential Equations.
    
        These methods are embedded explicit Runge-Kutta methods with two sets of coefficients allowing to estimate the error,
        their Butcher arrays are as follows :
    
        .. code-block: java
        
        
            0  |
           c2  | a21
           c3  | a31  a32
           ... |        ...
           cs  | as1  as2  ...  ass-1
               |--------------------------
               |  b1   b2  ...   bs-1  bs
               |  b'1  b'2 ...   b's-1 b's
         
    
        In fact, we rather use the array defined by ej = bj - b'j to compute directly the error rather than computing two
        estimates and then comparing them.
    
        Some methods are qualified as *fsal* (first same as last) methods. This means the last evaluation of the derivatives in
        one step is the same as the first in the next step. Then, this evaluation can be reused from one step to the next one
        and the cost of such a method is really s-1 evaluations despite the method still has s stages. This behaviour is true
        only for successful steps, if the step is rejected after the error estimation phase, no evaluation is saved. For an
        *fsal* method, we have cs = 1 and asi = bi for all i.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def getMaxGrowth(self) -> float:
        """
            Get the maximal growth factor for stepsize control.
        
            Returns:
                maximal growth factor
        
        
        """
        ...
    def getMinReduction(self) -> float:
        """
            Get the minimal reduction factor for stepsize control.
        
            Returns:
                minimal reduction factor
        
        
        """
        ...
    def getOrder(self) -> int:
        """
            Get the order of the method.
        
            Returns:
                order of the method
        
        
        """
        ...
    def getSafety(self) -> float:
        """
            Get the safety factor for stepsize control.
        
            Returns:
                safety factor
        
        
        """
        ...
    @typing.overload
    def integrate(self, firstOrderDifferentialEquations: fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def integrate(self, expandableStatefulODE: fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE, double: float) -> None:
        """
            Integrate a set of differential equations up to the given time.
        
            This method solves an Initial Value Problem (IVP).
        
            The set of differential equations is composed of a main set, which can be extended by some sets of secondary equations.
            The set of equations must be already set up with initial time and partial states. At integration completion, the final
            time and partial states will be available in the same object.
        
            Since this method stores some internal state variables made available in its public interface during integration
            (:meth:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator.getCurrentSignedStepsize`), it is *not* thread-safe.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdaptiveStepsizeIntegrator.integrate` in
                class :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdaptiveStepsizeIntegrator`
        
            Parameters:
                equations (:class:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE`): complete set of differential equations to integrate
                t (double): target time for the integration (can be set to a value smaller than :code:`t0` for backward integration)
        
        
        """
        ...
    def setMaxGrowth(self, double: float) -> None:
        """
            Set the maximal growth factor for stepsize control.
        
            Parameters:
                maxGrowthIn (double): maximal growth factor
        
        
        """
        ...
    def setMinReduction(self, double: float) -> None:
        """
            Set the minimal reduction factor for stepsize control.
        
            Parameters:
                minReductionIn (double): minimal reduction factor
        
        
        """
        ...
    def setSafety(self, double: float) -> None:
        """
            Set the safety factor for stepsize control.
        
            Parameters:
                safetyIn (double): safety factor
        
        
        """
        ...

class EulerIntegrator(RungeKuttaIntegrator):
    """
    public class EulerIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.RungeKuttaIntegrator`
    
        This class implements a simple Euler integrator for Ordinary Differential Equations.
    
        The Euler algorithm is the simplest one that can be used to integrate ordinary differential equations. It is a simple
        inversion of the forward difference expression : :code:`f'=(f(t+h)-f(t))/h` which leads to :code:`f(t+h)=f(t)+hf'`. The
        interpolation scheme used for dense output is the linear scheme already used for integration.
    
        This algorithm looks cheap because it needs only one function evaluation per step. However, as it uses linear estimates,
        it needs very small steps to achieve high accuracy, and small steps lead to numerical errors and instabilities.
    
        This algorithm is almost never used and has been included in this package only as a comparison reference for more useful
        integrators.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.MidpointIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.ClassicalRungeKuttaIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.GillIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.ThreeEighthesIntegrator`, :meth:`~serialized`
    """
    def __init__(self, double: float): ...

class GillIntegrator(RungeKuttaIntegrator):
    """
    public class GillIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.RungeKuttaIntegrator`
    
        This class implements the Gill fourth order Runge-Kutta integrator for Ordinary Differential Equations .
    
        This method is an explicit Runge-Kutta method, its Butcher-array is the following one :
    
        .. code-block: java
        
        
            0  |    0        0       0      0
           1/2 |   1/2       0       0      0
           1/2 | (q-1)/2  (2-q)/2    0      0
            1  |    0       -q/2  (2+q)/2   0
               |-------------------------------
               |   1/6    (2-q)/6 (2+q)/6  1/6
         
        where q = sqrt(2)
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EulerIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.ClassicalRungeKuttaIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.MidpointIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.ThreeEighthesIntegrator`, :meth:`~serialized`
    """
    def __init__(self, double: float): ...

class GraggBulirschStoerIntegrator(AdaptiveStepsizeIntegrator):
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def addEventHandler(self, eventHandler: fr.cnes.sirius.patrius.math.ode.events.EventHandler, double: float, double2: float, int: int) -> None: ...
    @typing.overload
    def addEventHandler(self, eventHandler: fr.cnes.sirius.patrius.math.ode.events.EventHandler, double: float, double2: float, int: int, univariateSolver: fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver) -> None: ...
    def addStepHandler(self, stepHandler: fr.cnes.sirius.patrius.math.ode.sampling.StepHandler) -> None: ...
    @typing.overload
    def integrate(self, firstOrderDifferentialEquations: fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def integrate(self, expandableStatefulODE: fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE, double: float) -> None: ...
    def setControlFactors(self, double: float, double2: float, double3: float, double4: float) -> None: ...
    def setInterpolationControl(self, boolean: bool, int: int) -> None: ...
    def setOrderControl(self, int: int, double: float, double2: float) -> None: ...
    def setStabilityCheck(self, boolean: bool, int: int, int2: int, double: float) -> None: ...

class MidpointIntegrator(RungeKuttaIntegrator):
    """
    public class MidpointIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.RungeKuttaIntegrator`
    
        This class implements a second order Runge-Kutta integrator for Ordinary Differential Equations.
    
        This method is an explicit Runge-Kutta method, its Butcher-array is the following one :
    
        .. code-block: java
        
        
            0  |  0    0
           1/2 | 1/2   0
               |----------
               |  0    1
         
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EulerIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.ClassicalRungeKuttaIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.GillIntegrator`, :meth:`~serialized`
    """
    def __init__(self, double: float): ...

class RungeKutta6Integrator(RungeKuttaIntegrator):
    def __init__(self, double: float): ...
    @staticmethod
    def buildRK6StepInterpolator(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], int: int, int2: int) -> 'RungeKutta6StepInterpolator': ...

class ThreeEighthesIntegrator(RungeKuttaIntegrator):
    """
    public class ThreeEighthesIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.RungeKuttaIntegrator`
    
        This class implements the 3/8 fourth order Runge-Kutta integrator for Ordinary Differential Equations.
    
        This method is an explicit Runge-Kutta method, its Butcher-array is the following one :
    
        .. code-block: java
        
        
            0  |  0    0    0    0
           1/3 | 1/3   0    0    0
           2/3 |-1/3   1    0    0
            1  |  1   -1    1    0
               |--------------------
               | 1/8  3/8  3/8  1/8
         
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EulerIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.ClassicalRungeKuttaIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.GillIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.MidpointIntegrator`, :meth:`~serialized`
    """
    def __init__(self, double: float): ...

class DormandPrince54Integrator(EmbeddedRungeKuttaIntegrator):
    """
    public class DormandPrince54Integrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EmbeddedRungeKuttaIntegrator`
    
        This class implements the 5(4) Dormand-Prince integrator for Ordinary Differential Equations.
    
        This integrator is an embedded Runge-Kutta integrator of order 5(4) used in local extrapolation mode (i.e. the solution
        is computed using the high order formula) with stepsize control (and automatic step initialization) and continuous
        output. This method uses 7 functions evaluations per step. However, since this is an *fsal*, the last evaluation of one
        step is the same as the first evaluation of the next step and hence can be avoided. So the cost is really 6 functions
        evaluations per step.
    
        This method has been published (whithout the continuous output that was added by Shampine in 1986) in the following
        article :
    
        .. code-block: java
        
        
          A family of embedded Runge-Kutta formulae
          J. R. Dormand and P. J. Prince
          Journal of Computational and Applied Mathematics
          volume 6, no 1, 1980, pp. 19-26
         
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, boolean: bool): ...
    @typing.overload
    def __init__(self, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool): ...
    def getOrder(self) -> int:
        """
            Get the order of the method.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EmbeddedRungeKuttaIntegrator.getOrder` in
                class :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EmbeddedRungeKuttaIntegrator`
        
            Returns:
                order of the method
        
        
        """
        ...

class DormandPrince853Integrator(EmbeddedRungeKuttaIntegrator):
    """
    public class DormandPrince853Integrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EmbeddedRungeKuttaIntegrator`
    
        This class implements the 8(5,3) Dormand-Prince integrator for Ordinary Differential Equations.
    
        This integrator is an embedded Runge-Kutta integrator of order 8(5,3) used in local extrapolation mode (i.e. the
        solution is computed using the high order formula) with stepsize control (and automatic step initialization) and
        continuous output. This method uses 12 functions evaluations per step for integration and 4 evaluations for
        interpolation. However, since the first interpolation evaluation is the same as the first integration evaluation of the
        next step, we have included it in the integrator rather than in the interpolator and specified the method was an *fsal*.
        Hence, despite we have 13 stages here, the cost is really 12 evaluations per step even if no interpolation is done, and
        the overcost of interpolation is only 3 evaluations.
    
        This method is based on an 8(6) method by Dormand and Prince (i.e. order 8 for the integration and order 6 for error
        estimation) modified by Hairer and Wanner to use a 5th order error estimator with 3rd order correction. This
        modification was introduced because the original method failed in some cases (wrong steps can be accepted when step size
        is too large, for example in the Brusselator problem) and also had *severe difficulties when applied to problems with
        discontinuities*. This modification is explained in the second edition of the first volume (Nonstiff Problems) of the
        reference book by Hairer, Norsett and Wanner: *Solving Ordinary Differential Equations* (Springer-Verlag, ISBN
        3-540-56670-8).
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, boolean: bool): ...
    @typing.overload
    def __init__(self, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool): ...
    def getOrder(self) -> int:
        """
            Get the order of the method.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EmbeddedRungeKuttaIntegrator.getOrder` in
                class :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EmbeddedRungeKuttaIntegrator`
        
            Returns:
                order of the method
        
        
        """
        ...

class HighamHall54Integrator(EmbeddedRungeKuttaIntegrator):
    """
    public class HighamHall54Integrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EmbeddedRungeKuttaIntegrator`
    
        This class implements the 5(4) Higham and Hall integrator for Ordinary Differential Equations.
    
        This integrator is an embedded Runge-Kutta integrator of order 5(4) used in local extrapolation mode (i.e. the solution
        is computed using the high order formula) with stepsize control (and automatic step initialization) and continuous
        output. This method uses 7 functions evaluations per step.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, boolean: bool): ...
    @typing.overload
    def __init__(self, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool): ...
    def getOrder(self) -> int:
        """
            Get the order of the method.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EmbeddedRungeKuttaIntegrator.getOrder` in
                class :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.EmbeddedRungeKuttaIntegrator`
        
            Returns:
                order of the method
        
        
        """
        ...

class RungeKutta6StepInterpolator(fr.cnes.sirius.patrius.math.ode.nonstiff.RungeKuttaStepInterpolator):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, rungeKutta6StepInterpolator: 'RungeKutta6StepInterpolator'): ...
    def isIncoherentState(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> bool: ...
    def reinitialize(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], boolean: bool, equationsMapper: fr.cnes.sirius.patrius.math.ode.EquationsMapper, equationsMapperArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.ode.EquationsMapper], jpype.JArray]) -> None: ...

class RungeKuttaStepInterpolator: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.ode.nonstiff")``.

    AdamsBashforthIntegrator: typing.Type[AdamsBashforthIntegrator]
    AdamsIntegrator: typing.Type[AdamsIntegrator]
    AdamsMoultonIntegrator: typing.Type[AdamsMoultonIntegrator]
    AdamsNordsieckTransformer: typing.Type[AdamsNordsieckTransformer]
    AdaptiveStepsizeIntegrator: typing.Type[AdaptiveStepsizeIntegrator]
    ClassicalRungeKuttaIntegrator: typing.Type[ClassicalRungeKuttaIntegrator]
    DormandPrince54Integrator: typing.Type[DormandPrince54Integrator]
    DormandPrince853Integrator: typing.Type[DormandPrince853Integrator]
    EmbeddedRungeKuttaIntegrator: typing.Type[EmbeddedRungeKuttaIntegrator]
    EulerIntegrator: typing.Type[EulerIntegrator]
    GillIntegrator: typing.Type[GillIntegrator]
    GraggBulirschStoerIntegrator: typing.Type[GraggBulirschStoerIntegrator]
    HighamHall54Integrator: typing.Type[HighamHall54Integrator]
    MidpointIntegrator: typing.Type[MidpointIntegrator]
    RungeKutta6Integrator: typing.Type[RungeKutta6Integrator]
    RungeKutta6StepInterpolator: typing.Type[RungeKutta6StepInterpolator]
    RungeKuttaIntegrator: typing.Type[RungeKuttaIntegrator]
    RungeKuttaStepInterpolator: typing.Type[RungeKuttaStepInterpolator]
    ThreeEighthesIntegrator: typing.Type[ThreeEighthesIntegrator]
    cowell: fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.__module_protocol__
