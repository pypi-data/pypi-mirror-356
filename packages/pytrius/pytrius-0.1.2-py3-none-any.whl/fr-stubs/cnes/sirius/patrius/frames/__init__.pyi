
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes.directions
import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.frames.configuration
import fr.cnes.sirius.patrius.frames.transformations
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import typing



class Frame(fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider):
    """
    public class Frame extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
    
        Tridimensional references frames class.
    
        Frame Presentation
    ------------------
    
    
        This class is the base class for all frames in OREKIT. The frames are linked together in a tree with some specific frame
        chosen as the root of the tree. Each frame is defined by
        :class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` combining any number of translations and rotations
        from a reference frame which is its parent frame in the tree structure.
    
        When we say a :class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` t is *from frame :sub:`A` to frame
        :sub:`B`*, we mean that if the coordinates of some absolute vector (say the direction of a distant star for example) has
        coordinates u :sub:`A` in frame :sub:`A` and u :sub:`B` in frame :sub:`B` , then u :sub:`B`
        =:meth:`~fr.cnes.sirius.patrius.frames.transformations.Transform.transformVector`.
    
        The transforms may be constant or varying, depending on the implementation of the
        :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider` used to define the frame. For simple fixed
        transforms, using :class:`~fr.cnes.sirius.patrius.frames.transformations.FixedTransformProvider` is sufficient. For
        varying transforms (time-dependent or telemetry-based for example), it may be useful to define specific implementations
        of :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, frame: 'Frame', transform: fr.cnes.sirius.patrius.frames.transformations.Transform, string: str): ...
    @typing.overload
    def __init__(self, frame: 'Frame', transform: fr.cnes.sirius.patrius.frames.transformations.Transform, string: str, boolean: bool): ...
    @typing.overload
    def __init__(self, frame: 'Frame', transformProvider: fr.cnes.sirius.patrius.frames.transformations.TransformProvider, string: str): ...
    @typing.overload
    def __init__(self, frame: 'Frame', transformProvider: fr.cnes.sirius.patrius.frames.transformations.TransformProvider, string: str, boolean: bool): ...
    def getFirstCommonPseudoInertialAncestor(self, frame: 'Frame') -> 'Frame':
        """
            Returns the first pseudo-inertial common ancestor between this and provided frame. Except for
            :class:`~fr.cnes.sirius.patrius.frames.OrphanFrame`, it cannot be null since root frame is ICRF which is inertial.
        
            Parameters:
                frame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): a frame
        
            Returns:
                the first pseudo-inertial common ancestor between this and provided frame
        
        
        """
        ...
    def getFirstPseudoInertialAncestor(self) -> 'Frame':
        """
            Returns the first pseudo-inertial ancestor in the frame tree. Except for
            :class:`~fr.cnes.sirius.patrius.frames.OrphanFrame`, it cannot be null since root frame is ICRF which is inertial.
        
            Returns:
                the first pseudo-inertial ancestor, this if this is pseudo-inertial
        
        
        """
        ...
    @typing.overload
    def getFrozenFrame(self, frame: 'Frame', absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, string: str) -> 'Frame': ...
    @typing.overload
    def getFrozenFrame(self, frame: 'Frame', string: str) -> 'Frame': ...
    def getName(self) -> str:
        """
            Get the name.
        
            Returns:
                the name
        
        
        """
        ...
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'Frame': ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: 'Frame') -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getParent(self) -> 'Frame':
        """
            Get the parent frame.
        
            Returns:
                parent frame
        
        
        """
        ...
    def getTransformJacobian(self, frame: 'Frame', absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def getTransformProvider(self) -> fr.cnes.sirius.patrius.frames.transformations.TransformProvider:
        """
            Get the provider for transform from parent frame to instance.
        
            Returns:
                provider for transform from parent frame to instance
        
        
        """
        ...
    @typing.overload
    def getTransformTo(self, frame: 'Frame', absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def getTransformTo(self, frame: 'Frame', absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def getTransformTo(self, frame: 'Frame', absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def getTransformTo(self, frame: 'Frame', absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    def isChildOf(self, frame: 'Frame') -> bool:
        """
            Determine if a Frame is a child of another one.
        
            Parameters:
                potentialAncestor (:class:`~fr.cnes.sirius.patrius.frames.Frame`): supposed ancestor frame
        
            Returns:
                true if the potentialAncestor belongs to the path from instance to the root frame
        
        
        """
        ...
    def isPseudoInertial(self) -> bool:
        """
            Check if the frame is pseudo-inertial.
        
            Pseudo-inertial frames are frames that do have a linear motion and either do not rotate or rotate at a very low rate
            resulting in neglectible inertial forces. This means they are suitable for orbit definition and propagation using
            Newtonian mechanics. Frames that are *not* pseudo-inertial are *not* suitable for orbit definition and propagation.
        
            Warning: this notion depends on the horizon of propagation and the "level of inertiality of the frame". As a rule of
            thumb, precession/nutation effects of Earth frames such as CIRF/MOD are considered small enough on a horizon of a day to
            consider them pseudo-inertial.
        
            Returns:
                true if frame is pseudo-inertial
        
        
        """
        ...
    def setName(self, string: str) -> None:
        """
            Set frame name.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): frame name
        
        
        """
        ...
    def setReferential(self, frame: 'Frame') -> None: ...
    def toString(self) -> str:
        """
            New definition of the java.util toString() method.
        
            Overrides:
                 in class 
        
            Returns:
                the name
        
        
        """
        ...

class FramesFactory(java.io.Serializable):
    """
    public final class FramesFactory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Factory for predefined reference frames.
    
        FramesFactory Presentation
    --------------------------
    
    
        Several predefined reference frames are implemented in OREKIT. They are linked together in a tree with the
        *International Celestial Reference Frame* (ICRF) as the root of the tree. The IERS frames require a FramesConfiguration.
        If no configuration is specified by the user, a default one is used. The user can create a configuration with the
        :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfigurationBuilder`, and pass it to the
        :class:`~fr.cnes.sirius.patrius.frames.FramesFactory` with the
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.setConfiguration` method.
    
        Reference Frames
    ----------------
    
    
        The user can retrieve those reference frames using various static methods (
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getFrame`,
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getICRF`,
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getGCRF`,
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getCIRF`,
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getTIRF`,
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getITRF`,
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getEME2000`,
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getMOD`,
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getTOD`,
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getGTOD`,
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getITRFEquinox`,
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getTEME` and
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getVeis1950`).
    
        International Earth Rotation Service Frames
    -------------------------------------------
    
    
        The frames defined by the IERS are available, and are described in the IERS conventions (2010). The are fully
        configurable. Using the :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfigurationBuilder`, one can
        specify all models pertaining to the transformations between the IERS frames.
    
        This frame is used to define position on solid Earth. It rotates with the Earth and includes the pole motion with
        respect to Earth crust as provided by the :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`. Its
        pole axis is the IERS Reference Pole (IRP).
    
        Classical paradigm: equinox-based transformations
    -------------------------------------------------
    
    
        The classical paradigm used prior to IERS conventions 2003 is equinox based and uses more intermediate frames. Only some
        of these frames are supported in Orekit.
    
        Here is a schematic representation of the predefined reference frames tree:
    
        .. code-block: java
        
        
                                                             ICRF
                                                               │
                                                               │
                                                             GCRF
                                                               │
                                                      ┌────────┴────┬────────────────────┐
                                                      │             │     Frame bias     │
                                                      │             │                 EME2000
                                                      │             │                    │
                                                      │             │ Precession effects │
                Bias, Precession and Nutation effects │             │                    │
                  with or w/o EOP nutation correction │            MOD                  MOD  (Mean equator Of Date)
                                                      │             │             w/o EOP corrections
                                                      │     ┌───────┤  Nutation effects  ├───────────────────────────┐
            (Celestial Intermediate Reference Frame) CIRF   │       │                    │                           │
                                                      │     │      TOD                  TOD  (True equator Of Date)  │
                               Earth natural rotation │     │       │             w/o EOP corrections                │
                                                      │     │       │    Sidereal Time   │                           │
                                                      │     │       │                    │                           │
          (Terrestrial Intermediate Reference Frame) TIRF  EOD     GTOD                 GTOD  (Green. True Of Date) EOD
                                                      │                           w/o EOP corrections
                                          Pole motion │                                  │
                                                      │                                  ├────────────┬─────────────┐
                                                      │                                  │            │             │
         (International Terrestrial Reference Frame) ITRF                               ITRF        VEIS1950   G50 (Gamma 50)
                                                                                   equinox-based
         
         
    
        This is a utility class, so its constructor is private.
    
        Also see:
            :meth:`~serialized`
    """
    @staticmethod
    def clear() -> None:
        """
            Clear the frames tree.
        
            Caution: use this method carefully. It will clear the frames tree but does not remove objects from JVM.
        
        """
        ...
    @staticmethod
    def clearConfiguration() -> None:
        """
            Clear frames configuration. Unless a new frames configuration is later set,
            :meth:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfigurationFactory.getIERS2010Configuration` will be used by
            default.
        
        """
        ...
    @staticmethod
    def getCIRF() -> 'CelestialBodyFrame':
        """
            Get the CIRF reference frame.
        
            Returns:
                the selected reference frame singleton.
        
        
        """
        ...
    @staticmethod
    def getConfiguration() -> fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration:
        """
            Getter for the current configuration.
        
            Returns:
                configuration the current configuration
        
        
        """
        ...
    @staticmethod
    def getEMB() -> 'CelestialBodyFrame':
        """
            Get the unique Earth-Moon barycenter frame. It is aligned with GCRF and ICRF frame.
        
            Returns:
                the unique instance of the Earth-Moon barycenter frame
        
        
        """
        ...
    @staticmethod
    def getEME2000() -> 'CelestialBodyFrame':
        """
            Get the unique EME2000 frame.
        
            The EME2000 frame is also called the J2000 frame. The former denomination is preferred in PATRIUS.
        
            Returns:
                the unique instance of the EME2000 frame
        
        
        """
        ...
    @staticmethod
    def getEclipticJ2000() -> 'CelestialBodyFrame':
        """
        
            This class implements the Ecliptic J2000 frame.
            See "Astronomical Algorithms", chapter 24 "Solar Coordinates", Jean Meeus, 1991.
        
            Returns:
                the EclipticJ2000 frame
        
        
        """
        ...
    @staticmethod
    def getEclipticMOD(boolean: bool) -> 'CelestialBodyFrame':
        """
        
            This class implements the Ecliptic MOD frame (mean ecliptic and equinox of the epoch) (formerly called EOD).
        
            Parameters:
                applyEOPCorr (boolean): true to take into account EOP corrections
        
            Returns:
                the Ecliptic MOD frame
        
        
        """
        ...
    @staticmethod
    def getFrame(predefinedFrameType: 'PredefinedFrameType') -> Frame: ...
    @staticmethod
    def getG50() -> 'CelestialBodyFrame': ...
    @staticmethod
    def getGCRF() -> 'CelestialBodyFrame':
        """
            Get the unique GCRF frame.
        
            Returns:
                the unique instance of the GCRF frame
        
        
        """
        ...
    @staticmethod
    def getGTOD(boolean: bool) -> 'CelestialBodyFrame': ...
    @typing.overload
    @staticmethod
    def getH0MinusN(string: str, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> Frame: ...
    @typing.overload
    @staticmethod
    def getH0MinusN(string: str, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float) -> Frame: ...
    @staticmethod
    def getICRF() -> 'CelestialBodyFrame':
        """
            Get the unique ICRF frame.
        
            The ICRF frame is centered at solar system barycenter and aligned with GCRF.
        
            The ICRF frame is the root frame in the frame tree.
        
            Returns:
                the unique instance of the ICRF frame
        
        
        """
        ...
    @staticmethod
    def getITRF() -> 'CelestialBodyFrame': ...
    @staticmethod
    def getITRFEquinox() -> 'CelestialBodyFrame': ...
    @staticmethod
    def getMOD(boolean: bool) -> 'CelestialBodyFrame':
        """
            Get the MOD reference frame.
        
            The applyEOPCorr parameter is available mainly for testing purposes or for consistency with legacy software that don't
            handle EOP correction parameters. Beware that setting this parameter to :code:`false` leads to crude accuracy (order of
            magnitudes for errors might be above 1m in LEO and 10m in GEO).
        
            Parameters:
                applyEOPCorr (boolean): if true, EOP corrections are applied (EME2000/GCRF bias compensation)
        
            Returns:
                the selected reference frame singleton.
        
        
        """
        ...
    @staticmethod
    def getTEME() -> 'CelestialBodyFrame': ...
    @staticmethod
    def getTIRF() -> 'CelestialBodyFrame': ...
    @staticmethod
    def getTOD(boolean: bool) -> 'CelestialBodyFrame': ...
    @staticmethod
    def getVeis1950() -> 'CelestialBodyFrame': ...
    @staticmethod
    def setConfiguration(framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> None:
        """
            Sets a new configuration. Replaces the current instance of the configuration by the provided parameter.
        
            Parameters:
                newCfg (:class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`): the new configuration.
        
        
        """
        ...

class LOFType(java.lang.Enum['LOFType']):
    """
    public enum LOFType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.frames.LOFType`>
    
        Enumerate for different types of Local Orbital Frames. Formulas comes from the CNES document:
        DYNVOL-NT-ORB/MOD-1245-CNES Ed. 01 Rev. 00.
    """
    TNW: typing.ClassVar['LOFType'] = ...
    QSW: typing.ClassVar['LOFType'] = ...
    mQmSW: typing.ClassVar['LOFType'] = ...
    LVLH: typing.ClassVar['LOFType'] = ...
    VNC: typing.ClassVar['LOFType'] = ...
    @typing.overload
    def transformFromInertial(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates) -> fr.cnes.sirius.patrius.frames.transformations.Transform:
        """
            Get the transform from an inertial frame defining position-velocity and the local orbital frame.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                pv (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`): position-velocity of the spacecraft in some inertial frame
                computeSpinDerivatives (boolean): true if spin derivatives has to be computed
        
            Returns:
                transform from the frame where position-velocity are defined to local orbital frame
        
            Get the transform from an inertial frame defining position-velocity and the local orbital frame.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                pv (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`): position-velocity of the spacecraft in some inertial frame
        
            Returns:
                transform from the frame where position-velocity are defined to local orbital frame
        
        
        """
        ...
    @typing.overload
    def transformFromInertial(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, boolean: bool) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'LOFType':
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
    def values() -> typing.MutableSequence['LOFType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (LOFType c : LOFType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class OrphanFrame:
    """
    public final class OrphanFrame extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class allows creating a frame that is not linked to the Orekit frames tree.
    
        Since:
            1.1
    """
    @staticmethod
    def getNewOrphanFrame(string: str) -> Frame:
        """
            This method creates an Orphan Frame.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): Orphan frame name
        
            Returns:
                the created orphan frame
        
        
        """
        ...

class PredefinedFrameType(java.lang.Enum['PredefinedFrameType']):
    """
    public enum PredefinedFrameType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.frames.PredefinedFrameType`>
    
        Predefined frames provided by :class:`~fr.cnes.sirius.patrius.frames.FramesFactory`.
    """
    GCRF: typing.ClassVar['PredefinedFrameType'] = ...
    EMB: typing.ClassVar['PredefinedFrameType'] = ...
    ICRF: typing.ClassVar['PredefinedFrameType'] = ...
    EME2000: typing.ClassVar['PredefinedFrameType'] = ...
    ITRF: typing.ClassVar['PredefinedFrameType'] = ...
    ITRF_EQUINOX: typing.ClassVar['PredefinedFrameType'] = ...
    TIRF: typing.ClassVar['PredefinedFrameType'] = ...
    CIRF: typing.ClassVar['PredefinedFrameType'] = ...
    VEIS_1950: typing.ClassVar['PredefinedFrameType'] = ...
    G50: typing.ClassVar['PredefinedFrameType'] = ...
    GTOD_WITHOUT_EOP_CORRECTIONS: typing.ClassVar['PredefinedFrameType'] = ...
    GTOD_WITH_EOP_CORRECTIONS: typing.ClassVar['PredefinedFrameType'] = ...
    TOD_WITHOUT_EOP_CORRECTIONS: typing.ClassVar['PredefinedFrameType'] = ...
    TOD_WITH_EOP_CORRECTIONS: typing.ClassVar['PredefinedFrameType'] = ...
    MOD_WITHOUT_EOP_CORRECTIONS: typing.ClassVar['PredefinedFrameType'] = ...
    MOD_WITH_EOP_CORRECTIONS: typing.ClassVar['PredefinedFrameType'] = ...
    TEME: typing.ClassVar['PredefinedFrameType'] = ...
    ECLIPTIC_MOD_WITHOUT_EOP_CORRECTIONS: typing.ClassVar['PredefinedFrameType'] = ...
    ECLIPTIC_MOD_WITH_EOP_CORRECTIONS: typing.ClassVar['PredefinedFrameType'] = ...
    ECLIPTIC_J2000: typing.ClassVar['PredefinedFrameType'] = ...
    def getCelestialPoint(self) -> fr.cnes.sirius.patrius.bodies.CelestialPoint: ...
    def getName(self) -> str:
        """
            Get the name of the frame.
        
            Returns:
                name of the frame
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'PredefinedFrameType':
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
    def values() -> typing.MutableSequence['PredefinedFrameType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (PredefinedFrameType c : PredefinedFrameType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class CelestialBodyFrame(Frame):
    """
    public class CelestialBodyFrame extends :class:`~fr.cnes.sirius.patrius.frames.Frame`
    
        Frame centered on a :class:`~fr.cnes.sirius.patrius.bodies.CelestialPoint`.
    
        **Warning: this class does not check if provided celestial body is indeed centered on this frame.**
    
        Since:
            4.10
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, frame: Frame, transform: fr.cnes.sirius.patrius.frames.transformations.Transform, string: str, boolean: bool, celestialPoint: fr.cnes.sirius.patrius.bodies.CelestialPoint): ...
    @typing.overload
    def __init__(self, frame: Frame, transform: fr.cnes.sirius.patrius.frames.transformations.Transform, string: str, celestialPoint: fr.cnes.sirius.patrius.bodies.CelestialPoint): ...
    @typing.overload
    def __init__(self, frame: Frame, transformProvider: fr.cnes.sirius.patrius.frames.transformations.TransformProvider, string: str, boolean: bool, celestialPoint: fr.cnes.sirius.patrius.bodies.CelestialPoint): ...
    @typing.overload
    def __init__(self, frame: Frame, transformProvider: fr.cnes.sirius.patrius.frames.transformations.TransformProvider, string: str, celestialPoint: fr.cnes.sirius.patrius.bodies.CelestialPoint): ...
    def getCelestialPoint(self) -> fr.cnes.sirius.patrius.bodies.CelestialPoint: ...

class FrozenFrame(Frame):
    """
    public final class FrozenFrame extends :class:`~fr.cnes.sirius.patrius.frames.Frame`
    
        Provide a wrapper frame between a reference and a coordinate frame, so that it has no angular velocity
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, frame: Frame, frame2: Frame, string: str): ...

class H0MinusNFrame(Frame):
    """
    public class H0MinusNFrame extends :class:`~fr.cnes.sirius.patrius.frames.Frame`
    
    
        "H0 - n" reference frame.
        The "H0 - n" frame is a pseudo-inertial frame, built from the GCRF-ITRF transformation at the date H0 - n; this
        transformation is "frozen" in time, and it is combined to a rotation of an angle "longitude" around the Z axis of the
        ITRF frame.
    
        Its parent frame is the GCRF frame.
    
        Since:
            3.4
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float): ...
    def getH0(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the reference date.
        
            Returns:
                the reference date
        
        
        """
        ...
    def getLongitude(self) -> float:
        """
            Getter for the rotation angle around the ITRF Z axis.
        
            Returns:
                the rotation angle around the ITRF Z axis (rad)
        
        
        """
        ...
    def getN(self) -> float:
        """
            Getter for the reference date shift.
        
            Returns:
                the reference date shift
        
        
        """
        ...

class LocalOrbitalFrame(Frame):
    """
    public class LocalOrbitalFrame extends :class:`~fr.cnes.sirius.patrius.frames.Frame`
    
        Class for frames moving with an orbiting satellite.
    
        There are several local orbital frames available. They are specified by the
        :class:`~fr.cnes.sirius.patrius.frames.LOFType` enumerate.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, frame: Frame, lOFType: LOFType, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, string: str): ...
    def getCenter(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Returns the center of the LOF.
        
            Returns:
                the center of the LOF
        
        
        """
        ...
    def getLofType(self) -> LOFType:
        """
            Returns the local orbital frame type.
        
            Returns:
                the local orbital frame type
        
        
        """
        ...
    def setCenter(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider) -> None:
        """
        
            Parameters:
                center (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`): the center to set
        
        
        """
        ...

class SynodicFrame(Frame):
    """
    public class SynodicFrame extends :class:`~fr.cnes.sirius.patrius.frames.Frame`
    
        Synodic frame. A synodic frame is a frame aligned on a :class:`~fr.cnes.sirius.patrius.frames.LocalOrbitalFrame` and
        translated by a proportional distance along the axis defined by the 2 centers (LOF center and LOF parent center). This
        kind of frame is well suited for the 3rd body problem, for which the classical synodic frame is:
    
        LOF frame is of type :meth:`~fr.cnes.sirius.patrius.frames.LOFType.QSW` centered around 2nd body and normalized center
        position is defined using bodies mass ratio (in [0, 1]). 0 means the synodic frame is centered around the main body, 1
        means the synodic frame is centered around the LOF (i.e. the second body in case of three body problem).
    
        Since:
            4.8
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, localOrbitalFrame: LocalOrbitalFrame, string: str, double: float): ...

