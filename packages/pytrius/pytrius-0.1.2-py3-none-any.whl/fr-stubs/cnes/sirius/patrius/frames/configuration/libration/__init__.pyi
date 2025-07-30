
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames.configuration
import fr.cnes.sirius.patrius.frames.configuration.eop
import fr.cnes.sirius.patrius.time
import java.io
import typing



class LibrationCorrectionModel(java.io.Serializable):
    """
    public interface LibrationCorrectionModel extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface provides the pole corrections as well as the ut1-utc corrections due to libration.
    
        Since:
            1.2
    """
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection: ...
    def getUT1Correction(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the UT1-TAI corrections at a given date.
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                ut1-tai corrections
        
        
        """
        ...

class LibrationCorrectionModelFactory:
    """
    public final class LibrationCorrectionModelFactory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Factory for predefined models.
    
        Since:
            1.3
    """
    NO_LIBRATION: typing.ClassVar[LibrationCorrectionModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel` NO_LIBRATION
    
        Ignore the libration effects.
    
    """
    LIBRATION_IERS2010: typing.ClassVar[LibrationCorrectionModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel` LIBRATION_IERS2010
    
        IERS 2010.
    
    """

class IERS2010LibrationCorrection(LibrationCorrectionModel):
    """
    public class IERS2010LibrationCorrection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel`
    
    
        This class computes the diurnal lunisolar effect. **It is a java translation of the fortran subroutine PM_GRAVI
        (provided by CNES and from IERS conventions, see chapter 5, tables 5.1a and 5.2a).**
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection: ...
    def getUT1Correction(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the dUT1 value. The correction is due to diurnal lunisolar effect.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel.getUT1Correction` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which the value is desired
        
            Returns:
                dUT1 in seconds
        
        
        """
        ...

class LibrationCorrectionPerThread(LibrationCorrectionModel):
    """
    public abstract class LibrationCorrectionPerThread extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel`
    
        Provides per-thread LibrationCorrectionModel.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection: ...
    def getUT1Correction(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the UT1-TAI corrections at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel.getUT1Correction` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                ut1-tai corrections
        
        
        """
        ...

class NoLibrationCorrection(LibrationCorrectionModel):
    """
    public class NoLibrationCorrection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel`
    
        This class ignores the libration effects.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection:
        """
            Compute the pole corrections at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel.getPoleCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel`
        
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
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel.getUT1Correction` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                ut1-tai corrections
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.frames.configuration.libration")``.

    IERS2010LibrationCorrection: typing.Type[IERS2010LibrationCorrection]
    LibrationCorrectionModel: typing.Type[LibrationCorrectionModel]
    LibrationCorrectionModelFactory: typing.Type[LibrationCorrectionModelFactory]
    LibrationCorrectionPerThread: typing.Type[LibrationCorrectionPerThread]
    NoLibrationCorrection: typing.Type[NoLibrationCorrection]
