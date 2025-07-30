
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.orbitalparameters
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.stela.forces
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



class JacobianConverter:
    """
    public final class JacobianConverter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Jacobian matrix converter: it is used to get Jacobian matrix from some equinoctial parameters to cartesian parameters
    
        Since:
            1.3
    """
    @staticmethod
    def computeEquinoctialToCartesianJacobian(stelaEquinoctialOrbit: 'StelaEquinoctialOrbit') -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Computes Jacobian matrix from equinoctial to cartesian.
        
            Parameters:
                orbit (:class:`~fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit`): Stela equinoctial orbit
        
            Returns:
                the Jacobian matrix
        
        
        """
        ...

class OrbitNatureConverter(java.io.Serializable):
    """
    public final class OrbitNatureConverter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Converts a :class:`~fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit` from mean to osculating parameters, and
        reverse. Since the :class:`~fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit` does not contain a "mean" or
        "osculating" information flag, it is the user's responsibility to ensure a coherent use of this converter.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, list: java.util.List[fr.cnes.sirius.patrius.stela.forces.StelaForceModel]): ...
    def getForceModels(self) -> java.util.List[fr.cnes.sirius.patrius.stela.forces.StelaForceModel]: ...
    @staticmethod
    def setThreshold(double: float) -> None:
        """
            Setter for osculating to mean conversion relative convergence threshold. Default value for this threshold is
            :meth:`~fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter.DEFAULT_THRESHOLD`.
        
            Parameters:
                newThreshold (double): new threshold to set
        
        
        """
        ...
    @staticmethod
    def setThresholdDegraded(double: float) -> None:
        """
            Setter for osculating to mean conversion second relative convergence threshold. This threshold is used only if
            convergence has not been reached within maximum number of iterations. If convergence is reached with this threshold,
            then last bulletin is returned, otherwise an exception is thrown. Default value for this threshold is
            :meth:`~fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter.DEFAULT_THRESHOLD`.
        
            Parameters:
                newThreshold (double): new threshold to set
        
        
        """
        ...
    def toMean(self, stelaEquinoctialOrbit: 'StelaEquinoctialOrbit') -> 'StelaEquinoctialOrbit': ...
    def toOsculating(self, stelaEquinoctialOrbit: 'StelaEquinoctialOrbit') -> 'StelaEquinoctialOrbit': ...

class StelaEquinoctialOrbit(fr.cnes.sirius.patrius.orbits.Orbit):
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double7: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double7: float, boolean: bool): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit): ...
    @typing.overload
    def __init__(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, boolean: bool): ...
    @typing.overload
    def __init__(self, iOrbitalParameters: fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float): ...
    def addKeplerContribution(self, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def equals(self, object: typing.Any) -> bool: ...
    def getA(self) -> float: ...
    def getE(self) -> float: ...
    def getEquinoctialEx(self) -> float: ...
    def getEquinoctialEy(self) -> float: ...
    def getEquinoctialParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.StelaEquinoctialParameters: ...
    def getHx(self) -> float: ...
    def getHy(self) -> float: ...
    def getI(self) -> float: ...
    def getIx(self) -> float: ...
    def getIy(self) -> float: ...
    def getLE(self) -> float: ...
    def getLM(self) -> float: ...
    def getLv(self) -> float: ...
    def getN(self) -> float: ...
    @typing.overload
    def getPVCoordinates(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    @typing.overload
    def getPVCoordinates(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    @typing.overload
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getParameters(self) -> fr.cnes.sirius.patrius.orbits.orbitalparameters.IOrbitalParameters: ...
    def getType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType: ...
    def hashCode(self) -> int: ...
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, collection: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.orbits.Orbit], typing.Sequence[fr.cnes.sirius.patrius.orbits.Orbit], typing.Set[fr.cnes.sirius.patrius.orbits.Orbit]]) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def kepEq(self, double: float, double2: float) -> float: ...
    def mapOrbitToArray(self) -> typing.MutableSequence[float]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.orbits")``.

    JacobianConverter: typing.Type[JacobianConverter]
    OrbitNatureConverter: typing.Type[OrbitNatureConverter]
    StelaEquinoctialOrbit: typing.Type[StelaEquinoctialOrbit]
