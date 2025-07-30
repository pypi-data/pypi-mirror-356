
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.ode
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.propagation.precomputed.multi
import fr.cnes.sirius.patrius.time
import fr.cnes.sirius.patrius.time.interpolation
import fr.cnes.sirius.patrius.utils
import java.util
import typing



class Ephemeris(fr.cnes.sirius.patrius.propagation.AbstractPropagator, fr.cnes.sirius.patrius.propagation.BoundedPropagator):
    """
    public class Ephemeris extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator` implements :class:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator`
    
        This class is designed to accept and handle tabulated orbital entries. Tabulated entries are classified and then
        extrapolated in way to obtain continuous output, with accuracy and computation methods configured by the user.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.propagation.SpacecraftState], int: int): ...
    def basicPropagate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def basicPropagateOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def getInitialState(self) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
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
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getSpacecraftState(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def resetInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...

class IntegratedEphemeris(fr.cnes.sirius.patrius.propagation.AbstractPropagator, fr.cnes.sirius.patrius.propagation.BoundedPropagator):
    """
    public class IntegratedEphemeris extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator` implements :class:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator`
    
        This class stores sequentially generated orbital parameters for later retrieval.
    
        Instances of this class are built and then must be fed with the results provided by
        :class:`~fr.cnes.sirius.patrius.propagation.Propagator` objects configured in
        :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.setEphemerisMode`. Once propagation is o, random access to any
        intermediate state of the orbit throughout the propagation range is possible.
    
        A typical use case is for numerically integrated orbits, which can be used by algorithms that need to wander around
        according to their own algorithm without cumbersome tight links with the integrator.
    
        Another use case is for persistence, as this class is serializable.
    
        As this class implements the :class:`~fr.cnes.sirius.patrius.propagation.Propagator` interface, it can itself be used in
        batch mode to build another instance of the same type. This is however not recommended since it would be a waste of
        resources.
    
        Note that this class stores all intermediate states along with interpolation models, so it may be memory intensive.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], list2: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], list3: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo]], list4: java.util.List[fr.cnes.sirius.patrius.math.ode.ContinuousOutputModel], frame: fr.cnes.sirius.patrius.frames.Frame, double: float): ...
    @typing.overload
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], list2: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], list3: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo], typing.Mapping[str, fr.cnes.sirius.patrius.propagation.numerical.AdditionalStateInfo]], list4: java.util.List[fr.cnes.sirius.patrius.math.ode.ContinuousOutputModel], frame: fr.cnes.sirius.patrius.frames.Frame, double: float): ...
    def getInitialState(self) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
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
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getSpacecraftState(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def manageStateFrame(self) -> None: ...
    def resetInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...

class PVEphemeris(fr.cnes.sirius.patrius.propagation.AbstractPropagator, fr.cnes.sirius.patrius.propagation.BoundedPropagator):
    """
    public class PVEphemeris extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator` implements :class:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator`
    
        This class is designed to accept and handle tabulated orbital entries described by
        :class:`~fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates`.
    
    
        Tabulated entries are classified and then extrapolated in a way to obtain continuous output, with accuracy and
        computation methods configured by the user.
    
        Note: This implementation does not support all the methods of the
        :class:`~fr.cnes.sirius.patrius.propagation.Propagator` interface in the case the provided frame is not pseudo-inertial.
        In particular, the propagate methods.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates], int: int, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, cartesianDerivativesFilter: fr.cnes.sirius.patrius.utils.CartesianDerivativesFilter): ...
    @typing.overload
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates], int: int, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, cartesianDerivativesFilter: fr.cnes.sirius.patrius.utils.CartesianDerivativesFilter, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider): ...
    @typing.overload
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates], int: int, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, cartesianDerivativesFilter: fr.cnes.sirius.patrius.utils.CartesianDerivativesFilter, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, boolean: bool): ...
    @typing.overload
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates], int: int, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, cartesianDerivativesFilter: fr.cnes.sirius.patrius.utils.CartesianDerivativesFilter, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, boolean: bool, int2: int): ...
    @typing.overload
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates], int: int, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, cartesianDerivativesFilter: fr.cnes.sirius.patrius.utils.CartesianDerivativesFilter, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, boolean: bool, int2: int, boolean2: bool): ...
    def getCacheReusabilityRatio(self) -> float:
        """
            Provides the ratio of reusability of the internal cache. This method can help to chose the size of the cache.
        
            Returns:
                the reusability ratio (0 means no reusability at all, 0.5 means that the supplier is called only half time compared to
                computeIf method)
        
        
        """
        ...
    def getFirstTimeStampedPVCoordinates(self) -> fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates:
        """
            Getter for the first time-stamped PVCoordinates.
        
            Returns:
                the first time-stamped PVCoordinates
        
        
        """
        ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Getter for the frame in which the time-stamped PVCoordinates are defined.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getFrame` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator.getFrame` in
                class :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`
        
            Returns:
                frame in which the time-stamped PVCoordinates are defined.
        
        
        """
        ...
    def getInitialState(self) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def getLastTimeStampedPVCoordinates(self) -> fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates:
        """
            Getter for the last time-stamped PVCoordinates.
        
            Returns:
                the last time-stamped PVCoordinates
        
        
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
    def getMaxOptimalDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
        
            Returns:
                The last optimal date.
        
        
        """
        ...
    def getMaxSampleDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
        
            Returns:
                The last sample date.
        
        
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
    def getMinOptimalDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
        
            Returns:
                The first optimal date.
        
        
        """
        ...
    def getMinSampleDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
        
            Returns:
                The first sample date.
        
        
        """
        ...
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Getter for the frame in which the time-stamped PVCoordinates are defined.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider.getNativeFrame` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getNativeFrame` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                frame in which the time-stamped PVCoordinates are defined.
        
        
        """
        ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getSearchMethod(self) -> fr.cnes.sirius.patrius.time.interpolation.TimeStampedInterpolableEphemeris.SearchMethod:
        """
            Getter for the search method.
        
            Returns:
                the search method
        
        
        """
        ...
    def getSpacecraftState(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def getTimeStampedPVCoordinates(self, boolean: bool) -> typing.MutableSequence[fr.cnes.sirius.patrius.utils.TimeStampedPVCoordinates]:
        """
            Getter for the time-stamped PVCoordinates array.
        
            Parameters:
                copy (boolean): if :code:`true` return a copy of the time-stamped PVCoordinates array, otherwise return the stored array
        
            Returns:
                the time-stamped PVCoordinates array
        
        
        """
        ...
    def getTimeStampedPVCoordinatesSize(self) -> int:
        """
            Getter for the time-stamped PVCoordinates size.
        
            Returns:
                the time-stamped PVCoordinates size
        
        
        """
        ...
    def isAcceptOutOfOptimalRange(self) -> bool:
        """
            Indicates whether accept dates outside of the optimal interval which is a sub-interval from the full interval interval
            required for interpolation with respect to the interpolation order.
        
            Returns:
                :code:`true` if the dates outside of the optimal interval are accepted, :code:`false` otherwise
        
        
        """
        ...
    def propagateOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit:
        """
            Extrapolate an orbit up to a specific target date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator.propagateOrbit` in
                class :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): target date for the orbit
        
            Returns:
                extrapolated parameters
        
            Raises:
                : if the date is outside the supported interval if the instance has been built with the setting
                    :code:`acceptOutOfOptimalRange = false` and the date is outside the optimal interval which is a sub-interval from the
                    full interval interval required for interpolation with respect to the interpolation order
        
        
        """
        ...
    def resetInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    def setOrbitFrame(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> None:
        """
            Set propagation frame.
        
            This feature isn't supported by this implementation as the frame in which the time-stamped PVCoordinates are defined is
            set in the constructor and this frame is used to propagate the time-stamped PVCoordinates.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator.setOrbitFrame` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator.setOrbitFrame` in
                class :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`
        
            Parameters:
                frameIn (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the frame to use
        
            Raises:
                : always thrown by this implementation
        
        
        """
        ...
    def setSearchMethod(self, searchMethod: fr.cnes.sirius.patrius.time.interpolation.TimeStampedInterpolableEphemeris.SearchMethod) -> None:
        """
            Setter for the search method.
        
            Parameters:
                searchMethod (:class:`~fr.cnes.sirius.patrius.time.interpolation.TimeStampedInterpolableEphemeris.SearchMethod`): the search method to set
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if :code:`searchMethod` is null
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation.precomputed")``.

    Ephemeris: typing.Type[Ephemeris]
    IntegratedEphemeris: typing.Type[IntegratedEphemeris]
    PVEphemeris: typing.Type[PVEphemeris]
    multi: fr.cnes.sirius.patrius.propagation.precomputed.multi.__module_protocol__
