
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly
import fr.cnes.sirius.patrius.assembly.models.aerocoeffs
import fr.cnes.sirius.patrius.assembly.models.cook
import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.events.detectors
import fr.cnes.sirius.patrius.forces.atmospheres
import fr.cnes.sirius.patrius.forces.drag
import fr.cnes.sirius.patrius.forces.radiation
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.groundstation
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.math.util
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.time
import fr.cnes.sirius.patrius.wrenches
import java.io
import java.lang
import java.util
import jpype
import typing



class AeroModel(fr.cnes.sirius.patrius.math.parameter.Parameterizable, fr.cnes.sirius.patrius.forces.drag.DragSensitive):
    """
    public final class AeroModel extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive`
    
        Class that represents an aero model, based on the vehicle.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    @typing.overload
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid): ...
    @typing.overload
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid, double: float): ...
    def addDDragAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDDragAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double3: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, boolean: bool, boolean2: bool) -> None: ...
    def copy(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly) -> fr.cnes.sirius.patrius.forces.drag.DragSensitive:
        """
            Copy drag sensitive object using new assembly.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive.copy` in
                interface :class:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive`
        
            Parameters:
                newAssembly (:class:`~fr.cnes.sirius.patrius.assembly.Assembly`): new assembly
        
            Returns:
                drag sensitive object with new assembly
        
        
        """
        ...
    def dragAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getJacobianParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...

class AeroWrenchModel(fr.cnes.sirius.patrius.wrenches.DragWrenchSensitive):
    """
    public class AeroWrenchModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.wrenches.DragWrenchSensitive`
    
        This class represents a :class:`~fr.cnes.sirius.patrius.wrenches.DragWrenchSensitive` assembly model.
    
        Since:
            2.1
    """
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    @typing.overload
    def dragWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.wrenches.Wrench: ...
    @typing.overload
    def dragWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.wrenches.Wrench: ...

class DirectRadiativeModel(fr.cnes.sirius.patrius.math.parameter.Parameterizable, fr.cnes.sirius.patrius.forces.radiation.RadiationSensitive):
    """
    public final class DirectRadiativeModel extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.radiation.RadiationSensitive`
    
    
        Class that represents a radiative model, based on the vehicle.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    K0_COEFFICIENT: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` K0_COEFFICIENT
    
        Parameter name for K0 coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    @typing.overload
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly, double: float): ...
    @typing.overload
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def addDSRPAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray], vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> None: ...
    def addDSRPAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> None:
        """
            Compute acceleration derivatives with respect to state parameters.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.forces.radiation.RadiationSensitive`
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
                dAccdPos (double[][]): acceleration derivatives with respect to position parameters
                dAccdVel (double[][]): acceleration derivatives with respect to velocity parameters
                satSunVector (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): satellite to sun vector, expressed in the spacecraft frame
        
        
        """
        ...
    def getJacobianParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def radiationPressureAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class DirectRadiativeWrenchModel(fr.cnes.sirius.patrius.wrenches.RadiationWrenchSensitive):
    """
    public class DirectRadiativeWrenchModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.wrenches.RadiationWrenchSensitive`
    
        This class represents a spacecraft capable of computing the wrench caused by solar radiation pressure.
    
        Since:
            2.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    @typing.overload
    def radiationWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.wrenches.Wrench: ...
    @typing.overload
    def radiationWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.wrenches.Wrench: ...

class DragCoefficient:
    """
    public final class DragCoefficient extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Drag coefficient container. Drag coefficient is split in 4 parts:
    
          - Absorption part.
          - Specular part.
          - Diffuse part (front).
          - Diffuse part (rear).
    
    
        Drag coefficient must be expressed in satellite frame.
    
        Since:
            3.3
    """
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D4: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    def getScAbs(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the absorption part in satellite frame.
        
            Returns:
                the absorption part in satellite frame
        
        
        """
        ...
    def getScDiffAr(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the diffuse part (rear) in satellite frame.
        
            Returns:
                the diffuse part (rear) in satellite frame
        
        
        """
        ...
    def getScDiffAv(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the diffuse part (front) in satellite frame.
        
            Returns:
                the diffuse part (front) in satellite frame
        
        
        """
        ...
    def getScSpec(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the specular part in satellite frame.
        
            Returns:
                the specular part in satellite frame
        
        
        """
        ...

class DragCoefficientProvider(java.io.Serializable):
    """
    public interface DragCoefficientProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Drag coefficient (x surface) provider.
    
        Since:
            3.3
    """
    def getCoefficients(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, atmosphereData: fr.cnes.sirius.patrius.forces.atmospheres.AtmosphereData, assembly: fr.cnes.sirius.patrius.assembly.Assembly) -> DragCoefficient:
        """
            Provides drag coefficient (x surface).
        
            Parameters:
                relativeVelocity (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): relative velocity of atmosphere with respect to spacecraft in satellite frame
                atmoData (:class:`~fr.cnes.sirius.patrius.forces.atmospheres.AtmosphereData`): atmosphere data
                assembly (:class:`~fr.cnes.sirius.patrius.assembly.Assembly`): assembly
        
            Returns:
                drag coefficient (x surface) in satellite frame
        
        
        """
        ...

class DragLiftModel(fr.cnes.sirius.patrius.math.parameter.Parameterizable, fr.cnes.sirius.patrius.forces.drag.DragSensitive):
    """
    public final class DragLiftModel extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive`
    
        Class that represents an drag and lift aero model, based on the vehicle.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    def addDDragAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDDragAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double3: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, boolean: bool, boolean2: bool) -> None: ...
    def copy(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly) -> fr.cnes.sirius.patrius.forces.drag.DragSensitive:
        """
            Copy drag sensitive object using new assembly.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive.copy` in
                interface :class:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive`
        
            Parameters:
                newAssembly (:class:`~fr.cnes.sirius.patrius.assembly.Assembly`): new assembly
        
            Returns:
                drag sensitive object with new assembly
        
        
        """
        ...
    def dragAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getJacobianParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...

