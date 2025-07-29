
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly
import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.events.detectors
import fr.cnes.sirius.patrius.forces
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.frames.transformations
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



class ElementaryFlux:
    """
    public class ElementaryFlux extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Elementary flux
    
        Since:
            1.2
    """
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, double2: float): ...
    def getAlbedoPressure(self) -> float:
        """
            get the albedo pressure (N/M²)
        
            Returns:
                albedo pressure
        
            Since:
                1.2
        
        
        """
        ...
    def getDirFlux(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            get the direction flux
        
            Returns:
                direction flux
        
            Since:
                1.2
        
        
        """
        ...
    def getInfraRedPressure(self) -> float:
        """
            get the infrared pressure (N/M²)
        
            Returns:
                infrared pressure
        
            Since:
                1.2
        
        
        """
        ...

class IEmissivityModel(java.io.Serializable):
    """
    public interface IEmissivityModel extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This is the interface for all emissivity models (albedo and infrared).
    
        Since:
            1.2
    """
    def getEmissivity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float) -> typing.MutableSequence[float]:
        """
            Get the albedo and infrared emissivities.
        
            Parameters:
                cdate (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                latitude (double): (rad) geocentric latitude
                longitude (double): (rad) geocentric longitude
        
            Returns:
                albedo emissivity ([0]) and infrared emissivity ([1])
        
        
        """
        ...

class LightingRatio(java.io.Serializable):
    """
    public class LightingRatio extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class computing the lighting ratio in the interval [0; 1], used for
        :class:`~fr.cnes.sirius.patrius.events.detectors.EclipseDetector` and
        :class:`~fr.cnes.sirius.patrius.forces.radiation.SolarRadiationPressure`:
    
          - 0: occulted body is entirely hidden by occulting body
          - 1: occulted body is fully visible from object.
          - Between 0 and 1: occulted body is partly visible from object.
    
    
        The lighting ratio is the percentage of occulted body visible from spacecraft.
    
        Signal propagation can be taken into account.
    
        Computation hypothesis:
    
          - Occulted body is spherical
          - Occulting body can have any shape, but computation is made using a sphere of radius the "apparent occulting radius"
            which is the angular radius of the occulting body in the direction of occulted body.
    
    
        Since:
            4.13
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float): ...
    def compute(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def computeExtended(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getEpsilonSignalPropagation(self) -> float:
        """
            Getter for the epsilon for signal propagation when signal propagation is taken into account.
        
            Returns:
                the epsilon for signal propagation when signal propagation is taken into account
        
        
        """
        ...
    def getInertialFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Getter for the inertial frame used for signal propagation computation.
        
            Returns:
                the inertial frame
        
        
        """
        ...
    def getMaxIterSignalPropagation(self) -> int:
        """
            Getter for the maximum number of iterations for signal propagation when signal propagation is taken into account.
        
            Returns:
                the maximum number of iterations for signal propagation
        
        
        """
        ...
    def getPropagationDelayType(self) -> fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType:
        """
            Getter for the propagation delay type.
        
            Returns:
                the propagation delay type
        
        
        """
        ...
    def setEpsilonSignalPropagation(self, double: float) -> None:
        """
            Setter for the epsilon for signal propagation when signal propagation is taken into account.
        
        
            This epsilon (in s) directly reflect the accuracy of signal propagation (1s of accuracy = 3E8m of accuracy on distance
            between emitter and receiver)
        
            Parameters:
                epsilon (double): Epsilon for the signal propagation
        
        
        """
        ...
    def setMaxIterSignalPropagation(self, int: int) -> None:
        """
            Setter for the maximum number of iterations for signal propagation when signal propagation is taken into account.
        
            Parameters:
                maxIterSignalPropagationIn (int): Maximum number of iterations for signal propagation
        
        
        """
        ...
    def setPropagationDelayType(self, propagationDelayType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType, frame: fr.cnes.sirius.patrius.frames.Frame) -> None:
        """
            Setter for the propagation delay computation type. Warning: check Javadoc of detector to see if detector takes into
            account propagation time delay. if not, signals are always considered instantaneous. The provided frame is used to
            compute the signal propagation when delay is taken into account.
        
            Parameters:
                propagationDelayTypeIn (:class:`~fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType`): Propagation delay type used in events computation
                frameIn (:class:`~fr.cnes.sirius.patrius.frames.Frame`): Frame to use for signal propagation with delay (may be null if propagation delay type is considered instantaneous).
                    Warning: the usage of a pseudo inertial frame is tolerated, however it will lead to some inaccuracies due to the
                    non-invariance of the frame with respect to time. For this reason, it is suggested to use the ICRF frame or a frame
                    which is frozen with respect to the ICRF.
        
            Raises:
                : if the provided frame is not pseudo inertial.
        
        
        """
        ...

class RadiationSensitive(java.io.Serializable, fr.cnes.sirius.patrius.propagation.numerical.JacobianParametersProvider):
    """
    public interface RadiationSensitive extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, :class:`~fr.cnes.sirius.patrius.propagation.numerical.JacobianParametersProvider`
    
        Interface for spacecraft that are sensitive to radiation pressure forces.
    """
    def addDSRPAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray], vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> None: ...
    def addDSRPAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> None: ...
    def radiationPressureAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class RediffusedFlux:
    """
    public class RediffusedFlux extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        creating a set of solar pressure rediffused by the Earth for a satellite position.
    
        This force only applies to Earth.
    
        Since:
            1.2
    """
    @typing.overload
    def __init__(self, int: int, int2: int, celestialBodyFrame: fr.cnes.sirius.patrius.frames.CelestialBodyFrame, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, pVCoordinatesProvider2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, iEmissivityModel: typing.Union[IEmissivityModel, typing.Callable]): ...
    @typing.overload
    def __init__(self, int: int, int2: int, celestialBodyFrame: fr.cnes.sirius.patrius.frames.CelestialBodyFrame, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, pVCoordinatesProvider2: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, iEmissivityModel: typing.Union[IEmissivityModel, typing.Callable], boolean: bool, boolean2: bool): ...
    @typing.overload
    def getFlux(self) -> typing.MutableSequence[ElementaryFlux]:
        """
            Getter for all elementary rediffused fluxes.
        
            Returns:
                rediffused fluxes in bodyFrame frame
        
            Since:
                1.2
        
        """
        ...
    @typing.overload
    def getFlux(self, transform: fr.cnes.sirius.patrius.frames.transformations.Transform) -> typing.MutableSequence[ElementaryFlux]:
        """
            Getter for all elementary rediffused fluxes.
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.frames.transformations.Transform`): the transform from body frame to the wanted frame
        
            Returns:
                rediffused fluxes in the wanted frame
        
            Since:
                4.10
        
        
        """
        ...
    def isAlbedo(self) -> bool:
        """
            Calculation indicator of the albedo force.
        
            Returns:
                if albedo force is computed
        
        
        """
        ...
    def isIr(self) -> bool:
        """
            Calculation indicator of the infrared force.
        
            Returns:
                the ir force is computed
        
        
        """
        ...

class RediffusedRadiationPressure(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable, fr.cnes.sirius.patrius.forces.ForceModel, fr.cnes.sirius.patrius.forces.GradientModel):
    """
    public final class RediffusedRadiationPressure extends :class:`~fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
    
    
        Class that represents a rediffused radiative force.
    
        The implementation of this class enables the computation of partial derivatives with respect to **K0 albedo global
        coefficient**, **K0 infrared global coefficient**, **absorption**, **specular reflection** or **diffusion reflection
        coefficients**.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, rediffusedRadiationPressure: 'RediffusedRadiationPressure', assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, celestialBodyFrame: fr.cnes.sirius.patrius.frames.CelestialBodyFrame, int: int, int2: int, iEmissivityModel: typing.Union[IEmissivityModel, typing.Callable], rediffusedRadiationSensitive: 'RediffusedRadiationSensitive'): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, celestialBodyFrame: fr.cnes.sirius.patrius.frames.CelestialBodyFrame, int: int, int2: int, iEmissivityModel: typing.Union[IEmissivityModel, typing.Callable], rediffusedRadiationSensitive: 'RediffusedRadiationSensitive', boolean: bool): ...
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            This methods throws an exception if the user did not provide all the required data to perform model call on provided
            range [start; end]. It is the responsibility of the model implementation to properly throw exceptions (for example
            DragForce will throw an exception if solar activity data is missing in the range [start, end]).
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.ForceModel.checkData` in
                interface :class:`~fr.cnes.sirius.patrius.forces.ForceModel`
        
            Parameters:
                start (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): range start date
                end (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): range end date
        
        
        """
        ...
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientPosition` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
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
    def getAssembly(self) -> fr.cnes.sirius.patrius.assembly.Assembly:
        """
            Getter for the assembly used at construction.
        
            Returns:
                the assembly.
        
        
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
    def getInBodyFrame(self) -> fr.cnes.sirius.patrius.frames.CelestialBodyFrame:
        """
            Getter for the boby frame used at construction.
        
            Returns:
                the boby frame.
        
        
        """
        ...
    def getInCorona(self) -> int:
        """
            Getter for the number of corona used at construction.
        
            Returns:
                the number of corona.
        
        
        """
        ...
    def getInEmissivityModel(self) -> IEmissivityModel:
        """
            Getter for the emissivity model used at construction.
        
            Returns:
                the emissivity model.
        
        
        """
        ...
    def getInMeridian(self) -> int:
        """
            Getter for the number of meridian used at construction.
        
            Returns:
                the number of meridian.
        
        
        """
        ...
    def getInSun(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Getter for the coordinate of sun used at construction.
        
            Returns:
                the coordinate of sun.
        
        
        """
        ...
    def getK0Albedo(self) -> float:
        """
            Getter for the albedo global multiplicative factor used at construction.
        
            Returns:
                the albedo global multiplicative factor.
        
        
        """
        ...
    def getK0Ir(self) -> float:
        """
            Getter for the infrared global multiplicative factor used at construction.
        
            Returns:
                the infrared global multiplicative factor.
        
        
        """
        ...
    def isAlbedoComputed(self) -> bool:
        """
            Getter for the albedo indicator used at construction.
        
            Returns:
                the albedo indicator.
        
        
        """
        ...
    def isIRComputed(self) -> bool:
        """
            Getter for the infrared indicator used at construction.
        
            Returns:
                the infrared indicator.
        
        
        """
        ...

class RediffusedRadiationSensitive(fr.cnes.sirius.patrius.propagation.numerical.JacobianParametersProvider):
    """
    public interface RediffusedRadiationSensitive extends :class:`~fr.cnes.sirius.patrius.propagation.numerical.JacobianParametersProvider`
    
        rediffused radiative pressure interface
    
        Since:
            1.2
    """
    def addDAccDParamRediffusedRadiativePressure(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDStateRediffusedRadiativePressure(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def getAssembly(self) -> fr.cnes.sirius.patrius.assembly.Assembly:
        """
            assembly getter
        
            Returns:
                assembly
        
        
        """
        ...
    def getFlagAlbedo(self) -> bool:
        """
            albedo getter
        
            Returns:
                calculation indicator of the albedo force
        
        
        """
        ...
    def getFlagIr(self) -> bool:
        """
            infrared getter
        
            Returns:
                calculation indicator of the infrared force
        
        
        """
        ...
    def getK0Albedo(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            K0 albedo getter
        
            Returns:
                albedo global multiplicative factor
        
        
        """
        ...
    def getK0Ir(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            K0 infrared getter
        
            Returns:
                the infrared global multiplicative factor
        
        
        """
        ...
    def initDerivatives(self) -> None:
        """
            derivatives initialisation
        
        """
        ...
    def rediffusedRadiationPressureAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, elementaryFluxArray: typing.Union[typing.List[ElementaryFlux], jpype.JArray]) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class SolarRadiationPressure(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable, fr.cnes.sirius.patrius.forces.ForceModel, fr.cnes.sirius.patrius.forces.GradientModel):
    """
    public class SolarRadiationPressure extends :class:`~fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
    
        Solar radiation pressure force model considering spherical/circular or non-spherical (ellipsoid) occulting bodies.
    
        The implementation of this class enables the computation of partial derivatives with respect to **absorption**,
        **specular reflection** or **diffusion reflection coefficients**.
    
        Eclipses computation can be deactivated by using
        :meth:`~fr.cnes.sirius.patrius.forces.radiation.SolarRadiationPressure.setEclipsesComputation`. By default, eclipses are
        taken into account.
    
        This class allows to consider any occulting body (Earth, Moon, etc.).
    
    
        In case of multiple occulting bodies, the assumption is made that only one body occults the spacecraft at a time.
    
        Light speed is currently never taken into account.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    REFERENCE_FLUX: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` REFERENCE_FLUX
    
        Normalized reference flux.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, double: float, double2: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double3: float, double4: float, radiationSensitive: RadiationSensitive): ...
    @typing.overload
    def __init__(self, double: float, double2: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double3: float, double4: float, radiationSensitive: RadiationSensitive, boolean: bool): ...
    @typing.overload
    def __init__(self, double: float, double2: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double3: float, double4: float, celestialBodyFrame: fr.cnes.sirius.patrius.frames.CelestialBodyFrame, radiationSensitive: RadiationSensitive, boolean: bool): ...
    @typing.overload
    def __init__(self, double: float, double2: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double3: float, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, assembly: fr.cnes.sirius.patrius.assembly.Assembly, double4: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double3: float, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, radiationSensitive: RadiationSensitive): ...
    @typing.overload
    def __init__(self, double: float, double2: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double3: float, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, radiationSensitive: RadiationSensitive, boolean: bool): ...
    @typing.overload
    def __init__(self, solarRadiationPressure: 'SolarRadiationPressure', assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float, double2: float, celestialBodyFrame: fr.cnes.sirius.patrius.frames.CelestialBodyFrame, radiationSensitive: RadiationSensitive, boolean: bool): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, radiationSensitive: RadiationSensitive, boolean: bool): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float, radiationSensitive: RadiationSensitive): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float, radiationSensitive: RadiationSensitive, boolean: bool): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, radiationSensitive: RadiationSensitive): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float, radiationSensitive: RadiationSensitive): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float, radiationSensitive: RadiationSensitive, boolean: bool): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float, celestialBodyFrame: fr.cnes.sirius.patrius.frames.CelestialBodyFrame, radiationSensitive: RadiationSensitive, boolean: bool): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, radiationSensitive: RadiationSensitive): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, radiationSensitive: RadiationSensitive, boolean: bool): ...
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def addOccultingBody(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape) -> None:
        """
            Add an occulting body.
        
            Parameters:
                body (:class:`~fr.cnes.sirius.patrius.bodies.BodyShape`): Occulting body to add
        
        
        """
        ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientPosition` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
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
    @staticmethod
    def convertRadiativePressureToFlux(double: float, double2: float) -> float:
        """
            Get the solar flux (SF) from the solar radiation pressure: SF = pRef * dRef :sup:`2`
        
            Parameters:
                dRef (double): Reference distance for the solar radiation pressure (m)
                pRef (double): solar radiation pressure at reference distance dRef (N/m :sup:`2` )
        
            Returns:
                the normalized reference flux.
        
        
        """
        ...
    def getEpsilonSignalPropagation(self) -> float:
        """
            Getter for the epsilon for signal propagation when signal propagation is taken into account.
        
            Returns:
                the epsilon for signal propagation when signal propagation is taken into account
        
        
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
    def getInertialFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Getter for the inertial frame used for signal propagation computation.
        
            Returns:
                the inertial frame
        
        
        """
        ...
    def getLightingRatio(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMaxIterSignalPropagation(self) -> int:
        """
            Getter for the maximum number of iterations for signal propagation when signal propagation is taken into account.
        
            Returns:
                the maximum number of iterations for signal propagation
        
        
        """
        ...
    def getMultiplicativeFactor(self) -> float:
        """
            Getter for the multiplicative factor.
        
            Returns:
                the multiplicative factor
        
        
        """
        ...
    def getOccultingBodies(self) -> java.util.List[fr.cnes.sirius.patrius.bodies.BodyShape]: ...
    def getPropagationDelayType(self) -> fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType:
        """
            Getter for the propagation delay type.
        
            Returns:
                the propagation delay type
        
        
        """
        ...
    def getReferenceFlux(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Getter for the parameter representing the reference flux normalized for a 1m distance (N).
        
            Returns:
                the normlized reference flux parameter
        
        
        """
        ...
    def getSolarFlux(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getSunBody(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Getter for the Sun model used at construction.
        
            Returns:
                the Sun model.
        
        
        """
        ...
    def isEclipseComputation(self) -> bool:
        """
            Returns flag indicating if eclipses should be taken into account.
        
            Returns:
                flag indicating if eclipses should be taken into account
        
        
        """
        ...
    def setEclipsesComputation(self, boolean: bool) -> None:
        """
            Setter for enabling/disabling eclipses computation.
        
            Parameters:
                eclipsesComputationFlagIn (boolean): True if eclipses should be taken into account, false otherwise
        
        
        """
        ...
    def setEpsilonSignalPropagation(self, double: float) -> None:
        """
            Setter for the epsilon for signal propagation when signal propagation is taken into account.
        
        
            This epsilon (in s) directly reflect the accuracy of signal propagation (1s of accuracy = 3E8m of accuracy on distance
            between emitter and receiver)
        
            Parameters:
                epsilon (double): Epsilon for the signal propagation
        
        
        """
        ...
    def setMaxIterSignalPropagation(self, int: int) -> None:
        """
            Setter for the maximum number of iterations for signal propagation when signal propagation is taken into account.
        
            Parameters:
                maxIterSignalPropagationIn (int): Maximum number of iterations for signal propagation
        
        
        """
        ...
    def setPropagationDelayType(self, propagationDelayType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType, frame: fr.cnes.sirius.patrius.frames.Frame) -> None:
        """
            Setter for the propagation delay computation type. Warning: check Javadoc of detector to see if detector takes into
            account propagation time delay. if not, signals are always considered instantaneous. The provided frame is used to
            compute the signal propagation when delay is taken into account.
        
            Parameters:
                propagationDelayTypeIn (:class:`~fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType`): Propagation delay type used in events computation
                frameIn (:class:`~fr.cnes.sirius.patrius.frames.Frame`): Frame to use for signal propagation with delay (may be null if propagation delay type is considered instantaneous).
                    Warning: the usage of a pseudo inertial frame is tolerated, however it will lead to some inaccuracies due to the
                    non-invariance of the frame with respect to time. For this reason, it is suggested to use the ICRF frame or a frame
                    which is frozen with respect to the ICRF.
        
            Raises:
                : if the provided frame is not pseudo inertial.
        
        
        """
        ...

class KnockeRiesModel(IEmissivityModel):
    """
    public final class KnockeRiesModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.radiation.IEmissivityModel`
    
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    A0: typing.ClassVar[float] = ...
    """
    public static final double A0
    
        coefficient a0 of Knocke-Ries model.
    
        Also see:
            :meth:`~constant`
    
    
    """
    A2: typing.ClassVar[float] = ...
    """
    public static final double A2
    
        coefficient a2 of Knocke-Ries model.
    
        Also see:
            :meth:`~constant`
    
    
    """
    C1AL: typing.ClassVar[float] = ...
    """
    public static final double C1AL
    
        coefficient c1al of Knocke-Ries model.
    
        Also see:
            :meth:`~constant`
    
    
    """
    D0: typing.ClassVar[float] = ...
    """
    public static final double D0
    
        coefficient a0 of Knocke-Ries model.
    
        Also see:
            :meth:`~constant`
    
    
    """
    E2: typing.ClassVar[float] = ...
    """
    public static final double E2
    
        coefficient a2 of Knocke-Ries model.
    
        Also see:
            :meth:`~constant`
    
    
    """
    C1IR: typing.ClassVar[float] = ...
    """
    public static final double C1IR
    
        coefficient c1ir of Knocke-Ries model.
    
        Also see:
            :meth:`~constant`
    
    
    """
    REFDAY: typing.ClassVar[fr.cnes.sirius.patrius.time.AbsoluteDate] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` REFDAY
    
        reference day of Knocke-Ries model.
    
    """
    DAYSYEAR: typing.ClassVar[float] = ...
    """
    public static final double DAYSYEAR
    
        duration of a year (in days).
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def getEmissivity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float) -> typing.MutableSequence[float]:
        """
        
            Computing of the emissivities of earth (albedo and infrared) based of the Knocke-Reis model (the longitude is not used
            in this model)
            See Obelix Reference manuel (NT-07-1)
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.radiation.IEmissivityModel.getEmissivity` in
                interface :class:`~fr.cnes.sirius.patrius.forces.radiation.IEmissivityModel`
        
            Parameters:
                cdate (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                latitude (double): (rad) geocentric latitude. The angle between the radius (from centre to the point on the surface) and the equatorial
                    plane
                longitude (double): (rad) geocentric longitude
        
            Returns:
                albedo emissivity (emissivity[0]) and infrared emissivity (emissivity[1])
        
            Since:
                1.2
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.radiation")``.

    ElementaryFlux: typing.Type[ElementaryFlux]
    IEmissivityModel: typing.Type[IEmissivityModel]
    KnockeRiesModel: typing.Type[KnockeRiesModel]
    LightingRatio: typing.Type[LightingRatio]
    RadiationSensitive: typing.Type[RadiationSensitive]
    RediffusedFlux: typing.Type[RediffusedFlux]
    RediffusedRadiationPressure: typing.Type[RediffusedRadiationPressure]
    RediffusedRadiationSensitive: typing.Type[RediffusedRadiationSensitive]
    SolarRadiationPressure: typing.Type[SolarRadiationPressure]
