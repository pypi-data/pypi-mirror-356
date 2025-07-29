
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.forces
import fr.cnes.sirius.patrius.forces.gravity.tides.coefficients
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import jpype
import typing



class IOceanTidesDataProvider(fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider):
    """
    public interface IOceanTidesDataProvider extends :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
    
    
        Interface that provides ocean tides inputs.
    
        Since:
            2.3.1
    """
    def getLoveNumbers(self) -> typing.MutableSequence[float]:
        """
            Get love numbers.
        
            Returns:
                the love numbers.
        
            Since:
                2.3.1
        
        
        """
        ...
    def getStandard(self) -> 'TidesStandards.TidesStandard':
        """
            Get the ocean tides standard
        
            Returns:
                the ocean tides standard
        
            Since:
                2.3.1
        
        
        """
        ...

class ITerrestrialTidesDataProvider(java.io.Serializable):
    """
    public interface ITerrestrialTidesDataProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface that provides terrestrial tides inputs.
    
        Since:
            1.2
    """
    def getAnelasticityCorrectionLoveNumber2(self) -> typing.MutableSequence[float]:
        """
            Get second degree Love number for the third body perturbation.
        
            Returns:
                a table of Love numbers
        
        
        """
        ...
    def getAnelasticityCorrectionLoveNumber3(self) -> typing.MutableSequence[float]:
        """
            Get third degree Love number for the third body perturbation.
        
            Returns:
                a table of Love numbers
        
        
        """
        ...
    def getDoodsonNumbers(self) -> typing.MutableSequence[float]:
        """
            Get the Doodson numbers used by the standard.
        
            Returns:
                table of Doodson numbers.
        
        
        """
        ...
    def getEllipticityCorrectionLoveNumber2(self) -> typing.MutableSequence[float]:
        """
            Get second degree Love number for the ellipticity perturbation.
        
            Returns:
                a table of Love numbers
        
        
        """
        ...
    def getFrequencyCorrection(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Get the frequency corrections as a table of Love number corrections associated to a Doodson number i.e. a wave.
        
            Returns:
                a table of frequency corrections (for the considered wave, double[i][0] is the real part and double[i][1] is the
                imaginary part of Love number correction).
        
        
        """
        ...
    def getNutationCoefficients(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Get constant coefficients coming from the luni solar nutation theory in order to compute the fundamental arguments.
        
            Returns:
                a table of nutation coefficients
        
        
        """
        ...
    def getStandard(self) -> 'TidesStandards.TidesStandard':
        """
        
            Returns:
                the TidesStandard enum for this standard.
        
        
        """
        ...

class PotentialTimeVariations:
    """
    public interface PotentialTimeVariations
    
        Interface for perturbating forces that moficate the C and S coefficients over the time.
    
        Since:
            1.1
    """
    def updateCoefficientsCandS(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def updateCoefficientsCandSPD(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class ReferencePointsDisplacement:
    """
    public final class ReferencePointsDisplacement extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class provides the model describing the displacements of reference points due to the effect of the solid Earth
        tides.
    
        Since:
            1.2
    """
    @staticmethod
    def poleTidesCorrections(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @staticmethod
    def solidEarthTidesCorrections(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class TidesStandards:
    """
    public class TidesStandards extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Tides standards
    
        Since:
            1.2
    """
    def __init__(self): ...
    class TidesStandard(java.lang.Enum['TidesStandards.TidesStandard']):
        IERS1996: typing.ClassVar['TidesStandards.TidesStandard'] = ...
        IERS2003: typing.ClassVar['TidesStandards.TidesStandard'] = ...
        GINS2004: typing.ClassVar['TidesStandards.TidesStandard'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'TidesStandards.TidesStandard': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['TidesStandards.TidesStandard']: ...

class TidesToolbox:
    """
    public final class TidesToolbox extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Tides toolbox
    
        Since:
            2.1
    """
    @staticmethod
    def computeFundamentalArguments(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, tidesStandard: TidesStandards.TidesStandard) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @staticmethod
    def computeNutationArguments(double: float, tidesStandard: TidesStandards.TidesStandard) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Method to compute the fundamental arguments from the luni-solar nutation theory.
        
            Parameters:
                jd (double): duration from the J2000 epoch to the given date with TT scale in julian days
                standard (:class:`~fr.cnes.sirius.patrius.forces.gravity.tides.TidesStandards.TidesStandard`): the tides standard to use
        
            Returns:
                a table of the nutation arguments and their first and second derivatives in columns
        
        
        """
        ...
    @staticmethod
    def nDoodson(double: float) -> typing.MutableSequence[int]:
        """
            Doodson number decomposition as a sextuplet of integers. The six small integers multipliers encode the frequency of the
            tidal argument concerned and form the Doodson numbers: in practice all except the first are usually biased upwards by +5
            to avoid negative numbers in the notation. (In the case that the biased multiple exceeds 9, the system adopts X for 10,
            and E for 11.) For example, the Doodson number 273.555 means that the tidal frequency is composed of twice the first
            Doodson argument, +2 times the second, -2 times the third and zero times each of the other three. See
            http://en.wikipedia.org/wiki/Arthur_Thomas_Doodson
        
            Parameters:
                doodsonNumber (double): : Doodson number (xxx.xxx)
        
            Returns:
                Doodson sextuplet
        
        
        """
        ...

class AbstractTides(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable, fr.cnes.sirius.patrius.forces.ForceModel, fr.cnes.sirius.patrius.forces.GradientModel, PotentialTimeVariations):
    """
    public abstract class AbstractTides extends :class:`~fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.forces.GradientModel`, :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.PotentialTimeVariations`
    
    
        Common handling of :class:`~fr.cnes.sirius.patrius.forces.ForceModel` methods for tides models.
    
        This abstract class allows to provide easily the full set of :class:`~fr.cnes.sirius.patrius.forces.ForceModel` methods
        to tides models. Only one method must be implemented by derived classes:
        :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.AbstractTides.updateCoefficientsCandS`.
    
        Since:
            2.3
    
        Also see:
            :meth:`~serialized`
    """
    MU: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` MU
    
        Parameter name for central attraction coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    RADIUS: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` RADIUS
    
        Parameter name for equatorial radius.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    @typing.overload
    def computeAcceleration(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Parameters:
                pv (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`): PV coordinates of the spacecraft
                frame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): frame in which the acceleration is computed
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                acceleration vector
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if an Orekit error occurs
        
        
        """
        ...
    def computeGradientVelocity(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to velocity have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientVelocity` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def getEventsDetectors(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.events.EventDetector]:
        """
            Get the discrete events related to the model.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.ForceModel.getEventsDetectors` in
                interface :class:`~fr.cnes.sirius.patrius.forces.ForceModel`
        
            Returns:
                array of events detectors or null if the model is not related to any discrete events
        
        
        """
        ...
    def updateCoefficientsCandS(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def updateCoefficientsCandSPD(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class OceanTidesDataProvider(IOceanTidesDataProvider):
    """
    public class OceanTidesDataProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.IOceanTidesDataProvider`
    
    
        Ocean tides parameters given by the IERS 1996, 2003 or GINS 2004 standard.
    
        Since:
            2.3.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, oceanTidesCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider, tidesStandard: TidesStandards.TidesStandard): ...
    def getCpmEpm(self, double: float, int: int, int2: int) -> typing.MutableSequence[float]:
        """
            Get the C :sub:`lm` :sup:`±` and ε :sub:`lm` :sup:`±` for given wave
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getCpmEpm` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Parameters:
                nDoodson (double): doodson number doodson number
                l (int): order
                m (int): degree
        
            Returns:
                double[4] array containing {C :sub:`lm` :sup:`+` , C :sub:`lm` :sup:`-` , ε :sub:`lm` :sup:`+` , ε :sub:`lm` :sup:`-` }
        
        
        """
        ...
    def getCpmSpm(self, double: float, int: int, int2: int) -> typing.MutableSequence[float]:
        """
            Get the C :sub:`lm` :sup:`±` and S :sub:`lm` :sup:`±` for given wave
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getCpmSpm` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Parameters:
                nDoodson (double): doodson number
                l (int): order
                m (int): degree
        
            Returns:
                double[4] array containing {C :sub:`lm` :sup:`+` , C :sub:`lm` :sup:`-` , S :sub:`lm` :sup:`+` , S :sub:`lm` :sup:`-` }
        
        
        """
        ...
    def getDoodsonNumbers(self) -> typing.MutableSequence[float]:
        """
            Get available Doodson numbers
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getDoodsonNumbers` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Returns:
                array of Doodson numbers
        
        
        """
        ...
    def getLoveNumbers(self) -> typing.MutableSequence[float]:
        """
            Get love numbers.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.IOceanTidesDataProvider.getLoveNumbers` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.IOceanTidesDataProvider`
        
            Returns:
                the love numbers.
        
        
        """
        ...
    def getMaxDegree(self, double: float, int: int) -> int:
        """
            Get maximum degree for given wave and order
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getMaxDegree` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Parameters:
                doodson (double): number
                order (int): of wave
        
            Returns:
                Max degree for given wave
        
        
        """
        ...
    def getMaxOrder(self, double: float) -> int:
        """
            Get maximum order for given wave
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getMaxOrder` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Parameters:
                doodson (double): number
        
            Returns:
                Max order for given wave
        
        
        """
        ...
    def getMinDegree(self, double: float, int: int) -> int:
        """
            Get min degree for given wave and order
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getMinDegree` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Parameters:
                doodson (double): number
                order (int): of wave
        
            Returns:
                Min degree for given wave
        
        
        """
        ...
    def getStandard(self) -> TidesStandards.TidesStandard:
        """
            Get the ocean tides standard
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.IOceanTidesDataProvider.getStandard` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.IOceanTidesDataProvider`
        
            Returns:
                the ocean tides standard
        
        
        """
        ...

class TerrestrialTidesDataProvider(ITerrestrialTidesDataProvider):
    """
    public final class TerrestrialTidesDataProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider`
    
    
        Terrestrial tides parameters given by the IERS 2003 standard.
    
        Since:
            2.3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, tidesStandard: TidesStandards.TidesStandard): ...
    def getAnelasticityCorrectionLoveNumber2(self) -> typing.MutableSequence[float]:
        """
            Get second degree Love number for the third body perturbation.
        
            Specified by:
                
                meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider.getAnelasticityCorrectionLoveNumber2` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider`
        
            Returns:
                a table of Love numbers
        
        
        """
        ...
    def getAnelasticityCorrectionLoveNumber3(self) -> typing.MutableSequence[float]:
        """
            Get third degree Love number for the third body perturbation.
        
            Specified by:
                
                meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider.getAnelasticityCorrectionLoveNumber3` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider`
        
            Returns:
                a table of Love numbers
        
        
        """
        ...
    def getDoodsonNumbers(self) -> typing.MutableSequence[float]:
        """
            Get the Doodson numbers used by the standard.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider.getDoodsonNumbers` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider`
        
            Returns:
                table of Doodson numbers.
        
        
        """
        ...
    def getEllipticityCorrectionLoveNumber2(self) -> typing.MutableSequence[float]:
        """
            Get second degree Love number for the ellipticity perturbation.
        
            Specified by:
                
                meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider.getEllipticityCorrectionLoveNumber2` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider`
        
            Returns:
                a table of Love numbers
        
        
        """
        ...
    def getFrequencyCorrection(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Get the frequency corrections as a table of Love number corrections associated to a Doodson number i.e. a wave.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider.getFrequencyCorrection` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider`
        
            Returns:
                a table of frequency corrections (for the considered wave, double[i][0] is the real part and double[i][1] is the
                imaginary part of Love number correction).
        
        
        """
        ...
    def getNutationCoefficients(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Get constant coefficients coming from the luni solar nutation theory in order to compute the fundamental arguments.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider.getNutationCoefficients` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider`
        
            Returns:
                a table of nutation coefficients
        
        
        """
        ...
    def getStandard(self) -> TidesStandards.TidesStandard:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider.getStandard` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.ITerrestrialTidesDataProvider`
        
            Returns:
                the TidesStandard enum for this standard.
        
        
        """
        ...

class OceanTides(AbstractTides):
    """
    public class OceanTides extends :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.AbstractTides`
    
        This class implements the perturbating force due to ocean tides.
    
        The implementation of this class enables the computation of partial derivatives by finite differences with respect to
        the **central attraction coefficient**.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    RHO: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` RHO
    
        Parameter name for Density at surface.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, double3: float, int: int, int2: int, boolean: bool, iOceanTidesDataProvider: IOceanTidesDataProvider): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, double3: float, int: int, int2: int, int3: int, int4: int, boolean: bool, iOceanTidesDataProvider: IOceanTidesDataProvider): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter, int: int, int2: int, boolean: bool, iOceanTidesDataProvider: IOceanTidesDataProvider): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter, int: int, int2: int, int3: int, int4: int, boolean: bool, iOceanTidesDataProvider: IOceanTidesDataProvider): ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def getDenormalizedCCoefs(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getDenormalizedSCoefs(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getNormalizedCCoefs(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getNormalizedSCoefs(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getOceanTidesData(self) -> IOceanTidesDataProvider:
        """
        
            Returns:
                the oceanTidesData
        
        
        """
        ...
    def updateCoefficientsCandS(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def updateCoefficientsCandSPD(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class PoleTides(AbstractTides):
    """
    public class PoleTides extends :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.AbstractTides`
    
        This class implements the perturbating force due to pole tides. Pole tide is the deformation of the Earth due to the
        movement of its rotation axis. Polar tides directly depends on Earth pole position (xp, yp) and have two contributors:
    
          - Solid Earth pole tides
          - Earth ocean pole tides
    
        It is possible to activate/deactivate each of these contributors through flags at construction.
    
        Since:
            4.6
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, boolean: bool, boolean2: bool): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, boolean: bool, boolean2: bool, boolean3: bool): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, boolean: bool, boolean2: bool): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, boolean: bool, boolean2: bool, boolean3: bool): ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def updateCoefficientsCandS(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def updateCoefficientsCandSPD(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class TerrestrialTides(AbstractTides):
    """
    public class TerrestrialTides extends :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.AbstractTides`
    
        This class implements the perturbating force due to terrestrial tides (deformation due to third body attraction on an
        aneslatic crust, ellipticity correction, frequency correction). It is possible to activate/deactivate one of these
        corrections. At least the model take into account the deformation due to the moon and the sun attraction up to degree 2.
    
        The implementation of this class enables the computation of partial derivatives by finite differences with respect to
        the **central attraction coefficient**.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, boolean: bool): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, list: java.util.List[fr.cnes.sirius.patrius.bodies.CelestialPoint], boolean: bool, boolean2: bool, boolean3: bool, iTerrestrialTidesDataProvider: ITerrestrialTidesDataProvider): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, list: java.util.List[fr.cnes.sirius.patrius.bodies.CelestialPoint], boolean: bool, boolean2: bool, boolean3: bool, iTerrestrialTidesDataProvider: ITerrestrialTidesDataProvider, boolean4: bool): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, boolean: bool): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, list: java.util.List[fr.cnes.sirius.patrius.bodies.CelestialPoint], boolean: bool, boolean2: bool, boolean3: bool, iTerrestrialTidesDataProvider: ITerrestrialTidesDataProvider): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, list: java.util.List[fr.cnes.sirius.patrius.bodies.CelestialPoint], boolean: bool, boolean2: bool, boolean3: bool, iTerrestrialTidesDataProvider: ITerrestrialTidesDataProvider, boolean4: bool): ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def updateCoefficientsCandS(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def updateCoefficientsCandSPD(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.gravity.tides")``.

    AbstractTides: typing.Type[AbstractTides]
    IOceanTidesDataProvider: typing.Type[IOceanTidesDataProvider]
    ITerrestrialTidesDataProvider: typing.Type[ITerrestrialTidesDataProvider]
    OceanTides: typing.Type[OceanTides]
    OceanTidesDataProvider: typing.Type[OceanTidesDataProvider]
    PoleTides: typing.Type[PoleTides]
    PotentialTimeVariations: typing.Type[PotentialTimeVariations]
    ReferencePointsDisplacement: typing.Type[ReferencePointsDisplacement]
    TerrestrialTides: typing.Type[TerrestrialTides]
    TerrestrialTidesDataProvider: typing.Type[TerrestrialTidesDataProvider]
    TidesStandards: typing.Type[TidesStandards]
    TidesToolbox: typing.Type[TidesToolbox]
    coefficients: fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.__module_protocol__
