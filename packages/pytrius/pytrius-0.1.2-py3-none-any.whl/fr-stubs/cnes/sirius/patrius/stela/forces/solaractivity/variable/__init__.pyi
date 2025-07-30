
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.forces.atmospheres.solarActivity
import fr.cnes.sirius.patrius.stela.forces.solaractivity
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



class StelaPastCycleSolarActivityProperties(java.io.Serializable):
    """
    public final class StelaPastCycleSolarActivityProperties extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class to store the past cycles solar activity files
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    @staticmethod
    def getPastCycleFilePath() -> java.util.List[java.io.InputStream]: ...
    @staticmethod
    def setPastCycleFilePaths(list: java.util.List[str]) -> None: ...

class StelaPastCyclesData(java.io.Serializable):
    """
    public class StelaPastCyclesData extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Data necessary for past cycles solar activity.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int, list: java.util.List[int], boolean: bool): ...
    def getSolarActivityCycles(self) -> java.util.List[int]: ...
    def getSolarActivityFirstDay(self) -> int:
        """
            Getter for the solar activity first day.
        
            Returns:
                the solar activity first day
        
        
        """
        ...
    def isAdditionalCycle(self) -> bool:
        """
        
            Returns:
                true if an additional cycle is appended at the beginning of the solar activity cycles' list
        
        
        """
        ...

