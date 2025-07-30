
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.forces.gravity.potential
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.stela.forces
import fr.cnes.sirius.patrius.stela.forces.gravity.recurrence
import fr.cnes.sirius.patrius.stela.orbits
import java.io
import java.util
import typing



class AbstractStelaZonalAttraction(fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution):
    """
    public abstract class AbstractStelaZonalAttraction extends :class:`~fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution`
    
        This abstract class represents the zonal harmonics.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, int: int, boolean: bool): ...
    def computeJ2Square(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def getZonalDegreeMaxPerturbation(self) -> int:
        """
            Getter for the degree of development for zonal perturbations.
        
            Returns:
                the degree of development for zonal perturbations
        
        
        """
        ...
    def isJ2SquareComputed(self) -> bool:
        """
            Indicate if J2 should be computed or not.
        
            Returns:
                :code:`true` if J2² is computed, :code:`false` otherwise
        
        
        """
        ...

class SolidTidesAcc(fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution):
    """
    public class SolidTidesAcc extends :class:`~fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution`
    
    
        Class representing the tidal contribution.
    
        Since:
            3.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, boolean: bool, boolean2: bool, celestialPoint: fr.cnes.sirius.patrius.bodies.CelestialPoint, celestialPoint2: fr.cnes.sirius.patrius.bodies.CelestialPoint): ...
    @typing.overload
    def __init__(self, celestialPoint: fr.cnes.sirius.patrius.bodies.CelestialPoint, celestialPoint2: fr.cnes.sirius.patrius.bodies.CelestialPoint): ...
    def computePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...
    def getMoon(self) -> fr.cnes.sirius.patrius.bodies.CelestialPoint:
        """
            Get the Moon.
        
            Returns:
                Moon
        
        
        """
        ...
    def getSun(self) -> fr.cnes.sirius.patrius.bodies.CelestialPoint:
        """
            Get the Sun.
        
            Returns:
                Sun
        
        
        """
        ...

class StelaTesseralAttraction(fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution):
    """
    public final class StelaTesseralAttraction extends :class:`~fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution`
    
        This class represent the tesseral perturbations
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, potentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.potential.PotentialCoefficientsProvider): ...
    @typing.overload
    def __init__(self, potentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.potential.PotentialCoefficientsProvider, int: int, int2: int, double: float, int3: int): ...
    def computePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...
    def getQuadsList(self) -> java.util.List['TesseralQuad']: ...
    def updateQuads(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> None:
        """
            Compute quads (n, m, p, q).
        
            Parameters:
                orbit (:class:`~fr.cnes.sirius.patrius.orbits.Orbit`): orbit
        
        
        """
        ...

class StelaThirdBodyAttraction(fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution):
    """
    public class StelaThirdBodyAttraction extends :class:`~fr.cnes.sirius.patrius.stela.forces.AbstractStelaLagrangeContribution`
    
    
        Class computing third body attraction perturbations.
    
        It computes third body perturbations, short periods and partial derivatives depending on the degree of development
        asked.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, celestialPoint: fr.cnes.sirius.patrius.bodies.CelestialPoint, int: int, int2: int, int3: int): ...
    def computePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...

class TesseralQuad(java.io.Serializable):
    """
    public final class TesseralQuad extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Tesseral harmonics quad (n, m, p, q) and related data.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, potentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.potential.PotentialCoefficientsProvider, int: int, int2: int, int3: int, int4: int, orbit: fr.cnes.sirius.patrius.orbits.Orbit): ...
    def getCentralEccentricity(self) -> float:
        """
            Getter for the central eccentricity e :sub:`c` .
        
            Returns:
                the central eccentricity e :sub:`c`
        
        
        """
        ...
    def getDeltaEccentricity(self) -> float:
        """
            Getter for the delta eccentricity Δe.
        
            Returns:
                the delta eccentricity Δe
        
        
        """
        ...
    def getDiffTaylorCoeffs(self) -> typing.MutableSequence[float]:
        """
            Getter for the Taylor coefficients (up to the 2nd order) of the eccentricity function derivative G'(e).
        
            Returns:
                the Taylor coefficients (up to the 2nd order) of the eccentricity function derivative G'G(e)
        
        
        """
        ...
    def getFc(self) -> float:
        """
            Getter for f :sub:`c` .
        
            Returns:
                f :sub:`c`
        
        
        """
        ...
    def getFs(self) -> float:
        """
            Getter for f :sub:`s` .
        
            Returns:
                f :sub:`s`
        
        
        """
        ...
    def getM(self) -> int:
        """
            Getter for m coefficient.
        
            Returns:
                m coefficient
        
        
        """
        ...
    def getN(self) -> int:
        """
            Getter for n coefficient.
        
            Returns:
                n coefficient
        
        
        """
        ...
    def getP(self) -> int:
        """
            Getter for p coefficient.
        
            Returns:
                p coefficient
        
        
        """
        ...
    def getQ(self) -> int:
        """
            Getter for q coefficient.
        
            Returns:
                q coefficient
        
        
        """
        ...
    def getQuad(self) -> typing.MutableSequence[int]:
        """
            Getter for quads as an array.
        
            Returns:
                quad list as an array
        
        
        """
        ...
    def getTaylorCoeffs(self) -> typing.MutableSequence[float]:
        """
            Getter for the Taylor coefficients (up to the 2nd order) of the eccentricity function G(e).
        
            Returns:
                the Taylor coefficients (up to the 2nd order) of the eccentricity function G(e)
        
        
        """
        ...
    def updateEccentricityInterval(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> None:
        """
            Update eccentricity interval [e :sub:`c` - Δe; e :sub:`c` + Δe]. G(e) and G'(e) functions using taylor approximations
            are valid upon this interval.
        
            Parameters:
                orbit (:class:`~fr.cnes.sirius.patrius.orbits.Orbit`): the orbit
        
        
        """
        ...

class StelaZonalAttraction(AbstractStelaZonalAttraction):
    def __init__(self, potentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.potential.PotentialCoefficientsProvider, int: int, boolean: bool, int2: int, int3: int, boolean2: bool): ...
    def computeJ10(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ11(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ12(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ13(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ14(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ15(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    @typing.overload
    def computeJ2(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    @typing.overload
    def computeJ2(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, double: float) -> typing.MutableSequence[float]: ...
    def computeJ2PartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computeJ2ShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ2Square(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ2SquarePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @typing.overload
    def computeJ3(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    @typing.overload
    def computeJ3(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, double: float) -> typing.MutableSequence[float]: ...
    def computeJ3PartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computeJ4(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ4PartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computeJ5(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ5PartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computeJ6(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ6PartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computeJ7(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ7PartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computeJ8(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeJ9(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...
    def isJ2SquareComputed(self) -> bool: ...
    def isJ2SquareParDerComputed(self) -> bool: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.forces.gravity")``.

    AbstractStelaZonalAttraction: typing.Type[AbstractStelaZonalAttraction]
    SolidTidesAcc: typing.Type[SolidTidesAcc]
    StelaTesseralAttraction: typing.Type[StelaTesseralAttraction]
    StelaThirdBodyAttraction: typing.Type[StelaThirdBodyAttraction]
    StelaZonalAttraction: typing.Type[StelaZonalAttraction]
    TesseralQuad: typing.Type[TesseralQuad]
    recurrence: fr.cnes.sirius.patrius.stela.forces.gravity.recurrence.__module_protocol__
