
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.events.detectors
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.signalpropagation.ionosphere
import fr.cnes.sirius.patrius.signalpropagation.troposphere
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import typing



class AngularCorrection(fr.cnes.sirius.patrius.math.parameter.IParameterizable):
    """
    public interface AngularCorrection extends :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
    
        This interface is an angular correction model enabling the computation of the satellite elevation angular correction.
    
        Since:
            2.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.signalpropagation.troposphere.TroposphericCorrection`,
            :class:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.IonosphericCorrection`
    """
    def computeElevationCorrectionFromApparentElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float:
        """
            Compute the angular correction from the apparent elevation.
        
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
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date at which we want to compute the angular correction
                geometricElevation (double): The geometric elevation (without atmosphere) [rad]
        
            Returns:
                the elevation correction [rad] so that :code:`apparent_elevation = geometric_elevation + elevation_correction`
        
        
        """
        ...
    def derivativeValueFromApparentElevation(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> float:
        """
            Compute the elevation correction derivative value with respect to the input parameter.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): Parameter
                apparentElevation (double): The apparent elevation (with atmosphere) of the satellite [rad]
        
            Returns:
                the elevation derivative value
        
        
        """
        ...
    def derivativeValueFromGeometricElevation(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> float:
        """
            Compute the elevation correction derivative value with respect to the input parameter.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): Parameter
                geometricElevation (double): The geometric elevation (without atmosphere) of the satellite [rad]
        
            Returns:
                the elevation derivative value
        
        
        """
        ...
    def getMinimalToleratedApparentElevation(self) -> float:
        """
            Getter for the minimal tolerated apparent elevation for this model (some models cannot compute correction for too low
            elevations).
        
            Returns:
                the minimal tolerated apparent elevation [rad]
        
        
        """
        ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Tell if the function is differentiable by the given parameter.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): Parameter
        
            Returns:
                :code:`true` if the function is differentiable by the given parameter
        
        
        """
        ...

class MeteorologicalConditions(java.io.Serializable):
    """
    public class MeteorologicalConditions extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Simple container for pressure/temperature/humidity (PTH) triplets to describe meteorological conditions.
    
        Instances of this class are guaranteed to be immutable.
    
        Also see:
            :meth:`~serialized`
    """
    P0: typing.ClassVar[float] = ...
    """
    public static final double P0
    
        Standard reference pressure [Pa].
    
        Also see:
            :meth:`~constant`
    
    
    """
    T0: typing.ClassVar[float] = ...
    """
    public static final double T0
    
        Standard reference temperature [°C].
    
        Also see:
            :meth:`~constant`
    
    
    """
    RH0: typing.ClassVar[float] = ...
    """
    public static final double RH0
    
        Standard reference relative humidity [%].
    
        Also see:
            :meth:`~constant`
    
    
    """
    H0: typing.ClassVar[float] = ...
    """
    public static final double H0
    
        Standard reference altitude [m].
    
        Also see:
            :meth:`~constant`
    
    
    """
    ABSOLUTE_ZERO: typing.ClassVar[float] = ...
    """
    public static final double ABSOLUTE_ZERO
    
        Absolute zero for temperatures.
    
        Also see:
            :meth:`~constant`
    
    
    """
    STANDARD: typing.ClassVar['MeteorologicalConditions'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditions` STANDARD
    
        Standard meteorological conditions: :meth:`~fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditions.P0`,
        :meth:`~fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditions.T0` (in [°K]) and
        :meth:`~fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditions.RH0`.
    
    """
    def __init__(self, double: float, double2: float, double3: float): ...
    @typing.overload
    @staticmethod
    def computeStandardValues(double: float) -> 'MeteorologicalConditions':
        """
            Computes standard model values [P, T, RH] for provided altitude given reference values [P0, T0, RH0 H0] with:
        
              - P = pressure [Pa]
              - T = temperature [K]
              - RH = relative humidity [%]
        
        
            Parameters:
                referenceMeteoConditions (:class:`~fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditions`): reference temperature, pressure and relative humidity
                referenceAltitude (double): reference altitude
                altitude (double): altitude for which values [P, T, RH] should be returned
        
            Returns:
                [P, T, RH] values
        
            Computes standard model values [P, T, R] for provided altitude with standard reference values [P0, T0, RH0] provided by
            tropospheric models :
        
              - P = pressure [Pa] - P0 = 101325 [Pa]
              - T = temperature [K] - T0 = 18 [°C]
              - RH = humidity rate [%] - RH0 = 50 [%]
        
        
            Parameters:
                altitude (double): altitude for which values [P, T, RH] should be returned
        
            Returns:
                standard model values [P, T, RH]
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def computeStandardValues(meteorologicalConditions: 'MeteorologicalConditions', double: float, double2: float) -> 'MeteorologicalConditions': ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getHumidity(self) -> float:
        """
            Getter for the relative humidity [%].
        
            Returns:
                the relative humidity
        
        
        """
        ...
    def getPressure(self) -> float:
        """
            Getter for the pressure [Pa].
        
            Returns:
                the pressure
        
        
        """
        ...
    def getTemperature(self) -> float:
        """
            Getter for the temperature [°K].
        
            Returns:
                the temperature
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @staticmethod
    def mean(collection: typing.Union[java.util.Collection['MeteorologicalConditions'], typing.Sequence['MeteorologicalConditions'], typing.Set['MeteorologicalConditions']]) -> 'MeteorologicalConditions': ...
    def toString(self) -> str:
        """
            Get a String representation of this meteorological conditions.
        
            Overrides:
                 in class 
        
            Returns:
                a String representation of this meteorological conditions
        
        
        """
        ...

class MeteorologicalConditionsProvider(java.io.Serializable):
    """
    `@FunctionalInterface <http://docs.oracle.com/javase/8/docs/api/java/lang/FunctionalInterface.html?is-external=true>` public interface MeteorologicalConditionsProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface is used to compute meteorological conditions at a given date, allowing to adapt the computation of
        atmospheric effects to the moment when a signal propagates through the atmosphere.
    """
    def getMeteorologicalConditions(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> MeteorologicalConditions:
        """
            Returns the meteorological conditions at a given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date of meteo conditions
        
            Returns:
                MeteorologicalConditions (temperature, pressure, humidity) at date
        
        
        """
        ...

class VacuumSignalPropagation(java.io.Serializable):
    """
    public class VacuumSignalPropagation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class describes the propagation of a signal in space
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, pVCoordinates2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, fixedDate: 'VacuumSignalPropagationModel.FixedDate'): ...
    def getEmissionDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the emission date.
        
            Returns:
                the emission date
        
        
        """
        ...
    def getEmitterPV(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates:
        """
            Getter for PV coordinates of the emitter, in the
            :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.getFrame`.
        
            Returns:
                the PV coordinates of the emitter
        
        
        """
        ...
    def getFixedDateType(self) -> 'VacuumSignalPropagationModel.FixedDate':
        """
            Getter for the fixed date : emission or reception.
        
            Returns:
                the fixed date
        
        
        """
        ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Getter for the reference frame.
        
            Returns:
                the reference frame
        
        
        """
        ...
    def getPVPropagation(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates:
        """
            Getter for the propagation position/velocity vectors in the reference frame.
        
            This method is a combination of the methods
            :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.getVector` and
            :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.getdPropdT`.
        
            Returns:
                the propagation position/velocity vectors
        
        
        """
        ...
    def getReceiverPV(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates:
        """
            Getter for PV coordinates of the receiver, in the
            :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.getFrame`.
        
            Returns:
                the PV coordinates of the receiver
        
        
        """
        ...
    def getReceptionDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Getter for the reception date.
        
            Returns:
                the reception date
        
        
        """
        ...
    @typing.overload
    def getShapiroTimeCorrection(self, double: float) -> float:
        """
            Computes the Shapiro time dilation due to the gravitational attraction of the body present at the center of the
            :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.getFrame`.
        
            Optimized version of the
            :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.getShapiroTimeCorrection` method for the frame
            attractive body.
        
            Parameters:
                mu (double): The gravitational constant of the body.
        
            Returns:
                the Shapiro time dilation
        
        
        """
        ...
    @typing.overload
    def getShapiroTimeCorrection(self, celestialPoint: fr.cnes.sirius.patrius.bodies.CelestialPoint) -> float: ...
    def getSignalPropagationDuration(self) -> float:
        """
            Getter for the signal propagation duration (delay in seconds between the
            :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.emissionDate` and the
            :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.receptionDate`).
        
            Returns:
                the signal propagation duration
        
        
        """
        ...
    @typing.overload
    def getVector(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the propagation vector in the reference frame.
        
            The returned vector can be projected in any frame thanks to
            :meth:`~fr.cnes.sirius.patrius.frames.transformations.Transform.transformVector`.
        
        
            But beware that it is only a projection and that the propagation process remains with respect to the
            :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.getFrame`. Indeed, the result of a propagation
            process depends, in a more complex manner than just a vector projection, to the
            :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.getFrame`.
        
            Returns:
                the propagation vector
        
        
        """
        ...
    @typing.overload
    def getVector(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getdPropdPem(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Getter for the propagation position vector derivatives wrt the emitter position express in the reference frame.
        
            Returns:
                the propagation position vector derivatives wrt the emitter position
        
        
        """
        ...
    @typing.overload
    def getdPropdPem(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    @typing.overload
    def getdPropdPrec(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Getter for the propagation position vector derivatives wrt the receiver position express in the reference frame.
        
            Returns:
                the propagation position vector derivatives wrt the receiver position
        
        
        """
        ...
    @typing.overload
    def getdPropdPrec(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    @typing.overload
    def getdPropdT(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the propagation velocity vector (= propagation vector derivative wrt time) in the reference frame.
        
            Returns:
                the propagation velocity vector
        
        
        """
        ...
    @typing.overload
    def getdPropdT(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getdTpropdPem(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the signal propagation partial derivatives vector wrt the emitter position in the reference frame at the
            emitting date.
        
            *Note: dTpropdPem = -dTpropdPrec*
        
            Returns:
                the signal propagation partial derivatives vector
        
        `@Deprecated <http://docs.oracle.com/javase/8/docs/api/java/lang/Deprecated.html?is-external=true>` public :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D` getdTpropdPem(:class:`~fr.cnes.sirius.patrius.frames.Frame` expressionFrame) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Deprecated. as of 4.13, use :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.getdTpropdPem`
            instead
            Getter for the signal propagation partial derivatives vector wrt the emitter position in the specified frame at the
            emitting date.
        
            *Note: dTpropdPem = -dTpropdPrec*
        
            Parameters:
                expressionFrame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the signal propagation partial derivatives vector frame expression
        
            Returns:
                the signal propagation partial derivatives vector
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if some frame specific error occurs
        
        
        """
        ...
    @typing.overload
    def getdTpropdPem(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getdTpropdPrec(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the signal propagation partial derivatives vector wrt the receiver position in the reference frame at the
            reception date.
        
            Returns:
                the signal propagation partial derivatives vector
        
        `@Deprecated <http://docs.oracle.com/javase/8/docs/api/java/lang/Deprecated.html?is-external=true>` public :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D` getdTpropdPrec(:class:`~fr.cnes.sirius.patrius.frames.Frame` expressionFrame) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Deprecated. as of 4.13, use :meth:`~fr.cnes.sirius.patrius.signalpropagation.VacuumSignalPropagation.getdTpropdPrec`
            instead
            Getter for the signal propagation partial derivatives vector wrt the receiver position in the specified frame at the
            reception date.
        
            Parameters:
                expressionFrame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the signal propagation partial derivatives vector frame expression
        
            Returns:
                the signal propagation partial derivatives vector
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if some frame specific error occurs
        
        
        """
        ...
    @typing.overload
    def getdTpropdPrec(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getdTpropdT(self) -> float:
        """
            Getter for the signal propagation partial derivatives wrt time.
        
            Returns:
                the signal propagation partial derivatives
        
        
        """
        ...
    class SignalPropagationRole(java.lang.Enum['VacuumSignalPropagation.SignalPropagationRole']):
        TRANSMITTER: typing.ClassVar['VacuumSignalPropagation.SignalPropagationRole'] = ...
        RECEIVER: typing.ClassVar['VacuumSignalPropagation.SignalPropagationRole'] = ...
        def getDate(self, vacuumSignalPropagation: 'VacuumSignalPropagation') -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
        def getdPropDPos(self, vacuumSignalPropagation: 'VacuumSignalPropagation') -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
        def getdTPropDPos(self, vacuumSignalPropagation: 'VacuumSignalPropagation') -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'VacuumSignalPropagation.SignalPropagationRole': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['VacuumSignalPropagation.SignalPropagationRole']: ...

class VacuumSignalPropagationModel:
    """
    public class VacuumSignalPropagationModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Model for the computation of a signal propagation vector and toolbox for the different corrections to be applied to it.
    
        Since:
            1.2
    """
    DEFAULT_MAX_ITER: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_MAX_ITER
    
        Default max number of iterations for signal propagation computation.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_THRESHOLD: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_THRESHOLD
    
        Default threshold (s) for signal propagation computation.
    
        This value guarantees that the propagation time is computed with a light travel distance precision below 0.3 mm.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, convergenceAlgorithm: 'VacuumSignalPropagationModel.ConvergenceAlgorithm'): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, convergenceAlgorithm: 'VacuumSignalPropagationModel.ConvergenceAlgorithm', int: int): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, int: int): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, convergenceAlgorithm: 'VacuumSignalPropagationModel.ConvergenceAlgorithm'): ...
    def computeSignalPropagation(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, pVCoordinatesProvider2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, fixedDate: 'VacuumSignalPropagationModel.FixedDate') -> VacuumSignalPropagation: ...
    @typing.overload
    @staticmethod
    def getSignalEmissionDate(pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, pVCoordinatesProvider2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, propagationDelayType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
    @typing.overload
    @staticmethod
    def getSignalEmissionDate(pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, pVCoordinatesProvider2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, propagationDelayType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType, frame: fr.cnes.sirius.patrius.frames.Frame, int: int) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
    @typing.overload
    @staticmethod
    def getSignalReceptionDate(pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, pVCoordinatesProvider2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, propagationDelayType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
    @typing.overload
    @staticmethod
    def getSignalReceptionDate(pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, pVCoordinatesProvider2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, propagationDelayType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType, frame: fr.cnes.sirius.patrius.frames.Frame, int: int) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
    class ConvergenceAlgorithm(java.lang.Enum['VacuumSignalPropagationModel.ConvergenceAlgorithm']):
        FIXE_POINT: typing.ClassVar['VacuumSignalPropagationModel.ConvergenceAlgorithm'] = ...
        NEWTON: typing.ClassVar['VacuumSignalPropagationModel.ConvergenceAlgorithm'] = ...
        def computeTprop(self, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float: ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'VacuumSignalPropagationModel.ConvergenceAlgorithm': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['VacuumSignalPropagationModel.ConvergenceAlgorithm']: ...
    class FixedDate(java.lang.Enum['VacuumSignalPropagationModel.FixedDate']):
        EMISSION: typing.ClassVar['VacuumSignalPropagationModel.FixedDate'] = ...
        RECEPTION: typing.ClassVar['VacuumSignalPropagationModel.FixedDate'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'VacuumSignalPropagationModel.FixedDate': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['VacuumSignalPropagationModel.FixedDate']: ...

class ConstantMeteorologicalConditionsProvider(MeteorologicalConditionsProvider):
    """
    public class ConstantMeteorologicalConditionsProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider`
    
        Provides constant meteorological conditions on a given date interval.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, meteorologicalConditions: MeteorologicalConditions): ...
    @typing.overload
    def __init__(self, meteorologicalConditions: MeteorologicalConditions, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getMeteorologicalConditions(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> MeteorologicalConditions:
        """
            Returns the meteorological conditions at a given date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider.getMeteorologicalConditions` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.MeteorologicalConditionsProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date of meteo conditions
        
            Returns:
                MeteorologicalConditions (temperature, pressure, humidity) at date
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class FiniteDistanceAngularCorrection(AngularCorrection):
    """
    public interface FiniteDistanceAngularCorrection extends :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection`
    
        This interface extends the :class:`~fr.cnes.sirius.patrius.signalpropagation.AngularCorrection` to take into account an
        angular correction when the distance between the observer and the target is not infinite (i.e.: the parallax
        correction).
    
        Since:
            4.13
    """
    @typing.overload
    def computeElevationCorrectionFromApparentElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float) -> float:
        """
            Compute the angular correction from the apparent elevation and distance.
        
            This method takes into account the finite distance of the observed object to add a parallax correction.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date at which we want to compute the angular correction
                apparentElevation (double): The apparent elevation (with atmosphere) [rad]
                distance (double): The distance to the object [m]. Can be `null
                    <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#POSITIVE_INFINITY>` (equivalent to not
                    take into account the parallax correction)
        
            Returns:
                the elevation correction [rad] so that :code:`apparent_elevation = geometric_elevation + elevation_correction`
        
        """
        ...
    @typing.overload
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
    @typing.overload
    def computeElevationCorrectionFromGeometricElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float) -> float:
        """
            Compute the angular correction from the geometric elevation and distance.
        
            This method takes into account the finite distance of the observed object to add a parallax correction.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): The date at which we want to compute the angular correction
                geometricElevation (double): The geometric elevation (without atmosphere) [rad]
                distance (double): The distance to the object [m]. Can be `null
                    <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#POSITIVE_INFINITY>` (equivalent to not
                    take into account the parallax correction)
        
            Returns:
                the elevation correction [rad] so that :code:`apparent_elevation = geometric_elevation + elevation_correction`
        
        """
        ...
    @typing.overload
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


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.signalpropagation")``.

    AngularCorrection: typing.Type[AngularCorrection]
    ConstantMeteorologicalConditionsProvider: typing.Type[ConstantMeteorologicalConditionsProvider]
    FiniteDistanceAngularCorrection: typing.Type[FiniteDistanceAngularCorrection]
    MeteorologicalConditions: typing.Type[MeteorologicalConditions]
    MeteorologicalConditionsProvider: typing.Type[MeteorologicalConditionsProvider]
    VacuumSignalPropagation: typing.Type[VacuumSignalPropagation]
    VacuumSignalPropagationModel: typing.Type[VacuumSignalPropagationModel]
    ionosphere: fr.cnes.sirius.patrius.signalpropagation.ionosphere.__module_protocol__
    troposphere: fr.cnes.sirius.patrius.signalpropagation.troposphere.__module_protocol__
