
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.ode
import java.io
import java.lang
import jpype
import typing



class FixedStepHandler:
    """
    public interface FixedStepHandler
    
        This interface represents a handler that should be called after each successful fixed step.
    
        This interface should be implemented by anyone who is interested in getting the solution of an ordinary differential
        equation at fixed time steps. Objects implementing this interface should be wrapped within an instance of
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer` that itself is used as the general
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler` by the integrator. The
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer` object is called according to the integrator internal
        algorithms and it calls objects implementing this interface as necessary at fixed time steps.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer`
    """
    def handleStep(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], boolean: bool) -> None:
        """
            Handle the last accepted step
        
            Parameters:
                t (double): time of the current step
                y (double[]): state vector at t. For efficiency purposes, the :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer` class
                    reuses the same array on each call, so if the instance wants to keep it across all calls (for example to provide at the
                    end of the integration a complete array of all steps), it should build a local copy store this copy.
                yDot (double[]): derivatives of the state vector state vector at t. For efficiency purposes, the
                    :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer` class reuses the same array on each call, so if the
                    instance wants to keep it across all calls (for example to provide at the end of the integration a complete array of all
                    steps), it should build a local copy store this copy.
                isLast (boolean): true if the step is the last one
        
        
        """
        ...
    def init(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float) -> None:
        """
            Initialize step handler at the start of an ODE integration.
        
            This method is called once at the start of the integration. It may be used by the step handler to initialize some
            internal data if needed.
        
            Parameters:
                t0 (double): start value of the independent *time* variable
                y0 (double[]): array containing the start value of the state vector
                t (double): target time for the integration
        
        
        """
        ...

class StepHandler:
    """
    public interface StepHandler
    
        This interface represents a handler that should be called after each successful step.
    
        The ODE integrators compute the evolution of the state vector at some grid points that depend on their own internal
        algorithm. Once they have found a new grid point (possibly after having computed several evaluation of the derivative at
        intermediate points), they provide it to objects implementing this interface. These objects typically either ignore the
        intermediate steps and wait for the last one, store the points in an ephemeris, or forward them to specialized
        processing or output methods.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.SecondOrderIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
    """
    def handleStep(self, stepInterpolator: 'StepInterpolator', boolean: bool) -> None:
        """
            Handle the last accepted step
        
            Parameters:
                interpolator (:class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`): interpolator for the last accepted step. For efficiency purposes, the various integrators reuse the same object on each
                    call, so if the instance wants to keep it across all calls (for example to provide at the end of the integration a
                    continuous model valid throughout the integration range, as the
                    :class:`~fr.cnes.sirius.patrius.math.ode.ContinuousOutputModel` class does), it should build a local copy using the
                    clone method of the interpolator and store this copy. Keeping only a reference to the interpolator and reusing it will
                    result in unpredictable behavior (potentially crashing the application).
                isLast (boolean): true if the step is the last one
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the interpolator throws one because the number of functions evaluations is exceeded
        
        
        """
        ...
    def init(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float) -> None:
        """
            Initialize step handler at the start of an ODE integration.
        
            This method is called once at the start of the integration. It may be used by the step handler to initialize some
            internal data if needed.
        
            Parameters:
                t0 (double): start value of the independent *time* variable
                y0 (double[]): array containing the start value of the state vector
                t (double): target time for the integration
        
        
        """
        ...

