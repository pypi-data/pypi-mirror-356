
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames.configuration.eop
import fr.cnes.sirius.patrius.frames.configuration.libration
import fr.cnes.sirius.patrius.frames.configuration.modprecession
import fr.cnes.sirius.patrius.frames.configuration.precessionnutation
import fr.cnes.sirius.patrius.frames.configuration.sp
import fr.cnes.sirius.patrius.frames.configuration.tides
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import typing



class DiurnalRotation(java.io.Serializable):
    """
    public class DiurnalRotation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class contains the different ut1-utc corrections (libration, tidal effects).
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, tidalCorrectionModel: fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel, librationCorrectionModel: fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel): ...
    def getLibrationCorrectionModel(self) -> fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel:
        """
        
            Returns:
                the libration model
        
        
        """
        ...
    def getTidalCorrectionModel(self) -> fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel:
        """
        
            Returns:
                the tidal model
        
        
        """
        ...
    def getUT1Correction(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute ut1-tai correction.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for which one we want to compute the correction
        
            Returns:
                ut1-tai correction as a double
        
        
        """
        ...

class FrameConvention(java.lang.Enum['FrameConvention']):
    """
    public enum FrameConvention extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.frames.configuration.FrameConvention`>
    
        IERS conventions enumeration.
    
        Since:
            3.3
    """
    IERS2003: typing.ClassVar['FrameConvention'] = ...
    IERS2010: typing.ClassVar['FrameConvention'] = ...
    STELA: typing.ClassVar['FrameConvention'] = ...
    NONE: typing.ClassVar['FrameConvention'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'FrameConvention':
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
    def values() -> typing.MutableSequence['FrameConvention']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (FrameConvention c : FrameConvention.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class FramesConfiguration(java.io.Serializable):
    """
    public interface FramesConfiguration extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface providing the basic services for frame configurations.
    
        Since:
            1.2
    """
    def getCIPCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.precessionnutation.CIPCoordinates:
        """
            Compute the corrected Celestial Intermediate Pole motion (X, Y, S, Xdot, Ydot, Sdot) in the GCRS.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for which one the CIP motion is computed.
        
            Returns:
                X, Y, S, Xdot, Ydot, Sdot
        
        
        """
        ...
    def getCIRFPrecessionNutationModel(self) -> fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutation:
        """
            Get the CIRF precession nutation model.
        
            Returns:
                the CIRF precession nutation model
        
        
        """
        ...
    def getDiurnalRotationModel(self) -> DiurnalRotation:
        """
            Get the diurnal rotation model.
        
            Returns:
                the diurnal rotation model
        
        
        """
        ...
    def getEOPHistory(self) -> fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory:
        """
            Get the EOP history.
        
            Returns:
                the EOP history
        
        
        """
        ...
    def getEOPInterpolationMethod(self) -> fr.cnes.sirius.patrius.frames.configuration.eop.EOPInterpolators:
        """
            Return the EOP interpolation method.
        
            Returns:
                eop interpolation method
        
        
        """
        ...
    def getEarthObliquity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Getter for the Earth obliquity at provided date used in MOD to Ecliptic MOD transformation.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                the Earth obliquity at provided date used in MOD to Ecliptic MOD transformation
        
        
        """
        ...
    def getMODPrecession(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation:
        """
            Getter for the MOD precession transformation from GCRF/EME2000 to MOD at provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                the MOD precession rotation from GCRF/EME2000 to MOD at provided date
        
        
        """
        ...
    def getMODPrecessionModel(self) -> fr.cnes.sirius.patrius.frames.configuration.modprecession.MODPrecessionModel:
        """
            Get the MOD precession model.
        
            Returns:
                the MOD precession model
        
        
        """
        ...
    def getPolarMotion(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection: ...
    def getPolarMotionModel(self) -> 'PolarMotion':
        """
            Get the polar motion model.
        
            Returns:
                the pola motion model
        
        
        """
        ...
    def getSprime(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute S' value.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for which one S prime is computed
        
            Returns:
                s'
        
        
        """
        ...
    def getTimeIntervalOfValidity(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Time interval of validity for the EOP files.
        
            Returns:
                time interval of validity as a :class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`
        
        
        """
        ...
    def getUT1Correction(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute correction dut1.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for which the correction is computed.
        
            Returns:
                dut1
        
        
        """
        ...
    def getUT1MinusTAI(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute corrected ut1-tai.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for which one the ut1-tai is computed.
        
            Returns:
                ut1-tai
        
        
        """
        ...

class FramesConfigurationBuilder:
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, framesConfiguration: FramesConfiguration): ...
    def getConfiguration(self) -> FramesConfiguration: ...
    def setCIRFPrecessionNutation(self, precessionNutation: fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutation) -> None: ...
    def setDiurnalRotation(self, diurnalRotation: DiurnalRotation) -> None: ...
    def setEOPHistory(self, eOPHistory: fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory) -> None: ...
    def setMODPrecession(self, mODPrecessionModel: fr.cnes.sirius.patrius.frames.configuration.modprecession.MODPrecessionModel) -> None: ...
    def setPolarMotion(self, polarMotion: 'PolarMotion') -> None: ...

class FramesConfigurationFactory:
    """
    public final class FramesConfigurationFactory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Frames configuration factory. Contains useful configurations.
    
        Since:
            1.3
    """
    @staticmethod
    def getIERS2003Configuration(boolean: bool) -> FramesConfiguration:
        """
            Gets the default IERS2003 configuration (always the same instance, not a new one).
        
            Parameters:
                ignoreTides (boolean): tides if tides are to be ignored, false otherwise
        
            Returns:
                default IERS2003 configuration
        
        
        """
        ...
    @staticmethod
    def getIERS2010Configuration() -> FramesConfiguration:
        """
            Gets the default IERS2010 configuration (always the same instance, not a new one).
        
            Returns:
                default IERS2010 configuration
        
        
        """
        ...
    @staticmethod
    def getSimpleConfiguration(boolean: bool) -> FramesConfiguration:
        """
            Gets a simple configuration (always the same instance, not a new one). It contains only an optional precession /
            nutation model :code:`PrecessionNutationModelFactory#PN_IERS2010_INTERPOLATED_NON_CONSTANT` without use of EOP data.
            This configuration is useful if you don't want to provide or don't have EOP data while keeping good model accuracy.
            Particularly this configuration always returns TIRF = ITRF.
        
            Parameters:
                usePrecessionNutationModel (boolean): true if default IERS precession-nutation model should be used (without any need for additional data), false if no
                    precession-nutation model shall be used (in this case CIRF frame = GCRF frame)
        
            Returns:
                simple frame configuration
        
        
        """
        ...
    @staticmethod
    def getStelaConfiguration() -> FramesConfiguration:
        """
            Gets the official STELA configuration (always the same instance, not a new one).
        
            Returns:
                official STELA configuration
        
        
        """
        ...

class PolarMotion(java.io.Serializable):
    """
    public class PolarMotion extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class contains the different polar motion corrections (libration, tidal effects, sp correction).
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, boolean: bool, tidalCorrectionModel: fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel, librationCorrectionModel: fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel, sPrimeModel: fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel): ...
    def getLibrationCorrectionModel(self) -> fr.cnes.sirius.patrius.frames.configuration.libration.LibrationCorrectionModel:
        """
        
            Returns:
                the libration model
        
        
        """
        ...
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection: ...
    def getSP(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute S'.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for which the s' quantity is computed
        
            Returns:
                s' as a double
        
        
        """
        ...
    def getSPrimeModel(self) -> fr.cnes.sirius.patrius.frames.configuration.sp.SPrimeModel:
        """
        
            Returns:
                the sp model
        
        
        """
        ...
    def getTidalCorrectionModel(self) -> fr.cnes.sirius.patrius.frames.configuration.tides.TidalCorrectionModel:
        """
        
            Returns:
                the tidal model
        
        
        """
        ...
    def useEopData(self) -> bool:
        """
            Use EOP pole correction data.
        
            Returns:
                true if EOP data is to be used, flase if not.
        
        
        """
        ...

class FramesConfigurationImplementation(FramesConfiguration):
    """
    public class FramesConfigurationImplementation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
    
        This class represents a frames configuration.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def getCIPCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.precessionnutation.CIPCoordinates:
        """
            Compute the corrected Celestial Intermediate Pole motion (X, Y, S, Xdot, Ydot, Sdot) in the GCRS.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getCIPCoordinates` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for which one the CIP motion is computed.
        
            Returns:
                X, Y, S, Xdot, Ydot, Sdot
        
        
        """
        ...
    def getCIRFPrecessionNutationModel(self) -> fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutation:
        """
            Get the CIRF precession nutation model.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getCIRFPrecessionNutationModel` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Returns:
                the CIRF precession nutation model
        
        
        """
        ...
    def getDiurnalRotationModel(self) -> DiurnalRotation:
        """
            Get the diurnal rotation model.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getDiurnalRotationModel` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Returns:
                the diurnal rotation model
        
        
        """
        ...
    def getEOPHistory(self) -> fr.cnes.sirius.patrius.frames.configuration.eop.EOPHistory:
        """
            Get the EOP history.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getEOPHistory` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Returns:
                the EOP history
        
        
        """
        ...
    def getEOPInterpolationMethod(self) -> fr.cnes.sirius.patrius.frames.configuration.eop.EOPInterpolators:
        """
            Return the EOP interpolation method.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getEOPInterpolationMethod` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Returns:
                eop interpolation method
        
        
        """
        ...
    def getEarthObliquity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Getter for the Earth obliquity at provided date used in MOD to Ecliptic MOD transformation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getEarthObliquity` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                the Earth obliquity at provided date used in MOD to Ecliptic MOD transformation
        
        
        """
        ...
    def getMODPrecession(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation:
        """
            Getter for the MOD precession transformation from GCRF/EME2000 to MOD at provided date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getMODPrecession` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                the MOD precession rotation from GCRF/EME2000 to MOD at provided date
        
        
        """
        ...
    def getMODPrecessionModel(self) -> fr.cnes.sirius.patrius.frames.configuration.modprecession.MODPrecessionModel:
        """
            Get the MOD precession model.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getMODPrecessionModel` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Returns:
                the MOD precession model
        
        
        """
        ...
    def getPolarMotion(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection: ...
    def getPolarMotionModel(self) -> PolarMotion:
        """
            Get the polar motion model.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getPolarMotionModel` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Returns:
                the pola motion model
        
        
        """
        ...
    def getSprime(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute S' value.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getSprime` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for which one S prime is computed
        
            Returns:
                s'
        
        
        """
        ...
    def getTimeIntervalOfValidity(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Time interval of validity for the EOP files.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getTimeIntervalOfValidity` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Returns:
                time interval of validity as a :class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`
        
        
        """
        ...
    def getUT1Correction(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute correction dut1.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getUT1Correction` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for which the correction is computed.
        
            Returns:
                dut1
        
        
        """
        ...
    def getUT1MinusTAI(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute corrected ut1-tai.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration.getUT1MinusTAI` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for which one the ut1-tai is computed.
        
            Returns:
                ut1-tai
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.frames.configuration")``.

    DiurnalRotation: typing.Type[DiurnalRotation]
    FrameConvention: typing.Type[FrameConvention]
    FramesConfiguration: typing.Type[FramesConfiguration]
    FramesConfigurationBuilder: typing.Type[FramesConfigurationBuilder]
    FramesConfigurationFactory: typing.Type[FramesConfigurationFactory]
    FramesConfigurationImplementation: typing.Type[FramesConfigurationImplementation]
    PolarMotion: typing.Type[PolarMotion]
    eop: fr.cnes.sirius.patrius.frames.configuration.eop.__module_protocol__
    libration: fr.cnes.sirius.patrius.frames.configuration.libration.__module_protocol__
    modprecession: fr.cnes.sirius.patrius.frames.configuration.modprecession.__module_protocol__
    precessionnutation: fr.cnes.sirius.patrius.frames.configuration.precessionnutation.__module_protocol__
    sp: fr.cnes.sirius.patrius.frames.configuration.sp.__module_protocol__
    tides: fr.cnes.sirius.patrius.frames.configuration.tides.__module_protocol__
