
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames.configuration
import fr.cnes.sirius.patrius.frames.configuration.eop
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import typing



class TidalCorrection(fr.cnes.sirius.patrius.time.TimeStamped, java.io.Serializable):
    """
    public final class TidalCorrection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class represents a Pole, UT1-TAI and length of day correction set for a given date.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, poleCorrection: fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection, double: float, double2: float): ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate`
            Get the date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                the date
        
        
        """
        ...
    def getLODCorrection(self) -> float:
        """
            Get the length of day correction.
        
            Returns:
                lod correction
        
        
        """
        ...
    def getPoleCorrection(self) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection:
        """
        
            Returns:
                the pole correction data
        
        
        """
        ...
    def getUT1Correction(self) -> float:
        """
            Returns the UT1-TAI correction.
        
            Returns:
                the UT1-TAI correction (seconds)
        
        
        """
        ...

class TidalCorrectionGenerator(fr.cnes.sirius.patrius.time.TimeStampedGenerator[TidalCorrection]):
    """
    public class TidalCorrectionGenerator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStampedGenerator`<:class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrection`>
    
        Tidal corrections generator for the TimeStampedCache.
    
        Since:
            1.3
    
        Also see:
            :code:`TidalCorrectionCache`, :meth:`~serialized`
    """
    def generate(self, tidalCorrection: TidalCorrection, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.List[TidalCorrection]: ...

class TidalCorrectionModel(java.io.Serializable):
    """
    public interface TidalCorrectionModel extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface provides the pole corrections as well as the UT1-TAI corrections due to tidal effects.
    
        Since:
            1.2
    """
    def getLODCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get length of day correction.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                length of day correction (in secs)
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection:
        """
            Compute the pole corrections at a given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                pole correction
        
        
        """
        ...
    def getUT1Correction(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the UT1-TAI corrections at a given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                UT1-TAI corrections
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Returns true if model uses direct computation, false if interpolated computation.
        
            Returns:
                true if model uses direct computation, false if interpolated computation
        
        
        """
        ...

class TidalCorrectionModelFactory:
    """
    public final class TidalCorrectionModelFactory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Factory for predefined models.
    
        Since:
            1.3
    """
    NO_TIDE: typing.ClassVar[TidalCorrectionModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel` NO_TIDE
    
        Ignore tidal effects.
    
    """
    TIDE_IERS2010_INTERPOLATED: typing.ClassVar[TidalCorrectionModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel` TIDE_IERS2010_INTERPOLATED
    
        IERS 2010 with interpolation.
    
    """
    TIDE_IERS2003_INTERPOLATED: typing.ClassVar[TidalCorrectionModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel` TIDE_IERS2003_INTERPOLATED
    
        IERS 2003 with interpolation.
    
    """
    TIDE_IERS2010_DIRECT: typing.ClassVar[TidalCorrectionModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel` TIDE_IERS2010_DIRECT
    
        IERS 2010 without interpolation.
    
    """
    TIDE_IERS2003_DIRECT: typing.ClassVar[TidalCorrectionModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel` TIDE_IERS2003_DIRECT
    
        IERS 2003 without interpolation.
    
    """

class IERS2003TidalCorrection(TidalCorrectionModel):
    """
    public class IERS2003TidalCorrection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
    
        Compute tidal correction to the pole motion.
    
        This class computes the diurnal and semidiurnal variations in the Earth orientation. It is a java translation of the
        fortran subroutine found at ftp://tai.bipm.org/iers/conv2003 /chapter8/ortho_eop.f.
    
        This class has been adapted from the TidalCorrection Orekit class.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getLODCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get length of day correction.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getLODCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                length of day correction (in secs)
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection:
        """
            Compute the pole corrections at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getPoleCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                pole correction
        
        
        """
        ...
    def getUT1Correction(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the UT1-TAI corrections at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getUT1Correction` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                UT1-TAI corrections
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Returns true if model uses direct computation, false if interpolated computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.isDirect` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Returns:
                true if model uses direct computation, false if interpolated computation
        
        
        """
        ...

class IERS2010TidalCorrection(TidalCorrectionModel):
    """
    public class IERS2010TidalCorrection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
    
    
        This class applies the integral Ray model (71 tidal waves) and Brzezinski-Mathews-Bretagnon-Capitaine-Bizouard model (10
        lunisolar waves) of the semidiurnal/diurnal variations in the Earth's orientation as recommended in the IERS 2003
        Conventions (McCarthy, 2002).
    
        This class is adapted for the fortran routine `PMUT1_OCEANS <http://hpiers.obspm.fr/iers/models/interp.f>`.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`, :code:`TidalCorrectionCache`,
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getLODCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get length of day correction.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getLODCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                length of day correction (in secs)
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection:
        """
            Compute the pole corrections at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getPoleCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                pole correction
        
        
        """
        ...
    def getUT1Correction(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the UT1-TAI corrections at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getUT1Correction` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                UT1-TAI corrections
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Returns true if model uses direct computation, false if interpolated computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.isDirect` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Returns:
                true if model uses direct computation, false if interpolated computation
        
        
        """
        ...

class NoTidalCorrection(TidalCorrectionModel):
    """
    public class NoTidalCorrection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
    
        This class ignores the tidal effects.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getLODCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get length of day correction.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getLODCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                length of day correction (in secs)
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection:
        """
            Compute the pole corrections at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getPoleCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                pole correction
        
        
        """
        ...
    def getUT1Correction(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the UT1-TAI corrections at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getUT1Correction` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                UT1-TAI corrections
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Returns true if model uses direct computation, false if interpolated computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.isDirect` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Returns:
                true if model uses direct computation, false if interpolated computation
        
        
        """
        ...

class TidalCorrectionPerThread(TidalCorrectionModel):
    """
    public abstract class TidalCorrectionPerThread extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
    
        Provides per-thread TidalCorrectionModel.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getLODCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get length of day correction.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getLODCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                length of day correction (in secs)
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection:
        """
            Compute the pole corrections at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getPoleCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                pole correction
        
        
        """
        ...
    def getUT1Correction(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the UT1-TAI corrections at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.getUT1Correction` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                UT1-TAI corrections
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Returns true if model uses direct computation, false if interpolated computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel.isDirect` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel`
        
            Returns:
                true if model uses direct computation, false if interpolated computation
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.frames.configuration.tides")``.

    IERS2003TidalCorrection: typing.Type[IERS2003TidalCorrection]
    IERS2010TidalCorrection: typing.Type[IERS2010TidalCorrection]
    NoTidalCorrection: typing.Type[NoTidalCorrection]
    TidalCorrection: typing.Type[TidalCorrection]
    TidalCorrectionGenerator: typing.Type[TidalCorrectionGenerator]
    TidalCorrectionModel: typing.Type[TidalCorrectionModel]
    TidalCorrectionModelFactory: typing.Type[TidalCorrectionModelFactory]
    TidalCorrectionPerThread: typing.Type[TidalCorrectionPerThread]