class StepInterpolator(java.io.Externalizable):
    """
    public interface StepInterpolator extends `Externalizable <http://docs.oracle.com/javase/8/docs/api/java/io/Externalizable.html?is-external=true>`
    
        This interface represents an interpolator over the last step during an ODE integration.
    
        The various ODE integrators provide objects implementing this interface to the step handlers. These objects are often
        custom objects tightly bound to the integrator internal algorithms. The handlers can use these objects to retrieve the
        state vector at intermediate times between the previous and the current grid points (this feature is often called dense
        output).
    
        One important thing to note is that the step handlers may be so tightly bound to the integrators that they often share
        some internal state arrays. This imply that one should *never* use a direct reference to a step interpolator outside of
        the step handler, either for future use or for use in another thread. If such a need arise, the step interpolator *must*
        be copied using the dedicated :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.copy` method.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.SecondOrderIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`
    """
    def copy(self) -> 'StepInterpolator':
        """
            Copy the instance.
        
            The copied instance is guaranteed to be independent from the original one. Both can be used with different settings for
            interpolated time without any side effect.
        
            Returns:
                a deep copy of the instance, which can be used independently.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded during step finalization
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.setInterpolatedTime`
        
        
        """
        ...
    def getCurrentTime(self) -> float:
        """
            Get the current grid point time.
        
            Returns:
                current grid point time
        
        
        """
        ...
    def getInterpolatedDerivatives(self) -> typing.MutableSequence[float]:
        """
            Get the derivatives of the state vector of the interpolated point.
        
            The returned vector is a reference to a reused array, so it should not be modified and it should be copied if it needs
            to be preserved across several calls.
        
            Returns:
                derivatives of the state vector at time
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedTime`
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
        
            Since:
                2.0
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedState`
        
        
        """
        ...
    def getInterpolatedSecondaryDerivatives(self, int: int) -> typing.MutableSequence[float]:
        """
            Get the interpolated secondary derivatives corresponding to the secondary equations.
        
            The returned vector is a reference to a reused array, so it should not be modified and it should be copied if it needs
            to be preserved across several calls.
        
            Parameters:
                index (int): index of the secondary set, as returned by ExpandableStatefulODE.addSecondaryEquations()
        
            Returns:
                interpolated secondary derivatives at the current interpolation date
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
        
            Since:
                3.0
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedState`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedDerivatives`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedSecondaryState`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.setInterpolatedTime`
        
        
        """
        ...
    def getInterpolatedSecondaryState(self, int: int) -> typing.MutableSequence[float]:
        """
            Get the interpolated secondary state corresponding to the secondary equations.
        
            The returned vector is a reference to a reused array, so it should not be modified and it should be copied if it needs
            to be preserved across several calls.
        
            Parameters:
                index (int): index of the secondary set, as returned by ExpandableStatefulODE.addSecondaryEquations()
        
            Returns:
                interpolated secondary state at the current interpolation date
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
        
            Since:
                3.0
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedState`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedDerivatives`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedSecondaryDerivatives`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.setInterpolatedTime`
        
        
        """
        ...
    def getInterpolatedState(self) -> typing.MutableSequence[float]:
        """
            Get the state vector of the interpolated point.
        
            The returned vector is a reference to a reused array, so it should not be modified and it should be copied if it needs
            to be preserved across several calls.
        
            Returns:
                state vector at time :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedTime`
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedDerivatives`
        
        
        """
        ...
    def getInterpolatedTime(self) -> float:
        """
            Get the time of the interpolated point. If
            :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.setInterpolatedTime` has not been called, it returns
            the current grid point time.
        
            Returns:
                interpolation point time
        
        
        """
        ...
    def getPreviousTime(self) -> float:
        """
            Get the previous grid point time.
        
            Returns:
                previous grid point time
        
        
        """
        ...
    def isForward(self) -> bool:
        """
            Check if the natural integration direction is forward.
        
            This method provides the integration direction as specified by the integrator itself, it avoid some nasty problems in
            degenerated cases like null steps due to cancellation at step initialization, step control or discrete events
            triggering.
        
            Returns:
                true if the integration variable (time) increases during integration
        
        
        """
        ...
    def setInterpolatedTime(self, double: float) -> None:
        """
            Set the time of the interpolated point.
        
            Setting the time outside of the current step is now allowed, but should be used with care since the accuracy of the
            interpolator will probably be very poor far from this step. This allowance has been added to simplify implementation of
            search algorithms near the step endpoints.
        
            Setting the time changes the instance internal state. If a specific state must be preserved, a copy of the instance must
            be created using :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.copy`.
        
            Parameters:
                time (double): time of the interpolated point
        
        
        """
        ...

