
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.forces
import fr.cnes.sirius.patrius.forces.atmospheres
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.time
import java.io
import jpype
import typing



class DragForce(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable, fr.cnes.sirius.patrius.forces.ForceModel, fr.cnes.sirius.patrius.forces.GradientModel):
    """
    public class DragForce extends :class:`~fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
    
        Atmospheric drag force model.
    
        The drag acceleration is computed as follows : γ = (1/2 * k * ρ * V :sup:`2` * S / Mass) * DragCoefVector
    
    
        With:
    
          - DragCoefVector = {Cx, Cy, Cz} and S given by the user through the interface
            :class:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive`.
          - k: user-added multiplicative coefficient to atmospheric drag. Partial derivatives wrt this coefficient can be computed.
    
    
        The implementation of this class enables the computation of partial derivatives with respect to **normal** and
        **tangential ballistic coefficients**.
    
        Also see:
            :meth:`~serialized`
    """
    K_COEFFICIENT: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` K_COEFFICIENT
    
        Parameter name for k coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, double: float, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    @typing.overload
    def __init__(self, double: float, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, dragSensitive: 'DragSensitive'): ...
    @typing.overload
    def __init__(self, double: float, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, dragSensitive: 'DragSensitive', boolean: bool, boolean2: bool): ...
    @typing.overload
    def __init__(self, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, dragSensitive: 'DragSensitive'): ...
    @typing.overload
    def __init__(self, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, dragSensitive: 'DragSensitive', boolean: bool, boolean2: bool): ...
    @typing.overload
    def __init__(self, dragForce: 'DragForce', assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    @typing.overload
    def __init__(self, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, dragSensitive: 'DragSensitive'): ...
    @typing.overload
    def __init__(self, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, dragSensitive: 'DragSensitive', boolean: bool, boolean2: bool): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, dragSensitive: 'DragSensitive'): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, dragSensitive: 'DragSensitive', boolean: bool, boolean2: bool): ...
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    @typing.overload
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            In the validation context, we assume that the multiplicative factor is equal to 1.
        
            Parameters:
                pv (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates`): PV coordinates of the spacecraft (spherical spacecraft only for the validation)
                frame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): frame in which the PV coordinates are given
                atm (:class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`): atmosphere
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
                kD (double): Composite drag coefficient (S.Cd/2).
                mass (double): mass of the spacecraft
        
            Returns:
                acceleration
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if an Orekit error occurs
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def computeAcceleration(pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, frame: fr.cnes.sirius.patrius.frames.Frame, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
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
    def getAtmosphere(self) -> fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere:
        """
            Get the atmosphere model.
        
            Returns:
                the atmosphere
        
        
        """
        ...
    def getEventsDetectors(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.events.EventDetector]:
        """
            There are no discrete events for this model.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.ForceModel.getEventsDetectors` in
                interface :class:`~fr.cnes.sirius.patrius.forces.ForceModel`
        
            Returns:
                an empty array
        
        
        """
        ...
    @typing.overload
    def getMultiplicativeFactor(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Getter for the multiplicative factor used at construction.
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): state
        
            Returns:
                the multiplicative factor.
        
        
        """
        ...
    @typing.overload
    def getMultiplicativeFactor(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction:
        """
            Getter for the multiplicative factor.
        
            Returns:
                the multiplicative factor
        
        """
        ...

class DragSensitive(java.io.Serializable, fr.cnes.sirius.patrius.propagation.numerical.JacobianParametersProvider):
    """
    public interface DragSensitive extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, :class:`~fr.cnes.sirius.patrius.propagation.numerical.JacobianParametersProvider`
    
        Interface for spacecraft that are sensitive to atmospheric drag and lift forces.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.drag.DragForce`
    """
    def addDDragAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDDragAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double3: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, boolean: bool, boolean2: bool) -> None: ...
    def copy(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly) -> 'DragSensitive':
        """
            Copy drag sensitive object using new assembly.
        
            Parameters:
                assembly (:class:`~fr.cnes.sirius.patrius.assembly.Assembly`): new assembly
        
            Returns:
                drag sensitive object with new assembly
        
        
        """
        ...
    def dragAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.drag")``.

    DragForce: typing.Type[DragForce]
    DragSensitive: typing.Type[DragSensitive]
