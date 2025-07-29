
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



class SolarActivityDataFactory:
    ACSOL_FILENAME: typing.ClassVar[str] = ...
    NOAA_FILENAME: typing.ClassVar[str] = ...
    @staticmethod
    def addDefaultSolarActivityDataReaders() -> None: ...
    @staticmethod
    def addSolarActivityDataReader(solarActivityDataReader: 'SolarActivityDataReader') -> None: ...
    @staticmethod
    def clearSolarActivityDataReaders() -> None: ...
    @staticmethod
    def getSolarActivityDataProvider() -> 'SolarActivityDataProvider': ...

class SolarActivityDataProvider(java.io.Serializable):
    """
    public interface SolarActivityDataProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for solar activity data providers, to be used for atmosphere models
    
        Since:
            1.1
    """
    def checkApKpValidity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Check that solar data (ap/kp) are available in the user range [start; end].
        
            Parameters:
                start (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): range start date
                end (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): range end date
        
        
        """
        ...
    def checkFluxValidity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Check that solar data (flux) are available in the user range [start; end].
        
            Parameters:
                start (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): range start date
                end (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): range end date
        
        
        """
        ...
    def getAp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getApKpMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date of ap / kp values
        
            Returns:
                a date
        
        
        """
        ...
    def getApKpMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date of ap / kp values
        
            Returns:
                a date
        
        
        """
        ...
    def getApKpValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.SortedMap[fr.cnes.sirius.patrius.time.AbsoluteDate, typing.MutableSequence[float]]: ...
    def getFluxMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date of flux values
        
            Returns:
                a date
        
        
        """
        ...
    def getFluxMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date of flux values
        
            Returns:
                a date
        
        
        """
        ...
    def getInstantFluxValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getInstantFluxValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.SortedMap[fr.cnes.sirius.patrius.time.AbsoluteDate, float]: ...
    def getKp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date at which both flux and ap values are available
        
            Returns:
                a date
        
        
        """
        ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date at which both flux and ap values are available
        
            Returns:
                a date
        
        
        """
        ...
    def getStepApKp(self) -> float: ...
    def getStepF107(self) -> float: ...