class StepNormalizerBounds(java.lang.Enum['StepNormalizerBounds']):
    """
    public enum StepNormalizerBounds extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizerBounds`>
    
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer` bounds settings. They influence whether the underlying
        fixed step size step handler is called for the first and last points. Note that if the last point coincides with a
        normalized point, then the underlying fixed step size step handler is always called, regardless of these settings.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizerMode`
    """
    NEITHER: typing.ClassVar['StepNormalizerBounds'] = ...
    FIRST: typing.ClassVar['StepNormalizerBounds'] = ...
    LAST: typing.ClassVar['StepNormalizerBounds'] = ...
    BOTH: typing.ClassVar['StepNormalizerBounds'] = ...
    def firstIncluded(self) -> bool:
        """
            Returns a value indicating whether the first point should be passed to the underlying fixed step size step handler.
        
            Returns:
                value indicating whether the first point should be passed to the underlying fixed step size step handler.
        
        
        """
        ...
    def lastIncluded(self) -> bool:
        """
            Returns a value indicating whether the last point should be passed to the underlying fixed step size step handler.
        
            Returns:
                value indicating whether the last point should be passed to the underlying fixed step size step handler.
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'StepNormalizerBounds':
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
    def values() -> typing.MutableSequence['StepNormalizerBounds']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (StepNormalizerBounds c : StepNormalizerBounds.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class StepNormalizerMode(java.lang.Enum['StepNormalizerMode']):
    """
    public enum StepNormalizerMode extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizerMode`>
    
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer` modes. Determines how the step size is interpreted.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizerBounds`
    """
    INCREMENT: typing.ClassVar['StepNormalizerMode'] = ...
    MULTIPLES: typing.ClassVar['StepNormalizerMode'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'StepNormalizerMode':
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
    def values() -> typing.MutableSequence['StepNormalizerMode']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (StepNormalizerMode c : StepNormalizerMode.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class AbstractStepInterpolator(StepInterpolator):
    """
    public abstract class AbstractStepInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
    
        This abstract class represents an interpolator over the last step during an ODE integration.
    
        The various ODE integrators provide objects extending this class to the step handlers. The handlers can use these
        objects to retrieve the state vector at intermediate times between the previous and the current grid points (dense
        output).
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.SecondOrderIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`, :meth:`~serialized`
    """
    def copy(self) -> StepInterpolator:
        """
            Copy the instance.
        
            The copied instance is guaranteed to be independent from the original one. Both can be used with different settings for
            interpolated time without any side effect.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
        
            Returns:
                a deep copy of the instance, which can be used independently.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.setInterpolatedTime`
        
        
        """
        ...
    def finalizeStep(self) -> None:
        """
            Finalize the step.
        
            Some embedded Runge-Kutta integrators need fewer functions evaluations than their counterpart step interpolators. These
            interpolators should perform the last evaluations they need by themselves only if they need them. This method triggers
            these extra evaluations. It can be called directly by the user step handler and it is called automatically if
            :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.AbstractStepInterpolator.setInterpolatedTime` is called.
        
            Once this method has been called, **no** other evaluation will be performed on this step. If there is a need to have
            some side effects between the step handler and the differential equations (for example update some data in the equations
            once the step has been done), it is advised to call this method explicitly from the step handler before these side
            effects are set up. If the step handler induces no side effect, then this method can safely be ignored, it will be
            called transparently as needed.
        
            **Warning**: since the step interpolator provided to the step handler as a parameter of the
            :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler.handleStep` is valid only for the duration of the
            :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler.handleStep` call, one cannot simply store a reference and
            reuse it later. One should first finalize the instance, then copy this finalized instance into a new object that can be
            kept.
        
            This method calls the protected :code:`doFinalize` method if it has never been called during this step and set a flag
            indicating that it has been called once. It is the :code:`doFinalize` method which should perform the evaluations. This
            wrapping prevents from calling :code:`doFinalize` several times and hence evaluating the differential equations too
            often. Therefore, subclasses are not allowed not reimplement it, they should rather reimplement :code:`doFinalize`.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
        
        
        """
        ...
    def getCurrentTime(self) -> float:
        """
            Get the current soft grid point time.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getCurrentTime` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
        
            Returns:
                current soft grid point time
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.AbstractStepInterpolator.setSoftCurrentTime`
        
        
        """
        ...
    def getGlobalCurrentTime(self) -> float:
        """
            Get the current global grid point time.
        
            Returns:
                current global grid point time
        
        
        """
        ...
    def getGlobalPreviousTime(self) -> float:
        """
            Get the previous global grid point time.
        
            Returns:
                previous global grid point time
        
        
        """
        ...
    def getInterpolatedDerivatives(self) -> typing.MutableSequence[float]:
        """
            Get the derivatives of the state vector of the interpolated point.
        
            The returned vector is a reference to a reused array, so it should not be modified and it should be copied if it needs
            to be preserved across several calls.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedDerivatives` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
        
            Returns:
                derivatives of the state vector at time
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedTime`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedState`
        
        
        """
        ...
    def getInterpolatedSecondaryDerivatives(self, int: int) -> typing.MutableSequence[float]:
        """
            Get the interpolated secondary derivatives corresponding to the secondary equations.
        
            The returned vector is a reference to a reused array, so it should not be modified and it should be copied if it needs
            to be preserved across several calls.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedSecondaryDerivatives` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
        
            Parameters:
                index (int): index of the secondary set, as returned by ExpandableStatefulODE.addSecondaryEquations()
        
            Returns:
                interpolated secondary derivatives at the current interpolation date
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedState`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedDerivatives`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedSecondaryState`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.setInterpolatedTime`
        
        
        """
        ...
    def getInterpolatedSecondaryState(self, int: int) -> typing.MutableSequence[float]:
        """
            Get the interpolated secondary state corresponding to the secondary equations.
        
            The returned vector is a reference to a reused array, so it should not be modified and it should be copied if it needs
            to be preserved across several calls.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedSecondaryState` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
        
            Parameters:
                index (int): index of the secondary set, as returned by ExpandableStatefulODE.addSecondaryEquations()
        
            Returns:
                interpolated secondary state at the current interpolation date
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedState`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedDerivatives`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedSecondaryDerivatives`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.setInterpolatedTime`
        
        
        """
        ...
    def getInterpolatedState(self) -> typing.MutableSequence[float]:
        """
            Get the state vector of the interpolated point.
        
            The returned vector is a reference to a reused array, so it should not be modified and it should be copied if it needs
            to be preserved across several calls.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedState` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
        
            Returns:
                state vector at time :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedTime`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedDerivatives`
        
        
        """
        ...
    def getInterpolatedTime(self) -> float:
        """
            Get the time of the interpolated point. If
            :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.setInterpolatedTime` has not been called, it returns
            the current grid point time.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getInterpolatedTime` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
        
            Returns:
                interpolation point time
        
        
        """
        ...
    def getPreviousTime(self) -> float:
        """
            Get the previous soft grid point time.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.getPreviousTime` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
        
            Returns:
                previous soft grid point time
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.AbstractStepInterpolator.setSoftPreviousTime`
        
        
        """
        ...
    def isForward(self) -> bool:
        """
            Check if the natural integration direction is forward.
        
            This method provides the integration direction as specified by the integrator itself, it avoid some nasty problems in
            degenerated cases like null steps due to cancellation at step initialization, step control or discrete events
            triggering.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.isForward` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
        
            Returns:
                true if the integration variable (time) increases during integration
        
        
        """
        ...
    def readExternal(self, objectInput: java.io.ObjectInput) -> None: ...
    def reinitialize(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], boolean: bool, equationsMapper: fr.cnes.sirius.patrius.math.ode.EquationsMapper, equationsMapperArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.ode.EquationsMapper], jpype.JArray]) -> None:
        """
            Reinitialize the instance
        
            Parameters:
                y (double[]): reference to the integrator array holding the state at the end of the step
                isForward (boolean): integration direction indicator
                primary (:class:`~fr.cnes.sirius.patrius.math.ode.EquationsMapper`): equations mapper for the primary equations set
                secondary (:class:`~fr.cnes.sirius.patrius.math.ode.EquationsMapper`[]): equations mappers for the secondary equations sets
        
        
        """
        ...
    def setInterpolatedTime(self, double: float) -> None:
        """
            Set the time of the interpolated point.
        
            Setting the time outside of the current step is now allowed, but should be used with care since the accuracy of the
            interpolator will probably be very poor far from this step. This allowance has been added to simplify implementation of
            search algorithms near the step endpoints.
        
            Setting the time changes the instance internal state. If a specific state must be preserved, a copy of the instance must
            be created using :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.copy`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator.setInterpolatedTime` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`
        
            Parameters:
                time (double): time of the interpolated point
        
        
        """
        ...
    def setSoftCurrentTime(self, double: float) -> None:
        """
            Restrict step range to a limited part of the global step.
        
            This method can be used to restrict a step and make it appear as if the original step was smaller. Calling this method
            *only* changes the value returned by
            :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.AbstractStepInterpolator.getCurrentTime`, it does not change any other
            property
        
            Parameters:
                softCurrentTimeIn (double): end of the restricted step
        
            Since:
                2.2
        
        
        """
        ...
    def setSoftPreviousTime(self, double: float) -> None:
        """
            Restrict step range to a limited part of the global step.
        
            This method can be used to restrict a step and make it appear as if the original step was smaller. Calling this method
            *only* changes the value returned by
            :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.AbstractStepInterpolator.getPreviousTime`, it does not change any other
            property
        
            Parameters:
                softPreviousTimeIn (double): start of the restricted step
        
            Since:
                2.2
        
        
        """
        ...
    def shift(self) -> None:
        """
            Shift one step forward. Copy the current time into the previous time, hence preparing the interpolator for future calls
            to :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.AbstractStepInterpolator.storeTime`
        
        """
        ...
    def storeTime(self, double: float) -> None:
        """
            Store the current step time.
        
            Parameters:
                t (double): current time
        
        
        """
        ...
    def writeExternal(self, objectOutput: java.io.ObjectOutput) -> None: ...

class DummyStepHandler(StepHandler):
    """
    public final class DummyStepHandler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`
    
        This class is a step handler that does nothing.
    
        This class is provided as a convenience for users who are only interested in the final state of an integration and not
        in the intermediate steps. Its handleStep method does nothing.
    
        Since this class has no internal state, it is implemented using the Singleton design pattern. This means that only one
        instance is ever created, which can be retrieved using the getInstance method. This explains why there is no public
        constructor.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`
    """
    @staticmethod
    def getInstance() -> 'DummyStepHandler':
        """
            Get the only instance.
        
            Returns:
                the only instance
        
        
        """
        ...
    def handleStep(self, stepInterpolator: StepInterpolator, boolean: bool) -> None:
        """
            Handle the last accepted step. This method does nothing in this class.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler.handleStep` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`
        
            Parameters:
                interpolator (:class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`): interpolator for the last accepted step. For efficiency purposes, the various integrators reuse the same object on each
                    call, so if the instance wants to keep it across all calls (for example to provide at the end of the integration a
                    continuous model valid throughout the integration range), it should build a local copy using the clone method and store
                    this copy.
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

