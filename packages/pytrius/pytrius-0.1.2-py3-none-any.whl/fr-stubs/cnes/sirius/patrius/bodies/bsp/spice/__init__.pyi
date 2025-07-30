
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.linear
import java.io
import java.lang
import java.util
import jpype
import jpype.protocol
import typing



class CommentSectionDAF:
    """
    public final class CommentSectionDAF extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class dedicated to the reading of the comment section of binary DAF files. A binary DAF contains an area which is
        reserved for storing annotations or descriptive textual information describing the data contained in a file. This area
        is referred to as the ''comment area'' of the file. The comment area of a DAF is a line oriented medium for storing
        textual information. The comment area preserves any leading or embedded white space in the line(s) of text which are
        stored, so that the appearance of the of information will be unchanged when it is retrieved (extracted) at some other
        time. The class is inspired by the dafec.for file from the SPICE library.
    
        Since:
            4.11
    """
    @staticmethod
    def readComments(int: int, int2: int, int3: int, intArray: typing.Union[typing.List[int], jpype.JArray], stringArray: typing.Union[typing.List[str], jpype.JArray], booleanArray: typing.Union[typing.List[bool], jpype.JArray]) -> None: ...

class CounterArray:
    """
    public class CounterArray extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class class defines the object CounterArray and all the methods to manipulate it. These methods where originally
        defined in ZZCTR.for
    
        A counter array consists of SpiceCommon.ctrsiz elements representing cascading counters. The fastest counter is at index
        0, the slowest counter is at index CTRSIZ. At the start of counting all counter array elements are set to INTMIN. In the
        process of counting the fastest element is incremented by one. As with any cascading counters when the fastest counter
        reaches INTMAX it rolls back to INTMIN and the next counter is incremented by 1. When all counters reach INTMAX,
        Increment signals an error.
    
        Since:
            4.11
    """
    def __init__(self, string: str): ...
    def checkAndUpdate(self, counterArray: 'CounterArray') -> bool:
        """
            Check and update, if needed, counter array.
        
            Parameters:
                newCounter (:class:`~fr.cnes.sirius.patrius.bodies.bsp.spice.CounterArray`): to compare with the current counter
        
            Returns:
                true if there has been an update
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def increment(self) -> None: ...

class DafHandle:
    """
    public final class DafHandle extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class is and adaptation of one part of the dafah.for file of the SPICE library.
    
        This class has as objective to manage DAF files by their handle. This includes opening, closing and retrieving
        information about the summary.
    
        Several files may be opened for use simultaneously. (This makes it convenient to combine data from several files to
        produce a single result.) As each DAF is opened, it is assigned a file handle, which is used to keep track of the file
        internally, and which is used by the calling program to refer to the file in all subsequent calls to DAF methods.
    
        Currently DAF files can only be opened for read purposes. Writing in a DAF or creating a DAF file is not implemented.
    
        Since:
            4.11
    """
    @staticmethod
    def checkHandleAccess(int: int, string: str) -> None: ...
    @staticmethod
    def closeDAF(int: int) -> None: ...
    @staticmethod
    def getHandleList() -> java.util.List[int]: ...
    @staticmethod
    def getSummaryFormatDAF(int: int) -> typing.MutableSequence[int]: ...
    @staticmethod
    def handleToFilenameDAF(int: int) -> str: ...
    @staticmethod
    def isLoaded(string: str, intArray: typing.Union[typing.List[int], jpype.JArray]) -> bool: ...
    @staticmethod
    def openReadDAF(string: str) -> int: ...

class DafHandleManager:
    """
    public final class DafHandleManager extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class is intended to provide low-level services for the creation, updating, and reading of direct access files
        utilized by the DAF and DAS systems within SPICE.
    
    
        This class based on the zzddhman.for file in the SPICE library.
    
        Since:
            4.11
    """
    @staticmethod
    def closeFile(int: int, string: str) -> None: ...
    @staticmethod
    def getArchitectureFromHandle(int: int) -> str:
        """
            Indicate the architecture of the file associated to handle.
        
        
            Inspired by ZZDDHNFO routine in the SPICE library.
        
            Parameters:
                handle (int): File handle assigned to file of interest
        
            Returns:
                file's architecture
        
        
        """
        ...
    @staticmethod
    def getBinaryFileFormatFromHandle(int: int) -> str:
        """
            Indicate the binary file format of the file associated to handle.
        
        
            Inspired by ZZDDHNFO routine in the SPICE library.
        
            Parameters:
                handle (int): File handle assigned to file of interest
        
            Returns:
                file's binary file format
        
        
        """
        ...
    @staticmethod
    def getFile(int: int) -> java.io.File:
        """
            Return the File object associated with a handle.
        
        
            Inspired by ZZDDHHLU routine from the SPICE library.
        
            Parameters:
                handle (int): Handle associated with the file of interest
        
            Returns:
                the corresponding File object
        
        
        """
        ...
    @staticmethod
    def getFilename(int: int) -> str:
        """
            Indicate the file name associated to a handle.
        
        
            Inspired by ZZDDHNFO routine in the SPICE library.
        
            Parameters:
                handle (int): File handle assigned to file of interest
        
            Returns:
                name of the file associated with HANDLE
        
        
        """
        ...
    @staticmethod
    def getFound(int: int) -> bool:
        """
            Indicate if the handle is found in the list.
        
        
            Inspired by ZZDDHNFO routine in the SPICE library.
        
            Parameters:
                handle (int): File handle assigned to file of interest
        
            Returns:
                boolean that indicates if handle was found
        
        
        """
        ...
    @staticmethod
    def getHandle(string: str) -> int: ...
    @staticmethod
    def openFile(string: str, string2: str, string3: str) -> int: ...

class DafReader:
    """
    public final class DafReader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class containing high level methods for the reading of several parts of a DAF binary file.
    
        Based on several routines of the SPICE library.
    
        Since:
            4.11
    """
    @staticmethod
    def readComments(int: int, int2: int, int3: int, intArray: typing.Union[typing.List[int], jpype.JArray], stringArray: typing.Union[typing.List[str], jpype.JArray], booleanArray: typing.Union[typing.List[bool], jpype.JArray]) -> None: ...
    @staticmethod
    def readDataDaf(int: int, int2: int, int3: int) -> typing.MutableSequence[float]: ...
    @staticmethod
    def readFileRecord(int: int, intArray: typing.Union[typing.List[int], jpype.JArray], intArray2: typing.Union[typing.List[int], jpype.JArray], stringArray: typing.Union[typing.List[str], jpype.JArray], intArray3: typing.Union[typing.List[int], jpype.JArray], intArray4: typing.Union[typing.List[int], jpype.JArray], intArray5: typing.Union[typing.List[int], jpype.JArray]) -> None: ...

class DafReaderTools:
    """
    public final class DafReaderTools extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class includes auxiliary methods for the DAF files reading.
    
        Since:
            4.11
    """
    @staticmethod
    def address2RecordWord(int: int, intArray: typing.Union[typing.List[int], jpype.JArray], intArray2: typing.Union[typing.List[int], jpype.JArray]) -> None:
        """
            Transform an address into a record number and a word inside the record.
        
        
            There are 128 words in each record, being each 8 bytes (a double precision).
        
            Parameters:
                address (int): byte address we want to transform
                record (int[]): (output) file record where the address points
                word (int[]): (output) word inside the record where the address points
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the address isn't valid
        
        
        """
        ...
    @staticmethod
    def nRecord2nByte(int: int) -> int:
        """
            Transform a record number into the byte address of its beginning.
        
            Parameters:
                nRecord (int): File record we want to access
        
            Returns:
                file byte where the record starts
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the nRecord isn't valid
        
        
        """
        ...
    @staticmethod
    def readString(randomAccessFile: java.io.RandomAccessFile, int: int) -> str: ...

class DafState:
    """
    public class DafState extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Define a DAF binary file state indicating where in the file we are and containing the last summary record read.
    
        Since:
            4.11
    """
    def __init__(self): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getHandle(self) -> int:
        """
            Getter for the state handle.
        
            Returns:
                the handle of the DAF
        
        
        """
        ...
    def getIndexCurrSummary(self) -> int:
        """
            Getter for the index of the current summary within the summary record.
        
            Returns:
                index of the current summary within the summary record
        
        
        """
        ...
    def getLastNameRecord(self) -> str:
        """
            Getter for the name of the last name record read.
        
            Returns:
                name of the last name record read
        
        
        """
        ...
    def getLastSummaryRecord(self) -> typing.MutableSequence[float]:
        """
            Getter for the contents of the last summary record.
        
            Returns:
                a double array containing the content of the last summary record
        
        
        """
        ...
    def getRecnoCurrSummary(self) -> int:
        """
            Getter for the record containing the current summary record.
        
            Returns:
                current summary record
        
        
        """
        ...
    def getRecnoNextSummary(self) -> int:
        """
            Getter for the record containing the next summary record.
        
            Returns:
                next summary record
        
        
        """
        ...
    def getRecnoPrevSummary(self) -> int:
        """
            Getter for the record containing the previous summary record.
        
            Returns:
                previous summary record
        
        
        """
        ...
    def getnSummariesCurrSummaryRecord(self) -> int:
        """
            Getter for the number of summaries in the current summary record.
        
            Returns:
                number of summaries in the current summary record
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def isBuffered(self) -> bool:
        """
            Getter for whether name record containing name of current array is buffered.
        
            Returns:
                boolean indicating if the name record is buffered
        
        
        """
        ...
    def setBuffered(self, boolean: bool) -> None:
        """
            Set whether name record containing name of current array is buffered.
        
            Parameters:
                isBuf (boolean): if name record containing name of current array is buffered
        
        
        """
        ...
    def setHandle(self, int: int) -> None:
        """
            Setter for the state handle.
        
            Parameters:
                handle (int): handle of the DAF
        
        
        """
        ...
    def setIndexCurrSummary(self, int: int) -> None:
        """
            Setter for the index of the current summary within the summary record.
        
            Parameters:
                indexCurrSummary (int): index of the current summary in the summary record
        
        
        """
        ...
    def setLastNameRecord(self, string: str) -> None:
        """
            Setter for the name of the last name record read.
        
            Parameters:
                lastNameRecord (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): last name record read
        
        
        """
        ...
    def setLastSummaryRecord(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Store the content of the last summary record into the state.
        
            Parameters:
                lastSummaryRecord (double[]): double array containing the last summary record content
        
        
        """
        ...
    def setRecnoCurrSummary(self, int: int) -> None:
        """
            Set the current summary record of the DAF.
        
            Parameters:
                recnoCurrSummary (int): current summary record
        
        
        """
        ...

class FileRecordDAF:
    """
    public final class FileRecordDAF extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class is used to store the file record of a DAF in a object. It is based on the SPICE library.
    
        Since:
            4.11
    """
    def __init__(self, int: int): ...
    def getBackward(self) -> int:
        """
            Getter for the last summary record.
        
            Returns:
                the last summary record
        
        
        """
        ...
    def getForward(self) -> int:
        """
            Getter for the first summary record.
        
            Returns:
                the first summary record
        
        
        """
        ...
    def getFree(self) -> int:
        """
            Getter for the first free address in the file.
        
            Returns:
                the first free address in the file
        
        
        """
        ...
    def getInternalFilename(self) -> str:
        """
            Getter for the internal file name.
        
            Returns:
                the internal file name
        
        
        """
        ...
    def getnDouble(self) -> int:
        """
            Getter for the number of double precision components in summaries.
        
            Returns:
                the number of double precision components in summaries
        
        
        """
        ...
    def getnInt(self) -> int:
        """
            Getter for the number of integer components in a summary.
        
            Returns:
                the number of integer components in a summary
        
        
        """
        ...
    def isFound(self) -> bool:
        """
            Getter for a boolean indicating if a file associated to the handle was found or not.
        
            Returns:
                a boolean indicating if a file associated to the handle was found or not
        
        
        """
        ...

class FindArraysDAF:
    """
    public final class FindArraysDAF extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class for the search of arrays inside a DAF file.
    
    
        The main function of these methods is to allow the contents of any DAF to be examined on an array-by-array basis.
    
        Conceptually, the arrays in a DAF form a doubly linked list, which can be searched in either of two directions: forward
        or backward. It is possible to search multiple DAFs simultaneously.
    
        Based on various routines of the daffa.for file in the SPICE library.
    
        Since:
            4.11
    """
    @staticmethod
    def beginBackwardSearch(int: int) -> None: ...
    @staticmethod
    def beginForwardSearch(int: int) -> None: ...
    @staticmethod
    def findNextArray() -> bool: ...
    @staticmethod
    def findPreviousArray() -> bool: ...
    @staticmethod
    def getNameOfArray() -> str: ...
    @staticmethod
    def getSummaryOfArray() -> typing.MutableSequence[float]: ...
    @staticmethod
    def readCharacterRecordDaf(int: int, int2: int) -> str: ...
    @staticmethod
    def selectDaf(int: int) -> None: ...

class KernelPool:
    """
    public class KernelPool extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class class reproduces the data structure created in pool.for for holding kernel pool variables.
    
    
        This is and adaptation of the structure formed by NMPOOL,PNAME,DATLST,DPPOOL,DPVALS,CHPOOL,CHVALS.
    
        Since:
            4.11
    """
    def __init__(self, string: str, string2: str): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class PoolSpice:
    """
    public final class PoolSpice extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class class reproduces the necessary routines of the pool.for file in original Spice library.
    
        Since:
            4.11
    """
    @staticmethod
    def checkPoolStateCounter(counterArray: CounterArray) -> bool:
        """
            Check and update the POOL state counter tracked by a caller (user) routine.
        
            Translation of ZZPCTRCK from the Spice library
        
            Parameters:
                c (:class:`~fr.cnes.sirius.patrius.bodies.bsp.spice.CounterArray`): State counter to check
        
            Returns:
                flag indicating if input counter was updated
        
        
        """
        ...
    @staticmethod
    def checkUpdates(string: str) -> bool:
        """
            Indicate whether or not any watched kernel variables that have a specified agent on their notification list have been
            updated.
        
            Inspired by CVPOOL of the SPICE library.
        
            Parameters:
                agent (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): Name of the agent to check for notices
        
            Returns:
                :code:`true` if variables for AGENT have been updated
        
        
        """
        ...
    @staticmethod
    def checkUpdatesIfCounterUpdate(counterArray: CounterArray, string: str) -> bool:
        """
            Determine whether or not any of the POOL variables that are to be watched and have AGENT on their distribution list have
            been updated, but do the full watcher check only if the POOL state counter has changed.
        
            Translation of ZZCVPOOL from the Spice Library
        
            Parameters:
                c (:class:`~fr.cnes.sirius.patrius.bodies.bsp.spice.CounterArray`): POOL state counter tracked by the caller
                agent (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of the agent (routine) that need acess to the kernel pool
        
            Returns:
                logical flag that will be set to true if the variables in the kernel pool that are required by AGENT have been updated
                since the last call to CVPOOL
        
        
        """
        ...
    @staticmethod
    def clpool() -> None: ...
    @staticmethod
    def getIntVals(string: str) -> java.util.List[int]: ...
    @staticmethod
    def getStrVals(string: str) -> java.util.List[str]: ...
    @staticmethod
    def init() -> None:
        """
            This routine initializes the data structures needed for maintaining the kernel pool.
        
        """
        ...
    @staticmethod
    def setWatch(string: str, int: int, stringArray: typing.Union[typing.List[str], jpype.JArray]) -> None: ...

class ReadDoublePrecisionDAF:
    """
    public final class ReadDoublePrecisionDAF extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class for reading double precision records from DAFs readContentDPRecord, getContentSummaryRecord are the only approved
        means for reading double precision records to and from DAFs.
    
    
        They keep track of which records have been read most recently, and of which records have been requested most often, in
        order to minimize the amount of time spent actually reading from external storage.
    
        This class is based on the dafwrd.for file of the SPICE library
    
        Since:
            4.11
    """
    READ_ACCESS: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` READ_ACCESS
    
        Reading access identifier.
    
        Also see:
            :meth:`~constant`
    
    
    """
    BYTES_DOUBLE: typing.ClassVar[int] = ...
    """
    public static final int BYTES_DOUBLE
    
        Number of bytes that represent a double precision number.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @staticmethod
    def getContentSummaryRecord(int: int, int2: int, int3: int, int4: int, booleanArray: typing.Union[typing.List[bool], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @staticmethod
    def readContentDPRecord(int: int, int2: int, int3: int, int4: int, booleanArray: typing.Union[typing.List[bool], jpype.JArray]) -> typing.MutableSequence[float]: ...

class SpiceBody:
    """
    public final class SpiceBody extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class allows the translation of SPICE body identifiers to the body names and vice-versa. It will look first in the
        built-in database, and then in the kernel manager if it has read bodies information.
    
        This class is based on the bodc2n, bodc2s and zzbodtrn files of the SPICE library.
    
        Since:
            4.11
    """
    @staticmethod
    def addSpiceBodyMapping(map: typing.Union[java.util.Map[int, str], typing.Mapping[int, str]]) -> None: ...
    @staticmethod
    def bodyCode2Name(int: int) -> str: ...
    @staticmethod
    def bodyCode2String(int: int) -> str: ...
    @staticmethod
    def bodyName2Code(string: str, booleanArray: typing.Union[typing.List[bool], jpype.JArray]) -> int: ...
    @staticmethod
    def bodyString2Code(string: str, booleanArray: typing.Union[typing.List[bool], jpype.JArray]) -> int: ...
    @staticmethod
    def bodyString2CodeBypass(counterArray: CounterArray, stringArray: typing.Union[typing.List[str], jpype.JArray], intArray: typing.Union[typing.List[int], jpype.JArray], booleanArray: typing.Union[typing.List[bool], jpype.JArray], string2: str, booleanArray2: typing.Union[typing.List[bool], jpype.JArray]) -> int: ...
    @staticmethod
    def clearSpiceBodyMapping() -> None:
        """
            Clear the SPICE body mapping.
        
        """
        ...
    @staticmethod
    def getBodycodenamemapping() -> java.util.Map[int, str]: ...

class SpiceChangeFrame:
    """
    public final class SpiceChangeFrame extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class is made to support changes among a standard set of inertial coordinate reference frames.
    
        This class is based on the CHGIRF.for file from the SPICE library.
    
        Since:
            4.11
    """
    STATE_LENGTH: typing.ClassVar[int] = ...
    """
    public static final int STATE_LENGTH
    
        Length of an state array.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @staticmethod
    def frameRotationMatrix(int: int, int2: int) -> fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix: ...
    @staticmethod
    def intertialRefFrameNumber(string: str) -> int:
        """
            Return the index of one of the standard inertial reference frames supported by IRFROT.
        
            Based on the IRFNUM routine from the SPICE library
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): Name of standard inertial reference frame
        
            Returns:
                integer containing the index of the frame
        
        
        """
        ...

class SpiceCommon:
    """
    public final class SpiceCommon extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class containing constants and auxiliary methods for the rest of the SPICE related classes.
    
        Since:
            4.11
    """
    CTRSIZ: typing.ClassVar[int] = ...
    """
    public static final int CTRSIZ
    
        Size of counter arrays.
    
        Also see:
            :meth:`~constant`
    
    
    """
    FILE_TABLE_SIZE: typing.ClassVar[int] = ...
    """
    public static final int FILE_TABLE_SIZE
    
        Size of the file tables.
    
        Also see:
            :meth:`~constant`
    
    
    """
    BINARY_FORMAT: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` BINARY_FORMAT
    
        Java binary format.
    
        Also see:
            :meth:`~constant`
    
    
    """
    RECORD_LENGTH: typing.ClassVar[int] = ...
    """
    public static final int RECORD_LENGTH
    
        Number of bytes in a record.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MAX_CHAR_RECORD: typing.ClassVar[int] = ...
    """
    public static final int MAX_CHAR_RECORD
    
        Max number of characters in a record.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UNKNOWN: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` UNKNOWN
    
        String to define an unknown architecture or file type.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EMPTY: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` EMPTY
    
        Empty string for comparisons.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DAF: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DAF
    
        String literal for DAF architecture.
    
        Also see:
            :meth:`~constant`
    
    
    """
    SPK: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` SPK
    
        String literal for SPK file type.
    
        Also see:
            :meth:`~constant`
    
    
    """
    BYTES_DOUBLE: typing.ClassVar[int] = ...
    """
    public static final int BYTES_DOUBLE
    
        Number of bytes in a double precision number.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @staticmethod
    def ftpCheck(string: str) -> bool:
        """
            Check a character string that may contain the FTP validation string for FTP based errors.
        
            Based on the ZZFTPCHK routine from the SPICE library
        
            Parameters:
                ftp (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): String that may contain the FTP validation string
        
            Returns:
                boolean indicating if FTP corruption occurred
        
        
        """
        ...
    @staticmethod
    def idword2architype(string: str) -> typing.MutableSequence[str]: ...
    @staticmethod
    def indexOfNoChar(string: str, char: str) -> int:
        """
            Find the first occurrence in a string of a character NOT being the char on input.
        
            Based on the NCPOS routine in the SPICE library
        
            Parameters:
                s (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): Any character string
                ch (char): a character
        
            Returns:
                the function returns the index of the first character of STR that is not the character in input. If no such character is
                found, the function returns -1
        
        
        """
        ...
    @staticmethod
    def unpackSummary(doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int, doubleArray2: typing.Union[typing.List[float], jpype.JArray], intArray: typing.Union[typing.List[int], jpype.JArray]) -> None:
        """
            Unpack an array summary into its double precision and integer components.
        
            Based on the DAFUS routine of the SPICE library
        
            Parameters:
                sum (double[]): Array summary
                nd (int): Number of double precision components
                ni (int): Number of integer components
                dc (double[]): (out) Double precision components
                ic (int[]): (out) Integer components
        
        
        """
        ...

class SpiceFrame:
    """
    public final class SpiceFrame extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class contains the methods necessaries for manipulating different reference frames.
    
        It is build as an adaptation of the framex.for file from the SPICE library.
    
        Since:
            4.11
    """
    NINERT: typing.ClassVar[int] = ...
    """
    public static final int NINERT
    
        Number of inertial frames.
    
        Also see:
            :meth:`~constant`
    
    
    """
    INERTL: typing.ClassVar[int] = ...
    """
    public static final int INERTL
    
        Inertial frame type.
    
        Also see:
            :meth:`~constant`
    
    
    """
    PCK: typing.ClassVar[int] = ...
    """
    public static final int PCK
    
        PCK frame type.
    
        Also see:
            :meth:`~constant`
    
    
    """
    CK: typing.ClassVar[int] = ...
    """
    public static final int CK
    
        CK frame type.
    
        Also see:
            :meth:`~constant`
    
    
    """
    TK: typing.ClassVar[int] = ...
    """
    public static final int TK
    
        TK frame type.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @staticmethod
    def frameId2Name(int: int) -> str: ...
    @staticmethod
    def frameInfo(int: int, intArray: typing.Union[typing.List[int], jpype.JArray], intArray2: typing.Union[typing.List[int], jpype.JArray], intArray3: typing.Union[typing.List[int], jpype.JArray]) -> bool: ...
    @staticmethod
    def frameName2Id(string: str) -> int: ...
    @staticmethod
    def frameName2IdBypass(counterArray: CounterArray, stringArray: typing.Union[typing.List[str], jpype.JArray], intArray: typing.Union[typing.List[int], jpype.JArray], string2: str) -> int: ...
    @staticmethod
    def getFrameFromClass(int: int, int2: int, intArray: typing.Union[typing.List[int], jpype.JArray], stringArray: typing.Union[typing.List[str], jpype.JArray], intArray2: typing.Union[typing.List[int], jpype.JArray]) -> bool:
        """
            Getter for the frame name, frame ID, and center associated with a given frame class and class ID.
        
            Method based on the CCIFRM routine from the SPICE library.
        
            Parameters:
                frClass (int): Class of frame
                classId (int): Class ID of frame
                frCode (int[]): (out) ID code of the frame identified by FRCLSS, CLSSID
                frName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`[]): (out) Name of the frame identified by FRCLSS, CLSSID
                cent (int[]): (out) Center of the frame identified by FRCLSS, CLSSI
        
            Returns:
                :code:`true` if the requested information is available
        
        
        """
        ...
    @staticmethod
    def isInertial(int: int) -> bool:
        """
            Determine if a frame ID code corresponds to an inertial frame code.
        
            Parameters:
                code (int): frame SPICE ID code
        
            Returns:
                a boolean indicating if the frame is an inertial or non-inertial frame
        
        
        """
        ...

class SpiceKernelInfo:
    """
    public final class SpiceKernelInfo extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class created to contain the information relative to SPICE kernel loaded for
        :class:`~fr.cnes.sirius.patrius.bodies.bsp.spice.SpiceKernelManager`.
    
        Since:
            4.11
    """
    def __init__(self, string: str, string2: str, int: int, int2: int): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getFile(self) -> str:
        """
            Getter for the file name.
        
            Returns:
                the file name
        
        
        """
        ...
    def getHandle(self) -> int:
        """
            Getter for the handle associated to the file.
        
            Returns:
                the handle associated to the file
        
        
        """
        ...
    def getSource(self) -> int:
        """
            Getter for the file source.
        
            Returns:
                the file source
        
        
        """
        ...
    def getType(self) -> str:
        """
            Getter for the file type.
        
            Returns:
                the file type
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def setHandle(self, int: int) -> None:
        """
            Setter for the handle associated to the file.
        
            Parameters:
                h (int): the new handle associated to the file
        
        
        """
        ...

class SpiceKernelManager:
    """
    public final class SpiceKernelManager extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class goal is to manage the loading and unloading of SPICE kernels from other PATRIUS methods.
    
        It is based on the keeper.for file in the SPICE library.
    
        Since:
            4.11
    """
    @staticmethod
    def clearAllKernels() -> None: ...
    @staticmethod
    def getArchAndType(file: typing.Union[java.io.File, jpype.protocol.SupportsPath]) -> None: ...
    @staticmethod
    def loadSpiceKernel(string: str) -> None: ...
    @staticmethod
    def totalNumberOfKernel(string: str) -> int:
        """
            Return the number of kernels of a specified type that are currently loaded via the loadSpiceKernel interface.
        
            Based on the KTOTAL routine from the SPICE library
        
            Parameters:
                type (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): a kernel type (actually only SPK is allowed. add other types)
        
            Returns:
                the number of kernels of type TYPE
        
        
        """
        ...
    @staticmethod
    def unloadKernel(string: str) -> None: ...

class SpkBody:
    """
    public class SpkBody extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class that allows to instantiate a SpkBody to be used in :class:`~fr.cnes.sirius.patrius.bodies.bsp.spice.SpkFile`.
    
    
        Each body contains all the segments corresponding to it that were read among other informations.
    
        This class is based on the data structure description of SPKBSR in the SPICE library.
    
        Since:
            4.11
    """
    SIZEDESC: typing.ClassVar[int] = ...
    """
    public static final int SIZEDESC
    
        Size of the descriptor array.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int, int3: int, int4: int, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], string: str, int5: int, boolean: bool, int6: int): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getExpense(self) -> int:
        """
            Getter for the expense.
        
            Returns:
                the expense associated to the body
        
        
        """
        ...
    def getHighestFile(self) -> int:
        """
            Getter for the highest file number searched during the construction of the segment list.
        
            Returns:
                the highest file number searched during the construction of the segment list
        
        
        """
        ...
    def getLowerBound(self) -> float:
        """
            Getter for the lower bound of the re-use interval.
        
            Returns:
                the lower bound of the re-use interval
        
        
        """
        ...
    def getLowestFile(self) -> int:
        """
            Getter for the lowest file number searched during the construction of the segment list.
        
            Returns:
                the lowest file number searched during the construction of the segment list
        
        
        """
        ...
    def getPreviousDescriptor(self) -> typing.MutableSequence[float]:
        """
            Getter for the previous descriptor returned.
        
            Returns:
                Previous descriptor returned.
        
        
        """
        ...
    def getPreviousHandle(self) -> int:
        """
            Getter for the previous handle returned.
        
            Returns:
                the previous handle returned
        
        
        """
        ...
    def getPreviousSegmentId(self) -> str:
        """
            Getter for the previous segment identifier returned.
        
            Returns:
                the previous segment identifier returned
        
        
        """
        ...
    def getReuseExpense(self) -> int:
        """
            Getter for the expense of the re-use interval.
        
            Returns:
                the expense of the re-use interval
        
        
        """
        ...
    def getSegmentTable(self) -> java.util.List['SpkSegment']: ...
    def getUpperBound(self) -> float:
        """
            Getter for the upper bound of the re-use interval.
        
            Returns:
                the upper bound of the re-use interval
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def isCheckPrevious(self) -> bool:
        """
            Indicates if the previous segment needs to be check.
        
            Returns:
                a boolean indicating if the previous segment needs to be checked
        
        
        """
        ...
    def setCheckPrevious(self, boolean: bool) -> None:
        """
            Setter for the boolean indicating if the previous segment needs to be checked.
        
            Parameters:
                checkPrevious (boolean): boolean indicating if the previous segment needs to be checked
        
        
        """
        ...
    def setExpense(self, int: int) -> None:
        """
            Setter for the expense associated to a body.
        
            Parameters:
                expense (int): Expense to associate to the body
        
        
        """
        ...
    def setHighestFile(self, int: int) -> None:
        """
            Setter for the highest file number searched during the construction of the segment list.
        
            Parameters:
                highestFile (int): highest file number searched during the construction of the segment list
        
        
        """
        ...
    def setLowerBound(self, double: float) -> None:
        """
            Setter for the lower bound of the re-use interval.
        
            Parameters:
                lowerBound (double): the lower bound of the re-use interval
        
        
        """
        ...
    def setLowestFile(self, int: int) -> None:
        """
            Setter for the lowest file number searched during the construction of the segment list.
        
            Parameters:
                lowestFile (int): the lowest file number searched during the construction of the segment list
        
        
        """
        ...
    def setPreviousDescriptor(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Setter for the previous descriptor returned.
        
            Parameters:
                previousDescriptor (double[]): Previous descriptor returned.
        
        
        """
        ...
    def setPreviousHandle(self, int: int) -> None:
        """
            Setter for the previous handle returned.
        
            Parameters:
                previousHandle (int): the previous handle returned
        
        
        """
        ...
    def setPreviousSegmentId(self, string: str) -> None:
        """
            Setter for the previous segment identifier returned.
        
            Parameters:
                previousSegmentId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the previous segment identifier returned
        
        
        """
        ...
    def setReuseExpense(self, int: int) -> None:
        """
            Setter for the expense of the re-use interval.
        
            Parameters:
                reuseExpense (int): the expense of the re-use interval
        
        
        """
        ...
    def setUpperBound(self, double: float) -> None:
        """
            Setter for the upper bound of the re-use interval.
        
            Parameters:
                upperBound (double): the upper bound of the re-use interval
        
        
        """
        ...

class SpkFile:
    """
    public final class SpkFile extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Load and unload files for use by the readers. Buffer segments for readers.
    
        Before a file can be read by the S/P-kernel readers, it must be loaded by loadSpkFile, which among other things, loads
        the file into the DAF system.
    
        Up to MAX_FILES files may be loaded for use simultaneously, and a file only has to be loaded once to become a potential
        search target for any number of subsequent reads.
    
        Once an SPK file has been loaded, it is assigned a file handle, which is used to keep track of the file internally, and
        which is used by the calling program to refer to the file in all subsequent calls to SPK routines.
    
        A file may be removed from the list of files for potential searching by unloading it via a call to unloadSpkFile.
    
        SPKSFS performs the search for segments within a file for the S/P-kernel readers. It searches through last-loaded files
        first. Within a single file, it searches through last-inserted segments first, thus assuming that "newest data is best".
    
        Information on loaded files is used by SPKSFS to manage a buffer of saved segment descriptors and identifiers to speed
        up access time without having to necessarily perform file reads.
    
        This class is based on the SPKBSR.for file of the SPICE library.
    
        Since:
            4.11
    """
    ND: typing.ClassVar[int] = ...
    """
    public static final int ND
    
        Number of double precision components in a summary.
    
        Also see:
            :meth:`~constant`
    
    
    """
    NI: typing.ClassVar[int] = ...
    """
    public static final int NI
    
        Number of integer components in a summary.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @staticmethod
    def loadSpkFile(string: str) -> int: ...
    @staticmethod
    def searchSegment(int: int, double: float, intArray: typing.Union[typing.List[int], jpype.JArray], doubleArray: typing.Union[typing.List[float], jpype.JArray], stringArray: typing.Union[typing.List[str], jpype.JArray]) -> bool: ...
    @staticmethod
    def unloadSpkFile(int: int) -> None: ...

class SpkReader:
    @staticmethod
    def getStateRelativeToBody(string: str, double: float, string2: str, string3: str, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @staticmethod
    def getStateRelativeToCenterOfMotion(int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, intArray: typing.Union[typing.List[int], jpype.JArray], intArray2: typing.Union[typing.List[int], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @staticmethod
    def spkObjects(string: str, set: java.util.Set[int]) -> None: ...

class SpkRecord:
    """
    public final class SpkRecord extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class for the reading and evaluation of SPK records.
    
    
        The interpolation and evaluation of the Chebyshev polynome is also done here.
    
        Since:
            4.11
    """
    @staticmethod
    def evaluateType2(double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @staticmethod
    def evaluateType3(double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @staticmethod
    def readType2(int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> typing.MutableSequence[float]: ...
    @staticmethod
    def readType3(int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> typing.MutableSequence[float]: ...

class SpkSegment:
    """
    public class SpkSegment extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class allowing to instantiate Spk Segments for the list in :class:`~fr.cnes.sirius.patrius.bodies.bsp.spice.SpkBody`.
    
    
        The information stored here is the associated handle, description and identifier.
    
        This class is based on the structure defined in SPKBSR.for in the SPICE library.
    
        Since:
            4.11
    """
    def __init__(self, int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray], string: str): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getDescription(self) -> typing.MutableSequence[float]:
        """
            // Check for null input the descriptor of the segment.
        
            Returns:
                the descriptor of the segment
        
        
        """
        ...
    def getHandle(self) -> int:
        """
            Getter for the handle associated to the segment.
        
            Returns:
                the handle associated to the segment
        
        
        """
        ...
    def getId(self) -> str:
        """
            // Check for null input the identifier of the segment.
        
            Returns:
                the identifier of the segment
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class Watcher(java.lang.Comparable['Watcher']):
    """
    public class Watcher extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.bodies.bsp.spice.Watcher`>
    
        This class make up the data structure that maps variables to their associated agents. This will allow to notify all the
        agents if there is a change in the variable.
    
        This class is based on a data structure described at POOL.for from the SPICE library.
    
        Since:
            4.11
    """
    def __init__(self, string: str): ...
    def addAgent(self, string: str) -> None:
        """
            Add an agent to the list.
        
            Parameters:
                agent (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): agent to be added to the list
        
        
        """
        ...
    def compareTo(self, watcher: 'Watcher') -> int:
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
    def getAgents(self) -> java.util.List[str]: ...
    def getVarName(self) -> str:
        """
            Getter for the variable name of the watcher.
        
            Returns:
                the variable name of the watcher
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.bodies.bsp.spice")``.

    CommentSectionDAF: typing.Type[CommentSectionDAF]
    CounterArray: typing.Type[CounterArray]
    DafHandle: typing.Type[DafHandle]
    DafHandleManager: typing.Type[DafHandleManager]
    DafReader: typing.Type[DafReader]
    DafReaderTools: typing.Type[DafReaderTools]
    DafState: typing.Type[DafState]
    FileRecordDAF: typing.Type[FileRecordDAF]
    FindArraysDAF: typing.Type[FindArraysDAF]
    KernelPool: typing.Type[KernelPool]
    PoolSpice: typing.Type[PoolSpice]
    ReadDoublePrecisionDAF: typing.Type[ReadDoublePrecisionDAF]
    SpiceBody: typing.Type[SpiceBody]
    SpiceChangeFrame: typing.Type[SpiceChangeFrame]
    SpiceCommon: typing.Type[SpiceCommon]
    SpiceFrame: typing.Type[SpiceFrame]
    SpiceKernelInfo: typing.Type[SpiceKernelInfo]
    SpiceKernelManager: typing.Type[SpiceKernelManager]
    SpkBody: typing.Type[SpkBody]
    SpkFile: typing.Type[SpkFile]
    SpkReader: typing.Type[SpkReader]
    SpkRecord: typing.Type[SpkRecord]
    SpkSegment: typing.Type[SpkSegment]
    Watcher: typing.Type[Watcher]