class SolarActivityToolbox:
    """
    public final class SolarActivityToolbox extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Solar activity toolbox. Has methods to compute mean flux values, to convert from ap to kp.
    
        Since:
            1.2
    """
    @typing.overload
    @staticmethod
    def apToKp(double: float) -> float:
        """
            Convert a single ap coefficient to a kp coefficient
        
            Parameters:
                ap (double): coefficient to convert
        
            Returns:
                corresponding kp coefficient, linear interpolation
        
            Convert an array
        
            Parameters:
                ap (double[]): array to convert
        
            Returns:
                corresponding kp array
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def apToKp(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @staticmethod
    def checkApSanity(double: float) -> None:
        """
            Check that the specified ap coefficient is within bounds
        
            Parameters:
                ap (double): ap coefficient
        
        
        """
        ...
    @staticmethod
    def checkKpSanity(double: float) -> None:
        """
            Check that the specified kp coefficient is within bounds
        
            Parameters:
                kp (double): kp coefficient
        
        
        """
        ...
    @staticmethod
    def getAverageFlux(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, solarActivityDataProvider: SolarActivityDataProvider) -> float: ...
    @staticmethod
    def getMeanAp(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, solarActivityDataProvider: SolarActivityDataProvider) -> float: ...
    @staticmethod
    def getMeanFlux(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, solarActivityDataProvider: SolarActivityDataProvider) -> float: ...
    @typing.overload
    @staticmethod
    def kpToAp(double: float) -> float:
        """
            Convert a single kp coefficient to a ap coefficient
        
            Parameters:
                kp (double): coefficient to convert
        
            Returns:
                corresponding ap coefficient, linear interpolation
        
            Convert an array
        
            Parameters:
                kp (double[]): array to convert
        
            Returns:
                corresponding ap array
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def kpToAp(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...

class ConstantSolarActivity(SolarActivityDataProvider):
    """
    public class ConstantSolarActivity extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
    
        This class represents constant solar activity
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...
    def getAp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get Geomagnetic activity Ap value at given user date
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getAp` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): user date
        
            Returns:
                Ap value
        
        
        """
        ...
    def getApKpMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date of ap / kp values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getApKpMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getApKpMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date of ap / kp values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getApKpMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getApKpValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.SortedMap[fr.cnes.sirius.patrius.time.AbsoluteDate, typing.MutableSequence[float]]: ...
    def getFluxMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date of flux values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getFluxMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getFluxMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date of flux values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getFluxMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getInstantFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the value of the instantaneous solar flux.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the current date
        
            Returns:
                the instantaneous solar flux
        
        
        """
        ...
    def getInstantFluxValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getInstantFluxValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.SortedMap[fr.cnes.sirius.patrius.time.AbsoluteDate, float]: ...
    def getKp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get Kp value at given user date
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getKp` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): user date
        
            Returns:
                Kp value
        
        
        """
        ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date at which both flux and ap values are available
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date at which both flux and ap values are available
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getStepApKp(self) -> float: ...
    def getStepF107(self) -> float: ...

class ExtendedSolarActivityWrapper(SolarActivityDataProvider):
    """
    public class ExtendedSolarActivityWrapper extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
    
        This class is a solar activity data provider fed with:
    
          - a user-defined :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
          - A averaged duration *d*
    
        It is built with the following convention:
    
          - It returns solar activity from user-provided solar activity data provider if date is within timespan of the
            user-provided solar activity data provider.
          - It returns an average of first available solar data over user-defined period *d* if date is before lower boundary of the
            user-provided solar activity data provider.
          - It returns an average of last available solar data over user-defined period *d* if date is after upper boundary of the
            user-provided solar activity data provider.
    
    
        Since:
            3.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, solarActivityDataProvider: SolarActivityDataProvider, double: float): ...
    def getAp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getApKpMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date of ap / kp values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getApKpMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getApKpMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date of ap / kp values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getApKpMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getApKpValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.SortedMap[fr.cnes.sirius.patrius.time.AbsoluteDate, typing.MutableSequence[float]]: ...
    def getFluxMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date of flux values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getFluxMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getFluxMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date of flux values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getFluxMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getInstantFluxValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getInstantFluxValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.SortedMap[fr.cnes.sirius.patrius.time.AbsoluteDate, float]: ...
    def getKp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date at which both flux and ap values are available
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date at which both flux and ap values are available
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getStepApKp(self) -> float: ...
    def getStepF107(self) -> float: ...

class SolarActivityDataReader(fr.cnes.sirius.patrius.data.DataLoader, SolarActivityDataProvider):
    """
    public abstract class SolarActivityDataReader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataLoader`, :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
    
        Represents a basic solar activity file reader. This class puts in common the same methods used by solar activity file
        readers, and defines a common abstract class.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def getAp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get Geomagnetic activity Ap value at given user date
        
        
            Warning: for performance reasons, this method does not check if data are available for provided date. If not data is
            available for provided date, null is returned. The method
            :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.checkApKpValidity` should be
            called to ensure data are available for provided date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getAp` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): user date
        
            Returns:
                Ap value
        
        
        """
        ...
    def getApKpMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date of ap / kp values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getApKpMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getApKpMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date of ap / kp values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getApKpMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getApKpValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.SortedMap[fr.cnes.sirius.patrius.time.AbsoluteDate, typing.MutableSequence[float]]: ...
    def getFluxMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date of flux values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getFluxMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getFluxMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date of flux values
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getFluxMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getInstantFluxValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get instant flux values at the given dates (possibly interpolated) This is the default implementation for this method :
            it interpolates the flux values before or after
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getInstantFluxValue` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): user date
        
            Returns:
                instant flux values
        
        
        """
        ...
    def getInstantFluxValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.SortedMap[fr.cnes.sirius.patrius.time.AbsoluteDate, float]: ...
    def getKp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get Kp value at given user date Warning: for performance reasons, this method does not check if data are available for
            provided date. If not data is available for provided date, null is returned. The method
            :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.checkApKpValidity` should be
            called to ensure data are available for provided date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getKp` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): user date
        
            Returns:
                Kp value
        
        
        """
        ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get maximum date at which both flux and ap values are available
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get minimum date at which both flux and ap values are available
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider.getMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`
        
            Returns:
                a date
        
        
        """
        ...
    def getStepApKp(self) -> float: ...
    def getStepF107(self) -> float: ...
    def getSupportedNames(self) -> str:
        """
            Get the regular expression for supported files names.
        
            Returns:
                regular expression for supported files names
        
        
        """
        ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...
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

class ACSOLFormatReader(SolarActivityDataReader):
    """
    public class ACSOLFormatReader extends :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataReader`
    
        This class reads ACSOL format solar activity data
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str): ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...

class NOAAFormatReader(SolarActivityDataReader):
    """
    public class NOAAFormatReader extends :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataReader`
    
        This class reads NOAA format solar activity data
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str): ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.atmospheres.solarActivity")``.

    ACSOLFormatReader: typing.Type[ACSOLFormatReader]
    ConstantSolarActivity: typing.Type[ConstantSolarActivity]
    ExtendedSolarActivityWrapper: typing.Type[ExtendedSolarActivityWrapper]
    NOAAFormatReader: typing.Type[NOAAFormatReader]
    SolarActivityDataFactory: typing.Type[SolarActivityDataFactory]
    SolarActivityDataProvider: typing.Type[SolarActivityDataProvider]
    SolarActivityDataReader: typing.Type[SolarActivityDataReader]
    SolarActivityToolbox: typing.Type[SolarActivityToolbox]
    specialized: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.__module_protocol__
