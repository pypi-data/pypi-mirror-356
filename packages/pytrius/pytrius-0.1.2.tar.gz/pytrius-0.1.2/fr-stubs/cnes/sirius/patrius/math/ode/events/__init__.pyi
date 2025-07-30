
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis.solver
import fr.cnes.sirius.patrius.math.ode.sampling
import java.lang
import jpype
import typing



class EventHandler:
    """
    public interface EventHandler
    
        This interface represents a handler for discrete events triggered during ODE integration.
    
        Some events can be triggered at discrete times as an ODE problem is solved. This occurs for example when the integration
        process should be stopped as some state is reached (G-stop facility) when the precise date is unknown a priori, or when
        the derivatives have discontinuities, or simply when the user wants to monitor some states boundaries crossings.
    
        These events are defined as occurring when a :code:`g` switching function sign changes.
    
        Since events are only problem-dependent and are triggered by the independent *time* variable and the state vector, they
        can occur at virtually any time, unknown in advance. The integrators will take care to avoid sign changes inside the
        steps, they will reduce the step size when such an event is detected in order to put this event exactly at the end of
        the current step. This guarantees that step interpolation (which always has a one step scope) is relevant even in
        presence of discontinuities. This is independent from the stepsize control provided by integrators that monitor the
        local error (this event handling feature is available for all integrators, including fixed step ones).
    
        Since:
            1.2
    """
    INCREASING: typing.ClassVar[int] = ...
    """
    static final int INCREASING
    
        Increasing g-function related events parameter.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DECREASING: typing.ClassVar[int] = ...
    """
    static final int DECREASING
    
        Decreasing g-function related events parameter.
    
        Also see:
            :meth:`~constant`
    
    
    """
    INCREASING_DECREASING: typing.ClassVar[int] = ...
    """
    static final int INCREASING_DECREASING
    
        Both increasing and decreasing g-function related events parameter.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def eventOccurred(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], boolean: bool, boolean2: bool) -> 'EventHandler.Action':
        """
            Handle an event and choose what to do next.
        
            This method is called when the integrator has accepted a step ending exactly on a sign change of the function, just
            *before* the step handler itself is called (see below for scheduling). It allows the user to update his internal data to
            acknowledge the fact the event has been handled (for example setting a flag in the
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations` to switch the derivatives computation in case
            of discontinuity), or to direct the integrator to either stop or continue integration, possibly with a reset state or
            derivatives.
        
              - if :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.STOP` is returned, the step handler will be called
                with the :code:`isLast` flag of the :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler.handleStep` method set
                to true and the integration will be stopped,
              - if :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.RESET_STATE` is returned, the null method will be
                called once the step handler has finished its task, and the integrator will also recompute the derivatives,
              - if :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.RESET_DERIVATIVES` is returned, the integrator
                will recompute the derivatives,
              - if :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.CONTINUE` is returned, no specific action will be
                taken (apart from having called this method) and integration will continue.
        
        
            The scheduling between this method and the :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler` method
            handleStep() is to call this method first and :code:`handleStep` afterwards. This scheduling allows the integrator to
            pass :code:`true` as the :code:`isLast` parameter to the step handler to make it aware the step will be the last one if
            this method returns :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.STOP`. As the interpolator may be
            used to navigate back throughout the last step (as :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer`
            does for example), user code called by this method and user code called by step handlers may experience apparently out
            of order values of the independent time variable. As an example, if the same user object implements both this
            :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler` interface and the
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.FixedStepHandler` interface, a *forward* integration may call its
            :code:`eventOccurred` method with t = 10 first and call its :code:`handleStep` method with t = 9 afterwards. Such out of
            order calls are limited to the size of the integration step for
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler` and to the size of the fixed step for
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.FixedStepHandler`.
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector
                increasing (boolean): if true, the value of the switching function increases when times increases around event (note that increase is measured
                    with respect to physical time, not with respect to integration which may go backward in time)
                forward (boolean): if true, the integration variable (time) increases during integration
        
            Returns:
                indication of what the integrator should do next, this value must be one of
                :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.STOP`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.RESET_STATE`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.RESET_DERIVATIVES`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.CONTINUE`
        
        
        """
        ...
    def filterEvent(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], boolean: bool, boolean2: bool) -> bool:
        """
            Filter last event: returns true if the last event is a false detection, false otherwise.
        
            This method is called right before null method.
        
            This may be useful in order to filter some events in particular when angles are at stake (see for example
            :class:`~fr.cnes.sirius.patrius.events.detectors.LocalTimeAngleDetector`).
        
            Parameters:
                t (double): event date
                y (double[]): array containing the current value of the state vector
                increasing (boolean): if true, the value of the switching function increases when times increases around event (note that increase is measured
                    with respect to physical time, not with respect to propagation which may go backward in time)
                forward (boolean): if true, the integration variable (time) increases during integration
        
            Returns:
                true if the last event is a false detection, false otherwise
        
        
        """
        ...
    def g(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Compute the value of the switching function.
        
            The discrete events are generated when the sign of this switching function changes. The integrator will take care to
            change the stepsize in such a way these events occur exactly at step boundaries. The switching function must be
            continuous in its roots neighborhood (but not necessarily smooth), as the integrator will need to find its roots to
            locate precisely the events.
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector
        
            Returns:
                value of the g switching function
        
        
        """
        ...
    def getSlopeSelection(self) -> int:
        """
            Get the parameter in charge of the selection of detected events by the slope of the g-function.
        
            Returns:
                EventHandler.INCREASING (0): events related to the increasing g-function;
        
        
                EventHandler.DECREASING (1): events related to the decreasing g-function;
        
        
                EventHandler.INCREASING_DECREASING (2): events related to both increasing and decreasing g-function.
        
        
        """
        ...
    def init(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float) -> None:
        """
            Initialize event handler at the start of an ODE integration.
        
            This method is called once at the start of the integration. It may be used by the event handler to initialize some
            internal data if needed.
        
            Parameters:
                t0 (double): start value of the independent *time* variable
                y0 (double[]): array containing the start value of the state vector
                t (double): target time for the integration
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: thrown if initialization failed
        
        
        """
        ...
    def resetState(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Reset the state prior to continue the integration.
        
            This method is called after the step handler has returned and before the next step is started, but only when null has
            itself returned the :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.RESET_STATE` indicator. It allows
            the user to reset the state vector for the next step, without perturbing the step handler of the finishing step. If the
            null never returns the :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.RESET_STATE` indicator, this
            function will never be called, and it is safe to leave its body empty.
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector the new state should be put in the same array
        
        
        """
        ...
    def shouldBeRemoved(self) -> bool:
        """
        
            This method is called after the step handler has returned and before the next step is started, but only when null has
            been called.
        
            Returns:
                true if the current detector should be removed
        
        
        """
        ...
    class Action(java.lang.Enum['EventHandler.Action']):
        STOP: typing.ClassVar['EventHandler.Action'] = ...
        RESET_STATE: typing.ClassVar['EventHandler.Action'] = ...
        RESET_DERIVATIVES: typing.ClassVar['EventHandler.Action'] = ...
        CONTINUE: typing.ClassVar['EventHandler.Action'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'EventHandler.Action': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['EventHandler.Action']: ...

class EventState:
    """
    public class EventState extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class handles the state for one :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler` during integration
        steps.
    
        Each time the integrator proposes a step, the event handler switching function should be checked. This class handles the
        state of one handler during one integration step, with references to the state at the end of the preceding step. This
        information is used to decide if the handler should trigger an event or not during the proposed step.
    
        Since:
            1.2
    """
    def __init__(self, eventHandler: EventHandler, double: float, double2: float, int: int, univariateSolver: fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver): ...
    def cancelStepAccepted(self) -> None:
        """
            Cancel stepAccepted call (does not cancel event). This method is used only when some missed event have occurred: event
            search algorithm goes backward in time, rewriting the future: stepAccepted() call leading to this jump in the past needs
            to be canceled.
        
        """
        ...
    @typing.overload
    def evaluateStep(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> bool:
        """
            Evaluate the impact of the proposed step on the event handler. In that case, the step is of null size (the provided time
            should be equal to t0)
        
            Parameters:
                t (double): current time
                y (double[]): current state
        
            Returns:
                true if the event handler triggers an event before the end of the proposed step
        
        """
        ...
    @typing.overload
    def evaluateStep(self, stepInterpolator: fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator) -> bool:
        """
            Evaluate the impact of the proposed step on the event handler.
        
            Parameters:
                interpolator (:class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`): step interpolator for the proposed step
        
            Returns:
                true if the event handler triggers an event before the end of the proposed step
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the interpolator throws one because the number of functions evaluations is exceeded
                :class:`~fr.cnes.sirius.patrius.math.exception.NoBracketingException`: if the event cannot be bracketed
        
        
        """
        ...
    def getConvergence(self) -> float:
        """
            Get the convergence threshold for event localization.
        
            Returns:
                convergence threshold for event localization
        
        
        """
        ...
    def getEventHandler(self) -> EventHandler:
        """
            Get the underlying event handler.
        
            Returns:
                underlying event handler
        
        
        """
        ...
    def getEventTime(self) -> float:
        """
            Get the occurrence time of the event triggered in the current step.
        
            Returns:
                occurrence time of the event triggered in the current step or infinity if no events are triggered
        
        
        """
        ...
    def getMaxCheckInterval(self) -> float:
        """
            Get the maximal time interval between events handler checks.
        
            Returns:
                maximal time interval between events handler checks
        
        
        """
        ...
    def getMaxIterationCount(self) -> int:
        """
            Get the upper limit in the iteration count for event localization.
        
            Returns:
                upper limit in the iteration count for event localization
        
        
        """
        ...
    def getPreviousEventTime(self) -> float:
        """
            Get previous event time.
        
            Returns:
                previous event time
        
        
        """
        ...
    def getT0(self) -> float:
        """
            Getter for t0.
        
            Returns:
                t0
        
        
        """
        ...
    def isPendingReset(self) -> bool:
        """
            Check if some reset is being triggered.
        
            Returns:
                true is some reset is being triggered
        
        
        """
        ...
    def reinitializeBegin(self, stepInterpolator: fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator) -> None:
        """
            Reinitialize the beginning of the step.
        
            Parameters:
                interpolator (:class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`): valid for the current step
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the interpolator throws one because the number of functions evaluations is exceeded
        
        
        """
        ...
    def removeDetector(self) -> bool:
        """
            Check the current detector should be removed at the end of the current step current step.
        
            Returns:
                true if the detector should be removed
        
        
        """
        ...
    def reset(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> bool:
        """
            Let the event handler reset the state if it wants.
        
            Parameters:
                t (double): value of the independent *time* variable at the beginning of the next step
                y (double[]): array were to put the desired state vector at the beginning of the next step
        
            Returns:
                true if the integrator should reset the derivatives too
        
        
        """
        ...
    def stepAccepted(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Acknowledge the fact the step has been accepted by the integrator.
        
            Parameters:
                t (double): value of the independent *time* variable at the end of the step
                y (double[]): array containing the current value of the state vector at the end of the step
        
        
        """
        ...
    def stop(self) -> bool:
        """
            Check if the integration should be stopped at the end of the current step.
        
            Returns:
                true if the integration should be stopped
        
        
        """
        ...
    def storeState(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], boolean: bool) -> None:
        """
            Store event state with provided time and state.
        
            Parameters:
                t (double): current time
                y (double[]): current state
                forceUpdate (boolean): force update of event parameters
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.ode.events")``.

    EventHandler: typing.Type[EventHandler]
    EventState: typing.Type[EventState]
