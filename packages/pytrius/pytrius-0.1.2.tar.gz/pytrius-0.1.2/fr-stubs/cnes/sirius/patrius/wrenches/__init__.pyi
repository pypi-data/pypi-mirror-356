
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly.models
import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.forces
import fr.cnes.sirius.patrius.forces.atmospheres
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.models.earth
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import java.io
import jpype
import typing



class DragWrenchSensitive:
    """
    public interface DragWrenchSensitive
    
        Interface to represent solar drag wrench sensitive vehicles
    
        Since:
            2.1
    """
    @typing.overload
    def dragWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> 'Wrench': ...
    @typing.overload
    def dragWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> 'Wrench': ...

class RadiationWrenchSensitive(java.io.Serializable):
    """
    public interface RadiationWrenchSensitive extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface to represent solar radiation wrench sensitive vehicles
    
        Since:
            2.1
    """
    @typing.overload
    def radiationWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> 'Wrench': ...
    @typing.overload
    def radiationWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> 'Wrench': ...

class Wrench:
    """
    public class Wrench extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class represents a wrench.
    
        Since:
            1.3
    """
    ZERO: typing.ClassVar['Wrench'] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.wrenches.Wrench` ZERO
    
        Zero wrench.
    
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    def add(self, wrench: 'Wrench') -> 'Wrench':
        """
            Sum of two wrenches.
        
            Parameters:
                wrench (:class:`~fr.cnes.sirius.patrius.wrenches.Wrench`): wrench to add
        
            Returns:
                sum of wrenches
        
        
        """
        ...
    @typing.overload
    def displace(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> 'Wrench':
        """
            Displace current wrench.
        
            Parameters:
                newOrigin (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): new origin
        
            Returns:
                displaced wrench
        
            Displace current wrench.
        
            Parameters:
                wrench (:class:`~fr.cnes.sirius.patrius.wrenches.Wrench`): the wrench to displace
                newOrigin (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): new origin
        
            Returns:
                displaced wrench
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def displace(wrench: 'Wrench', vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> 'Wrench': ...
    def getForce(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
        
            Returns:
                the force
        
        
        """
        ...
    def getOrigin(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
        
            Returns:
                the origin of the torque
        
        
        """
        ...
    @typing.overload
    def getTorque(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
        
            Returns:
                the torque
        
        """
        ...
    @typing.overload
    def getTorque(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the torque expressed in another point.
        
            Parameters:
                origin (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): new origin for torque expression
        
            Returns:
                the torque expressed in another point
        
        
        """
        ...
    def getWrench(self) -> typing.MutableSequence[float]:
        """
            Get a double[] representation of this wrench.
        
            .. code-block: java
            
            
             data = wrench.getWrench();
             data =
             {o :sub:`x` , o :sub:`y` , o :sub:`z` ,
             f :sub:`x` , f :sub:`y` , f :sub:`z` ,
             t :sub:`x` , t :sub:`y` , t :sub:`z` }
             
            where o is the origin, f the force and t the torque.
        
            Returns:
                wrench as a double[].
        
        
        """
        ...
    @staticmethod
    def sum(wrench: 'Wrench', wrench2: 'Wrench') -> 'Wrench':
        """
            Sum of two wrenches.
        
            Parameters:
                wrench1 (:class:`~fr.cnes.sirius.patrius.wrenches.Wrench`): first wrench
                wrench2 (:class:`~fr.cnes.sirius.patrius.wrenches.Wrench`): second wrench
        
            Returns:
                sum of wrenches
        
        
        """
        ...
    def toString(self) -> str:
        """
            Get a String representation for this Wrench.
        
            Overrides:
                 in class 
        
            Returns:
                a representation for this wrench
        
        
        """
        ...

class WrenchModel:
    """
    public interface WrenchModel
    
        Interface to represents wrench models.
    
        Since:
            2.1
    """
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> Wrench: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> Wrench: ...

class DragWrench(WrenchModel):
    """
    public class DragWrench extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.wrenches.WrenchModel`
    
        This class represents a drag wrench model. It requires a spacecraft capable of computing the wrench caused by drag
        forces.
    
        Since:
            2.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.wrenches.DragWrenchSensitive`
    """
    def __init__(self, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, dragWrenchSensitive: DragWrenchSensitive): ...
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> Wrench: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> Wrench: ...

class GenericWrenchModel(WrenchModel):
    """
    public class GenericWrenchModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.wrenches.WrenchModel`
    
        This class represents a generic wrench model.
    
        Since:
            2.1
    """
    def __init__(self, forceModel: fr.cnes.sirius.patrius.forces.ForceModel, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> Wrench: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> Wrench: ...

class GravitationalAttractionWrench(WrenchModel):
    """
    public class GravitationalAttractionWrench extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.wrenches.WrenchModel`
    
        This class represents a gravitational attraction wrench
    
        Since:
            $$
    """
    def __init__(self, iInertiaModel: fr.cnes.sirius.patrius.assembly.models.IInertiaModel, double: float): ...
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> Wrench: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> Wrench: ...

class MagneticWrench(WrenchModel):
    """
    public class MagneticWrench extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.wrenches.WrenchModel`
    
        This class represents a wrench model
    
        Since:
            2.1
    """
    def __init__(self, magneticMomentProvider: typing.Union[fr.cnes.sirius.patrius.assembly.models.MagneticMomentProvider, typing.Callable], geoMagneticField: fr.cnes.sirius.patrius.models.earth.GeoMagneticField): ...
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> Wrench: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> Wrench: ...

class SolarRadiationWrench(fr.cnes.sirius.patrius.math.parameter.Parameterizable, WrenchModel):
    """
    public class SolarRadiationWrench extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.wrenches.WrenchModel`
    
        This class represents a solar radiation wrench model. It requires a spacecraft capable of computing the wrench caused by
        solar radiation pressure.
    
        Since:
            2.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.wrenches.RadiationWrenchSensitive`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, radiationWrenchSensitive: RadiationWrenchSensitive): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, radiationWrenchSensitive: RadiationWrenchSensitive): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, bodyShape: fr.cnes.sirius.patrius.bodies.BodyShape, radiationWrenchSensitive: RadiationWrenchSensitive): ...
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeTorque(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> Wrench: ...
    @typing.overload
    def computeWrench(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> Wrench: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.wrenches")``.

    DragWrench: typing.Type[DragWrench]
    DragWrenchSensitive: typing.Type[DragWrenchSensitive]
    GenericWrenchModel: typing.Type[GenericWrenchModel]
    GravitationalAttractionWrench: typing.Type[GravitationalAttractionWrench]
    MagneticWrench: typing.Type[MagneticWrench]
    RadiationWrenchSensitive: typing.Type[RadiationWrenchSensitive]
    SolarRadiationWrench: typing.Type[SolarRadiationWrench]
    Wrench: typing.Type[Wrench]
    WrenchModel: typing.Type[WrenchModel]
