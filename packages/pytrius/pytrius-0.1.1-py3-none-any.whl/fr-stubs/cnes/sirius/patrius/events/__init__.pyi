
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.events.detectors
import fr.cnes.sirius.patrius.events.postprocessing
import fr.cnes.sirius.patrius.events.utils
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import typing



class EventDetector(java.io.Serializable):
    """
    public interface EventDetector extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface represents space-dynamics aware events detectors with support for additional states.
    
        It mirrors the :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler` interface from ` commons-math
        <http://commons.apache.org/math/>` but provides a space-dynamics interface to the methods.
    
        Events detectors are a useful solution to meet the requirements of propagators concerning discrete conditions. The state
        of each event detector is queried by the integrator at each step. When the sign of the underlying g switching function
        changes, the step is rejected and reduced, in order to make sure the sign changes occur only at steps boundaries.
    
        When step ends exactly at a switching function sign change, the corresponding event is triggered, by calling the
        :meth:`~fr.cnes.sirius.patrius.events.EventDetector.eventOccurred` method. The method can do whatever it needs with the
        event (logging it, performing some processing, ignore it ...). The return value of the method will be used by the
        propagator to stop or resume propagation, possibly changing the state vector or the future event detection.
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
    def copy(self) -> 'EventDetector':
        """
            A copy of the detector. By default copy is deep. If not, detector javadoc will specify which attribute is not fully
            copied. In that case, the attribute reference is passed.
        
            Returns:
                a copy of the detector.
        
        
        """
        ...
    def eventOccurred(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool, boolean2: bool) -> 'EventDetector.Action': ...
    def filterEvent(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool, boolean2: bool) -> bool: ...
    def g(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    def getMaxCheckInterval(self) -> float:
        """
            Get maximal time interval between switching function checks.
        
            Returns:
                maximal time interval (s) between switching function checks
        
        
        """
        ...
    def getMaxIterationCount(self) -> int:
        """
            Get maximal number of iterations in the event time search.
        
            Returns:
                maximal number of iterations in the event time search
        
        
        """
        ...
    def getSlopeSelection(self) -> int:
        """
            Get the parameter in charge of the selection of detected events by the slope of the g-function.
        
            Returns:
                EventDetector.INCREASING (0): events related to the increasing g-function;
        
        
                EventDetector.DECREASING (1): events related to the decreasing g-function;
        
        
                EventDetector.INCREASING_DECREASING (2): events related to both increasing and decreasing g-function.
        
        
        """
        ...
    def getThreshold(self) -> float:
        """
            Get the convergence threshold in the event time search.
        
            Returns:
                convergence threshold (s)
        
        
        """
        ...
    def init(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def resetState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def shouldBeRemoved(self) -> bool:
        """
            This method is called after :meth:`~fr.cnes.sirius.patrius.events.EventDetector.eventOccurred` has been triggered. It
            returns true if the current detector should be removed after first event detection. **WARNING:** this method can be
            called only once a event has been triggered. Before, the value is not available.
        
            Returns:
                true if the current detector should be removed after first event detection
        
        
        """
        ...
    class Action(java.lang.Enum['EventDetector.Action']):
        STOP: typing.ClassVar['EventDetector.Action'] = ...
        RESET_STATE: typing.ClassVar['EventDetector.Action'] = ...
        RESET_DERIVATIVES: typing.ClassVar['EventDetector.Action'] = ...
        CONTINUE: typing.ClassVar['EventDetector.Action'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'EventDetector.Action': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['EventDetector.Action']: ...

class MultiEventDetector:
    """
    public interface MultiEventDetector
    
    
        This interface is copied from :class:`~fr.cnes.sirius.patrius.events.EventDetector` and adapted to multi propagation.
    
        This interface represents space-dynamics aware events detectors.
    
        It mirrors the :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler` interface from ` commons-math
        <http://commons.apache.org/math/>` but provides a space-dynamics interface to the methods.
    
        Events detectors are a useful solution to meet the requirements of propagators concerning discrete conditions. The state
        of each event detector is queried by the integrator at each step. When the sign of the underlying g switching function
        changes, the step is rejected and reduced, in order to make sure the sign changes occur only at steps boundaries.
    
        When step ends exactly at a switching function sign change, the corresponding event is triggered, by calling the
        :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.eventOccurred` method. The method can do whatever it needs with
        the event (logging it, performing some processing, ignore it ...). The return value of the method will be used by the
        propagator to stop or resume propagation, possibly changing the state vector or the future event detection.
    
        Since:
            3.0
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
    def eventOccurred(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool, boolean2: bool) -> EventDetector.Action: ...
    def filterEvent(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool, boolean2: bool) -> bool: ...
    def g(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]]) -> float: ...
    def getMaxCheckInterval(self) -> float:
        """
            Get maximal time interval between switching function checks.
        
            Returns:
                maximal time interval (s) between switching function checks
        
        
        """
        ...
    def getMaxIterationCount(self) -> int:
        """
            Get maximal number of iterations in the event time search.
        
            Returns:
                maximal number of iterations in the event time search
        
        
        """
        ...
    def getSlopeSelection(self) -> int:
        """
            Get the parameter in charge of the selection of detected events by the slope of the g-function.
        
            Returns:
                EventDetector.INCREASING (0): events related to the increasing g-function;
        
        
                EventDetector.DECREASING (1): events related to the decreasing g-function;
        
        
                EventDetector.INCREASING_DECREASING (2): events related to both increasing and decreasing g-function.
        
        
        """
        ...
    def getThreshold(self) -> float:
        """
            Get the convergence threshold in the event time search.
        
            Returns:
                convergence threshold (s)
        
        
        """
        ...
    def init(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def resetStates(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]]) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    def shouldBeRemoved(self) -> bool:
        """
        
            This method is called after the step handler has returned and before the next step is started, but only when
            :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.eventOccurred` has been called.
        
            Returns:
                true if the current detector should be removed
        
        
        """
        ...

class AbstractDetector(EventDetector):
    """
    public abstract class AbstractDetector extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.EventDetector`
    
        Common parts shared by several events finders. A default implementation of most of the methods of EventDetector
        Interface. Make it easier to create a new detector.
    
        Also see:
            :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.addEventDetector`, :meth:`~serialized`
    """
    DEFAULT_MAXCHECK: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_MAXCHECK
    
        Default maximum checking interval (s).
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_THRESHOLD: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_THRESHOLD
    
        Default convergence threshold (s) for the algorithm which searches for the zero of the g function.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_MAXITER: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_MAXITER
    
        Default maximum number of iterations allowed for the algorithm which searches for the zero of the g function.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, action: EventDetector.Action, action2: EventDetector.Action, boolean: bool, boolean2: bool): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, action: EventDetector.Action, boolean: bool): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, action: EventDetector.Action, action2: EventDetector.Action, boolean: bool, boolean2: bool): ...
    def eventOccurred(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool, boolean2: bool) -> EventDetector.Action: ...
    def filterEvent(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool, boolean2: bool) -> bool: ...
    def g(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    def getActionAtEntry(self) -> EventDetector.Action:
        """
        
            Returns:
                the action at entry
        
        
        """
        ...
    def getActionAtExit(self) -> EventDetector.Action:
        """
        
            Returns:
                the action at exit
        
        
        """
        ...
    def getMaxCheckInterval(self) -> float:
        """
            Get maximal time interval between switching function checks.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.getMaxCheckInterval` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Returns:
                maximal time interval (s) between switching function checks
        
        
        """
        ...
    def getMaxIterationCount(self) -> int:
        """
            Get maximal number of iterations in the event time search.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.getMaxIterationCount` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Returns:
                maximal number of iterations in the event time search
        
        
        """
        ...
    def getSlopeSelection(self) -> int:
        """
            Get the parameter in charge of the selection of detected events by the slope of the g-function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.getSlopeSelection` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Returns:
                EventDetector.INCREASING (0): events related to the increasing g-function;
        
        
                EventDetector.DECREASING (1): events related to the decreasing g-function;
        
        
                EventDetector.INCREASING_DECREASING (2): events related to both increasing and decreasing g-function.
        
        
        """
        ...
    def getThreshold(self) -> float:
        """
            Get the convergence threshold in the event time search.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.getThreshold` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Returns:
                convergence threshold (s)
        
        
        """
        ...
    def init(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def isRemoveAtEntry(self) -> bool:
        """
        
            Returns:
                the flag removeAtEntry
        
        
        """
        ...
    def isRemoveAtExit(self) -> bool:
        """
        
            Returns:
                the flag removeAtExit
        
        
        """
        ...
    @staticmethod
    def logEventsOverTimeInterval(codedEventsLogger: fr.cnes.sirius.patrius.events.postprocessing.CodedEventsLogger, propagator: fr.cnes.sirius.patrius.propagation.Propagator, codingEventDetector: fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def resetState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def setMaxCheckInterval(self, double: float) -> None:
        """
            Setter for the max check interval.
        
            Parameters:
                maxCheckIn (double): the max check interval to set
        
        
        """
        ...
    def setMaxIter(self, int: int) -> None:
        """
            Set the maximum number of iterations allowed for the algorithm which searches for the zero of the g function.
        
            Parameters:
                maxIterIn (int): maximum number of iterations allowed for the algorithm which searches for the zero of the g function
        
        
        """
        ...
    def shouldBeRemoved(self) -> bool:
        """
            This method is called after :meth:`~fr.cnes.sirius.patrius.events.EventDetector.eventOccurred` has been triggered. It
            returns true if the current detector should be removed after first event detection. **WARNING:** this method can be
            called only once a event has been triggered. Before, the value is not available.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.shouldBeRemoved` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Returns:
                true if the current detector should be removed after first event detection
        
        
        """
        ...

class MultiAbstractDetector(MultiEventDetector):
    """
    public abstract class MultiAbstractDetector extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`
    
    
        This class is copied from :class:`~fr.cnes.sirius.patrius.events.AbstractDetector` and adapted to multi propagation.
    
        Common parts shared by several events finders. A default implementation of most of the methods of
        :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`. Make it easier to create a new detector.
    
        Since:
            3.0
    
        Also see:
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addEventDetector`
    """
    DEFAULT_MAXCHECK: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_MAXCHECK
    
        Default maximum checking interval (s).
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_THRESHOLD: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_THRESHOLD
    
        Default convergence threshold (s).
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_MAX_ITERATION_COUNT: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_MAX_ITERATION_COUNT
    
        Default maximal number of iterations in the event time search.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self, int: int, double: float, double2: float): ...
    def eventOccurred(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool, boolean2: bool) -> EventDetector.Action: ...
    def filterEvent(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool, boolean2: bool) -> bool: ...
    def g(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]]) -> float: ...
    def getMaxCheckInterval(self) -> float:
        """
            Get maximal time interval between switching function checks.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.getMaxCheckInterval` in
                interface :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`
        
            Returns:
                maximal time interval (s) between switching function checks
        
        
        """
        ...
    def getMaxIterationCount(self) -> int:
        """
            Get maximal number of iterations in the event time search.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.getMaxIterationCount` in
                interface :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`
        
            Returns:
                maximal number of iterations in the event time search
        
        
        """
        ...
    def getSlopeSelection(self) -> int:
        """
            Get the parameter in charge of the selection of detected events by the slope of the g-function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.getSlopeSelection` in
                interface :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`
        
            Returns:
                EventDetector.INCREASING (0): events related to the increasing g-function;
        
        
                EventDetector.DECREASING (1): events related to the decreasing g-function;
        
        
                EventDetector.INCREASING_DECREASING (2): events related to both increasing and decreasing g-function.
        
        
        """
        ...
    def getThreshold(self) -> float:
        """
            Get the convergence threshold in the event time search.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.getThreshold` in
                interface :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`
        
            Returns:
                convergence threshold (s)
        
        
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
        
            Returns:
                true if the current detector should be removed
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.events")``.

    AbstractDetector: typing.Type[AbstractDetector]
    EventDetector: typing.Type[EventDetector]
    MultiAbstractDetector: typing.Type[MultiAbstractDetector]
    MultiEventDetector: typing.Type[MultiEventDetector]
    detectors: fr.cnes.sirius.patrius.events.detectors.__module_protocol__
    postprocessing: fr.cnes.sirius.patrius.events.postprocessing.__module_protocol__
    utils: fr.cnes.sirius.patrius.events.utils.__module_protocol__
