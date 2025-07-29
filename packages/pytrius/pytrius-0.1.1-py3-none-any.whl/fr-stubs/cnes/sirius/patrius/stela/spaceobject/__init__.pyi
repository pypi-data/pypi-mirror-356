
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.stela.forces.drag
import java.io
import typing



class StelaSpaceObject(java.io.Serializable):
    """
    public class StelaSpaceObject extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class represents the space object used in STELA.
    
    
        In the future, should be replaced with the :class:`~fr.cnes.sirius.patrius.stela.StelaSpacecraftFactory`
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str, double: float, double2: float, double3: float, double4: float, abstractStelaDragCoef: fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef): ...
    def copy(self) -> 'StelaSpaceObject': ...
    def getDragArea(self) -> float:
        """
            Gets the drag area of the object.
        
            Returns:
                the drag area as a double.
        
        
        """
        ...
    def getDragCoef(self) -> fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef:
        """
            Gets the drag coefficient associated with the object.
        
            Returns:
                the drag coefficient as an instance of AbstractStelaDragCoef.
        
        
        """
        ...
    def getInformation(self, boolean: bool, boolean2: bool) -> str: ...
    def getMass(self) -> float:
        """
            Gets the mass of the object.
        
            Returns:
                the mass of the object as a double.
        
        
        """
        ...
    def getName(self) -> str:
        """
            Gets the name of the object.
        
            Returns:
                the name of the object as a String.
        
        
        """
        ...
    def getReflectingArea(self) -> float:
        """
            Gets the reflecting area of the object.
        
            Returns:
                the reflecting area as a double.
        
        
        """
        ...
    def getReflectionCoef(self) -> float:
        """
            Gets the reflection coefficient of the object.
        
            Returns:
                the reflection coefficient as a double.
        
        
        """
        ...
    def reSetReflectivityCoef(self) -> None:
        """
            Reset the reflectivity Coefficient of SpaceObject to
            :meth:`~fr.cnes.sirius.patrius.utils.Constants.STELA_SPACE_OBJECT_REFLECT_COEF`.
        
        """
        ...
    def setDragCoef(self, abstractStelaDragCoef: fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef) -> None:
        """
            Sets the drag coefficient associated with the object.
        
            Parameters:
                dragCoef (:class:`~fr.cnes.sirius.patrius.stela.forces.drag.AbstractStelaDragCoef`): the new drag coefficient
        
        
        """
        ...
    def setMass(self, double: float) -> None:
        """
            Sets the mass of the object.
        
            Parameters:
                mass (double): the new mass of the object
        
        
        """
        ...
    def setMeanArea(self, double: float) -> None:
        """
            Sets the mean drag area of the object.
        
            Parameters:
                dragArea (`Double <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>`): the new drag area
        
        
        """
        ...
    def setName(self, string: str) -> None:
        """
            Sets the name of the object. Replaces any occurrence of "∞" with "Infinity".
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the new name of the object
        
        
        """
        ...
    def setReflectingArea(self, double: float) -> None:
        """
            Sets the reflecting area of the object.
        
            Parameters:
                reflectingArea (`Double <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>`): the new reflecting area
        
        
        """
        ...
    def setReflectionCoef(self, double: float) -> None:
        """
            Sets the reflection coefficient of the object. Logs the new reflection coefficient value.
        
            Parameters:
                reflectivityCoefficient (`Double <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>`): the new reflection coefficient
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.spaceobject")``.

    StelaSpaceObject: typing.Type[StelaSpaceObject]