class StelaPastCyclesSolarActivityReader(fr.cnes.sirius.patrius.data.DataLoader, java.io.Serializable):
    """
    public class StelaPastCyclesSolarActivityReader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataLoader`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class to read solar activity past cycles files
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getSolarAPMap(self) -> java.util.NavigableMap[float, java.util.List[float]]: ...
    def getSolarFluxMap(self) -> java.util.NavigableMap[float, java.util.List[float]]: ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...
    def setReadCompleted(self, boolean: bool) -> None: ...
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

class StelaVariableSolarActivity(fr.cnes.sirius.patrius.stela.forces.solaractivity.AbstractStelaSolarActivity):
    """
    public class StelaVariableSolarActivity extends :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.AbstractStelaSolarActivity`
    
        Variable model of solar activity. This model uses the solar activity file provided in the *configuration* folder.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider): ...
    def copy(self) -> 'StelaVariableSolarActivity': ...
    def getAp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getEntireAPMap(self) -> java.util.NavigableMap[fr.cnes.sirius.patrius.time.AbsoluteDate, float]: ...
    def getInstantFluxValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMeanFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    def getSolarActivity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]: ...
    def toString(self) -> str:
        """
            Get information of Solar Activity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity.toString` in
                interface :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity`
        
            Overrides:
                 in class 
        
            Returns:
                a string with all solar activity
        
        
        """
        ...

class Stela3StepsSolarActivity(StelaVariableSolarActivity):
    """
    public class Stela3StepsSolarActivity extends :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.StelaVariableSolarActivity`
    
        Class for variable solar activity using 3 steps method: keep variable file until
        :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.Stela3StepsSolarActivity.date1`, disperse file
        between :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.Stela3StepsSolarActivity.date1` and
        :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.Stela3StepsSolarActivity.date2` (using coefficients
        :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.Stela3StepsSolarActivity.f107Coef` and
        :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.Stela3StepsSolarActivity.apCoef`) and use random
        cycles after :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.Stela3StepsSolarActivity.date2`.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, list: java.util.List[int], solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider): ...
    def buildSolarActivity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Build solar activity. The resulting solar activity is stored in
            :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.Stela3StepsSolarActivity.solarFluxMap` and
            :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.Stela3StepsSolarActivity.solarAPMap`. The resulting
            maps is a map following the pattern [:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`, solar activity] and built
            similarly as
            :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.StelaPastCyclesSolarActivity.buildSolarActivity`.
        
            Parameters:
                startDate (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): simulation starting date
        
        
        """
        ...
    def copy(self) -> 'Stela3StepsSolarActivity': ...
    def getApCoef(self) -> float:
        """
            Getter for the Ap dispersion coefficient.
        
            Returns:
                the Ap dispersion coefficient
        
        
        """
        ...
    def getDate1(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the first date.
        
            Returns:
                the first date
        
        
        """
        ...
    def getDate2(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the second date.
        
            Returns:
                the second date
        
        
        """
        ...
    def getEntireAPMap(self) -> java.util.TreeMap[fr.cnes.sirius.patrius.time.AbsoluteDate, float]: ...
    def getF107Coef(self) -> float:
        """
            Getter for the F10.7 dispersion coefficient.
        
            Returns:
                the F10.7 dispersion coefficient
        
        
        """
        ...
    def getSolarActivityCycles(self) -> java.util.List[int]: ...
    def toString(self) -> str:
        """
            Get information of Solar Activity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity.toString` in
                interface :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.StelaVariableSolarActivity.toString` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.StelaVariableSolarActivity`
        
            Returns:
                a string with all solar activity
        
        
        """
        ...
    def writeToFile(self, string: str) -> None:
        """
            Write solar activity array into file following STELA solar activity file pattern.
        
            Parameters:
                fileName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): file name
        
        
        """
        ...

class StelaPastCyclesSolarActivity(StelaVariableSolarActivity):
    @typing.overload
    def __init__(self, stelaPastCyclesData: StelaPastCyclesData): ...
    @typing.overload
    def __init__(self, int: int, list: java.util.List[int]): ...
    def buildSolarActivity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def copy(self) -> 'StelaPastCyclesSolarActivity': ...
    def emptyMaps(self) -> None: ...
    def getEntireAPMap(self) -> java.util.TreeMap[fr.cnes.sirius.patrius.time.AbsoluteDate, float]: ...
    def getSolarActivityCycles(self) -> java.util.List[int]: ...
    def getSolarActivityFirstDay(self) -> int: ...
    def isAdditionalCycle(self) -> bool: ...
    def toString(self) -> str: ...

class StelaVariableDispersedSolarActivity(StelaVariableSolarActivity):
    """
    public class StelaVariableDispersedSolarActivity extends :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.StelaVariableSolarActivity`
    
        Class for variable solar activity with a multiplicative coefficient applied.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider): ...
    @typing.overload
    def __init__(self, solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider): ...
    def copy(self) -> 'StelaVariableDispersedSolarActivity': ...
    def getAp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getApCoef(self) -> float:
        """
            Get the AP coefficient of the variable solar activity.
        
            Returns:
                the AP coefficient of the variable solar activity.
        
        
        """
        ...
    def getEntireAPMap(self) -> java.util.TreeMap[fr.cnes.sirius.patrius.time.AbsoluteDate, float]: ...
    def getFluxCoef(self) -> float:
        """
            Get the F10.7 coefficient of the variable solar activity.
        
            Returns:
                the F10.7 coefficient of the variable solar activity.
        
        
        """
        ...
    def getInstantFluxValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getSolarActivity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]: ...
    def toString(self) -> str:
        """
            Get information of Solar Activity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity.toString` in
                interface :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.StelaVariableSolarActivity.toString` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.StelaVariableSolarActivity`
        
            Returns:
                a string with all solar activity
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.forces.solaractivity.variable")``.

    Stela3StepsSolarActivity: typing.Type[Stela3StepsSolarActivity]
    StelaPastCycleSolarActivityProperties: typing.Type[StelaPastCycleSolarActivityProperties]
    StelaPastCyclesData: typing.Type[StelaPastCyclesData]
    StelaPastCyclesSolarActivity: typing.Type[StelaPastCyclesSolarActivity]
    StelaPastCyclesSolarActivityReader: typing.Type[StelaPastCyclesSolarActivityReader]
    StelaVariableDispersedSolarActivity: typing.Type[StelaVariableDispersedSolarActivity]
    StelaVariableSolarActivity: typing.Type[StelaVariableSolarActivity]
