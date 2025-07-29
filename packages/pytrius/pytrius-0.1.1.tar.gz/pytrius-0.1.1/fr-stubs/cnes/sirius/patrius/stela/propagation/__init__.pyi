
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.ode
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.propagation.sampling
import fr.cnes.sirius.patrius.stela.forces
import fr.cnes.sirius.patrius.stela.forces.noninertial
import fr.cnes.sirius.patrius.stela.orbits
import fr.cnes.sirius.patrius.stela.propagation.data
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



class ForcesStepHandler(fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler):
    """
    public class ForcesStepHandler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler`
    
        Step handler handling forces requiring to be updated every step and not every substep.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter, nonInertialContribution: fr.cnes.sirius.patrius.stela.forces.noninertial.NonInertialContribution): ...
    def getDnonInertial(self) -> typing.MutableSequence[float]:
        """
            Getter for non-inertial contribution.
        
            Returns:
                non-inertial contribution
        
        
        """
        ...
    def handleStep(self, patriusStepInterpolator: fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator, boolean: bool) -> None: ...
    def init(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Initialize step handler at the start of a propagation.
        
            This method is called once at the start of the propagation. It may be used by the step handler to initialize some
            internal data if needed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler.init` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler`
        
            Parameters:
                s0 (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): initial state
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): target time for the integration
        
        
        """
        ...

