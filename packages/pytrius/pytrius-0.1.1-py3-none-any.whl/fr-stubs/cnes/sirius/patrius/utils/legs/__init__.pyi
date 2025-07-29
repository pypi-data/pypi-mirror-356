
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.time
import java.util
import java.util.function
import jpype
import typing



class Leg(fr.cnes.sirius.patrius.time.TimeStamped):
    """
    public interface Leg extends :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
    
        A *leg* is an object which is valid between two dates.
    
        It’s also :class:`~fr.cnes.sirius.patrius.time.TimeStamped` by the beginning date.
    
        Please note a :code:`Leg` **should be immutable**, and please see :code:`Leg#copy(AbsoluteDateInterval)` method.
    
        Since:
            4.7
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
    """
    LEG_NATURE: typing.ClassVar[str] = ...
    """
    static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` LEG_NATURE
    
        Default nature.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def contains(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> bool:
        """
            Check whether the given date is contained in the interval of the current leg.
        
            Parameters:
                dateIn (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date to check
        
            Returns:
                boolean: if true, the given date is contained in the interval; if false, it is not
        
        
        """
        ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'Leg':
        """
            Creates a new leg from this one.
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
            Raises:
                : If the given :code:`newInterval` is problematic (too long, too short, whatever)
        
        
        """
        ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Returns the leg start date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                the leg start date
        
        
        """
        ...
    def getEnd(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Returns the leg end date.
        
            Returns:
                the leg end date
        
        
        """
        ...
    def getNature(self) -> str:
        """
            Returns the nature of the leg.
        
            Returns:
                The “nature” of the leg.
        
        
        """
        ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Returns the time interval of the leg.
        
            Returns:
                the time interval of the leg.
        
        
        """
        ...
    def toPrettyString(self) -> str:
        """
            Returns a nice `null <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` representation.
        
            Returns:
                A nice `null <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` representation.
        
        
        """
        ...

class Sequences:
    """
    public final class Sequences extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Collection of static method for handling sequences of legs :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence` ands
        time sequences :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`.
    
        Since:
            4.8
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`, :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
    """
    _emptyLegsSequence__L = typing.TypeVar('_emptyLegsSequence__L', bound=Leg)  # <L>
    @staticmethod
    def emptyLegsSequence() -> 'LegsSequence'[_emptyLegsSequence__L]:
        """
            Build an empty legs sequence.
        
            Returns:
                an empty legs sequence
        
        
        """
        ...
    _emptyTimeSequence__T = typing.TypeVar('_emptyTimeSequence__T', bound=fr.cnes.sirius.patrius.time.TimeStamped)  # <T>
    @staticmethod
    def emptyTimeSequence() -> 'TimeSequence'[_emptyTimeSequence__T]:
        """
            Build an empty time sequence.
        
            Returns:
                an empty time sequence
        
        
        """
        ...
    _unmodifiableLegsSequence__L = typing.TypeVar('_unmodifiableLegsSequence__L', bound=Leg)  # <L>
    @staticmethod
    def unmodifiableLegsSequence(legsSequence: 'LegsSequence'[_unmodifiableLegsSequence__L]) -> 'LegsSequence'[_unmodifiableLegsSequence__L]:
        """
            Build an unmodifiable legs sequence. This sequence can be manipulated like any sequence but no element can be added or
            removed.
        
            Parameters:
                sequence (:class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`<L> sequence): a legs sequence
        
            Returns:
                an unmodifiable legs sequence
        
        
        """
        ...
    _unmodifiableTimeSequence__T = typing.TypeVar('_unmodifiableTimeSequence__T', bound=fr.cnes.sirius.patrius.time.TimeStamped)  # <T>
    @staticmethod
    def unmodifiableTimeSequence(timeSequence: 'TimeSequence'[_unmodifiableTimeSequence__T]) -> 'TimeSequence'[_unmodifiableTimeSequence__T]:
        """
            Build an unmodifiable time sequence. This sequence can be manipulated like any sequence but no element can be added or
            removed.
        
            Parameters:
                sequence (:class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`<T> sequence): a time sequence
        
            Returns:
                an unmodifiable time sequence
        
        
        """
        ...

_TimeSequence__T = typing.TypeVar('_TimeSequence__T', bound=fr.cnes.sirius.patrius.time.TimeStamped)  # <T>
class TimeSequence(java.util.Collection[_TimeSequence__T], typing.Generic[_TimeSequence__T]):
    """
    public interface TimeSequence<T extends :class:`~fr.cnes.sirius.patrius.time.TimeStamped`> extends `Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<T>
    
        A `null <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>` of
        :class:`~fr.cnes.sirius.patrius.time.TimeStamped` objects.
    
        This sequence is designed to sort objects by their date (:meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate`). Some
        might suggest that a `null <http://docs.oracle.com/javase/8/docs/api/java/util/NavigableSet.html?is-external=true>`
        would have done the job, but a :code:`NavigableSet` has some methods too complicated and too ambiguous to implement (as
        :code:`lower()`, :code:`floor()`, …) with “time-sorted” objects.
    
        Besides, as stated in the :code:`SortedSet` interface documentation, the used :code:`Comparator` must be *“consistent
        with equals”*, and it cannot be achieved with such :code:`TimeStamped` objects.
    
        Since:
            4.7
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
    """
    def contains(self, object: typing.Any) -> bool:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    def containsAll(self, collection: typing.Union[java.util.Collection[typing.Any], typing.Sequence[typing.Any], typing.Set[typing.Any]]) -> bool: ...
    def copy(self) -> 'TimeSequence'[_TimeSequence__T]: ...
    def equals(self, object: typing.Any) -> bool: ...
    @typing.overload
    def first(self) -> _TimeSequence__T:
        """
            Returns the first element currently in this sequence.
        
            Returns:
                The first element currently in this sequence.
        
        """
        ...
    @typing.overload
    def first(self, timeStamped: typing.Union[fr.cnes.sirius.patrius.time.TimeStamped, typing.Callable]) -> _TimeSequence__T:
        """
            Returns the first element after the given date.
        
            See :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.next` for “strict” comparison.
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.TimeStamped`): A date from any :class:`~fr.cnes.sirius.patrius.time.TimeStamped` object.
        
            Returns:
                The first element *starting after (or at)* the given date :code:`t`.
        
        
        """
        ...
    def hashCode(self) -> int: ...
    def head(self, t: _TimeSequence__T) -> 'TimeSequence'[_TimeSequence__T]: ...
    @typing.overload
    def last(self) -> _TimeSequence__T:
        """
            Returns the last element currently in this sequence.
        
            Returns:
                The last element currently in this sequence.
        
        """
        ...
    @typing.overload
    def last(self, timeStamped: typing.Union[fr.cnes.sirius.patrius.time.TimeStamped, typing.Callable]) -> _TimeSequence__T:
        """
            Returns the last element before the given date.
        
            See :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.previous` for “strict” comparison.
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.TimeStamped`): A date from any :class:`~fr.cnes.sirius.patrius.time.TimeStamped` object.
        
            Returns:
                The last element *starting after (or at)* the given date :code:`t`.
        
        
        """
        ...
    def next(self, t: _TimeSequence__T) -> _TimeSequence__T:
        """
            Returns the *strictly* next element.
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`): Any element of this sequence.
        
            Returns:
                The previous element of the given one, :code:`null` if none. It’s a *strictly* next: its date is strictly upper. Note
                also there may be simultaneous elements…
        
        
        """
        ...
    def previous(self, t: _TimeSequence__T) -> _TimeSequence__T:
        """
            Returns the *strictly* previous element.
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`): Any element of this sequence.
        
            Returns:
                The previous element of the given one, :code:`null` if none. It’s a *strictly* previous: its date is strictly lower.
                Note also there may be simultaneous elements…
        
        
        """
        ...
    def simultaneous(self, timeStamped: typing.Union[fr.cnes.sirius.patrius.time.TimeStamped, typing.Callable]) -> java.util.Set[_TimeSequence__T]: ...
    def sub(self, t: _TimeSequence__T, t2: _TimeSequence__T) -> 'TimeSequence'[_TimeSequence__T]: ...
    def tail(self, t: _TimeSequence__T) -> 'TimeSequence'[_TimeSequence__T]: ...
    def toPrettyString(self) -> str:
        """
        
            Returns:
                A nice :code:`String` representation.
        
        
        """
        ...

_LegsSequence__L = typing.TypeVar('_LegsSequence__L', bound=Leg)  # <L>
class LegsSequence(TimeSequence[_LegsSequence__L], typing.Generic[_LegsSequence__L]):
    """
    public interface LegsSequence<L extends :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`> extends :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`<L>
    
        A `null <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>` of
        :class:`~fr.cnes.sirius.patrius.utils.legs.Leg` objects.
    
        Previously, this :code:`LegsSequence` has been a :code:`NavigableSet`, but too much methods were unsuitable for
        :code:`Leg`s objects.
    
        Since:
            4.7
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`, :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`,
            :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
    """
    @typing.overload
    def copy(self) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'LegsSequence'[_LegsSequence__L]: ...
    def current(self, timeStamped: typing.Union[fr.cnes.sirius.patrius.time.TimeStamped, typing.Callable]) -> _LegsSequence__L:
        """
            Returns the current leg at the given date.
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.TimeStamped`): A date from any :class:`~fr.cnes.sirius.patrius.time.TimeStamped` object.
        
            Returns:
                The current :code:`Leg` at the :code:`t` date, or :code:`null` if none.
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool: ...
    @typing.overload
    def first(self) -> _LegsSequence__L:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.first`
            Returns the first element currently in this sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.first` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Returns:
                The first :code:`Leg`, :code:`null` if none.
        
        """
        ...
    @typing.overload
    def first(self, timeStamped: typing.Union[fr.cnes.sirius.patrius.time.TimeStamped, typing.Callable]) -> _LegsSequence__L:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.first`
            Returns the first element after the given date.
        
            See :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.next` for “strict” comparison.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.first` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.TimeStamped`): A date from any :class:`~fr.cnes.sirius.patrius.time.TimeStamped` object.
        
            Returns:
                The first :code:`Leg` *starting after (or at)* the given date :code:`t`.
        
        
        """
        ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Returns the time interval of the legs sequence.
        
            Returns:
                the time interval of the legs sequence.
        
        
        """
        ...
    def hashCode(self) -> int: ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def head(self, l: _LegsSequence__L) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def isEmpty(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> bool:
        """
            Checks whether the sequence is free on the given interval or not.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The “beginning” date.
                end (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The “end” date.
        
            Returns:
                :code:`true` if this sequence is completely free during the given time interval.
        
        
        """
        ...
    @typing.overload
    def isEmpty(self) -> bool: ...
    @typing.overload
    def last(self) -> _LegsSequence__L:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.last`
            Returns the last element currently in this sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.last` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Returns:
                The last :code:`Leg`, :code:`null` if none.
        
        """
        ...
    @typing.overload
    def last(self, timeStamped: typing.Union[fr.cnes.sirius.patrius.time.TimeStamped, typing.Callable]) -> _LegsSequence__L:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.last`
            Returns the last element before the given date.
        
            See :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.previous` for “strict” comparison.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.last` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.TimeStamped`): A date from any :class:`~fr.cnes.sirius.patrius.time.TimeStamped` object.
        
            Returns:
                The last :code:`Leg` *finishing before (or at)* the given date :code:`t`.
        
        
        """
        ...
    def next(self, l: _LegsSequence__L) -> _LegsSequence__L:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.next`
            Returns the *strictly* next element.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.next` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Parameters:
                leg (:class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`): Any element of this sequence.
        
            Returns:
                The next :code:`Leg` of the given :code:`leg`, :code:`null` if none.
        
        
        """
        ...
    def previous(self, l: _LegsSequence__L) -> _LegsSequence__L:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.previous`
            Returns the *strictly* previous element.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.previous` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Parameters:
                leg (:class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`): Any element of this sequence.
        
            Returns:
                The previous :code:`Leg` of the given :code:`leg`, :code:`null` if none.
        
        
        """
        ...
    @typing.overload
    def simultaneous(self, l: _LegsSequence__L) -> java.util.Set[_LegsSequence__L]: ...
    @typing.overload
    def simultaneous(self, timeStamped: typing.Union[fr.cnes.sirius.patrius.time.TimeStamped, typing.Callable]) -> java.util.Set[fr.cnes.sirius.patrius.time.TimeStamped]: ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def sub(self, l: _LegsSequence__L, l2: _LegsSequence__L) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def tail(self, l: _LegsSequence__L) -> 'LegsSequence'[_LegsSequence__L]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'LegsSequence'[_LegsSequence__L]: ...
    def toPrettyString(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.toPrettyString` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Returns:
                A nice :code:`String` representation.
        
        
        """
        ...

_StrictLegsSequence__L = typing.TypeVar('_StrictLegsSequence__L', bound=Leg)  # <L>
class StrictLegsSequence(LegsSequence[_StrictLegsSequence__L], typing.Generic[_StrictLegsSequence__L]):
    """
    public class StrictLegsSequence<L extends :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`<L>
    
        A :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence` which does not accept simultaneous or overlapping legs. Legs
        are considered to have closed boundaries.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`, :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
    """
    def __init__(self): ...
    def add(self, l: _StrictLegsSequence__L) -> bool:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    def addAll(self, collection: typing.Union[java.util.Collection[_StrictLegsSequence__L], typing.Sequence[_StrictLegsSequence__L], typing.Set[_StrictLegsSequence__L]]) -> bool: ...
    def clear(self) -> None:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    @typing.overload
    def copy(self) -> 'StrictLegsSequence'[_StrictLegsSequence__L]: ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'StrictLegsSequence'[_StrictLegsSequence__L]: ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'StrictLegsSequence'[_StrictLegsSequence__L]: ...
    def current(self, timeStamped: typing.Union[fr.cnes.sirius.patrius.time.TimeStamped, typing.Callable]) -> _StrictLegsSequence__L:
        """
            Returns the current leg at the given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.current` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.TimeStamped`): A date from any :class:`~fr.cnes.sirius.patrius.time.TimeStamped` object.
        
            Returns:
                The current :code:`Leg` at the :code:`t` date, or :code:`null` if none.
        
        
        """
        ...
    @typing.overload
    def first(self) -> _StrictLegsSequence__L:
        """
            Returns the first element currently in this sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.first` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.first` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Returns:
                The first :code:`Leg`, :code:`null` if none.
        
        """
        ...
    @typing.overload
    def first(self, timeStamped: typing.Union[fr.cnes.sirius.patrius.time.TimeStamped, typing.Callable]) -> _StrictLegsSequence__L:
        """
            Returns the first element after the given date.
        
            See :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.next` for “strict” comparison.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.first` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.first` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.TimeStamped`): A date from any :class:`~fr.cnes.sirius.patrius.time.TimeStamped` object.
        
            Returns:
                The first :code:`Leg` *starting after (or at)* the given date :code:`t`.
        
        
        """
        ...
    def getSet(self) -> java.util.NavigableSet[fr.cnes.sirius.patrius.time.TimeStamped]: ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Returns the time interval of the legs sequence.
        
            Null is returned if the sequence is empty.
        
            Warning: in case of sequences with holes, the sequence in the returned interval will not contain continuous data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.getTimeInterval` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Returns:
                the time interval of the legs sequence.
        
        
        """
        ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> LegsSequence[_StrictLegsSequence__L]: ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> LegsSequence[_StrictLegsSequence__L]: ...
    @typing.overload
    def head(self, l: _StrictLegsSequence__L) -> LegsSequence[_StrictLegsSequence__L]: ...
    @typing.overload
    def isEmpty(self) -> bool:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    @typing.overload
    def isEmpty(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> bool:
        """
            Checks whether the sequence is free on the given interval or not.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.isEmpty` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The “beginning” date.
                end (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The “end” date.
        
            Returns:
                :code:`true` if this sequence is completely free during the given time interval.
        
        """
        ...
    def iterator(self) -> java.util.Iterator[_StrictLegsSequence__L]: ...
    @typing.overload
    def last(self) -> _StrictLegsSequence__L:
        """
            Returns the last element currently in this sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.last` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.last` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Returns:
                The last :code:`Leg`, :code:`null` if none.
        
        """
        ...
    @typing.overload
    def last(self, timeStamped: typing.Union[fr.cnes.sirius.patrius.time.TimeStamped, typing.Callable]) -> _StrictLegsSequence__L:
        """
            Returns the last element before the given date.
        
            See :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.previous` for “strict” comparison.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.last` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.last` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.TimeStamped`): A date from any :class:`~fr.cnes.sirius.patrius.time.TimeStamped` object.
        
            Returns:
                The last :code:`Leg` *finishing before (or at)* the given date :code:`t`.
        
        
        """
        ...
    def next(self, l: _StrictLegsSequence__L) -> _StrictLegsSequence__L:
        """
            Returns the *strictly* next element.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.next` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.next` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Parameters:
                leg (:class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`): Any element of this sequence.
        
            Returns:
                The next :code:`Leg` of the given :code:`leg`, :code:`null` if none.
        
        
        """
        ...
    def previous(self, l: _StrictLegsSequence__L) -> _StrictLegsSequence__L:
        """
            Returns the *strictly* previous element.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.previous` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.previous` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Parameters:
                leg (:class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`): Any element of this sequence.
        
            Returns:
                The previous :code:`Leg` of the given :code:`leg`, :code:`null` if none.
        
        
        """
        ...
    def remove(self, object: typing.Any) -> bool:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    def removeAll(self, collection: typing.Union[java.util.Collection[typing.Any], typing.Sequence[typing.Any], typing.Set[typing.Any]]) -> bool: ...
    def retainAll(self, collection: typing.Union[java.util.Collection[typing.Any], typing.Sequence[typing.Any], typing.Set[typing.Any]]) -> bool: ...
    @typing.overload
    def simultaneous(self, timeStamped: typing.Union[fr.cnes.sirius.patrius.time.TimeStamped, typing.Callable]) -> java.util.Set[_StrictLegsSequence__L]: ...
    @typing.overload
    def simultaneous(self, l: _StrictLegsSequence__L) -> java.util.Set[_StrictLegsSequence__L]: ...
    def size(self) -> int:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> LegsSequence[_StrictLegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> LegsSequence[_StrictLegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> LegsSequence[_StrictLegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> LegsSequence[_StrictLegsSequence__L]: ...
    @typing.overload
    def sub(self, l: _StrictLegsSequence__L, l2: _StrictLegsSequence__L) -> LegsSequence[_StrictLegsSequence__L]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> LegsSequence[_StrictLegsSequence__L]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> LegsSequence[_StrictLegsSequence__L]: ...
    @typing.overload
    def tail(self, l: _StrictLegsSequence__L) -> LegsSequence[_StrictLegsSequence__L]: ...
    _toArray_0__T = typing.TypeVar('_toArray_0__T')  # <T>
    _toArray_2__T = typing.TypeVar('_toArray_2__T')  # <T>
    @typing.overload
    def toArray(self, intFunction: typing.Union[java.util.function.IntFunction[typing.Union[typing.List[_toArray_0__T], jpype.JArray]], typing.Callable[[int], typing.Union[typing.List[_toArray_0__T], jpype.JArray]]]) -> typing.MutableSequence[_toArray_0__T]:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    @typing.overload
    def toArray(self) -> typing.MutableSequence[typing.Any]:
        """
        
            Specified by:
                 in interface 
        
        """
        ...
    @typing.overload
    def toArray(self, tArray: typing.Union[typing.List[_toArray_2__T], jpype.JArray]) -> typing.MutableSequence[_toArray_2__T]: ...
    def toPrettyString(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.toPrettyString` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.toPrettyString` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Returns:
                A nice :code:`String` representation.
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
            Returns:
                A :code:`String` representation.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.utils.legs")``.

    Leg: typing.Type[Leg]
    LegsSequence: typing.Type[LegsSequence]
    Sequences: typing.Type[Sequences]
    StrictLegsSequence: typing.Type[StrictLegsSequence]
    TimeSequence: typing.Type[TimeSequence]
