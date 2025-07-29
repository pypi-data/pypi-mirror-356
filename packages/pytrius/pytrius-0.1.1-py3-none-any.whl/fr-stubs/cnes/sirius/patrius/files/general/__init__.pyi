
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import typing



class OrbitFile:
    """
    public interface OrbitFile
    
        Interface for orbit file representations.
    """
    def containsSatellite(self, string: str) -> bool:
        """
            Tests whether a satellite with the given id is contained in this orbit file.
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the satellite id
        
            Returns:
                :code:`true` if the satellite is contained in the file, :code:`false` otherwise
        
        
        """
        ...
    def getCoordinateSystem(self) -> str:
        """
            Returns the coordinate system of the entries in this orbit file.
        
            Returns:
                the coordinate system
        
        
        """
        ...
    def getEpoch(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Returns the start epoch of the orbit file.
        
            Returns:
                the start epoch
        
        
        """
        ...
    def getEpochInterval(self) -> float:
        """
            Returns the time interval between epochs (in seconds).
        
            Returns:
                the time interval between epochs
        
        
        """
        ...
    def getNumberOfEpochs(self) -> int:
        """
            Returns the number of epochs contained in this orbit file.
        
            Returns:
                the number of epochs
        
        
        """
        ...
    def getSatellite(self, string: str) -> 'SatelliteInformation':
        """
            Get additional information about a satellite.
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the satellite id
        
            Returns:
                a :class:`~fr.cnes.sirius.patrius.files.general.SatelliteInformation` object describing the satellite if present,
                :code:`null` otherwise
        
        
        """
        ...
    def getSatelliteCoordinates(self, string: str) -> java.util.List['SatelliteTimeCoordinate']: ...
    def getSatelliteCount(self) -> int:
        """
            Get the number of satellites contained in this orbit file.
        
            Returns:
                the number of satellites
        
        
        """
        ...
    def getSatellites(self) -> java.util.Collection['SatelliteInformation']: ...
    def getTimeSystem(self) -> 'OrbitFile.TimeSystem':
        """
            Returns the :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile.TimeSystem` used to time-stamp position entries.
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.files.general.OrbitFile.TimeSystem` of the orbit file
        
        
        """
        ...
    class TimeSystem(java.lang.Enum['OrbitFile.TimeSystem']):
        GPS: typing.ClassVar['OrbitFile.TimeSystem'] = ...
        GLO: typing.ClassVar['OrbitFile.TimeSystem'] = ...
        GAL: typing.ClassVar['OrbitFile.TimeSystem'] = ...
        TAI: typing.ClassVar['OrbitFile.TimeSystem'] = ...
        UTC: typing.ClassVar['OrbitFile.TimeSystem'] = ...
        QZS: typing.ClassVar['OrbitFile.TimeSystem'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'OrbitFile.TimeSystem': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['OrbitFile.TimeSystem']: ...

class OrbitFileParser:
    """
    public interface OrbitFileParser
    
        Interface for orbit file parsers.
    """
    @typing.overload
    def parse(self, inputStream: java.io.InputStream) -> OrbitFile: ...
    @typing.overload
    def parse(self, string: str) -> OrbitFile: ...

class SatelliteInformation(java.io.Serializable):
    """
    public class SatelliteInformation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Contains general information about a satellite as contained in an orbit file.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str): ...
    def getAccuracy(self) -> int:
        """
            Returns the estimated accuracy of the orbit entries for this satellite (in m).
        
            Returns:
                the accuracy in m (one standard deviation)
        
        
        """
        ...
    def getSatelliteId(self) -> str:
        """
            Returns the id for this satellite object.
        
            Returns:
                the satellite id
        
        
        """
        ...
    def setAccuracy(self, int: int) -> None:
        """
            Set the accuracy for this satellite.
        
            Parameters:
                accuracyIn (int): the accuracy in m (one standard deviation)
        
        
        """
        ...
    def setSatelliteId(self, string: str) -> None:
        """
            Set the id of this satellite.
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the satellite id to be set
        
        
        """
        ...

class SatelliteTimeCoordinate(fr.cnes.sirius.patrius.time.TimeStamped, java.io.Serializable):
    """
    public class SatelliteTimeCoordinate extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Contains the position/velocity of a satellite at an specific epoch.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, double: float, double2: float): ...
    def getClockCorrection(self) -> float:
        """
            Returns the clock correction value.
        
            Returns:
                the clock correction in microseconds
        
        
        """
        ...
    def getClockRateChange(self) -> float:
        """
            Returns the clock rate change value.
        
            Returns:
                the clock rate change in 10^(-4) microseconds/second
        
        
        """
        ...
    def getCoordinate(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates:
        """
            Returns the coordinate of this entry.
        
            Returns:
                the coordinate in SI units (position in meters, velocity in meters/second and acceleration in meters/(second^2))
        
        
        """
        ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                date attached to the object
        
        
        """
        ...
    def getEpoch(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Returns the epoch for this coordinate.
        
            Returns:
                the epoch
        
        
        """
        ...
    def setClockCorrection(self, double: float) -> None:
        """
            Set the clock correction to the given value.
        
            Parameters:
                corr (double): the clock correction value in microseconds
        
        
        """
        ...
    def setClockRateChange(self, double: float) -> None:
        """
            Set the clock rate change to the given value.
        
            Parameters:
                rateChange (double): the clock rate change value in 10^(-4) microseconds/second
        
        
        """
        ...
    def setCoordinate(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates) -> None:
        """
            Set the coordinate for this entry.
        
            Parameters:
                coordinateIn (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`): the coordinate to be set in SI units (position in meters, velocity in meters/second and acceleration in
                    meters/(second^2))
        
        
        """
        ...
    def setEpoch(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Set the epoch for this coordinate.
        
            Parameters:
                epochIn (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the epoch to be set
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.files.general")``.

    OrbitFile: typing.Type[OrbitFile]
    OrbitFileParser: typing.Type[OrbitFileParser]
    SatelliteInformation: typing.Type[SatelliteInformation]
    SatelliteTimeCoordinate: typing.Type[SatelliteTimeCoordinate]