class StepNormalizer(StepHandler):
    """
    public class StepNormalizer extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`
    
        This class wraps an object implementing :class:`~fr.cnes.sirius.patrius.math.ode.sampling.FixedStepHandler` into a
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`.
    
        This wrapper allows to use fixed step handlers with general integrators which cannot guaranty their integration steps
        will remain constant and therefore only accept general step handlers.
    
        The stepsize used is selected at construction time. The null method of the underlying
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.FixedStepHandler` object is called at normalized times. The normalized
        times can be influenced by the :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizerMode` and
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizerBounds`.
    
        There is no constraint on the integrator, it can use any time step it needs (time steps longer or shorter than the fixed
        time step and non-integer ratios are all allowed).
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.FixedStepHandler`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizerMode`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizerBounds`
    """
    @typing.overload
    def __init__(self, double: float, fixedStepHandler: FixedStepHandler): ...
    @typing.overload
    def __init__(self, double: float, fixedStepHandler: FixedStepHandler, stepNormalizerBounds: StepNormalizerBounds): ...
    @typing.overload
    def __init__(self, double: float, fixedStepHandler: FixedStepHandler, stepNormalizerMode: StepNormalizerMode): ...
    @typing.overload
    def __init__(self, double: float, fixedStepHandler: FixedStepHandler, stepNormalizerMode: StepNormalizerMode, stepNormalizerBounds: StepNormalizerBounds): ...
    def handleStep(self, stepInterpolator: StepInterpolator, boolean: bool) -> None:
        """
            Handle the last accepted step
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler.handleStep` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`
        
            Parameters:
                interpolator (:class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`): interpolator for the last accepted step. For efficiency purposes, the various integrators reuse the same object on each
                    call, so if the instance wants to keep it across all calls (for example to provide at the end of the integration a
                    continuous model valid throughout the integration range), it should build a local copy using the clone method and store
                    this copy.
                isLast (boolean): true if the step is the last one
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the interpolator throws one because the number of functions evaluations is exceeded
        
        
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

class NordsieckStepInterpolator(AbstractStepInterpolator):
    """
    public class NordsieckStepInterpolator extends :class:`~fr.cnes.sirius.patrius.math.ode.sampling.AbstractStepInterpolator`
    
        This class implements an interpolator for integrators using Nordsieck representation.
    
        This interpolator computes dense output around the current point. The interpolation equation is based on Taylor series
        formulas.
    
        Since:
            2.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsBashforthIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsMoultonIntegrator`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, nordsieckStepInterpolator: 'NordsieckStepInterpolator'): ...
    def getInterpolatedStateVariation(self) -> typing.MutableSequence[float]:
        """
            Get the state vector variation from current to interpolated state.
        
            This method is aimed at computing y(t :sub:`interpolation` ) -y(t :sub:`current` ) accurately by avoiding the
            cancellation errors that would occur if the subtraction were performed explicitly.
        
            The returned vector is a reference to a reused array, so it should not be modified and it should be copied if it needs
            to be preserved across several calls.
        
            Returns:
                state vector at time :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.AbstractStepInterpolator.getInterpolatedTime`
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.AbstractStepInterpolator.getInterpolatedDerivatives`
        
        
        """
        ...
    def readExternal(self, objectInput: java.io.ObjectInput) -> None: ...
    @typing.overload
    def reinitialize(self, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], array2DRowRealMatrix: fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix) -> None:
        """
            Reinitialize the instance.
        
            Beware that all arrays *must* be references to integrator arrays, in order to ensure proper update without copy.
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.ode.sampling.AbstractStepInterpolator`
        
            Parameters:
                y (double[]): reference to the integrator array holding the state at the end of the step
                forward (boolean): integration direction indicator
                primaryMapper (:class:`~fr.cnes.sirius.patrius.math.ode.EquationsMapper`): equations mapper for the primary equations set
                secondaryMappers (:class:`~fr.cnes.sirius.patrius.math.ode.EquationsMapper`[]): equations mappers for the secondary equations sets
        
            Reinitialize the instance.
        
            Beware that all arrays *must* be references to integrator arrays, in order to ensure proper update without copy.
        
            Parameters:
                time (double): time at which all arrays are defined
                stepSize (double): step size used in the scaled and nordsieck arrays
                scaledDerivative (double[]): reference to the integrator array holding the first scaled derivative
                nordsieckVector (:class:`~fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix`): reference to the integrator matrix holding the nordsieck vector
        
        
        """
        ...
    @typing.overload
    def reinitialize(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], boolean: bool, equationsMapper: fr.cnes.sirius.patrius.math.ode.EquationsMapper, equationsMapperArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.ode.EquationsMapper], jpype.JArray]) -> None: ...
    def rescale(self, double: float) -> None:
        """
            Rescale the instance.
        
            Since the scaled and Nordiseck arrays are shared with the caller, this method has the side effect of rescaling this
            arrays in the caller too.
        
            Parameters:
                stepSize (double): new step size to use in the scaled and nordsieck arrays
        
        
        """
        ...
    def writeExternal(self, objectOutput: java.io.ObjectOutput) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.ode.sampling")``.

    AbstractStepInterpolator: typing.Type[AbstractStepInterpolator]
    DummyStepHandler: typing.Type[DummyStepHandler]
    FixedStepHandler: typing.Type[FixedStepHandler]
    NordsieckStepInterpolator: typing.Type[NordsieckStepInterpolator]
    StepHandler: typing.Type[StepHandler]
    StepInterpolator: typing.Type[StepInterpolator]
    StepNormalizer: typing.Type[StepNormalizer]
    StepNormalizerBounds: typing.Type[StepNormalizerBounds]
    StepNormalizerMode: typing.Type[StepNormalizerMode]
