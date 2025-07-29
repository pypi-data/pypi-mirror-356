
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.stela.forces
import fr.cnes.sirius.patrius.stela.orbits
import fr.cnes.sirius.patrius.time
import typing



class NonInertialContribution(fr.cnes.sirius.patrius.stela.forces.AbstractStelaGaussContribution):
    """
    public class NonInertialContribution extends :class:`~fr.cnes.sirius.patrius.stela.forces.AbstractStelaGaussContribution`
    
        Class representing the non-inertial contribution for STELA propagator.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    def computeOmega(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, frame2: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeOmegaDerivative(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, frame2: fr.cnes.sirius.patrius.frames.Frame, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...
    def computeShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.forces.noninertial")``.

    NonInertialContribution: typing.Type[NonInertialContribution]
