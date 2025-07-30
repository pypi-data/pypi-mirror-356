
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.events.detectors
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import typing



class CodedEvent(fr.cnes.sirius.patrius.time.TimeStamped, java.lang.Comparable['CodedEvent'], java.io.Serializable):
    """
    public final class CodedEvent extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        This class represents an event occurrence.
    
    
        An event is identified by a code (its name), the date of occurrence, a string representing a comment and a flag that
        indicates if the event is a "starting" event (i.e. an event that starts a phenomenon, like an eclipse) or an "ending"
        event.
    
    
        Coded events are built by the :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector` during
        propagation using the :meth:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector.buildCodedEvent` method.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector`,
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEventsList`, :meth:`~serialized`
    """
    def __init__(self, string: str, string2: str, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool): ...
    @staticmethod
    def buildUndefinedEvent(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'CodedEvent':
        """
            Factory method for an undefined event, that still has a valid date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` of the event, needed even for an undefined event.
                isStarting (boolean): true when the event is a "starting" event.
        
            Returns:
                a new :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`.
        
        
        """
        ...
    def compareTo(self, codedEvent: 'CodedEvent') -> int:
        """
            Compares two :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` instances.
        
        
            The ordering for :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` is consistent with equals, so that a
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` can be used in any `null
            <http://docs.oracle.com/javase/8/docs/api/java/util/SortedSet.html?is-external=true>` or `null
            <http://docs.oracle.com/javase/8/docs/api/java/util/SortedMap.html?is-external=true>`.
        
        
            The ordering is :
        
              - the ordering of the events' dates if they differ.
              - if not, the alphabetical ordering of the code is used if they differ.
              - if not, the alphabetical ordering of the comment is used if they differ.
              - if not, the starting boolean is used (the starting event is "before").
        
        
            Specified by:
                 in interface 
        
            Parameters:
                event (:class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`): the :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` to compare to
        
            Returns:
                a negative integer, zero, or a positive integer as the :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`
                is before, simultaneous, or after the specified event.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true#compareTo-T->`
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
            Checks if the instance represents the same :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` as another
            instance.
        
            Overrides:
                 in class 
        
            Parameters:
                event (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): other event
        
            Returns:
                true if the instance and the other event are equals
        
        
        """
        ...
    def getCode(self) -> str:
        """
        
            Returns:
                the code of the event.
        
        
        """
        ...
    def getComment(self) -> str:
        """
        
            Returns:
                the comment of the event.
        
        
        """
        ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate`
            Get the date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` of the event.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate`
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def isStartingEvent(self) -> bool:
        """
        
            Returns:
                true if the event is a "starting" event or false if the event is a "ending" event.
        
        
        """
        ...
    def toString(self) -> str:
        """
            Provides a String representation, based on this pattern : "<date> - <(Beg) or (End)> - <code> : <comment>".
        
        
            (Beg) is for a starting event, (End) for an ending event.
        
            Overrides:
                 in class 
        
            Returns:
                the String representation
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#toString-->`
        
        
        """
        ...

class CodedEventsList:
    """
    public final class CodedEventsList extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
    
        This class represents a list of objects :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`.
    
    
        One or more lists of coded events are created during propagation when
        :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector` is used, via the
        :meth:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEventsLogger.monitorDetector` method.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`
    """
    def __init__(self): ...
    def add(self, codedEvent: CodedEvent) -> None:
        """
            Add a :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` to the list.
        
            Parameters:
                codedEvent (:class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`): the element to add.
        
        
        """
        ...
    def getEvents(self, string: str, string2: str, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.Set[CodedEvent]: ...
    def getList(self) -> java.util.List[CodedEvent]: ...
    def remove(self, codedEvent: CodedEvent) -> bool:
        """
            Remove a :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` to the list.
        
            Parameters:
                codedEvent (:class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`): the element to remove.
        
            Returns:
                true if the set contains the coded event that has to be removed.
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class CodedEventsLogger:
    def __init__(self): ...
    def buildCodedEventListMap(self) -> java.util.Map['CodingEventDetector', CodedEventsList]: ...
    def buildPhenomenaListMap(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> java.util.Map['CodingEventDetector', 'PhenomenaList']: ...
    def getCodedEventsList(self) -> CodedEventsList: ...
    def getLoggedCodedEventSet(self) -> java.util.SortedSet['CodedEventsLogger.LoggedCodedEvent']: ...
    def monitorDetector(self, codingEventDetector: 'CodingEventDetector') -> fr.cnes.sirius.patrius.events.EventDetector: ...
    class LoggedCodedEvent(fr.cnes.sirius.patrius.time.TimeStamped, java.lang.Comparable['CodedEventsLogger.LoggedCodedEvent']):
        def compareTo(self, loggedCodedEvent: 'CodedEventsLogger.LoggedCodedEvent') -> int: ...
        def equals(self, object: typing.Any) -> bool: ...
        def getCodedEvent(self) -> CodedEvent: ...
        def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
        def getDetector(self) -> 'CodingEventDetector': ...
        def getState(self) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
        def hashCode(self) -> int: ...
        def isIncreasing(self) -> bool: ...

class CodingEventDetector(fr.cnes.sirius.patrius.events.EventDetector):
    def buildCodedEvent(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool) -> CodedEvent: ...
    def buildDelayedCodedEvent(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool) -> CodedEvent: ...
    def buildOccurrenceCodedEvent(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool) -> CodedEvent: ...
    def getEventType(self) -> str: ...
    def getPhenomenonCode(self) -> str: ...
    def positiveSignMeansActive(self) -> bool: ...

class EventsLogger(java.io.Serializable):
    """
    public class EventsLogger extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class logs events detectors events during propagation.
    
        As :class:`~fr.cnes.sirius.patrius.events.EventDetector` are triggered during orbit propagation, an event specific
        :meth:`~fr.cnes.sirius.patrius.events.EventDetector.eventOccurred` method is called. This class can be used to add a
        global logging feature registering all events with their corresponding states in a chronological sequence (or
        reverse-chronological if propagation occurs backward).
    
        This class works by wrapping user-provided :class:`~fr.cnes.sirius.patrius.events.EventDetector` before they are
        registered to the propagator. The wrapper monitor the calls to
        :meth:`~fr.cnes.sirius.patrius.events.EventDetector.eventOccurred` and store the corresponding events as
        :class:`~fr.cnes.sirius.patrius.events.postprocessing.EventsLogger.LoggedEvent` instances. After propagation is
        complete, the user can retrieve all the events that have occured at once by calling method
        :meth:`~fr.cnes.sirius.patrius.events.postprocessing.EventsLogger.getLoggedEvents`.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def clearLoggedEvents(self) -> None:
        """
            Clear the logged events.
        
        """
        ...
    def getLoggedEvents(self) -> java.util.List['EventsLogger.LoggedEvent']: ...
    def monitorDetector(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector) -> fr.cnes.sirius.patrius.events.EventDetector:
        """
            Monitor an event detector.
        
            In order to monitor an event detector, it must be wrapped thanks to this method as follows:
        
            .. code-block: java
            
            
             Propagator propagator = new XyzPropagator(...);
             EventsLogger logger = new EventsLogger();
             EventDetector detector = new UvwDetector(...);
             propagator.addEventDetector(logger.monitorDetector(detector));
             
        
            Note that the event detector returned by the
            :meth:`~fr.cnes.sirius.patrius.events.postprocessing.EventsLogger.LoggedEvent.getEventDetector` method in
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.EventsLogger.LoggedEvent` instances returned by
            :meth:`~fr.cnes.sirius.patrius.events.postprocessing.EventsLogger.getLoggedEvents` are the :code:`monitoredDetector`
            instances themselves, not the wrapping detector returned by this method.
        
            Parameters:
                monitoredDetector (:class:`~fr.cnes.sirius.patrius.events.EventDetector`): event detector to monitor
        
            Returns:
                the wrapping detector to add to the propagator
        
        
        """
        ...
    class LoggedEvent(java.io.Serializable):
        def getEventDate(self, eventDatationType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.EventDatationType) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
        def getEventDetector(self) -> fr.cnes.sirius.patrius.events.EventDetector: ...
        def getState(self) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
        def isIncreasing(self) -> bool: ...

class MultiCodedEventsLogger:
    """
    public class MultiCodedEventsLogger extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
    
        This class is copied from :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEventsLogger` and adapted to multi
        propagation.
    
        This class logs coded events during multi propagation. It is based on the
        :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiEventsLogger` class in Patrius.
    
        This class works by wrapping user-provided
        :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector` before they are registered to the multi
        propagator. The wrapper monitors the calls to :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.eventOccurred`
        and store the corresponding events as
        :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodedEventsLogger.MultiLoggedCodedEvent` instances. After
        propagation is complete, the user can retrieve all the events that have occurred at once by calling methods
        :meth:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodedEventsLogger.getCodedEventsList` or
        :meth:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodedEventsLogger.getLoggedCodedEventSet`.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiEventsLogger`,
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector`
    """
    def __init__(self): ...
    def buildCodedEventListMap(self) -> java.util.Map['MultiCodingEventDetector', CodedEventsList]: ...
    def buildPhenomenaListMap(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]]) -> java.util.Map['MultiCodingEventDetector', 'PhenomenaList']: ...
    def getCodedEventsList(self) -> CodedEventsList:
        """
            Gets the :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEventsList`. This method can be called after
            propagation to get the list of detected events.
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEventsList`.
        
        
        """
        ...
    def getLoggedCodedEventSet(self) -> java.util.SortedSet['MultiCodedEventsLogger.MultiLoggedCodedEvent']: ...
    def monitorDetector(self, multiCodingEventDetector: 'MultiCodingEventDetector') -> fr.cnes.sirius.patrius.events.MultiEventDetector:
        """
            Takes a :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector` instance and returns an
            :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector` instance that will trigger this
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodedEventsLogger` every time
            :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.eventOccurred` is called. The returned
            :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector` is meant to be provided to a propagator.
        
            Parameters:
                detector (:class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector`): the wrapped :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector`
        
            Returns:
                a wrapper for the parameter, as an :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`.
        
        
        """
        ...
    class MultiLoggedCodedEvent(fr.cnes.sirius.patrius.time.TimeStamped, java.lang.Comparable['MultiCodedEventsLogger.MultiLoggedCodedEvent']):
        def compareTo(self, multiLoggedCodedEvent: 'MultiCodedEventsLogger.MultiLoggedCodedEvent') -> int: ...
        def equals(self, object: typing.Any) -> bool: ...
        def getCodedEvent(self) -> CodedEvent: ...
        def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
        def getMultiDetector(self) -> 'MultiCodingEventDetector': ...
        def getStates(self) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
        def hashCode(self) -> int: ...
        def isIncreasing(self) -> bool: ...

class MultiCodingEventDetector(fr.cnes.sirius.patrius.events.MultiEventDetector):
    """
    public interface MultiCodingEventDetector extends :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`
    
    
        This class is copied from :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector` and adapted to
        multi propagation.
    
        This interface represents a multi event detector that is able to build a
        :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` object.
    
        A :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector` can be used during propagation when we
        want to log the occurred events.
    
    
        These events are detected by the :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector` that has been specified when
        creating the :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector`.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`
    """
    def buildCodedEvent(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool) -> CodedEvent: ...
    def buildDelayedCodedEvent(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool) -> CodedEvent: ...
    def buildOccurrenceCodedEvent(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool) -> CodedEvent: ...
    def getEventType(self) -> str:
        """
            Gets a code indicating the type of event we want to log: DELAY when a delay is associated to the logged events with
            respect to the detected events, N_OCCURRENCE when we want to log the nth occurrence of the detected events, STANDARD
            when no delays and no occurrence numbers are taken into consideration.
        
            Returns:
                the type of event to log
        
        
        """
        ...
    def getPhenomenonCode(self) -> str:
        """
            If the implementation supports a :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`, provides a code for
            the phenomenon associated to the event. If not, returns null.
        
            Returns:
                either a code, or null if Phenomena are not supported.
        
        
        """
        ...
    def positiveSignMeansActive(self) -> bool:
        """
            Get the sign of the g method that means "the phenomenon associated to the event is active".
        
        
            This method has been implemented because of the inconsistency of the sign of the g functions in the
            :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector` classes in Patrius: for some events, g is positive when its
            associated phenomenon is active, and for others, g is positive when its phenomenon is not active.
        
        
            WARNING : If Phenomena are not supported, the behavior of this method is undefined.
        
            Returns:
                true for positive, false for negative.
        
        
        """
        ...

class MultiEventsLogger:
    """
    public class MultiEventsLogger extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
    
        This class is copied from :class:`~fr.cnes.sirius.patrius.events.postprocessing.EventsLogger` and adapted to multi
        propagation.
        This class logs multi events detectors events.
    
        As :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector` are triggered during orbit propagation, an event specific
        :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.eventOccurred` method is called. This class can be used to add
        a global logging feature registering all events with their corresponding states in a chronological sequence (or
        reverse-chronological if propagation occurs backward).
    
        This class works by wrapping user-provided :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector` before they are
        registered to the propagator. The wrapper monitor the calls to
        :meth:`~fr.cnes.sirius.patrius.events.MultiEventDetector.eventOccurred` and store the corresponding events as
        :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiEventsLogger.MultiLoggedEvent` instances. After propagation
        is complete, the user can retrieve all the events that have occurred at once by calling method
        :meth:`~fr.cnes.sirius.patrius.events.postprocessing.MultiEventsLogger.getLoggedEvents`.
    
        Since:
            3.0
    """
    def __init__(self): ...
    def clearLoggedEvents(self) -> None:
        """
            Clear the logged events.
        
        """
        ...
    def getLoggedEvents(self) -> java.util.List['MultiEventsLogger.MultiLoggedEvent']: ...
    def monitorDetector(self, multiEventDetector: fr.cnes.sirius.patrius.events.MultiEventDetector) -> fr.cnes.sirius.patrius.events.MultiEventDetector:
        """
            Monitor a multi event detector.
        
            In order to monitor a multi event detector, it must be wrapped thanks to this method as follows:
        
            .. code-block: java
            
            
             MultiPropagator propagator = new XyzPropagator(...);
             MultiEventsLogger logger = new MultiEventsLogger();
             MultiEventDetector detector = new UvwDetector(...);
             propagator.addEventDetector(logger.monitorDetector(detector));
             
        
            Note that the event detector returned by the
            :meth:`~fr.cnes.sirius.patrius.events.postprocessing.MultiEventsLogger.MultiLoggedEvent.getEventDetector` method in
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiEventsLogger.MultiLoggedEvent` instances returned by
            :meth:`~fr.cnes.sirius.patrius.events.postprocessing.MultiEventsLogger.getLoggedEvents` are the
            :code:`monitoredDetector` instances themselves, not the wrapping detector returned by this method.
        
            Parameters:
                monitoredDetector (:class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`): multi event detector to monitor
        
            Returns:
                the wrapping detector to add to the propagator
        
        
        """
        ...
    class MultiLoggedEvent:
        def getEventDetector(self) -> fr.cnes.sirius.patrius.events.MultiEventDetector: ...
        def getStates(self) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
        def isIncreasing(self) -> bool: ...

class PhenomenaList(java.io.Serializable):
    """
    public final class PhenomenaList extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        This class represents a list of objects :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`.
    
    
        One or more lists of phenomena are created during propagation when
        :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector` is used, via the
        :meth:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEventsLogger.monitorDetector` method.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`, :meth:`~serialized`
    """
    def __init__(self): ...
    def add(self, phenomenon: 'Phenomenon') -> None:
        """
            Add a :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon` to the list.
        
            Parameters:
                phenomenon (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`): the :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon` to add.
        
        
        """
        ...
    def getList(self) -> java.util.List['Phenomenon']: ...
    def getPhenomena(self, string: str, string2: str, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> java.util.Set['Phenomenon']: ...
    def remove(self, phenomenon: 'Phenomenon') -> bool:
        """
            Remove a :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon` to the list.
        
            Parameters:
                phenomenon (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`): the :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon` to add.
        
            Returns:
                true if the set contains the phenomenon that has to be removed
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class Phenomenon(java.lang.Comparable['Phenomenon'], java.io.Serializable):
    """
    public final class Phenomenon extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        This class represents an observable phenomenon.
    
        A phenomenon is represented by a time interval and two boundaries; the boundaries can coincide with two
        :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`, or just be computational boundaries.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, codedEvent: CodedEvent, boolean: bool, codedEvent2: CodedEvent, boolean2: bool, string: str, string2: str): ...
    def compareTo(self, phenomenon: 'Phenomenon') -> int:
        """
            Compares the Phenomenon instances.
        
        
            If the beginning events differ, their comparison is the result. If not, if the ending events differ, they are compared.
            If not, the status of the boundaries is used to order
        
        
            Please note that the CodedEvent comparison uses more than the dates to order the CodedEvents.
        
            Specified by:
                 in interface 
        
            Parameters:
                o (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`): the :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon` to compare to
        
            Returns:
                a negative integer, zero, or a positive integer as the :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`
                is before, simultaneous, or after the specified one.
        
            Also see:
                `null <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true#compareTo-T->`
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
            Checks if the instance represents the same :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon` as another
            instance.
        
            Overrides:
                 in class 
        
            Parameters:
                phenomenon (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): other phenomenon
        
            Returns:
                true if the instance and the other are equals
        
        
        """
        ...
    def getCode(self) -> str:
        """
        
            Returns:
                the phenomenon code
        
        
        """
        ...
    def getComment(self) -> str:
        """
        
            Returns:
                the phenomenon comment
        
        
        """
        ...
    def getEndingEvent(self) -> CodedEvent:
        """
            Get the ending event.
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` instance.
        
        
        """
        ...
    def getEndingIsDefined(self) -> bool:
        """
            True if the second boundary value is defined.
        
            Returns:
                true or false
        
        
        """
        ...
    def getStartingEvent(self) -> CodedEvent:
        """
            Get the starting event.
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` instance.
        
        
        """
        ...
    def getStartingIsDefined(self) -> bool:
        """
            True if the first boundary value is defined.
        
            Returns:
                true or false
        
        
        """
        ...
    def getTimespan(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Get the timespan as an AbsoluteDateInterval.
        
            Returns:
                the AbsoluteDateInterval instance.
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class PostProcessing:
    """
    public interface PostProcessing
    
    
        Since:
            1.1
    """
    def applyTo(self, timeline: 'Timeline') -> None:
        """
        
            Parameters:
                list (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Timeline`): : the timeline that has to be processed
        
        
        """
        ...

class Timeline:
    """
    public class Timeline extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
    
        Since:
            1.1
    """
    @typing.overload
    def __init__(self, codedEventsLogger: CodedEventsLogger, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState): ...
    @typing.overload
    def __init__(self, timeline: 'Timeline'): ...
    @typing.overload
    def __init__(self, timeline: 'Timeline', absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval): ...
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval): ...
    def addCodedEvent(self, codedEvent: CodedEvent) -> None:
        """
        
            Parameters:
                event (:class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`): : event that has to be added to the list
        
        
        """
        ...
    def addPhenomenon(self, phenomenon: Phenomenon) -> None:
        """
        
            Parameters:
                phenomenon (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`): : phenomenon that has to be added to the list
        
        
        """
        ...
    def getCodedEventsList(self) -> java.util.List[CodedEvent]: ...
    def getIntervalOfValidity(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
        
            Returns:
                the interval of validity
        
        
        """
        ...
    def getPhenomenaCodesList(self) -> java.util.List[str]: ...
    def getPhenomenaList(self) -> java.util.List[Phenomenon]: ...
    def join(self, timeline: 'Timeline') -> 'Timeline': ...
    def merge(self, timeline: 'Timeline') -> None: ...
    def removeCodedEvent(self, codedEvent: CodedEvent) -> None:
        """
        
            Parameters:
                event (:class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`): : coded event that has to be removed from the list
        
        
        """
        ...
    def removeOnlyCodedEvent(self, codedEvent: CodedEvent) -> None:
        """
        
            Parameters:
                event (:class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`): : coded event that has to be removed from the list
        
        
        """
        ...
    def removePhenomenon(self, phenomenon: Phenomenon) -> None:
        """
        
            Parameters:
                phenomenon (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`): : phenomenon that has to be removed from the list
        
        
        """
        ...

class AndCriterion(PostProcessing):
    def __init__(self, string: str, string2: str, string3: str, string4: str): ...
    def applyTo(self, timeline: Timeline) -> None: ...

class DelayCriterion(PostProcessing):
    """
    public final class DelayCriterion extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
    
    
        Since:
            1.1
    """
    @typing.overload
    def __init__(self, string: str, double: float): ...
    @typing.overload
    def __init__(self, string: str, double: float, string2: str, string3: str): ...
    def applyTo(self, timeline: Timeline) -> None:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing.applyTo` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
        
            Parameters:
                list (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Timeline`): : the timeline that has to be processed
        
        
        """
        ...

class ElementTypeFilter(PostProcessing):
    """
    public final class ElementTypeFilter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
    
    
        Since:
            1.1
    """
    @typing.overload
    def __init__(self, string: str, boolean: bool): ...
    @typing.overload
    def __init__(self, list: java.util.List[str], boolean: bool): ...
    def applyTo(self, timeline: Timeline) -> None:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing.applyTo` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
        
            Parameters:
                list (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Timeline`): : the timeline that has to be processed
        
        
        """
        ...

class EventsDuringPhenomenaFilter(PostProcessing):
    """
    public final class EventsDuringPhenomenaFilter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
    
    
        Since:
            1.1
    """
    @typing.overload
    def __init__(self, string: str, string2: str, boolean: bool): ...
    @typing.overload
    def __init__(self, list: java.util.List[str], string: str, boolean: bool): ...
    def applyTo(self, timeline: Timeline) -> None:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing.applyTo` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
        
            Parameters:
                list (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Timeline`): : the timeline that has to be processed
        
        
        """
        ...

class GenericCodingEventDetector(CodingEventDetector):
    """
    public class GenericCodingEventDetector extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector`
    
    
        This class represents an all-purpose implementation of the
        :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector` interface.
    
    
        It works using the :class:`~fr.cnes.sirius.patrius.events.EventDetector` provided in the constructor.
        This detector is able to build a :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` for a given date
        using the method :meth:`~fr.cnes.sirius.patrius.events.postprocessing.GenericCodingEventDetector.buildCodedEvent`.
    
    
        You cannot set the CodedEvent comment through this implementation. Subclassing is permitted for the purpose of adding
        functionality.
    
        It supports phenomena or not, depending on which constructor was used. When it does support phenomena, the user can know
        for a given input if the state is active using the method
        :meth:`~fr.cnes.sirius.patrius.events.postprocessing.GenericCodingEventDetector.isStateActive`.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, string: str, string2: str): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, string: str, string2: str, boolean: bool, string3: str): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, string: str, string2: str, boolean: bool, string3: str, double: float, int: int): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, string: str, string2: str, double: float, int: int): ...
    def buildCodedEvent(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool) -> CodedEvent:
        """
            Build a :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` instance appropriate for the provided
            :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector.buildCodedEvent` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector`
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the current state information : date, kinematics, attitude
                increasing (boolean): if true, g function increases around event date.
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`
        
        
        """
        ...
    def buildDelayedCodedEvent(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool) -> CodedEvent:
        """
            Build a delayed :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` instance appropriate for the provided
            :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`. This instance will have a delay with respect to the
            associated detected event.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector.buildDelayedCodedEvent` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector`
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the current state information : date, kinematics, attitude
                increasing (boolean): if true, g function increases around event date.
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`
        
        
        """
        ...
    def buildOccurrenceCodedEvent(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool) -> CodedEvent:
        """
            Build a :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` instance appropriate for the provided
            :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`. This method will return an instance only if it is be the
            nth occurrence of the corresponding event, otherwise it will return null. A delay can be applied to the event.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector.buildOccurrenceCodedEvent` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector`
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the current state information : date, kinematics, attitude
                increasing (boolean): if true, g function increases around event date.
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent`
        
        
        """
        ...
    def copy(self) -> fr.cnes.sirius.patrius.events.EventDetector:
        """
            A copy of the detector. By default copy is deep. If not, detector javadoc will specify which attribute is not fully
            copied. In that case, the attribute reference is passed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.copy` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Returns:
                a copy of the detector.
        
        
        """
        ...
    def eventOccurred(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool, boolean2: bool) -> fr.cnes.sirius.patrius.events.EventDetector.Action: ...
    def filterEvent(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool, boolean2: bool) -> bool: ...
    def g(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    def getEventType(self) -> str:
        """
            Gets a code indicating the type of event we want to log: DELAY when a delay is associated to the logged events with
            respect to the detected events, N_OCCURRENCE when we want to log the nth occurrence of the detected events, STANDARD
            when no delays and no occurrence numbers are taken into consideration.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector.getEventType` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector`
        
            Returns:
                the type of event to log
        
        
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
    def getPhenomenonCode(self) -> str:
        """
            If the implementation supports a :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`, provides a code for
            the phenomenon associated to the event. If not, returns null.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector.getPhenomenonCode` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector`
        
            Returns:
                either a code, or null if Phenomena are not supported.
        
        
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
    def isStateActive(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> bool: ...
    @staticmethod
    def logEventsOverTimeInterval(codedEventsLogger: CodedEventsLogger, propagator: fr.cnes.sirius.patrius.propagation.Propagator, codingEventDetector: CodingEventDetector, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def positiveSignMeansActive(self) -> bool:
        """
            Get the sign of the g method that means "the phenomenon associated to the event is active".
        
        
            This method has been implemented because of the inconsistency of the sign of the g functions in the
            :class:`~fr.cnes.sirius.patrius.events.EventDetector` classes in Orekit: for some events, g is positive when its
            associated phenomenon is active, and for others, g is positive when its phenomenon is not active.
        
        
            WARNING : If Phenomena are not supported, the behavior of this method is undefined.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector.positiveSignMeansActive` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodingEventDetector`
        
            Returns:
                true for positive, false for negative.
        
        
        """
        ...
    def resetState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
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

class MergePhenomenaCriterion(PostProcessing):
    """
    public final class MergePhenomenaCriterion extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
    
    
        Since:
            1.1
    """
    @typing.overload
    def __init__(self, string: str, double: float): ...
    @typing.overload
    def __init__(self, string: str, double: float, string2: str): ...
    @typing.overload
    def __init__(self, list: java.util.List[str], double: float): ...
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]], double: float): ...
    def applyTo(self, timeline: Timeline) -> None:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing.applyTo` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
        
            Parameters:
                list (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Timeline`): : the timeline that has to be processed
        
        
        """
        ...

class MergeTimelines(PostProcessing):
    """
    public class MergeTimelines extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
    
    
        Since:
            1.1
    """
    def __init__(self, timeline: Timeline): ...
    def applyTo(self, timeline: Timeline) -> None:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing.applyTo` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
        
            Parameters:
                list (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Timeline`): : the timeline that has to be processed
        
        
        """
        ...

class MultiGenericCodingEventDetector(MultiCodingEventDetector):
    """
    public class MultiGenericCodingEventDetector extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector`
    
    
        This class is copied from :class:`~fr.cnes.sirius.patrius.events.postprocessing.GenericCodingEventDetector` and adapted
        to multi propagation.
    
        This class represents an all-purpose implementation of the
        :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector` interface.
    
    
        It works using the :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector` provided in the constructor.
        This detector is able to build a :class:`~fr.cnes.sirius.patrius.events.postprocessing.CodedEvent` for a given date
        using the method :meth:`~fr.cnes.sirius.patrius.events.postprocessing.MultiGenericCodingEventDetector.buildCodedEvent`.
    
    
        You cannot set the CodedEvent comment through this implementation. Subclassing is permitted for the purpose of adding
        functionality.
    
        It supports phenomena or not, depending on which constructor was used. When it does support phenomena, the user can know
        for a given input if the state is active using the method
        :meth:`~fr.cnes.sirius.patrius.events.postprocessing.MultiGenericCodingEventDetector.isStateActive`.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector`
    """
    @typing.overload
    def __init__(self, multiEventDetector: fr.cnes.sirius.patrius.events.MultiEventDetector, string: str, string2: str): ...
    @typing.overload
    def __init__(self, multiEventDetector: fr.cnes.sirius.patrius.events.MultiEventDetector, string: str, string2: str, boolean: bool, string3: str): ...
    @typing.overload
    def __init__(self, multiEventDetector: fr.cnes.sirius.patrius.events.MultiEventDetector, string: str, string2: str, boolean: bool, string3: str, double: float, int: int): ...
    @typing.overload
    def __init__(self, multiEventDetector: fr.cnes.sirius.patrius.events.MultiEventDetector, string: str, string2: str, double: float, int: int): ...
    def buildCodedEvent(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool) -> CodedEvent: ...
    def buildDelayedCodedEvent(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool) -> CodedEvent: ...
    def buildOccurrenceCodedEvent(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool) -> CodedEvent: ...
    def eventOccurred(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool, boolean2: bool) -> fr.cnes.sirius.patrius.events.EventDetector.Action: ...
    def filterEvent(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool, boolean2: bool) -> bool: ...
    def g(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]]) -> float: ...
    def getEventType(self) -> str:
        """
            Gets a code indicating the type of event we want to log: DELAY when a delay is associated to the logged events with
            respect to the detected events, N_OCCURRENCE when we want to log the nth occurrence of the detected events, STANDARD
            when no delays and no occurrence numbers are taken into consideration.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector.getEventType` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector`
        
            Returns:
                the type of event to log
        
        
        """
        ...
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
    def getPhenomenonCode(self) -> str:
        """
            If the implementation supports a :class:`~fr.cnes.sirius.patrius.events.postprocessing.Phenomenon`, provides a code for
            the phenomenon associated to the event. If not, returns null.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector.getPhenomenonCode` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector`
        
            Returns:
                either a code, or null if Phenomena are not supported.
        
        
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
    def isStateActive(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]]) -> bool: ...
    def positiveSignMeansActive(self) -> bool:
        """
            Get the sign of the g method that means "the phenomenon associated to the event is active".
        
        
            This method has been implemented because of the inconsistency of the sign of the g functions in the
            :class:`~fr.cnes.sirius.patrius.events.MultiEventDetector` classes in Patrius: for some events, g is positive when its
            associated phenomenon is active, and for others, g is positive when its phenomenon is not active.
        
        
            WARNING : If Phenomena are not supported, the behavior of this method is undefined.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector.positiveSignMeansActive` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.MultiCodingEventDetector`
        
            Returns:
                true for positive, false for negative.
        
        
        """
        ...
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

class NotCriterion(PostProcessing):
    """
    public class NotCriterion extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
    
        This criterion adds to the phenomena list of a Timeline the complementary phenomena of a given phenomenon. The
        complementary phenomena are defined for every time interval for which the phenomenon of interest does not occur.
        Depending the replication of the original phenomenon over the timeline, the events defining the beginning and the end of
        those new phenomena can be :
    
    
        - the ones of the original phenomena
    
    
        - the (dummy) events corresponding to the beginning of the timeline validity interval
    
    
        - the (dummy) events corresponding to the end of the timeline validity interval
    """
    def __init__(self, string: str, string2: str, string3: str): ...
    def applyTo(self, timeline: Timeline) -> None:
        """
            Adds to the phenomena list of a TimeLine object the phenomena corresponding to each time intervals when a phenomenon
            does not occur. The events defining the beginning and the end of those new phenomena are directly the ones of the
            original phenomenon or dummy events corresponding to the bounds of the validity interval.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing.applyTo` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
        
            Parameters:
                list (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Timeline`): the list of events and phenomenon to be modified
        
        
        """
        ...

class OccurrenceFilter(PostProcessing):
    """
    public final class OccurrenceFilter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
    
    
        Since:
            1.1
    """
    def __init__(self, string: str, int: int, boolean: bool): ...
    def applyTo(self, timeline: Timeline) -> None:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing.applyTo` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
        
            Parameters:
                list (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Timeline`): : the timeline that has to be processed
        
        
        """
        ...

class OrCriterion(PostProcessing):
    def __init__(self, string: str, string2: str, string3: str, string4: str): ...
    def applyTo(self, timeline: Timeline) -> None: ...

class PhenomenonDurationFilter(PostProcessing):
    @typing.overload
    def __init__(self, string: str, double: float, boolean: bool): ...
    @typing.overload
    def __init__(self, list: java.util.List[str], double: float, boolean: bool): ...
    def applyTo(self, timeline: Timeline) -> None: ...

class PolarizationSingleSelection(PostProcessing):
    """
    public final class PolarizationSingleSelection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
    
        This class is a post processing creation that creates a new polarization single selection phenomenon from two sets of
        visibility phenomena. While no changes are made to the events list of the timeline, the phenomena list will contain a
        new element.
    
        Since:
            1.2
    """
    def __init__(self, string: str, string2: str, double: float, double2: float): ...
    def applyTo(self, timeline: Timeline) -> None:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing.applyTo` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
        
            Parameters:
                list (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Timeline`): : the timeline that has to be processed
        
        
        """
        ...

class PolarizationSwitch(PostProcessing):
    """
    public final class PolarizationSwitch extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
    
        This class is a post processing creation that creates new elements corresponding to polarization switch events. While no
        changes are made to the phenomena list of the timeline, the events list will contain new elements.
    
        Since:
            1.2
    """
    def __init__(self, string: str, string2: str, double: float, double2: float): ...
    def applyTo(self, timeline: Timeline) -> None:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing.applyTo` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
        
            Parameters:
                list (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Timeline`): : the timeline that has to be processed
        
        
        """
        ...

class TimeFilter(PostProcessing):
    """
    public final class TimeFilter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
    
    
        Since:
            1.1
    """
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool): ...
    @typing.overload
    def __init__(self, string: str, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool): ...
    @typing.overload
    def __init__(self, list: java.util.List[str], absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool): ...
    def applyTo(self, timeline: Timeline) -> None:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing.applyTo` in
                interface :class:`~fr.cnes.sirius.patrius.events.postprocessing.PostProcessing`
        
            Parameters:
                list (:class:`~fr.cnes.sirius.patrius.events.postprocessing.Timeline`): : the timeline that has to be processed
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.events.postprocessing")``.

    AndCriterion: typing.Type[AndCriterion]
    CodedEvent: typing.Type[CodedEvent]
    CodedEventsList: typing.Type[CodedEventsList]
    CodedEventsLogger: typing.Type[CodedEventsLogger]
    CodingEventDetector: typing.Type[CodingEventDetector]
    DelayCriterion: typing.Type[DelayCriterion]
    ElementTypeFilter: typing.Type[ElementTypeFilter]
    EventsDuringPhenomenaFilter: typing.Type[EventsDuringPhenomenaFilter]
    EventsLogger: typing.Type[EventsLogger]
    GenericCodingEventDetector: typing.Type[GenericCodingEventDetector]
    MergePhenomenaCriterion: typing.Type[MergePhenomenaCriterion]
    MergeTimelines: typing.Type[MergeTimelines]
    MultiCodedEventsLogger: typing.Type[MultiCodedEventsLogger]
    MultiCodingEventDetector: typing.Type[MultiCodingEventDetector]
    MultiEventsLogger: typing.Type[MultiEventsLogger]
    MultiGenericCodingEventDetector: typing.Type[MultiGenericCodingEventDetector]
    NotCriterion: typing.Type[NotCriterion]
    OccurrenceFilter: typing.Type[OccurrenceFilter]
    OrCriterion: typing.Type[OrCriterion]
    PhenomenaList: typing.Type[PhenomenaList]
    Phenomenon: typing.Type[Phenomenon]
    PhenomenonDurationFilter: typing.Type[PhenomenonDurationFilter]
    PolarizationSingleSelection: typing.Type[PolarizationSingleSelection]
    PolarizationSwitch: typing.Type[PolarizationSwitch]
    PostProcessing: typing.Type[PostProcessing]
    TimeFilter: typing.Type[TimeFilter]
    Timeline: typing.Type[Timeline]
