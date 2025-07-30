
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.attitudes.multi
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.sampling.multi
import fr.cnes.sirius.patrius.time
import java.util
import typing



class MultiAnalyticalPropagator(fr.cnes.sirius.patrius.propagation.MultiPropagator):
    """
    public class MultiAnalyticalPropagator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
    
    
        This class is inspired from :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator` and adapted to multi
        propagation.
    
        This class propagates N :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState` using analytical propagators (any
        non-numerical propagator is accepted). Each state is identified with an ID of type String.
    
        Multi spacecraft analytical propagation requires at least one satellite to be added to the propagator using
        :meth:`~fr.cnes.sirius.patrius.propagation.analytical.multi.MultiAnalyticalPropagator.addPropagator`.
    
        The following general parameters can also be set :
    
          - the discrete events that should be triggered during propagation
            (:meth:`~fr.cnes.sirius.patrius.propagation.analytical.multi.MultiAnalyticalPropagator.addEventDetector`,
            :meth:`~fr.cnes.sirius.patrius.propagation.analytical.multi.MultiAnalyticalPropagator.clearEventsDetectors`)
          - the binding logic with the rest of the application
            (:meth:`~fr.cnes.sirius.patrius.propagation.analytical.multi.MultiAnalyticalPropagator.setSlaveMode`,
            :meth:`~fr.cnes.sirius.patrius.propagation.analytical.multi.MultiAnalyticalPropagator.setMasterMode`,
            :meth:`~fr.cnes.sirius.patrius.propagation.analytical.multi.MultiAnalyticalPropagator.setMasterMode`)
    
    
        **Important notes**:
    
          - trying to add an instance of :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator` is forbidden but
            any other class based on analytical (e.g. :class:`~fr.cnes.sirius.patrius.propagation.precomputed.Ephemeris`) or
            semi-analytical (e.g. STELA) propagation is accepted, that is to say all implementations of
            :class:`~fr.cnes.sirius.patrius.propagation.Propagator` except
            :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator`
          - the ephemeris mode is not implemented in this propagator (not useful as of 4.14)
          - the use of a :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector` is *not* possible through
            :meth:`~fr.cnes.sirius.patrius.propagation.analytical.multi.MultiAnalyticalPropagator.addEventDetector`, but can be used
            with :meth:`~fr.cnes.sirius.patrius.propagation.analytical.multi.MultiAnalyticalPropagator.addEventDetector` under the
            condition that it also implements :class:`~fr.cnes.sirius.patrius.events.EventDetector`
          - methods linked to these points throw a :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException` with an
            :meth:`~fr.cnes.sirius.patrius.utils.exception.PatriusMessages.ILLEGAL_STATE` message
    
    
        The same instance cannot be used simultaneously by different threads, the class is *not* thread-safe.
    
        Since:
            4.14
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`,
            :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`,
            :class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepHandler`,
            :class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusFixedStepHandler`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.Propagator], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.Propagator]], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def addEventDetector(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, string: str) -> None:
        """
            Add an event detector to a specific spacecraft. The spacecraft defined by the input ID should already be added using
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addEventDetector` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                detector (:class:`~fr.cnes.sirius.patrius.events.EventDetector`): event detector to add
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.clearEventsDetectors`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getEventsDetectors`
        
        
        """
        ...
    @typing.overload
    def addEventDetector(self, multiEventDetector: fr.cnes.sirius.patrius.events.MultiEventDetector) -> None:
        """
            Not authorized method: throws an unchecked exception when called.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addEventDetector` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                detector (:class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`): event detector to add
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.clearEventsDetectors`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getEventsDetectors`
        
        """
        ...
    def addInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, string: str) -> None: ...
    def addPropagator(self, propagator: fr.cnes.sirius.patrius.propagation.Propagator, string: str) -> None: ...
    def clearEventsDetectors(self) -> None:
        """
            Remove all events detectors.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.clearEventsDetectors` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addEventDetector`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addEventDetector`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getEventsDetectors`
        
        
        """
        ...
    def getAttitudeProvider(self, string: str) -> fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider:
        """
        
            Get the default attitude provider.
        
            The unique attitude provider given by default is returned. If null, the attitude provider for forces computation, and
            then the attitude provider for events computation is returned.
        
            **Warning: if you provided an :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider` then to get back your
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`, the returned
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider` should be cast to
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper` and method
            :meth:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper.getAttitudeProvider` should be used.**
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getAttitudeProvider` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                attitude provider for forces computation (by default)
        
        
        """
        ...
    def getAttitudeProviderEvents(self, string: str) -> fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider:
        """
        
            Get the attitude provider for events computation.
        
            **Warning: if you provided an :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider` then to get back your
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`, the returned
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider` should be cast to
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper` and method
            :meth:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper.getAttitudeProvider` should be used.**
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getAttitudeProviderEvents` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                attitude provider for events computation, return null if not defined.
        
        
        """
        ...
    def getAttitudeProviderForces(self, string: str) -> fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider:
        """
        
            Get the attitude provider for forces computation.
        
            **Warning: if you provided an :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider` then to get back your
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`, the returned
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider` should be cast to
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper` and method
            :meth:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper.getAttitudeProvider` should be used.**
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getAttitudeProviderForces` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                attitude provider for forces computation, return null if not defined.
        
        
        """
        ...
    def getEventsDetectors(self) -> java.util.Collection[fr.cnes.sirius.patrius.events.MultiEventDetector]: ...
    def getFrame(self, string: str) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the frame in which the orbit is propagated.
        
            The propagation frame is the definition frame of the initial state, so this method should be called after this state has
            been set.
        
            The spacecraft defined by the input ID should already be added using
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getFrame` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                frame in which the orbit is propagated
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`
        
        
        """
        ...
    def getGeneratedEphemeris(self, string: str) -> fr.cnes.sirius.patrius.propagation.BoundedPropagator:
        """
            Not authorized method: throws an unchecked exception when called.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getGeneratedEphemeris` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                generated ephemeris
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`
        
        
        """
        ...
    def getInitialState(self, string: str) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def getInitialStates(self) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    def getMode(self) -> int:
        """
            Get the current operating mode of the propagator.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getMode` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Returns:
                one of :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.SLAVE_MODE`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.MASTER_MODE`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.EPHEMERIS_GENERATION_MODE`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`
        
        
        """
        ...
    def getPropagators(self) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftStateProvider]: ...
    def getReferenceDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the reference date.
        
            Returns:
                the reference date
        
        
        """
        ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    def resetSingleInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, string: str) -> None:
        """
            Reset the initial state of a single satellite in the initial states map.
        
            Parameters:
                newSpacecraftState (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): new spacecraft state that shall be set
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): satellite ID whose state shall be reseted
        
        
        """
        ...
    def setAttitudeProvider(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, string: str) -> None:
        """
        
            Set attitude provider for defined spacecraft.
        
            A default attitude provider is available in :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            The spacecraft defined by the input ID should already be added using
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setAttitudeProvider` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                attitudeProvider (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
        
        """
        ...
    def setAttitudeProviderEvents(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, string: str) -> None:
        """
        
            Set attitude provider for events computation.
        
            A default attitude provider is available in :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            The spacecraft defined by the input ID should already be added using
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setAttitudeProviderEvents` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                attitudeProviderEvents (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider for events computation
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
        
        """
        ...
    def setAttitudeProviderForces(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, string: str) -> None:
        """
        
            Set attitude provider for forces computation.
        
            A default attitude provider is available in :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            The spacecraft defined by the input ID should already be added using
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setAttitudeProviderForces` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                attitudeProviderForces (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider for forces computation
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
        
        """
        ...
    def setEphemerisMode(self) -> None:
        """
            Not authorized method: throws an unchecked exception when called.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getGeneratedEphemeris`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.EPHEMERIS_GENERATION_MODE`
        
        
        """
        ...
    @typing.overload
    def setMasterMode(self, double: float, multiPatriusFixedStepHandler: fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusFixedStepHandler) -> None:
        """
            Set the propagator to master mode with fixed steps.
        
            This mode is used when the user needs to have some custom function called at the end of each finalized step during
            integration. The (master) propagator integration loop calls the (slave) application callback methods at each finalized
            step.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                h (double): fixed stepsize (s)
                handler (:class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusFixedStepHandler`): handler called at the end of each finalized step
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.MASTER_MODE`
        
        """
        ...
    @typing.overload
    def setMasterMode(self, multiPatriusStepHandler: fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepHandler) -> None:
        """
            Set the propagator to master mode with variable steps.
        
            This mode is used when the user needs to have some custom function called at the end of each finalized step during
            integration. The (master) propagator integration loop calls the (slave) application callback methods at each finalized
            step.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Parameters:
                handler (:class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepHandler`): handler called at the end of each finalized step
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.MASTER_MODE`
        
        
        """
        ...
    def setSlaveMode(self) -> None:
        """
            Set the propagator to slave mode.
        
            This mode is used when the user needs only the final orbit at the target time. The (slave) propagator computes this
            result and return it to the calling (master) application, without any intermediate feedback.
        
            This is the default mode.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setSlaveMode` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.SLAVE_MODE`
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation.analytical.multi")``.

    MultiAnalyticalPropagator: typing.Type[MultiAnalyticalPropagator]
