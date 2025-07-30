
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.signalpropagation
import fr.cnes.sirius.patrius.time
import java.util
import jpype
import typing



_AbstractMeteoBasedCorrectionFactory__T = typing.TypeVar('_AbstractMeteoBasedCorrectionFactory__T')  # <T>
class AbstractMeteoBasedCorrectionFactory(typing.Generic[_AbstractMeteoBasedCorrectionFactory__T]):
    """
    public abstract class AbstractMeteoBasedCorrectionFactory<T> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Meteorologically based correction model factory.
    
        This class can initialize and store in cache meteorologically based correction models.
    
        The correction models are organized within a `null
        <http://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ConcurrentHashMap.html?is-external=true>` to ensure
        multi-thread safety.
    
        Since:
            4.13
    """
    def __init__(self): ...
    def getCorrectionModel(self, meteorologicalConditionsProvider: typing.Union[fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider, typing.Callable], bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint) -> _AbstractMeteoBasedCorrectionFactory__T:
        """
            Getter for a meteorologically based correction model.
        
            This method looks if the required model is already initialized.
        
        
            If it's the case the model is directly returned, otherwise the model is initialized, stored and returned.
        
            Parameters:
                meteoConditionsProvider (:class:`~fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider`): Provider for the meteorological conditions
                point (:class:`~fr.cnes.sirius.patrius.bodies.BodyPoint`): Point
        
            Returns:
                the correction model
        
        
        """
        ...