class TopocentricFrame(Frame):
    @typing.overload
    def __init__(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint, double: float, string: str): ...
    @typing.overload
    def __init__(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, string: str): ...
    @typing.overload
    def __init__(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, string: str): ...
    @typing.overload
    def __init__(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint, string: str): ...
    def computeLimitVisibilityPoint(self, double: float, double2: float, double3: float) -> fr.cnes.sirius.patrius.bodies.BodyPoint: ...
    def getAzimuth(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getAzimuthRate(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getDAzimuth(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getDElevation(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getDXangleCardan(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getDYangleCardan(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getEast(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getElevation(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getElevationRate(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getFrameOrigin(self) -> fr.cnes.sirius.patrius.bodies.BodyPoint: ...
    def getNadir(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getNorth(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getOrientation(self) -> float: ...
    def getRange(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getRangeRate(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getSouth(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getWest(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getXangleCardan(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getXangleCardanRate(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getYangleCardan(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getYangleCardanRate(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getZenith(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def pointAtDistance(self, double: float, double2: float, double3: float) -> fr.cnes.sirius.patrius.bodies.BodyPoint: ...
    def transformFromCardanToPV(self, cardanMountPV: fr.cnes.sirius.patrius.orbits.pvcoordinates.CardanMountPV) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def transformFromCardanToPosition(self, cardanMountPosition: fr.cnes.sirius.patrius.orbits.pvcoordinates.CardanMountPosition) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def transformFromPVToCardan(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.CardanMountPV: ...
    def transformFromPVToTopocentric(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.TopocentricPV: ...
    def transformFromPositionToCardan(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.CardanMountPosition: ...
    def transformFromPositionToTopocentric(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.TopocentricPosition: ...
    def transformFromTopocentricToPV(self, topocentricPV: fr.cnes.sirius.patrius.orbits.pvcoordinates.TopocentricPV) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def transformFromTopocentricToPosition(self, topocentricPosition: fr.cnes.sirius.patrius.orbits.pvcoordinates.TopocentricPosition) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class TranslatedFrame(Frame):
    def __init__(self, frame: Frame, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, string: str, boolean: bool): ...
    def getCenter(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider: ...

class TwoDirectionFrame(Frame):
    """
    public class TwoDirectionFrame extends :class:`~fr.cnes.sirius.patrius.frames.Frame`
    
        Class for frames built with two directions and the two axes they correspond to.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, frame: Frame, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, string: str, iDirection: fr.cnes.sirius.patrius.attitudes.directions.IDirection, iDirection2: fr.cnes.sirius.patrius.attitudes.directions.IDirection, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, frame: Frame, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, string: str, iDirection: fr.cnes.sirius.patrius.attitudes.directions.IDirection, iDirection2: fr.cnes.sirius.patrius.attitudes.directions.IDirection, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    def getAxisOne(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
        
            Returns:
                the axisOne
        
        
        """
        ...
    def getAxisTwo(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
        
            Returns:
                the axisTwo
        
        
        """
        ...
    def getDirectionOne(self) -> fr.cnes.sirius.patrius.attitudes.directions.IDirection:
        """
        
            Returns:
                the directionOne
        
        
        """
        ...
    def getDirectionTwo(self) -> fr.cnes.sirius.patrius.attitudes.directions.IDirection:
        """
        
            Returns:
                the directionTwo
        
        
        """
        ...

class UpdatableFrame(Frame):
    """
    public class UpdatableFrame extends :class:`~fr.cnes.sirius.patrius.frames.Frame`
    
        Frame whose transform from its parent can be updated.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, frame: Frame, transform: fr.cnes.sirius.patrius.frames.transformations.Transform, string: str): ...
    @typing.overload
    def __init__(self, frame: Frame, transform: fr.cnes.sirius.patrius.frames.transformations.Transform, string: str, boolean: bool): ...
    def setTransform(self, transform: fr.cnes.sirius.patrius.frames.transformations.Transform) -> None:
        """
            Update the transform from the parent frame to the instance.
        
            Parameters:
                transform (:class:`~fr.cnes.sirius.patrius.frames.transformations.Transform`): new transform from parent frame to instance
        
        
        """
        ...
    def updateTransform(self, frame: Frame, frame2: Frame, transform: fr.cnes.sirius.patrius.frames.transformations.Transform, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class PredefinedFrame(CelestialBodyFrame):
    """
    public class PredefinedFrame extends :class:`~fr.cnes.sirius.patrius.frames.CelestialBodyFrame`
    
        Base class for the predefined frames that are managed by :class:`~fr.cnes.sirius.patrius.frames.FramesFactory`.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, frame: Frame, transformProvider: fr.cnes.sirius.patrius.frames.transformations.TransformProvider, boolean: bool, predefinedFrameType: PredefinedFrameType): ...
    def getCelestialPoint(self) -> fr.cnes.sirius.patrius.bodies.CelestialPoint: ...
    def getFactoryKey(self) -> PredefinedFrameType:
        """
            Get the key of the frame within the factory.
        
            Returns:
                key of the frame within the factory
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.frames")``.

    CelestialBodyFrame: typing.Type[CelestialBodyFrame]
    Frame: typing.Type[Frame]
    FramesFactory: typing.Type[FramesFactory]
    FrozenFrame: typing.Type[FrozenFrame]
    H0MinusNFrame: typing.Type[H0MinusNFrame]
    LOFType: typing.Type[LOFType]
    LocalOrbitalFrame: typing.Type[LocalOrbitalFrame]
    OrphanFrame: typing.Type[OrphanFrame]
    PredefinedFrame: typing.Type[PredefinedFrame]
    PredefinedFrameType: typing.Type[PredefinedFrameType]
    SynodicFrame: typing.Type[SynodicFrame]
    TopocentricFrame: typing.Type[TopocentricFrame]
    TranslatedFrame: typing.Type[TranslatedFrame]
    TwoDirectionFrame: typing.Type[TwoDirectionFrame]
    UpdatableFrame: typing.Type[UpdatableFrame]
    configuration: fr.cnes.sirius.patrius.frames.configuration.__module_protocol__
    transformations: fr.cnes.sirius.patrius.frames.transformations.__module_protocol__
