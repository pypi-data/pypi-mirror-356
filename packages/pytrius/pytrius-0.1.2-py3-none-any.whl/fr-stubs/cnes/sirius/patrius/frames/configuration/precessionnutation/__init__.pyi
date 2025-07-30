
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames.configuration
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import jpype
import typing



class CIPCoordinates(fr.cnes.sirius.patrius.time.TimeStamped, java.io.Serializable):
    """
    public final class CIPCoordinates extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class represents a Celestial Intermediate Pole. It contains a date and the CIP coordinates at that date.
    
        Also see:
            :meth:`~serialized`
    """
    ZERO: typing.ClassVar['CIPCoordinates'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.CIPCoordinates` ZERO
    
        Zero CIP coordinates.
    
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getCIPMotion(self) -> typing.MutableSequence[float]:
        """
            Get for the CIP motion.
        
            Returns:
                the CIP motion as an array
        
        
        """
        ...
    def getCIPMotionTimeDerivatives(self) -> typing.MutableSequence[float]:
        """
            Getter for the CIP motion time derivatives.
        
            Returns:
                the CIP motion time derivatives as an array
        
        
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
    def getS(self) -> float:
        """
            Getter for the s-coordinate of pole.
        
            Returns:
                the s-coordinate of pole
        
        
        """
        ...
    def getX(self) -> float:
        """
            Getter for the x-coordinate of pole.
        
            Returns:
                the x-coordinate of pole
        
        
        """
        ...
    def getY(self) -> float:
        """
            Getter for the y-coordinate of pole.
        
            Returns:
                the y-coordinate of pole
        
        
        """
        ...
    def getsP(self) -> float:
        """
            Getter for the s-coordinate derivative of pole.
        
            Returns:
                the s-coordinate derivative of pole
        
        
        """
        ...
    def getxP(self) -> float:
        """
            Getter for the x-coordinate derivative of pole.
        
            Returns:
                the x-coordinate derivative of pole
        
        
        """
        ...
    def getyP(self) -> float:
        """
            Getter for the y-coordinate derivative of pole.
        
            Returns:
                the y-coordinate derivative of pole
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def isCIPMotionTimeDerivativesZero(self) -> bool:
        """
            Indicate if the coordinates derivatives of pole are zero.
        
            Returns:
                true if the coordinates derivatives of pole are zero
        
        
        """
        ...
    def isCIPMotionZero(self) -> bool:
        """
            Indicate if the coordinates of pole are zero.
        
            Returns:
                true if the coordinates of pole are zero
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class CIPCoordinatesGenerator(fr.cnes.sirius.patrius.time.TimeStampedGenerator[CIPCoordinates]):
    """
    public class CIPCoordinatesGenerator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStampedGenerator`<:class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.CIPCoordinates`>
    
        The class generates :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.CIPCoordinates` to be used
        independently or within a :class:`~fr.cnes.sirius.patrius.time.TimeStampedCache`. The method applied is that of the
        IAU-2000.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`, :meth:`~serialized`
    """
    def generate(self, cIPCoordinates: CIPCoordinates, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.List[CIPCoordinates]: ...

class PrecessionNutation(java.io.Serializable):
    """
    public class PrecessionNutation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class contains the CIRF precession nutation model used within the
        :class:`~fr.cnes.sirius.patrius.frames.configuration.FramesConfigurationImplementation` class.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, boolean: bool, precessionNutationModel: 'PrecessionNutationModel'): ...
    def getCIPCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> CIPCoordinates:
        """
            Compute the CIP pole coordinates at given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date at which to compute CIP coordinates
        
            Returns:
                the CIP pole coordinates
        
        
        """
        ...
    def getPrecessionNutationModel(self) -> 'PrecessionNutationModel':
        """
        
            Returns:
                the precession nutation model
        
        
        """
        ...
    def useEopData(self) -> bool:
        """
            Use EOP data for nutation correction.
        
            Returns:
                true if EOP data is to be used, false if not.
        
        
        """
        ...

class PrecessionNutationConvention(java.lang.Enum['PrecessionNutationConvention']):
    """
    public enum PrecessionNutationConvention extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationConvention`>
    
        IERS Precession Nutation enumerate. Each enumerate provides data file locations.
    """
    IERS2003: typing.ClassVar['PrecessionNutationConvention'] = ...
    IERS2010: typing.ClassVar['PrecessionNutationConvention'] = ...
    def getIERSConvention(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Getter for IERS convention.
        
            Returns:
                IERS convention
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'PrecessionNutationConvention':
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
    def values() -> typing.MutableSequence['PrecessionNutationConvention']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (PrecessionNutationConvention c : PrecessionNutationConvention.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class PrecessionNutationModel(java.io.Serializable):
    """
    public interface PrecessionNutationModel extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface provides the Celestial Intermediate Pole motion (CIP) in the GCRS, those coordinates are used for the
        GCRF to CIRF transformation.
    """
    def getCIPCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> CIPCoordinates:
        """
            Getter for the CIP coordinates at the provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date for the CIP coordinates
        
            Returns:
                the CIP coordinates
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Return computation type : direct or interpolated.
        
            Returns:
                true if direct computation, false if interpolated
        
        
        """
        ...

class PrecessionNutationModelFactory:
    """
    public final class PrecessionNutationModelFactory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Factory for predefined models.
    
        Since:
            1.3
    """
    NO_PN: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` NO_PN
    
        No precession Nutation.
    
    """
    PN_IERS2010_INTERPOLATED: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2010_INTERPOLATED
    
        IERS 2010 with interpolation.
    
    
        The cache is shared by all threads (still, this is thread-safe).
    
        Note: when the threads are separated by a long duration, we recommend using
        :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModelFactory.PN_IERS2010_INTERPOLATED_BY_THREAD`
        instead (in term of performance).
    
    """
    PN_IERS2003_INTERPOLATED: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2003_INTERPOLATED
    
        IERS 2003 with interpolation.
    
    
        The cache is shared by all threads (still, this is thread-safe).
    
        Note: when the threads are separated by a long duration, we recommend using
        :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModelFactory.PN_IERS2003_INTERPOLATED_BY_THREAD`
        instead (in term of performance).
    
    """
    PN_IERS2010_INTERPOLATED_BY_THREAD: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2010_INTERPOLATED_BY_THREAD
    
        IERS 2010 with interpolation.
    
    
        The cache is specific for each thread.
    
    """
    PN_IERS2003_INTERPOLATED_BY_THREAD: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2003_INTERPOLATED_BY_THREAD
    
        IERS 2003 with interpolation.
    
    
        The cache is specific for each thread.
    
    """
    PN_IERS2010_DIRECT: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2010_DIRECT
    
        IERS 2010 without interpolation.
    
    """
    PN_IERS2003_DIRECT: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2003_DIRECT
    
        IERS 2003 without interpolation.
    
    """
    PN_STELA: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_STELA
    
        Stela model.
    
    
        The cache is specific for each thread.
    
    """
    PN_IERS2010_INTERPOLATED_NON_CONSTANT_OLD: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2010_INTERPOLATED_NON_CONSTANT_OLD
    
        IERS 2010 with interpolation.
    
    """
    PN_IERS2003_INTERPOLATED_NON_CONSTANT_OLD: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2003_INTERPOLATED_NON_CONSTANT_OLD
    
        IERS 2003 with interpolation.
    
    """
    PN_IERS2010_DIRECT_NON_CONSTANT_OLD: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2010_DIRECT_NON_CONSTANT_OLD
    
        IERS 2010 without interpolation.
    
    """
    PN_IERS2003_DIRECT_NON_CONSTANT_OLD: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2003_DIRECT_NON_CONSTANT_OLD
    
        IERS 2003 without interpolation.
    
    """
    PN_IERS2010_INTERPOLATED_CONSTANT_OLD: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2010_INTERPOLATED_CONSTANT_OLD
    
        IERS 2010 with interpolation.
    
    """
    PN_IERS2003_INTERPOLATED_CONSTANT_OLD: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2003_INTERPOLATED_CONSTANT_OLD
    
        IERS 2003 with interpolation.
    
    """
    PN_IERS2010_DIRECT_CONSTANT_OLD: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2010_DIRECT_CONSTANT_OLD
    
        IERS 2010 without interpolation.
    
    """
    PN_IERS2003_DIRECT_CONSTANT_OLD: typing.ClassVar[PrecessionNutationModel] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` PN_IERS2003_DIRECT_CONSTANT_OLD
    
        IERS 2003 without interpolation.
    
    """

class IERS20032010PrecessionNutation(PrecessionNutationModel):
    """
    public class IERS20032010PrecessionNutation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
    
        This class implement the IERS 2003 and 2010 CIRF Precession Nutation models.
    
        The computations of this class are very heavy. It should not be used directly but only through
        :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationInterpolation` that will
        perform a limited number of access to this class.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, precessionNutationConvention: PrecessionNutationConvention): ...
    @typing.overload
    def __init__(self, precessionNutationConvention: PrecessionNutationConvention, boolean: bool): ...
    def getCIPCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> CIPCoordinates:
        """
            Getter for the CIP coordinates at the provided date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getCIPCoordinates` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date for the CIP coordinates
        
            Returns:
                the CIP coordinates
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Return computation type : direct or interpolated.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.isDirect` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                true if direct computation, false if interpolated
        
        
        """
        ...

class NoPrecessionNutation(PrecessionNutationModel):
    """
    public class NoPrecessionNutation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
    
        In this model the CIP doesn't move. This class is to be used for GCRF to CIRF transformation.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getCIPCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> CIPCoordinates:
        """
            Getter for the CIP coordinates at the provided date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getCIPCoordinates` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date for the CIP coordinates
        
            Returns:
                the CIP coordinates
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Return computation type : direct or interpolated.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.isDirect` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                true if direct computation, false if interpolated
        
        
        """
        ...

class PrecessionNutationCache(PrecessionNutationModel):
    """
    Deprecated. 
    since 4.13 as the precession nutation corrections cache management is deported in the
    :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationInterpolation` class which
    uses a more efficient :class:`~fr.cnes.sirius.patrius.time.interpolation.TimeStampedInterpolableEphemeris` cache system.
    `@Deprecated <http://docs.oracle.com/javase/8/docs/api/java/lang/Deprecated.html?is-external=true>` public class PrecessionNutationCache extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
    
        Cache for precession nutation correction computation. This class is to be used for GCRF to CIRF transformation.
    
        This implementation includes a caching/interpolation feature to tremendously improve efficiency. The IAU-2000 model
        involves lots of terms (1600 components for x, 1275 components for y and 66 components for s). Recomputing all these
        components for each point is really slow. The shortest period for these components is about 5.5 days (one fifth of the
        moon revolution period), hence the pole motion is smooth at the day or week scale. This implies that these motions can
        be computed accurately using a few reference points per day or week and interpolated between these points. This
        implementation uses 12 points separated by 1/2 day (43200 seconds) each, the resulting maximal interpolation error on
        the frame is about 1.3×10 :sup:`-10` arcseconds. *-- Orekit*
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, precessionNutationModel: PrecessionNutationModel): ...
    @typing.overload
    def __init__(self, precessionNutationModel: PrecessionNutationModel, double: float, int: int): ...
    def getCIPCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> CIPCoordinates:
        """
            Deprecated. 
            Getter for the CIP coordinates at the provided date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getCIPCoordinates` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date for the CIP coordinates
        
            Returns:
                the CIP coordinates
        
        
        """
        ...
    def getCIPMotion(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]:
        """
            Deprecated. 
            Compute the Celestial Intermediate pole motion in the GCRS.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date for the CIP motion
        
            Returns:
                CIP motion as an array of doubles
        
        
        """
        ...
    def getCIPMotionTimeDerivative(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]:
        """
            Deprecated. 
            Compute the Celestial Intermediate pole motion in the GCRS.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date for the CIP motion time derivatives
        
            Returns:
                CIP motion time derivatives as an array of doubles
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Deprecated. 
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Deprecated. 
            Return computation type : direct or interpolated.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.isDirect` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                true if direct computation, false if interpolated
        
        
        """
        ...

class PrecessionNutationInterpolation(PrecessionNutationModel):
    """
    public class PrecessionNutationInterpolation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
    
        Precession nutation correction computation through an interpolation process.
    
        This implementation includes a caching/interpolation feature to tremendously improve efficiency. The IAU-2000 model
        involves lots of terms (1600 components for x, 1275 components for y and 66 components for s). Recomputing all these
        components for each point is really slow. The shortest period for these components is about 5.5 days (one fifth of the
        moon revolution period), hence the pole motion is smooth at the day or week scale. This implies that these motions can
        be computed accurately using a few reference points per day or week and interpolated between these points. This
        implementation uses 4 points (CIP and CIP velocities) separated by 1/2 day (43200 seconds) each, the resulting maximal
        interpolation error on the frame is about 1.3×10 :sup:`-10` arcseconds.
    
        Some information about performance: The CIP coordinates are interpolated thanks to reference CIPCoordinates that we will
        call "references".
    
    
        These references are computed in function of the needs for the interpolation. For implementation simplicity, it is
        imposed that there is no holes between references. Thus, if dates are too apart from each other (more than
        :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationInterpolation.allowedExtensionBeforeEphemerisReset`
        holes to be filled), the references are reinitialized. As a consequence, if the dates are erratically spread, it is
        advised to pre-initialize the reference values with :code:`#initializeCipEphemeris` in order to avoid too many
        re-initializations of the references.
    
    
        Another aspect is that if the required dates are separated of more than the
        :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationInterpolation.getInterpolationStep`,
        the interpolation management will not be efficient and it is advised to use a direct
        :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel` instead.
    
        Since:
            4.13
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_INTERP_ORDER: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_INTERP_ORDER
    
        Default number of interpolation points.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_INTERP_STEP: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_INTERP_STEP
    
        Default time span between generated reference points.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_EPHEM_MAX_SIZE: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_EPHEM_MAX_SIZE
    
        Default ephemeris max size before resetting for memory usage purpose.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_ALLOWED_EXTENSION_BEFORE_EPHEM_RESET: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_ALLOWED_EXTENSION_BEFORE_EPHEM_RESET
    
        Default allowed extra CIPCoordinates to compute in order to keep the same ephemeris.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, precessionNutationModel: PrecessionNutationModel): ...
    @typing.overload
    def __init__(self, precessionNutationModel: PrecessionNutationModel, int: int, int2: int, int3: int, int4: int): ...
    def getAllowedExtensionBeforeEphemerisReset(self) -> int:
        """
            Getter for the maximum allowed reference extensions before reinitialization.
        
            Returns:
                the maximum allowed reference extensions before reinitialization
        
        
        """
        ...
    def getCIPCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> CIPCoordinates:
        """
            Getter for the CIP coordinates at the provided date.
        
            This method is thread-safe.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getCIPCoordinates` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date for the CIP coordinates
        
            Returns:
                the CIP coordinates
        
        
        """
        ...
    def getCurrentUsableInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Getter for the current usable interval of the ephemeris.
        
            Returns:
                the current usable interval of the ephemeris. Can be :code:`null` if the ephemeris has not been initialized yet.
        
        
        """
        ...
    def getEphemerisCacheReusabilityRatio(self) -> float:
        """
            Getter for the cache reusability ratio.
        
        
            See :meth:`~fr.cnes.sirius.patrius.time.interpolation.TimeStampedInterpolableEphemeris.getCacheReusabilityRatio` for
            more information.
        
            Returns:
                the reusability ratio
        
        
        """
        ...
    def getEphemerisMaxSize(self) -> int:
        """
            Getter for the maximal internal reference values size before reinitialization.
        
            Returns:
                the maximal internal reference values size before reinitialization
        
        
        """
        ...
    def getEphemerisSize(self) -> int:
        """
            Getter for the ephemeris size.
        
            Returns:
                the ephemeris size
        
        
        """
        ...
    def getInterpolationOrder(self) -> int:
        """
            Getter for the interpolation order.
        
            Returns:
                the interpolation order
        
        
        """
        ...
    def getInterpolationStep(self) -> int:
        """
            Getter for the interpolation step.
        
            Returns:
                the interpolation step
        
        
        """
        ...
    def getModel(self) -> PrecessionNutationModel:
        """
            Getter for the internal precession nutation model.
        
            Returns:
                the internal precession nutation model
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def initializeCIPEphemeris(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Pre-initialize (optional) the CIP coordinates for a given interval for performance purpose.
        
            Can be useful when CIP coordinates are required at very different dates that would lead to multiple ephemeris
            re-initializations (with regards to the
            :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationInterpolation.allowedExtensionBeforeEphemerisReset`.
        
        
            Calling this method does not prevent the class to extend the ephemeris, it is just a way to reduce the re-initialization
            occurrences.
        
            This method is thread-safe.
        
            Parameters:
                firstUsableDate (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): First usable date of the ephemeris
                lastUsableDate (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Last usable date of the ephemeris
        
            Raises:
                : if the ephemeris exceeds the maximum allowed size
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Return computation type : direct or interpolated.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.isDirect` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                true if direct computation, false if interpolated
        
        
        """
        ...

class PrecessionNutationPerThread(PrecessionNutationModel):
    """
    public abstract class PrecessionNutationPerThread extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
    
        Provides per-thread PrecessionNutationCorrectionModel. This class is to be used for GCRF to CIRF transformation.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getCIPCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> CIPCoordinates:
        """
            Getter for the CIP coordinates at the provided date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getCIPCoordinates` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date for the CIP coordinates
        
            Returns:
                the CIP coordinates
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Return computation type : direct or interpolated.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.isDirect` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                true if direct computation, false if interpolated
        
        
        """
        ...

class StelaPrecessionNutationModel(PrecessionNutationModel):
    """
    public final class StelaPrecessionNutationModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
    
        STELA specific precession/nutation model. This class is to be used for GCRF to CIRF transformation.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getCIPCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> CIPCoordinates:
        """
            Description copied from
            interface: :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getCIPCoordinates`
            Getter for the CIP coordinates at the provided date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getCIPCoordinates` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date for the CIP coordinates
        
            Returns:
                the CIP coordinates
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.frames.configuration.FrameConvention:
        """
            Get IERS model origin.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.getOrigin` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                IERS model origin
        
        
        """
        ...
    def isDirect(self) -> bool:
        """
            Return computation type : direct or interpolated.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel.isDirect` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.precessionnutation.PrecessionNutationModel`
        
            Returns:
                true if direct computation, false if interpolated
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.frames.configuration.precessionnutation")``.

    CIPCoordinates: typing.Type[CIPCoordinates]
    CIPCoordinatesGenerator: typing.Type[CIPCoordinatesGenerator]
    IERS20032010PrecessionNutation: typing.Type[IERS20032010PrecessionNutation]
    NoPrecessionNutation: typing.Type[NoPrecessionNutation]
    PrecessionNutation: typing.Type[PrecessionNutation]
    PrecessionNutationCache: typing.Type[PrecessionNutationCache]
    PrecessionNutationConvention: typing.Type[PrecessionNutationConvention]
    PrecessionNutationInterpolation: typing.Type[PrecessionNutationInterpolation]
    PrecessionNutationModel: typing.Type[PrecessionNutationModel]
    PrecessionNutationModelFactory: typing.Type[PrecessionNutationModelFactory]
    PrecessionNutationPerThread: typing.Type[PrecessionNutationPerThread]
    StelaPrecessionNutationModel: typing.Type[StelaPrecessionNutationModel]
