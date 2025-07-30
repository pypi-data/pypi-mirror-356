
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes.multi
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.ode
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical.multi
import fr.cnes.sirius.patrius.time
import java.util
import typing



class MultiIntegratedEphemeris(fr.cnes.sirius.patrius.propagation.AbstractPropagator, fr.cnes.sirius.patrius.propagation.BoundedPropagator):
    """
    public class MultiIntegratedEphemeris extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator` implements :class:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator`
    
    
        This interface is copied from IntegratedEphemeris and adapted to multi propagation.
    
        This class stores sequentially generated orbital parameters for later retrieval.
    
        Instances of this class are built and then must be fed with the results provided by
        :class:`~fr.cnes.sirius.patrius.propagation.MultiPropagator` objects configured in
        :meth:`~fr.cnes.sirius.patrius.propagation.MultiPropagator.setEphemerisMode`. Once propagation is over, random access to
        any intermediate state of the orbit throughout the propagation range is possible.
    
        A typical use case is for numerically integrated orbits, which can be used by algorithms that need to wander around
        according to their own algorithm without cumbersome tight links with the integrator.
    
        Another use case is for persistence, as this class is serializable.
    
        As this class implements the :class:`~fr.cnes.sirius.patrius.propagation.Propagator` interface, it can itself be used in
        batch mode to build another instance of the same type. This is however not recommended since it would be a waste of
        resources.
    
        Note that this class stores all intermediate states along with interpolation models, so it may be memory intensive.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], list2: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], list3: java.util.List[fr.cnes.sirius.patrius.time.AbsoluteDate], orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, multiAttitudeProvider: fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider, multiAttitudeProvider2: fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider, multiStateVectorInfo: fr.cnes.sirius.patrius.propagation.numerical.multi.MultiStateVectorInfo, list4: java.util.List[fr.cnes.sirius.patrius.math.ode.ContinuousOutputModel], frame: fr.cnes.sirius.patrius.frames.Frame, string: str): ...
    def getInitialState(self) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the last date of the range.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator.getMaxDate` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator`
        
            Returns:
                the last date of the range
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator.getMaxDate`
        
        
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
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.BoundedPropagator.getMinDate`
        
        
        """
        ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def resetInitialState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation.precomputed.multi")``.

    MultiIntegratedEphemeris: typing.Type[MultiIntegratedEphemeris]
