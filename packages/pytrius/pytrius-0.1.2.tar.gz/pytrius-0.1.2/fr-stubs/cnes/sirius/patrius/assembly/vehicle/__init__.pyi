
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly
import fr.cnes.sirius.patrius.assembly.models.aerocoeffs
import fr.cnes.sirius.patrius.assembly.properties
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import java.io
import typing



class AerodynamicProperties(java.io.Serializable):
    """
    public class AerodynamicProperties extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class defines an aerodynamic property to be applyied to aerodynamic parts of a vehicle (PATRIUS assembly). It has a
        dual nature, actually it is either an :class:`~fr.cnes.sirius.patrius.assembly.properties.AeroGlobalProperty` or an
        :class:`~fr.cnes.sirius.patrius.assembly.properties.AeroSphereProperty` depending on the constructor used.
    
        Since:
            4.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, vehicleSurfaceModel: 'VehicleSurfaceModel', double: float, double2: float): ...
    @typing.overload
    def __init__(self, sphere: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Sphere, double: float): ...
    @typing.overload
    def __init__(self, sphere: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Sphere, aerodynamicCoefficient: fr.cnes.sirius.patrius.assembly.models.aerocoeffs.AerodynamicCoefficient, aerodynamicCoefficient2: fr.cnes.sirius.patrius.assembly.models.aerocoeffs.AerodynamicCoefficient): ...
    def getConstantDragCoef(self) -> float: ...
    def getConstantLiftCoef(self) -> float: ...
    def getDragCoef(self) -> fr.cnes.sirius.patrius.assembly.models.aerocoeffs.AerodynamicCoefficient:
        """
            Get the drag coefficient.
        
            Returns:
                the drag coefficient
        
        
        """
        ...
    def getFunctionType(self) -> fr.cnes.sirius.patrius.assembly.models.aerocoeffs.AerodynamicCoefficientType: ...
    def getLiftCoef(self) -> fr.cnes.sirius.patrius.assembly.models.aerocoeffs.AerodynamicCoefficient:
        """
            Get the lift coefficient.
        
            Returns:
                the lift coefficient
        
        
        """
        ...
    def getVehicleSurfaceModel(self) -> 'VehicleSurfaceModel':
        """
            Get the surface model.
        
            Returns:
                the surface model
        
        
        """
        ...
    def setAerodynamicProperties(self, assemblyBuilder: fr.cnes.sirius.patrius.assembly.AssemblyBuilder, string: str, double: float) -> None:
        """
            Set aerodynamic property to a part (it modifies vehicle surface model as a function of the multplicative factor).
        
            Parameters:
                builder (:class:`~fr.cnes.sirius.patrius.assembly.AssemblyBuilder`): assembly builder
                mainPartName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): main part name
                multiplicativeFactor (double): the multiplicative factor (applied to the reference surface)
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class RadiativeProperties(java.io.Serializable):
    """
    public class RadiativeProperties extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class to define vehicle radiative properties.
    
        Since:
            4.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, radiativeProperty: fr.cnes.sirius.patrius.assembly.properties.RadiativeProperty, radiativeIRProperty: fr.cnes.sirius.patrius.assembly.properties.RadiativeIRProperty, vehicleSurfaceModel: 'VehicleSurfaceModel'): ...
    @staticmethod
    def coeffsSumOne(double: float, double2: float, double3: float) -> bool:
        """
            Function to check if the absortion, specular and difusse coefficients sum is one.
        
            Parameters:
                ka (double): absortion coefficient
                ks (double): specular coefficient
                kd (double): diffuse coefficient
        
            Returns:
                true if they sum one, false otherwise.
        
        
        """
        ...
    def getRadiativeIRProperty(self) -> fr.cnes.sirius.patrius.assembly.properties.RadiativeIRProperty:
        """
            Get infrared radiative properties.
        
            Returns:
                the radiativeIRProperty (null if not provided)
        
        
        """
        ...
    def getRadiativeProperty(self) -> fr.cnes.sirius.patrius.assembly.properties.RadiativeProperty:
        """
            Get radiative properties.
        
            Returns:
                the radiativeProperty (null if not provided)
        
        
        """
        ...
    def getVehicleSurfaceModel(self) -> 'VehicleSurfaceModel':
        """
            Get vehicle surface model.
        
            Returns:
                the vehicleSurfaceModel
        
        
        """
        ...
    def setRadiativeProperties(self, assemblyBuilder: fr.cnes.sirius.patrius.assembly.AssemblyBuilder, string: str, double: float) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class VehicleSurfaceModel(fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, java.io.Serializable):
    """
    public class VehicleSurfaceModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Vehicle surface model class. It defines a derivative function parameterizable where the variable is the spacecraft state
        and the function is the cross section surface (including solar panels) as seen from the velocity vector direction. It
        includes a multiplicative factor as a parameter.
    
        Since:
            4.1
    
        Also see:
            :meth:`~serialized`
    """
    MULTIPLICATIVE_FACTOR: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` MULTIPLICATIVE_FACTOR
    
        Multiplicative factor parameter name.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable]): ...
    @typing.overload
    def __init__(self, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable], rightParallelepiped: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.RightParallelepiped): ...
    @typing.overload
    def __init__(self, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable], rightParallelepiped: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.RightParallelepiped, double: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getCrossSection(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the cross section from the direction defined by a Vector3D.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider.getCrossSection` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector
        
            Returns:
                the cross section
        
        
        """
        ...
    def getMainPartShape(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider:
        """
            Get the main part vehicle shape.
        
            Returns:
                the shape
        
        
        """
        ...
    def getMultiplicativeFactor(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Get the multiplicative factor applied to the reference surface as a parameter.
        
            Returns:
                the multiplicative factor parameter
        
        
        """
        ...
    def getSolarPanelsShape(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.RightParallelepiped:
        """
            Get solar panels. If no solar panels are defined, null is returned.
        
            Returns:
                the solar panels
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def setMultiplicativeFactor(self, double: float) -> None:
        """
            Set the multiplicative factor applied to the reference surface.
        
            Parameters:
                multiplicativeFactorIn (double): the multiplicative factor
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.assembly.vehicle")``.

    AerodynamicProperties: typing.Type[AerodynamicProperties]
    RadiativeProperties: typing.Type[RadiativeProperties]
    VehicleSurfaceModel: typing.Type[VehicleSurfaceModel]
