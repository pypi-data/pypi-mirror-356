
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.forces
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.time
import jpype
import typing



class CoriolisRelativisticEffect(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable, fr.cnes.sirius.patrius.forces.ForceModel, fr.cnes.sirius.patrius.forces.GradientModel):
    """
    public class CoriolisRelativisticEffect extends :class:`~fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
    
        Computation of the relativistic Coriolis effect (Einstein-de-Sitter effect) - IERS2003 standard (applies to Earth only).
    
        This is the 2nd order relativistic effect.
    
        Since:
            3.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    @typing.overload
    def __init__(self, double: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, boolean: bool): ...
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientPosition` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def computeGradientVelocity(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to velocity have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientVelocity` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def getEventsDetectors(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.events.EventDetector]:
        """
            Get the discrete events related to the model..
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.ForceModel.getEventsDetectors` in
                interface :class:`~fr.cnes.sirius.patrius.forces.ForceModel`
        
            Returns:
                array of events detectors or null if the model is not related to any discrete events
        
        
        """
        ...

class LenseThirringRelativisticEffect(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable, fr.cnes.sirius.patrius.forces.ForceModel, fr.cnes.sirius.patrius.forces.GradientModel):
    """
    public class LenseThirringRelativisticEffect extends :class:`~fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
    
        Computation of the relativistic Lense-Thirring effect - IERS2003 standard (applies to Earth only).
    
        This is the 3rd order relativistic effect.
    
        Since:
            3.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, double: float, frame: fr.cnes.sirius.patrius.frames.Frame, boolean: bool, boolean2: bool): ...
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientPosition` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def computeGradientVelocity(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to velocity have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientVelocity` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def getEventsDetectors(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.events.EventDetector]:
        """
            Get the discrete events related to the model..
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.ForceModel.getEventsDetectors` in
                interface :class:`~fr.cnes.sirius.patrius.forces.ForceModel`
        
            Returns:
                array of events detectors or null if the model is not related to any discrete events
        
        
        """
        ...

class SchwarzschildRelativisticEffect(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable, fr.cnes.sirius.patrius.forces.ForceModel, fr.cnes.sirius.patrius.forces.GradientModel):
    """
    public class SchwarzschildRelativisticEffect extends :class:`~fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
    
        Computation of the relativistic Schwarzschild effect.
    
        This is the 1st order relativistic effect.
    
        Since:
            3.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, boolean: bool, boolean2: bool): ...
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientPosition` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def computeGradientVelocity(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to velocity have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientVelocity` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def getEventsDetectors(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.events.EventDetector]:
        """
            Get the discrete events related to the model..
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.ForceModel.getEventsDetectors` in
                interface :class:`~fr.cnes.sirius.patrius.forces.ForceModel`
        
            Returns:
                array of events detectors or null if the model is not related to any discrete events
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.relativistic")``.

    CoriolisRelativisticEffect: typing.Type[CoriolisRelativisticEffect]
    LenseThirringRelativisticEffect: typing.Type[LenseThirringRelativisticEffect]
    SchwarzschildRelativisticEffect: typing.Type[SchwarzschildRelativisticEffect]
