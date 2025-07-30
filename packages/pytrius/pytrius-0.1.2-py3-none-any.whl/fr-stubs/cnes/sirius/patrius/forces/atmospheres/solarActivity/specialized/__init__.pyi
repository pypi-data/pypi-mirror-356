
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.forces.atmospheres
import fr.cnes.sirius.patrius.forces.atmospheres.solarActivity
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import typing



class AbstractMSISE2000SolarData(fr.cnes.sirius.patrius.forces.atmospheres.MSISE2000InputParameters):
    """
    public abstract class AbstractMSISE2000SolarData extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSISE2000InputParameters`
    
        This abstract class represents a solar data container adapted for the
        :class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSISE2000` atmosphere model. It implements the methods and constants
        common to the MSISE2000 data providers.
    
        Since:
            2.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.ContinuousMSISE2000SolarData`,
            :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.ClassicalMSISE2000SolarData`,
            :meth:`~serialized`
    """
    def __init__(self, solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider): ...
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def getApValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]: ...
    def getInstantFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range maximum date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.MSISE2000InputParameters.getMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSISE2000InputParameters`
        
            Returns:
                the maximum date.
        
        
        """
        ...
    def getMeanFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range minimum date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.MSISE2000InputParameters.getMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSISE2000InputParameters`
        
            Returns:
                the minimum date.
        
        
        """
        ...

class DTMSolarData(fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters):
    """
    public class DTMSolarData extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters`
    
        This class represents a solar data container adapted for the :class:`~fr.cnes.sirius.patrius.forces.atmospheres.DTM2000`
        and :class:`~fr.cnes.sirius.patrius.forces.atmospheres.DTM2012` atmosphere models
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider): ...
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def get24HoursKp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getInstantFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range maximum date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters.getMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters`
        
            Returns:
                the maximum date.
        
        
        """
        ...
    def getMeanFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range minimum date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters.getMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters`
        
            Returns:
                the minimum date.
        
        
        """
        ...
    def getThreeHourlyKP(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...

class MarshallSolarActivityFutureEstimation(fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters, fr.cnes.sirius.patrius.data.DataLoader):
    """
    public class MarshallSolarActivityFutureEstimation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters`, :class:`~fr.cnes.sirius.patrius.data.DataLoader`
    
        This class reads and provides solar activity data needed by atmospheric models: F107 solar flux and Kp indexes.
    
        The data are retrieved through the NASA Marshall Solar Activity Future Estimation (MSAFE) as estimates of monthly F10.7
        Mean solar flux and Ap geomagnetic parameter. The data can be retrieved at the NASA ` Marshall Solar Activity website
        <http://sail.msfc.nasa.gov/archive_index.htm>`. Here Kp indices are deduced from Ap indexes, which in turn are tabulated
        equivalent of retrieved Ap values.
    
        If several MSAFE files are available, some dates may appear in several files (for example August 2007 is in all files
        from the first one published in March 1999 to the February 2008 file). In this case, the data from the most recent file
        is used and the older ones are discarded. The date of the file is assumed to be 6 months after its first entry (which
        explains why the file having August 2007 as its first entry is the February 2008 file). This implies that MSAFE files
        must *not* be edited to change their time span, otherwise this would break the old entries overriding mechanism.
    
        With these data, the
        :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.MarshallSolarActivityFutureEstimation.getInstantFlux`
        and
        :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.MarshallSolarActivityFutureEstimation.getMeanFlux`
        methods return the same values and the
        :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.MarshallSolarActivityFutureEstimation.get24HoursKp`
        and
        :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.MarshallSolarActivityFutureEstimation.getThreeHourlyKP`
        methods return the same values.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str, strengthLevel: 'MarshallSolarActivityFutureEstimation.StrengthLevel'): ...
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def get24HoursKp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getFileDate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.time.DateComponents: ...
    def getInstantFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range maximum date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters.getMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters`
        
            Returns:
                the maximum date.
        
        
        """
        ...
    def getMeanFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range minimum date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters.getMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.DTMInputParameters`
        
            Returns:
                the minimum date.
        
        
        """
        ...
    def getStrengthLevel(self) -> 'MarshallSolarActivityFutureEstimation.StrengthLevel':
        """
            Get the strength level for activity.
        
            Returns:
                strength level to set
        
        
        """
        ...
    def getSupportedNames(self) -> str:
        """
            Get the supported names for data files.
        
            Returns:
                regular expression for the supported names for data files
        
        
        """
        ...
    def getThreeHourlyKP(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
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
    class StrengthLevel(java.lang.Enum['MarshallSolarActivityFutureEstimation.StrengthLevel']):
        STRONG: typing.ClassVar['MarshallSolarActivityFutureEstimation.StrengthLevel'] = ...
        AVERAGE: typing.ClassVar['MarshallSolarActivityFutureEstimation.StrengthLevel'] = ...
        WEAK: typing.ClassVar['MarshallSolarActivityFutureEstimation.StrengthLevel'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'MarshallSolarActivityFutureEstimation.StrengthLevel': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['MarshallSolarActivityFutureEstimation.StrengthLevel']: ...

class ClassicalMSISE2000SolarData(AbstractMSISE2000SolarData):
    """
    public class ClassicalMSISE2000SolarData extends :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.AbstractMSISE2000SolarData`
    
        This class represents a solar data container adapted for the
        :class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSISE2000` atmosphere model This model of input parameters computes
        averages for SOME of the ap values required by the MSISE2000 model. See the
        :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.ClassicalMSISE2000SolarData.getApValues` and
        :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.ContinuousMSISE2000SolarData.getApValues`
        methods.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider): ...
    def getApValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]: ...

class ContinuousMSISE2000SolarData(AbstractMSISE2000SolarData):
    """
    public class ContinuousMSISE2000SolarData extends :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.AbstractMSISE2000SolarData`
    
        This class represents a solar data container adapted for the
        :class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSISE2000` atmosphere model This model of input parameters computes
        averages for ALL the ap values required by the MSISE2000 model. See the
        :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.ClassicalMSISE2000SolarData.getApValues` and
        :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized.ContinuousMSISE2000SolarData.getApValues`
        methods.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider): ...
    def getApValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]: ...
    def getInstantFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMeanFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.specialized")``.

    AbstractMSISE2000SolarData: typing.Type[AbstractMSISE2000SolarData]
    ClassicalMSISE2000SolarData: typing.Type[ClassicalMSISE2000SolarData]
    ContinuousMSISE2000SolarData: typing.Type[ContinuousMSISE2000SolarData]
    DTMSolarData: typing.Type[DTMSolarData]
    MarshallSolarActivityFutureEstimation: typing.Type[MarshallSolarActivityFutureEstimation]
