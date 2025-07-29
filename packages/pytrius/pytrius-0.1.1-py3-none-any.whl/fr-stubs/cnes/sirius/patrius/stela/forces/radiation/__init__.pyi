
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.forces.radiation
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.stela.forces
import fr.cnes.sirius.patrius.stela.orbits
import typing



class SRPPotential(fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution):
    """
    public class SRPPotential extends :class:`~fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution`
    
    
        This class represents the PRS Lagrange contribution in the STELA propagator context.
    
        Note that short periods are not available with this model.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float, double2: float, double3: float): ...
    def computePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]:
        """
            Compute the short periodic variations for a given spacecraft state.
        
            Parameters:
                orbit (:class:`~fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit`): current orbit information: date, kinematics
                converter (:class:`~fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter`): converter necessary in some specific case (drag short periods computation)
        
            Returns:
                the short periodic variations of the current force
        
        
        """
        ...

class SRPSquaring(fr.cnes.sirius.patrius.stela.forces.AbstractStelaGaussContribution):
    DEFAULT_QUADRATURE_POINTS: typing.ClassVar[int] = ...
    @typing.overload
    def __init__(self, radiationSensitive: fr.cnes.sirius.patrius.forces.radiation.RadiationSensitive, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float): ...
    @typing.overload
    def __init__(self, radiationSensitive: fr.cnes.sirius.patrius.forces.radiation.RadiationSensitive, int: int, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float): ...
    @typing.overload
    def __init__(self, radiationSensitive: fr.cnes.sirius.patrius.forces.radiation.RadiationSensitive, int: int, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float, double2: float, double3: float): ...
    @typing.overload
    def __init__(self, radiationSensitive: fr.cnes.sirius.patrius.forces.radiation.RadiationSensitive, int: int, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double: float, double2: float, double3: float, int2: int): ...
    def computeAcceleration(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...
    def computeShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...

class StelaSRPSquaring(fr.cnes.sirius.patrius.stela.forces.AbstractStelaGaussContribution):
    """
    public class StelaSRPSquaring extends :class:`~fr.cnes.sirius.patrius.stela.forces.AbstractStelaGaussContribution`
    
        This class represents the Stela SRP model, which computes perturbations using the squaring method and the partial
        derivatives using the potential approximation.
    
        Short periods are computed only using squaring model.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.stela.forces.radiation.SRPSquaring`,
            :class:`~fr.cnes.sirius.patrius.stela.forces.radiation.SRPPotential`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, int: int, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, int: int, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double4: float, double5: float, double6: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, int: int, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, double4: float, double5: float, double6: float, int2: int): ...
    def computePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...
    def computePotentialPerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.forces.radiation")``.

    SRPPotential: typing.Type[SRPPotential]
    SRPSquaring: typing.Type[SRPSquaring]
    StelaSRPSquaring: typing.Type[StelaSRPSquaring]
