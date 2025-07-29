
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.forces.gravity.potential
import fr.cnes.sirius.patrius.stela.forces.gravity
import fr.cnes.sirius.patrius.stela.orbits
import java.io
import typing



class StelaRecurrenceZonalAttraction(fr.cnes.sirius.patrius.stela.forces.gravity.AbstractStelaZonalAttraction):
    """
    public class StelaRecurrenceZonalAttraction extends :class:`~fr.cnes.sirius.patrius.stela.forces.gravity.AbstractStelaZonalAttraction`
    
        Class representing the Earth zonal harmonics computed using recurrence methods.
    
        Computes Zonal perturbations, short periods and partial derivatives using recurrence methods depending on the degree of
        development asked.
    
        The class is adapted from STELA RecurrenceZonalAcc in
        fr.cnes.los.stela.elib.business.implementation.earthpotential.zonal.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, potentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.potential.PotentialCoefficientsProvider, int: int): ...
    @typing.overload
    def __init__(self, potentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.potential.PotentialCoefficientsProvider, int: int, boolean: bool, boolean2: bool): ...
    def buildStelaRecurrenceZonalEquation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> 'StelaRecurrenceZonalEquation':
        """
            Build the :class:`~fr.cnes.sirius.patrius.stela.forces.gravity.recurrence.StelaRecurrenceZonalEquation` object from this
            class initialized parameters.
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.stela.forces.gravity.recurrence.StelaRecurrenceZonalEquation` object
        
        
        """
        ...
    def computeJ2Square(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def computeShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]:
        """
            Compute the short periodic variations for a given spacecraft state.
        
            **Note: the short periods (forces switches and degrees) are not used for this force model (return 0 array).**
        
            Parameters:
                orbit (:class:`~fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit`): current orbit information: date, kinematics
                converter (:class:`~fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter`): converter necessary in some specific case (drag short periods computation)
        
            Returns:
                the short periodic variations of the current force
        
        
        """
        ...
    def derParUdeg22(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def isNormalizedLegendrePolynomials(self) -> bool:
        """
            Indicate if the zonal perturbation are normalized Legendre Polynomials or not.
        
            Returns:
                :code:`true` if the zonal perturbation are normalized Legendre Polynomials, :code:`false` otherwise
        
        
        """
        ...
    def nDegZonalPartialDerivatives(self, stelaRecurrenceZonalEquation: 'StelaRecurrenceZonalEquation', int: int) -> typing.MutableSequence[float]:
        """
            Compute Jn zonal term (n: order of potential development).
        
            Parameters:
                zonalEq (:class:`~fr.cnes.sirius.patrius.stela.forces.gravity.recurrence.StelaRecurrenceZonalEquation`): zonal terms
                n (int): order
        
            Returns:
                Jn zonal term
        
        
        """
        ...

class StelaRecurrenceZonalEquation(java.io.Serializable):
    """
    public class StelaRecurrenceZonalEquation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class carries the Earth zonal harmonics recurrence methods equations and is meant to be used by
        :class:`~fr.cnes.sirius.patrius.stela.forces.gravity.recurrence.StelaRecurrenceZonalAttraction`.
    
        The class is adapted from STELA RecurrenceZonalEq in
        fr.cnes.los.stela.elib.business.implementation.earthpotential.zonal.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    def computeEvenMeanPotential(self, int: int) -> float:
        """
            Compute the mean potential U at a given order of development (even case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (42).
        
            Parameters:
                np (int): n' (order of development)
        
            Returns:
                U (even case)
        
        
        """
        ...
    def computeEvenParDerA(self, int: int, double: float) -> float:
        """
            Compute the mean potential (at a given order of development) partial derivatives with respect to a (even case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (67).
        
            Parameters:
                np (int): n' (order of development)
                meanU (double): U (even)
        
            Returns:
                dU/da (even case)
        
        
        """
        ...
    def computeEvenParDerEx(self, int: int, double: float) -> float:
        """
            Compute the mean potential (at a given order of development) partial derivatives with respect to ex (even case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (7).
        
            Parameters:
                np (int): n' (order of development)
                meanU (double): U (even)
        
            Returns:
                dU/dex
        
        
        """
        ...
    def computeEvenParDerEy(self, int: int, double: float) -> float:
        """
            Compute the mean potential (at a given order of development) partial derivatives with respect to ey (even case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (74).
        
            Parameters:
                np (int): n' (order of development)
                meanU (double): U (even)
        
            Returns:
                dU/dey
        
        
        """
        ...
    def computeEvenParDerIx(self, int: int, double: float) -> float:
        """
            Compute the mean potential (at a given order of development) partial derivatives with respect to ix (even case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (77).
        
            Parameters:
                np (int): n' (order of development)
                meanU (double): U (even)
        
            Returns:
                dU/dix
        
        
        """
        ...
    def computeEvenParDerIy(self, int: int, double: float) -> float:
        """
            Compute the mean potential (at a given order of development) partial derivatives with respect to iy (even case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (78).
        
            Parameters:
                np (int): n' (order of development)
                meanU (double): U (even)
        
            Returns:
                dU/diy
        
        
        """
        ...
    def computeOddMeanPotential(self, int: int) -> float:
        """
            Compute the mean potential U at a given order of development (odd case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (46).
        
            Parameters:
                np (int): n' (order of development)
        
            Returns:
                U (odd case)
        
        
        """
        ...
    def computeOddParDerA(self, int: int, double: float) -> float:
        """
            Compute the mean potential (at a given order of development) partial derivatives with respect to a (odd case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (68).
        
            Parameters:
                np (int): n' (order of development)
                meanU (double): U (odd)
        
            Returns:
                dU/da (odd case)
        
        
        """
        ...
    def computeOddParDerEx(self, int: int, double: float) -> float:
        """
            Compute the mean potential (at a given order of development) partial derivatives with respect to ex (odd case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (75).
        
            Parameters:
                np (int): n' (order of development)
                meanU (double): U (odd)
        
            Returns:
                dU/dex (odd case)
        
        
        """
        ...
    def computeOddParDerEy(self, int: int, double: float) -> float:
        """
            Compute the mean potential (at a given order of development) partial derivatives with respect to ey (odd case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (76).
        
            Parameters:
                np (int): n' (order of development)
                meanU (double): U (odd)
        
            Returns:
                dU/dey (odd case)
        
        
        """
        ...
    def computeOddParDerIx(self, int: int, double: float) -> float:
        """
            Compute the mean potential (at a given order of development) partial derivatives with respect to ix (odd case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (79).
        
            Parameters:
                np (int): n' (order of development)
                meanU (double): U (odd)
        
            Returns:
                dU/dix (odd case)
        
        
        """
        ...
    def computeOddParDerIy(self, int: int, double: float) -> float:
        """
            Compute the mean potential (at a given order of development) partial derivatives with respect to iy (odd case).
        
        
            (FAST NT-zonaux-hautsdegres) Eq. (80).
        
            Parameters:
                np (int): n' (order of development)
                meanU (double): U (odd)
        
            Returns:
                dU/diy (odd case)
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.forces.gravity.recurrence")``.

    StelaRecurrenceZonalAttraction: typing.Type[StelaRecurrenceZonalAttraction]
    StelaRecurrenceZonalEquation: typing.Type[StelaRecurrenceZonalEquation]
