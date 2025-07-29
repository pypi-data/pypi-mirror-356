
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.attitudes.multi
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.events.detectors
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.analysis.solver
import fr.cnes.sirius.patrius.math.ode.events
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.propagation.numerical.multi
import fr.cnes.sirius.patrius.propagation.sampling
import fr.cnes.sirius.patrius.propagation.sampling.multi
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



class AdaptedEventDetector(fr.cnes.sirius.patrius.math.ode.events.EventHandler, java.io.Serializable):
    """
    public class AdaptedEventDetector extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Adapt an :class:`~fr.cnes.sirius.patrius.events.EventDetector` to commons-math
        :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler` interface.
    
    
        The implemented classes should A list of :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo` is
        needed, so that the state vector can be translated to/from additional states in a simple and generic manner by
        :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`. Conditionally thread-safe if all attributes are
        thread-safe.
    
    
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo]], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    def eventOccurred(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], boolean: bool, boolean2: bool) -> fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action:
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector
        
            Returns:
                value of the g switching function
        
        
        """
        ...
    def getDetector(self) -> fr.cnes.sirius.patrius.events.EventDetector:
        """
            Get the detector object.
        
            Returns:
                detector
        
        
        """
        ...
    def getSlopeSelection(self) -> int:
        """
            Get the parameter in charge of the selection of detected events by the slope of the g-function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.getSlopeSelection` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Parameters:
                t0 (double): start value of the independent *time* variable
                y0 (double[]): array containing the start value of the state vector
                t (double): target time for the integration
        
        
        """
        ...
    def reinitialize(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo]], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, frame: fr.cnes.sirius.patrius.frames.Frame) -> None: ...
    def resetState(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Reset the state prior to continue the integration.
        
            This method is called after the step handler has returned and before the next step is started, but only when null has
            itself returned the :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.RESET_STATE` indicator. It allows
            the user to reset the state vector for the next step, without perturbing the step handler of the finishing step. If the
            null never returns the :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.RESET_STATE` indicator, this
            function will never be called, and it is safe to leave its body empty.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector the new state should be put in the same array
        
        
        """
        ...
    def shouldBeRemoved(self) -> bool:
        """
        
            This method is called after the step handler has returned and before the next step is started, but only when null has
            been called.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.shouldBeRemoved` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Returns:
                true if the current detector should be removed
        
        
        """
        ...

class AdaptedMonoEventDetector(fr.cnes.sirius.patrius.math.ode.events.EventHandler):
    """
    public class AdaptedMonoEventDetector extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
    
    
        This interface is copied from :class:`~fr.cnes.sirius.patrius.events.utils.AdaptedEventDetector` and adapted to multi
        propagation.
    
        Adapt an :class:`~fr.cnes.sirius.patrius.events.EventDetector` to commons-math
        :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler` interface. A
        :class:`~fr.cnes.sirius.patrius.propagation.numerical.multi.MultiStateVectorInfo` is needed, so that the state vector
        can be translated to/from a map of :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`.
    
        Since:
            3.0
    """
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, multiAttitudeProvider: fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider, multiAttitudeProvider2: fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, multiStateVectorInfo: fr.cnes.sirius.patrius.propagation.numerical.multi.MultiStateVectorInfo, string: str): ...
    @staticmethod
    def convertIntoCMAction(action: fr.cnes.sirius.patrius.events.EventDetector.Action) -> fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action:
        """
            Convert Orekit action into Commons-Math action
        
            Parameters:
                orekitAction (:class:`~fr.cnes.sirius.patrius.events.EventDetector.Action`): orekit action
        
            Returns:
                commons math action
        
        
        """
        ...
    def eventOccurred(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], boolean: bool, boolean2: bool) -> fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action:
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector
        
            Returns:
                value of the g switching function
        
        
        """
        ...
    def getSatId(self) -> str:
        """
            Returns satellite ID.
        
            Returns:
                satellite ID
        
        
        """
        ...
    def getSlopeSelection(self) -> int:
        """
            Get the parameter in charge of the selection of detected events by the slope of the g-function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.getSlopeSelection` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Parameters:
                t0 (double): start value of the independent *time* variable
                y0 (double[]): array containing the start value of the state vector
                t (double): target time for the integration
        
        
        """
        ...
    def reinitialize(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, multiAttitudeProvider: fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider, multiAttitudeProvider2: fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, multiStateVectorInfo: fr.cnes.sirius.patrius.propagation.numerical.multi.MultiStateVectorInfo, string: str) -> None:
        """
            Reinitialize data.
        
            Parameters:
                orbitType (:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`): orbit type
                angleType (:class:`~fr.cnes.sirius.patrius.orbits.PositionAngle`): position angle type
                attProviderForces (:class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider`): attitude provider for forces computation
                attProviderEvents (:class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider`): attitude provider for events computation
                referenceDate (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): reference date from which t is counted
                stateVectorInfo (:class:`~fr.cnes.sirius.patrius.propagation.numerical.multi.MultiStateVectorInfo`): informations about the global state vector
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): spacecraft Id
        
        
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector the new state should be put in the same array
        
        
        """
        ...
    def shouldBeRemoved(self) -> bool:
        """
        
            This method is called after the step handler has returned and before the next step is started, but only when null has
            been called.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.shouldBeRemoved` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Returns:
                true if the current detector should be removed
        
        
        """
        ...

class AdaptedMultiEventDetector(fr.cnes.sirius.patrius.math.ode.events.EventHandler):
    """
    public class AdaptedMultiEventDetector extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
    
    
        This interface is copied from :class:`~fr.cnes.sirius.patrius.events.utils.AdaptedEventDetector` and adapted to multi
        propagation.
    
        Adapt a :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector` to commons-math
        :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler` interface. A
        :class:`~fr.cnes.sirius.patrius.propagation.numerical.multi.MultiStateVectorInfo` is needed, so that the state vector
        can be translated to/from a map of :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`.
    
        Since:
            2.3
    """
    def __init__(self, multiEventDetector: fr.cnes.sirius.patrius.events.MultiEventDetector, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], map2: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, map3: typing.Union[java.util.Map[str, float], typing.Mapping[str, float]], map4: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.frames.Frame], typing.Mapping[str, fr.cnes.sirius.patrius.frames.Frame]], multiStateVectorInfo: fr.cnes.sirius.patrius.propagation.numerical.multi.MultiStateVectorInfo): ...
    def eventOccurred(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], boolean: bool, boolean2: bool) -> fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action:
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector
        
            Returns:
                value of the g switching function
        
        
        """
        ...
    def getMultiDetector(self) -> fr.cnes.sirius.patrius.events.MultiEventDetector:
        """
            Get the multiDetector object.
        
            Returns:
                multiDetector
        
        
        """
        ...
    def getSlopeSelection(self) -> int:
        """
            Get the parameter in charge of the selection of detected events by the slope of the g-function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.getSlopeSelection` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
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
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Parameters:
                t0 (double): start value of the independent *time* variable
                y0 (double[]): array containing the start value of the state vector
                t (double): target time for the integration
        
        
        """
        ...
    def reinitialize(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], map2: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, map3: typing.Union[java.util.Map[str, float], typing.Mapping[str, float]], map4: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.frames.Frame], typing.Mapping[str, fr.cnes.sirius.patrius.frames.Frame]], multiStateVectorInfo: fr.cnes.sirius.patrius.propagation.numerical.multi.MultiStateVectorInfo) -> None: ...
    def resetState(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Reset the state prior to continue the integration.
        
            This method is called after the step handler has returned and before the next step is started, but only when null has
            itself returned the :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.RESET_STATE` indicator. It allows
            the user to reset the state vector for the next step, without perturbing the step handler of the finishing step. If the
            null never returns the :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.Action.RESET_STATE` indicator, this
            function will never be called, and it is safe to leave its body empty.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector the new state should be put in the same array
        
        
        """
        ...
    def shouldBeRemoved(self) -> bool:
        """
        
            This method is called after the step handler has returned and before the next step is started, but only when null has
            been called.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler.shouldBeRemoved` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
        
            Returns:
                true if the current detector should be removed
        
        
        """
        ...

class EventShifter(fr.cnes.sirius.patrius.events.AbstractDetector):
    """
    public class EventShifter extends :class:`~fr.cnes.sirius.patrius.events.AbstractDetector`
    
        Wrapper shifting events occurrences times.
    
        This class wraps an :class:`~fr.cnes.sirius.patrius.events.EventDetector` to slightly shift the events occurrences
        times. A typical use case is for handling operational delays before or after some physical event really occurs.
    
        For example, the satellite attitude mode may be switched from sun pointed to spin-stabilized a few minutes before
        eclipse entry, and switched back to sun pointed a few minutes after eclipse exit. This behavior is handled by wrapping
        an :class:`~fr.cnes.sirius.patrius.events.detectors.EclipseDetector` into an instance of this class with a positive
        times shift for increasing events (eclipse exit) and a negative times shift for decreasing events (eclipse entry).
    
        Also see:
            :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.addEventDetector`,
            :class:`~fr.cnes.sirius.patrius.events.EventDetector`, :meth:`~serialized`
    """
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, boolean: bool, double: float, double2: float): ...
    def copy(self) -> fr.cnes.sirius.patrius.events.EventDetector:
        """
            A copy of the detector. By default copy is deep. If not, detector javadoc will specify which attribute is not fully
            copied. In that case, the attribute reference is passed.
        
            The following attributes are not deeply copied:
        
              - topo: :class:`~fr.cnes.sirius.patrius.frames.TopocentricFrame`
        
        
            Returns:
                a copy of the detector.
        
        
        """
        ...
    def eventOccurred(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool, boolean2: bool) -> fr.cnes.sirius.patrius.events.EventDetector.Action: ...
    def g(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    def getDecreasingTimeShift(self) -> float:
        """
            Get the decreasing events time shift.
        
            Returns:
                decreasing events time shift
        
        
        """
        ...
    def getIncreasingTimeShift(self) -> float:
        """
            Get the increasing events time shift.
        
            Returns:
                increasing events time shift
        
        
        """
        ...
    def init(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def shouldBeRemoved(self) -> bool:
        """
            This method is called after :meth:`~fr.cnes.sirius.patrius.events.EventDetector.eventOccurred` has been triggered. It
            returns true if the current detector should be removed after first event detection. **WARNING:** this method can be
            called only once a event has been triggered. Before, the value is not available.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.shouldBeRemoved` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.events.AbstractDetector.shouldBeRemoved` in
                class :class:`~fr.cnes.sirius.patrius.events.AbstractDetector`
        
            Returns:
                true if the current detector should be removed after first event detection
        
        
        """
        ...

class EventState(java.io.Serializable):
    """
    public class EventState extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class handles the state for one :class:`~fr.cnes.sirius.patrius.events.EventDetector` during integration steps.
    
        This class is heavily based on the class with the same name from the Apache commons-math library. The changes performed
        consist in replacing raw types (double and double arrays) with space dynamics types
        (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`).
    
        Each time the propagator proposes a step, the event detector should be checked. This class handles the state of one
        detector during one propagation step, with references to the state at the end of the preceding step. This information is
        used to determine if the detector should trigger an event or not during the proposed step (and hence the step should be
        reduced to ensure the event occurs at a bound rather than inside the step).
    
        See Orekit issue 110 for more information. Default constructor changed in order to instanciate a bracketing solver, to
        solve the bracketing exception.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, univariateSolver: fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver, string: str): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, string: str): ...
    def cancelStepAccepted(self) -> None:
        """
            Cancel stepAccepted call (does not cancel event). This method is used only when some missed event have occurred: event
            search algorithm goes backward in time, rewriting the future: stepAccepted() call leading to this jump in the past needs
            to be canceled.
        
        """
        ...
    @typing.overload
    def evaluateStep(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> bool: ...
    @typing.overload
    def evaluateStep(self, patriusStepInterpolator: fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator) -> bool: ...
    @typing.overload
    def evaluateStep(self, multiPatriusStepInterpolator: fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator, string: str) -> bool: ...
    def getEventDetector(self) -> fr.cnes.sirius.patrius.events.EventDetector:
        """
            Get the underlying event detector.
        
            Returns:
                underlying event detector
        
        
        """
        ...
    def getEventTime(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the occurrence time of the event triggered in the current step.
        
            Returns:
                occurrence time of the event triggered in the current step.
        
        
        """
        ...
    def getSpacecraftId(self) -> str:
        """
            Get the identifier of the spacecraft.
        
            Returns:
                the identifier of the spacecraft
        
        
        """
        ...
    def getT0(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
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
    def reinitializeBegin(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    def removeDetector(self) -> bool:
        """
            Check if the current detector should be removed at the end of the current step.
        
            Returns:
                true if the detector should be removed
        
        
        """
        ...
    def reset(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def stepAccepted(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    def stop(self) -> bool:
        """
            Check if the propagation should be stopped at the end of the current step.
        
            Returns:
                true if the propagation should be stopped
        
        
        """
        ...
    def storeState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool) -> None: ...

class OneSatEventDetectorWrapper(fr.cnes.sirius.patrius.events.MultiAbstractDetector):
    """
    public class OneSatEventDetectorWrapper extends :class:`~fr.cnes.sirius.patrius.events.MultiAbstractDetector`
    
    
        This class allows to convert an :class:`~fr.cnes.sirius.patrius.events.EventDetector` into a
        :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`. The :class:`~fr.cnes.sirius.patrius.events.EventDetector` is
        associated with a single spacecraft identified by its ID.
    
        Since:
            3.0
    
        Also see:
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addEventDetector`
    """
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, string: str): ...
    def eventOccurred(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool, boolean2: bool) -> fr.cnes.sirius.patrius.events.EventDetector.Action: ...
    def filterEvent(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool, boolean2: bool) -> bool: ...
    @typing.overload
    def g(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    @typing.overload
    def g(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]]) -> float: ...
    def getID(self) -> str:
        """
            Returns the ID of the spacecraft associated with the detector.
        
            Returns:
                the ID of the spacecraft associated with the detector
        
        
        """
        ...
    def init(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def resetStates(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]]) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    def shouldBeRemoved(self) -> bool:
        """
        
            This method is called after the step handler has returned and before the next step is started, but only when
            :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.eventOccurred` has been called.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.shouldBeRemoved` in
                interface :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.MultiAbstractDetector.shouldBeRemoved` in
                class :class:`~fr.cnes.sirius.patrius.events.MultiAbstractDetector`
        
            Returns:
                true if the current detector should be removed
        
        
        """
        ...

class SignalPropagationWrapperDetector(fr.cnes.sirius.patrius.events.EventDetector):
    def __init__(self, abstractSignalPropagationDetector: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector): ...
    def copy(self) -> fr.cnes.sirius.patrius.events.EventDetector: ...
    def eventOccurred(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool, boolean2: bool) -> fr.cnes.sirius.patrius.events.EventDetector.Action: ...
    def filterEvent(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool, boolean2: bool) -> bool: ...
    def g(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    def getEmitterDatesList(self) -> java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate]: ...
    def getEmitterDatesMap(self) -> java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDate, fr.cnes.sirius.patrius.time.AbsoluteDate]: ...
    def getEventDatationType(self) -> fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.EventDatationType: ...
    def getMaxCheckInterval(self) -> float: ...
    def getMaxIterationCount(self) -> int: ...
    def getNBOccurredEvents(self) -> int: ...
    def getReceiverDatesList(self) -> java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate]: ...
    def getReceiverDatesMap(self) -> java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDate, fr.cnes.sirius.patrius.time.AbsoluteDate]: ...
    def getSlopeSelection(self) -> int: ...
    def getThreshold(self) -> float: ...
    def getWrappedDetector(self) -> fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector: ...
    def init(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def resetState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def shouldBeRemoved(self) -> bool: ...
    def toString(self) -> str: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.events.utils")``.

    AdaptedEventDetector: typing.Type[AdaptedEventDetector]
    AdaptedMonoEventDetector: typing.Type[AdaptedMonoEventDetector]
    AdaptedMultiEventDetector: typing.Type[AdaptedMultiEventDetector]
    EventShifter: typing.Type[EventShifter]
    EventState: typing.Type[EventState]
    OneSatEventDetectorWrapper: typing.Type[OneSatEventDetectorWrapper]
    SignalPropagationWrapperDetector: typing.Type[SignalPropagationWrapperDetector]
