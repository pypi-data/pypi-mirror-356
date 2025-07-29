
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes.multi
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.ode.sampling
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical.multi
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



class MultiPatriusFixedStepHandler(java.io.Serializable):
    """
    public interface MultiPatriusFixedStepHandler extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        This interface is copied from :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusFixedStepHandler` and adapted
        to multi propagation.
    
        This interface represents a handler that should be called after each successful fixed step.
    
        This interface should be implemented by anyone who is interested in getting the solution of an ordinary differential
        equation at fixed time steps. Objects implementing this interface should be wrapped within an instance of
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer` that itself is used as the general
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler` by the integrator. The
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer` object is called according to the integrator internal
        algorithms and it calls objects implementing this interface as necessary at fixed time steps.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepNormalizer`
    """
    def handleStep(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], boolean: bool) -> None: ...
    def init(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class MultiPatriusStepHandler(java.io.Serializable):
    def handleStep(self, multiPatriusStepInterpolator: 'MultiPatriusStepInterpolator', boolean: bool) -> None: ...
    def init(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class MultiPatriusStepInterpolator:
    def getCurrentDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
    def getInterpolatedDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
    def getInterpolatedStates(self) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    def getPreviousDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
    def isForward(self) -> bool: ...
    def setInterpolatedDate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class MultiAdaptedStepHandler(MultiPatriusStepInterpolator, fr.cnes.sirius.patrius.math.ode.sampling.StepHandler, fr.cnes.sirius.patrius.propagation.numerical.multi.MultiModeHandler, java.io.Serializable):
    """
    public class MultiAdaptedStepHandler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator`, :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`, :class:`~fr.cnes.sirius.patrius.propagation.numerical.multi.MultiModeHandler`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        This class is copied from :class:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler` and adapted to multi
        propagation.
    
        Adapt an :class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepHandler` to commons-math
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler` interface.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, multiPatriusStepHandler: MultiPatriusStepHandler): ...
    def copy(self) -> 'MultiAdaptedStepHandler':
        """
        
            Copy this.
        
            Following attributes are deeply copied:
        
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.orbitType` (primitive data type)
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.angleType` (primitive data type)
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.activate` (primitive data type)
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.rawInterpolator`
        
        
            Following attributes reference is passed (no deep copy):
        
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.attitudeProvidersForces`
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.attitudeProvidersEvents`
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.stateInfo`
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.initializedReference`
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.initializedMus`
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.initializedFrames`
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.handler`
        
        
            Returns:
                copy of this
        
        
        """
        ...
    def getCurrentDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the current grid date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator.getCurrentDate` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator`
        
            Returns:
                current grid date
        
        
        """
        ...
    def getInterpolatedDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the interpolated date.
        
            If :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator.setInterpolatedDate` has not
            been called, the date returned is the same as
            :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator.getCurrentDate`.
        
            If :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.setInterpolatedDate` has not been
            called, the date returned is the same as
            :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiAdaptedStepHandler.getCurrentDate`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator.getInterpolatedDate` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator`
        
            Returns:
                interpolated date
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator.setInterpolatedDate`,
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator.getInterpolatedStates`
        
        
        """
        ...
    def getInterpolatedStates(self) -> java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    def getPreviousDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the previous grid date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator.getPreviousDate` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator`
        
            Returns:
                previous grid date
        
        
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
    def initialize(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], map2: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider], typing.Mapping[str, fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider]], multiStateVectorInfo: fr.cnes.sirius.patrius.propagation.numerical.multi.MultiStateVectorInfo, boolean: bool, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, map3: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.frames.Frame], typing.Mapping[str, fr.cnes.sirius.patrius.frames.Frame]], map4: typing.Union[java.util.Map[str, float], typing.Mapping[str, float]]) -> None: ...
    def isForward(self) -> bool:
        """
            Check is integration direction is forward in date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator.isForward` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.multi.MultiPatriusStepInterpolator`
        
            Returns:
                true if integration is forward in date
        
        
        """
        ...
    def setInterpolatedDate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
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

class MultiPatriusStepNormalizer(MultiPatriusStepHandler):
    def __init__(self, double: float, multiPatriusFixedStepHandler: MultiPatriusFixedStepHandler): ...
    def handleStep(self, multiPatriusStepInterpolator: MultiPatriusStepInterpolator, boolean: bool) -> None: ...
    def init(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.SpacecraftState]], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation.sampling.multi")``.

    MultiAdaptedStepHandler: typing.Type[MultiAdaptedStepHandler]
    MultiPatriusFixedStepHandler: typing.Type[MultiPatriusFixedStepHandler]
    MultiPatriusStepHandler: typing.Type[MultiPatriusStepHandler]
    MultiPatriusStepInterpolator: typing.Type[MultiPatriusStepInterpolator]
    MultiPatriusStepNormalizer: typing.Type[MultiPatriusStepNormalizer]
