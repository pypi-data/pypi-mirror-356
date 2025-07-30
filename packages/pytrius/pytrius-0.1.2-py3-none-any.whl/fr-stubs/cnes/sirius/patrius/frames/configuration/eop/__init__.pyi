
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import typing



class EOP1980HistoryLoader(fr.cnes.sirius.patrius.data.DataLoader):
    """
    public interface EOP1980HistoryLoader extends :class:`~fr.cnes.sirius.patrius.data.DataLoader`
    
        Interface for loading Earth Orientation Parameters 1980 history.
    """
    def fillHistory(self, eOP1980History: 'EOP1980History') -> None: ...

class EOP2000HistoryLoader(fr.cnes.sirius.patrius.data.DataLoader):
    """
    public interface EOP2000HistoryLoader extends :class:`~fr.cnes.sirius.patrius.data.DataLoader`
    
        Interface for loading Earth Orientation Parameters 2000 history.
    """
    def fillHistory(self, eOP2000History: 'EOP2000History') -> None: ...

class EOPEntry(fr.cnes.sirius.patrius.time.TimeStamped, java.io.Serializable):
    """
    public class EOPEntry extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class holds an Earth Orientation Parameters entry.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, dtType: 'EOPEntry.DtType'): ...
    @typing.overload
    def __init__(self, dateComponents: fr.cnes.sirius.patrius.time.DateComponents, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, dateComponents: fr.cnes.sirius.patrius.time.DateComponents, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, dtType: 'EOPEntry.DtType'): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, dtType: 'EOPEntry.DtType'): ...
    def getDX(self) -> float:
        """
            Get the dx correction of the X component of the celestial pole (IAU 2000) or celestial pole offset in longitude (IAU
            1980).
        
            Returns:
                δ&Delta;ψ :sub:`1980` parameter (radians) or δX :sub:`2000` parameter (radians)
        
        
        """
        ...
    def getDY(self) -> float:
        """
            Get the dy correction of the Y component of the celestial pole (IAU 2000) or celestial pole offset in obliquity (IAU
            1980).
        
            Returns:
                δ&Delta;ε :sub:`1980` parameter (radians) or δY :sub:`2000` parameter (radians)
        
        
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
    def getLOD(self) -> float:
        """
            Get the LoD (Length of Day) value.
        
            Returns:
                LoD in seconds
        
        
        """
        ...
    def getUT1MinusTAI(self) -> float:
        """
            Get the UT1-TAI value.
        
            Returns:
                UT1-TAI in seconds
        
        
        """
        ...
    def getX(self) -> float:
        """
            Get the X component of the pole motion.
        
            Returns:
                X component of pole motion
        
        
        """
        ...
    def getY(self) -> float:
        """
            Get the Y component of the pole motion.
        
            Returns:
                Y component of pole motion
        
        
        """
        ...
    class DtType(java.lang.Enum['EOPEntry.DtType']):
        UT1_TAI: typing.ClassVar['EOPEntry.DtType'] = ...
        UT1_UTC: typing.ClassVar['EOPEntry.DtType'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'EOPEntry.DtType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['EOPEntry.DtType']: ...

class EOPHistory(java.lang.Iterable[fr.cnes.sirius.patrius.time.TimeStamped]):
    """
    public interface EOPHistory extends `Iterable <http://docs.oracle.com/javase/8/docs/api/java/lang/Iterable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.time.TimeStamped`>
    
        Interface for retrieving Earth Orientation Parameters history throughout a large time range.
    """
    def addEntry(self, eOPEntry: EOPEntry) -> None:
        """
            Add an Earth Orientation Parameters entry.
        
            Parameters:
                entry (:class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPEntry`): entry to add
        
        
        """
        ...
    def getEOPInterpolationMethod(self) -> 'EOPInterpolators':
        """
            Return the EOP interpolation method.
        
            Returns:
                eop interpolation method
        
        
        """
        ...
    def getEndDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date of the last available Earth Orientation Parameters.
        
            Returns:
                the end date of the available data
        
        
        """
        ...
    def getLOD(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the LoD (Length of Day) value.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the value is desired
        
            Returns:
                LoD in seconds (0 if date is outside covered range)
        
        
        """
        ...
    def getNutationCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'NutationCorrection':
        """
            Get the correction to the nutation parameters.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the correction is desired
        
            Returns:
                nutation correction (:meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.NutationCorrection.NULL_CORRECTION` if date
                is outside covered range)
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'PoleCorrection': ...
    def getStartDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date of the first available Earth Orientation Parameters.
        
            Returns:
                the start date of the available data
        
        
        """
        ...
    def getUT1MinusTAI(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the UT1-TAI value.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the value is desired
        
            Returns:
                UT1-TAI in seconds (0 if date is outside covered range)
        
        
        """
        ...
    def getUT1MinusUTC(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the UT1-UTC value.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the value is desired
        
            Returns:
                UT1-UTC in seconds (0 if date is outside covered range)
        
        
        """
        ...
    def size(self) -> int:
        """
            Get the number of entries in the history.
        
            Returns:
                number of entries in the history
        
        
        """
        ...

class EOPHistoryFactory:
    RAPID_DATA_PREDICITON_COLUMNS_1980_FILENAME: typing.ClassVar[str] = ...
    RAPID_DATA_PREDICITON_XML_1980_FILENAME: typing.ClassVar[str] = ...
    EOPC04_1980_FILENAME: typing.ClassVar[str] = ...
    BULLETINB_1980_FILENAME: typing.ClassVar[str] = ...
    RAPID_DATA_PREDICITON_COLUMNS_2000_FILENAME: typing.ClassVar[str] = ...
    RAPID_DATA_PREDICITON_XML_2000_FILENAME: typing.ClassVar[str] = ...
    EOPC04_2000_FILENAME: typing.ClassVar[str] = ...
    BULLETINB_2000_FILENAME: typing.ClassVar[str] = ...
    @staticmethod
    def addDefaultEOP1980HistoryLoaders(string: str, string2: str, string3: str, string4: str) -> None: ...
    @staticmethod
    def addDefaultEOP2000HistoryLoaders(string: str, string2: str, string3: str, string4: str) -> None: ...
    @staticmethod
    def addEOP1980HistoryLoader(eOP1980HistoryLoader: EOP1980HistoryLoader) -> None: ...
    @staticmethod
    def addEOP2000HistoryLoader(eOP2000HistoryLoader: EOP2000HistoryLoader) -> None: ...
    @staticmethod
    def clearEOP1980HistoryLoaders() -> None: ...
    @staticmethod
    def clearEOP2000HistoryLoaders() -> None: ...
    @typing.overload
    @staticmethod
    def getEOP1980History() -> 'EOP1980History': ...
    @typing.overload
    @staticmethod
    def getEOP1980History(eOPInterpolators: 'EOPInterpolators') -> 'EOP1980History': ...
    @typing.overload
    @staticmethod
    def getEOP2000History() -> 'EOP2000History': ...
    @typing.overload
    @staticmethod
    def getEOP2000History(eOPInterpolators: 'EOPInterpolators') -> 'EOP2000History': ...
    @typing.overload
    @staticmethod
    def getEOP2000History(eOPInterpolators: 'EOPInterpolators', eOP2000HistoryLoader: EOP2000HistoryLoader) -> 'EOP2000History': ...
    @typing.overload
    @staticmethod
    def getEOP2000HistoryConstant() -> 'EOP2000HistoryConstantOutsideInterval': ...
    @typing.overload
    @staticmethod
    def getEOP2000HistoryConstant(eOPInterpolators: 'EOPInterpolators') -> 'EOP2000HistoryConstantOutsideInterval': ...
    @typing.overload
    @staticmethod
    def getEOP2000HistoryConstant(eOPInterpolators: 'EOPInterpolators', eOP2000HistoryLoader: EOP2000HistoryLoader) -> 'EOP2000HistoryConstantOutsideInterval': ...

class EOPInterpolators(java.lang.Enum['EOPInterpolators']):
    """
    public enum EOPInterpolators extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPInterpolators`>
    
        This enumerate lists available interpolators for EOP data.
    """
    LAGRANGE4: typing.ClassVar['EOPInterpolators'] = ...
    LINEAR: typing.ClassVar['EOPInterpolators'] = ...
    def getInterpolationPoints(self) -> int:
        """
            Return the number of points to use in interpolation.
        
            Returns:
                the number of points to use in interpolation
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'EOPInterpolators':
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
    def values() -> typing.MutableSequence['EOPInterpolators']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (EOPInterpolators c : EOPInterpolators.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class NutationCorrection(java.io.Serializable):
    """
    public class NutationCorrection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Simple container class for nutation correction (IAU 1980) parameters.
    
        This class is a simple container, it does not provide any processing method.
    
        Also see:
            :meth:`~serialized`
    """
    NULL_CORRECTION: typing.ClassVar['NutationCorrection'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.NutationCorrection` NULL_CORRECTION
    
        Null correction (ddeps = 0, ddpsi = 0).
    
    """
    def __init__(self, double: float, double2: float): ...
    def getDX(self) -> float:
        """
            Get the δX :sub:`2000` parameter (radians).
        
            Returns:
                δX :sub:`2000` parameter (radians)
        
        
        """
        ...
    def getDY(self) -> float:
        """
            Get the δY :sub:`2000` parameter (radians).
        
            Returns:
                δY :sub:`2000` parameter (radians)
        
        
        """
        ...
    def getDdeps(self) -> float:
        """
            Get the δ&Delta;ε :sub:`1980` parameter.
        
            Returns:
                δ&Delta;ε :sub:`1980` parameter
        
        
        """
        ...
    def getDdpsi(self) -> float:
        """
            Get the δ&Delta;ψ :sub:`1980` parameter.
        
            Returns:
                δ&Delta;ψ :sub:`1980` parameter
        
        
        """
        ...

class PoleCorrection(java.io.Serializable):
    """
    public class PoleCorrection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Simple container class for pole correction parameters.
    
        This class is a simple container, it does not provide any processing method.
    
        Also see:
            :meth:`~serialized`
    """
    NULL_CORRECTION: typing.ClassVar['PoleCorrection'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection` NULL_CORRECTION
    
        Null correction (xp = 0, yp = 0).
    
    """
    def __init__(self, double: float, double2: float): ...
    def getXp(self) -> float:
        """
            Get the x :sub:`p` parameter.
        
            Returns:
                x :sub:`p` parameter
        
        
        """
        ...
    def getYp(self) -> float:
        """
            Get the y :sub:`p` parameter.
        
            Returns:
                y :sub:`p` parameter
        
        
        """
        ...

class AbstractEOPHistory(java.io.Serializable, EOPHistory):
    """
    public abstract class AbstractEOPHistory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
    
        This class loads any kind of Earth Orientation Parameter data throughout a large time range.
    
        Also see:
            :meth:`~serialized`
    """
    def addEntry(self, eOPEntry: EOPEntry) -> None:
        """
            Add an Earth Orientation Parameters entry.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.addEntry` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Parameters:
                entry (:class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPEntry`): entry to add
        
        
        """
        ...
    def checkEOPContinuity(self, double: float) -> None: ...
    @staticmethod
    def fillHistory(collection: typing.Union[java.util.Collection[EOPEntry], typing.Sequence[EOPEntry], typing.Set[EOPEntry]], eOPHistory: EOPHistory) -> None: ...
    def getEOPInterpolationMethod(self) -> EOPInterpolators:
        """
            Return the EOP interpolation method.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getEOPInterpolationMethod` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Returns:
                eop interpolation method
        
        
        """
        ...
    def getEndDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date of the last available Earth Orientation Parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getEndDate` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Returns:
                the end date of the available data
        
        
        """
        ...
    def getLOD(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the LoD (Length of Day) value.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getLOD` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the value is desired
        
            Returns:
                LoD in seconds (0 if date is outside covered range)
        
        
        """
        ...
    def getNutationCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> NutationCorrection:
        """
            Get the correction to the nutation parameters.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getNutationCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the correction is desired
        
            Returns:
                nutation correction (:meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.NutationCorrection.NULL_CORRECTION` if date
                is outside covered range)
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> PoleCorrection:
        """
            Get the pole IERS Reference Pole correction.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getPoleCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the correction is desired
        
            Returns:
                pole correction (:meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection.NULL_CORRECTION` if date is
                outside covered range)
        
        
        """
        ...
    def getStartDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date of the first available Earth Orientation Parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getStartDate` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Returns:
                the start date of the available data
        
        
        """
        ...
    def getUT1MinusTAI(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the UT1-TAI value.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getUT1MinusTAI` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the value is desired
        
            Returns:
                UT1-TAI in seconds (0 if date is outside covered range)
        
        
        """
        ...
    def getUT1MinusUTC(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the UT1-UTC value.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getUT1MinusUTC` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the value is desired
        
            Returns:
                UT1-UTC in seconds (0 if date is outside covered range)
        
        
        """
        ...
    def iterator(self) -> java.util.Iterator[fr.cnes.sirius.patrius.time.TimeStamped]: ...
    def size(self) -> int:
        """
            Get the number of entries in the history.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.size` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Returns:
                number of entries in the history
        
        
        """
        ...

class BulletinBFilesLoader(EOP1980HistoryLoader, EOP2000HistoryLoader):
    """
    public class BulletinBFilesLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP1980HistoryLoader`, :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP2000HistoryLoader`
    
        Loader for bulletin B files.
    
        Bulletin B files contain :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPEntry` for a few months periods.
    
        The bulletin B files are recognized thanks to their base names, which must match one of the the patterns
        :code:`bulletinb_IAU2000-###.txt`, :code:`bulletinb_IAU2000.###`, :code:`bulletinb-###.txt` or :code:`bulletinb.###` (or
        the same ending with :code:`.gz` for gzip-compressed files) where # stands for a digit character. The files with
        IAU_2000 in their names correspond to the IAU-2000 precession-nutation model wheareas the files without any identifier
        correspond to the IAU-1980 precession-nutation model.
    
        Note that since early 2010, IERS has ceased publication of bulletin B for both precession-nutation models from its `
        main site <http://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html>`. The files for IAU-1980 only are
        still available from `Paris-Meudon observatory site <http://hpiers.obspm.fr/eoppc/bul/bulb_new/>` in a new format (but
        with the same name pattern :code:`bulletinb.###`). This class handles both the old and the new format and takes care to
        use the new format only for the IAU-2000 precession-nutation model.
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def fillHistory(self, eOP1980History: 'EOP1980History') -> None: ...
    @typing.overload
    def fillHistory(self, eOP2000History: 'EOP2000History') -> None: ...
    @typing.overload
    def fillHistory(self, eOP2000History: 'EOP2000History', inputStream: java.io.InputStream) -> None: ...
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

class EOP1980Entry(EOPEntry):
    """
    public class EOP1980Entry extends :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPEntry`
    
        This class holds an Earth Orientation Parameters entry (IAU1980).
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, dtType: EOPEntry.DtType): ...
    @typing.overload
    def __init__(self, dateComponents: fr.cnes.sirius.patrius.time.DateComponents, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, dateComponents: fr.cnes.sirius.patrius.time.DateComponents, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, dtType: EOPEntry.DtType): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, dtType: EOPEntry.DtType): ...

class EOP2000Entry(EOPEntry):
    """
    public class EOP2000Entry extends :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPEntry`
    
        This class holds an Earth Orientation Parameters entry (IAU2000).
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, dtType: EOPEntry.DtType): ...
    @typing.overload
    def __init__(self, dateComponents: fr.cnes.sirius.patrius.time.DateComponents, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, dateComponents: fr.cnes.sirius.patrius.time.DateComponents, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, dtType: EOPEntry.DtType): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, int: int, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, dtType: EOPEntry.DtType): ...

class EOPC04FilesLoader(EOP1980HistoryLoader, EOP2000HistoryLoader):
    """
    public class EOPC04FilesLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP1980HistoryLoader`, :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP2000HistoryLoader`
    
        Loader for EOP 05 C04 files.
    
        EOP 05 C04 files contain :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPEntry` consistent with ITRF2005 for
        one year periods.
    
        The EOP 05 C04 files are recognized thanks to their base names, which must match one of the the patterns
        :code:`eopc04_IAU2000.##` or :code:`eopc04.##` (or the same ending with :code:`.gz` for gzip-compressed files) where #
        stands for a digit character.
    
        Between 2002 and 2007, another series of Earth Orientation Parameters was in use: EOPC04 (without the 05). These
        parameters were consistent with the previous ITRS realization: ITRF2000. These files are no longer provided by IERS and
        only 6 files covering the range 2002 to 2007 were generated. The content of these files is not the same as the content
        of the new files supported by this class, however IERS uses the same file naming convention for both. If a file from the
        older series is found by this class, a parse error will be triggered. Users must remove such files to avoid being lured
        in believing they do have EOP data.
    
        Files containing old data (back to 1962) have been regenerated in the new file format and are available at IERS web
        site: `Index of /iers/eop/eopc04_05 <http://hpiers.obspm.fr/iers/eop/eopc04_05/>`.
    """
    def __init__(self, string: str): ...
    @typing.overload
    @staticmethod
    def fillHistory(eOP1980History: 'EOP1980History', inputStream: java.io.InputStream) -> None: ...
    @typing.overload
    @staticmethod
    def fillHistory(eOP2000History: 'EOP2000History', inputStream: java.io.InputStream) -> None: ...
    @typing.overload
    def fillHistory(self, eOP1980History: 'EOP1980History') -> None: ...
    @typing.overload
    def fillHistory(self, eOP2000History: 'EOP2000History') -> None: ...
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

class NoEOP1980HistoryLoader(EOP1980HistoryLoader):
    """
    public class NoEOP1980HistoryLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP1980HistoryLoader`
    
        NoEOP2000History. In order to use this class, the user must use the loader in the EOPHistoryFactory :
    
        .. code-block: java
        
        
         final EOP1980HistoryLoader loader = new NoEOP1980HistoryLoader();
         EOPHistoryFactory.addEOP1980HistoryLoader(loader);
         
    
        Since:
            2.2
    """
    def __init__(self): ...
    def fillHistory(self, eOP1980History: 'EOP1980History') -> None: ...
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

class RapidDataAndPredictionColumnsLoader(EOP1980HistoryLoader, EOP2000HistoryLoader):
    """
    public class RapidDataAndPredictionColumnsLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP1980HistoryLoader`, :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP2000HistoryLoader`
    
        Loader for IERS rapid data and prediction files in columns format (finals file).
    
        Rapid data and prediction files contain :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPEntry` for several
        years periods, in one file only that is updated regularly.
    
        These files contain both the data from IERS Bulletin A and IERS bulletin B. This class parses only the part from
        Bulletin A.
    
        The rapid data and prediction file is recognized thanks to its base name, which must match one of the the patterns
        :code:`finals.*` or :code:`finals2000A.*` (or the same ending with :code:`.gz` for gzip-compressed files) where * stands
        for a word like "all", "daily", or "data". The file with 2000A in their name correspond to the IAU-2000
        precession-nutation model whereas the files without any identifier correspond to the IAU-1980 precession-nutation model.
        The files with the all suffix start from 1973-01-01, the file with the data suffix start from 1992-01-01 and the files
        with the daily suffix.
    
        Also see:
            `file format description at USNO <http://maia.usno.navy.mil/ser7/readme.finals2000A>`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def fillHistory(self, eOP1980History: 'EOP1980History') -> None: ...
    @typing.overload
    def fillHistory(self, eOP2000History: 'EOP2000History') -> None: ...
    @typing.overload
    def fillHistory(self, eOP2000History: 'EOP2000History', inputStream: java.io.InputStream) -> None: ...
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

class RapidDataAndPredictionXMLLoader(EOP1980HistoryLoader, EOP2000HistoryLoader):
    """
    public class RapidDataAndPredictionXMLLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP1980HistoryLoader`, :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP2000HistoryLoader`
    
        Loader for IERS rapid data and prediction file in XML format (finals file).
    
        Rapid data and prediction file contain :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPEntry` for several
        years periods, in one file only that is updated regularly.
    
        The XML EOP files are recognized thanks to their base names, which must match one of the the patterns
        :code:`finals.2000A.*.xml` or :code:`finals.*.xml` (or the same ending with :code:`.gz` for gzip-compressed files) where
        * stands for a word like "all", "daily", or "data".
    
        Files containing data (back to 1973) are available at IERS web site: `Earth orientation data
        <http://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html>`.
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def fillHistory(self, eOP1980History: 'EOP1980History') -> None: ...
    @typing.overload
    def fillHistory(self, eOP2000History: 'EOP2000History') -> None: ...
    @typing.overload
    def fillHistory(self, eOP2000History: 'EOP2000History', inputStream: java.io.InputStream) -> None: ...
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

class EOP1980History(AbstractEOPHistory):
    """
    public class EOP1980History extends :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
    
        This class holds Earth Orientation Parameters (IAU1980) data throughout a large time range.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, eOPInterpolators: EOPInterpolators): ...
    @typing.overload
    @staticmethod
    def fillHistory(collection: typing.Union[java.util.Collection[EOPEntry], typing.Sequence[EOPEntry], typing.Set[EOPEntry]], eOPHistory: EOPHistory) -> None: ...
    @typing.overload
    @staticmethod
    def fillHistory(collection: typing.Union[java.util.Collection[EOP1980Entry], typing.Sequence[EOP1980Entry], typing.Set[EOP1980Entry]], eOP1980History: 'EOP1980History') -> None: ...

class EOP2000History(AbstractEOPHistory):
    """
    public class EOP2000History extends :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
    
        This class holds Earth Orientation Parameters (IAU2000) data throughout a large time range.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, eOPInterpolators: EOPInterpolators): ...
    @typing.overload
    @staticmethod
    def fillHistory(collection: typing.Union[java.util.Collection[EOPEntry], typing.Sequence[EOPEntry], typing.Set[EOPEntry]], eOPHistory: EOPHistory) -> None: ...
    @typing.overload
    @staticmethod
    def fillHistory(collection: typing.Union[java.util.Collection[EOP2000Entry], typing.Sequence[EOP2000Entry], typing.Set[EOP2000Entry]], eOP2000History: 'EOP2000History') -> None: ...
    def isActive(self) -> bool:
        """
            Returns true if EOP are computed.
        
            Returns:
                true if EOP are computed
        
        
        """
        ...

class EOP2000HistoryConstantOutsideInterval(EOP2000History):
    """
    public class EOP2000HistoryConstantOutsideInterval extends :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP2000History`
    
        This class extends the EOP data outside of the historic definition interval. Outside of this interval the value
        corresponding to the closest bound will be returned.
    
        Warning: as the UT1-TAI remains constant the (UT1-UTC) absolute value may become higher than 0.9 second depending on
        leap seconds (for UTC time scale) existing outside this interval.
    
        Since:
            version 3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, eOPInterpolators: EOPInterpolators): ...
    def getEndDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Description copied from class: :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getEndDate`
            Get the date of the last available Earth Orientation Parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getEndDate` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getEndDate` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Returns:
                the end date of the available data
        
        
        """
        ...
    def getLOD(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the LoD (Length of Day) value.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getLOD` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getLOD` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the value is desired
        
            Returns:
                LoD in seconds if date is within history interval bounds. If date is outside history interval bounds value corresponding
                to closest bound is returned
        
        
        """
        ...
    def getNutationCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> NutationCorrection:
        """
            Get the correction to the nutation parameters.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getNutationCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getNutationCorrection` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the correction is desired
        
            Returns:
                nutation correction to be applied if date is within history interval bounds. If date is outside history interval bounds
                value corresponding to closest bound is returned
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> PoleCorrection:
        """
            Get the pole IERS Reference Pole correction.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getPoleCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getPoleCorrection` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the correction is desired
        
            Returns:
                pole correction to be applied if date is within history interval bounds. If date is outside history interval bounds
                value corresponding to closest bound is returned
        
        
        """
        ...
    def getStartDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Description copied from class: :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getStartDate`
            Get the date of the first available Earth Orientation Parameters.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getStartDate` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getStartDate` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Returns:
                the start date of the available data
        
        
        """
        ...
    def getUT1MinusTAI(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the UT1-TAI value.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getUT1MinusTAI` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getUT1MinusTAI` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the value is desired
        
            Returns:
                UT1-TAI in seconds if date is within history interval bounds. If date is outside history interval bounds value
                corresponding to closest bound is returned
        
        
        """
        ...
    def getUT1MinusUTC(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the UT1-UTC value.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getUT1MinusUTC` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getUT1MinusUTC` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the value is desired
        
            Returns:
                UT1-UTC in seconds if date is within history interval bounds. If date is outside history interval bounds value
                corresponding to closest bound is returned. As the UT1-TAI remains constant the (UT1-UTC) absolute value may become
                higher than 0.9 second depending on leap seconds (for UTC time scale) existing outside this interval.
        
        
        """
        ...

class NoEOP2000History(EOP2000History):
    """
    public final class NoEOP2000History extends :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP2000History`
    
        NoEOP2000History.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getEOPInterpolationMethod(self) -> EOPInterpolators:
        """
            EOPInterpolators.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getEOPInterpolationMethod` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getEOPInterpolationMethod` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Returns:
                0
        
        
        """
        ...
    def getEndDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            getEndDate.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getEndDate` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getEndDate` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Returns:
                FUTURE_INFINITY
        
        
        """
        ...
    def getLOD(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            getLOD.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getLOD` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getLOD` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                0
        
        
        """
        ...
    def getNutationCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> NutationCorrection:
        """
            Get the correction to the nutation parameters.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getNutationCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getNutationCorrection` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the correction is desired
        
            Returns:
                nutation correction (:meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.NutationCorrection.NULL_CORRECTION` if date
                is outside covered range)
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> PoleCorrection:
        """
            Get the pole IERS Reference Pole correction.
        
            The data provided comes from the IERS files. It is smoothed data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getPoleCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getPoleCorrection` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the correction is desired
        
            Returns:
                pole correction (:meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection.NULL_CORRECTION` if date is
                outside covered range)
        
        
        """
        ...
    def getStartDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            getStartDate.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getStartDate` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getStartDate` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Returns:
                PAST_INFINITY
        
        
        """
        ...
    def getUT1MinusTAI(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            getUT1MinusTAI.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.getUT1MinusTAI` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.getUT1MinusTAI` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                0
        
        
        """
        ...
    def isActive(self) -> bool:
        """
            Returns true if EOP are computed.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP2000History.isActive` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOP2000History`
        
            Returns:
                true if EOP are computed
        
        
        """
        ...
    def iterator(self) -> java.util.Iterator[fr.cnes.sirius.patrius.time.TimeStamped]: ...
    def size(self) -> int:
        """
            size.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory.size` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory.size` in
                class :class:`~fr.cnes.sirius.patrius.frames.configuration.eop.AbstractEOPHistory`
        
            Returns:
                0
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.frames.configuration.eop")``.

    AbstractEOPHistory: typing.Type[AbstractEOPHistory]
    BulletinBFilesLoader: typing.Type[BulletinBFilesLoader]
    EOP1980Entry: typing.Type[EOP1980Entry]
    EOP1980History: typing.Type[EOP1980History]
    EOP1980HistoryLoader: typing.Type[EOP1980HistoryLoader]
    EOP2000Entry: typing.Type[EOP2000Entry]
    EOP2000History: typing.Type[EOP2000History]
    EOP2000HistoryConstantOutsideInterval: typing.Type[EOP2000HistoryConstantOutsideInterval]
    EOP2000HistoryLoader: typing.Type[EOP2000HistoryLoader]
    EOPC04FilesLoader: typing.Type[EOPC04FilesLoader]
    EOPEntry: typing.Type[EOPEntry]
    EOPHistory: typing.Type[EOPHistory]
    EOPHistoryFactory: typing.Type[EOPHistoryFactory]
    EOPInterpolators: typing.Type[EOPInterpolators]
    NoEOP1980HistoryLoader: typing.Type[NoEOP1980HistoryLoader]
    NoEOP2000History: typing.Type[NoEOP2000History]
    NutationCorrection: typing.Type[NutationCorrection]
    PoleCorrection: typing.Type[PoleCorrection]
    RapidDataAndPredictionColumnsLoader: typing.Type[RapidDataAndPredictionColumnsLoader]
    RapidDataAndPredictionXMLLoader: typing.Type[RapidDataAndPredictionXMLLoader]
