
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.attitudes.multi
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.frames.transformations
import fr.cnes.sirius.patrius.math.utils
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation.analytical
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.propagation.precomputed
import fr.cnes.sirius.patrius.propagation.sampling
import fr.cnes.sirius.patrius.propagation.sampling.multi
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import jpype
import typing



class AdditionalStateProvider(java.io.Serializable):
    """
    public interface AdditionalStateProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface represents providers for additional state data beyond
        :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`.
    
        This interface is the analytical (read already integrated) counterpart of the
        :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations` interface. It allows to append various
        additional state parameters to any :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`,
            :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`
    """
    def getAdditionalState(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]: ...
    def getName(self) -> str:
        """
            Get the name of the additional state.
        
            Returns:
                name of the additional state
        
        
        """
        ...

class MassProvider(java.lang.Cloneable, java.io.Serializable):
    """
    public interface MassProvider extends `Cloneable <http://docs.oracle.com/javase/8/docs/api/java/lang/Cloneable.html?is-external=true>`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for spacecraft models that provide the mass.
    
        Since:
            2.1
    """
    MASS: typing.ClassVar[str] = ...
    """
    static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` MASS
    
        Default prefix for additional equation from MassProvider.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def addMassDerivative(self, string: str, double: float) -> None:
        """
            Add the mass derivate of the given part.
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of part subject to mass variation
                flowRate (double): flow rate of specified part
        
        
        """
        ...
    def getAdditionalEquation(self, string: str) -> fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations:
        """
            Get the mass equation related to the part.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): part name
        
            Returns:
                the associated mass equation
        
        
        """
        ...
    def getAllPartsNames(self) -> java.util.List[str]: ...
    def getMass(self, string: str) -> float:
        """
            Return the mass of the given part.
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): given part
        
            Returns:
                mass of part
        
        
        """
        ...
    @typing.overload
    def getTotalMass(self) -> float:
        """
            Return the mass of the spacecraft.
        
            Returns:
                spacecraft mass
        
        """
        ...
    @typing.overload
    def getTotalMass(self, spacecraftState: 'SpacecraftState') -> float:
        """
            Return the mass of the spacecraft following the order.
        
              - If mass is in spacecraft state, mass from spacecraft state will be returned
              - Otherwise mass from mass provider is returned (same as
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass`)
        
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
            Returns:
                spacecraft mass
        
        
        """
        ...
    def setMassDerivativeZero(self, string: str) -> None:
        """
            Set mass derivative to zero.
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of part whose mass derivative is set to zero
        
        
        """
        ...
    def updateMass(self, string: str, double: float) -> None: ...

class MeanOsculatingElementsProvider:
    """
    public interface MeanOsculatingElementsProvider
    
        Interface for mean/osculating elements converter.
    
        This interface provides methods to convert from mean elements to osculating elements and in return.
    
        Since:
            3.2
    """
    def mean2osc(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def osc2mean(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def propagateMeanOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit: ...

class MultiPropagator:
    """
    public interface MultiPropagator
    
    
        This interface is copied from :class:`~fr.cnes.sirius.patrius.propagation.Propagator` and adapted to multi propagation.
    
        This interface provides a way to propagate several :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`
        (including orbit, attitudes and additional states) at any time.
    
        This interface is the top-level abstraction for multi states propagation. An initial state is identified by its ID. It
        could be added to the propagator through :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`.
        All initial states added should have the same initial state. Each initial state is defined with a proper frame with can
        be retrieved using :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getFrame`. This interface only allows
        propagation to a predefined date by calling :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.propagate` or
        :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.propagate`.
    
        This interface is implemented by numerical integrators using rich force models and by continuous models built after
        numerical integration has been completed and dense output data as been gathered.
    
        Since:
            3.0
    """
    SLAVE_MODE: typing.ClassVar[int] = ...
    """
    static final int SLAVE_MODE
    
        Indicator for slave mode.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MASTER_MODE: typing.ClassVar[int] = ...
    """
    static final int MASTER_MODE
    
        Indicator for master mode.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EPHEMERIS_GENERATION_MODE: typing.ClassVar[int] = ...
    """
    static final int EPHEMERIS_GENERATION_MODE
    
        Indicator for ephemeris generation mode.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def addEventDetector(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, string: str) -> None:
        """
            Add an event detector to a specific spacecraft. The spacecraft defined by the input ID should already be added using
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`.
        
            Parameters:
                detector (:class:`~fr.cnes.sirius.patrius.events.EventDetector`): event detector to add
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.clearEventsDetectors`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getEventsDetectors`
        
        
        """
        ...
    @typing.overload
    def addEventDetector(self, multiEventDetector: fr.cnes.sirius.patrius.events.MultiEventDetector) -> None:
        """
            Add a multi spacecraft event detector.
        
            Parameters:
                detector (:class:`~fr.cnes.sirius.patrius.events.MultiEventDetector`): event detector to add
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.clearEventsDetectors`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getEventsDetectors`
        
        """
        ...
    def addInitialState(self, spacecraftState: 'SpacecraftState', string: str) -> None: ...
    def clearEventsDetectors(self) -> None:
        """
            Remove all events detectors.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addEventDetector`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addEventDetector`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getEventsDetectors`
        
        
        """
        ...
    def getAttitudeProvider(self, string: str) -> fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider:
        """
        
            Get the default attitude provider.
        
            The unique attitude provider given by default is returned. If null, the attitude provider for forces computation, and
            then the attitude provider for events computation is returned.
        
            **Warning: if you provided an :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider` then to get back your
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`, the returned
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider` should be cast to
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper` and method
            :meth:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper.getAttitudeProvider` should be used.**
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                attitude provider for forces computation (by default)
        
        
        """
        ...
    def getAttitudeProviderEvents(self, string: str) -> fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider:
        """
        
            Get the attitude provider for events computation.
        
            **Warning: if you provided an :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider` then to get back your
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`, the returned
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider` should be cast to
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper` and method
            :meth:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper.getAttitudeProvider` should be used.**
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                attitude provider for events computation, return null if not defined.
        
        
        """
        ...
    def getAttitudeProviderForces(self, string: str) -> fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider:
        """
        
            Get the attitude provider for forces computation.
        
            **Warning: if you provided an :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider` then to get back your
            :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`, the returned
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider` should be cast to
            :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper` and method
            :meth:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProviderWrapper.getAttitudeProvider` should be used.**
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                attitude provider for forces computation, return null if not defined.
        
        
        """
        ...
    def getEventsDetectors(self) -> java.util.Collection[fr.cnes.sirius.patrius.events.MultiEventDetector]: ...
    def getFrame(self, string: str) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the frame in which the orbit is propagated.
        
            The propagation frame is the definition frame of the initial state, so this method should be called after this state has
            been set.
        
            The spacecraft defined by the input ID should already be added using
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`.
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                frame in which the orbit is propagated
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`
        
        
        """
        ...
    def getGeneratedEphemeris(self, string: str) -> 'BoundedPropagator':
        """
            Get the ephemeris generated during propagation for a defined spacecraft.
        
            Parameters:
                satId (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the spacecraft ID
        
            Returns:
                generated ephemeris
        
            Raises:
                : if the propagator was not set in ephemeris generation mode before propagation
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`
        
        
        """
        ...
    def getInitialStates(self) -> java.util.Map[str, 'SpacecraftState']: ...
    def getMode(self) -> int:
        """
            Get the current operating mode of the propagator.
        
            Returns:
                one of :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.SLAVE_MODE`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.MASTER_MODE`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.EPHEMERIS_GENERATION_MODE`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`
        
        
        """
        ...
    def getSpacecraftState(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, string: str) -> 'SpacecraftState': ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.Map[str, 'SpacecraftState']: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> java.util.Map[str, 'SpacecraftState']: ...
    def setAttitudeProvider(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, string: str) -> None:
        """
        
            Set attitude provider for defined spacecraft.
        
            A default attitude provider is available in :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            The spacecraft defined by the input ID should already be added using
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`.
        
            Parameters:
                satId (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): the spacecraft ID
                attitudeProvider (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): attitude provider
        
        
        """
        ...
    def setAttitudeProviderEvents(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, string: str) -> None:
        """
        
            Set attitude provider for events computation.
        
            A default attitude provider is available in :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            The spacecraft defined by the input ID should already be added using
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`.
        
            Parameters:
                satId (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): the spacecraft ID
                attitudeProviderEvents (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): attitude provider for events computation
        
        
        """
        ...
    def setAttitudeProviderForces(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, string: str) -> None:
        """
        
            Set attitude provider for forces computation.
        
            A default attitude provider is available in :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            The spacecraft defined by the input ID should already be added using
            :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.addInitialState`.
        
            Parameters:
                satId (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): the spacecraft ID
                attitudeProviderForces (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): attitude provider for forces computation
        
        
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
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getGeneratedEphemeris`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.EPHEMERIS_GENERATION_MODE`
        
        
        """
        ...
    @typing.overload
    def setMasterMode(self, double: float, multiPatriusFixedStepHandler: fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusFixedStepHandler) -> None:
        """
            Set the propagator to master mode with fixed steps.
        
            This mode is used when the user needs to have some custom function called at the end of each finalized step during
            integration. The (master) propagator integration loop calls the (slave) application callback methods at each finalized
            step.
        
            Parameters:
                h (double): fixed stepsize (s)
                handler (:class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusFixedStepHandler`): handler called at the end of each finalized step
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.MASTER_MODE`
        
        """
        ...
    @typing.overload
    def setMasterMode(self, multiPatriusStepHandler: fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepHandler) -> None:
        """
            Set the propagator to master mode with variable steps.
        
            This mode is used when the user needs to have some custom function called at the end of each finalized step during
            integration. The (master) propagator integration loop calls the (slave) application callback methods at each finalized
            step.
        
            Parameters:
                handler (:class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepHandler`): handler called at the end of each finalized step
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.MASTER_MODE`
        
        
        """
        ...
    def setSlaveMode(self) -> None:
        """
            Set the propagator to slave mode.
        
            This mode is used when the user needs only the final orbit at the target time. The (slave) propagator computes this
            result and return it to the calling (master) application, without any intermediate feedback.
        
            This is the default mode.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.SLAVE_MODE`
        
        
        """
        ...

class ParametersType(java.lang.Enum['ParametersType']):
    """
    public enum ParametersType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.propagation.ParametersType`>
    
        Enum class for elements type (mean or osculating).
    
        Since:
            3.2
    """
    MEAN: typing.ClassVar['ParametersType'] = ...
    OSCULATING: typing.ClassVar['ParametersType'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'ParametersType':
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
    def values() -> typing.MutableSequence['ParametersType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (ParametersType c : ParametersType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class SpacecraftState(fr.cnes.sirius.patrius.time.TimeStamped, fr.cnes.sirius.patrius.time.TimeShiftable['SpacecraftState'], fr.cnes.sirius.patrius.time.TimeInterpolable['SpacecraftState'], java.io.Serializable):
    MASS: typing.ClassVar[str] = ...
    ORBIT_DIMENSION: typing.ClassVar[int] = ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double2: float, frame: fr.cnes.sirius.patrius.frames.Frame, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo]], attitude: fr.cnes.sirius.patrius.attitudes.Attitude, attitude2: fr.cnes.sirius.patrius.attitudes.Attitude): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double2: float, frame: fr.cnes.sirius.patrius.frames.Frame, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo]], attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider): ...
    @typing.overload
    def __init__(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, orbit: fr.cnes.sirius.patrius.orbits.Orbit): ...
    @typing.overload
    def __init__(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, orbit: fr.cnes.sirius.patrius.orbits.Orbit, massProvider: MassProvider): ...
    @typing.overload
    def __init__(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, orbit: fr.cnes.sirius.patrius.orbits.Orbit, massProvider: MassProvider, map: typing.Union[java.util.Map[str, typing.Union[typing.List[float], jpype.JArray]], typing.Mapping[str, typing.Union[typing.List[float], jpype.JArray]]]): ...
    @typing.overload
    def __init__(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, orbit: fr.cnes.sirius.patrius.orbits.Orbit, map: typing.Union[java.util.Map[str, typing.Union[typing.List[float], jpype.JArray]], typing.Mapping[str, typing.Union[typing.List[float], jpype.JArray]]]): ...
    @typing.overload
    def __init__(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, orbit: fr.cnes.sirius.patrius.orbits.Orbit): ...
    @typing.overload
    def __init__(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, orbit: fr.cnes.sirius.patrius.orbits.Orbit, massProvider: MassProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitude: fr.cnes.sirius.patrius.attitudes.Attitude): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitude: fr.cnes.sirius.patrius.attitudes.Attitude, attitude2: fr.cnes.sirius.patrius.attitudes.Attitude): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitude: fr.cnes.sirius.patrius.attitudes.Attitude, attitude2: fr.cnes.sirius.patrius.attitudes.Attitude, massProvider: MassProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitude: fr.cnes.sirius.patrius.attitudes.Attitude, attitude2: fr.cnes.sirius.patrius.attitudes.Attitude, massProvider: MassProvider, map: typing.Union[java.util.Map[str, typing.Union[typing.List[float], jpype.JArray]], typing.Mapping[str, typing.Union[typing.List[float], jpype.JArray]]]): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitude: fr.cnes.sirius.patrius.attitudes.Attitude, attitude2: fr.cnes.sirius.patrius.attitudes.Attitude, map: typing.Union[java.util.Map[str, typing.Union[typing.List[float], jpype.JArray]], typing.Mapping[str, typing.Union[typing.List[float], jpype.JArray]]]): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitude: fr.cnes.sirius.patrius.attitudes.Attitude, massProvider: MassProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, massProvider: MassProvider): ...
    def addAdditionalState(self, string: str, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> 'SpacecraftState': ...
    def addAttitude(self, attitude: fr.cnes.sirius.patrius.attitudes.Attitude, attitudeType: fr.cnes.sirius.patrius.propagation.numerical.AttitudeEquation.AttitudeType) -> 'SpacecraftState': ...
    def addAttitudeToAdditionalStates(self, attitudeType: fr.cnes.sirius.patrius.propagation.numerical.AttitudeEquation.AttitudeType) -> 'SpacecraftState': ...
    def addMassProvider(self, massProvider: MassProvider) -> 'SpacecraftState': ...
    @staticmethod
    def equalsAddStates(map: typing.Union[java.util.Map[str, typing.Union[typing.List[float], jpype.JArray]], typing.Mapping[str, typing.Union[typing.List[float], jpype.JArray]]], map2: typing.Union[java.util.Map[str, typing.Union[typing.List[float], jpype.JArray]], typing.Mapping[str, typing.Union[typing.List[float], jpype.JArray]]]) -> bool: ...
    def getA(self) -> float: ...
    def getAdditionalState(self, string: str) -> typing.MutableSequence[float]: ...
    def getAdditionalStates(self) -> java.util.Map[str, typing.MutableSequence[float]]: ...
    def getAdditionalStatesInfos(self) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo]: ...
    def getAdditionalStatesMass(self) -> java.util.Map[str, typing.MutableSequence[float]]: ...
    @typing.overload
    def getAttitude(self) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, lOFType: fr.cnes.sirius.patrius.frames.LOFType) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitudeEvents(self) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitudeEvents(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitudeEvents(self, lOFType: fr.cnes.sirius.patrius.frames.LOFType) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitudeForces(self) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitudeForces(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitudeForces(self, lOFType: fr.cnes.sirius.patrius.frames.LOFType) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
    def getE(self) -> float: ...
    def getEquinoctialEx(self) -> float: ...
    def getEquinoctialEy(self) -> float: ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame: ...
    def getHx(self) -> float: ...
    def getHy(self) -> float: ...
    def getI(self) -> float: ...
    def getKeplerianMeanMotion(self) -> float: ...
    def getKeplerianPeriod(self) -> float: ...
    def getLE(self) -> float: ...
    def getLM(self) -> float: ...
    def getLv(self) -> float: ...
    def getMass(self, string: str) -> float: ...
    def getMu(self) -> float: ...
    def getOrbit(self) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    @typing.overload
    def getPVCoordinates(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    @typing.overload
    def getPVCoordinates(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    @staticmethod
    def getSpacecraftStateLight(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'SpacecraftState': ...
    def getStateVectorSize(self) -> int: ...
    @typing.overload
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, list: java.util.List[fr.cnes.sirius.patrius.orbits.Orbit]) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    @typing.overload
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection['SpacecraftState'], typing.Sequence['SpacecraftState'], typing.Set['SpacecraftState']]) -> 'SpacecraftState': ...
    def mapStateToArray(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def shiftedBy(self, double: float) -> 'SpacecraftState': ...
    @typing.overload
    def toTransform(self) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def toTransform(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def toTransform(self, frame: fr.cnes.sirius.patrius.frames.Frame, lOFType: fr.cnes.sirius.patrius.frames.LOFType) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def toTransform(self, lOFType: fr.cnes.sirius.patrius.frames.LOFType) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def toTransformEvents(self) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def toTransformEvents(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def toTransformForces(self) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    @typing.overload
    def toTransformForces(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...
    def updateMass(self, string: str, double: float) -> 'SpacecraftState': ...
    def updateOrbit(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> 'SpacecraftState': ...

class SpacecraftStateProvider(fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider):
    """
    public interface SpacecraftStateProvider extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
    
        Interface for spacecraft state providers.
    """
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getSpacecraftState(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> SpacecraftState: ...

class Propagator(SpacecraftStateProvider):
    """
    public interface Propagator extends :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftStateProvider`
    
        This interface provides a way to propagate an orbit at any time.
    
        This interface is the top-level abstraction for orbit propagation. It only allows propagation to a predefined date. It
        is implemented by analytical models which have no time limit, by orbit readers based on external data files, by
        numerical integrators using rich force models and by continuous models built after numerical integration has been
        completed and dense output data as been gathered.
    """
    SLAVE_MODE: typing.ClassVar[int] = ...
    """
    static final int SLAVE_MODE
    
        Indicator for slave mode.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MASTER_MODE: typing.ClassVar[int] = ...
    """
    static final int MASTER_MODE
    
        Indicator for master mode.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EPHEMERIS_GENERATION_MODE: typing.ClassVar[int] = ...
    """
    static final int EPHEMERIS_GENERATION_MODE
    
        Indicator for ephemeris generation mode.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def addEventDetector(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector) -> None:
        """
            Add an event detector.
        
            Parameters:
                detector (:class:`~fr.cnes.sirius.patrius.events.EventDetector`): event detector to add
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.clearEventsDetectors`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getEventsDetectors`
        
        
        """
        ...
    def clearEventsDetectors(self) -> None:
        """
            Remove all events detectors.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.addEventDetector`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getEventsDetectors`
        
        
        """
        ...
    def getAttitudeProvider(self) -> fr.cnes.sirius.patrius.attitudes.AttitudeProvider:
        """
            Get attitude provider.
        
            Returns:
                attitude provider for forces computation (by default)
        
        
        """
        ...
    def getAttitudeProviderEvents(self) -> fr.cnes.sirius.patrius.attitudes.AttitudeProvider:
        """
            Get attitude provider for events computation.
        
            Returns:
                attitude provider for events computation
        
        
        """
        ...
    def getAttitudeProviderForces(self) -> fr.cnes.sirius.patrius.attitudes.AttitudeProvider:
        """
            Get attitude provider for forces computation.
        
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
        
        
            Returns:
                frame in which the orbit is propagated
        
        
        """
        ...
    def getGeneratedEphemeris(self) -> 'BoundedPropagator':
        """
            Get the ephemeris generated during propagation.
        
            Returns:
                generated ephemeris
        
            Raises:
                : if the propagator was not set in ephemeris generation mode before propagation
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setEphemerisMode`
        
        
        """
        ...
    def getInitialState(self) -> SpacecraftState: ...
    def getMode(self) -> int:
        """
            Get the current operating mode of the propagator.
        
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
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.Frame: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> SpacecraftState: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> SpacecraftState: ...
    def resetInitialState(self, spacecraftState: SpacecraftState) -> None: ...
    def setAttitudeProvider(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None:
        """
            Set attitude provider for forces and events computation. A default attitude provider is available in
            :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            Parameters:
                attitudeProvider (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider
        
        
        """
        ...
    def setAttitudeProviderEvents(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None:
        """
            Set attitude provider for events computation. A default attitude provider is available in
            :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            Parameters:
                attitudeProviderEvents (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider for events computation
        
        
        """
        ...
    def setAttitudeProviderForces(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None:
        """
            Set attitude provider for forces computation. A default attitude provider is available in
            :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            Parameters:
                attitudeProviderForces (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider for forces computation
        
        
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
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getGeneratedEphemeris`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setSlaveMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.EPHEMERIS_GENERATION_MODE`
        
        
        """
        ...
    @typing.overload
    def setMasterMode(self, double: float, patriusFixedStepHandler: fr.cnes.sirius.patrius.propagation.sampling.PatriusFixedStepHandler) -> None:
        """
            Set the propagator to master mode with fixed steps.
        
            This mode is used when the user needs to have some custom function called at the end of each finalized step during
            integration. The (master) propagator integration loop calls the (slave) application callback methods at each finalized
            step.
        
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
    def setSlaveMode(self) -> None:
        """
            Set the propagator to slave mode.
        
            This mode is used when the user needs only the final orbit at the target time. The (slave) propagator computes this
            result and return it to the calling (master) application, without any intermediate feedback.
        
            This is the default mode.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setMasterMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setEphemerisMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getMode`,
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.SLAVE_MODE`
        
        
        """
        ...

class SimpleAdditionalStateProvider(AdditionalStateProvider):
    """
    public final class SimpleAdditionalStateProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.AdditionalStateProvider`
    
    
        This class is a simple implementation of additionalStateProvider. It is composed of a name, a dates table, and an
        additional states table associated to the dates. An ISearch index provides a way to find the nearest index table for a
        given date. It provides an additional state at a date through linear interpolation of the given additional states table.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str, absoluteDateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.time.AbsoluteDate], jpype.JArray], doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex): ...
    def getAdditionalState(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]:
        """
            Get the additional state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.AdditionalStateProvider.getAdditionalState` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.AdditionalStateProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date to which additional state is computed
        
            Returns:
                additional state at this date
        
        
        """
        ...
    def getName(self) -> str:
        """
            Get the name of the additional state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.AdditionalStateProvider.getName` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.AdditionalStateProvider`
        
            Returns:
                name of the additional state
        
        
        """
        ...

class SimpleMassModel(MassProvider):
    """
    public class SimpleMassModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
    
        Simple implementation of :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`. The mass DOESNT vary!
    
        Since:
            2.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, string: str): ...
    def addMassDerivative(self, string: str, double: float) -> None:
        """
            This model represents one part only. The expected partName is the name of the model given at construction time. Add the
            mass derivate of the given part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.addMassDerivative` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of part subject to mass variation
                flowRate (double): flow rate of specified part
        
        
        """
        ...
    def getAdditionalEquation(self, string: str) -> fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations:
        """
            Get the mass equation related to the part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getAdditionalEquation` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): part name
        
            Returns:
                the associated mass equation
        
        
        """
        ...
    def getAllPartsNames(self) -> java.util.List[str]: ...
    def getMass(self, string: str) -> float:
        """
            This model represents one part only. The expected partName is the name of the model given at construction time. Return
            the mass of the given part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): given part
        
            Returns:
                mass of part
        
        
        """
        ...
    @typing.overload
    def getTotalMass(self) -> float:
        """
            Return the mass of the spacecraft.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Returns:
                spacecraft mass
        
        """
        ...
    @typing.overload
    def getTotalMass(self, spacecraftState: SpacecraftState) -> float:
        """
            Return the mass of the spacecraft following the order.
        
              - If mass is in spacecraft state, mass from spacecraft state will be returned
              - Otherwise mass from mass provider is returned (same as
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass`)
        
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
            Returns:
                spacecraft mass
        
        
        """
        ...
    def setMassDerivativeZero(self, string: str) -> None:
        """
            Set mass derivative to zero.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.setMassDerivativeZero` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of part whose mass derivative is set to zero
        
        
        """
        ...
    def updateMass(self, string: str, double: float) -> None:
        """
            This model represents one part only. The expected partName is the name of the model given at construction time. Update
            the mass of the given part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.updateMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): given part
                mass (double): mass of the given part
        
        
        """
        ...

class AbstractPropagator(Propagator):
    """
    public abstract class AbstractPropagator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
    
        Common handling of :class:`~fr.cnes.sirius.patrius.propagation.Propagator` methods for analytical propagators.
    
        This abstract class allows to provide easily the full set of :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        methods, including all propagation modes support and discrete events support for any simple propagation method. Only one
        method must be implemented by derived classes:
        :meth:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator.propagateOrbit`. The first method should perform
        straightforward propagation starting from some internally stored initial state up to the specified target date.
    
        Also see:
            :meth:`~serialized`
    """
    MASS: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` MASS
    
        Default prefix for additional state provider from MassProvider.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def addAdditionalStateProvider(self, additionalStateProvider: AdditionalStateProvider) -> None:
        """
            Add a set of user-specified state parameters to be computed along with the orbit propagation.
        
            Parameters:
                additionalStateProvider (:class:`~fr.cnes.sirius.patrius.propagation.AdditionalStateProvider`): provider for additional state
        
            Add a set of state parameters from MassProvider to be computed along with the orbit propagation.
        
            Parameters:
                massProvider (:class:`~fr.cnes.sirius.patrius.propagation.MassProvider`): mass provider for additional state
        
        
        """
        ...
    @typing.overload
    def addAdditionalStateProvider(self, massProvider: MassProvider) -> None: ...
    def addEventDetector(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector) -> None:
        """
            Add an event detector.
        
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
    def getGeneratedEphemeris(self) -> 'BoundedPropagator':
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
    def getInitialState(self) -> SpacecraftState: ...
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
    def getSpacecraftState(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> SpacecraftState: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> SpacecraftState: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> SpacecraftState: ...
    def resetInitialState(self, spacecraftState: SpacecraftState) -> None: ...
    def setAttitudeProvider(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None:
        """
            Set attitude provider for forces and events computation. A default attitude provider is available in
            :class:`~fr.cnes.sirius.patrius.attitudes.ConstantAttitudeLaw`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setAttitudeProvider` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Parameters:
                attitudeProvider (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider
        
        
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
                attProviderEvents (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider for events computation
        
        
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
                attProviderForces (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider for forces computation
        
        
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
    @typing.overload
    def setMasterMode(self, double: float, patriusFixedStepHandler: fr.cnes.sirius.patrius.propagation.sampling.PatriusFixedStepHandler) -> None:
        """
            Set the propagator to master mode with fixed steps.
        
            This mode is used when the user needs to have some custom function called at the end of each finalized step during
            integration. The (master) propagator integration loop calls the (slave) application callback methods at each finalized
            step.
        
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

class BoundedPropagator(Propagator):
    """
    public interface BoundedPropagator extends :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
    
        This interface is intended for ephemerides valid only during a time range.
    
        This interface provides a mean to retrieve orbital parameters at any time within a given range. It should be implemented
        by orbit readers based on external data files and by continuous models built after numerical integration has been
        completed and dense output data as been gathered.
    """
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the last date of the range.
        
            Returns:
                the last date of the range
        
        
        """
        ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the first date of the range.
        
            Returns:
                the first date of the range
        
        
        """
        ...
    def setOrbitFrame(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> None: ...

class AnalyticalIntegratedEphemeris(AbstractPropagator, BoundedPropagator):
    """
    public class AnalyticalIntegratedEphemeris extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator` implements :class:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator`
    
        This class stores sequentially generated orbital parameters for later retrieval.
    
        Instances of this class are built and then must be fed with the results provided by
        :class:`~fr.cnes.sirius.patrius.propagation.Propagator` objects configured in
        :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setEphemerisMode`. Once propagation is o, random access to any
        intermediate state of the orbit throughout the propagation range is possible.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], list2: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], list3: java.util.List[SpacecraftState], propagator: Propagator, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, boolean: bool): ...
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
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator.getFrame` in
                class :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`
        
            Returns:
                frame in which the orbit is propagated
        
        
        """
        ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the last date of the range.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator.getMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator`
        
            Returns:
                the last date of the range
        
        
        """
        ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the first date of the range.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator.getMinDate` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator`
        
            Returns:
                the first date of the range
        
        
        """
        ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> SpacecraftState: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> SpacecraftState: ...

class PVCoordinatesPropagator(AbstractPropagator):
    """
    public class PVCoordinatesPropagator extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`
    
    
        This class is an analytical propagator which propagates states from the input PV, Attitude, and additional state
        provider.
    
        It can handle events and all functionalities from extended
        :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator` class.
    
        The :meth:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator.resetInitialState` will do nothing on this propagator
        but is authorized to reset possible included attitude laws for instance.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, frame: fr.cnes.sirius.patrius.frames.Frame, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, list: java.util.List[AdditionalStateProvider]): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation")``.

    AbstractPropagator: typing.Type[AbstractPropagator]
    AdditionalStateProvider: typing.Type[AdditionalStateProvider]
    AnalyticalIntegratedEphemeris: typing.Type[AnalyticalIntegratedEphemeris]
    BoundedPropagator: typing.Type[BoundedPropagator]
    MassProvider: typing.Type[MassProvider]
    MeanOsculatingElementsProvider: typing.Type[MeanOsculatingElementsProvider]
    MultiPropagator: typing.Type[MultiPropagator]
    PVCoordinatesPropagator: typing.Type[PVCoordinatesPropagator]
    ParametersType: typing.Type[ParametersType]
    Propagator: typing.Type[Propagator]
    SimpleAdditionalStateProvider: typing.Type[SimpleAdditionalStateProvider]
    SimpleMassModel: typing.Type[SimpleMassModel]
    SpacecraftState: typing.Type[SpacecraftState]
    SpacecraftStateProvider: typing.Type[SpacecraftStateProvider]
    analytical: fr.cnes.sirius.patrius.propagation.analytical.__module_protocol__
    numerical: fr.cnes.sirius.patrius.propagation.numerical.__module_protocol__
    precomputed: fr.cnes.sirius.patrius.propagation.precomputed.__module_protocol__
    sampling: fr.cnes.sirius.patrius.propagation.sampling.__module_protocol__
