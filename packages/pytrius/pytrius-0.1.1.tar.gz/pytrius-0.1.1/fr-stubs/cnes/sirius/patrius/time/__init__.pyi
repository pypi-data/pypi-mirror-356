
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.frames.configuration.eop
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.interval
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.time.interpolation
import fr.cnes.sirius.patrius.tools.cache
import java.io
import java.lang
import java.math
import java.time
import java.util
import jpype
import typing



class AbsoluteDateInterval(fr.cnes.sirius.patrius.math.interval.ComparableInterval['AbsoluteDate']):
    INFINITY: typing.ClassVar['AbsoluteDateInterval'] = ...
    @typing.overload
    def __init__(self, comparableInterval: fr.cnes.sirius.patrius.math.interval.ComparableInterval['AbsoluteDate']): ...
    @typing.overload
    def __init__(self, comparableInterval: fr.cnes.sirius.patrius.math.interval.ComparableInterval[float], absoluteDate: 'AbsoluteDate'): ...
    @typing.overload
    def __init__(self, intervalEndpointType: fr.cnes.sirius.patrius.math.interval.IntervalEndpointType, absoluteDate: 'AbsoluteDate', absoluteDate2: 'AbsoluteDate', intervalEndpointType2: fr.cnes.sirius.patrius.math.interval.IntervalEndpointType): ...
    @typing.overload
    def __init__(self, absoluteDate: 'AbsoluteDate', double: float): ...
    @typing.overload
    def __init__(self, absoluteDate: 'AbsoluteDate', absoluteDate2: 'AbsoluteDate'): ...
    def compareDurationTo(self, absoluteDateInterval: 'AbsoluteDateInterval') -> int: ...
    def durationFrom(self, absoluteDateInterval: 'AbsoluteDateInterval') -> float: ...
    def extendTo(self, absoluteDate: 'AbsoluteDate') -> 'AbsoluteDateInterval': ...
    def getDateListFromSize(self, int: int) -> java.util.List['AbsoluteDate']: ...
    def getDateListFromStep(self, double: float) -> java.util.List['AbsoluteDate']: ...
    def getDuration(self) -> float: ...
    @typing.overload
    def getIntersectionWith(self, comparableInterval: fr.cnes.sirius.patrius.math.interval.ComparableInterval[java.lang.Comparable]) -> fr.cnes.sirius.patrius.math.interval.ComparableInterval[java.lang.Comparable]: ...
    @typing.overload
    def getIntersectionWith(self, absoluteDateInterval: 'AbsoluteDateInterval') -> 'AbsoluteDateInterval': ...
    def getMiddleDate(self) -> 'AbsoluteDate': ...
    @typing.overload
    def mergeTo(self, comparableInterval: fr.cnes.sirius.patrius.math.interval.ComparableInterval[java.lang.Comparable]) -> fr.cnes.sirius.patrius.math.interval.ComparableInterval[java.lang.Comparable]: ...
    @typing.overload
    def mergeTo(self, absoluteDateInterval: 'AbsoluteDateInterval') -> 'AbsoluteDateInterval': ...
    @typing.overload
    def scale(self, double: float) -> 'AbsoluteDateInterval': ...
    @typing.overload
    def scale(self, double: float, absoluteDate: 'AbsoluteDate') -> 'AbsoluteDateInterval': ...
    @typing.overload
    def shift(self, double: float) -> 'AbsoluteDateInterval': ...
    @typing.overload
    def shift(self, double: float, double2: float) -> 'AbsoluteDateInterval': ...
    @typing.overload
    def toString(self) -> str: ...
    @typing.overload
    def toString(self, absoluteDate: 'AbsoluteDate') -> str: ...
    @typing.overload
    def toString(self, timeScale: 'TimeScale') -> str: ...

class AbsoluteDateIntervalsList(java.util.TreeSet[AbsoluteDateInterval]):
    """
    public class AbsoluteDateIntervalsList extends `TreeSet <http://docs.oracle.com/javase/8/docs/api/java/util/TreeSet.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`>
    
    
        This class represents a list of objects :class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`.
    
    
        It extends a TreeSet of :class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval` instances ; as the
        :class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval` objects implement the
        :class:`~fr.cnes.sirius.patrius.math.interval.ComparableInterval` class, the list is an ordered collection of time
        intervals.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`, `null
            <http://docs.oracle.com/javase/8/docs/api/java/util/TreeSet.html?is-external=true>`, :meth:`~serialized`
    """
    def __init__(self): ...
    def getComplementaryIntervals(self) -> 'AbsoluteDateIntervalsList':
        """
            Gets the list of complementary intervals of the given list of intervals.
        
        
        
            Returns:
                an :class:`~fr.cnes.sirius.patrius.time.AbsoluteDateIntervalsList` including all the complementary intervals
        
        
        """
        ...
    def getInclusiveInterval(self) -> AbsoluteDateInterval:
        """
            Gets the shortest interval containing all the intervals belonging to the list.
        
        
            While a date included in at least one of the listed intervals must be contained in this global interval, the opposite is
            not guaranteed (the inclusive interval can contain dates that do not belong to any listed interval).
        
            Returns:
                an :class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval` including all the intervals of the list
        
        
        """
        ...
    def getIntersectionWith(self, absoluteDateInterval: AbsoluteDateInterval) -> 'AbsoluteDateIntervalsList':
        """
            Returns the intersection between an interval and all the intervals of the list.
        
            The list returned can be empty if the provided interval does not intersects any interval of the list.
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): the interval
        
            Returns:
                the intersection between the interval and the list of intervals
        
        
        """
        ...
    def getIntervalsContainingDate(self, absoluteDate: 'AbsoluteDate') -> 'AbsoluteDateIntervalsList':
        """
            Gets the :class:`~fr.cnes.sirius.patrius.time.AbsoluteDateIntervalsList` containing the specified date. The list can
            contain zero, one or more :class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the date included in the time intervals
        
            Returns:
                a list of time intervals containing the input date.
        
        
        """
        ...
    def getMergedIntervals(self) -> 'AbsoluteDateIntervalsList':
        """
            Merges the intervals of the list that overlap and returns the list of merged intervals.
        
            The list returned should not contain any overlapping intervals.
        
            Returns:
                the list of merged intervals
        
        
        """
        ...
    def includes(self, absoluteDateInterval: AbsoluteDateInterval) -> bool:
        """
            Returns true if the provided interval is included in one of the intervals of the list.
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): the interval
        
            Returns:
                true if the interval is included in one of the intervals of the list
        
        
        """
        ...
    def overlaps(self, absoluteDateInterval: AbsoluteDateInterval) -> bool:
        """
            Returns true if the provided interval overlaps one of the intervals of the list.
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): the interval
        
            Returns:
                true if the interval overlaps one of the interval of the list
        
        
        """
        ...

class ChronologicalComparator(java.util.Comparator['TimeStamped'], java.io.Serializable):
    """
    public class ChronologicalComparator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Comparator <http://docs.oracle.com/javase/8/docs/api/java/util/Comparator.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.time.TimeStamped`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Comparator for :class:`~fr.cnes.sirius.patrius.time.TimeStamped` instance.
    
        :code:`null` is not an accepted value for generic :class:`~fr.cnes.sirius.patrius.time.ChronologicalComparator`. In
        order to handle :code:`null` values, a null-compliant comparator should be built with one of the following methods:
    
          - :code:`Comparator.nullsFirst(new ChronologicalComparator())`: :code:`null` values being set first
          - :code:`Comparator.nullsLast(new ChronologicalComparator())`: :code:`null` values being set last
    
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :class:`~fr.cnes.sirius.patrius.time.TimeStamped`,
            :meth:`~serialized`
    """
    def __init__(self): ...
    def compare(self, timeStamped: typing.Union['TimeStamped', typing.Callable], timeStamped2: typing.Union['TimeStamped', typing.Callable]) -> int:
        """
            Compare two time-stamped instances.
        
            Specified by:
                 in interface 
        
            Parameters:
                timeStamped1 (:class:`~fr.cnes.sirius.patrius.time.TimeStamped`): first time-stamped instance
                timeStamped2 (:class:`~fr.cnes.sirius.patrius.time.TimeStamped`): second time-stamped instance
        
            Returns:
                a negative integer, zero, or a positive integer as the first instance is before, simultaneous, or after the second one.
        
        
        """
        ...

