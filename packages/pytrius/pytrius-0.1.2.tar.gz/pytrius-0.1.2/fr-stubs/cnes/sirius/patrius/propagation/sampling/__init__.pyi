
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.ode.sampling
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.propagation.sampling.multi
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



class PatriusFixedStepHandler(java.io.Serializable):
    """
    public interface PatriusFixedStepHandler extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface is a space-dynamics aware fixed size step handler.
    
        It mirrors the :code:`FixedStepHandler` interface from `commons-math <http://commons.apache.org/math/>` but provides a
        space-dynamics interface to the methods.
    """
    def handleStep(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool) -> None: ...
    def init(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class PatriusStepHandler(java.io.Serializable):
    """
    public interface PatriusStepHandler extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface is a space-dynamics aware step handler.
    
        It mirrors the :code:`StepHandler` interface from ` commons-math <http://commons.apache.org/math/>` but provides a
        space-dynamics interface to the methods.
    """
    def handleStep(self, patriusStepInterpolator: 'PatriusStepInterpolator', boolean: bool) -> None: ...
    def init(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class PatriusStepInterpolator(java.io.Serializable):
    """
    public interface PatriusStepInterpolator extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface is a space-dynamics aware step interpolator.
    
        It mirrors the :code:`StepInterpolator` interface from ` commons-math <http://commons.apache.org/math/>` but provides a
        space-dynamics interface to the methods.
    """
    def getCurrentDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the current grid date.
        
            Returns:
                current grid date
        
        
        """
        ...
    def getInterpolatedDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the interpolated date.
        
            If :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.setInterpolatedDate` has not been called,
            the date returned is the same as
            :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.getCurrentDate`.
        
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
        
            Returns:
                previous grid date
        
        
        """
        ...
    def isForward(self) -> bool:
        """
            Check is integration direction is forward in date.
        
            Returns:
                true if integration is forward in date
        
        
        """
        ...
    def setInterpolatedDate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class AdaptedStepHandler(PatriusStepInterpolator, fr.cnes.sirius.patrius.math.ode.sampling.StepHandler, fr.cnes.sirius.patrius.propagation.numerical.ModeHandler):
    """
    public class AdaptedStepHandler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator`, :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`, :class:`~fr.cnes.sirius.patrius.propagation.numerical.ModeHandler`
    
        Adapt an :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler` to commons-math
        :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler` interface.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, patriusStepHandler: PatriusStepHandler): ...
    def copy(self) -> 'AdaptedStepHandler':
        """
        
            Copy this.
        
            Following attributes are deeply copied:
        
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.orbitType` (primitive data type)
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.angleType` (primitive data type)
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.initializedMu` (primitive data type)
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.activate` (primitive data type)
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.rawInterpolator`
        
        
            Following attributes reference is passed (no deep copy):
        
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.attProviderForces`
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.attProviderEvents`
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.addStateInfos`
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.initializedReference`
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.initializedFrame`
              - :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.handler`
        
        
            Returns:
                copy of this
        
        
        """
        ...
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
    def getInterpolatedDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the interpolated date.
        
            If :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.setInterpolatedDate` has not been called, the
            date returned is the same as :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.getCurrentDate`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.getInterpolatedDate` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator`
        
            Returns:
                interpolated date
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.setInterpolatedDate`,
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.getInterpolatedState`
        
        
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
    def initialize(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo]], boolean: bool, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, double: float) -> None: ...
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
    def setInterpolatedDate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Set the interpolated date.
        
            It is possible to set the interpolation date outside of the current step range, but accuracy will decrease as date is
            farther.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator.setInterpolatedDate` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): interpolated date to set
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.getInterpolatedDate`,
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.AdaptedStepHandler.getInterpolatedState`
        
        
        """
        ...
    def setReference(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Define new reference date.
        
            To be called by :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator` only.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.numerical.ModeHandler.setReference` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.numerical.ModeHandler`
        
            Parameters:
                newReference (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): new reference date
        
        
        """
        ...

class BasicStepInterpolator(PatriusStepInterpolator):
    """
    public class BasicStepInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator`
    
        Implementation of the :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator` interface based on a
        :class:`~fr.cnes.sirius.patrius.propagation.Propagator`.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, propagator: fr.cnes.sirius.patrius.propagation.Propagator): ...
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
    def setInterpolatedDate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def shift(self) -> None:
        """
            Shift one step forward. Copy the current date into the previous date, hence preparing the interpolator for future calls
            to :meth:`~fr.cnes.sirius.patrius.propagation.sampling.BasicStepInterpolator.storeDate`
        
        """
        ...
    def storeDate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class PatriusStepHandlerMultiplexer(PatriusStepHandler):
    """
    public class PatriusStepHandlerMultiplexer extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler`
    
        This class gathers several :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler` instances into one.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def add(self, patriusStepHandler: PatriusStepHandler) -> None:
        """
            Add a step handler.
        
            Parameters:
                handler (:class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler`): step handler to add
        
        
        """
        ...
    def handleStep(self, patriusStepInterpolator: PatriusStepInterpolator, boolean: bool) -> None: ...
    def init(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class PatriusStepNormalizer(PatriusStepHandler):
    """
    public class PatriusStepNormalizer extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler`
    
        This class wraps an object implementing :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusFixedStepHandler`
        into a :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler`.
    
        It mirrors the :code:`StepNormalizer` interface from `commons-math <http://commons.apache.org/math/>` but provides a
        space-dynamics interface to the methods.
    
        Modified to take into account propagation direction (in time). Lines 111 to 115 Cf A-1031.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, patriusFixedStepHandler: PatriusFixedStepHandler): ...
    def handleStep(self, patriusStepInterpolator: PatriusStepInterpolator, boolean: bool) -> None: ...
    def init(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def requiresDenseOutput(self) -> bool:
        """
            Determines whether this handler needs dense output. This handler needs dense output in order to provide data at
            regularly spaced steps regardless of the steps the propagator uses, so this method always returns true.
        
            Returns:
                always true
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation.sampling")``.

    AdaptedStepHandler: typing.Type[AdaptedStepHandler]
    BasicStepInterpolator: typing.Type[BasicStepInterpolator]
    PatriusFixedStepHandler: typing.Type[PatriusFixedStepHandler]
    PatriusStepHandler: typing.Type[PatriusStepHandler]
    PatriusStepHandlerMultiplexer: typing.Type[PatriusStepHandlerMultiplexer]
    PatriusStepInterpolator: typing.Type[PatriusStepInterpolator]
    PatriusStepNormalizer: typing.Type[PatriusStepNormalizer]
    multi: fr.cnes.sirius.patrius.propagation.sampling.multi.__module_protocol__
