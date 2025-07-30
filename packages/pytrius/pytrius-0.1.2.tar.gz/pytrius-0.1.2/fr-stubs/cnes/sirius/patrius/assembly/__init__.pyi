
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly.models
import fr.cnes.sirius.patrius.assembly.models.aerocoeffs
import fr.cnes.sirius.patrius.assembly.properties
import fr.cnes.sirius.patrius.assembly.properties.features
import fr.cnes.sirius.patrius.assembly.vehicle
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.frames.transformations
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import typing



class Assembly(java.io.Serializable):
    """
    public class Assembly extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class describes an assembly by all its sub parts.
    
        This assembly shall be created and modified using the associated builder. Then user can access to each part by its name
        and get its properties. This assembly does not include the physical models : models shall be created in separated
        classes using this one.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.AssemblyBuilder`, :class:`~fr.cnes.sirius.patrius.assembly.MainPart`,
            :class:`~fr.cnes.sirius.patrius.assembly.Part`, :meth:`~serialized`
    """
    FRAME: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` FRAME
    
        String Frame
    
        Also see:
            :meth:`~constant`
    
    
    """
    def addMainPart(self, mainPart: 'MainPart') -> None:
        """
            Adds the main part to the assembly.
        
            Parameters:
                part (:class:`~fr.cnes.sirius.patrius.assembly.MainPart`): the main part to add
        
            Raises:
                : if the main part is already created
        
        
        """
        ...
    def addPart(self, iPart: 'IPart') -> None:
        """
            Adds a part to the assembly.
        
            Parameters:
                part (:class:`~fr.cnes.sirius.patrius.assembly.IPart`): the part to add to the assembly
        
            Raises:
                : if a part with this name already exists or if the main part has not been created yet.
        
        
        """
        ...
    def getAllPartsNames(self) -> java.util.Set[str]: ...
    def getMainPart(self) -> 'MainPart':
        """
        
            Returns:
                the main part
        
        
        """
        ...
    def getPart(self, string: str) -> 'IPart':
        """
            Returns the part whose name is specified.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the part
        
            Returns:
                the part whose the name is specified
        
            Raises:
                : if no part has this name
        
        
        """
        ...
    def getParts(self) -> java.util.Map[str, 'IPart']: ...
    @typing.overload
    def initMainPartFrame(self, updatableFrame: fr.cnes.sirius.patrius.frames.UpdatableFrame) -> None: ...
    @typing.overload
    def initMainPartFrame(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    def removePart(self, string: str) -> None:
        """
            Removes a part from the assembly. All the children parts of the one removed will be removed too : they won't have no
            parent frame.
        
            boolean :meth:`~fr.cnes.sirius.patrius.assembly.Assembly.hasMobileParts` is not updated for simplicity (this situation
            is not common and is still perfectly valid).
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the part to remove
        
            Raises:
                : if no part has this name
        
        
        """
        ...
    @typing.overload
    def updateMainPartFrame(self, transform: fr.cnes.sirius.patrius.frames.transformations.Transform) -> None: ...
    @typing.overload
    def updateMainPartFrame(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...

class AssemblyBuilder:
    """
    public class AssemblyBuilder extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
    
        - This class is the builder that shall be needed to create an instance of the assembly.
    
        - Its purpose is to simplify the building process of the assembly. It provides the method that allow the user to add a
        part to the assembly, and then to add properties to each of the parts.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.Assembly`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, assembly: Assembly): ...
    def addMainPart(self, string: str) -> None:
        """
            Adds the main part to the assembly : shall be done before adding any other part.
        
            Parameters:
                mainBodyName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the part
        
        
        """
        ...
    @typing.overload
    def addPart(self, string: str, string2: str, transform: fr.cnes.sirius.patrius.frames.transformations.Transform) -> None:
        """
            This method adds a new part to the currently built assembly. The new part is defined relatively to its parent part with
            a transform law.
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the part
                parentPartName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the parent of the part
                transformStateProvider (:class:`~fr.cnes.sirius.patrius.frames.transformations.TransformStateProvider`): the transformation law that defines the new part's frame wrt the parent frame
        
            Raises:
                : if a part with this name already exists, if the main part has not been created yet or if the parent part does not exist
                    (no part with this name).
        
            This method adds a new part to the currently built assembly, defining its new frame by a Transform object.
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the part
                parentPartName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the parent of the part
                transform (:class:`~fr.cnes.sirius.patrius.frames.transformations.Transform`): the transformation law that defines the new part's frame
        
            Raises:
                : if a part with this name already exists, if the main part has not been created yet or if the parent part does not exist
                    (no part with this name).
        
            This method adds a new part to the currently built assembly. Its frame is defined by a translation from its parent
            part's frame and then a rotation.
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the part
                parentPartName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the parent of the part
                translation (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the translation
                rotation (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation`): the rotation
        
        
        """
        ...
    @typing.overload
    def addPart(self, string: str, string2: str, transformStateProvider: typing.Union[fr.cnes.sirius.patrius.frames.transformations.TransformStateProvider, typing.Callable]) -> None: ...
    @typing.overload
    def addPart(self, string: str, string2: str, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation) -> None: ...
    def addProperty(self, iPartProperty: typing.Union['IPartProperty', typing.Callable], string: str) -> None:
        """
            Adds a property of any type to a part of the assembly.
        
            Parameters:
                property (:class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`): the property to add
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the part to which the property must be added
        
            Raises:
                : if the part already contains a property of this type or if the assembly contains no part of this name.
        
        
        """
        ...
    def getPart(self, string: str) -> 'IPart':
        """
            This method returns the part whose name is given in parameter.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the part
        
            Returns:
                the part
        
        
        """
        ...
    @typing.overload
    def initMainPartFrame(self, updatableFrame: fr.cnes.sirius.patrius.frames.UpdatableFrame) -> None: ...
    @typing.overload
    def initMainPartFrame(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    def removePart(self, string: str) -> None:
        """
            This method removes one part from the assembly.
        
            Parameters:
                partName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the part to remove.
        
        
        """
        ...
    def returnAssembly(self) -> Assembly:
        """
            This method returns the assembly when the user wants to get the instance of the assembly that has been built so far.
        
            Returns:
                the assembly instance
        
        
        """
        ...

class IPart(java.io.Serializable):
    """
    public interface IPart extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        -Interface for the assembly's parts.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.Part`, :class:`~fr.cnes.sirius.patrius.assembly.MainPart`
    """
    def addProperty(self, iPartProperty: typing.Union['IPartProperty', typing.Callable]) -> None:
        """
            Adds a property to the part.
        
            Parameters:
                property (:class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`): the property
        
        
        """
        ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
        
            Returns:
                the associated frame
        
        
        """
        ...
    def getName(self) -> str:
        """
        
            Returns:
                the name of the part
        
        
        """
        ...
    def getParent(self) -> 'IPart':
        """
        
            Returns:
                the parent part
        
        
        """
        ...
    def getPartLevel(self) -> int:
        """
        
            Returns:
                the level of the part in the tree
        
        
        """
        ...
    def getProperty(self, propertyType: 'PropertyType') -> 'IPartProperty':
        """
            Returns a property of the part : if in this part, one exists of the given type.
        
            Parameters:
                propertyType (:class:`~fr.cnes.sirius.patrius.assembly.PropertyType`): the type of the wanted property
        
            Returns:
                the property
        
        
        """
        ...
    def hasProperty(self, propertyType: 'PropertyType') -> bool:
        """
            Checks if a property of the given type exists in this part.
        
            Parameters:
                propertyType (:class:`~fr.cnes.sirius.patrius.assembly.PropertyType`): the type
        
            Returns:
                true if the property exists
        
        
        """
        ...
    @typing.overload
    def updateFrame(self, transform: fr.cnes.sirius.patrius.frames.transformations.Transform) -> None:
        """
            Update frame at provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
        void updateFrame(:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState` s) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Update frame with provided spacecraft state.
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: thrown if update fails
        
        
        """
        ...
    @typing.overload
    def updateFrame(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    @typing.overload
    def updateFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class IPartProperty(java.io.Serializable):
    """
    public interface IPartProperty extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for the assembly's part properties.
    
        Since:
            1.1
    """
    def getType(self) -> 'PropertyType':
        """
            Get the type of the property.
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class PropertyType(java.lang.Enum['PropertyType']):
    """
    public enum PropertyType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.assembly.PropertyType`>
    
        This enumeration lists the possible types of properties that can be added to a part.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    """
    GEOMETRY: typing.ClassVar['PropertyType'] = ...
    CROSS_SECTION: typing.ClassVar['PropertyType'] = ...
    RADIATIVE_CROSS_SECTION: typing.ClassVar['PropertyType'] = ...
    RADIATIVE_FACET: typing.ClassVar['PropertyType'] = ...
    RADIATIVE: typing.ClassVar['PropertyType'] = ...
    RADIATIVEIR: typing.ClassVar['PropertyType'] = ...
    AERO_FACET: typing.ClassVar['PropertyType'] = ...
    AERO_CROSS_SECTION: typing.ClassVar['PropertyType'] = ...
    MASS: typing.ClassVar['PropertyType'] = ...
    INERTIA: typing.ClassVar['PropertyType'] = ...
    SENSOR: typing.ClassVar['PropertyType'] = ...
    RF: typing.ClassVar['PropertyType'] = ...
    DRAG: typing.ClassVar['PropertyType'] = ...
    RADIATION_APPLICATION_POINT: typing.ClassVar['PropertyType'] = ...
    AERO_APPLICATION_POINT: typing.ClassVar['PropertyType'] = ...
    AERO_GLOBAL: typing.ClassVar['PropertyType'] = ...
    WALL: typing.ClassVar['PropertyType'] = ...
    TANK: typing.ClassVar['PropertyType'] = ...
    PROPULSIVE: typing.ClassVar['PropertyType'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'PropertyType':
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
    def values() -> typing.MutableSequence['PropertyType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (PropertyType c : PropertyType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class Vehicle(java.io.Serializable):
    """
    public class Vehicle extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Vehicle class: it represent a classic satellite: main body + solar panels. This satellite can have tanks, engines and
        masses. To build a more complex satellite (with sensors, etc.), use :class:`~fr.cnes.sirius.patrius.assembly.Assembly`
        class.
    
        Since:
            4.0
    
        Also see:
            :meth:`~serialized`
    """
    MAIN_SHAPE: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` MAIN_SHAPE
    
        Main shape.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable], list: java.util.List[fr.cnes.sirius.patrius.assembly.properties.features.Facet], massProperty: fr.cnes.sirius.patrius.assembly.properties.MassProperty, aerodynamicProperties: fr.cnes.sirius.patrius.assembly.vehicle.AerodynamicProperties, radiativeProperties: fr.cnes.sirius.patrius.assembly.vehicle.RadiativeProperties, list2: java.util.List[fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty], list3: java.util.List[fr.cnes.sirius.patrius.assembly.properties.TankProperty]): ...
    def addEngine(self, string: str, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty) -> None:
        """
            Add an engine to the vehicle.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): engine name
                engine (:class:`~fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty`): an engine
        
        
        """
        ...
    def addSolarPanel(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float) -> None:
        """
            Add a solar panel to the vehicle.
        
            Parameters:
                normalPanel (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): vector normal to the panel in satellite frame
                areaPanel (double): panel area
        
        
        """
        ...
    def addTank(self, string: str, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty) -> None:
        """
            Add a tank to the vehicle.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): tank name
                tank (:class:`~fr.cnes.sirius.patrius.assembly.properties.TankProperty`): a tank
        
        
        """
        ...
    @typing.overload
    def createAssembly(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> Assembly: ...
    @typing.overload
    def createAssembly(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, double3: float) -> Assembly: ...
    def getAerodynamicProperties(self) -> fr.cnes.sirius.patrius.assembly.vehicle.AerodynamicProperties:
        """
            Get main shape aerodynamic properties.
        
            Returns:
                the main shape aerodynamic properties (null if they were not given)
        
        
        """
        ...
    def getAerodynamicsPropertiesFunction(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction]:
        """
            Returns the aero properties : drag and lift coefficients.
        
            Returns:
                aero properties
        
        
        """
        ...
    def getDryMass(self) -> float:
        """
            Returns dry mass.
        
            Returns:
                dry mass
        
        
        """
        ...
    def getEngine(self, string: str) -> fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty:
        """
            Public method to search the engine object corresponding to the specified name.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of the engine
        
            Returns:
                engine object
        
        
        """
        ...
    def getEngineCount(self) -> int:
        """
        
            Returns:
                the s_engineCount
        
        
        """
        ...
    def getEnginesList(self) -> java.util.List[fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty]: ...
    def getErgolsMass(self) -> float:
        """
            Returns the sum of ergols masses.
        
            Returns:
                total ergol mass
        
        
        """
        ...
    def getMainShape(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider:
        """
            Returns the main shape.
        
            Returns:
                main shape
        
        
        """
        ...
    def getMassProperty(self) -> fr.cnes.sirius.patrius.assembly.properties.MassProperty:
        """
            Get mass property.
        
            Returns:
                the mass property (null if it was not given)
        
        
        """
        ...
    def getRadiativeProperties(self) -> fr.cnes.sirius.patrius.assembly.vehicle.RadiativeProperties:
        """
            Get main shape radiative properties.
        
            Returns:
                the radiative properties (null if they where not given)
        
        
        """
        ...
    def getRadiativePropertiesTab(self) -> typing.MutableSequence[float]:
        """
            Returns the radiative properties : absorption, specular and diffusion coefficient (visible and IR), as an array : [0] :
            absorption coefficient (visible) [1] : specular coefficient (visible) [2] : diffusion coefficient (visible) [3] :
            absorption coefficient (IR) [4] : specular coefficient (IR) [5] : diffusion coefficient (IR)
        
            Returns:
                radiative properties
        
        
        """
        ...
    def getSolarPanelsList(self) -> java.util.List[fr.cnes.sirius.patrius.assembly.properties.features.Facet]: ...
    def getTank(self, string: str) -> fr.cnes.sirius.patrius.assembly.properties.TankProperty:
        """
            Public method to search the tank object corresponding to the specified name.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of the tank
        
            Returns:
                tank object
        
        
        """
        ...
    def getTankCount(self) -> int:
        """
        
            Returns:
                the s_tankCount
        
        
        """
        ...
    def getTanksList(self) -> java.util.List[fr.cnes.sirius.patrius.assembly.properties.TankProperty]: ...
    def getTotalMass(self) -> float:
        """
            Returns total mass : sum of dry mass and ergol mass.
        
            Returns:
                total mass
        
        
        """
        ...
    @typing.overload
    def setAerodynamicsProperties(self, double: float, double2: float) -> None: ...
    @typing.overload
    def setAerodynamicsProperties(self, aerodynamicCoefficient: fr.cnes.sirius.patrius.assembly.models.aerocoeffs.AerodynamicCoefficient, aerodynamicCoefficient2: fr.cnes.sirius.patrius.assembly.models.aerocoeffs.AerodynamicCoefficient) -> None: ...
    def setDryMass(self, double: float) -> None: ...
    def setMainShape(self, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable]) -> None:
        """
            Set the main vehicle shape.
        
            Parameters:
                shape (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider`): main shape
        
        
        """
        ...
    def setRadiativeProperties(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float) -> None: ...

class AbstractPart(IPart):
    """
    public abstract class AbstractPart extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPart`
    
        Abstract part: class gathering all common methods of assmelby parts.
    
        Since:
            4.4
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str, iPart: IPart): ...
    def addProperty(self, iPartProperty: typing.Union[IPartProperty, typing.Callable]) -> None:
        """
            Adds a property to the part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPart.addProperty` in interface :class:`~fr.cnes.sirius.patrius.assembly.IPart`
        
            Parameters:
                property (:class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`): the property
        
        
        """
        ...
    def getName(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPart.getName` in interface :class:`~fr.cnes.sirius.patrius.assembly.IPart`
        
            Returns:
                the name of the part
        
        
        """
        ...
    def getParent(self) -> IPart:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPart.getParent` in interface :class:`~fr.cnes.sirius.patrius.assembly.IPart`
        
            Returns:
                the parent part
        
        
        """
        ...
    def getPartLevel(self) -> int:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPart.getPartLevel` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPart`
        
            Returns:
                the level of the part in the tree
        
        
        """
        ...
    def getProperty(self, propertyType: PropertyType) -> IPartProperty:
        """
            Returns a property of the part : if in this part, one exists of the given type.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPart.getProperty` in interface :class:`~fr.cnes.sirius.patrius.assembly.IPart`
        
            Parameters:
                propertyType (:class:`~fr.cnes.sirius.patrius.assembly.PropertyType`): the type of the wanted property
        
            Returns:
                the property
        
        
        """
        ...
    def hasProperty(self, propertyType: PropertyType) -> bool:
        """
            Checks if a property of the given type exists in this part.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPart.hasProperty` in interface :class:`~fr.cnes.sirius.patrius.assembly.IPart`
        
            Parameters:
                propertyType (:class:`~fr.cnes.sirius.patrius.assembly.PropertyType`): the type
        
            Returns:
                true if the property exists
        
        
        """
        ...

class MainPart(AbstractPart):
    """
    public class MainPart extends :class:`~fr.cnes.sirius.patrius.assembly.AbstractPart`
    
        -Class to manage the assembly's main part.
    
        -Contains the assembly's main frame and the main part's properties.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.IPart`, :meth:`~serialized`
    """
    def __init__(self, string: str): ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
        
            Returns:
                the associated frame
        
        
        """
        ...
    def isLinkedToOrekitTree(self) -> bool:
        """
            Returns true if the part is linked to PATRIUS tree of frames.
        
            Returns:
                true if the assembly is linked to another tree of frames.
        
        
        """
        ...
    def setFrame(self, updatableFrame: fr.cnes.sirius.patrius.frames.UpdatableFrame) -> None:
        """
            Method to modify the frame of the main part.
        
            Parameters:
                frame (:class:`~fr.cnes.sirius.patrius.frames.UpdatableFrame`): the new frame of the main part
        
        
        """
        ...
    @typing.overload
    def updateFrame(self, transform: fr.cnes.sirius.patrius.frames.transformations.Transform) -> None:
        """
            This method implements no action for the main part. Update frame at provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
        
            Parameters:
                transform (:class:`~fr.cnes.sirius.patrius.frames.transformations.Transform`): new transformation to be applied Updates the part's frame with a new definition of its Transform.
        
        public final void updateFrame(:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState` s) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Update frame with provided spacecraft state.
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: thrown if update fails
        
        
        """
        ...
    @typing.overload
    def updateFrame(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    @typing.overload
    def updateFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class MobilePart(AbstractPart):
    """
    public class MobilePart extends :class:`~fr.cnes.sirius.patrius.assembly.AbstractPart`
    
        Mobile part of an assembly.
    
        Since:
            4.4
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str, iPart: IPart, transformStateProvider: typing.Union[fr.cnes.sirius.patrius.frames.transformations.TransformStateProvider, typing.Callable]): ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.UpdatableFrame:
        """
        
            Returns:
                the associated frame
        
        
        """
        ...
    def getTransformProvider(self) -> fr.cnes.sirius.patrius.frames.transformations.TransformStateProvider:
        """
            Returns the transform linking the part to its parent part.
        
            Returns:
                the transform linking the part to its parent part
        
        
        """
        ...
    @typing.overload
    def updateFrame(self, transform: fr.cnes.sirius.patrius.frames.transformations.Transform) -> None:
        """
            Update frame at provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
        public final void updateFrame(:class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` t) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.frames.transformations.Transform`): new transformation to be applied Updates the part's frame with a new definition of its Transform.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if update fails
        
        public final void updateFrame(:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState` s) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Update frame with provided spacecraft state.
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: thrown if update fails
        
        
        """
        ...
    @typing.overload
    def updateFrame(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    @typing.overload
    def updateFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class Part(AbstractPart):
    """
    public class Part extends :class:`~fr.cnes.sirius.patrius.assembly.AbstractPart`
    
    
        -Class to manage the assembly's part (the main part is excluded).
    
        -Contains the part's local frame and properties.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.IPart`, :meth:`~serialized`
    """
    def __init__(self, string: str, iPart: IPart, transform: fr.cnes.sirius.patrius.frames.transformations.Transform): ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.UpdatableFrame:
        """
        
            Returns:
                the associated frame
        
        
        """
        ...
    def getTransform(self) -> fr.cnes.sirius.patrius.frames.transformations.Transform:
        """
            Returns the transform linking the part to its parent part.
        
            Returns:
                the transform linking the part to its parent part
        
        
        """
        ...
    @typing.overload
    def updateFrame(self, transform: fr.cnes.sirius.patrius.frames.transformations.Transform) -> None:
        """
            Update frame at provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Update frame with provided spacecraft state.
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
        public final void updateFrame(:class:`~fr.cnes.sirius.patrius.frames.transformations.Transform` t) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.frames.transformations.Transform`): new transformation to be applied Updates the part's frame with a new definition of its Transform.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if update fails
        
        
        """
        ...
    @typing.overload
    def updateFrame(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    @typing.overload
    def updateFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.assembly")``.

    AbstractPart: typing.Type[AbstractPart]
    Assembly: typing.Type[Assembly]
    AssemblyBuilder: typing.Type[AssemblyBuilder]
    IPart: typing.Type[IPart]
    IPartProperty: typing.Type[IPartProperty]
    MainPart: typing.Type[MainPart]
    MobilePart: typing.Type[MobilePart]
    Part: typing.Type[Part]
    PropertyType: typing.Type[PropertyType]
    Vehicle: typing.Type[Vehicle]
    models: fr.cnes.sirius.patrius.assembly.models.__module_protocol__
    properties: fr.cnes.sirius.patrius.assembly.properties.__module_protocol__
    vehicle: fr.cnes.sirius.patrius.assembly.vehicle.__module_protocol__
