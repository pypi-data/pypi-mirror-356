
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly
import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.forces.atmospheres
import fr.cnes.sirius.patrius.forces.drag
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.stela.bodies
import fr.cnes.sirius.patrius.stela.forces
import fr.cnes.sirius.patrius.stela.orbits
import java.io
import java.lang
import java.util
import jpype
import typing



class AbstractStelaDragCoef(java.io.Serializable):
    """
    public abstract class AbstractStelaDragCoef extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Abstract class for drag coefficient
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    MAXIMUM_FRACTION_DIGITS: typing.ClassVar[int] = ...
    """
    public static final int MAXIMUM_FRACTION_DIGITS
    
        Maximum fraction digits
    
        Also see:
            :meth:`~constant`
    
    
    """
    def copy(self) -> 'AbstractStelaDragCoef':
        """
            Copy drag coefficient.
        
            Returns:
                copied drag coefficient
        
        
        """
        ...
    def getDragCoef(self, stelaDragCoefInput: 'StelaDragCoefInput') -> float: ...
    def getDragCoefType(self) -> 'StelaDragCoefType':
        """
            Get the drag coefficient type.
        
            Returns:
                drag coefficient type
        
        
        """
        ...

class StelaAeroModel(fr.cnes.sirius.patrius.math.parameter.Parameterizable, fr.cnes.sirius.patrius.forces.drag.DragSensitive):
    """
    public final class StelaAeroModel extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive`
    
    
        This class represents a STELA aero model, based on a spherical spacecraft.
    
        It contains the STELA algorithm for the drag computation, as well as the STELA algorithm for the computation of the
        partial derivatives with respect to position and velocity, in the TNW frame.
    
    
        As this class is an implementation of the :class:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive` interface, it is
        intended to be used in the :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaAtmosphericDrag` class.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.models.AeroModel`,
            :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaAtmosphericDrag`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, abstractStelaDragCoef: AbstractStelaDragCoef, double2: float): ...
    @typing.overload
    def __init__(self, double: float, abstractStelaDragCoef: AbstractStelaDragCoef, double2: float, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, double3: float): ...
    @typing.overload
    def __init__(self, double: float, abstractStelaDragCoef: AbstractStelaDragCoef, double2: float, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, double3: float, geodPosition: fr.cnes.sirius.patrius.stela.bodies.GeodPosition): ...
    def addDDragAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDDragAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double3: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, boolean: bool, boolean2: bool) -> None: ...
    def copy(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly) -> fr.cnes.sirius.patrius.forces.drag.DragSensitive:
        """
            Copy drag sensitive object using new assembly.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive.copy` in
                interface :class:`~fr.cnes.sirius.patrius.forces.drag.DragSensitive`
        
            Parameters:
                assembly (:class:`~fr.cnes.sirius.patrius.assembly.Assembly`): new assembly
        
            Returns:
                drag sensitive object with new assembly
        
        
        """
        ...
    def dragAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getJacobianParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...

class StelaAtmosphericDrag(fr.cnes.sirius.patrius.stela.forces.AbstractStelaGaussContribution):
    """
    public class StelaAtmosphericDrag extends :class:`~fr.cnes.sirius.patrius.stela.forces.AbstractStelaGaussContribution`
    
        Class representing the atmospheric drag for the Stela GTO extrapolator.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaAeroModel`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, dragSensitive: fr.cnes.sirius.patrius.forces.drag.DragSensitive, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, int: int, double: float, double2: float, int2: int): ...
    @typing.overload
    def __init__(self, dragSensitive: fr.cnes.sirius.patrius.forces.drag.DragSensitive, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, int: int, double: float, double2: float, int2: int, int3: int): ...
    def computePartialDerivatives(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computePerturbation(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...
    def computeShortPeriods(self, stelaEquinoctialOrbit: fr.cnes.sirius.patrius.stela.orbits.StelaEquinoctialOrbit, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter) -> typing.MutableSequence[float]: ...
    def getDragRecomputeStep(self) -> int:
        """
        
            Returns:
                the dragRecomputeStep
        
        
        """
        ...
    def setTransMatComputationFlag(self, boolean: bool) -> None:
        """
            Setter for the switch indicating whether the drag term of the transition matrix has to be computed.
        
            Parameters:
                transMatrixFlag (boolean): flag to set
        
        
        """
        ...

class StelaDragCoefInput(java.io.Serializable):
    """
    public class StelaDragCoefInput extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class for drag coefficients inputs.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, double2: float, double3: float): ...
    def getMolarMass(self) -> float:
        """
            Getter for mean molar mass of the atmosphere.
        
            Returns:
                the mean molar mass of the atmosphere
        
        
        """
        ...
    def getPosition(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Getter for the position.
        
            Returns:
                the position (m)
        
        
        """
        ...
    def getTemperature(self) -> float:
        """
            Getter for temperature of the atmosphere.
        
            Returns:
                the temperature of the atmosphere (K)
        
        
        """
        ...
    def getVelocity(self) -> float:
        """
            Getter for the relative velocity of the spacecraft with respect to the atmosphere.
        
            Returns:
                the relative velocity of the spacecraft with respect to the atmosphere (m/s)
        
        
        """
        ...

class StelaDragCoefType(java.lang.Enum['StelaDragCoefType']):
    """
    public enum StelaDragCoefType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaDragCoefType`>
    
        Drag coefficient types. They can be either constant or variable.
    
        Since:
            4.16
    """
    CONSTANT: typing.ClassVar['StelaDragCoefType'] = ...
    VARIABLE: typing.ClassVar['StelaDragCoefType'] = ...
    VARIABLE_DISPERSED: typing.ClassVar['StelaDragCoefType'] = ...
    COOK: typing.ClassVar['StelaDragCoefType'] = ...
    COOK_DISPERSED: typing.ClassVar['StelaDragCoefType'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'StelaDragCoefType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                : if this enum type has no constant with the specified name
                : if the argument is null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['StelaDragCoefType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (StelaDragCoefType c : StelaDragCoefType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class StelaVariableDragCoefReader(fr.cnes.sirius.patrius.data.DataLoader, java.io.Serializable):
    """
    public class StelaVariableDragCoefReader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataLoader`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class which reads values of a drag coefficient in a file.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_FILE: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_FILE
    
        Default file path.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def getCoefficients(self) -> java.util.Map[float, float]: ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...
    def loadDefaultData(self) -> None: ...
    def stillAcceptsData(self) -> bool:
        """
            Check if the loader still accepts new data.
        
            This method is used to speed up data loading by interrupting crawling the data sets as soon as a loader has found the
            data it was waiting for. For loaders that can merge data from any number of sources (for example JPL ephemerides or
            Earth Orientation Parameters that are split among several files), this method should always return true to make sure no
            data is left over.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.data.DataLoader.stillAcceptsData` in
                interface :class:`~fr.cnes.sirius.patrius.data.DataLoader`
        
            Returns:
                true while the loader still accepts new data
        
        
        """
        ...

class StelaConstantDragCoef(AbstractStelaDragCoef):
    """
    public class StelaConstantDragCoef extends :class:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef`
    
        Class defining constant drag coefficients. Whatever the value of space object's height is, drag coefficients from this
        class take a constant value.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    def copy(self) -> 'StelaConstantDragCoef':
        """
            Copy drag coefficient.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef.copy` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef`
        
            Returns:
                copied drag coefficient
        
        
        """
        ...
    def getDragCoef(self, stelaDragCoefInput: StelaDragCoefInput) -> float:
        """
            Get the drag coefficient value.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef.getDragCoef` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef`
        
            Parameters:
                stelaDragCoefInput (:class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaDragCoefInput`): input necessary for drag coefficient computation
        
            Returns:
                drag coefficient
        
        
        """
        ...
    def getStatInformation(self) -> str:
        """
            Get statistical drag coefficient information.
        
            Returns:
                statistical drag coefficient information
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class StelaCookDragCoef(AbstractStelaDragCoef):
    """
    public class StelaCookDragCoef extends :class:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef`
    
        Class for drag coefficients using Cook formula.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float): ...
    def copy(self) -> 'StelaCookDragCoef':
        """
            Copy drag coefficient.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef.copy` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef`
        
            Returns:
                copied drag coefficient
        
        
        """
        ...
    def getDragCoef(self, stelaDragCoefInput: StelaDragCoefInput) -> float:
        """
            Get the drag coefficient value.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef.getDragCoef` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef`
        
            Parameters:
                stelaDragCoefInput (:class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaDragCoefInput`): input necessary for drag coefficient computation
        
            Returns:
                drag coefficient
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class StelaVariableDragCoef(AbstractStelaDragCoef):
    """
    public class StelaVariableDragCoef extends :class:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef`
    
        Class for drag coefficients depending on space object's altitude.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[float, float], typing.Mapping[float, float]], double: float, double2: float): ...
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[float, float], typing.Mapping[float, float]], geodPosition: fr.cnes.sirius.patrius.stela.bodies.GeodPosition): ...
    def copy(self) -> 'StelaVariableDragCoef':
        """
            Copy drag coefficient.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef.copy` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef`
        
            Returns:
                copied drag coefficient
        
        
        """
        ...
    def getCdMap(self) -> java.util.Map[float, float]: ...
    def getDragCoef(self, stelaDragCoefInput: StelaDragCoefInput) -> float: ...
    def getGeodPosition(self) -> fr.cnes.sirius.patrius.stela.bodies.GeodPosition:
        """
            Get the geodetic model
        
            Returns:
                The geodetic model
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class StelaCookDispersedDragCoef(StelaCookDragCoef):
    """
    public class StelaCookDispersedDragCoef extends :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaCookDragCoef`
    
        Class for drag coefficients using Cook formula with a multiplicative coefficient applied to the computed drag
        coefficient.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...
    def copy(self) -> 'StelaCookDispersedDragCoef':
        """
            Copy drag coefficient.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaCookDragCoef.copy` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaCookDragCoef`
        
            Returns:
                copied drag coefficient
        
        
        """
        ...
    def getDragCoef(self, stelaDragCoefInput: StelaDragCoefInput) -> float:
        """
            Get the drag coefficient value.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaCookDragCoef.getDragCoef` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaCookDragCoef`
        
            Parameters:
                stelaDragCoefInput (:class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaDragCoefInput`): input necessary for drag coefficient computation
        
            Returns:
                drag coefficient
        
        
        """
        ...
    def getStatInformation(self) -> str:
        """
            Get statistical coefficient information.
        
            Returns:
                statistical coefficient information
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaCookDragCoef.toString` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaCookDragCoef`
        
        
        """
        ...

class StelaVariableDispersedDragCoef(StelaVariableDragCoef):
    """
    public class StelaVariableDispersedDragCoef extends :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaVariableDragCoef`
    
        Class for drag coefficients depending on space object's height, with a multiplicative coefficient applied to the read
        drag coefficients.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[float, float], typing.Mapping[float, float]], double: float, double2: float): ...
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[float, float], typing.Mapping[float, float]], double: float, double2: float, double3: float): ...
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[float, float], typing.Mapping[float, float]], geodPosition: fr.cnes.sirius.patrius.stela.bodies.GeodPosition, double: float): ...
    def copy(self) -> 'StelaVariableDispersedDragCoef':
        """
            Copy drag coefficient.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaVariableDragCoef.copy` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaVariableDragCoef`
        
            Returns:
                copied drag coefficient
        
        
        """
        ...
    def getCoef(self) -> float:
        """
            Get the coefficient of the variable drag coef.
        
            Returns:
                the coefficient of the variable drag coef.
        
        
        """
        ...
    def getDragCoef(self, stelaDragCoefInput: StelaDragCoefInput) -> float: ...
    def getStatInformation(self) -> str:
        """
            Get statistical coefficient information.
        
            Returns:
                statistical coefficient information
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaVariableDragCoef.toString` in
                class :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaVariableDragCoef`
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.forces.drag")``.

    AbstractStelaDragCoef: typing.Type[AbstractStelaDragCoef]
    StelaAeroModel: typing.Type[StelaAeroModel]
    StelaAtmosphericDrag: typing.Type[StelaAtmosphericDrag]
    StelaConstantDragCoef: typing.Type[StelaConstantDragCoef]
    StelaCookDispersedDragCoef: typing.Type[StelaCookDispersedDragCoef]
    StelaCookDragCoef: typing.Type[StelaCookDragCoef]
    StelaDragCoefInput: typing.Type[StelaDragCoefInput]
    StelaDragCoefType: typing.Type[StelaDragCoefType]
    StelaVariableDispersedDragCoef: typing.Type[StelaVariableDispersedDragCoef]
    StelaVariableDragCoef: typing.Type[StelaVariableDragCoef]
    StelaVariableDragCoefReader: typing.Type[StelaVariableDragCoefReader]
