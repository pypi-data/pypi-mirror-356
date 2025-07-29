
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames.configuration
import fr.cnes.sirius.patrius.frames.configuration.eop
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.time
import fr.cnes.sirius.patrius.utils
import fr.cnes.sirius.patrius.wrenches
import java.io
import java.util
import jpype
import typing



class HelmertTransformationFactory:
    """
    public final class HelmertTransformationFactory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Some :class:`~fr.cnes.sirius.patrius.frames.transformations.HelmertTransformation`.
    
        Since:
            1.3
    """
    ITRF05TO08: typing.ClassVar['HelmertTransformation'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.transformations.HelmertTransformation` ITRF05TO08
    
        Helmert transformation between ITRF2005 and ITRF 2008.
    
    
        see http://itrf.ign.fr/ITRF_solutions/2008/tp_08-05.php
    
    
    
    
        :code:`T1 T2 T3 D R1 R2 R3`
    
    
        :code:`mm mm mm 10-9 mas mas mas`
    
    
        :code:`-0.5 -0.9 -4.7 0.94 0.000 0.000 0.000`
    
    
        :code:`+/- 0.2 0.2 0.2 0.03 0.008 0.008 0.008`
    
    
    
    
        :code:`Rates 0.3 0.0 0.0 0.00 0.000 0.000 0.000`
    
    
        :code:`+/- 0.2 0.2 0.2 0.03 0.008 0.008 0.008`
    
    
    
    
        Table 1: Transformation parameters at epoch 2005.0 and their rates from ITRF2008 to ITRF2005 (ITRF2005 minus ITRF2008)
    
    
    
    """
    ITRF05TO00: typing.ClassVar['HelmertTransformation'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.transformations.HelmertTransformation` ITRF05TO00
    
        Helmert transformation between ITRF2005 and ITRF 2000.
    
    
        see http://itrf.ign.fr/ITRF_solutions/2005/tp_05-00.php
    
    
    
    
        :code:`T1 T2 T3 D R1 R2 R3`
    
    
        :code:`mm mm mm 10-9 mas mas mas`
    
    
        :code:`0.1 -0.8 -5.8 0.40 0.000 0.000 0.000`
    
    
        :code:`+/- 0.3 0.3 0.3 0.05 0.012 0.012 0.012`
    
    
    
    
        :code:`Rates -0.2 0.1 -1.8 0.08 0.000 0.000 0.000`
    
    
        :code:`+/- 0.3 0.3 0.3 0.05 0.012 0.012 0.012`
    
    
    
    
    
    
        Table 1: Transformation parameters at epoch 2000.0 and their rates from ITRF2005 to ITRF2000 (ITRF2000 minus ITRF2005)
    
    """
    ITRF00TO97: typing.ClassVar['HelmertTransformation'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.transformations.HelmertTransformation` ITRF00TO97
    
        Helmert transformation between ITRF2000 and ITRF97
    
    
        see ftp://itrf.ensg.ign.fr/pub/itrf/ITRF.TP
    
    
        -------------------------------------------------------------------------------------
    
    
        SOLUTION T1 T2 T3 D R1 R2 R3 EPOCH Ref.
    
    
        UNITS----------> cm cm cm ppb .001" .001" .001" IERS Tech.
    
    
        . . . . . . . Note #
    
    
        RATES T1 T2 T3 D R1 R2 R3
    
    
        UNITS----------> cm/y cm/y cm/y ppb/y .001"/y .001"/y .001"/y
    
    
        -------------------------------------------------------------------------------------
    
    
        ITRF97 0.67 0.61 -1.85 1.55 0.00 0.00 0.00 1997.0 27
    
    
        rates 0.00 -0.06 -0.14 0.01 0.00 0.00 0.02
    
    
        ...
    
    
    
    
        Note : These parameters are derived from those already published in the IERS Technical Notes indicated in the table
        above. The transformation parameters should be used with the standard model (1) given below and are valid at the
        indicated epoch.
    
    
    
    
        : XS : : X : : T1 : : D -R3 R2 : : X :
    
    
        : : : : : : : : : :
    
    
        : YS : = : Y : + : T2 : + : R3 D -R1 : : Y : (1)
    
    
        : : : : : : : : : :
    
    
        : ZS : : Z : : T3 : : -R2 R1 D : : Z :
    
    
    
    
        Where X,Y,Z are the coordinates in ITRF2000 and XS,YS,ZS are the coordinates in the other frames.
    
    """
    ITRF00TO93: typing.ClassVar['HelmertTransformation'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.transformations.HelmertTransformation` ITRF00TO93
    
        Helmert transformation between ITRF2000 and ITRF93.
    
    
        // see ftp://itrf.ensg.ign.fr/pub/itrf/ITRF.TP
    
    
        // -------------------------------------------------------------------------------------
    
    
        // SOLUTION T1 T2 T3 D R1 R2 R3 EPOCH Ref.
    
    
        // UNITS----------> cm cm cm ppb .001" .001" .001" IERS Tech.
    
    
        // . . . . . . . Note #
    
    
        // RATES T1 T2 T3 D R1 R2 R3
    
    
        // UNITS----------> cm/y cm/y cm/y ppb/y .001"/y .001"/y .001"/y
    
    
        // -------------------------------------------------------------------------------------
    
    
        // ...
    
    
        // ITRF93 1.27 0.65 -2.09 1.95 -0.39 0.80 -1.14 1988.0 18
    
    
        // rates -0.29 -0.02 -0.06 0.01 -0.11 -0.19 0.07
    
    
        // ...
    
    
        //
    
    
        // Note : These parameters are derived from those already published in the IERS // Technical Notes indicated in the
        table above. The transformation parameters // should be used with the standard model (1) given below and are valid at
        the // indicated epoch. //
    
    
    
    
        // : XS : : X : : T1 : : D -R3 R2 : : X :
    
    
        // : : : : : : : : : :
    
    
        // : YS : = : Y : + : T2 : + : R3 D -R1 : : Y : (1)
    
    
        // : : : : : : : : : :
    
    
        // : ZS : : Z : : T3 : : -R2 R1 D : : Z :
    
    
        //
    
    
        // Where X,Y,Z are the coordinates in ITRF2000 and XS,YS,ZS are the coordinates in // the other frames.
    
    
    
    """

class Transform(fr.cnes.sirius.patrius.time.TimeStamped, fr.cnes.sirius.patrius.time.TimeShiftable['Transform'], fr.cnes.sirius.patrius.time.TimeInterpolable['Transform'], java.io.Serializable):
    IDENTITY: typing.ClassVar['Transform'] = ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, transform: 'Transform', transform2: 'Transform'): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, transform: 'Transform', transform2: 'Transform', boolean: bool): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, transform: 'Transform', transform2: 'Transform', boolean: bool, boolean2: bool): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, angularCoordinates: fr.cnes.sirius.patrius.utils.AngularCoordinates): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, angularCoordinates: fr.cnes.sirius.patrius.utils.AngularCoordinates): ...
    def freeze(self) -> 'Transform': ...
    def getAcceleration(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getAngular(self) -> fr.cnes.sirius.patrius.utils.AngularCoordinates: ...
    def getCartesian(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
    @typing.overload
    def getInverse(self) -> 'Transform': ...
    @typing.overload
    def getInverse(self, boolean: bool) -> 'Transform': ...
    def getJacobian(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def getRotation(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation: ...
    def getRotationAcceleration(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getRotationRate(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getTranslation(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getVelocity(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection['Transform'], typing.Sequence['Transform'], typing.Set['Transform']]) -> 'Transform': ...
    @typing.overload
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection['Transform'], typing.Sequence['Transform'], typing.Set['Transform']], boolean: bool) -> 'Transform': ...
    @typing.overload
    @staticmethod
    def interpolate(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool, boolean2: bool, collection: typing.Union[java.util.Collection['Transform'], typing.Sequence['Transform'], typing.Set['Transform']]) -> 'Transform': ...
    @typing.overload
    @staticmethod
    def interpolate(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool, boolean2: bool, collection: typing.Union[java.util.Collection['Transform'], typing.Sequence['Transform'], typing.Set['Transform']], boolean3: bool) -> 'Transform': ...
    @typing.overload
    def shiftedBy(self, double: float) -> 'Transform': ...
    @typing.overload
    def shiftedBy(self, double: float, boolean: bool) -> 'Transform': ...
    def transformLine(self, line: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Line: ...
    @typing.overload
    def transformPVCoordinates(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    @typing.overload
    def transformPVCoordinates(self, timeStampedPVCoordinates: fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates) -> fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates: ...
    def transformPosition(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def transformVector(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def transformWrench(self, wrench: fr.cnes.sirius.patrius.wrenches.Wrench) -> fr.cnes.sirius.patrius.wrenches.Wrench: ...

class TransformProvider(java.io.Serializable):
    """
    public interface TransformProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for Transform providers.
    
        The transform provider interface is mainly used to define the transform between a frame and its parent frame.
    """
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class TransformStateProvider(java.io.Serializable):
    """
    public interface TransformStateProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for Transform providers.
    
        The transform provider interface is mainly used to define the transform between a frame and its parent frame.
    
        This class extends the concept of :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider` by
        considering state-dependant transforms
    
        Since:
            4.4
    """
    def getTransform(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> Transform: ...

class AbstractVeisProvider(TransformProvider):
    """
    public abstract class AbstractVeisProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        Abstract class for :class:`~fr.cnes.sirius.patrius.frames.transformations.VEISProvider` and
        :class:`~fr.cnes.sirius.patrius.frames.transformations.G50Provider` which only differ in UT1/UTC handling. The
        transformation remains the same, their parent frame is the
        :class:`~fr.cnes.sirius.patrius.frames.transformations.GTODProvider` without EOP correction application.
    
        Since:
            4.13
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class CIRFProvider(TransformProvider):
    """
    public final class CIRFProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        Celestial Intermediate Reference Frame 2000.
    
        This frame includes both precession and nutation effects according to the new IAU-2000 model. The single model replaces
        the two separate models used before: IAU-76 precession (Lieske) and IAU-80 theory of nutation (Wahr). It **must** be
        used with the Earth Rotation Angle (REA) defined by Capitaine's model and **not** IAU-82 sidereal time which is
        consistent with the previous models only.
    
        Its parent frame is the GCRF frame.
    
    
        Spin derivative is never computed and is either 0 or null. No analytical formula is available for spin derivative since
        data only provide CIP motion and its first derivative.
    
        Frames configuration precession-nutation model is used for computation.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class EMBProvider(TransformProvider):
    """
    public final class EMBProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        Earth-Moon barycenter frame Reference Frame.
    
        This frame is Earth-Moon barycenter-centered pseudo-inertial reference frame.
    
        Its parent frame is the Solar System barycenter frame (ICRF).
    
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class EclipticMODProvider(TransformProvider):
    """
    public final class EclipticMODProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider` for
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getEclipticMOD`.
    
        Spin derivative is either 0 or null since rotation is linear in time.
    
        Frames configuration is unused.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class FixedTransformProvider(TransformProvider):
    """
    public class FixedTransformProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        Transform provider using fixed transform.
    
        Spin derivative available only if defined in the transformation at construction.
    
        Frames configuration is unused.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, transform: Transform): ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform:
        """
            Get the :class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` corresponding to specified date.
        
            **Warning:**spin derivative is not computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider.getTransform` in
                interface :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
        
            Returns:
                transform at specified date
        
            Get the :class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` corresponding to specified date.
        
            **Warning:**spin derivative is not computed.
        
            Frames configuration is unused.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider.getTransform` in
                interface :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                config (:class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`): frames configuration to use
        
            Returns:
                transform at specified date
        
        public :class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` getTransform(:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` date, boolean computeSpinDerivatives) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Get the :class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` corresponding to specified date.
        
            Spin derivative available only if defined in the transformation at construction.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider.getTransform` in
                interface :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                computeSpinDerivatives (boolean): true if spin derivatives should be computed. If not, spin derivative is set to *null*
        
            Returns:
                transform at specified date
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if transform cannot be computed at given date
        
        public :class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` getTransform(:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` date, :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration` config, boolean computeSpinDerivatives) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Get the :class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` corresponding to specified date.
        
            Spin derivative available only if defined in the transformation at construction.
        
            Frames configuration is unused.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider.getTransform` in
                interface :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                config (:class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`): frames configuration to use
                computeSpinDerivatives (boolean): true if spin derivatives should be computed. If not, spin derivative is set to *null*
        
            Returns:
                transform at specified date
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if transform cannot be computed at given date
        
        
        """
        ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class GCRFProvider(TransformProvider):
    """
    public final class GCRFProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        Geocentric Celestial Reference Frame.
    
        This frame is Earth-centered pseudo-inertial reference frame.
    
        Its parent frame is the Earth-Moon barycenter frame.
    
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class GTODProvider(TransformProvider):
    """
    public final class GTODProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        Greenwich True Of Date Frame, also known as True of Date Rotating frame (TDR) or Greenwich Rotating Coordinate frame
        (GCR).
    
        This frame handles the sidereal time according to IAU-82 model.
    
        Its parent frame is the :class:`~fr.cnes.sirius.patrius.frames.transformations.TODProvider`.
    
        The pole motion is not applied here.
    
        Spin derivative is never computed and is either 0 or null. No analytical formula is currently available for spin
        derivative although a formula could be derived.
    
        Frames configuration LOD and UT1 - TAI is used.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getGAST(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    @typing.overload
    def getGAST(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> float: ...
    @typing.overload
    @staticmethod
    def getGMST(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    @typing.overload
    @staticmethod
    def getGMST(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> float: ...
    @typing.overload
    @staticmethod
    def getRotationRate(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    @typing.overload
    @staticmethod
    def getRotationRate(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> float: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class HelmertTransformation(TransformProvider):
    """
    public class HelmertTransformation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        Transformation class for ellipsoid systems.
    
        The Helmert transformation is mainly used to convert between various realizations of ellipsoid frames, for example in
        the ITRF family.
    
        The original Helmert transformation is a 14 parameters transform that includes translation, velocity, rotation, rotation
        rate and scale factor. The scale factor is useful for coordinates near Earth surface, but it cannot be extended to outer
        space as it would correspond to a non-unitary transform. Therefore, the scale factor is *not* used here.
    
        Instances of this class are guaranteed to be immutable.
    
        Spin derivative is never computed and is either 0 or null. No analytical formula is currently available for spin
        derivative although it could be derived.
    
        Frames configuration is unused.
    
        Since:
            5.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float, double10: float, double11: float, double12: float): ...
    def getCartesian(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates:
        """
            Returns the Cartesian part of the transform.
        
            Returns:
                the Cartesian part of the transform
        
        
        """
        ...
    def getEpoch(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the reference epoch of the transform.
        
            Returns:
                reference epoch of the transform
        
        
        """
        ...
    def getRotationRate(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Returns the first time derivative of the rotation (norm representing angular rate).
        
            Returns:
                the first time derivative of the rotation (norm representing angular rate)
        
        
        """
        ...
    def getRotationVector(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Returns the global rotation vector (applying rotation is done by computing cross product).
        
            Returns:
                the global rotation vector (applying rotation is done by computing cross product)
        
        
        """
        ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class ITRFEquinoxProvider(TransformProvider):
    """
    public final class ITRFEquinoxProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        International Terrestrial Reference Frame, based on old equinox conventions.
    
        Handles pole motion effects and depends on :class:`~fr.cnes.sirius.patrius.frames.transformations.GTODProvider`, its
        parent frame.
    
        Spin derivative is never computed and is either 0 or null. No analytical formula is available for spin derivative since
        data only provide pole correction without derivatives. Spin is also 0.
    
        Frames configuration Pole correction is used.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class ITRFProvider(TransformProvider):
    """
    public final class ITRFProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        International Terrestrial Reference Frame.
    
        Handles pole motion effects and depends on :class:`~fr.cnes.sirius.patrius.frames.transformations.TIRFProvider`, its
        parent frame.
    
        Spin derivative is never computed and is either 0 or null. No analytical formula is available for spin derivative since
        data only provide pole correction without derivatives. Spin is also 0. Spin is also 0.
    
        Frames configuration polar motion and S' is used.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class InterpolatingTransformProvider(TransformProvider):
    """
    public class InterpolatingTransformProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        Transform provider using thread-safe interpolation on transforms sample.
    
        The interpolation is a polynomial Hermite interpolation, which can either use or ignore the derivatives provided by the
        raw provider. This means that simple raw providers that do not compute derivatives can be used, the derivatives will be
        added appropriately by the interpolation process.
    
        Spin derivative is available and computed if required.
    
        Frames configuration is unused.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.time.TimeStampedCache`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, transformProvider: TransformProvider, boolean: bool, boolean2: bool, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, int: int, double: float, int2: int, double2: float, double3: float): ...
    @typing.overload
    def __init__(self, transformProvider: TransformProvider, boolean: bool, boolean2: bool, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, int: int, double: float, int2: int, double2: float, double3: float, boolean3: bool): ...
    def getRawProvider(self) -> TransformProvider:
        """
            Get the underlying provider for raw (non-interpolated) transforms.
        
            Returns:
                provider for raw (non-interpolated) transforms
        
        
        """
        ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class MODProvider(TransformProvider):
    """
    public final class MODProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        Mean Equator, Mean Equinox Frame.
    
        This frame handles precession effects according to the IAU-76 model (Lieske).
    
        Its parent frame is the GCRF frame.
    
        It is sometimes called Mean of Date (MoD) frame.
    
        Spin derivative is never computed and is either 0 or null. No analytical formula is currently available for spin
        derivative although a formula could be derived. Spin is also 0.
    
        Frames configuration is unused.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform:
        """
            Get the transfrom from parent frame.
        
            The update considers the precession effects.
        
            Frames configuration is unused.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider.getTransform` in
                interface :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): new value of the date
                config (:class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`): frames configuration to use
        
            Returns:
                transform at the specified date
        
        public :class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` getTransform(:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` date) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Get the transfrom from parent frame.
        
            The update considers the precession effects.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider.getTransform` in
                interface :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): new value of the date
        
            Returns:
                transform at the specified date
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if the default configuration cannot be retrieved
        
        public :class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` getTransform(:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` date, boolean computeSpinDerivatives) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Get the transfrom from parent frame.
        
            The update considers the precession effects.
        
            Spin derivative is never computed and is either 0 or null. No analytical formula is currently available for spin
            derivative although a formula could be derived. Spin is also 0.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider.getTransform` in
                interface :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): new value of the date
                computeSpinDerivatives (boolean): not used
        
            Returns:
                transform at the specified date
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if the default configuration cannot be retrieved
        
            Get the transfrom from parent frame.
        
            The update considers the precession effects.
        
            Spin derivative is never computed and is either 0 or null. No analytical formula is currently available for spin
            derivative although a formula could be derived. Spin is also 0.
        
            Frames configuration is unused.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider.getTransform` in
                interface :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): new value of the date
                config (:class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration`): frames configuration to use
                computeSpinDerivatives (boolean): not used
        
            Returns:
                transform at the specified date
        
        
        """
        ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class TEMEProvider(TransformProvider):
    """
    public final class TEMEProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        True Equator Mean Equinox Frame.
    
        This frame is used for the SGP4 model in TLE propagation. This frame has *no* official definition and there are some
        ambiguities about whether it should be used as "of date" or "of epoch". This frame should therefore be used *only* for
        TLE propagation and not for anything else, as recommended by the CCSDS Orbit Data Message blue book.
    
        Spin derivative is never computed and is either 0 or null. No analytical formula is currently available for spin
        derivative. Spin is also 0.
    
        Frames configuration is unused.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class TIRFProvider(TransformProvider):
    """
    public final class TIRFProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        Terrestrial Intermediate Reference Frame 2000.
    
        The pole motion is not considered : Pseudo Earth Fixed Frame. It handles the earth rotation angle, its parent frame is
        the :class:`~fr.cnes.sirius.patrius.frames.transformations.CIRFProvider`
    
        Spin derivative, when computed, is always 0.
    
        *Default* frames configuration UT1 - TAI is used.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @staticmethod
    def getEarthRotationAngle(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    @staticmethod
    def getEarthRotationRate() -> float:
        """
            Get the Earth Rotation rate.
        
            Returns:
                Earth Rotation rate
        
        
        """
        ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class TODProvider(TransformProvider):
    """
    public final class TODProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider`
    
        True Equator, Mean Equinox of Date Frame.
    
        This frame handles nutation effects according to the IAU-80 theory.
    
        Its parent frame is the :class:`~fr.cnes.sirius.patrius.frames.transformations.MODProvider`.
    
        It is sometimes called True of Date (ToD) frame.
    
    
        Spin derivative is never computed and is either 0 or null. No analytical formula is currently available for spin
        derivative. Spin is also 0.
    
        Frames configuration nutation correction is used.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, boolean: bool): ...
    @staticmethod
    def getEquationOfEquinoxes(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
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
    def getPoleCorrection(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.configuration.eop.PoleCorrection: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration) -> Transform: ...
    @typing.overload
    def getTransform(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, framesConfiguration: fr.cnes.sirius.patrius.frames.configuration.FramesConfiguration, boolean: bool) -> Transform: ...

class EME2000Provider(FixedTransformProvider):
    """
    public final class EME2000Provider extends :class:`~fr.cnes.sirius.patrius.frames.transformations.FixedTransformProvider`
    
        EME2000 frame : mean equator at J2000.0.
    
        This frame was the standard inertial reference prior to GCRF. It was defined using Lieske precession-nutation model for
        Earth. This frame has been superseded by GCRF which is implicitly defined from a few hundred quasars coordinates.
    
        The transformation between GCRF and EME2000 is a constant rotation bias.
    
        Spin derivative, when computed, is always 0 by definition.
    
        Frames configuration is unused.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...

class EclipticJ2000Provider(FixedTransformProvider):
    """
    public class EclipticJ2000Provider extends :class:`~fr.cnes.sirius.patrius.frames.transformations.FixedTransformProvider`
    
        :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformProvider` for
        :meth:`~fr.cnes.sirius.patrius.frames.FramesFactory.getEclipticJ2000`.
    
        Spin derivative is either 0 or null since rotation is linear in time.
    
        Frames configuration is unused.
    
        Since:
            4.13
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...

class G50Provider(AbstractVeisProvider):
    """
    public final class G50Provider extends :class:`~fr.cnes.sirius.patrius.frames.transformations.AbstractVeisProvider`
    
        G50 (Gamma 50) frame.
    
        Its parent frame is the :class:`~fr.cnes.sirius.patrius.frames.transformations.GTODProvider` without EOP correction
        application.
    
        This frame is mainly provided for consistency with legacy softwares.
    
        Spin derivative, when computed, is always 0.
    
        Since:
            4.13
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...

class H0MinusNProvider(FixedTransformProvider):
    """
    public final class H0MinusNProvider extends :class:`~fr.cnes.sirius.patrius.frames.transformations.FixedTransformProvider`
    
    
        "H0 - n" reference frame.
        The "H0 - n" frame is a pseudo-inertial frame, built from the GCRF-ITRF transformation at the date H0 - n; this
        transformation is "frozen" in time, and it is combined to a rotation of an angle "longitude" around the Z axis of the
        ITRF frame.
    
        Its parent frame is the GCRF frame.
    
        Spin derivative, when computed, is always 0 by definition.
    
        Frames configuration is unused.
    
        Since:
            2.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.frames.FramesFactory`, :meth:`~serialized`
    """
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float): ...

class VEISProvider(AbstractVeisProvider):
    """
    public final class VEISProvider extends :class:`~fr.cnes.sirius.patrius.frames.transformations.AbstractVeisProvider`
    
        Veis 1950 Frame.
    
        Its parent frame is the :class:`~fr.cnes.sirius.patrius.frames.transformations.GTODProvider` without EOP correction
        application.
    
        This frame is mainly provided for consistency with legacy softwares.
    
        Spin derivative, when computed, is always 0.
    
        Frames configuration UT1 - TAI is used.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.frames.transformations")``.

    AbstractVeisProvider: typing.Type[AbstractVeisProvider]
    CIRFProvider: typing.Type[CIRFProvider]
    EMBProvider: typing.Type[EMBProvider]
    EME2000Provider: typing.Type[EME2000Provider]
    EclipticJ2000Provider: typing.Type[EclipticJ2000Provider]
    EclipticMODProvider: typing.Type[EclipticMODProvider]
    FixedTransformProvider: typing.Type[FixedTransformProvider]
    G50Provider: typing.Type[G50Provider]
    GCRFProvider: typing.Type[GCRFProvider]
    GTODProvider: typing.Type[GTODProvider]
    H0MinusNProvider: typing.Type[H0MinusNProvider]
    HelmertTransformation: typing.Type[HelmertTransformation]
    HelmertTransformationFactory: typing.Type[HelmertTransformationFactory]
    ITRFEquinoxProvider: typing.Type[ITRFEquinoxProvider]
    ITRFProvider: typing.Type[ITRFProvider]
    InterpolatingTransformProvider: typing.Type[InterpolatingTransformProvider]
    MODProvider: typing.Type[MODProvider]
    TEMEProvider: typing.Type[TEMEProvider]
    TIRFProvider: typing.Type[TIRFProvider]
    TODProvider: typing.Type[TODProvider]
    Transform: typing.Type[Transform]
    TransformProvider: typing.Type[TransformProvider]
    TransformStateProvider: typing.Type[TransformStateProvider]
    VEISProvider: typing.Type[VEISProvider]