class GlobalAeroModel(fr.cnes.sirius.patrius.forces.drag.DragSensitive):
    """
    public final class GlobalAeroModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive`
    
        Global aero model for generic user-provided aero coefficients.
    
        This model requires a :class:`~fr.cnes.sirius.patrius.assembly.properties.AeroProperty`. This property has to be applied
        to Main part only:
    
          - If Main part does not have a :class:`~fr.cnes.sirius.patrius.assembly.properties.AeroProperty`, an exception is thrown.
          - If other parts have :class:`~fr.cnes.sirius.patrius.assembly.properties.AeroProperty`, they are not taken into account.
    
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly, dragCoefficientProvider: typing.Union[DragCoefficientProvider, typing.Callable], extendedAtmosphere: fr.cnes.sirius.patrius.forces.atmospheres.ExtendedAtmosphere): ...
    @typing.overload
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly, dragCoefficientProvider: typing.Union[DragCoefficientProvider, typing.Callable], extendedAtmosphere: fr.cnes.sirius.patrius.forces.atmospheres.ExtendedAtmosphere, double: float): ...
    def addDDragAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDDragAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double3: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, boolean: bool, boolean2: bool) -> None: ...
    def computeSC(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, frame: fr.cnes.sirius.patrius.frames.Frame, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def copy(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly) -> fr.cnes.sirius.patrius.forces.drag.DragSensitive:
        """
            Copy drag sensitive object using new assembly.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive.copy` in
                interface :class:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive`
        
            Parameters:
                newAssembly (:class:`~fr.cnes.sirius.patrius.assembly.Assembly`): new assembly
        
            Returns:
                drag sensitive object with new assembly
        
        
        """
        ...
    def dragAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getJacobianParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...

class IInertiaModel(fr.cnes.sirius.patrius.propagation.MassProvider):
    """
    public interface IInertiaModel extends :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
    
    
        Since:
            1.2
    """
    @typing.overload
    def getInertiaMatrix(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D: ...
    @typing.overload
    def getInertiaMatrix(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D: ...
    def getMassCenter(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class InterpolatedDragReader:
    """
    public class InterpolatedDragReader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Generic reader to read a file containing aero coefficients and store these coefficients. The file must have the
        following format : - lines starting with/containing only "#" are comments - the file is a column-files : each column is
        separated by spaces or tabs This reader is used to build an implementation of
        :class:`~fr.cnes.sirius.patrius.assembly.models.DragCoefficientProvider`.
    
        Since:
            3.4
    """
    def __init__(self): ...
    def readFile(self, string: str) -> typing.MutableSequence[typing.MutableSequence[float]]: ...

class MagneticMomentProvider:
    """
    public interface MagneticMomentProvider
    
        Interface for electromagnetic sensitive spacecraft
    
        Since:
            2.1
    """
    def getMagneticMoment(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the magnetic moment at given date, in the main frame of the spacecraft
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for computation of magnetic moment
        
            Returns:
                the computed magnetic moment
        
        
        """
        ...