class DateComponents(java.io.Serializable, java.lang.Comparable['DateComponents']):
    """
    public class DateComponents extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.time.DateComponents`>
    
        Class representing a date broken up as year, month and day components.
    
        This class uses the astronomical convention for calendars, which is also the convention used by :code:`java.util.Date`:
        a year zero is present between years -1 and +1, and 10 days are missing in 1582. The calendar used around these special
        dates are:
    
          - up to 0000-12-31 : proleptic julian calendar
          - from 0001-01-01 to 1582-10-04: julian calendar
          - from 1582-10-15: gregorian calendar
    
    
        Instances of this class are guaranteed to be immutable.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.TimeComponents`, :class:`~fr.cnes.sirius.patrius.time.DateTimeComponents`,
            :meth:`~serialized`
    """
    JULIAN_EPOCH: typing.ClassVar['DateComponents'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.DateComponents` JULIAN_EPOCH
    
        Reference epoch for julian dates: -4712-01-01.
    
        Both :code:`java.util.Date` and :class:`~fr.cnes.sirius.patrius.time.DateComponents` classes follow the astronomical
        conventions and consider a year 0 between years -1 and +1, hence this reference date lies in year -4712 and not in year
        -4713 as can be seen in other documents or programs that obey a different convention (for example the :code:`convcal`
        utility).
    
    """
    MODIFIED_JULIAN_EPOCH: typing.ClassVar['DateComponents'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.DateComponents` MODIFIED_JULIAN_EPOCH
    
        Reference epoch for modified julian dates: 1858-11-17.
    
    """
    FIFTIES_EPOCH: typing.ClassVar['DateComponents'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.DateComponents` FIFTIES_EPOCH
    
        Reference epoch for 1950 dates: 1950-01-01.
    
    """
    CCSDS_EPOCH: typing.ClassVar['DateComponents'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.DateComponents` CCSDS_EPOCH
    
        Reference epoch for CCSDS Time Code Format (CCSDS 301.0-B-4): 1958-01-01.
    
    """
    GALILEO_EPOCH: typing.ClassVar['DateComponents'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.DateComponents` GALILEO_EPOCH
    
        Reference epoch for Galileo System Time: 1999-08-22.
    
    """
    GPS_EPOCH: typing.ClassVar['DateComponents'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.DateComponents` GPS_EPOCH
    
        Reference epoch for GPS weeks: 1980-01-06.
    
    """
    BEIDOU_EPOCH: typing.ClassVar['DateComponents'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.DateComponents` BEIDOU_EPOCH
    
        Reference epoch for BeiDou weeks: 2006-01-01 00:00:00 UTC.
    
    """
    J2000_EPOCH: typing.ClassVar['DateComponents'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.DateComponents` J2000_EPOCH
    
        J2000.0 Reference epoch: 2000-01-01.
    
    """
    JAVA_EPOCH: typing.ClassVar['DateComponents'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.DateComponents` JAVA_EPOCH
    
        Java Reference epoch: 1970-01-01.
    
    """
    @typing.overload
    def __init__(self, dateComponents: 'DateComponents', int: int): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, month: 'Month', int2: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int, int3: int): ...
    def compareTo(self, dateComponents: 'DateComponents') -> int:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    @staticmethod
    def createFromWeekComponents(int: int, int2: int, int3: int) -> 'DateComponents':
        """
            Build a date from week components.
        
            The calendar week number is a number between 1 and 52 or 53 depending on the year. Week 1 is defined by ISO as the one
            that includes the first Thursday of a year. Week 1 may therefore start the previous year and week 52 or 53 may end in
            the next year. As an example calendar date 1995-01-01 corresponds to week date 1994-W52-7 (i.e. Sunday in the last week
            of 1994 is in fact the first day of year 1995). This date would beAnother example is calendar date 1996-12-31 which
            corresponds to week date 1997-W01-2 (i.e. Tuesday in the first week of 1997 is in fact the last day of year 1996).
        
            Parameters:
                wYear (int): year associated to week numbering
                week (int): week number in year,from 1 to 52 or 53
                dayOfWeek (int): day of week, from 1 (Monday) to 7 (Sunday)
        
            Returns:
                a builded date
        
            Raises:
                : if inconsistent arguments are given (parameters out of range, week 53 on a 52 weeks year ...)
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getCalendarWeek(self) -> int:
        """
            Get the calendar week number.
        
            The calendar week number is a number between 1 and 52 or 53 depending on the year. Week 1 is defined by ISO as the one
            that includes the first Thursday of a year. Week 1 may therefore start the previous year and week 52 or 53 may end in
            the next year. As an example calendar date 1995-01-01 corresponds to week date 1994-W52-7 (i.e. Sunday in the last week
            of 1994 is in fact the first day of year 1995). Another example is calendar date 1996-12-31 which corresponds to week
            date 1997-W01-2 (i.e. Tuesday in the first week of 1997 is in fact the last day of year 1996).
        
            Returns:
                calendar week number
        
        
        """
        ...
    def getDay(self) -> int:
        """
            Get the day.
        
            Returns:
                day number from 1 to 31
        
        
        """
        ...
    def getDayOfWeek(self) -> int:
        """
            Get the day of week.
        
            Day of week is a number between 1 (Monday) and 7 (Sunday).
        
            Returns:
                day of week
        
        
        """
        ...
    def getDayOfYear(self) -> int:
        """
            Get the day number in year.
        
            Day number in year is between 1 (January 1st) and either 365 or 366 inclusive depending on year.
        
            Returns:
                day number in year
        
        
        """
        ...
    def getJ2000Day(self) -> int:
        """
            Get the day number with respect to J2000 epoch.
        
            Returns:
                day number with respect to J2000 epoch
        
        
        """
        ...
    def getMJD(self) -> int:
        """
            Get the modified julian day.
        
            Returns:
                modified julian day
        
        
        """
        ...
    def getMonth(self) -> int:
        """
            Get the month.
        
            Returns:
                month number from 1 to 12
        
        
        """
        ...
    def getMonthEnum(self) -> 'Month':
        """
            Get the month as an enumerate.
        
            Returns:
                month as an enumerate
        
        
        """
        ...
    def getYear(self) -> int:
        """
            Get the year number.
        
            Returns:
                year number (may be 0 or negative for BC years)
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @staticmethod
    def parseDate(string: str) -> 'DateComponents':
        """
            Parse a string in ISO-8601 format to build a date.
        
            The supported formats are:
        
              - basic format calendar date: YYYYMMDD
              - extended format calendar date: YYYY-MM-DD
              - basic format ordinal date: YYYYDDD
              - extended format ordinal date: YYYY-DDD
              - basic format week date: YYYYWwwD
              - extended format week date: YYYY-Www-D
        
            As shown by the list above, only the complete representations defined in section 4.1 of ISO-8601 standard are supported,
            neither expended representations nor representations with reduced accuracy are supported.
        
            Parsing a single integer as a julian day is *not* supported as it may be ambiguous with either the basic format calendar
            date or the basic format ordinal date depending on the number of digits.
        
            Parameters:
                string (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): string to parse
        
            Returns:
                a parsed date
        
            Raises:
                : if string cannot be parsed
        
        
        """
        ...
    def toString(self) -> str:
        """
            Get a string representation (ISO-8601) of the date.
        
            Overrides:
                 in class 
        
            Returns:
                string representation of the date.
        
        
        """
        ...

class DateTimeComponents(java.io.Serializable, java.lang.Comparable['DateTimeComponents']):
    """
    public class DateTimeComponents extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.time.DateTimeComponents`>
    
        Holder for date and time components.
    
        This class is a simple holder with no processing methods.
    
        Instance of this class are guaranteed to be immutable.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :class:`~fr.cnes.sirius.patrius.time.DateComponents`,
            :class:`~fr.cnes.sirius.patrius.time.TimeComponents`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, dateComponents: DateComponents, timeComponents: 'TimeComponents'): ...
    @typing.overload
    def __init__(self, dateTimeComponents: 'DateTimeComponents', double: float): ...
    @typing.overload
    def __init__(self, int: int, month: 'Month', int2: int): ...
    @typing.overload
    def __init__(self, int: int, month: 'Month', int2: int, int3: int, int4: int, double: float): ...
    @typing.overload
    def __init__(self, int: int, int2: int, int3: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int, int3: int, int4: int, int5: int, double: float): ...
    def compareTo(self, dateTimeComponents: 'DateTimeComponents') -> int:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getDate(self) -> DateComponents:
        """
            Get the date component.
        
            Returns:
                date component
        
        
        """
        ...
    def getTime(self) -> 'TimeComponents':
        """
            Get the time component.
        
            Returns:
                time component
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def offsetFrom(self, dateTimeComponents: 'DateTimeComponents') -> float:
        """
            Compute the seconds offset between two instances.
        
            Parameters:
                dateTime (:class:`~fr.cnes.sirius.patrius.time.DateTimeComponents`): dateTime to subtract from the instance
        
            Returns:
                offset in seconds between the two instants (positive if the instance is posterior to the argument)
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.DateTimeComponents.DateTimeComponents`
        
        
        """
        ...
    @staticmethod
    def parseDateTime(string: str) -> 'DateTimeComponents':
        """
            Parse a string in ISO-8601 format to build a date/time.
        
            The supported formats are all date formats supported by :meth:`~fr.cnes.sirius.patrius.time.DateComponents.parseDate`
            and all time formats supported by :meth:`~fr.cnes.sirius.patrius.time.TimeComponents.parseTime` separated by the
            standard time separator 'T', or date components only (in which case a 00:00:00 hour is implied). Typical examples are
            2000-01-01T12:00:00Z or 1976W186T210000.
        
            Parameters:
                string (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): string to parse
        
            Returns:
                a parsed date/time
        
            Raises:
                : if string cannot be parsed
        
        
        """
        ...
    def toString(self) -> str:
        """
            Return a string representation of this pair.
        
            The format used is ISO8601.
        
            Overrides:
                 in class 
        
            Returns:
                string representation of this pair
        
        protected `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` toString(int precision, boolean isTimeNearLeapSecond)
        
            Return a string representation of this pair.
        
            The format used is ISO8601.
        
            Parameters:
                precision (int): digit number of the seconds fractional part
                isTimeNearLeapSecond (boolean): true if the date is inside or immediately before a leap second. It is used to set the upper boundary of the current day:
                    23:59:60.99.. when true, 23:59:59.99.. when false.
        
            Returns:
                a string representation of the instance, in ISO-8601 format with a seconds accuracy defined as input
        
        
        """
        ...

_IntervalMapSearcher__T = typing.TypeVar('_IntervalMapSearcher__T')  # <T>
class IntervalMapSearcher(java.lang.Iterable[fr.cnes.sirius.patrius.tools.cache.CacheEntry[AbsoluteDateInterval, _IntervalMapSearcher__T]], java.io.Serializable, typing.Generic[_IntervalMapSearcher__T]):
    """
    public class IntervalMapSearcher<T> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Iterable <http://docs.oracle.com/javase/8/docs/api/java/lang/Iterable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.tools.cache.CacheEntry`<:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`,T>>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class associates objects to :class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`. It allows to get
        efficiently the object corresponding to a given date.
    
        Since:
            4.13
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_CACHE_SIZE: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_CACHE_SIZE
    
        Default cache size.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, collection: typing.Union[java.util.Collection[AbsoluteDateInterval], typing.Sequence[AbsoluteDateInterval], typing.Set[AbsoluteDateInterval]], collection2: typing.Union[java.util.Collection[_IntervalMapSearcher__T], typing.Sequence[_IntervalMapSearcher__T], typing.Set[_IntervalMapSearcher__T]]): ...
    @typing.overload
    def __init__(self, collection: typing.Union[java.util.Collection[AbsoluteDateInterval], typing.Sequence[AbsoluteDateInterval], typing.Set[AbsoluteDateInterval]], collection2: typing.Union[java.util.Collection[_IntervalMapSearcher__T], typing.Sequence[_IntervalMapSearcher__T], typing.Set[_IntervalMapSearcher__T]], int: int): ...
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[AbsoluteDateInterval, _IntervalMapSearcher__T], typing.Mapping[AbsoluteDateInterval, _IntervalMapSearcher__T]]): ...
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[AbsoluteDateInterval, _IntervalMapSearcher__T], typing.Mapping[AbsoluteDateInterval, _IntervalMapSearcher__T]], int: int): ...
    def containsData(self, absoluteDate: 'AbsoluteDate') -> bool:
        """
            Check if the provided date belongs to any available interval.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date to check
        
            Returns:
                :code:`true` if the date belongs to an available interval
        
        
        """
        ...
    @typing.overload
    def getData(self, absoluteDate: 'AbsoluteDate') -> _IntervalMapSearcher__T:
        """
            Getter for the object associated to the provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date associated to the object
        
            Returns:
                the corresponding object
        
            Raises:
                : if the provided date does not belong to any of the intervals
        
            Getter for the object associated to the provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date associated to the object
                throwException (boolean): Indicate if the method should throw an exception if the provided date does not belong to any of the intervals
        
            Returns:
                the corresponding object
        
            Raises:
                : if :code:`throwException == true` and the provided date does not belong to any of the intervals
        
        
        """
        ...
    @typing.overload
    def getData(self, absoluteDate: 'AbsoluteDate', boolean: bool) -> _IntervalMapSearcher__T: ...
    @typing.overload
    def getData(self) -> java.util.List[_IntervalMapSearcher__T]: ...
    @typing.overload
    def getEntry(self, absoluteDate: 'AbsoluteDate') -> fr.cnes.sirius.patrius.tools.cache.CacheEntry[AbsoluteDateInterval, _IntervalMapSearcher__T]: ...
    @typing.overload
    def getEntry(self, absoluteDate: 'AbsoluteDate', boolean: bool) -> fr.cnes.sirius.patrius.tools.cache.CacheEntry[AbsoluteDateInterval, _IntervalMapSearcher__T]: ...
    def getFirstInterval(self) -> AbsoluteDateInterval:
        """
            Getter for the first interval.
        
            Returns:
                the first interval
        
        
        """
        ...
    def getIntervalDataAssociation(self) -> java.util.Map[AbsoluteDateInterval, _IntervalMapSearcher__T]: ...
    def getIntervals(self) -> AbsoluteDateIntervalsList:
        """
            Getter for the available intervals.
        
            Returns:
                the available intervals
        
        
        """
        ...
    def getLastInterval(self) -> AbsoluteDateInterval:
        """
            Getter for the last interval.
        
            Returns:
                the last interval
        
        
        """
        ...
    def iterator(self) -> java.util.Iterator[fr.cnes.sirius.patrius.tools.cache.CacheEntry[AbsoluteDateInterval, _IntervalMapSearcher__T]]: ...
    def size(self) -> int:
        """
            Return the number of elements.
        
            Returns:
                the number of elements
        
        
        """
        ...
    @typing.overload
    def toArray(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.tools.cache.CacheEntry[AbsoluteDateInterval, _IntervalMapSearcher__T]]: ...
    @typing.overload
    def toArray(self, boolean: bool) -> typing.MutableSequence[fr.cnes.sirius.patrius.tools.cache.CacheEntry[AbsoluteDateInterval, _IntervalMapSearcher__T]]: ...

class LocalTimeAngle(java.io.Serializable):
    """
    public class LocalTimeAngle extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class provides methods to compute local time angle (true local time angle and mean local time angle).
    
        The local time is represented by the angle between the projections of the Sun and the satellite in the equatorial plane;
        therefore this angle is equal to zero when the local time is 12.00h and Π when the local time is 0.00h (Local Time In
        Hours = 12.00h + local time angle * 12 / Π).
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    def computeEquationOfTime(self, absoluteDate: 'AbsoluteDate') -> float: ...
    @typing.overload
    def computeMeanLocalTimeAngle(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> float: ...
    @typing.overload
    def computeMeanLocalTimeAngle(self, absoluteDate: 'AbsoluteDate', vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def computeRAANFromMeanLocalTime(self, absoluteDate: 'AbsoluteDate', double: float) -> float: ...
    def computeRAANFromTrueLocalTime(self, absoluteDate: 'AbsoluteDate', double: float, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    @typing.overload
    def computeTrueLocalTimeAngle(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> float: ...
    @typing.overload
    def computeTrueLocalTimeAngle(self, absoluteDate: 'AbsoluteDate', vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...

class Month(java.lang.Enum['Month']):
    """
    public enum Month extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.time.Month`>
    
        Enumerate representing a calendar month.
    
        This enum is mainly useful to parse data files that use month names like Jan or JAN or January or numbers like 1 or 01.
        It handles month numbers as well as three letters abbreviation and full names, independently of capitalization.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.DateComponents`
    """
    JANUARY: typing.ClassVar['Month'] = ...
    FEBRUARY: typing.ClassVar['Month'] = ...
    MARCH: typing.ClassVar['Month'] = ...
    APRIL: typing.ClassVar['Month'] = ...
    MAY: typing.ClassVar['Month'] = ...
    JUNE: typing.ClassVar['Month'] = ...
    JULY: typing.ClassVar['Month'] = ...
    AUGUST: typing.ClassVar['Month'] = ...
    SEPTEMBER: typing.ClassVar['Month'] = ...
    OCTOBER: typing.ClassVar['Month'] = ...
    NOVEMBER: typing.ClassVar['Month'] = ...
    DECEMBER: typing.ClassVar['Month'] = ...
    def getCapitalizedAbbreviation(self) -> str:
        """
            Get the capitalized three letters abbreviation.
        
            Returns:
                capitalized three letters abbreviation
        
        
        """
        ...
    def getCapitalizedName(self) -> str:
        """
            Get the capitalized full name.
        
            Returns:
                capitalized full name
        
        
        """
        ...
    def getLowerCaseAbbreviation(self) -> str:
        """
            Get the lower case three letters abbreviation.
        
            Returns:
                lower case three letters abbreviation
        
        
        """
        ...
    def getLowerCaseName(self) -> str:
        """
            Get the lower case full name.
        
            Returns:
                lower case full name
        
        
        """
        ...
    @staticmethod
    def getMonth(int: int) -> 'Month':
        """
            Get the month corresponding to a number.
        
            Parameters:
                number (int): month number
        
            Returns:
                the month corresponding to the string
        
            Raises:
                : if the string does not correspond to a month
        
        
        """
        ...
    def getNumber(self) -> int:
        """
            Get the month number.
        
            Returns:
                month number between 1 and 12
        
        
        """
        ...
    def getUpperCaseAbbreviation(self) -> str:
        """
            Get the upper case three letters abbreviation.
        
            Returns:
                upper case three letters abbreviation
        
        
        """
        ...
    def getUpperCaseName(self) -> str:
        """
            Get the upper case full name.
        
            Returns:
                upper case full name
        
        
        """
        ...
    @staticmethod
    def parseMonth(string: str) -> 'Month':
        """
            Parse the string to get the month.
        
            The string can be either the month number, the full name or the three letter abbreviation. The parsing ignore the case
            of the specified string and trims surrounding blanks.
        
            Parameters:
                s (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): string to parse
        
            Returns:
                the month corresponding to the string
        
            Raises:
                : if the string does not correspond to a month
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'Month':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                : if this enum type has no constant with the specified name
                : if the argument is null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['Month']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (Month c : Month.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class TDBModel:
    """
    public interface TDBModel
    
        Barycentric Dynamic Time model.
    
        TDB is time used to take account of time dilation when calculating orbits of planets, asteroids, comets and
        interplanetary spacecraft in the Solar system. It was based on a Dynamical time scale but was not well defined and not
        rigorously correct as a relativistic time scale. It was subsequently deprecated in favour of Barycentric Coordinate Time
        (TCB), but at the 2006 General Assembly of the International Astronomical Union TDB was rehabilitated by making it a
        specific fixed linear transformation of TCB.
    
        Since:
            4.7
    """
    def offsetFromTAI(self, absoluteDate: 'AbsoluteDate') -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to
            :class:`~fr.cnes.sirius.patrius.time.TDBScale`.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
        
        """
        ...

class TimeComponents(java.io.Serializable, java.lang.Comparable['TimeComponents']):
    """
    public class TimeComponents extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.time.TimeComponents`>
    
        Class representing a time within the day broken up as hour, minute and second components.
    
        Instances of this class are guaranteed to be immutable.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.DateComponents`, :class:`~fr.cnes.sirius.patrius.time.DateTimeComponents`,
            :meth:`~serialized`
    """
    DEFAULT_SECONDS_PRECISION: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_SECONDS_PRECISION
    
        Default digit number of the seconds fractional part.
    
        Also see:
            :meth:`~constant`
    
    
    """
    H00: typing.ClassVar['TimeComponents'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.TimeComponents` H00
    
        Constant for commonly used hour 00:00:00.
    
    """
    H12: typing.ClassVar['TimeComponents'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.TimeComponents` H12
    
        Constant for commonly used hour 12:00:00.
    
    """
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, int: int, double: float): ...
    @typing.overload
    def __init__(self, int: int, int2: int, double: float): ...
    @typing.overload
    def __init__(self, int: int, int2: int, int3: int, double: float): ...
    def compareTo(self, timeComponents: 'TimeComponents') -> int:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getFractionSeconds(self) -> float:
        """
            Get the fractional part of seconds.
        
            Returns:
                fractional part of seconds
        
        
        """
        ...
    def getHour(self) -> int:
        """
            Get the hour number.
        
            Returns:
                hour number from 0 to 23
        
        
        """
        ...
    def getMinute(self) -> int:
        """
            Get the minute number.
        
            Returns:
                minute minute number from 0 to 59
        
        
        """
        ...
    def getPreciseSecondsInDay(self) -> java.math.BigDecimal:
        """
            Get the precise second number within the day.
        
            Returns:
                second number from 0.0 to Constants.JULIAN_DAY
        
        
        """
        ...
    def getSecond(self) -> float:
        """
            Get the seconds number (it includes the fractional part of seconds).
        
            Returns:
                second second number from 0.0 to 60.0 (excluded)
        
        
        """
        ...
    def getSecondsInDay(self) -> float:
        """
            Get the second number within the day.
        
            Returns:
                second number from 0.0 to Constants.JULIAN_DAY
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @staticmethod
    def parseTime(string: str) -> 'TimeComponents':
        """
            Parse a string in ISO-8601 format to build a time.
        
            The supported formats are:
        
              - basic format local time: hhmmss (with optional decimals in seconds)
              - extended format local time: hh:mm:ss (with optional decimals in seconds)
              - basic format UTC time: hhmmssZ (with optional decimals in seconds)
              - extended format UTC time: hh:mm:ssZ (with optional decimals in seconds)
              - basic format local time with 00h UTC offset: hhmmss+00 (with optional decimals in seconds)
              - extended format local time with 00h UTC offset: hhmmss+00 (with optional decimals in seconds)
              - basic format local time with 00h and 00m UTC offset: hhmmss+00:00 (with optional decimals in seconds)
              - extended format local time with 00h and 00m UTC offset: hhmmss+00:00 (with optional decimals in seconds)
        
            As shown by the list above, only the complete representations defined in section 4.2 of ISO-8601 standard are supported,
            neither expended representations nor representations with reduced accuracy are supported.
        
            As this class does not support time zones (because space flight dynamics uses
            :class:`~fr.cnes.sirius.patrius.time.TimeScale` with offsets from UTC having sub-second accuracy), only UTC is zone is
            supported (and in fact ignored). It is the responsibility of the :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`
            class to handle time scales appropriately.
        
            Parameters:
                string (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): string to parse
        
            Returns:
                a parsed time
        
            Raises:
                : if string cannot be parsed
        
        
        """
        ...
    @typing.overload
    def toString(self) -> str:
        """
            Get a string representation of the time.
        
            Overrides:
                 in class 
        
            Returns:
                string representation of the time
        
        """
        ...
    @typing.overload
    def toString(self, int: int) -> str:
        """
            Get a string representation of the time.
        
            Parameters:
                precision (int): digit number of the seconds fractional part
        
            Returns:
                string representation of the time
        
            Get a string representation of the time.
        
            Parameters:
                precision (int): digit number of the seconds fractional part
                isTimeNearLeapSecond (boolean): true if the date is inside or immediately before a leap second. It is used to set the upper boundary of the current day:
                    23:59:60.99.. when true, 23:59:59.99.. when false.
        
            Returns:
                string representation of the time
        
            Raises:
                : if inconsistent arguments are given (negative precision)
        
        
        """
        ...
    @typing.overload
    def toString(self, int: int, boolean: bool) -> str: ...

_TimeInterpolable__T = typing.TypeVar('_TimeInterpolable__T', bound='TimeInterpolable')  # <T>
class TimeInterpolable(typing.Generic[_TimeInterpolable__T]):
    """
    public interface TimeInterpolable<T extends TimeInterpolable<T>>
    
        This interface represents objects that can be interpolated in time.
    """
    def interpolate(self, absoluteDate: 'AbsoluteDate', collection: typing.Union[java.util.Collection[_TimeInterpolable__T], typing.Sequence[_TimeInterpolable__T], typing.Set[_TimeInterpolable__T]]) -> _TimeInterpolable__T: ...

class TimeScale(java.io.Serializable):
    """
    public interface TimeScale extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for time scales.
    
        This is the interface representing all time scales. Time scales are related to each other by some offsets that may be
        discontinuous (for example the :class:`~fr.cnes.sirius.patrius.time.UTCScale` with respect to the
        :class:`~fr.cnes.sirius.patrius.time.TAIScale`).
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`
    """
    def getName(self) -> str:
        """
            Get the name time scale.
        
            Returns:
                name of the time scale
        
        
        """
        ...
    def offsetFromTAI(self, absoluteDate: 'AbsoluteDate') -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to instance.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI`
        
        
        """
        ...
    def offsetToTAI(self, dateComponents: DateComponents, timeComponents: TimeComponents) -> float:
        """
            Get the offset to convert locations from instance to :class:`~fr.cnes.sirius.patrius.time.TAIScale`.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.DateComponents`): date location in the time scale
                time (:class:`~fr.cnes.sirius.patrius.time.TimeComponents`): time location in the time scale
        
            Returns:
                offset in seconds to add to a location in *instance time scale* to get a location in
                *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI`
        
        
        """
        ...

class TimeScalesFactory(java.io.Serializable):
    @staticmethod
    def addDefaultUTCTAILoader() -> None: ...
    @staticmethod
    def addUTCTAILoader(uTCTAILoader: 'UTCTAILoader') -> None: ...
    @staticmethod
    def clearTimeScales() -> None: ...
    @staticmethod
    def clearUTCTAILoaders() -> None: ...
    @staticmethod
    def get(string: str) -> TimeScale: ...
    @staticmethod
    def getGMST() -> 'GMSTScale': ...
    @staticmethod
    def getGPS() -> 'GPSScale': ...
    @staticmethod
    def getGST() -> 'GalileoScale': ...
    @staticmethod
    def getTAI() -> 'TAIScale': ...
    @staticmethod
    def getTCB() -> 'TCBScale': ...
    @staticmethod
    def getTCG() -> 'TCGScale': ...
    @staticmethod
    def getTDB() -> 'TDBScale': ...
    @staticmethod
    def getTT() -> 'TTScale': ...
    @staticmethod
    def getUT1() -> 'UT1Scale': ...
    @staticmethod
    def getUTC() -> 'UTCScale': ...

_TimeShiftable__T = typing.TypeVar('_TimeShiftable__T', bound='TimeShiftable')  # <T>
class TimeShiftable(typing.Generic[_TimeShiftable__T]):
    """
    public interface TimeShiftable<T extends TimeShiftable<T>>
    
        This interface represents objects that can be shifted in time.
    """
    def shiftedBy(self, double: float) -> _TimeShiftable__T: ...

class TimeStamped:
    """
    public interface TimeStamped
    
        This interface represents objects that have a :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` date attached to them.
    
        Classes implementing this interface can be stored chronologically in sorted sets using
        :class:`~fr.cnes.sirius.patrius.time.ChronologicalComparator` as the underlying comparator. An example using for
        :class:`~fr.cnes.sirius.patrius.orbits.Orbit` instances is given here:
    
        .. code-block: java
        
        
             SortedSet<Orbit> sortedOrbits =
                 new TreeSet<Orbit>(new ChronologicalComparator());
             sortedOrbits.add(orbit1);
             sortedOrbits.add(orbit2);
             ...
         
    
        This interface is also the base interface used to :class:`~fr.cnes.sirius.patrius.time.TimeStampedCache` series of
        time-dependent objects for interpolation in a thread-safe manner.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :class:`~fr.cnes.sirius.patrius.time.ChronologicalComparator`,
            :class:`~fr.cnes.sirius.patrius.time.TimeStampedCache`
    """
    def getDate(self) -> 'AbsoluteDate':
        """
            Get the date.
        
            Returns:
                date attached to the object
        
        
        """
        ...

_TimeStampedCache__T = typing.TypeVar('_TimeStampedCache__T', bound=TimeStamped)  # <T>
class TimeStampedCache(java.io.Serializable, typing.Generic[_TimeStampedCache__T]):
    """
    public class TimeStampedCache<T extends :class:`~fr.cnes.sirius.patrius.time.TimeStamped`> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Generic thread-safe cache for :class:`~fr.cnes.sirius.patrius.time.TimeStamped` data.
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_CACHED_SLOTS_NUMBER: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_CACHED_SLOTS_NUMBER
    
        Default number of independent cached time slots.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self, int: int, int2: int, double: float, double2: float, timeStampedGenerator: typing.Union['TimeStampedGenerator'[_TimeStampedCache__T], typing.Callable[[_TimeStampedCache__T, 'AbsoluteDate'], java.util.List[TimeStamped]]], class_: typing.Type[_TimeStampedCache__T]): ...
    def getEarliest(self) -> _TimeStampedCache__T:
        """
            Get the earliest cached entry.
        
            Returns:
                earliest cached entry
        
            Raises:
                : if the cache has no slots at all
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStampedCache.getSlots`
        
        
        """
        ...
    def getEntries(self) -> int:
        """
            Get the total number of entries cached.
        
            Returns:
                total number of entries cached
        
        
        """
        ...
    def getGenerateCalls(self) -> int:
        """
            Get the number of calls to the generate method.
        
            This number of calls is related to the number of cache misses and may be used to tune the cache configuration. Each
            cache miss implies at least one call is performed, but may require several calls if the new date is far offset from the
            existing cache, depending on the number of elements and step between elements in the arrays returned by the generator.
        
            Returns:
                number of calls to the generate method
        
        
        """
        ...
    def getGenerator(self) -> 'TimeStampedGenerator'[_TimeStampedCache__T]: ...
    def getLatest(self) -> _TimeStampedCache__T:
        """
            Get the latest cached entry.
        
            Returns:
                latest cached entry
        
            Raises:
                : if the cache has no slots at all
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStampedCache.getSlots`
        
        
        """
        ...
    def getMaxSlots(self) -> int:
        """
            Get the maximum number of independent cached time slots.
        
            Returns:
                maximum number of independent cached time slots
        
        
        """
        ...
    def getMaxSpan(self) -> float:
        """
            Get the maximum duration span in seconds of one slot.
        
            Returns:
                maximum duration span in seconds of one slot
        
        
        """
        ...
    def getNeighbors(self, absoluteDate: 'AbsoluteDate') -> typing.MutableSequence[_TimeStampedCache__T]: ...
    def getNeighborsSize(self) -> int:
        """
            Get the fixed size of the arrays to be returned by :meth:`~fr.cnes.sirius.patrius.time.TimeStampedCache.getNeighbors`.
        
            Returns:
                size of the array
        
        
        """
        ...
    def getNewSlotQuantumGap(self) -> float:
        """
            Get quantum gap above which a new slot is created instead of extending an existing one.
        
            The quantum gap is the :code:`newSlotInterval` value provided at construction rounded to the nearest quantum step used
            internally by the cache.
        
            Returns:
                quantum gap in seconds
        
        
        """
        ...
    def getSlots(self) -> int:
        """
            Get the number of slots in use.
        
            Returns:
                number of slots in use
        
        
        """
        ...
    def getSlotsEvictions(self) -> int:
        """
            Get the number of slots evictions.
        
            This number should remain small when the max number of slots is sufficient with respect to the number of concurrent
            requests to the cache. If it increases too much, then the cache configuration is probably bad and cache does not really
            improve things (in this case, the :meth:`~fr.cnes.sirius.patrius.time.TimeStampedCache.getGenerateCalls` will probably
            increase too.
        
            Returns:
                number of slots evictions
        
        
        """
        ...

_TimeStampedGenerator__T = typing.TypeVar('_TimeStampedGenerator__T', bound=TimeStamped)  # <T>
class TimeStampedGenerator(java.io.Serializable, typing.Generic[_TimeStampedGenerator__T]):
    """
    public interface TimeStampedGenerator<T extends :class:`~fr.cnes.sirius.patrius.time.TimeStamped`> extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Generator to use for creating entries in :class:`~fr.cnes.sirius.patrius.time.TimeStampedCache`.
    
        As long as a generator is referenced by one :class:`~fr.cnes.sirius.patrius.time.TimeStampedCache` only, it is
        guaranteed to be called in a thread-safe way, even if the cache is used in a multi-threaded environment. The cache takes
        care of scheduling the calls to all the methods defined in this interface so only one thread uses them at any time.
        There is no need for the implementing classes to handle synchronization or locks by themselves.
    
        The generator is provided by the user of the :class:`~fr.cnes.sirius.patrius.time.TimeStampedCache` and should be
        consistent with the way he will use the cached data.
    
        If entries must have regular time gaps (for example one entry every 3600 seconds), then the generator must ensure by
        itself all generated entries are exactly located on the expected regular grid, even if they are generated in random
        order. The reason for that is that the cache may ask for entries in different ranges and merge these ranges afterwards.
        A typical example would be a cache first calling the generator for 6 points around 2012-02-19T17:48:00 and when these
        points are exhausted calling the generator again for 6 new points around 2012-02-19T23:20:00. If all points must be
        exactly 3600 seconds apart, the generator should generate the first 6 points at 2012-02-19T15:00:00,
        2012-02-19T16:00:00, 2012-02-19T17:00:00, 2012-02-19T18:00:00, 2012-02-19T19:00:00 and 2012-02-19T20:00:00, and the next
        6 points at 2012-02-19T21:00:00, 2012-02-19T22:00:00, 2012-02-19T23:00:00, 2012-02-20T00:00:00, 2012-02-20T01:00:00 and
        2012-02-20T02:00:00. If the separation between the points is irrelevant, the first points could be generated at 17:48:00
        instead of 17:00:00 or 18:00:00. The cache *will* merge arrays returned from different calls in the same global time
        slot.
    """
    def generate(self, t: _TimeStampedGenerator__T, absoluteDate: 'AbsoluteDate') -> java.util.List[_TimeStampedGenerator__T]: ...

class UTCTAILoader(fr.cnes.sirius.patrius.data.DataLoader):
    """
    public interface UTCTAILoader extends :class:`~fr.cnes.sirius.patrius.data.DataLoader`
    
        Interface for loading UTC-TAI offsets data files.
    """
    def getSupportedNames(self) -> str:
        """
            Get the regular expression for supported UTC-TAI offsets files names.
        
            Returns:
                regular expression for supported UTC-TAI offsets files names
        
        
        """
        ...
    def loadTimeSteps(self) -> java.util.SortedMap[DateComponents, int]: ...

class AbsoluteDate(TimeStamped, TimeShiftable['AbsoluteDate'], java.lang.Comparable['AbsoluteDate'], java.io.Serializable):
    JULIAN_EPOCH: typing.ClassVar['AbsoluteDate'] = ...
    MODIFIED_JULIAN_EPOCH: typing.ClassVar['AbsoluteDate'] = ...
    FIFTIES_EPOCH_TT: typing.ClassVar['AbsoluteDate'] = ...
    FIFTIES_EPOCH_TAI: typing.ClassVar['AbsoluteDate'] = ...
    FIFTIES_EPOCH_UTC: typing.ClassVar['AbsoluteDate'] = ...
    CCSDS_EPOCH: typing.ClassVar['AbsoluteDate'] = ...
    GALILEO_EPOCH: typing.ClassVar['AbsoluteDate'] = ...
    GPS_EPOCH: typing.ClassVar['AbsoluteDate'] = ...
    BEIDOU_EPOCH: typing.ClassVar['AbsoluteDate'] = ...
    J2000_EPOCH: typing.ClassVar['AbsoluteDate'] = ...
    JAVA_EPOCH: typing.ClassVar['AbsoluteDate'] = ...
    PAST_INFINITY: typing.ClassVar['AbsoluteDate'] = ...
    FUTURE_INFINITY: typing.ClassVar['AbsoluteDate'] = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, absoluteDate: 'AbsoluteDate', double: float): ...
    @typing.overload
    def __init__(self, absoluteDate: 'AbsoluteDate', double: float, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, dateComponents: DateComponents, timeComponents: TimeComponents, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, dateComponents: DateComponents, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, dateTimeComponents: DateTimeComponents, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, int: int, month: Month, int2: int, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, int: int, month: Month, int2: int, int3: int, int4: int, double: float, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, int: int, int2: int, int3: int, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, int: int, int2: int, int3: int, int4: int, int5: int, double: float): ...
    @typing.overload
    def __init__(self, int: int, int2: int, int3: int, int4: int, int5: int, double: float, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, string: str, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, localDateTime: java.time.LocalDateTime, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, date: java.util.Date, timeScale: TimeScale): ...
    @typing.overload
    def __init__(self, long: int, double: float): ...
    def compareTo(self, absoluteDate: 'AbsoluteDate') -> int: ...
    @staticmethod
    def createGPSDate(int: int, double: float) -> 'AbsoluteDate': ...
    @typing.overload
    def durationFrom(self, absoluteDate: 'AbsoluteDate') -> float: ...
    @typing.overload
    def durationFrom(self, absoluteDate: 'AbsoluteDate', timeScale: TimeScale) -> float: ...
    def durationFromJ2000EpochInCenturies(self) -> float: ...
    def durationFromJ2000EpochInDays(self) -> float: ...
    def durationFromJ2000EpochInSeconds(self) -> float: ...
    def durationFromJ2000EpochInYears(self) -> float: ...
    @typing.overload
    def equals(self, object: typing.Any) -> bool: ...
    @typing.overload
    def equals(self, object: typing.Any, double: float) -> bool: ...
    def getComponents(self, timeScale: TimeScale) -> DateTimeComponents: ...
    def getDate(self) -> 'AbsoluteDate': ...
    def getEpoch(self) -> int: ...
    def getMilliInWeek(self) -> float: ...
    def getOffset(self) -> float: ...
    def getSecondsInDay(self, timeScale: TimeScale) -> float: ...
    def getWeekNumber(self) -> int: ...
    def hashCode(self) -> int: ...
    def offsetFrom(self, absoluteDate: 'AbsoluteDate', timeScale: TimeScale) -> float: ...
    @staticmethod
    def parseCCSDSCalendarSegmentedTimeCode(byte: int, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> 'AbsoluteDate': ...
    @staticmethod
    def parseCCSDSDaySegmentedTimeCode(byte: int, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], dateComponents: DateComponents) -> 'AbsoluteDate': ...
    @staticmethod
    def parseCCSDSUnsegmentedTimeCode(byte: int, byte2: int, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes], absoluteDate: 'AbsoluteDate') -> 'AbsoluteDate': ...
    def preciseDurationFrom(self, absoluteDate: 'AbsoluteDate') -> float: ...
    @typing.overload
    def shiftedBy(self, double: float) -> 'AbsoluteDate': ...
    @typing.overload
    def shiftedBy(self, double: float, absoluteDate: 'AbsoluteDate', boolean: bool) -> 'AbsoluteDate': ...
    @typing.overload
    def shiftedBy(self, double: float, timeScale: TimeScale) -> 'AbsoluteDate': ...
    def timeScalesOffset(self, timeScale: TimeScale, timeScale2: TimeScale) -> float: ...
    def toCNESJulianDate(self, timeScale: TimeScale) -> float: ...
    def toDate(self, timeScale: TimeScale) -> java.util.Date: ...
    def toLocalDateTime(self, timeScale: TimeScale) -> java.time.LocalDateTime: ...
    @typing.overload
    def toString(self) -> str: ...
    @typing.overload
    def toString(self, timeScale: TimeScale) -> str: ...
    @typing.overload
    def toString(self, int: int) -> str: ...
    @typing.overload
    def toString(self, int: int, timeScale: TimeScale) -> str: ...

class GMSTScale(TimeScale):
    """
    public class GMSTScale extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeScale`
    
        Greenwich Mean Sidereal Time.
    
        The Greenwich Mean Sidereal Time is the hour angle between the meridian of Greenwich and mean equinox of date at 0h UT1.
    
        This is intended to be accessed thanks to the :class:`~fr.cnes.sirius.patrius.time.TimeScalesFactory` class, so there is
        no public constructor.
    
        Since:
            5.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :meth:`~serialized`
    """
    def getName(self) -> str:
        """
            Get the name time scale.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.getName` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Returns:
                name of the time scale
        
        
        """
        ...
    def offsetFromTAI(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI`
        
        
        """
        ...
    def offsetToTAI(self, dateComponents: DateComponents, timeComponents: TimeComponents) -> float:
        """
            Get the offset to convert locations from instance to :class:`~fr.cnes.sirius.patrius.time.TAIScale`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.DateComponents`): date location in the time scale
                time (:class:`~fr.cnes.sirius.patrius.time.TimeComponents`): time location in the time scale
        
            Returns:
                offset in seconds to add to a location in *instance time scale* to get a location in
                *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI`
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class GPSScale(TimeScale):
    """
    public class GPSScale extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeScale`
    
        GPS time scale.
    
        By convention, TGPS = TAI - 19 s.
    
        This is intended to be accessed thanks to the :class:`~fr.cnes.sirius.patrius.time.TimeScalesFactory` class, so there is
        no public constructor.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :meth:`~serialized`
    """
    def getName(self) -> str:
        """
            Get the name time scale.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.getName` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Returns:
                name of the time scale
        
        
        """
        ...
    def offsetFromTAI(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI`
        
        
        """
        ...
    def offsetToTAI(self, dateComponents: DateComponents, timeComponents: TimeComponents) -> float:
        """
            Get the offset to convert locations from instance to :class:`~fr.cnes.sirius.patrius.time.TAIScale`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.DateComponents`): date location in the time scale
                time (:class:`~fr.cnes.sirius.patrius.time.TimeComponents`): time location in the time scale
        
            Returns:
                offset in seconds to add to a location in *instance time scale* to get a location in
                *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI`
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class GalileoScale(TimeScale):
    """
    public class GalileoScale extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeScale`
    
        Galileo system time scale.
    
        By convention, TGST = UTC + 13s at Galileo epoch (1999-08-22T00:00:00Z).
    
        This is intended to be accessed thanks to the :class:`~fr.cnes.sirius.patrius.time.TimeScalesFactory` class, so there is
        no public constructor.
    
        Galileo System Time and GPS time are very close scales. Without any errors, they should be identical. The offset between
        these two scales is the GGTO, it depends on the clocks used to realize the time scales. It is of the order of a few tens
        nanoseconds. This class does not implement this offset, so it is virtually identical to the
        :class:`~fr.cnes.sirius.patrius.time.GPSScale`.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :meth:`~serialized`
    """
    def getName(self) -> str:
        """
            Get the name time scale.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.getName` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Returns:
                name of the time scale
        
        
        """
        ...
    def offsetFromTAI(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI`
        
        
        """
        ...
    def offsetToTAI(self, dateComponents: DateComponents, timeComponents: TimeComponents) -> float:
        """
            Get the offset to convert locations from instance to :class:`~fr.cnes.sirius.patrius.time.TAIScale`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.DateComponents`): date location in the time scale
                time (:class:`~fr.cnes.sirius.patrius.time.TimeComponents`): time location in the time scale
        
            Returns:
                offset in seconds to add to a location in *instance time scale* to get a location in
                *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI`
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class TAIScale(TimeScale):
    """
    public class TAIScale extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeScale`
    
        International Atomic Time.
    
        This is intended to be accessed thanks to the :class:`~fr.cnes.sirius.patrius.time.TimeScalesFactory` class, so there is
        no public constructor.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :meth:`~serialized`
    """
    def getName(self) -> str:
        """
            Get the name time scale.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.getName` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Returns:
                name of the time scale
        
        
        """
        ...
    def offsetFromTAI(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                taiTime (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI`
        
        
        """
        ...
    def offsetToTAI(self, dateComponents: DateComponents, timeComponents: TimeComponents) -> float:
        """
            Get the offset to convert locations from instance to :class:`~fr.cnes.sirius.patrius.time.TAIScale`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.DateComponents`): date location in the time scale
                time (:class:`~fr.cnes.sirius.patrius.time.TimeComponents`): time location in the time scale
        
            Returns:
                offset in seconds to add to a location in *instance time scale* to get a location in
                *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI`
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class TCBScale(TimeScale):
    """
    public class TCBScale extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeScale`
    
        Barycentric Coordinate Time.
    
        Coordinate time at the center of mass of the Solar System. This time scale depends linearly from
        :class:`~fr.cnes.sirius.patrius.time.TDBScale`.
    
        This is intended to be accessed thanks to the :class:`~fr.cnes.sirius.patrius.time.TimeScalesFactory` class, so there is
        no public constructor.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :meth:`~serialized`
    """
    def getName(self) -> str:
        """
            Get the name time scale.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.getName` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Returns:
                name of the time scale
        
        
        """
        ...
    def offsetFromTAI(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI`
        
        
        """
        ...
    def offsetToTAI(self, dateComponents: DateComponents, timeComponents: TimeComponents) -> float:
        """
            Get the offset to convert locations from instance to :class:`~fr.cnes.sirius.patrius.time.TAIScale`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.DateComponents`): date location in the time scale
                time (:class:`~fr.cnes.sirius.patrius.time.TimeComponents`): time location in the time scale
        
            Returns:
                offset in seconds to add to a location in *instance time scale* to get a location in
                *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI`
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class TCGScale(TimeScale):
    """
    public class TCGScale extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeScale`
    
        Geocentric Coordinate Time.
    
        Coordinate time at the center of mass of the Earth. This time scale depends linearly from
        :class:`~fr.cnes.sirius.patrius.time.TTScale`.
    
        This is intended to be accessed thanks to the :class:`~fr.cnes.sirius.patrius.time.TimeScalesFactory` class, so there is
        no public constructor.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :meth:`~serialized`
    """
    def getName(self) -> str:
        """
            Get the name time scale.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.getName` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Returns:
                name of the time scale
        
        
        """
        ...
    def offsetFromTAI(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI`
        
        
        """
        ...
    def offsetToTAI(self, dateComponents: DateComponents, timeComponents: TimeComponents) -> float:
        """
            Get the offset to convert locations from instance to :class:`~fr.cnes.sirius.patrius.time.TAIScale`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.DateComponents`): date location in the time scale
                time (:class:`~fr.cnes.sirius.patrius.time.TimeComponents`): time location in the time scale
        
            Returns:
                offset in seconds to add to a location in *instance time scale* to get a location in
                *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI`
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class TDBDefaultModel(TDBModel):
    """
    public class TDBDefaultModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TDBModel`
    
        Barycentric Dynamic Time default model.
    
        TDB = TT + 0.001658 sin(g) + 0.000014 sin(2g)seconds where g = 357.53 + 0.9856003 (JD - 2451545) degrees.
    
        Since:
            4.7
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.TDBModel`
    """
    def __init__(self): ...
    def offsetFromTAI(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to
            :class:`~fr.cnes.sirius.patrius.time.TDBScale`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TDBModel.offsetFromTAI` in interface :class:`~fr.cnes.sirius.patrius.time.TDBModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
        
        """
        ...

class TDBScale(TimeScale):
    """
    public class TDBScale extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeScale`
    
        Barycentric Dynamic Time.
    
        Time used to take account of time dilation when calculating orbits of planets, asteroids, comets and interplanetary
        spacecraft in the Solar system. It was based on a Dynamical time scale but was not well defined and not rigorously
        correct as a relativistic time scale. It was subsequently deprecated in favour of Barycentric Coordinate Time (TCB), but
        at the 2006 General Assembly of the International Astronomical Union TDB was rehabilitated by making it a specific fixed
        linear transformation of TCB.
    
        By convention, TDB = TT + 0.001658 sin(g) + 0.000014 sin(2g)seconds where g = 357.53 + 0.9856003 (JD - 2451545) degrees.
    
        Also see:
            :meth:`~serialized`
    """
    def getName(self) -> str:
        """
            Get the name time scale.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.getName` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Returns:
                name of the time scale
        
        
        """
        ...
    def offsetFromTAI(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI`
        
        
        """
        ...
    def offsetToTAI(self, dateComponents: DateComponents, timeComponents: TimeComponents) -> float:
        """
            Get the offset to convert locations from instance to :class:`~fr.cnes.sirius.patrius.time.TAIScale`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.DateComponents`): date location in the time scale
                time (:class:`~fr.cnes.sirius.patrius.time.TimeComponents`): time location in the time scale
        
            Returns:
                offset in seconds to add to a location in *instance time scale* to get a location in
                *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI`
        
        
        """
        ...
    @staticmethod
    def setModel(tDBModel: typing.Union[TDBModel, typing.Callable]) -> None:
        """
            Set the TDB model.
        
            Parameters:
                modelIn (:class:`~fr.cnes.sirius.patrius.time.TDBModel`): the TDB model to set
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class TTScale(TimeScale):
    """
    public class TTScale extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeScale`
    
        Terrestrial Time as defined by IAU(1991) recommendation IV.
    
        Coordinate time at the surface of the Earth. IT is the successor of Ephemeris Time TE.
    
        By convention, TT = TAI + 32.184 s.
    
        This is intended to be accessed thanks to the :class:`~fr.cnes.sirius.patrius.time.TimeScalesFactory` class, so there is
        no public constructor.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :meth:`~serialized`
    """
    def getName(self) -> str:
        """
            Get the name time scale.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.getName` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Returns:
                name of the time scale
        
        
        """
        ...
    def offsetFromTAI(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI`
        
        
        """
        ...
    def offsetToTAI(self, dateComponents: DateComponents, timeComponents: TimeComponents) -> float:
        """
            Get the offset to convert locations from instance to :class:`~fr.cnes.sirius.patrius.time.TAIScale`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.DateComponents`): date location in the time scale
                time (:class:`~fr.cnes.sirius.patrius.time.TimeComponents`): time location in the time scale
        
            Returns:
                offset in seconds to add to a location in *instance time scale* to get a location in
                *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI`
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class UT1Scale(TimeScale):
    """
    public class UT1Scale extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeScale`
    
        Universal Time 1.
    
        UT1 is a time scale directly linked to the actual rotation of the Earth. It is an irregular scale, reflecting Earth
        irregular rotation rate. The offset between UT1 and :class:`~fr.cnes.sirius.patrius.time.UTCScale` is found in the Earth
        Orientation Parameters published by IERS.
    
        Since:
            5.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :meth:`~serialized`
    """
    def getHistory(self) -> fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory:
        """
            Package-private getter for the EOPHistory object.
        
            Returns:
                current history object.
        
        
        """
        ...
    def getName(self) -> str:
        """
            Get the name time scale.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.getName` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Returns:
                name of the time scale
        
        
        """
        ...
    def offsetFromTAI(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI`
        
        
        """
        ...
    def offsetToTAI(self, dateComponents: DateComponents, timeComponents: TimeComponents) -> float:
        """
            Get the offset to convert locations from instance to :class:`~fr.cnes.sirius.patrius.time.TAIScale`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.DateComponents`): date location in the time scale
                time (:class:`~fr.cnes.sirius.patrius.time.TimeComponents`): time location in the time scale
        
            Returns:
                offset in seconds to add to a location in *instance time scale* to get a location in
                *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI`
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class UTCScale(TimeScale):
    """
    public class UTCScale extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeScale`
    
        Coordinated Universal Time.
    
        UTC is related to TAI using step adjustments from time to time according to IERS (International Earth Rotation Service)
        rules. Before 1972, these adjustments were piecewise linear offsets. Since 1972, these adjustments are piecewise
        constant offsets, which require introduction of leap seconds.
    
        Leap seconds are always inserted as additional seconds at the last minute of the day, pushing the next day forward. Such
        minutes are therefore more than 60 seconds long. In theory, there may be seconds removal instead of seconds insertion,
        but up to now (2010) it has never been used. As an example, when a one second leap was introduced at the end of 2005,
        the UTC time sequence was 2005-12-31T23:59:59 UTC, followed by 2005-12-31T23:59:60 UTC, followed by 2006-01-01T00:00:00
        UTC.
    
        The OREKIT library retrieves the post-1972 constant time steps data thanks to the
        :class:`~fr.cnes.sirius.patrius.data.DataProvidersManager` class. The linear models used between 1961 and 1972 are
        built-in in the class itself.
    
        This is intended to be accessed thanks to the :class:`~fr.cnes.sirius.patrius.time.TimeScalesFactory` class, so there is
        no public constructor. Every call to :meth:`~fr.cnes.sirius.patrius.time.TimeScalesFactory.getUTC` will create a new
        :class:`~fr.cnes.sirius.patrius.time.UTCScale` instance, sharing the UTC-TAI offset table between all instances.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, :meth:`~serialized`
    """
    def getFirstKnownLeapSecond(self) -> AbsoluteDate:
        """
            Get the date of the first known leap second.
        
            Returns:
                date of the first known leap second
        
        
        """
        ...
    def getLastKnownLeapSecond(self) -> AbsoluteDate:
        """
            Get the date of the last known leap second.
        
            Returns:
                date of the last known leap second
        
        
        """
        ...
    def getLeap(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the value of the previous leap.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date to check
        
            Returns:
                value of the previous leap
        
        
        """
        ...
    def getName(self) -> str:
        """
            Get the name time scale.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.getName` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Returns:
                name of the time scale
        
        
        """
        ...
    def insideLeap(self, absoluteDate: AbsoluteDate) -> bool:
        """
            Check if date is within a leap second introduction.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date to check
        
            Returns:
                true if time is within a leap second introduction
        
        
        """
        ...
    def offsetFromTAI(self, absoluteDate: AbsoluteDate) -> float:
        """
            Get the offset to convert locations from :class:`~fr.cnes.sirius.patrius.time.TAIScale` to instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI` in
                interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): conversion date
        
            Returns:
                offset in seconds to add to a location in *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale* to get a location
                in *instance time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI`
        
        
        """
        ...
    def offsetToTAI(self, dateComponents: DateComponents, timeComponents: TimeComponents) -> float:
        """
            Get the offset to convert locations from instance to :class:`~fr.cnes.sirius.patrius.time.TAIScale`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetToTAI` in interface :class:`~fr.cnes.sirius.patrius.time.TimeScale`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.DateComponents`): date location in the time scale
                time (:class:`~fr.cnes.sirius.patrius.time.TimeComponents`): time location in the time scale
        
            Returns:
                offset in seconds to add to a location in *instance time scale* to get a location in
                *:class:`~fr.cnes.sirius.patrius.time.TAIScale` time scale*
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.time.TimeScale.offsetFromTAI`
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class UTCTAIHistoryFilesLoader(UTCTAILoader):
    """
    public class UTCTAIHistoryFilesLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.UTCTAILoader`
    
        Loader for UTC versus TAI history files.
    
        UTC versus TAI history files contain :code:`leap seconds` data since.
    
        The UTC versus TAI history files are recognized thanks to their base names, which must match the pattern
        :code:`UTC-TAI.history` (or :code:`UTC-TAI.history.gz` for gzip-compressed files)
    
        Only one history file must be present in the IERS directories hierarchy.
    """
    def __init__(self): ...
    def getSupportedNames(self) -> str:
        """
            Get the regular expression for supported files names.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.UTCTAILoader.getSupportedNames` in
                interface :class:`~fr.cnes.sirius.patrius.time.UTCTAILoader`
        
            Returns:
                regular expression for supported files names
        
        
        """
        ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...
    def loadTimeSteps(self) -> java.util.SortedMap[DateComponents, int]: ...
    def stillAcceptsData(self) -> bool:
        """
            Check if the loader still accepts new data.
        
            This method is used to speed up data loading by interrupting crawling the data sets as soon as a loader has found the
            data it was waiting for. For loaders that can merge data from any number of sources (for example JPL ephemerides or
            Earth Orientation Parameters that are split among several files), this method should always return true to make sure no
            data is left over.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.data.DataLoader.stillAcceptsData` in
                interface :class:`~fr.cnes.sirius.patrius.data.DataLoader`
        
            Returns:
                true while the loader still accepts new data
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.time")``.

    AbsoluteDate: typing.Type[AbsoluteDate]
    AbsoluteDateInterval: typing.Type[AbsoluteDateInterval]
    AbsoluteDateIntervalsList: typing.Type[AbsoluteDateIntervalsList]
    ChronologicalComparator: typing.Type[ChronologicalComparator]
    DateComponents: typing.Type[DateComponents]
    DateTimeComponents: typing.Type[DateTimeComponents]
    GMSTScale: typing.Type[GMSTScale]
    GPSScale: typing.Type[GPSScale]
    GalileoScale: typing.Type[GalileoScale]
    IntervalMapSearcher: typing.Type[IntervalMapSearcher]
    LocalTimeAngle: typing.Type[LocalTimeAngle]
    Month: typing.Type[Month]
    TAIScale: typing.Type[TAIScale]
    TCBScale: typing.Type[TCBScale]
    TCGScale: typing.Type[TCGScale]
    TDBDefaultModel: typing.Type[TDBDefaultModel]
    TDBModel: typing.Type[TDBModel]
    TDBScale: typing.Type[TDBScale]
    TTScale: typing.Type[TTScale]
    TimeComponents: typing.Type[TimeComponents]
    TimeInterpolable: typing.Type[TimeInterpolable]
    TimeScale: typing.Type[TimeScale]
    TimeScalesFactory: typing.Type[TimeScalesFactory]
    TimeShiftable: typing.Type[TimeShiftable]
    TimeStamped: typing.Type[TimeStamped]
    TimeStampedCache: typing.Type[TimeStampedCache]
    TimeStampedGenerator: typing.Type[TimeStampedGenerator]
    UT1Scale: typing.Type[UT1Scale]
    UTCScale: typing.Type[UTCScale]
    UTCTAIHistoryFilesLoader: typing.Type[UTCTAIHistoryFilesLoader]
    UTCTAILoader: typing.Type[UTCTAILoader]
    interpolation: fr.cnes.sirius.patrius.time.interpolation.__module_protocol__