class AstronomicalRefractionModel(fr.cnes.sirius.patrius.signalpropagation.FiniteDistanceAngularCorrection):
    """
    public class AstronomicalRefractionModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.signalpropagation.FiniteDistanceAngularCorrection`
    
        This class represent a tropospheric refraction model. It is directly extracted from [1].
    
        This class uses interpolation tables. Be aware that it accepts extrapolation of these table to some extent. When the
        extrapolation is likely to go too far compared to the table resolution, a verification is done. This is the case for the
        maximum zenithal distance and the wavelength of the signal. For the other values, no check is performed.
    
        **Source:** [1] "Introduction aux ephemerides astronomiques" Bureau des longitudes, edition 1997"
    
        All private methods will use the units of the source (which are often not SI) to keep as close as possible to the book
        formulas. All public methods will use international units.
    
        Since:
            4.13
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_THRESHOLD: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_THRESHOLD
    
        Default threshold value for the iterative algorithm used to compute the elevation correction from geometric elevation
        [rad].
    
    
        Justification: This tropospheric model is essentially used for Astrometric TAROT measurements. The precision of these
        measurements is currently around 1e-6 rad. It is safe to take 2 orders of magnitude lower than this precision.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_MAX_ITER: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_MAX_ITER
    
        Default max iteration number for the iterative algorithm used to compute the elevation correction from geometric
        elevation.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint, meteorologicalConditionsProvider: typing.Union[fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider, typing.Callable], double: float): ...
    @typing.overload
    def __init__(self, bodyPoint: fr.cnes.sirius.patrius.bodies.BodyPoint, meteorologicalConditionsProvider: typing.Union[fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider, typing.Callable], double: float, double2: float, int: int): ...
    @typing.overload
    def computeElevationCorrectionFromApparentElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float:
        """
            Compute the tropospheric correction from the apparent elevation and distance.
        
            This method takes into account the finite distance of the observed object to add a parallax correction.
        
            Specified by:
                
                meth:`~fr.cnes.sirius.patrius.signalpropagation.FiniteDistanceAngularCorrection.computeElevationCorrectionFromApparentElevation` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.FiniteDistanceAngularCorrection`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date at which we want to compute the tropospheric correction
                apparentElevation (double): The apparent elevation (with atmosphere) [rad]
                distance (double): The distance to the object [m]. Can be `null
                    <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#POSITIVE_INFINITY>` (equivalent to not
                    take into account the parallax correction)
        
            Returns:
                the elevation correction [rad] so that : :code:`apparent_elevation = geometric_elevation + elevation_correction`
        
            Compute the tropospheric correction from the apparent elevation and the provided conditions.
        
            This method takes into account the finite distance of the observed object to add a parallax correction.
        
            Parameters:
                apparentElevation (double): The apparent elevation [rad]
                pressure (double): The pressure [Pa]
                temperature (double): The temperature [K°]
                relativeHumidity (double): The relative humidity (from 0 to 100) [%]
                wavelengthNanometer (double): The wavelength [nanometer]
                latitude (double): The latitude [rad]
                altitude (double): The altitude [m]
                distance (double): The distance of the observed object [m]. Can be `null
                    <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#POSITIVE_INFINITY>` (equivalent to not
                    take into account the parallax correction).
        
            Returns:
                the elevation correction [rad] so that : :code:`apparentElevation = geometricElevation + elevationCorrection`
        
            Raises:
                : if the apparent zenithal distance is greater than the maximum apparent zenithal distance allowed for tables linear
                    extrapolations
        
        
        if the provided wavelength is outside the tolerated wavelength bound for tables linear extrapolations
        
        
        """
        ...
    @typing.overload
    def computeElevationCorrectionFromApparentElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def computeElevationCorrectionFromApparentElevation(double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float) -> float: ...
    @typing.overload
    def computeElevationCorrectionFromGeometricElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float:
        """
            Compute the tropospheric correction from the geometric elevation and distance.
        
            Note that this method uses an iterative algorithm to convert the geometric elevation into an apparent elevation. Note
            that if the convergence is not reached within the
            :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.AstronomicalRefractionModel.getMaxIter`, no exception is
            thrown.
        
            This method takes into account the finite distance of the observed object to add a parallax correction.
        
            Specified by:
                
                meth:`~fr.cnes.sirius.patrius.signalpropagation.FiniteDistanceAngularCorrection.computeElevationCorrectionFromGeometricElevation` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.FiniteDistanceAngularCorrection`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date at which we want to compute the tropospheric correction
                geometricElevation (double): The geometric elevation (without atmosphere) [rad]
                distance (double): The distance to the object [m]. Can be `null
                    <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#POSITIVE_INFINITY>` (equivalent to not
                    take into account the parallax correction).
        
            Returns:
                the elevation correction [rad] so that : :code:`apparent_elevation = geometric_elevation + elevation_correction`
        
            Compute the tropospheric correction from the geometric elevation and the provided conditions.
        
            The input is the geometric elevation while the model takes the apparent elevation as an input. An iterative algorithm
            (fix point) is used to call the model with the apparent elevation, hence the threshold and maxIter arguments. Note that
            if the convergence is not reached within the maxIter, no exception is thrown.
        
            This method takes into account the finite distance of the observed object to add a parallax correction.
        
            Parameters:
                geometricElevation (double): The geometric elevation [rad]
                pressure (double): The pressure [Pa]
                temperature (double): The temperature [K°]
                relativeHumidity (double): The relative humidity (from 0 to 100) [%]
                wavelengthNanometer (double): The wavelength [nanometer]
                latitude (double): The latitude [rad]
                altitude (double): The altitude [m]
                distance (double): The distance of the observed object [m]. Can be `null
                    <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#POSITIVE_INFINITY>` (equivalent to not
                    take into account the parallax correction).
                threshold (double): Threshold for the iterative algorithm [rad]
                maxIter (int): Max iteration number
        
            Returns:
                the geometric elevation [rad]
        
        
        """
        ...
    @typing.overload
    def computeElevationCorrectionFromGeometricElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def computeElevationCorrectionFromGeometricElevation(double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float, int: int) -> float: ...
    @staticmethod
    def computeGroundRefractivity(double: float, double2: float, double3: float) -> float:
        """
            Compute the ground refractivity by taking into account elevation, pressure and temperature.
        
            See [1] p. 194 Equation (7.3.9)
        
            Parameters:
                apparentElevation (double): The apparent elevation (with atmosphere) [rad]
                pressure (double): The pressure [Pa]
                temperature (double): The temperature [K°]
        
            Returns:
                the ground refraction [dimensionless]
        
        
        """
        ...
    @staticmethod
    def computeOOPrime(double: float, double2: float, double3: float) -> float:
        """
            Compute the OO' distance.
        
            This distance aims at computing a parallax effect for the elevation correction at finite distance.
        
            See [1] p.203 Equation (7.3.19)
        
            Parameters:
                groundRefractivity (double): The ground refractivity [dimensionless]
                elevationCorrection (double): The apparent elevation correction for an object at an infinite distance [rad]
                apparentElevation (double): Apparent elevation (with atmosphere) (for an object at infinite distance) [rad]
        
            Returns:
                the distance OO' [m]
        
        
        """
        ...
    @staticmethod
    def computeParallaxCorrection(double: float, double2: float, double3: float) -> float:
        """
            Compute the parallax correction due to a finite distance object.
        
            Parameters:
                geometricElevation (double): The geometric elevation (without atmosphere) (for an object at infinite distance) [rad]
                oOPrime (double): The fictive distance to compute the parallax [m]
                distance (double): The distance to the object [m]
        
            Returns:
                the parallax correction so that : :code:`elevationFiniteDistance = elevationInfiniteDistance + parallax`
        
        
        """
        ...
    def derivativeValueFromApparentElevation(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> float:
        """
            Compute the elevation correction derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection.derivativeValueFromApparentElevation` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): Parameter
                elevation (double): The apparent elevation (with atmosphere) of the satellite [rad]
        
            Returns:
                the elevation derivative value
        
        
        """
        ...
    def derivativeValueFromGeometricElevation(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> float:
        """
            Compute the elevation correction derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection.derivativeValueFromGeometricElevation` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): Parameter
                geometricElevation (double): The geometric elevation (without atmosphere) of the satellite [rad]
        
            Returns:
                the elevation derivative value
        
        
        """
        ...
    @staticmethod
    def elevationToZenithalDistance(double: float) -> float:
        """
            Convert elevation to zenithal distance [rad].
        
            Parameters:
                elevation (double): The elevation [rad]
        
            Returns:
                the zenithal distance
        
        
        """
        ...
    def getMaxIter(self) -> int:
        """
            Getter for the maximum iteration number used in the convergence algorithm to compute the correction from the geometric
            elevation.
        
            Note that if the convergence is not reached within this max iteration number, no exception is thrown.
        
            Returns:
                the maximum iteration number
        
        
        """
        ...
    def getMeteoConditionsProvider(self) -> fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider:
        """
            Getter for the meteo conditions provider.
        
            Returns:
                the meteo conditions provider
        
        
        """
        ...
    def getMinimalToleratedApparentElevation(self) -> float:
        """
            Getter for the minimal tolerated apparent elevation for this model (some models cannot compute correction for too low
            elevations).
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection.getMinimalToleratedApparentElevation` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
        
            Returns:
                the minimal tolerated apparent elevation [rad]
        
        
        """
        ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def getPoint(self) -> fr.cnes.sirius.patrius.bodies.BodyPoint:
        """
            Getter for the position where the model should be applied.
        
            Returns:
                the point where the model should be applied
        
        
        """
        ...
    def getThreshold(self) -> float:
        """
            Getter for the threshold used in the convergence algorithm to compute the correction from the geometric elevation.
        
            Returns:
                the threshold [rad]
        
        
        """
        ...
    def getWavelengthNanometer(self) -> float:
        """
            Getter for the wavelength [nanometer].
        
            Returns:
                the wavelength
        
        
        """
        ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Tell if the function is differentiable by the given parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection.isDifferentiableBy` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): Parameter
        
            Returns:
                :code:`true` if the function is differentiable by the given parameter
        
        
        """
        ...
    def supportsParameter(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Check if a parameter is supported.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable.supportsParameter` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
        
            Parameters:
                param (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to check
        
            Returns:
                true if the parameter is supported
        
        
        """
        ...
    @staticmethod
    def zenithalDistanceToElevation(double: float) -> float:
        """
            Convert zenithal distance to elevation [rad].
        
            Parameters:
                zenithalDistance (double): The zenithal distance [rad]
        
            Returns:
                the elevation
        
        
        """
        ...

