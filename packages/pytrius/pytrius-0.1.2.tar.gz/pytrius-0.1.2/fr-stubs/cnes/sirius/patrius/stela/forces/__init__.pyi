
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.stela.forces.atmospheres
import fr.cnes.sirius.patrius.stela.forces.drag
import fr.cnes.sirius.patrius.stela.forces.gravity
import fr.cnes.sirius.patrius.stela.forces.noninertial
import fr.cnes.sirius.patrius.stela.forces.radiation
import fr.cnes.sirius.patrius.stela.forces.solaractivity
import fr.cnes.sirius.patrius.stela.orbits
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



class Squaring:
    """
    public final class Squaring extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class containing methods used to compute Simpson's quadrature.
    
        Since:
            1.3
    """
    def __init__(self): ...
    def computeSquaringPoints(self, int: int, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, double: float, double2: float) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @staticmethod
    def computeSquaringPointsEccentric(int: int, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit]: ...
    @staticmethod
    def computeSquaringPointsEccentric2(int: int, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, double: float, double2: float) -> java.util.List[typing.MutableSequence[float]]: ...
    def getSquaringJDCNES(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.time.AbsoluteDate]:
        """
        
            Returns:
                the squaringJDCNES
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def simpsonMean(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    @staticmethod
    def simpsonMean(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> float: ...

class StelaForceModel(java.io.Serializable):
    """
    public interface StelaForceModel extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface represents a force modifying spacecraft motion for a
        :class:`~fr.cnes.sirius.patrius.stela.propagation.StelaGTOPropagator`.
    
        Objects implementing this interface are intended to be added to a
        :class:`~fr.cnes.sirius.patrius.stela.propagation.StelaGTOPropagator` before the propagation is started.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.ForceModel`
    """
    def computePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computeShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...
    def getType(self) -> str:
        """
        
            Returns:
                the type
        
        
        """
        ...

class StelaLagrangeEquations(java.io.Serializable):
    """
    public class StelaLagrangeEquations extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        Class for the computation of Lagrange Equations and its derivatives
    
        Computation of Lagrange Equations and its derivatives
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def computeLagrangeDerivativeEquations(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]:
        """
            Computation of the Lagrange equation derivatives matrix (Poisson Bracket derivatives).
        
            Parameters:
                orbit (:class:`~fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit`): current state information: date, kinematics, attitude
        
            Returns:
                Lagrange equations
        
        
        """
        ...
    @typing.overload
    def computeLagrangeEquations(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Compute the Lagrange Equation for GTO (Poisson Bracket).
        
            Parameters:
                orbit (:class:`~fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit`): current state information: date, kinematics, attitude
        
            Returns:
                Lagrange equations
        
            Compute the Lagrange Equation for GTO (Poisson Bracket) with specific mu.
        
            Parameters:
                orbit (:class:`~fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit`): current state information: date, kinematics, attitude
                mu (double): mu
        
            Returns:
                Lagrange equations
        
        
        """
        ...
    @typing.overload
    def computeLagrangeEquations(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, double: float) -> typing.MutableSequence[typing.MutableSequence[float]]: ...

class AbstractStelaGaussContribution(StelaForceModel):
    """
    public abstract class AbstractStelaGaussContribution extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.stela.forces.StelaForceModel`
    
    
        Abstract Class for the computation of Gauss Equations and its derivatives
    
        Computation of Gauss Equations and its derivatives Gives "GAUSS" attributes
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...
    def getType(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.StelaForceModel.getType` in
                interface :class:`~fr.cnes.sirius.patrius.stela.forces.StelaForceModel`
        
            Returns:
                the type
        
        
        """
        ...
    def getdPert(self) -> typing.MutableSequence[float]:
        """
        
            Returns:
                the dPert
        
        
        """
        ...

class AbstractStelaLagrangeContribution(StelaForceModel):
    """
    public abstract class AbstractStelaLagrangeContribution extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.stela.forces.StelaForceModel`
    
    
        This abstract class represents a force with Lagrange attribute, to be used in a
        :class:`~fr.cnes.sirius.patrius.stela.propagation.StelaGTOPropagator`.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[float]: ...
    def getType(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.StelaForceModel.getType` in
                interface :class:`~fr.cnes.sirius.patrius.stela.forces.StelaForceModel`
        
            Returns:
                the type
        
        
        """
        ...
    def getdPot(self) -> typing.MutableSequence[float]:
        """
        
            Returns:
                the dPot
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.forces")``.

    AbstractStelaGaussContribution: typing.Type[AbstractStelaGaussContribution]
    AbstractStelaLagrangeContribution: typing.Type[AbstractStelaLagrangeContribution]
    Squaring: typing.Type[Squaring]
    StelaForceModel: typing.Type[StelaForceModel]
    StelaLagrangeEquations: typing.Type[StelaLagrangeEquations]
    atmospheres: fr.cnes.sirius.patrius.stela.forces.atmospheres.__module_protocol__
    drag: fr.cnes.sirius.patrius.stela.forces.drag.__module_protocol__
    gravity: fr.cnes.sirius.patrius.stela.forces.gravity.__module_protocol__
    noninertial: fr.cnes.sirius.patrius.stela.forces.noninertial.__module_protocol__
    radiation: fr.cnes.sirius.patrius.stela.forces.radiation.__module_protocol__
    solaractivity: fr.cnes.sirius.patrius.stela.forces.solaractivity.__module_protocol__
