
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.forces.gravity.potential
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.analytical.covariance
import fr.cnes.sirius.patrius.propagation.analytical.multi
import fr.cnes.sirius.patrius.propagation.analytical.tle
import fr.cnes.sirius.patrius.propagation.analytical.twod
import fr.cnes.sirius.patrius.propagation.sampling
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import typing



class AbstractLyddanePropagator(fr.cnes.sirius.patrius.propagation.AbstractPropagator, fr.cnes.sirius.patrius.propagation.MeanOsculatingElementsProvider):
    """
    public abstract class AbstractLyddanePropagator extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator` implements :class:`~fr.cnes.sirius.patrius.propagation.MeanOsculatingElementsProvider`
    
        Abstract Lyddane propagator. This class contains common algorithms to all Lyddane propagators.
    
        Since:
            3.2
    
        Also see:
            :meth:`~serialized`
    """
    def propagateMeanOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def propagateOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def resetInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    def setThreshold(self, double: float) -> None:
        """
            Setter for relative convergence threshold for osculating to mean algorithm.
        
            Parameters:
                newThreshold (double): new relative threshold
        
        
        """
        ...
    class LyddaneParametersType(java.lang.Enum['AbstractLyddanePropagator.LyddaneParametersType']):
        SECULAR: typing.ClassVar['AbstractLyddanePropagator.LyddaneParametersType'] = ...
        MEAN: typing.ClassVar['AbstractLyddanePropagator.LyddaneParametersType'] = ...
        OSCULATING: typing.ClassVar['AbstractLyddanePropagator.LyddaneParametersType'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'AbstractLyddanePropagator.LyddaneParametersType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['AbstractLyddanePropagator.LyddaneParametersType']: ...
    class SubModel(java.lang.Enum['AbstractLyddanePropagator.SubModel']):
        DEFAULT: typing.ClassVar['AbstractLyddanePropagator.SubModel'] = ...
        LOW_ECC: typing.ClassVar['AbstractLyddanePropagator.SubModel'] = ...
        HIGH_ECC: typing.ClassVar['AbstractLyddanePropagator.SubModel'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'AbstractLyddanePropagator.SubModel': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['AbstractLyddanePropagator.SubModel']: ...

class AdapterPropagator(fr.cnes.sirius.patrius.propagation.AbstractPropagator):
    """
    public class AdapterPropagator extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`
    
        Orbit propagator that adapts an underlying propagator, adding
        :class:`~fr.cnes.sirius.patrius.propagation.analytical.AdapterPropagator.DifferentialEffect`.
    
        This propagator is used when a reference propagator does not handle some effects that we need. A typical example would
        be an ephemeris that was computed for a reference orbit, and we want to compute a station-keeping maneuver on top of
        this ephemeris, changing its final state. The principal is to add one or more
        :class:`~fr.cnes.sirius.patrius.forces.maneuvers.SmallManeuverAnalyticalModel` to it and use it as a new propagator,
        which takes the maneuvers into account.
    
        From a space flight dynamics point of view, this is a differential correction approach. From a computer science point of
        view, this is a use of the decorator design pattern.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.Propagator`,
            :class:`~fr.cnes.sirius.patrius.forces.maneuvers.SmallManeuverAnalyticalModel`, :meth:`~serialized`
    """
    def __init__(self, propagator: fr.cnes.sirius.patrius.propagation.Propagator): ...
    def addEffect(self, differentialEffect: typing.Union['AdapterPropagator.DifferentialEffect', typing.Callable]) -> None:
        """
            Add a differential effect.
        
            Parameters:
                effect (:class:`~fr.cnes.sirius.patrius.propagation.analytical.AdapterPropagator.DifferentialEffect`): differential effect
        
        
        """
        ...
    def getEffects(self) -> java.util.List['AdapterPropagator.DifferentialEffect']: ...
    def getInitialState(self) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def getPropagator(self) -> fr.cnes.sirius.patrius.propagation.Propagator:
        """
            Get the reference propagator.
        
            Returns:
                reference propagator
        
        
        """
        ...
    def resetInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    class DifferentialEffect:
        def apply(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...

class AnalyticalEphemerisModeHandler(fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler):
    """
    public class AnalyticalEphemerisModeHandler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler`
    
        This class stores sequentially generated orbital parameters for later retrieval.
    
        Instances of this class are built and then must be fed with the results provided by
        :class:`~fr.cnes.sirius.patrius.propagation.Propagator` objects configured in
        :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setEphemerisMode`. Once propagation is over, a
        :class:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator` can be built from the stored steps.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator`, :meth:`~serialized`
    """
    def __init__(self, propagator: fr.cnes.sirius.patrius.propagation.Propagator, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider): ...
    def getEphemeris(self) -> fr.cnes.sirius.patrius.propagation.BoundedPropagator:
        """
            Get the generated ephemeris.
        
            Returns:
                a new instance of the generated ephemeris
        
        
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
    def setAttitudeProviderEvents(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None:
        """
            Set attitude provider for events computation.
        
            Parameters:
                attProvEvents (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): the attitude provider
        
        
        """
        ...
    def setAttitudeProviderForces(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider) -> None:
        """
            Set attitude provider for forces computation.
        
            Parameters:
                attProvForces (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): the attitude provider
        
        
        """
        ...

class EcksteinHechlerPropagator(fr.cnes.sirius.patrius.propagation.AbstractPropagator, fr.cnes.sirius.patrius.propagation.MeanOsculatingElementsProvider):
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, frame: fr.cnes.sirius.patrius.frames.Frame, double3: float, double4: float, double5: float, double6: float, double7: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, frame: fr.cnes.sirius.patrius.frames.Frame, double3: float, double4: float, double5: float, double6: float, double7: float, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, double: float, double2: float, frame: fr.cnes.sirius.patrius.frames.Frame, double3: float, double4: float, double5: float, double6: float, double7: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, double: float, double2: float, frame: fr.cnes.sirius.patrius.frames.Frame, double3: float, double4: float, double5: float, double6: float, double7: float, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, double: float, double2: float, frame: fr.cnes.sirius.patrius.frames.Frame, double3: float, double4: float, double5: float, double6: float, double7: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, double: float, double2: float, frame: fr.cnes.sirius.patrius.frames.Frame, double3: float, double4: float, double5: float, double6: float, double7: float, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType): ...
    def mean2osc(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def osc2mean(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def propagateMeanOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def propagateOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def resetInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    @staticmethod
    def setThreshold(double: float) -> None: ...

class J2SecularPropagator(fr.cnes.sirius.patrius.propagation.AbstractPropagator):
    """
    public class J2SecularPropagator extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`
    
        J2 secular propagator.
    
        This propagator is an analytical propagator taking into account only mean secular effects of J2 zonal harmonic.
    
        Since:
            3.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, frame: fr.cnes.sirius.patrius.frames.Frame, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, frame: fr.cnes.sirius.patrius.frames.Frame, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, frame: fr.cnes.sirius.patrius.frames.Frame, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, frame: fr.cnes.sirius.patrius.frames.Frame, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, frame: fr.cnes.sirius.patrius.frames.Frame, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider): ...
    def getTransitionMatrix(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def propagateOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def resetInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...

class KeplerianPropagator(fr.cnes.sirius.patrius.propagation.AbstractPropagator):
    """
    public class KeplerianPropagator extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`
    
        Simple keplerian orbit propagator.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.orbits.Orbit`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, double: float): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, double: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, double: float): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, double: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider): ...
    def resetInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...

class LiuMeanOsculatingConverter(fr.cnes.sirius.patrius.propagation.MeanOsculatingElementsProvider):
    """
    public class LiuMeanOsculatingConverter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.MeanOsculatingElementsProvider`
    
        Liu mean - osculating elements converter. It provides a mean - osculating elements conversion following Liu theory. Liu
        theory is detailed in the article published by J.J.F. Liu in 1980 entitled "Semianalytic Theory for a Close-Earth
        Artificial Satellite".
    
        Since:
            4.5
    """
    def __init__(self, double: float, double2: float, double3: float, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    def mean2osc(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def osc2mean(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def propagateMeanOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def setThreshold(self, double: float) -> None:
        """
            Setter for relative convergence threshold for osculating to mean algorithm.
        
            Parameters:
                newThreshold (double): new relative threshold
        
        
        """
        ...

class J2DifferentialEffect(AdapterPropagator.DifferentialEffect, java.io.Serializable):
    """
    public class J2DifferentialEffect extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.analytical.AdapterPropagator.DifferentialEffect`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Analytical model for J2 effect.
    
        This class computes the differential effect of J2 due to an initial orbit offset. A typical case is when an inclination
        maneuver changes an orbit inclination at time t :sub:`0` . As ascending node drift rate depends on inclination, the
        change induces a time-dependent change in ascending node for later dates.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.maneuvers.SmallManeuverAnalyticalModel`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, orbit2: fr.cnes.sirius.patrius.orbits.Orbit, boolean: bool, double: float, double2: float, double3: float): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, orbit2: fr.cnes.sirius.patrius.orbits.Orbit, boolean: bool, potentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.potential.PotentialCoefficientsProvider): ...
    @typing.overload
    def __init__(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, differentialEffect: typing.Union[AdapterPropagator.DifferentialEffect, typing.Callable], boolean: bool, double: float, double2: float, double3: float): ...
    @typing.overload
    def __init__(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, differentialEffect: typing.Union[AdapterPropagator.DifferentialEffect, typing.Callable], boolean: bool, potentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.potential.PotentialCoefficientsProvider): ...
    @typing.overload
    def apply(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit:
        """
            Compute the effect of the maneuver on an orbit.
        
            Parameters:
                orbit1 (:class:`~fr.cnes.sirius.patrius.orbits.Orbit`): original orbit at t :sub:`1` , without maneuver
        
            Returns:
                orbit at t :sub:`1` , taking the maneuver into account if t :sub:`1` > t :sub:`0`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.analytical.J2DifferentialEffect.apply`
        
        public :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState` apply(:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState` state1) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Apply the effect to a :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`.
        
            Applying the effect may be a no-op in some cases. A typical example is maneuvers, for which the state is changed only
            for time *after* the maneuver occurrence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.analytical.AdapterPropagator.DifferentialEffect.apply` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.analytical.AdapterPropagator.DifferentialEffect`
        
            Parameters:
                state1 (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): original state *without* the effect
        
            Returns:
                updated state at the same date, taking the effect into account if meaningful
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if effect cannot be computed
        
        
        """
        ...
    @typing.overload
    def apply(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...

class LyddaneLongPeriodPropagator(AbstractLyddanePropagator):
    """
    public class LyddaneLongPeriodPropagator extends :class:`~fr.cnes.sirius.patrius.propagation.analytical.AbstractLyddanePropagator`
    
        Lyddane long period propagator.
    
        Lyddane propagator is an analytical propagator taking into account only mean secular and long period effects of J2 to J5
        zonal harmonics.
    
        This propagator is valid for orbits with eccentricity lower than 0.9 and inclination not close to critical inclinations
    
        Since:
            3.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider): ...
    def mean2osc(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def osc2mean(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...

class LyddaneSecularPropagator(AbstractLyddanePropagator):
    """
    public class LyddaneSecularPropagator extends :class:`~fr.cnes.sirius.patrius.propagation.analytical.AbstractLyddanePropagator`
    
        Lyddane secular propagator.
    
        Lyddane propagator is an analytical propagator taking into account only mean secular effects of J2 to J5 zonal
        harmonics.
    
        This propagator is valid for orbits with eccentricity lower than 0.9 and inclination not close to critical inclinations
    
        Since:
            3.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, parametersType: fr.cnes.sirius.patrius.propagation.ParametersType, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider): ...
    def mean2osc(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def osc2mean(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def propagateMeanOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation.analytical")``.

    AbstractLyddanePropagator: typing.Type[AbstractLyddanePropagator]
    AdapterPropagator: typing.Type[AdapterPropagator]
    AnalyticalEphemerisModeHandler: typing.Type[AnalyticalEphemerisModeHandler]
    EcksteinHechlerPropagator: typing.Type[EcksteinHechlerPropagator]
    J2DifferentialEffect: typing.Type[J2DifferentialEffect]
    J2SecularPropagator: typing.Type[J2SecularPropagator]
    KeplerianPropagator: typing.Type[KeplerianPropagator]
    LiuMeanOsculatingConverter: typing.Type[LiuMeanOsculatingConverter]
    LyddaneLongPeriodPropagator: typing.Type[LyddaneLongPeriodPropagator]
    LyddaneSecularPropagator: typing.Type[LyddaneSecularPropagator]
    covariance: fr.cnes.sirius.patrius.propagation.analytical.covariance.__module_protocol__
    multi: fr.cnes.sirius.patrius.propagation.analytical.multi.__module_protocol__
    tle: fr.cnes.sirius.patrius.propagation.analytical.tle.__module_protocol__
    twod: fr.cnes.sirius.patrius.propagation.analytical.twod.__module_protocol__
