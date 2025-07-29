
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.files.general
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import typing



class SP3File(fr.cnes.sirius.patrius.files.general.OrbitFile, java.io.Serializable):
    """
    public class SP3File extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Represents a parsed SP3 orbit file.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def addSatellite(self, string: str) -> None:
        """
            Add a new satellite with a given identifier to the list of stored satellites.
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the satellite identifier
        
        
        """
        ...
    def addSatelliteCoordinate(self, string: str, satelliteTimeCoordinate: fr.cnes.sirius.patrius.files.general.SatelliteTimeCoordinate) -> None:
        """
            Adds a new P/V coordinate for a given satellite.
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the satellite identifier
                coord (:class:`~fr.cnes.sirius.patrius.files.general.SatelliteTimeCoordinate`): the P/V coordinate of the satellite
        
        
        """
        ...
    def containsSatellite(self, string: str) -> bool:
        """
            Tests whether a satellite with the given id is contained in this orbit file.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.files.general.OrbitFile.containsSatellite` in
                interface :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile`
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the satellite id
        
            Returns:
                :code:`true` if the satellite is contained in the file, :code:`false` otherwise
        
        
        """
        ...
    def getAgency(self) -> str:
        """
            Returns the agency that prepared this SP3 file.
        
            Returns:
                the agency
        
        
        """
        ...
    def getCoordinateSystem(self) -> str:
        """
            Returns the coordinate system of the entries in this orbit file.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.files.general.OrbitFile.getCoordinateSystem` in
                interface :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile`
        
            Returns:
                the coordinate system
        
        
        """
        ...
    def getDataUsed(self) -> str:
        """
            Returns the data used indicator from the SP3 file.
        
            Returns:
                the data used indicator (unparsed)
        
        
        """
        ...
    def getDayFraction(self) -> float:
        """
            Returns the day fraction for this SP3 file.
        
            Returns:
                the day fraction
        
        
        """
        ...
    def getEpoch(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Returns the start epoch of the orbit file.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.files.general.OrbitFile.getEpoch` in
                interface :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile`
        
            Returns:
                the start epoch
        
        
        """
        ...
    def getEpochInterval(self) -> float:
        """
            Returns the time interval between epochs (in seconds).
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.files.general.OrbitFile.getEpochInterval` in
                interface :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile`
        
            Returns:
                the time interval between epochs
        
        
        """
        ...
    def getGpsWeek(self) -> int:
        """
            Returns the GPS week as contained in the SP3 file.
        
            Returns:
                the GPS week of the SP3 file
        
        
        """
        ...
    def getJulianDay(self) -> int:
        """
            Returns the julian day for this SP3 file.
        
            Returns:
                the julian day
        
        
        """
        ...
    def getNumberOfEpochs(self) -> int:
        """
            Returns the number of epochs contained in this orbit file.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.files.general.OrbitFile.getNumberOfEpochs` in
                interface :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile`
        
            Returns:
                the number of epochs
        
        
        """
        ...
    def getOrbitType(self) -> 'SP3File.SP3OrbitType':
        """
            Returns the :class:`~fr.cnes.sirius.patrius.files.sp3.SP3File.SP3OrbitType` for this SP3 file.
        
            Returns:
                the orbit type
        
        
        """
        ...
    @typing.overload
    def getSatellite(self, int: int) -> fr.cnes.sirius.patrius.files.general.SatelliteInformation:
        """
            Get additional information about a satellite.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.files.general.OrbitFile.getSatellite` in
                interface :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile`
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the satellite id
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.files.general.SatelliteInformation` object describing the satellite if present,
                :code:`null` otherwise
        
            Returns the nth satellite as contained in the SP3 file.
        
            Parameters:
                n (int): the index of the satellite
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.files.general.SatelliteInformation` object for the nth satellite
        
        
        """
        ...
    @typing.overload
    def getSatellite(self, string: str) -> fr.cnes.sirius.patrius.files.general.SatelliteInformation: ...
    def getSatelliteCoordinates(self, string: str) -> java.util.List[fr.cnes.sirius.patrius.files.general.SatelliteTimeCoordinate]: ...
    def getSatelliteCount(self) -> int:
        """
            Get the number of satellites contained in this orbit file.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.files.general.OrbitFile.getSatelliteCount` in
                interface :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile`
        
            Returns:
                the number of satellites
        
        
        """
        ...
    def getSatellites(self) -> java.util.Collection[fr.cnes.sirius.patrius.files.general.SatelliteInformation]: ...
    def getSecondsOfWeek(self) -> float:
        """
            Returns the seconds of the GPS week as contained in the SP3 file.
        
            Returns:
                the seconds of the GPS week
        
        
        """
        ...
    def getTimeSystem(self) -> fr.cnes.sirius.patrius.files.general.OrbitFile.TimeSystem:
        """
            Returns the :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile.TimeSystem` used to time-stamp position entries.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.files.general.OrbitFile.getTimeSystem` in
                interface :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile`
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile.TimeSystem` of the orbit file
        
        
        """
        ...
    def getType(self) -> 'SP3File.SP3FileType':
        """
            Returns the :class:`~fr.cnes.sirius.patrius.files.sp3.SP3File.SP3FileType` associated with this SP3 file.
        
            Returns:
                the file type for this SP3 file
        
        
        """
        ...
    def setAgency(self, string: str) -> None:
        """
            Set the agency string for this SP3 file.
        
            Parameters:
                agencyStr (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the agency string to be set
        
        
        """
        ...
    def setCoordinateSystem(self, string: str) -> None:
        """
            Set the coordinate system used for the orbit entries.
        
            Parameters:
                system (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the coordinate system to be set
        
        
        """
        ...
    def setDataUsed(self, string: str) -> None:
        """
            Set the data used indicator for this SP3 file.
        
            Parameters:
                data (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the data used indicator to be set
        
        
        """
        ...
    def setDayFraction(self, double: float) -> None:
        """
            Set the day fraction for this SP3 file.
        
            Parameters:
                fraction (double): the day fraction to be set
        
        
        """
        ...
    def setEpoch(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Set the epoch of the SP3 file.
        
            Parameters:
                time (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the epoch to be set
        
        
        """
        ...
    def setEpochInterval(self, double: float) -> None:
        """
            Set the epoch interval for this SP3 file.
        
            Parameters:
                interval (double): the interval between orbit entries
        
        
        """
        ...
    def setGpsWeek(self, int: int) -> None:
        """
            Set the GPS week of the SP3 file.
        
            Parameters:
                week (int): the GPS week to be set
        
        
        """
        ...
    def setJulianDay(self, int: int) -> None:
        """
            Set the julian day for this SP3 file.
        
            Parameters:
                day (int): the julian day to be set
        
        
        """
        ...
    def setNumberOfEpochs(self, int: int) -> None:
        """
            Set the number of epochs as contained in the SP3 file.
        
            Parameters:
                epochCount (int): the number of epochs to be set
        
        
        """
        ...
    def setOrbitType(self, sP3OrbitType: 'SP3File.SP3OrbitType') -> None:
        """
            Set the :class:`~fr.cnes.sirius.patrius.files.sp3.SP3File.SP3OrbitType` for this SP3 file.
        
            Parameters:
                oType (:class:`~fr.cnes.sirius.patrius.files.sp3.SP3File.SP3OrbitType`): the orbit type to be set
        
        
        """
        ...
    def setSecondsOfWeek(self, double: float) -> None:
        """
            Set the seconds of the GPS week for this SP3 file.
        
            Parameters:
                seconds (double): the seconds to be set
        
        
        """
        ...
    def setTimeSystem(self, timeSystem: fr.cnes.sirius.patrius.files.general.OrbitFile.TimeSystem) -> None:
        """
            Set the time system used in this SP3 file.
        
            Parameters:
                system (:class:`~fr.cnes.sirius.patrius.files.general.OrbitFile.TimeSystem`): the time system to be set
        
        
        """
        ...
    def setType(self, sP3FileType: 'SP3File.SP3FileType') -> None:
        """
            Set the file type for this SP3 file.
        
            Parameters:
                fileType (:class:`~fr.cnes.sirius.patrius.files.sp3.SP3File.SP3FileType`): the file type to be set
        
        
        """
        ...
    class SP3FileType(java.lang.Enum['SP3File.SP3FileType']):
        GPS: typing.ClassVar['SP3File.SP3FileType'] = ...
        MIXED: typing.ClassVar['SP3File.SP3FileType'] = ...
        GLONASS: typing.ClassVar['SP3File.SP3FileType'] = ...
        LEO: typing.ClassVar['SP3File.SP3FileType'] = ...
        GALILEO: typing.ClassVar['SP3File.SP3FileType'] = ...
        COMPASS: typing.ClassVar['SP3File.SP3FileType'] = ...
        QZSS: typing.ClassVar['SP3File.SP3FileType'] = ...
        UNDEFINED: typing.ClassVar['SP3File.SP3FileType'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'SP3File.SP3FileType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['SP3File.SP3FileType']: ...
    class SP3OrbitType(java.lang.Enum['SP3File.SP3OrbitType']):
        FIT: typing.ClassVar['SP3File.SP3OrbitType'] = ...
        EXT: typing.ClassVar['SP3File.SP3OrbitType'] = ...
        BCT: typing.ClassVar['SP3File.SP3OrbitType'] = ...
        HLM: typing.ClassVar['SP3File.SP3OrbitType'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'SP3File.SP3OrbitType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['SP3File.SP3OrbitType']: ...

class SP3Parser(fr.cnes.sirius.patrius.files.general.OrbitFileParser):
    """
    public class SP3Parser extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.files.general.OrbitFileParser`
    
        A parser for the SP3 orbit file format. It supports the original format as well as the latest SP3-c version.
    
        **Note:** this parser is thread-safe, so calling :meth:`~fr.cnes.sirius.patrius.files.sp3.SP3Parser.parse` from
        different threads is allowed.
    
        Also see:
            `SP3-a file format <http://igscb.jpl.nasa.gov/igscb/data/format/sp3_docu.txt>`, `SP3-c file format
            <http://igscb.jpl.nasa.gov/igscb/data/format/sp3c.txt>`
    """
    def __init__(self): ...
    @typing.overload
    def parse(self, inputStream: java.io.InputStream) -> SP3File: ...
    @typing.overload
    def parse(self, string: str) -> SP3File: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.files.sp3")``.

    SP3File: typing.Type[SP3File]
    SP3Parser: typing.Type[SP3Parser]