class TroposphericCorrection(fr.cnes.sirius.patrius.math.parameter.IParameterizable):
    """
    public interface TroposphericCorrection extends :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
    
        Defines a tropospheric model, used to calculate the signal delay for the signal path imposed to electro-magnetic signals
        between an orbital satellite and a ground station.
    """
    def computeSignalDelay(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float:
        """
            Calculates the tropospheric signal delay for the signal path from a ground station to a satellite at a given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date of meteo conditions
                elevation (double): the elevation of the satellite [rad]
        
            Returns:
                the signal delay due to the troposphere [s]
        
        
        """
        ...
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> float:
        """
            Compute the signal delay derivative value with respect to the input parameter.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter
                elevation (double): the elevation of the satellite [rad]
        
            Returns:
                the derivative value
        
        
        """
        ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Tell if the function is differentiable by the given parameter.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): function parameter
        
            Returns:
                true if the function is differentiable by the given parameter.
        
        
        """
        ...

class AstronomicalRefractionModelFactory(AbstractMeteoBasedCorrectionFactory[AstronomicalRefractionModel]):
    """
    public class AstronomicalRefractionModelFactory extends :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.AbstractMeteoBasedCorrectionFactory`<:class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.AstronomicalRefractionModel`>
    
        This class describes the :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.AstronomicalRefractionModel`
        correction factory.
    
        Since:
            4.13
    """
    def __init__(self, double: float): ...

class AzoulayModel(TroposphericCorrection, fr.cnes.sirius.patrius.signalpropagation.AngularCorrection):
    """
    public final class AzoulayModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`, :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
    
        This class is a tropospheric correction model that implements the TroposphericCorrection and AngularCorrection
        interfaces to correct a signal with the Azoulay model.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, meteorologicalConditionsProvider: typing.Union[fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider, typing.Callable], double: float): ...
    @typing.overload
    def __init__(self, meteorologicalConditionsProvider: typing.Union[fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider, typing.Callable], double: float, boolean: bool): ...
    def computeElevationCorrectionFromApparentElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float:
        """
            Compute the angular correction from the apparent elevation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection.computeElevationCorrectionFromApparentElevation` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date at which we want to compute the angular correction
                apparentElevation (double): The apparent elevation (with atmosphere) [rad]
        
            Returns:
                the elevation correction [rad] so that :code:`apparent_elevation = geometric_elevation + elevation_correction`
        
        
        """
        ...
    def computeElevationCorrectionFromGeometricElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float:
        """
            Compute the angular correction from the geometric elevation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection.computeElevationCorrectionFromGeometricElevation` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date at which we want to compute the angular correction
                geometricElevation (double): The geometric elevation (without atmosphere) [rad]
        
            Returns:
                the elevation correction [rad] so that :code:`apparent_elevation = geometric_elevation + elevation_correction`
        
        
        """
        ...
    def computeSignalDelay(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float:
        """
            Calculates the tropospheric signal delay for the signal path from a ground station to a satellite at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.computeSignalDelay` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date of meteo conditions
                elevation (double): the elevation of the satellite [rad]
        
            Returns:
                the signal delay due to the troposphere [s]
        
        
        """
        ...
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> float:
        """
            Compute the signal delay derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.derivativeValue` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter
                elevation (double): the elevation of the satellite [rad]
        
            Returns:
                the derivative value
        
        
        """
        ...
    def derivativeValueFromApparentElevation(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> float:
        """
            Compute the elevation correction derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection.derivativeValueFromApparentElevation` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): Parameter
                elevation (double): The apparent elevation (with atmosphere) of the satellite [rad]
        
            Returns:
                the elevation derivative value
        
        
        """
        ...
    def derivativeValueFromGeometricElevation(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> float:
        """
            Compute the elevation correction derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection.derivativeValueFromGeometricElevation` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): Parameter
                geometricElevation (double): The geometric elevation (without atmosphere) of the satellite [rad]
        
            Returns:
                the elevation derivative value
        
        
        """
        ...
    def getCorrectionsFromApparentElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> typing.MutableSequence[float]:
        """
            Computes the corrections due to the troposphere from the apparent value of the elevation at a given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date of meteorological conditions
                apparentElevation (double): The apparent elevation (rad)
        
            Returns:
                an array that contains both corrections : :code:`(apparent elevation - geometric elevation), (apparent distance -
                geometric distance)`
        
        
        """
        ...
    def getCorrectionsFromGeometricElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> typing.MutableSequence[float]:
        """
            Computes the corrections due to the troposphere from the geometric value of the elevation at a given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Date of meteorological conditions
                geometricElevation (double): The geometric elevation [rad]
        
            Returns:
                an array that contains both corrections : :code:`(apparent elevation - geometric elevation), (apparent distance -
                geometric distance)`
        
        
        """
        ...
    def getMinimalToleratedApparentElevation(self) -> float:
        """
            Getter for the minimal tolerated apparent elevation for this model (some models cannot compute correction for too low
            elevations).
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection.getMinimalToleratedApparentElevation` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
        
            Returns:
                the minimal tolerated apparent elevation [rad]
        
        
        """
        ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Tell if the function is differentiable by the given parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection.isDifferentiableBy` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.isDifferentiableBy` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): function parameter
        
            Returns:
                true if the function is differentiable by the given parameter.
        
        
        """
        ...
    def supportsParameter(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Check if a parameter is supported.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable.supportsParameter` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
        
            Parameters:
                param (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to check
        
            Returns:
                true if the parameter is supported
        
        
        """
        ...

class AzoulayModelFactory(AbstractMeteoBasedCorrectionFactory[AzoulayModel]):
    """
    public class AzoulayModelFactory extends :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.AbstractMeteoBasedCorrectionFactory`<:class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.AzoulayModel`>
    
        This class describes the tropospheric correction factory around the
        :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.AzoulayModel`.
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...

class FixedDelayModel(TroposphericCorrection):
    """
    public class FixedDelayModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
    
        A static tropospheric model that interpolates the actual tropospheric delay based on values read from a configuration
        file (tropospheric-delay.txt) via the :class:`~fr.cnes.sirius.patrius.data.DataProvidersManager`.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double4: float): ...
    @typing.overload
    def __init__(self, string: str, double: float): ...
    def computePathDelay(self, double: float) -> float:
        """
            Calculates the tropospheric path delay for the signal path from a ground station to a satellite.
        
            Parameters:
                elevation (double): The elevation of the satellite [rad]
        
            Returns:
                the path delay due to the troposphere [m]
        
        
        """
        ...
    @typing.overload
    def computeSignalDelay(self, double: float) -> float:
        """
            Calculates the tropospheric signal delay for the signal path from a ground station to a satellite.
        
            Parameters:
                elevation (double): The elevation of the satellite [rad]
        
            Returns:
                the signal delay due to the troposphere [s]
        
            Calculates the tropospheric signal delay for the signal path from a ground station to a satellite at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.computeSignalDelay` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date of meteo conditions
                elevation (double): the elevation of the satellite [rad]
        
            Returns:
                the signal delay due to the troposphere [s]
        
        
        """
        ...
    @typing.overload
    def computeSignalDelay(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float: ...
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> float:
        """
            Compute the signal delay derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.derivativeValue` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter
                elevation (double): the elevation of the satellite [rad]
        
            Returns:
                the derivative value
        
        
        """
        ...
    @staticmethod
    def getDefaultModel(double: float) -> 'FixedDelayModel': ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Tell if the function is differentiable by the given parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.isDifferentiableBy` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): function parameter
        
            Returns:
                true if the function is differentiable by the given parameter.
        
        
        """
        ...
    def supportsParameter(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Check if a parameter is supported.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable.supportsParameter` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
        
            Parameters:
                param (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to check
        
            Returns:
                true if the parameter is supported
        
        
        """
        ...

class MariniMurrayModel(TroposphericCorrection):
    """
    public class MariniMurrayModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
    
        This class provides the correction of laser range tracking data for the effect of atmospheric refraction. This
        derivation, provided by J. W. Marini and C. W. Murray Jr, applies to satellites with elevation above 10° and whose
        heights exceed 70km. The reference model used in this class is derived from the NASA technical report TM-X-70555
        (available at the following link: https://ntrs.nasa.gov/search.jsp?R=19740007037). Position accuracies of better than a
        few centimeters are achievable with this model. It is worth stressing once more that the desired accuracy with this
        formulation can be obtained just for elevation angles above 10°. It is important to add that this model does not
        provide any type of correction in the elevation. In other words, the Marini-Murray model is based on the assumption that
        there are no differences between geometric and real satellite elevation.
    
        Since:
            4.8
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, meteorologicalConditionsProvider: typing.Union[fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider, typing.Callable], double: float, double2: float, double3: float): ...
    def computeSignalDelay(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float:
        """
            Calculates the tropospheric signal delay for the signal path from a ground station to a satellite at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.computeSignalDelay` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date of meteo conditions
                elevation (double): the elevation of the satellite [rad]
        
            Returns:
                the signal delay due to the troposphere [s]
        
        
        """
        ...
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> float:
        """
            Compute the signal delay derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.derivativeValue` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter
                elevation (double): the elevation of the satellite [rad]
        
            Returns:
                the derivative value
        
        
        """
        ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Tell if the function is differentiable by the given parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.isDifferentiableBy` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): function parameter
        
            Returns:
                true if the function is differentiable by the given parameter.
        
        
        """
        ...
    def supportsParameter(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Check if a parameter is supported.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable.supportsParameter` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
        
            Parameters:
                param (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to check
        
            Returns:
                true if the parameter is supported
        
        
        """
        ...

class MariniMurrayModelFactory(AbstractMeteoBasedCorrectionFactory[MariniMurrayModel]):
    """
    public class MariniMurrayModelFactory extends :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.AbstractMeteoBasedCorrectionFactory`<:class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.MariniMurrayModel`>
    
        This class describes the tropospheric correction factory around the
        :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.MariniMurrayModel`.
    """
    def __init__(self, double: float): ...

class SaastamoinenModel(TroposphericCorrection):
    """
    public class SaastamoinenModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
    
        The modified Saastamoinen model. Estimates the path delay imposed to electro-magnetic signals by the troposphere
        according to the formula:
    
        .. code-block: java
        
        
         δ = 2.277e-3 / cos z * (P + (1255 / T + 0.05) * e - B * tan :sup:`2` 
         z) + δR
         
        with the following input data provided to the model:
    
          - z: zenith angle
          - P: atmospheric pressure
          - T: temperature
          - e: partial pressure of water vapour
          - B, δR: correction terms
    
    
        The model supports custom δR correction terms to be read from a configuration file (saastamoinen-correction.txt) via
        the :class:`~fr.cnes.sirius.patrius.data.DataProvidersManager`.
    
        Constants used in model are defined as such in the Saastamoinen model article.
    
        Also see:
            "Guochang Xu, GPS - Theory, Algorithms and Applications, Springer, 2007", :meth:`~serialized`
    """
    def __init__(self, meteorologicalConditionsProvider: typing.Union[fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider, typing.Callable], double: float): ...
    def calculatePathDelay(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float:
        """
            Calculates the tropospheric path delay for the signal path from a ground station to a satellite at a given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date of the meteorological conditions
                elevation (double): the elevation of the satellite in radians
        
            Returns:
                the path delay due to the troposphere in m
        
        
        """
        ...
    def computeSignalDelay(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float:
        """
            Calculates the tropospheric signal delay for the signal path from a ground station to a satellite at a given date. This
            method exists only for convenience reasons and returns the same as
        
            .. code-block: java
            
            
               SaastamoinenModel#calculatePathDelay(double)/
               :meth:`~fr.cnes.sirius.patrius.utils.Constants.SPEED_OF_LIGHT`
             
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.computeSignalDelay` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date of the meteorological conditions
                elevation (double): the elevation of the satellite in radians
        
            Returns:
                the signal delay due to the troposphere in s
        
        
        """
        ...
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> float:
        """
            Compute the signal delay derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.derivativeValue` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter
                elevation (double): the elevation of the satellite [rad]
        
            Returns:
                the derivative value
        
        
        """
        ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    @staticmethod
    def getStandardModel(double: float) -> 'SaastamoinenModel':
        """
            Create a new Saastamoinen model using a standard atmosphere model. The standard atmosphere model uses the following
            reference values at mean sea level:
        
              - reference temperature: 18 degree Celsius
              - reference pressure: 101325 Pa
              - reference humidity: 50%
        
        
            Parameters:
                altitude (double): the altitude above the mean sea level of the station [m]
        
            Returns:
                a Saastamoinen model with standard environmental values
        
        
        """
        ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Tell if the function is differentiable by the given parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection.isDifferentiableBy` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): function parameter
        
            Returns:
                true if the function is differentiable by the given parameter.
        
        
        """
        ...
    def supportsParameter(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Check if a parameter is supported.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable.supportsParameter` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
        
            Parameters:
                param (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to check
        
            Returns:
                true if the parameter is supported
        
        
        """
        ...

class SaastamoinenModelFactory(AbstractMeteoBasedCorrectionFactory[SaastamoinenModel]):
    """
    public class SaastamoinenModelFactory extends :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.AbstractMeteoBasedCorrectionFactory`<:class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.SaastamoinenModel`>
    
        This class describes the tropospheric correction factory around the
        :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.SaastamoinenModel`.
    """
    def __init__(self): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.signalpropagation.troposphere")``.

    AbstractMeteoBasedCorrectionFactory: typing.Type[AbstractMeteoBasedCorrectionFactory]
    AstronomicalRefractionModel: typing.Type[AstronomicalRefractionModel]
    AstronomicalRefractionModelFactory: typing.Type[AstronomicalRefractionModelFactory]
    AzoulayModel: typing.Type[AzoulayModel]
    AzoulayModelFactory: typing.Type[AzoulayModelFactory]
    FixedDelayModel: typing.Type[FixedDelayModel]
    MariniMurrayModel: typing.Type[MariniMurrayModel]
    MariniMurrayModelFactory: typing.Type[MariniMurrayModelFactory]
    SaastamoinenModel: typing.Type[SaastamoinenModel]
    SaastamoinenModelFactory: typing.Type[SaastamoinenModelFactory]
    TroposphericCorrection: typing.Type[TroposphericCorrection]
