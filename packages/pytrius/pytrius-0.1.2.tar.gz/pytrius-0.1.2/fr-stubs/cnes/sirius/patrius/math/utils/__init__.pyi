
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import jpype
import typing



class ISearchIndex(java.io.Serializable):
    def getConvention(self) -> 'ISearchIndex.SearchIndexIntervalConvention': ...
    @typing.overload
    def getIndex(self, double: float) -> int: ...
    @typing.overload
    def getIndex(self, double: float, int: int, int2: int) -> int: ...
    def getTab(self) -> typing.MutableSequence[float]: ...
    class SearchIndexIntervalConvention(java.lang.Enum['ISearchIndex.SearchIndexIntervalConvention']):
        CLOSED_OPEN: typing.ClassVar['ISearchIndex.SearchIndexIntervalConvention'] = ...
        OPEN_CLOSED: typing.ClassVar['ISearchIndex.SearchIndexIntervalConvention'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'ISearchIndex.SearchIndexIntervalConvention': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['ISearchIndex.SearchIndexIntervalConvention']: ...

class SearchIndexLibrary:
    @staticmethod
    def binarySearchClosedOpen(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, int: int, int2: int) -> int: ...
    @staticmethod
    def binarySearchOpenClosed(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, int: int, int2: int) -> int: ...
    @staticmethod
    def midPoint(int: int, int2: int) -> int: ...

class AbstractSearchIndex(ISearchIndex):
    """
    public abstract class AbstractSearchIndex extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.utils.ISearchIndex`
    
    
        Abstract class for index search algorithm with a coupled dichotomy-BinarySearch algorithms.
    
        **IMPORTANT**: the tab passed in the constructor has to be sorted by increasing order. Duplicates are allowed. If this
        tab is not sorting, no exception will be thrown, but the results can be totally wrong.
        Each implementation of this class defines a convention of SearchIndexIntervalConvention.
    
        Since:
            2.3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], searchIndexIntervalConvention: ISearchIndex.SearchIndexIntervalConvention): ...
    def getConvention(self) -> ISearchIndex.SearchIndexIntervalConvention:
        """
            Returns the convention that can be applied to the interval during the search index algorithm. Describes the boundaries
            of each interval defined by tab.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.utils.ISearchIndex.getConvention` in
                interface :class:`~fr.cnes.sirius.patrius.math.utils.ISearchIndex`
        
            Returns:
                CLOSED_OPEN if intervals are [tab[i], tab[i+1][ or OPEN_CLOSED for ]tab[i], tab[i+1]].
        
        
        """
        ...
    def getTab(self) -> typing.MutableSequence[float]:
        """
            Returns the array of values.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.utils.ISearchIndex.getTab` in
                interface :class:`~fr.cnes.sirius.patrius.math.utils.ISearchIndex`
        
            Returns:
                tab
        
        
        """
        ...

class BinarySearchIndexClosedOpen(AbstractSearchIndex):
    """
    public class BinarySearchIndexClosedOpen extends :class:`~fr.cnes.sirius.patrius.math.utils.AbstractSearchIndex`
    
    
        Searches index in a double[] with a coupled dichotomy-BinarySearch algorithms.
    
        **IMPORTANT**: the tab passed in the constructor has to be sorted by increasing order. Duplicates are allowed. If this
        tab is not sorting, no exception will be thrown, but the results can be totally wrong.
        The interval convention is set to
        :meth:`~fr.cnes.sirius.patrius.math.utils.ISearchIndex.SearchIndexIntervalConvention.CLOSED_OPEN`.
    
        Since:
            2.3.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def getIndex(self, double: float) -> int:
        """
            Returns the index of x in a tab with a dichotomy / BinarySearch algorithm under the convention
            :meth:`~fr.cnes.sirius.patrius.math.utils.ISearchIndex.SearchIndexIntervalConvention.CLOSED_OPEN`.
        
            Parameters:
                x (double): : the value to search.
        
            Returns:
                index of value that belongs to [0, numberOfPoints-1] that fits the above conditions.
        
            Returns the index of x in a tab with a dichotomy / BinarySearch algorithm under the convention
            :meth:`~fr.cnes.sirius.patrius.math.utils.ISearchIndex.SearchIndexIntervalConvention.CLOSED_OPEN`.
        
            Parameters:
                x (double): : the value to search.
                iMin2 (int): : defines the lower index bound of the tab for the search.
                iMax2 (int): : defines the upper index bound of the tab for the search.
        
            Returns:
                index of value that belongs to [iMin2, iMax2] that fits the above conditions.
        
        
        """
        ...
    @typing.overload
    def getIndex(self, double: float, int: int, int2: int) -> int: ...

class BinarySearchIndexOpenClosed(AbstractSearchIndex):
    """
    public class BinarySearchIndexOpenClosed extends :class:`~fr.cnes.sirius.patrius.math.utils.AbstractSearchIndex`
    
    
        Searches index in a double[] with a coupled dichotomy-BinarySearch algorithms.
    
        **IMPORTANT**: the tab passed in the constructor has to be sorted by increasing order. Duplicates are allowed. If this
        tab is not sorted, no exception will be thrown, but the results can be totally wrong.
        The interval convention is set to
        :meth:`~fr.cnes.sirius.patrius.math.utils.ISearchIndex.SearchIndexIntervalConvention.OPEN_CLOSED`.
    
        Since:
            2.3.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def getIndex(self, double: float) -> int:
        """
            Returns the index of x in a tab with a dichotomy / BinarySearch algorithm under the convention
            :meth:`~fr.cnes.sirius.patrius.math.utils.ISearchIndex.SearchIndexIntervalConvention.OPEN_CLOSED`.
        
            Parameters:
                x (double): : the value to search.
        
            Returns:
                index of value that belongs to [0, numberOfPoints-1] that fits the above conditions.
        
            Returns the index of x in a tab with a dichotomy / BinarySearch algorithm under the convention
            :meth:`~fr.cnes.sirius.patrius.math.utils.ISearchIndex.SearchIndexIntervalConvention.OPEN_CLOSED`.
        
            Parameters:
                x (double): : the value to search.
                iMin2 (int): : defines the lower index bound of the tab for the search.
                iMax2 (int): : defines the upper index bound of the tab for the search.
        
            Returns:
                index of value that belongs to [iMin2, iMax2] that fits the above conditions.
        
        
        """
        ...
    @typing.overload
    def getIndex(self, double: float, int: int, int2: int) -> int: ...

class RecordSegmentSearchIndex(AbstractSearchIndex):
    def __init__(self, iSearchIndex: ISearchIndex): ...
    @typing.overload
    def getIndex(self, double: float) -> int: ...
    @typing.overload
    def getIndex(self, double: float, int: int, int2: int) -> int: ...
    def getIndexClosedOpen(self, double: float) -> int: ...
    def getIndexOpenClosed(self, double: float) -> int: ...
    def updateStencil(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.utils")``.

    AbstractSearchIndex: typing.Type[AbstractSearchIndex]
    BinarySearchIndexClosedOpen: typing.Type[BinarySearchIndexClosedOpen]
    BinarySearchIndexOpenClosed: typing.Type[BinarySearchIndexOpenClosed]
    ISearchIndex: typing.Type[ISearchIndex]
    RecordSegmentSearchIndex: typing.Type[RecordSegmentSearchIndex]
    SearchIndexLibrary: typing.Type[SearchIndexLibrary]
