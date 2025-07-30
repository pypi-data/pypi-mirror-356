
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.ode
import java.io
import jpype
import typing



class CowellIntegrator(fr.cnes.sirius.patrius.math.ode.AbstractIntegrator):
    MAX_STANDARD_ORDER: typing.ClassVar[int] = ...
    def __init__(self, int: int, double: float, double2: float): ...
    def getMapper(self) -> 'SecondOrderStateMapper': ...
    def getOrder(self) -> int: ...
    @typing.overload
    def integrate(self, firstOrderDifferentialEquations: fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def integrate(self, expandableStatefulODE: fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE, double: float) -> None: ...
    def setMapper(self, secondOrderStateMapper: 'SecondOrderStateMapper') -> None: ...

class SecondOrderStateMapper(java.io.Externalizable):
    """
    public interface SecondOrderStateMapper extends `Externalizable <http://docs.oracle.com/javase/8/docs/api/java/io/Externalizable.html?is-external=true>`
    
        Mapper for second order integrator state vector. This mapper maps a full first order state vs a second order state (y,
        yDot). First order state is used for :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator`, second order state
        is used for second order integrator such as :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.cowell.CowellIntegrator`.
    
        For example for PV coordinates integration:
    
          - Full first order state is (x, y, z, vx, vy, vz). This state is built from second order state and state derivative using
            method null
          - Second order state y is (x, y, z). This state is retrieved using method null
          - Second order state derivative yDot is (vx, vy, vz). This state derivative is retrieved from first order state vector
            using methode null
    
    
        Since:
            4.6
    """
    def buildFullState(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Build full first order state from second order y and yDot.
        
            Parameters:
                y (double[]): second order state y
                yDot (double[]): second order state derivative yDot
        
            Returns:
                full first order state
        
        
        """
        ...
    def extractY(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Retrieve second order state y from full first order state.
        
            Parameters:
                fullState (double[]): full first order state
        
            Returns:
                second order state y
        
        
        """
        ...
    def extractYDot(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Retrieve second order state derivative yDot from full first order state.
        
            Parameters:
                fullState (double[]): full first order state
        
            Returns:
                second order state derivative yDot
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.ode.nonstiff.cowell")``.

    CowellIntegrator: typing.Type[CowellIntegrator]
    SecondOrderStateMapper: typing.Type[SecondOrderStateMapper]
