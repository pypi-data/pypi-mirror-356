
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.forces
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.ode
import fr.cnes.sirius.patrius.math.ode.nonstiff.cowell
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical.multi
import fr.cnes.sirius.patrius.propagation.sampling
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import jpype
import typing



class AdditionalEquations(java.io.Externalizable):
    """
    public interface AdditionalEquations extends `Externalizable <http://docs.oracle.com/javase/8/docs/api/java/io/Externalizable.html?is-external=true>`
    
        This interface allows users to add their own differential equations to a numerical propagator.
    
        In some cases users may need to integrate some problem-specific equations along with classical spacecraft equations of
        motions. One example is optimal control in low thrust where adjoint parameters linked to the minimized hamiltonian must
        be integrated. Another example is formation flying or rendez-vous which use the Clohessy-Whiltshire equations for the
        relative motion.
    
        This interface allows users to add such equations to a
        :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator`. Users provide the equations as an
        implementation of this interface and register it to the propagator thanks to its
        :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.addAdditionalEquations` method. Several such
        objects can be registered with each numerical propagator, but it is recommended to gather in the same object the sets of
        parameters which equations can interact on each others states.
    
        The additional parameters are gathered in a simple p array. The additional equations compute the pDot array, which is
        the time-derivative of the p array. Since the additional parameters p may also have an influence on the equations of
        motion themselves (for example an equation linked to a complex thrust model may induce an acceleration and a mass
        change), the same :class:`~fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations` already shared by all
        force models to add their contributions is also provided to the additional equations implementation object. This means
        these equations can be used as an additional force model if needed. If the additional parameters have no influence at
        all on the spacecraft state, this adder can simply be ignored.
    
        This interface is the numerical (read not already integrated) counterpart of the
        :class:`~fr.cnes.sirius.patrius.propagation.AdditionalStateProvider` interface. It allows to append various additional
        state parameters to any :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator`.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator`,
            :class:`~fr.cnes.sirius.patrius.propagation.AdditionalStateProvider`
    """
    def buildAdditionalState(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Build full first order additional state from second order y and yDot. This method is only used by second order
            integrator such as :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.CowellIntegrator`.
        
            Parameters:
                y (double[]): second order additional state y
                yDot (double[]): second order additional state derivative yDot
        
            Returns:
                full first order additional state
        
        
        """
        ...
    def computeDerivatives(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: 'TimeDerivativesEquations') -> None: ...
    def computeSecondDerivatives(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> typing.MutableSequence[float]: ...
    def extractY(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Retrieve second order additional state y from full first order additional state. This method is only used by second
            order integrator such as :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.CowellIntegrator`.
        
            Parameters:
                additionalState (double[]): full first order additional state
        
            Returns:
                second order additional state y
        
        
        """
        ...
    def extractYDot(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Retrieve second order additional state derivative yDot from full first order additional state. This method is only used
            by second order integrator such as :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.CowellIntegrator`.
        
            Parameters:
                additionalState (double[]): full first order additional state
        
            Returns:
                second order additional state derivative yDot
        
        
        """
        ...
    def getFirstOrderDimension(self) -> int:
        """
            Returns the number of first order additional states. This method is only used by second order integrator such as
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.CowellIntegrator`.
        
            Returns:
                the number of first order additional states
        
        
        """
        ...
    def getName(self) -> str:
        """
            Get the name of the additional state.
        
            Returns:
                name of the additional state
        
        
        """
        ...
    def getSecondOrderDimension(self) -> int:
        """
            Returns the number of second order additional states. This method is only used by second order integrator such as
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.CowellIntegrator`.
        
            Returns:
                the number of second order additional states
        
        
        """
        ...

class AdditionalEquationsAndTolerances(java.io.Externalizable):
    """
    public class AdditionalEquationsAndTolerances extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Externalizable <http://docs.oracle.com/javase/8/docs/api/java/io/Externalizable.html?is-external=true>`
    
        Internal class for additional equations and tolerances management.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, additionalEquations: AdditionalEquations): ...
    def getAbsTol(self) -> typing.MutableSequence[float]:
        """
            Returns absolute tolerance vector.
        
            Returns:
                absolute tolerance vector
        
        
        """
        ...
    def getEquations(self) -> AdditionalEquations:
        """
            Get the additional equations.
        
            Returns:
                additional equations
        
        
        """
        ...
    def getIndex1stOrder(self) -> int:
        """
            Returns position of equations in first order state vector.
        
            Returns:
                position of equations in first order state vector
        
        
        """
        ...
    def getIndex2ndOrder(self) -> int:
        """
            Returns position of equations in second order state vector.
        
            Returns:
                position of equations in second order state vector
        
        
        """
        ...
    def getRelTol(self) -> typing.MutableSequence[float]:
        """
            Returns relative tolerance vector.
        
            Returns:
                relative tolerance vector
        
        
        """
        ...
    def readExternal(self, objectInput: java.io.ObjectInput) -> None: ...
    def setIndex1stOrder(self, int: int) -> None:
        """
            Set position of equations in first order state vector (initially unknown).
        
            Parameters:
                index (int): index to set
        
        
        """
        ...
    def setIndex2ndOrder(self, int: int) -> None:
        """
            Set position of equations in second order state vector (initially unknown).
        
            Parameters:
                index (int): index to set
        
        
        """
        ...
    def setTolerances(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set tolerances (no size check).
        
            Parameters:
                aTol (double[]): absoluteTolerances
                rTol (double[]): relativeTolerances
        
        
        """
        ...
    def writeExternal(self, objectOutput: java.io.ObjectOutput) -> None: ...

class AdditionalStateInfo(java.io.Serializable, java.lang.Cloneable):
    """
    public final class AdditionalStateInfo extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, `Cloneable <http://docs.oracle.com/javase/8/docs/api/java/lang/Cloneable.html?is-external=true>`
    
        Utility class that describes in a minimal fashion the structure of an additional state. An instance contains the size of
        an additional state and its index in the state vector. The instance :code:`AdditionalStateInfo` is guaranteed to be
        immutable.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int, int2: int): ...
    def clone(self) -> 'AdditionalStateInfo':
        """
            Copy of the AdditionalStateInfo.
        
            Overrides:
                 in class 
        
            Returns:
                a copy of the AdditionalStateInfo object.
        
        
        """
        ...
    def getIndex(self) -> int:
        """
            Get the index of the additional state in the state vector.
        
            Returns:
                additional state index in the state vector
        
        
        """
        ...
    def getSize(self) -> int:
        """
            Get the size of the additional state.
        
            Returns:
                additional state size
        
        
        """
        ...

class JacobianParametersProvider:
    """
    public interface JacobianParametersProvider
    
        Interface for classes that can provide parameters for computing jacobians.
    
        Since:
            2.2
    """
    def getJacobianParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...

class Jacobianizer(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable):
    """
    public class Jacobianizer extends :class:`~fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable`
    
        Class enabling basic :class:`~fr.cnes.sirius.patrius.forces.ForceModel` instances to be used when processing spacecraft
        state partial derivatives.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, forceModel: fr.cnes.sirius.patrius.forces.ForceModel, collection: typing.Union[java.util.Collection['ParameterConfiguration'], typing.Sequence['ParameterConfiguration'], typing.Set['ParameterConfiguration']], double: float): ...
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...