class StelaAbstractPropagator(fr.cnes.sirius.patrius.propagation.Propagator):
    """
    public abstract class StelaAbstractPropagator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
    
        Common handling of :class:`~fr.cnes.sirius.patrius.propagation.Propagator` methods for analytical propagators.
    
        This abstract class allows to provide easily the full set of :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        methods, including all propagation modes support and discrete events support for any simple propagation method. Only two
        methods must be implemented by derived classes:
        :meth:`~fr.cnes.sirius.patrius.stela.propagation.StelaAbstractPropagator.propagateSpacecraftState` and
        :meth:`~fr.cnes.sirius.patrius.stela.propagation.StelaAbstractPropagator.getMass`. The first method should perform
        straightforward propagation starting from some internally stored initial state up to the specified target date.
    
        Also see:
            :meth:`~serialized`
    """
    def addAdditionalStateProvider(self, additionalStateProvider: fr.cnes.sirius.patrius.propagation.AdditionalStateProvider) -> None: ...
    def addEventDetector(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector) -> None:
        """
            Add an event detector. Note that mean elements will be provided to event detectors in *g* function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.addEventDetector` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Parameters:
                detector (:class:`~fr.cnes.sirius.patrius.events.EventDetector`): event detector to add
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.clearEventsDetectors`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getEventsDetectors`
        
        
        """
        ...
    def addTimeDerivativeData(self, timeDerivativeData: fr.cnes.sirius.patrius.stela.propagation.data.TimeDerivativeData) -> None:
        """
            Add time derivatives data to list. Method for internal use only.
        
            Parameters:
                data (:class:`~fr.cnes.sirius.patrius.stela.propagation.data.TimeDerivativeData`): time derivative data
        
        
        """
        ...
    def clearEventsDetectors(self) -> None:
        """
            Remove all events detectors.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.clearEventsDetectors` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.addEventDetector`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getEventsDetectors`
        
        
        """
        ...
    def getAttitudeProvider(self) -> fr.cnes.sirius.patrius.attitudes.AttitudeProvider:
        """
            Get attitude provider.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getAttitudeProvider` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Returns:
                attitude provider for forces computation (by default)
        
        
        """
        ...
    def getAttitudeProviderEvents(self) -> fr.cnes.sirius.patrius.attitudes.AttitudeProvider:
        """
            Get attitude provider for events computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getAttitudeProviderEvents` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Returns:
                attitude provider for events computation
        
        
        """
        ...
    def getAttitudeProviderForces(self) -> fr.cnes.sirius.patrius.attitudes.AttitudeProvider:
        """
            Get attitude provider for forces computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getAttitudeProviderForces` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Returns:
                attitude provider for forces computation
        
        
        """
        ...
    def getEventsDetectors(self) -> java.util.Collection[fr.cnes.sirius.patrius.events.EventDetector]: ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the frame in which the orbit is propagated.
        
            4 cases are possible:
        
              - The propagation frame has been defined (using :code:`#setOrbitFrame(Frame)`): it is returned.
              - The propagation frame has not been defined and the initial state has been provided and is expressed in a pseudo-inertial
                frame: the initial state frame is returned.
              - The propagation frame has not been defined and the initial state has been provided and is not expressed in a
                pseudo-inertial frame: null is returned.
              - The propagation frame has not been defined and the initial state has not been provided: null is returned.
        
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getFrame` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Returns:
                frame in which the orbit is propagated
        
        
        """
        ...
    def getGeneratedEphemeris(self) -> fr.cnes.sirius.patrius.propagation.BoundedPropagator:
        """
            Get the ephemeris generated during propagation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getGeneratedEphemeris` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Returns:
                generated ephemeris
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setEphemerisMode`
        
        
        """
        ...
    def getInitialState(self) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def getMode(self) -> int:
        """
            Get the current operating mode of the propagator.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getMode` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Returns:
                one of :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.SLAVE_MODE`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.MASTER_MODE`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.EPHEMERIS_GENERATION_MODE`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setEphemerisMode`
        
        
        """
        ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getPvProvider(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Get PV coordinates provider.
        
            Returns:
                PV coordinates provider
        
        
        """
        ...
    def getSpacecraftState(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def getTimeDerivativesList(self) -> java.util.List[fr.cnes.sirius.patrius.stela.propagation.data.TimeDerivativeData]: ...
    def isRegisterTimeDerivatives(self) -> bool:
        """
            Returns flag indicating if time derivatives dE'/dt have to be stored during next step. Method for internal use only.
        
            Returns:
                flag indicating if time derivatives dE'/dt have to be stored during next step
        
        
        """
        ...
    def isStoreTimeDerivatives(self) -> bool:
        """
            Returns flag indicating if time derivatives dE'/dt must be stored.
        
            Returns:
                flag indicating if time derivatives dE'/dt must be stored
        
        
        """
        ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def resetInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    def setAttitudeProvider(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None:
        """
            Set attitude provider for forces and events computation. A default attitude provider is available in
            :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setAttitudeProvider` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Parameters:
                attitudeProviderIn (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider
        
        
        """
        ...
    def setAttitudeProviderEvents(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None:
        """
            Set attitude provider for events computation. A default attitude provider is available in
            :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setAttitudeProviderEvents` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Parameters:
                attitudeProviderIn (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider for events computation
        
        
        """
        ...
    def setAttitudeProviderForces(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None:
        """
            Set attitude provider for forces computation. A default attitude provider is available in
            :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setAttitudeProviderForces` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Parameters:
                attitudeProviderIn (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider for forces computation
        
        
        """
        ...
    def setEphemerisMode(self) -> None:
        """
            Set the propagator to ephemeris generation mode.
        
            This mode is used when the user needs random access to the orbit state at any time between the initial and target times,
            and in no sequential order. A typical example is the implementation of search and iterative algorithms that may navigate
            forward and backward inside the propagation range before finding their result.
        
            Beware that since this mode stores **all** intermediate results, it may be memory intensive for long integration ranges
            and high precision/short time steps.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setEphemerisMode` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getGeneratedEphemeris`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.EPHEMERIS_GENERATION_MODE`
        
        
        """
        ...
    def setIntegrator(self, firstOrderIntegrator: fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator) -> None:
        """
            Set the integrator.
        
            Parameters:
                integrator (:class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator`): integrator to use for propagation.
        
        
        """
        ...
    @typing.overload
    def setMasterMode(self, double: float, patriusFixedStepHandler: fr.cnes.sirius.patrius.propagation.sampling.PatriusFixedStepHandler) -> None:
        """
            Set the propagator to master mode with fixed steps.
        
            This mode is used when the user needs to have some custom function called at the end of each finalized step during
            integration. The (master) propagator integration loop calls the (slave) application callback methods at each finalized
            step.
            Note that mean elements will be provided by the step handler.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Parameters:
                h (double): fixed stepsize (s)
                handler (:class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusFixedStepHandler`): handler called at the end of each finalized step
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setEphemerisMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.MASTER_MODE`
        
        """
        ...
    @typing.overload
    def setMasterMode(self, patriusStepHandler: fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler) -> None:
        """
            Set the propagator to master mode with variable steps.
        
            This mode is used when the user needs to have some custom function called at the end of each finalized step during
            integration. The (master) propagator integration loop calls the (slave) application callback methods at each finalized
            step.
            Note that mean elements will be provided by the step handler.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Parameters:
                handler (:class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler`): handler called at the end of each finalized step
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setEphemerisMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.MASTER_MODE`
        
        
        """
        ...
    def setOrbitFrame(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> None: ...
    def setSlaveMode(self) -> None:
        """
            Set the propagator to slave mode.
        
            This mode is used when the user needs only the final orbit at the target time. The (slave) propagator computes this
            result and return it to the calling (master) application, without any intermediate feedback.
        
            This is the default mode.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setSlaveMode` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setEphemerisMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.SLAVE_MODE`
        
        
        """
        ...
    def setStoreTimeDerivatives(self, boolean: bool) -> None:
        """
            Setter for flag indicating if time derivatives dE'/dt must be stored.
        
            Parameters:
                isStoreTimeDerivatives (boolean): flag indicating if time derivatives dE'/dt must be stored
        
        
        """
        ...

class StelaAdditionalEquations(java.io.Serializable):
    """
    public interface StelaAdditionalEquations extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface representing the Stela GTO propagator additional equations.
    
        Since:
            1.3
    """
    def addInitialAdditionalState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def computeDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def getEquationsDimension(self) -> int:
        """
        
            Returns:
                the additional equations dimension
        
        
        """
        ...
    def getName(self) -> str:
        """
            Get the name of the additional state.
        
            Returns:
                name of the additional state
        
        
        """
        ...

class StelaBasicInterpolator(fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator):
    """
    public class StelaBasicInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator`
    
    
        Basic Linear Step Interpolator for StelaAbstractPropagator. Does not interpolate the attitude of the spacecraft at the
        moment.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def getCurrentDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the current grid date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.getCurrentDate` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator`
        
            Returns:
                current grid date
        
        
        """
        ...
    def getInitialState(self) -> fr.cnes.sirius.patrius.propagation.SpacecraftState:
        """
        
            Returns:
                the initialState
        
        
        """
        ...
    def getInterpolatedDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the interpolated date.
        
            If :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.setInterpolatedDate` has not been called,
            the date returned is the same as
            :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.getCurrentDate`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.getInterpolatedDate` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator`
        
            Returns:
                interpolated date
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.setInterpolatedDate`,
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.getInterpolatedState`
        
        
        """
        ...
    def getInterpolatedState(self) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def getPreviousDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the previous grid date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.getPreviousDate` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator`
        
            Returns:
                previous grid date
        
        
        """
        ...
    def isForward(self) -> bool:
        """
            Check is integration direction is forward in date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.isForward` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator`
        
            Returns:
                true if integration is forward in date
        
        
        """
        ...
    def linearInterpolation(self, double: float, double2: float, double3: float) -> float:
        """
            Interpolates lineary
        
            Parameters:
                linearCoeff (double): the linear coefficient
                before (double): the previous state
                after (double): the current state
        
            Returns:
                inter the interpolated value
        
        
        """
        ...
    def setAdditionalStateProviders(self, list: java.util.List[fr.cnes.sirius.patrius.propagation.AdditionalStateProvider]) -> None: ...
    def setInterpolatedDate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def storeSC(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, spacecraftState2: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...

class StelaDifferentialEquations(fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations):
    """
    public class StelaDifferentialEquations extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`
    
        Class representing the differential system of a STELA GTO propagation. It implements a Commons-Math first order
        differential equations system.
    
        Forces contributions to dE'/dt are computed and summed in this class (E' being the state vector of the mean orbital
        parameters).
    
        Since:
            1.3
    """
    STATE_SIZE: typing.ClassVar[int] = ...
    """
    public static final int STATE_SIZE
    
        Size of the state vector.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self, stelaGTOPropagator: 'StelaGTOPropagator'): ...
    def computeDerivatives(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Get the current time derivative of the state vector.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector
                yDot (double[]): placeholder array where to put the time derivative of the state vector
        
        
        """
        ...
    def getDimension(self) -> int:
        """
            Get the dimension of the problem.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations.getDimension` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`
        
            Returns:
                dimension of the problem
        
        
        """
        ...

class StelaAttitudeAdditionalEquations(StelaAdditionalEquations):
    """
    public abstract class StelaAttitudeAdditionalEquations extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.stela.propagation.StelaAdditionalEquations`
    
    
        This abstract class allows users to add their own attitude differential equations to a Stela GTO propagator.
    
        Since:
            2.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.stela.propagation.StelaAdditionalEquations`, :meth:`~serialized`
    """
    def __init__(self, attitudeType: fr.cnes.sirius.patrius.propagation.numerical.AttitudeEquation.AttitudeType): ...
    def getAttitudeType(self) -> fr.cnes.sirius.patrius.propagation.numerical.AttitudeEquation.AttitudeType:
        """
            Get the attitude type.
        
            Returns:
                the attitude type : ATTITUDE_FORCES or ATTITUDE_EVENTS or ATTITUDE
        
        
        """
        ...
    def getName(self) -> str:
        """
            Get the name of the additional equation. The name is in the following form : "ATTITUDE_FORCES" or "ATTITUDE_EVENTS" or
            "ATTITUDE".
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.propagation.StelaAdditionalEquations.getName` in
                interface :class:`~fr.cnes.sirius.patrius.stela.propagation.StelaAdditionalEquations`
        
            Returns:
                name of the additional equation
        
        
        """
        ...

class StelaGTOPropagator(StelaAbstractPropagator):
    @typing.overload
    def __init__(self, firstOrderIntegrator: fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator): ...
    @typing.overload
    def __init__(self, firstOrderIntegrator: fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator, double: float, double2: float): ...
    @typing.overload
    def __init__(self, firstOrderIntegrator: fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, stelaBasicInterpolator: StelaBasicInterpolator, double: float, double2: float): ...
    @typing.overload
    def __init__(self, firstOrderIntegrator: fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, stelaBasicInterpolator: StelaBasicInterpolator, double: float, double2: float): ...
    def addAdditionalEquations(self, stelaAdditionalEquations: StelaAdditionalEquations) -> None: ...
    def addAttitudeEquation(self, stelaAttitudeAdditionalEquations: StelaAttitudeAdditionalEquations) -> None: ...
    def addForceModel(self, stelaForceModel: fr.cnes.sirius.patrius.stela.forces.StelaForceModel) -> None: ...
    def getAddEquations(self) -> java.util.List[StelaAdditionalEquations]: ...
    def getForceModels(self) -> java.util.List[fr.cnes.sirius.patrius.stela.forces.StelaForceModel]: ...
    def getForcesStepHandler(self) -> ForcesStepHandler: ...
    def getGaussForceModels(self) -> java.util.List[fr.cnes.sirius.patrius.stela.forces.AbstractStelaGaussContribution]: ...
    def getLagrangeForceModels(self) -> java.util.List[fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution]: ...
    def getOrbitNatureConverter(self) -> fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter: ...
    def getReferenceDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def removeForceModels(self) -> None: ...
    def setAttitudeProvider(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None: ...
    def setAttitudeProviderEvents(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None: ...
    def setAttitudeProviderForces(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None: ...
    def setInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, double: float, boolean: bool) -> None: ...
    def setNatureConverter(self, list: java.util.List[fr.cnes.sirius.patrius.stela.forces.StelaForceModel]) -> None: ...

class StelaPartialDerivativesEquations(StelaAdditionalEquations):
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.stela.forces.AbstractStelaGaussContribution], list2: java.util.List[fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution], int: int, stelaGTOPropagator: StelaGTOPropagator): ...
    def addInitialAdditionalState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def computeDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def getDerivatives(self) -> java.util.Map[fr.cnes.sirius.patrius.stela.forces.StelaForceModel, typing.MutableSequence[typing.MutableSequence[float]]]: ...
    def getEquationsDimension(self) -> int: ...
    def getMeanMotion(self) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getName(self) -> str: ...
    def updateStepCounter(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.propagation")``.

    ForcesStepHandler: typing.Type[ForcesStepHandler]
    StelaAbstractPropagator: typing.Type[StelaAbstractPropagator]
    StelaAdditionalEquations: typing.Type[StelaAdditionalEquations]
    StelaAttitudeAdditionalEquations: typing.Type[StelaAttitudeAdditionalEquations]
    StelaBasicInterpolator: typing.Type[StelaBasicInterpolator]
    StelaDifferentialEquations: typing.Type[StelaDifferentialEquations]
    StelaGTOPropagator: typing.Type[StelaGTOPropagator]
    StelaPartialDerivativesEquations: typing.Type[StelaPartialDerivativesEquations]
    data: fr.cnes.sirius.patrius.stela.propagation.data.__module_protocol__