class MassModel(fr.cnes.sirius.patrius.propagation.MassProvider):
    """
    public class MassModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
    
        This class represents a mass model for an assembly with parts that have mass properties.
    
        Note : when using this model within a propagation, it is necessary to feed the additional equations to the propagator.
        This has to be done prior to any propagation, to allow this model to account mass variations (i.e. due to maneuvers),
        using the method :meth:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator.setMassProviderEquation` which
        will register the additional equation and initialize the initial additional state.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.Assembly`, :class:`~fr.cnes.sirius.patrius.assembly.properties.MassProperty`,
            :meth:`~serialized`
    """
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    def addMassDerivative(self, string: str, double: float) -> None:
        """
            Add the mass derivate of the given part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.addMassDerivative` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of part subject to mass variation
                flowRate (double): flow rate of specified part
        
        
        """
        ...
    def getAdditionalEquation(self, string: str) -> fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations:
        """
            Get the mass equation related to the part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getAdditionalEquation` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): part name
        
            Returns:
                the associated mass equation
        
        
        """
        ...
    def getAllPartsNames(self) -> java.util.List[str]: ...
    def getMass(self, string: str) -> float:
        """
            Return the mass of the given part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): given part
        
            Returns:
                mass of part
        
        
        """
        ...
    @typing.overload
    def getTotalMass(self) -> float:
        """
            Return the mass of the spacecraft.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Returns:
                spacecraft mass
        
        """
        ...
    @typing.overload
    def getTotalMass(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Return the mass of the spacecraft following the order.
        
              - If mass is in spacecraft state, mass from spacecraft state will be returned
              - Otherwise mass from mass provider is returned (same as
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass`)
        
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
            Returns:
                spacecraft mass
        
        
        """
        ...
    def setMassDerivativeZero(self, string: str) -> None:
        """
            Set mass derivative to zero.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.setMassDerivativeZero` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of part whose mass derivative is set to zero
        
        
        """
        ...
    def updateMass(self, string: str, double: float) -> None: ...

class RFLinkBudgetModel(java.io.Serializable):
    """
    public class RFLinkBudgetModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class contains the algorithm to compute the link budget knowing the satellite transmitter and ground receiver
        parameters.
    
    
        The link budget is the accounting of all of the gains and losses from the transmitter (the satellite), through the
        medium to the receiver (the ground station).
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.events.detectors.RFVisibilityDetector`,
            :class:`~fr.cnes.sirius.patrius.assembly.properties.RFAntennaProperty`, :meth:`~serialized`
    """
    KDB: typing.ClassVar[float] = ...
    """
    public static final double KDB
    
        Boltzmann constant [dBW / Hz / K].
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self, rFStationAntenna: fr.cnes.sirius.patrius.groundstation.RFStationAntenna, assembly: fr.cnes.sirius.patrius.assembly.Assembly, string: str): ...
    @typing.overload
    def computeLinkBudget(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    @typing.overload
    def computeLinkBudget(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getReceiver(self) -> fr.cnes.sirius.patrius.groundstation.RFStationAntenna:
        """
            Returns the receiver (ground antenna).
        
            Returns:
                the receiver
        
        
        """
        ...
    def getSatellite(self) -> fr.cnes.sirius.patrius.assembly.Assembly:
        """
        
            Returns:
                the assembly representing the satellite
        
        
        """
        ...

class RediffusedRadiativeModel(fr.cnes.sirius.patrius.math.parameter.Parameterizable, fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive):
    """
    public final class RediffusedRadiativeModel extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive`
    
    
        Class that represents a rediffused radiative model, based on the vehicle.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    K0ALBEDO_COEFFICIENT: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` K0ALBEDO_COEFFICIENT
    
        Parameter name for K0 albedo global coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    K0IR_COEFFICIENT: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` K0IR_COEFFICIENT
    
        Parameter name for K0 infrared global coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, boolean: bool, boolean2: bool, double: float, double2: float, assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    @typing.overload
    def __init__(self, boolean: bool, boolean2: bool, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    def addDAccDParamRediffusedRadiativePressure(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDStateRediffusedRadiativePressure(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None:
        """
            Compute acceleration derivatives.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive`
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): Spacecraft state.
                dAccdPos (double[][]): acceleration derivatives with respect to position
                dAccdVel (double[][]): acceleration derivatives with respect to velocity
        
        
        """
        ...
    def getAssembly(self) -> fr.cnes.sirius.patrius.assembly.Assembly:
        """
            assembly getter
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive.getAssembly` in
                interface :class:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive`
        
            Returns:
                assembly
        
        
        """
        ...
    def getFlagAlbedo(self) -> bool:
        """
            albedo getter
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive.getFlagAlbedo` in
                interface :class:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive`
        
            Returns:
                calculation indicator of the albedo force
        
        
        """
        ...
    def getFlagIr(self) -> bool:
        """
            infrared getter
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive.getFlagIr` in
                interface :class:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive`
        
            Returns:
                calculation indicator of the infrared force
        
        
        """
        ...
    def getJacobianParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def getK0Albedo(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            K0 albedo getter
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive.getK0Albedo` in
                interface :class:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive`
        
            Returns:
                albedo global multiplicative factor
        
        
        """
        ...
    def getK0Ir(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            K0 infrared getter
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive.getK0Ir` in
                interface :class:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive`
        
            Returns:
                the infrared global multiplicative factor
        
        
        """
        ...
    def initDerivatives(self) -> None:
        """
            derivatives initialisation
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive.initDerivatives` in
                interface :class:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationSensitive`
        
        
        """
        ...
    def rediffusedRadiationPressureAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, elementaryFluxArray: typing.Union[typing.List[fr.cnes.sirius.patrius.forces.radiation.ElementaryFlux], jpype.JArray]) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class SecondarySpacecraft(java.io.Serializable):
    """
    public class SecondarySpacecraft extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        Secondary spacecraft to be used in events detections. It is described by its assembly of parts and a propagator.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly, propagator: fr.cnes.sirius.patrius.propagation.Propagator, string: str): ...
    def getAssembly(self) -> fr.cnes.sirius.patrius.assembly.Assembly:
        """
        
            Returns:
                the spacecraft's assembly
        
        
        """
        ...
    def getName(self) -> str:
        """
        
            Returns:
                the spacecraft's name
        
        
        """
        ...
    def getPropagator(self) -> fr.cnes.sirius.patrius.propagation.Propagator:
        """
        
            Returns:
                the propagator
        
        
        """
        ...
    def updateSpacecraftState(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class SensorModel(fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider):
    """
    public final class SensorModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
    
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.properties.SensorProperty`, :meth:`~serialized`
    """
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly, string: str): ...
    def addMaskingCelestialBody(self, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape) -> None:
        """
            Adds a celestial body shape to consider in maskings.
        
            Parameters:
                body (:class:`~fr.cnes.sirius.patrius.bodies.BodyShape`): the celestial body shape to consider
        
        
        """
        ...
    def addOwnMaskingParts(self, stringArray: typing.Union[typing.List[str], jpype.JArray]) -> None:
        """
            Enables the masking by the considered spacecraft's own parts, by giving the names of the parts that can cause maskings.
        
            Parameters:
                partsNames (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`[]): the names of the considered parts
        
        
        """
        ...
    def addSecondaryMaskingSpacecraft(self, secondarySpacecraft: SecondarySpacecraft, stringArray: typing.Union[typing.List[str], jpype.JArray]) -> None:
        """
            Enables the masking by a secondary spacecraft's parts, by giving the names of the parts that can cause maskings.
        
            Parameters:
                spacecraft (:class:`~fr.cnes.sirius.patrius.assembly.models.SecondarySpacecraft`): the secondary masking spacecraft
                partsNames (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`[]): partsNames the names of the considered parts
        
        
        """
        ...
    def celestialBodiesMaskingDistance(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, propagationDelayType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType, linkType: fr.cnes.sirius.patrius.events.detectors.VisibilityFromStationDetector.LinkType) -> float: ...
    @staticmethod
    def computeMinDistToMaskingBodies(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, signalPropagationRole: fr.cnes.sirius.patrius.events.detectors.LinkTypeHandler.SignalPropagationRole, frame: fr.cnes.sirius.patrius.frames.Frame, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, list: java.util.List[fr.cnes.sirius.patrius.bodies.BodyShape], propagationDelayType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType, double: float, int: int) -> fr.cnes.sirius.patrius.math.util.Pair[fr.cnes.sirius.patrius.bodies.BodyShape, float]: ...
    def getAssembly(self) -> fr.cnes.sirius.patrius.assembly.Assembly:
        """
        
            Returns:
                the assembly of this sensor
        
        
        """
        ...
    def getInhibitTargetCenterToFieldAngle(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, int: int) -> float: ...
    def getInhibitionFieldsNumber(self) -> int:
        """
        
            Returns:
                the number of couples inhibition field / inhibition target
        
        
        """
        ...
    def getInhibitionTarget(self, int: int) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Returns inhibition field number #i. Warning: no check is performed if provided number is beyond limits.
        
            Parameters:
                inhibitionFieldNumber (int): number of the inhibition field to consider (first is 1)
        
            Returns:
                inhibition field number #i
        
        
        """
        ...
    def getInhibitionTargetAngularRadius(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, int: int, propagationDelayType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType) -> float: ...
    def getMainTarget(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Getter for the main target.
        
            Returns:
                the main target
        
        
        """
        ...
    def getMainTargetAngularRadius(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMaskingBody(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Getter for the last masking body.
        
            Returns:
                the last masking body
        
        
        """
        ...
    def getMaskingBodyName(self) -> str:
        """
        
            Returns:
                the last masking body number
        
        
        """
        ...
    def getMaskingSpacecraft(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Getter for the last masking spacecraft.
        
            Returns:
                the last masking spacecraft
        
        
        """
        ...
    def getMaskingSpacecraftName(self) -> str:
        """
        
            Returns:
                the last masking spacecraft name
        
        
        """
        ...
    def getMaskingSpacecraftPartName(self) -> str:
        """
        
            Returns:
                the last masking spacecraft's part name
        
        
        """
        ...
    def getMaxIterSignalPropagation(self) -> int:
        """
            Getter for the maximum number of iterations for signal propagation when signal propagation is taken into account.
        
            Returns:
                the maximum number of iterations for signal propagation
        
        
        """
        ...
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the native frame, i.e. the raw frame in which PVCoordinates are expressed before transformation to user output
            frame.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider.getNativeFrame` in
                interface :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                the native frame
        
        
        """
        ...
    def getNormalisedTargetVectorInSensorFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getReferenceAxis(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D]: ...
    def getSightAxis(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getTargetCenterFOVAngle(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    @typing.overload
    def getTargetCenterFOVAngle(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getTargetDihedralAngles(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]: ...
    def getTargetRefAxisAngle(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, int: int) -> float: ...
    def getTargetRefAxisElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, int: int) -> float: ...
    def getTargetSightAxisAngle(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getTargetSightAxisElevation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    @typing.overload
    def getTargetVectorInSensorFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getTargetVectorInSensorFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def isMainTargetInField(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> bool: ...
    def noInhibition(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> bool: ...
    def resetProperty(self) -> None:
        """
            Resets the sensor property features. Shall be used each time the associated sensor property has been modified.
        
        """
        ...
    def setEpsilonSignalPropagation(self, double: float) -> None:
        """
            Set the epsilon for signal propagation used in :code:`#spacecraftsMaskingDistance(AbsoluteDate, AbsoluteDate,
            PropagationDelayType, LinkType)` and :code:`#celestialBodiesMaskingDistance(AbsoluteDate, AbsoluteDate,
            PropagationDelayType, LinkType)` methods. This epsilon (in s) directly reflect the accuracy of signal propagation (1s of
            accuracy = 3E8m of accuracy on distance between emitter and receiver).
        
            Parameters:
                epsSignalPropagation (double): epsilon for signal propagation
        
        
        """
        ...
    def setMainTarget(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, apparentRadiusProvider: typing.Union[fr.cnes.sirius.patrius.bodies.ApparentRadiusProvider, typing.Callable]) -> None:
        """
            Sets the main target of the sensor property.
        
            Parameters:
                target (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`): the new main target center
                radius (:class:`~fr.cnes.sirius.patrius.bodies.ApparentRadiusProvider`): the target's radius
        
        
        """
        ...
    def setMaxIterSignalPropagation(self, int: int) -> None:
        """
            Setter for the maximum number of iterations for signal propagation when signal propagation is taken into account.
        
            Parameters:
                maxIterSignalPropagation (int): Maximum number of iterations for signal propagation
        
        
        """
        ...
    def spacecraftsMaskingDistance(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, propagationDelayType: fr.cnes.sirius.patrius.events.detectors.AbstractSignalPropagationDetector.PropagationDelayType, linkType: fr.cnes.sirius.patrius.events.detectors.VisibilityFromStationDetector.LinkType) -> float: ...
    def visibilityOk(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> bool: ...

class GlobalDragCoefficientProvider(DragCoefficientProvider):
    def __init__(self, iNTERP: 'GlobalDragCoefficientProvider.INTERP', string: str): ...
    def getCoefficients(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, atmosphereData: fr.cnes.sirius.patrius.forces.atmospheres.AtmosphereData, assembly: fr.cnes.sirius.patrius.assembly.Assembly) -> DragCoefficient: ...
    class INTERP(java.lang.Enum['GlobalDragCoefficientProvider.INTERP']):
        LINEAR: typing.ClassVar['GlobalDragCoefficientProvider.INTERP'] = ...
        SPLINE: typing.ClassVar['GlobalDragCoefficientProvider.INTERP'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'GlobalDragCoefficientProvider.INTERP': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['GlobalDragCoefficientProvider.INTERP']: ...

class InertiaComputedModel(IInertiaModel):
    """
    public class InertiaComputedModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.models.IInertiaModel`
    
        This class is an inertia model computed from the inertia properties of each parts of an Assembly object.
    
        Note : when using this model within a propagation, it is necessary to feed the additional equations to the propagator.
        This has to be done prior to any propagation, to allow this model to account mass variations (i.e. due to maneuvers),
        using the method NumericalPropagator.setMassProviderEquation() which will register the additional equation and
        initialize the initial additional state.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.models.IInertiaModel`, :meth:`~serialized`
    """
    def __init__(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly): ...
    def addMassDerivative(self, string: str, double: float) -> None:
        """
            Add the mass derivate of the given part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.addMassDerivative` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of part subject to mass variation
                flowRate (double): flow rate of specified part
        
        
        """
        ...
    def getAdditionalEquation(self, string: str) -> fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations:
        """
            Get the mass equation related to the part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getAdditionalEquation` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): part name
        
            Returns:
                the associated mass equation
        
        
        """
        ...
    def getAllPartsNames(self) -> java.util.List[str]: ...
    @typing.overload
    def getInertiaMatrix(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D: ...
    @typing.overload
    def getInertiaMatrix(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D: ...
    def getMass(self, string: str) -> float:
        """
            Return the mass of the given part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): given part
        
            Returns:
                mass of part
        
        
        """
        ...
    def getMassCenter(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getTotalMass(self) -> float:
        """
            Return the mass of the spacecraft.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Returns:
                spacecraft mass
        
        """
        ...
    @typing.overload
    def getTotalMass(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Return the mass of the spacecraft following the order.
        
              - If mass is in spacecraft state, mass from spacecraft state will be returned
              - Otherwise mass from mass provider is returned (same as
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass`)
        
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
            Returns:
                spacecraft mass
        
        
        """
        ...
    def setMassDerivativeZero(self, string: str) -> None:
        """
            Set mass derivative to zero.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.setMassDerivativeZero` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of part whose mass derivative is set to zero
        
        
        """
        ...
    def updateMass(self, string: str, double: float) -> None: ...

class InertiaSimpleModel(IInertiaModel):
    """
    public final class InertiaSimpleModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.models.IInertiaModel`
    
        Simple inertia model : the mass, mass center and inertia matrix are directly given by the user.
    
        Note : when using this model within a propagation, it is necessary to feed the additional equations to the propagator.
        This has to be done prior to any propagation, to allow this model to account mass variations (i.e. due to maneuvers),
        using the method NumericalPropagator.setMassProviderEquation() which will register the additional equation and
        initialize the initial additional state.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.models.IInertiaModel`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, matrix3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D, frame: fr.cnes.sirius.patrius.frames.Frame, string: str): ...
    @typing.overload
    def __init__(self, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, matrix3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, string: str): ...
    def addMassDerivative(self, string: str, double: float) -> None:
        """
            Add the mass derivate of the given part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.addMassDerivative` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of part subject to mass variation
                flowRate (double): flow rate of specified part
        
        
        """
        ...
    def getAdditionalEquation(self, string: str) -> fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations:
        """
            Get the mass equation related to the part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getAdditionalEquation` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): part name
        
            Returns:
                the associated mass equation
        
        
        """
        ...
    def getAllPartsNames(self) -> java.util.List[str]: ...
    @typing.overload
    def getInertiaMatrix(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D: ...
    @typing.overload
    def getInertiaMatrix(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D: ...
    def getMass(self, string: str) -> float:
        """
            Return the mass of the given part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): given part
        
            Returns:
                mass of part
        
        
        """
        ...
    def getMassCenter(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def getTotalMass(self) -> float:
        """
            Return the mass of the spacecraft.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Returns:
                spacecraft mass
        
        """
        ...
    @typing.overload
    def getTotalMass(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Return the mass of the spacecraft following the order.
        
              - If mass is in spacecraft state, mass from spacecraft state will be returned
              - Otherwise mass from mass provider is returned (same as
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass`)
        
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.getTotalMass` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
            Returns:
                spacecraft mass
        
        
        """
        ...
    def setMassDerivativeZero(self, string: str) -> None:
        """
            Set mass derivative to zero.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.MassProvider.setMassDerivativeZero` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of part whose mass derivative is set to zero
        
        
        """
        ...
    def updateIntertiaMatrix(self, matrix3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D) -> None:
        """
            Updates the inertia matrix.
        
            Parameters:
                inertiaMatrix (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D`): the new inertia matrix.
        
        
        """
        ...
    def updateMass(self, string: str, double: float) -> None: ...
    def updateMassCenter(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> None:
        """
            Updates the mass center.
        
            Parameters:
                massCenter (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the new mass center
        
        
        """
        ...

class MagneticMoment(MagneticMomentProvider):
    """
    public class MagneticMoment extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.models.MagneticMomentProvider`
    
        This class represents the magnetic moment of a Spacecraft
    
        Since:
            2.1
    """
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    def getMagneticMoment(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the magnetic moment at given date, in the main frame of the spacecraft
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.models.MagneticMomentProvider.getMagneticMoment` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.models.MagneticMomentProvider`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date for computation of magnetic moment
        
            Returns:
                the computed magnetic moment
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.assembly.models")``.

    AeroModel: typing.Type[AeroModel]
    AeroWrenchModel: typing.Type[AeroWrenchModel]
    DirectRadiativeModel: typing.Type[DirectRadiativeModel]
    DirectRadiativeWrenchModel: typing.Type[DirectRadiativeWrenchModel]
    DragCoefficient: typing.Type[DragCoefficient]
    DragCoefficientProvider: typing.Type[DragCoefficientProvider]
    DragLiftModel: typing.Type[DragLiftModel]
    GlobalAeroModel: typing.Type[GlobalAeroModel]
    GlobalDragCoefficientProvider: typing.Type[GlobalDragCoefficientProvider]
    IInertiaModel: typing.Type[IInertiaModel]
    InertiaComputedModel: typing.Type[InertiaComputedModel]
    InertiaSimpleModel: typing.Type[InertiaSimpleModel]
    InterpolatedDragReader: typing.Type[InterpolatedDragReader]
    MagneticMoment: typing.Type[MagneticMoment]
    MagneticMomentProvider: typing.Type[MagneticMomentProvider]
    MassModel: typing.Type[MassModel]
    RFLinkBudgetModel: typing.Type[RFLinkBudgetModel]
    RediffusedRadiativeModel: typing.Type[RediffusedRadiativeModel]
    SecondarySpacecraft: typing.Type[SecondarySpacecraft]
    SensorModel: typing.Type[SensorModel]
    aerocoeffs: fr.cnes.sirius.patrius.assembly.models.aerocoeffs.__module_protocol__
    cook: fr.cnes.sirius.patrius.assembly.models.cook.__module_protocol__