class JacobiansMapper(java.io.Serializable):
    """
    public class JacobiansMapper extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Mapper between two-dimensional Jacobian matrices and one-dimensional additional state arrays.
    
        This class does not hold the states by itself. Instances of this class are guaranteed to be immutable.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.numerical.PartialDerivativesEquations`,
            :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator`,
            :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`, :meth:`~serialized`
    """
    def __init__(self, string: str, list: java.util.List[fr.cnes.sirius.patrius.math.parameter.Parameter], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    def getAdditionalStateDimension(self) -> int:
        """
            Compute the length of the one-dimensional additional state array needed.
        
            Returns:
                length of the one-dimensional additional state array
        
        
        """
        ...
    def getAngleType(self) -> fr.cnes.sirius.patrius.orbits.PositionAngle:
        """
            Getter for the position angle type.
        
            Returns:
                the position angle type
        
        
        """
        ...
    def getName(self) -> str:
        """
            Get the name of the partial Jacobians.
        
            Returns:
                name of the Jacobians
        
        
        """
        ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Getter for the orbit type.
        
            Returns:
                the orbit type
        
        
        """
        ...
    def getParameters(self) -> int:
        """
            Get the number of parameters.
        
            Returns:
                number of parameters
        
        
        """
        ...
    @typing.overload
    def getParametersJacobian(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> typing.MutableSequence[float]: ...
    @typing.overload
    def getParametersJacobian(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame) -> typing.MutableSequence[float]: ...
    @typing.overload
    def getParametersJacobian(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @typing.overload
    def getParametersJacobian(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @typing.overload
    def getParametersJacobian(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    def getParametersJacobian(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[float], jpype.JArray], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame) -> None: ...
    @typing.overload
    def getParametersJacobian(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    @typing.overload
    def getParametersJacobian(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame) -> None: ...
    def getParametersList(self) -> java.util.List[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def getPropagationFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Getter for the propagation frame.
        
            Returns:
                the propagation frame
        
        
        """
        ...
    def getStateDimension(self) -> int:
        """
            Get the state vector dimension.
        
            Returns:
                state vector dimension
        
        
        """
        ...
    @typing.overload
    def getStateJacobian(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @typing.overload
    def getStateJacobian(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @typing.overload
    def getStateJacobian(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    @typing.overload
    def getStateJacobian(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, frame: fr.cnes.sirius.patrius.frames.Frame) -> None: ...
    def setInitialJacobians(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray]) -> None: ...

class ModeHandler:
    """
    public interface ModeHandler
    
        Common interface for all propagator mode handlers initialization.
    """
    def initialize(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, map: typing.Union[java.util.Map[str, AdditionalStateInfo], typing.Mapping[str, AdditionalStateInfo]], boolean: bool, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> None: ...
    def setReference(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Define new reference date.
        
            To be called by :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator` only.
        
            Parameters:
                newReference (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): new reference date
        
        
        """
        ...

class NumericalPropagator(fr.cnes.sirius.patrius.propagation.Propagator, java.util.Observer):
    """
    public class NumericalPropagator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.Propagator`, `Observer <http://docs.oracle.com/javase/8/docs/api/java/util/Observer.html?is-external=true>`
    
        This class propagates :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState` using numerical integration.
    
        Numerical propagation is much more accurate than analytical propagation like for example
        :class:`~fr.cnes.sirius.patrius.propagation.analytical.KeplerianPropagator` or
        :class:`~fr.cnes.sirius.patrius.propagation.analytical.EcksteinHechlerPropagator`, but requires a few more steps to set
        up to be used properly. Whereas analytical propagators are configured only thanks to their various constructors and can
        be used immediately after construction, numerical propagators configuration involve setting several parameters between
        construction time and propagation time.
    
        The configuration parameters that can be set are:
    
          -         the initial spacecraft state (:meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.setInitialState`)
          - the central attraction coefficient (:code:`#setMu(double)`)
          - the various force models (:meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.addForceModel`,
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.removeForceModels`)
          - the :class:`~fr.cnes.sirius.patrius.orbits.OrbitType` of orbital parameters to be used for propagation (
            :code:`#setOrbitType(OrbitType)`),
          - the :class:`~fr.cnes.sirius.patrius.orbits.PositionAngle` of position angle to be used in orbital parameters to be used
            for propagation where it is relevant (:code:`#setPositionAngleType(PositionAngle)`),
          - whether :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations` (for example
            :class:`~fr.cnes.sirius.patrius.propagation.numerical.PartialDerivativesEquations`) should be propagated along with
            orbital state ( :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.addAdditionalEquations`),
          - the discrete events that should be triggered during propagation (
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.addEventDetector`,
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.clearEventsDetectors`)
          - the binding logic with the rest of the application
            (:meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.setSlaveMode`,
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.setMasterMode`,
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.setMasterMode`,
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.setEphemerisMode`,
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.getGeneratedEphemeris`)
    
    
        From these configuration parameters, only the initial state is mandatory. The default propagation settings are in
        :meth:`~fr.cnes.sirius.patrius.orbits.OrbitType.EQUINOCTIAL` parameters with
        :meth:`~fr.cnes.sirius.patrius.orbits.PositionAngle.TRUE` longitude argument. If the central attraction coefficient is
        not explicitly specified, the one used to define the initial orbit will be used. However, specifying only the initial
        state and a Newtonian gravity model would mean the propagator would use only keplerian forces. In this case, the simpler
        :class:`~fr.cnes.sirius.patrius.propagation.analytical.KeplerianPropagator` class would perhaps be more effective.
    
        The underlying numerical integrator set up in the constructor may also have its own configuration parameters. Typical
        configuration parameters for adaptive stepsize integrators are the min, max and perhaps start step size as well as the
        absolute and/or relative errors thresholds.
    
        The state that is seen by the integrator is a simple six elements double array. The six first elements are either:
    
          - the :class:`~fr.cnes.sirius.patrius.orbits.EquinoctialOrbit` (a, e :sub:`x` , e :sub:`y` , h :sub:`x` , h :sub:`y` , λ
            :sub:`M` or λ :sub:`E` or λ :sub:`v` ) in meters and radians,
          - the :class:`~fr.cnes.sirius.patrius.orbits.KeplerianOrbit` (a, e, i, ω, Ω, M or E or v) in meters and radians,
          - the :class:`~fr.cnes.sirius.patrius.orbits.CircularOrbit` (a, e :sub:`x` , e :sub:`y` , i, Ω, α :sub:`M` or α
            :sub:`E` or α :sub:`v` ) in meters and radians,
          - the :class:`~fr.cnes.sirius.patrius.orbits.CartesianOrbit` (x, y, z, v :sub:`x` , v :sub:`y` , v :sub:`z` ) in meters
            and meters per seconds.
    
    
        The following code snippet shows a typical setting for Low Earth Orbit propagation in equinoctial parameters and true
        longitude argument:
    
        .. code-block: java
        
        
         final double dP = 0.001;
         final double minStep = 0.001;
         final double maxStep = 500;
         final double initStep = 60;
         AdaptiveStepsizeIntegrator integrator = new DormandPrince853Integrator(minStep, maxStep, AbsTolerance, RelTolerance);
         integrator.setInitialStepSize(initStep);
         propagator = new NumericalPropagator(integrator);
         
    
        The same propagator can be reused for several state extrapolations, by resetting the initial state without modifying the
        other configuration parameters. However, the same instance cannot be used simultaneously by different threads, the class
        is *not* thread-safe.
        **Warning** : when using a fixed step handler (method
        :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.setMasterMode`, with an Assembly, users must
        access to the additional states (such as mass) by the spacecraft AND NOT using the Assembly since Assembly is
        synchronized only once per integration step. In any other case (using an
        :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler` ) for instance), both assembly and spacecraft
        can be used to retrieve additional states.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`, :class:`~fr.cnes.sirius.patrius.forces.ForceModel`,
            :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler`,
            :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusFixedStepHandler`,
            :class:`~fr.cnes.sirius.patrius.propagation.precomputed.IntegratedEphemeris`,
            :class:`~fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, firstOrderIntegrator: fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator): ...
    @typing.overload
    def __init__(self, firstOrderIntegrator: fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, firstOrderIntegrator: fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator, frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle): ...
    def addAdditionalEquations(self, additionalEquations: AdditionalEquations) -> None:
        """
            Add a set of user-specified equations to be integrated along with the orbit propagation. If the set of equations is
            already registered, it is replaced by the new one.
        
            Parameters:
                addEqu (:class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`): additional equations
        
            Also see:
        
        
        """
        ...
    def addAttitudeEquation(self, attitudeEquation: 'AttitudeEquation') -> None:
        """
            Add a set of user-specified attitude equations to be integrated along with the orbit propagation. If the set of attitude
            equations is already registered for the current attitude, it is replaced by the new one.
        
            Parameters:
                addEqu (:class:`~fr.cnes.sirius.patrius.propagation.numerical.AttitudeEquation`): attitude additional equations
        
        
        """
        ...
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
    def addForceModel(self, forceModel: fr.cnes.sirius.patrius.forces.ForceModel) -> None:
        """
            Add a force model to the global model.
        
            Advice: in order to minimize absorption effects leading to reduced accuracy, add force models from least force to
            highest force. Example: for LEO orbits, drag should be added in last.
        
            Parameters:
                model (:class:`~fr.cnes.sirius.patrius.forces.ForceModel`): :class:`~fr.cnes.sirius.patrius.forces.ForceModel` to add
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.removeForceModels`
        
        
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
    def getBasicDimension(self) -> int:
        """
            Get state vector dimension without additional parameters.
        
            Returns:
                state vector dimension without additional parameters.
        
        
        """
        ...
    def getCalls(self) -> int:
        """
            Get the number of calls to the differential equations computation method.
        
            The number of calls is reset each time the
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.propagate` method is called.
        
            Returns:
                number of calls to the differential equations computation method
        
        
        """
        ...
    def getDimension(self) -> int:
        """
            Compute complete state vector dimension.
        
            Returns:
                state vector dimension
        
        
        """
        ...
    def getEventsDetectors(self) -> java.util.Collection[fr.cnes.sirius.patrius.events.EventDetector]: ...
    def getForceModels(self) -> java.util.List[fr.cnes.sirius.patrius.forces.ForceModel]: ...
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
    def getInitialState(self) -> fr.cnes.sirius.patrius.propagation.SpacecraftState:
        """
            Get the propagator initial state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getInitialState` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Returns:
                initial state
        
        
        """
        ...
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
    def getMu(self) -> float:
        """
            Get the central attraction coefficient μ.
        
            Returns:
                mu central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
            Also see:
                :code:`#setMu(double)`
        
        
        """
        ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Get propagation parameter type.
        
            Returns:
                orbit type used for propagation
        
        
        """
        ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getPositionAngleType(self) -> fr.cnes.sirius.patrius.orbits.PositionAngle:
        """
            Get propagation parameter type.
        
            Returns:
                angle type to use for propagation
        
        
        """
        ...
    def getSpacecraftState(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    @typing.overload
    def propagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def removeForceModels(self) -> None:
        """
            Remove all force models from the global model.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.addForceModel`
        
        
        """
        ...
    def resetInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None:
        """
            Reset the propagator initial state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.resetInitialState` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): new initial state to consider
        
        
        """
        ...
    def setAdditionalStateTolerance(self, string: str, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
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
                attitudeEventsProvider (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider for events computation
        
        
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
                attitudeForcesProvider (:class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`): attitude provider for forces computation
        
        
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
        
            Note that this method has the side effect of replacing the step handlers of the underlying integrator set up in the
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.NumericalPropagator` or the
            :code:`setIntegrator` method. So if a specific step handler is needed, it should be added after this method has been
            called.
        
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
    def setInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None:
        """
            Set the initial state.
        
            Parameters:
                initialStateIn (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): initial state
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.propagate`
        
        
        """
        ...
    def setMassProviderEquation(self, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider) -> None:
        """
            Add additional equations associated with the mass provider. A null-mass detector associated with the input mass provider
            is automatically added.
        
            Note that this method should be called after
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.setSlaveMode` or
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.setMasterMode` or
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.setEphemerisMode` since this method reset the
            integrator step handlers list.
        
            **WARNING**: This method should be called only once and provided mass provider should be the same used for force models.
        
            Parameters:
                massProvider (:class:`~fr.cnes.sirius.patrius.propagation.MassProvider`): the mass provider
        
        
        """
        ...
    @typing.overload
    def setMasterMode(self, double: float, patriusFixedStepHandler: fr.cnes.sirius.patrius.propagation.sampling.PatriusFixedStepHandler) -> None:
        """
            Set the propagator to master mode with fixed steps.
        
            This mode is used when the user needs to have some custom function called at the end of each finalized step during
            integration. The (master) propagator integration loop calls the (slave) application callback methods at each finalized
            step.
        
            Note that this method has the side effect of replacing the step handlers of the underlying integrator set up in the
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.NumericalPropagator` or the
            :code:`setIntegrator` method. So if a specific step handler is needed, it should be added after this method has been
            called.
        
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
        
            Note that this method has the side effect of replacing the step handlers of the underlying integrator set up in the
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.NumericalPropagator` or the
            :code:`setIntegrator` method. So if a specific step handler is needed, it should be added after this method has been
            callled.
        
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
    def setSlaveMode(self) -> None:
        """
            Set the propagator to slave mode.
        
            This mode is used when the user needs only the final orbit at the target time. The (slave) propagator computes this
            result and return it to the calling (master) application, without any intermediate feedback.
        
            This is the default mode.
        
            Note that this method has the side effect of replacing the step handlers of the underlying integrator set up in the
            :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.NumericalPropagator` or the
            :code:`setIntegrator` method. So if a specific step handler is needed, it should be added after this method has been
            callled.
        
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
    @staticmethod
    def tolerances(double: float, orbit: fr.cnes.sirius.patrius.orbits.Orbit, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Estimate tolerance vectors for integrators.
        
            The errors are estimated from partial derivatives properties of orbits, starting from a scalar position error specified
            by the user. Considering the energy conservation equation V = sqrt(mu (2/r - 1/a)), we get at constant energy (i.e. on a
            Keplerian trajectory):
        
            .. code-block: java
            
            
             V :sup:`2`  r |dV| = mu |dr|
             
            So we deduce a scalar velocity error consistent with the position error. From here, we apply orbits Jacobians matrices
            to get consistent errors on orbital parameters.
        
            The tolerances are only *orders of magnitude*, and integrator tolerances are only local estimates, not global ones. So
            some care must be taken when using these tolerances. Setting 1mm as a position error does NOT mean the tolerances will
            guarantee a 1mm error position after several orbits integration.
        
            Parameters:
                dP (double): user specified position error
                orbit (:class:`~fr.cnes.sirius.patrius.orbits.Orbit`): reference orbit
                type (:class:`~fr.cnes.sirius.patrius.orbits.OrbitType`): propagation type for the meaning of the tolerance vectors elements (it may be different from :code:`orbit.getType()`)
        
            Returns:
                a two rows array, row 0 being the absolute tolerance error and row 1 being the relative tolerance error
        
        
        """
        ...
    def update(self, observable: java.util.Observable, object: typing.Any) -> None:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...

class ParameterConfiguration(java.io.Serializable):
    """
    public class ParameterConfiguration extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Simple container associating a parameter name with a step to compute its jacobian and the provider thant manages it.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float): ...
    def getHP(self) -> float:
        """
            Get parameter step.
        
            Returns:
                hP parameter step
        
        
        """
        ...
    def getParameter(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Get parameter.
        
            Returns:
                parameter
        
        
        """
        ...
    def getProvider(self) -> fr.cnes.sirius.patrius.math.parameter.IJacobiansParameterizable:
        """
            Get the povider handling this parameter.
        
            Returns:
                provider handling this parameter
        
        
        """
        ...
    def setProvider(self, iJacobiansParameterizable: fr.cnes.sirius.patrius.math.parameter.IJacobiansParameterizable) -> None:
        """
            Set the povider handling this parameter.
        
            Parameters:
                providerIn (:class:`~fr.cnes.sirius.patrius.math.parameter.IJacobiansParameterizable`): provider handling this parameter
        
        
        """
        ...

class SecondOrderMapper(fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.SecondOrderStateMapper):
    """
    public class SecondOrderMapper extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.SecondOrderStateMapper`
    
        Second-order / first order integrator state mapper.
    
        Since:
            4.6
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, list: java.util.List[AdditionalEquationsAndTolerances]): ...
    def buildFullState(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Build full first order state from second order y and yDot.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.SecondOrderStateMapper`
        
            Parameters:
                y (double[]): second order state y
                yDot (double[]): second order state derivative yDot
        
            Returns:
                full first order state
        
        
        """
        ...
    def extractY(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Retrieve second order state y from full first order state.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.SecondOrderStateMapper`
        
            Parameters:
                fullState (double[]): full first order state
        
            Returns:
                second order state y
        
        
        """
        ...
    def extractYDot(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Retrieve second order state derivative yDot from full first order state.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.SecondOrderStateMapper`
        
            Parameters:
                fullState (double[]): full first order state
        
            Returns:
                second order state derivative yDot
        
        
        """
        ...
    def readExternal(self, objectInput: java.io.ObjectInput) -> None: ...
    def writeExternal(self, objectOutput: java.io.ObjectOutput) -> None: ...

class TimeDerivativesEquations(java.io.Serializable):
    """
    public interface TimeDerivativesEquations extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface summing up the contribution of several forces into orbit and mass derivatives.
    
        The aim of this interface is to gather the contributions of various perturbing forces expressed as accelerations into
        one set of time-derivatives of :class:`~fr.cnes.sirius.patrius.orbits.Orbit`. It implements Gauss equations for
        different kind of parameters.
    
        An implementation of this interface is automatically provided by
        :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator` to the various
        :class:`~fr.cnes.sirius.patrius.forces.ForceModel`.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.ForceModel`,
            :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator`
    """
    def addAcceleration(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> None: ...
    def addAdditionalStateDerivative(self, string: str, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Add the contribution of the change rate (dX/dt) of the additional state.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the additional state name
                pDot (double[]): the change rate (dX/dt)
        
            Raises:
                : if the mass flow-rate is positive
        
        
        """
        ...
    def addXYZAcceleration(self, double: float, double2: float, double3: float) -> None:
        """
            Add the contribution of an acceleration expressed in the inertial frame (it is important to make sure this acceleration
            is defined in the same frame as the orbit) .
        
            Parameters:
                x (double): acceleration along the X axis (m/s :sup:`2` )
                y (double): acceleration along the Y axis (m/s :sup:`2` )
                z (double): acceleration along the Z axis (m/s :sup:`2` )
        
        
        """
        ...
    def initDerivatives(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> None: ...

class AbstractPartialDerivativesEquations(AdditionalEquations):
    """
    public abstract class AbstractPartialDerivativesEquations extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`
    
        Abstract class for :class:`~fr.cnes.sirius.patrius.propagation.numerical.PartialDerivativesEquations` and
        :class:`~fr.cnes.sirius.patrius.propagation.numerical.multi.MultiPartialDerivativesEquations`.
    
        Since:
            4.8
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...
    def buildAdditionalState(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Build full first order additional state from second order y and yDot. This method is only used by second order
            integrator such as :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.CowellIntegrator`.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`
        
            Parameters:
                y (double[]): second order additional state y
                yDot (double[]): second order additional state derivative yDot
        
            Returns:
                full first order additional state
        
        
        """
        ...
    def clearSelectedParameters(self) -> None:
        """
            Clear the selected parameters list.
        
        """
        ...
    def computeDerivatives(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: TimeDerivativesEquations) -> None: ...
    def computeSecondDerivatives(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> typing.MutableSequence[float]: ...
    def concatenate(self, list: java.util.List[fr.cnes.sirius.patrius.math.parameter.Parameter]) -> None: ...
    def contains(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Check if the parameter is already in the selectedParameters list
        
            Parameters:
                parameter (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): to check
        
            Returns:
                true if the parameter is in the list false otherwise
        
        
        """
        ...
    def extractY(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Retrieve second order additional state y from full first order additional state. This method is only used by second
            order integrator such as :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.CowellIntegrator`.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`
        
            Parameters:
                additionalState (double[]): full first order additional state
        
            Returns:
                second order additional state y
        
        
        """
        ...
    def extractYDot(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Retrieve second order additional state derivative yDot from full first order additional state. This method is only used
            by second order integrator such as :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.CowellIntegrator`.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`
        
            Parameters:
                additionalState (double[]): full first order additional state
        
            Returns:
                second order additional state derivative yDot
        
        
        """
        ...
    def getAvailableParameters(self) -> java.util.List[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def getFirstOrderDimension(self) -> int:
        """
            Returns the number of first order additional states. This method is only used by second order integrator such as
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.CowellIntegrator`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations.getFirstOrderDimension` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`
        
            Returns:
                the number of first order additional states
        
        
        """
        ...
    def getJacobiansProviders(self) -> java.util.List[fr.cnes.sirius.patrius.math.parameter.IJacobiansParameterizable]: ...
    def getMapper(self) -> JacobiansMapper: ...
    def getName(self) -> str:
        """
            Get the name of the additional state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations.getName` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`
        
            Returns:
                name of the additional state
        
        
        """
        ...
    def getParamDim(self) -> int:
        """
            Returns the parameters dimension.
        
            Returns:
                the parameters dimension
        
        
        """
        ...
    def getSecondOrderDimension(self) -> int:
        """
            Returns the number of second order additional states. This method is only used by second order integrator such as
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.CowellIntegrator`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations.getSecondOrderDimension` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`
        
            Returns:
                the number of second order additional states
        
        
        """
        ...
    def getSelectedParameters(self) -> java.util.List[ParameterConfiguration]: ...
    def gethPos(self) -> float:
        """
            Returns the step used for finite difference computation with respect to spacecraft position.
        
            Returns:
                the step used for finite difference computation with respect to spacecraft position
        
        
        """
        ...
    def isDirty(self) -> bool:
        """
            Returns a boolean for force models / selected parameters consistency.
        
            Returns:
                the boolean for force models / selected parameters consistency
        
        
        """
        ...
    def isInitialJacobians(self) -> bool:
        """
            Returns true if the initial Jacobians have not been initialized yet.
        
            Returns:
                the if the initial Jacobians have not been initialized yet
        
        
        """
        ...
    def readExternal(self, objectInput: java.io.ObjectInput) -> None: ...
    def selectParamAndStep(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float) -> None:
        """
            Select the parameters to consider for Jacobian processing.
        
            Parameters names have to be consistent with some :class:`~fr.cnes.sirius.patrius.forces.ForceModel` added elsewhere.
        
            Parameters:
                parameter (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to consider for Jacobian processing. Parameter will not be added if already added elsewhere
                hP (double): step to use for computing Jacobian column with respect to the specified parameter
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.addForceModel`, null,
                :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable`
        
        
        """
        ...
    @typing.overload
    def selectParameters(self, *parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> None:
        """
            Select the parameters to consider for Jacobian processing.
        
            Parameters names have to be consistent with some :class:`~fr.cnes.sirius.patrius.forces.ForceModel` added elsewhere.
        
            Parameters:
                parameters (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`...): parameters to consider for Jacobian processing. Parameters will not be added if already added elsewhere
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.addForceModel`, null,
                :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable`
        
        public void selectParameters(`List <http://docs.oracle.com/javase/8/docs/api/java/util/List.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`> parameters)
        
            Select the parameters to consider for Jacobian processing.
        
            Parameters names have to be consistent with some :class:`~fr.cnes.sirius.patrius.forces.ForceModel` added elsewhere.
        
            Parameters:
                parameters (`List <http://docs.oracle.com/javase/8/docs/api/java/util/List.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`> parameters): list of parameters to consider for Jacobian processing
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.addForceModel`, null,
                :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable`
        
        
        """
        ...
    @typing.overload
    def selectParameters(self, list: java.util.List[fr.cnes.sirius.patrius.math.parameter.Parameter]) -> None: ...
    def setDirty(self, boolean: bool) -> None:
        """
            Setter for the boolean for force models / selected parameters consistency.
        
            Parameters:
                value (boolean): the new boolean for force models / selected parameters consistency
        
        
        """
        ...
    def setHPos(self, double: float) -> None:
        """
            Setter for the step used for finite difference computation with respect to spacecraft position
        
            Parameters:
                value (double): the new step used for finite difference computation with respect to spacecraft position
        
        
        """
        ...
    @typing.overload
    def setInitialJacobians(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    @typing.overload
    def setInitialJacobians(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    @typing.overload
    def setInitialJacobians(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    @typing.overload
    def setInitialJacobians(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def setSteps(self, double: float) -> None:
        """
            Set the step for finite differences with respect to spacecraft position.
        
            Parameters:
                hPosition (double): step used for finite difference computation with respect to spacecraft position (m)
        
        
        """
        ...
    def writeExternal(self, objectOutput: java.io.ObjectOutput) -> None: ...

class AttitudeEquation(AdditionalEquations):
    """
    public abstract class AttitudeEquation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`
    
    
        This interface allows users to add their own attitude differential equations to a numerical propagator.
    
        Since:
            2.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`, :meth:`~serialized`
    """
    def __init__(self, attitudeType: 'AttitudeEquation.AttitudeType'): ...
    def getAttitudeType(self) -> 'AttitudeEquation.AttitudeType':
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
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations.getName` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations`
        
            Returns:
                name of the additional equation
        
        
        """
        ...
    class AttitudeType(java.lang.Enum['AttitudeEquation.AttitudeType']):
        ATTITUDE_FORCES: typing.ClassVar['AttitudeEquation.AttitudeType'] = ...
        ATTITUDE_EVENTS: typing.ClassVar['AttitudeEquation.AttitudeType'] = ...
        ATTITUDE: typing.ClassVar['AttitudeEquation.AttitudeType'] = ...
        def toString(self) -> str: ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'AttitudeEquation.AttitudeType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['AttitudeEquation.AttitudeType']: ...

class PartialDerivativesEquations(AbstractPartialDerivativesEquations):
    """
    public class PartialDerivativesEquations extends :class:`~fr.cnes.sirius.patrius.propagation.numerical.AbstractPartialDerivativesEquations`
    
        Set of :class:`~fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations` computing the partial derivatives of
        the state (orbit) with respect to initial state and force models parameters.
    
        This set of equations are automatically added to a
        :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator` in order to compute partial derivatives of
        the orbit along with the orbit itself. This is useful for example in orbit determination applications.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str, numericalPropagator: NumericalPropagator): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation.numerical")``.

    AbstractPartialDerivativesEquations: typing.Type[AbstractPartialDerivativesEquations]
    AdditionalEquations: typing.Type[AdditionalEquations]
    AdditionalEquationsAndTolerances: typing.Type[AdditionalEquationsAndTolerances]
    AdditionalStateInfo: typing.Type[AdditionalStateInfo]
    AttitudeEquation: typing.Type[AttitudeEquation]
    JacobianParametersProvider: typing.Type[JacobianParametersProvider]
    Jacobianizer: typing.Type[Jacobianizer]
    JacobiansMapper: typing.Type[JacobiansMapper]
    ModeHandler: typing.Type[ModeHandler]
    NumericalPropagator: typing.Type[NumericalPropagator]
    ParameterConfiguration: typing.Type[ParameterConfiguration]
    PartialDerivativesEquations: typing.Type[PartialDerivativesEquations]
    SecondOrderMapper: typing.Type[SecondOrderMapper]
    TimeDerivativesEquations: typing.Type[TimeDerivativesEquations]
    multi: fr.cnes.sirius.patrius.propagation.numerical.multi.__module_protocol__
