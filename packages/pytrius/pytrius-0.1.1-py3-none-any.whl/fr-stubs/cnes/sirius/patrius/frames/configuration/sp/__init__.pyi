
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames.configuration
import fr.cnes.sirius.patrius.time
import java.io
import typing



class SPrimeModel(java.io.Serializable):
    """
    public interface SPrimeModel extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface provides the s' correction (used for the following transformation : TIRF -> ITRF).
    
        s is a quantity, named "TIO (Terrestrial Intermediate Origin) locator", which provides the position of the TIO on the
        equator of the CIP (Celestial Intermediate Pole) corresponding to the kinematical definition of the "non-rotating"
        origin (NRO) in the ITRS when the CIP is moving with respect to the ITRS due to polar motion. (see chapter 5.4.1 of the
        IERS Convention 2010)
    
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
    def getSP(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the correction S' at a given date.
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                correction S'
        
        
        """
        ...

class SPrimeModelFactory:
    """
    public final class SPrimeModelFactory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Factory for predefined models.
    
        Since:
            1.3
    """
    NO_SP: typing.ClassVar[SPrimeModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel` NO_SP
    
        Ignore SP correction.
    
    """
    SP_IERS2003: typing.ClassVar[SPrimeModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel` SP_IERS2003
    
        IERS 2003 convention.
    
    """
    SP_IERS2010: typing.ClassVar[SPrimeModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel` SP_IERS2010
    
        IERS 2010 convention.
    
    """

class IERS2003SPCorrection(SPrimeModel):
    """
    public class IERS2003SPCorrection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel`
    
        Compute s' correction (IERS 2003 convention).
    
        IERS 2003 convention exactly matches IERS 2010 convention. As a result this class returns exactly the same results as
        :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.IERS2010SPCorrection`.
    
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
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getSP(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the correction S' at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel.getSP` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                correction S'
        
        
        """
        ...

class IERS2010SPCorrection(SPrimeModel):
    """
    public class IERS2010SPCorrection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel`
    
        Compute s' correction.
    
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
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getSP(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the correction S' at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel.getSP` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                correction S'
        
        
        """
        ...

class NoSpCorrection(SPrimeModel):
    """
    public class NoSpCorrection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel`
    
        This class ignores the quantity s'.
    
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
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def getSP(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the correction S' at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel.getSP` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                correction S'
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.frames.configuration.sp")``.

    IERS2003SPCorrection: typing.Type[IERS2003SPCorrection]
    IERS2010SPCorrection: typing.Type[IERS2010SPCorrection]
    NoSpCorrection: typing.Type[NoSpCorrection]
    SPrimeModel: typing.Type[SPrimeModel]
    SPrimeModelFactory: typing.Type[SPrimeModelFactory]
