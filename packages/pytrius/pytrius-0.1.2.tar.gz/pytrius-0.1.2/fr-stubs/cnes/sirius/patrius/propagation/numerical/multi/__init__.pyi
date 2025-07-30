
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.attitudes.multi
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.forces
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.ode
import fr.cnes.sirius.patrius.math.ode.sampling
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.propagation.sampling.multi
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



class MultiModeHandler:
    """
    public interface MultiModeHandler
    
    
        This interface is copied from :class:`~fr.cnes.sirius.patrius.propagation.numerical.ModeHandler` and adapted to multi
        propagation.
    
        Common interface for all propagator mode handlers initialization.
    
        Since:
            3.0
    """
    def initialize(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], map2: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], multiStateVectorInfo: 'MultiStateVectorInfo', boolean: bool, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, map3: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.frames.Frame], typing.Mapping[str, fr.cnes.sirius.patrius.frames.Frame]], map4: typing.Union[java.util.Map[str, float], typing.Mapping[str, float]]) -> None: ...
    def setReference(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Define new reference date.
        
            To be called by :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator` only.
        
            Parameters:
                newReference (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): new reference date
        
        
        """
        ...

class MultiNumericalPropagator(fr.cnes.sirius.patrius.propagation.MultiPropagator, java.util.Observer, java.io.Serializable):
    @typing.overload
    def __init__(self, firstOrderIntegrator: fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator): ...
    @typing.overload
    def __init__(self, firstOrderIntegrator: fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.frames.Frame], typing.Mapping[str, fr.cnes.sirius.patrius.frames.Frame]]): ...
    @typing.overload
    def __init__(self, firstOrderIntegrator: fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.frames.Frame], typing.Mapping[str, fr.cnes.sirius.patrius.frames.Frame]], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle): ...
    def addAdditionalEquations(self, additionalEquations: fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations, string: str) -> None: ...
    def addAttitudeEquation(self, attitudeEquation: fr.cnes.sirius.patrius.propagation.numerical.AttitudeEquation, string: str) -> None: ...
    @typing.overload
    def addEventDetector(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, string: str) -> None: ...
    @typing.overload
    def addEventDetector(self, multiEventDetector: fr.cnes.sirius.patrius.events.MultiEventDetector) -> None: ...
    def addForceModel(self, forceModel: fr.cnes.sirius.patrius.forces.ForceModel, string: str) -> None: ...
    def addInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, string: str) -> None: ...
    def addStateProvider(self, spacecraftStateProvider: fr.cnes.sirius.patrius.propagation.SpacecraftStateProvider, string: str) -> None: ...
    def clearEventsDetectors(self) -> None: ...
    def getAttitudeProvider(self, string: str) -> fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider: ...
    def getAttitudeProviderEvents(self, string: str) -> fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider: ...
    def getAttitudeProviderForces(self, string: str) -> fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider: ...
    def getCalls(self) -> int: ...
    def getEventsDetectors(self) -> java.util.Collection[fr.cnes.sirius.patrius.events.MultiEventDetector]: ...
    def getForceModels(self, string: str) -> java.util.List[fr.cnes.sirius.patrius.forces.ForceModel]: ...
    def getFrame(self, string: str) -> fr.cnes.sirius.patrius.frames.Frame: ...
    def getGeneratedEphemeris(self, string: str) -> fr.cnes.sirius.patrius.propagation.BoundedPropagator: ...
    def getInitialStates(self) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    def getMode(self) -> int: ...
    def getMu(self, string: str) -> float: ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType: ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, string: str) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getPositionAngleType(self) -> fr.cnes.sirius.patrius.orbits.PositionAngle: ...
    def getStateProviders(self) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftStateProvider]: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    def removeForceModels(self) -> None: ...
    def removeInitialState(self, string: str) -> None: ...
    def setAdditionalStateTolerance(self, string: str, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], string2: str) -> None: ...
    @typing.overload
    def setAttitudeProvider(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, string: str) -> None: ...
    @typing.overload
    def setAttitudeProvider(self, multiAttitudeProvider: fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider, string: str) -> None: ...
    @typing.overload
    def setAttitudeProviderEvents(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, string: str) -> None: ...
    @typing.overload
    def setAttitudeProviderEvents(self, multiAttitudeProvider: fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider, string: str) -> None: ...
    @typing.overload
    def setAttitudeProviderForces(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, string: str) -> None: ...
    @typing.overload
    def setAttitudeProviderForces(self, multiAttitudeProvider: fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider, string: str) -> None: ...
    def setEphemerisMode(self) -> None: ...
    def setMassProviderEquation(self, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, string: str) -> None: ...
    @typing.overload
    def setMasterMode(self, double: float, multiPatriusFixedStepHandler: fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusFixedStepHandler) -> None: ...
    @typing.overload
    def setMasterMode(self, multiPatriusStepHandler: fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepHandler) -> None: ...
    def setOrbitTolerance(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], string: str) -> None: ...
    def setSlaveMode(self) -> None: ...
    def update(self, observable: java.util.Observable, object: typing.Any) -> None: ...

class MultiPartialDerivativesEquations(fr.cnes.sirius.patrius.propagation.numerical.AbstractPartialDerivativesEquations):
    """
    public class MultiPartialDerivativesEquations extends :class:`~fr.cnes.sirius.patrius.propagation.numerical.AbstractPartialDerivativesEquations`
    
        Set of :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations` computing the partial derivatives of
        the state (orbit) with respect to initial state and force models parameters.
    
        This set of equations are automatically added to a
        :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator` in order to compute partial derivatives of
        the orbit along with the orbit itself. This is useful for example in orbit determination applications.
    
        Since:
            4.5
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str, multiNumericalPropagator: MultiNumericalPropagator, string2: str): ...

class MultiStateVectorInfo(java.io.Serializable):
    """
    public final class MultiStateVectorInfo extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Utility class that describes in a minimal fashion the structure of a state. An instance contains the size of an
        additional state and its index in the state vector. The instance :code:`AdditionalStateInfo` is guaranteed to be
        immutable.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], map2: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.frames.Frame], typing.Mapping[str, fr.cnes.sirius.patrius.frames.Frame]], map3: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftStateProvider], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftStateProvider]]): ...
    def getAddStatesInfos(self, string: str) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo]: ...
    def getIdList(self) -> java.util.List[str]: ...
    def getIdListAddedProviders(self) -> java.util.List[str]: ...
    def getSatAddStatesSize(self, string: str) -> int:
        """
            Get the additional states size of the given spacecraft .
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                the additional states size
        
        
        """
        ...
    def getSatRank(self, string: str) -> int:
        """
            Get the state vector index of the given spacecraft in the global state vector.
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                the state vector index
        
        
        """
        ...
    def getStateVectorSize(self) -> int:
        """
            Get global state vector size.
        
            Returns:
                the global state vector size.
        
        
        """
        ...
    def mapArrayToState(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, multiAttitudeProvider: fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider, multiAttitudeProvider2: fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider, string: str) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def mapArrayToStates(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], map2: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], map3: typing.Union[java.util.Map[str, float], typing.Mapping[str, float]], map4: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.frames.Frame], typing.Mapping[str, fr.cnes.sirius.patrius.frames.Frame]]) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    def mapStatesToArray(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...

class MultiEphemerisModeHandler(MultiModeHandler, fr.cnes.sirius.patrius.math.ode.sampling.StepHandler):
    """
    public class MultiEphemerisModeHandler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.numerical.multi.MultiModeHandler`, :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`
    
    
        This interface is copied from :code:`EphemerisModeHandler` and adapted to multi propagation.
    
        This class stores sequentially generated orbital parameters of each states for later retrieval.
    
        Instances of this class are built and then must be fed with the results provided by
        :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator` objects configured in
        :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`. Once propagation is over, a
        :class:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator` can be built for each spacecraft from the stored steps.
    
        Since:
            3.0
    """
    def __init__(self): ...
    def getEphemeris(self, string: str) -> fr.cnes.sirius.patrius.propagation.BoundedPropagator:
        """
            Get the generated ephemeris of the given spacecraft Id.
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft Id
        
            Returns:
                a new instance of the generated ephemeris of the given spacecraft Id.
        
        
        """
        ...
    def handleStep(self, stepInterpolator: fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator, boolean: bool) -> None:
        """
            Handle the last accepted step
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler.handleStep` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`
        
            Parameters:
                interpolator (:class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`): interpolator for the last accepted step. For efficiency purposes, the various integrators reuse the same object on each
                    call, so if the instance wants to keep it across all calls (for example to provide at the end of the integration a
                    continuous model valid throughout the integration range, as the
                    :class:`~fr.cnes.sirius.patrius.math.ode.ContinuousOutputModel` class does), it should build a local copy using the
                    clone method of the interpolator and store this copy. Keeping only a reference to the interpolator and reusing it will
                    result in unpredictable behavior (potentially crashing the application).
                isLast (boolean): true if the step is the last one
        
        
        """
        ...
    def init(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float) -> None:
        """
            Initialize step handler at the start of an ODE integration.
        
            This method is called once at the start of the integration. It may be used by the step handler to initialize some
            internal data if needed.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`
        
            Parameters:
                t0 (double): start value of the independent *time* variable
                y0 (double[]): array containing the start value of the state vector
                t (double): target time for the integration
        
        
        """
        ...
    def initialize(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], map2: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], multiStateVectorInfo: MultiStateVectorInfo, boolean: bool, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, map3: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.frames.Frame], typing.Mapping[str, fr.cnes.sirius.patrius.frames.Frame]], map4: typing.Union[java.util.Map[str, float], typing.Mapping[str, float]]) -> None: ...
    def setForward(self, boolean: bool) -> None:
        """
            Set forward propagation flag.
        
            Parameters:
                isForward (boolean): true if propagation is forward
        
        
        """
        ...
    def setReference(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Define new reference date.
        
            To be called by :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator` only.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.multi.MultiModeHandler.setReference` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.numerical.multi.MultiModeHandler`
        
            Parameters:
                newReference (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): new reference date
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation.numerical.multi")``.

    MultiEphemerisModeHandler: typing.Type[MultiEphemerisModeHandler]
    MultiModeHandler: typing.Type[MultiModeHandler]
    MultiNumericalPropagator: typing.Type[MultiNumericalPropagator]
    MultiPartialDerivativesEquations: typing.Type[MultiPartialDerivativesEquations]
    MultiStateVectorInfo: typing.Type[MultiStateVectorInfo]
