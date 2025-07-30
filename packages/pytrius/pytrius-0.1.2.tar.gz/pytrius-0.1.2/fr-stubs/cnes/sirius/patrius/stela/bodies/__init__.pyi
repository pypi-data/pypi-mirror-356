
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.time
import java.io
import typing



class EarthRotation:
    """
    public final class EarthRotation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class represents the Earth rotation.
    
    
        It is used to compute the Earth rotation rate when computing the atmospheric drag acceleration.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaAeroModel`
    """
    @staticmethod
    def getERA(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the Earth Rotation Angle (ERA) using Capitaine model (2000).
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                Earth Rotation Angle (rad)
        
        
        """
        ...
    @staticmethod
    def getERADerivative(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the Earth Rotation Angle (ERA) derivative.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                the Earth Rotation Angle derivative (rad/s)
        
        
        """
        ...
    @staticmethod
    def getGMST(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute Greenwich Mean Sideral Time.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                Greenwich Mean Sideral Time (rad)
        
        
        """
        ...
    @staticmethod
    def getGMSTDerivative(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute Greenwich Mean Sideral Time derivative.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                Greenwich Mean Sideral Time derivative (rad/s)
        
        
        """
        ...

class GeodPosition(java.io.Serializable):
    """
    public final class GeodPosition extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class representing the Geodetic representation of a position.
    
    
        It is used to compute the spacecraft Geodetic latitude when computing the atmospheric drag acceleration.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.stela.forces.drag.StelaAeroModel`, :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float): ...
    def getGeodeticAltitude(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float: ...
    def getGeodeticLatitude(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float: ...
    def getGeodeticLongitude(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getTloc(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute the local solar time at a given date.
        
            Parameters:
                position (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the spacecraft position
                positionSun (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the Sun position
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the date
        
            Returns:
                the local solar time
        
        
        """
        ...

class MeeusMoonStela(fr.cnes.sirius.patrius.bodies.AbstractIAUCelestialBody):
    """
    public class MeeusMoonStela extends :class:`~fr.cnes.sirius.patrius.bodies.AbstractIAUCelestialBody`
    
    
        This class implements the Moon ephemerides according to the algorithm of Meeus, it only provides the position. Note that
        it is not possible to build this Moon from the CelestialBodyFactory.
        See Stela's implementation of this model
    
        This class contains methods to store :code:`#getInertialFrame(IAUPoleModelType.CONSTANT)` to integration frame (CIRF)
        transform to speed up computation during the integration process. As this transform varies slowly through time, it has
        been demonstrated it is not necessary to recompute it every time. Warning: these methods should not be used in a
        stand-alone use (unless you known what you are doing). There are two methods:
    
          - :code:`#updateTransform(AbsoluteDate, Frame)`: store transform from :code:`#getInertialFrame(IAUPoleModelType.CONSTANT)`
            to provided frame at provided date.
          - :code:`#resetTransform()`: reset stored transform
    
    
        Note that pole information allowing to define inertially-centered frame and rotating frame are defined in
        :class:`~fr.cnes.sirius.patrius.bodies.IAUPoleFactory` since Meeus model does not provide the information.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float): ...
    def toString(self) -> str:
        """
            Returns a string representation of the celestial point and its attributes.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.bodies.CelestialPoint.toString` in
                interface :class:`~fr.cnes.sirius.patrius.bodies.CelestialPoint`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.bodies.AbstractIAUCelestialBody.toString` in
                class :class:`~fr.cnes.sirius.patrius.bodies.AbstractIAUCelestialBody`
        
            Returns:
                a string representation of the celestial point and its attributes
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.bodies")``.

    EarthRotation: typing.Type[EarthRotation]
    GeodPosition: typing.Type[GeodPosition]
    MeeusMoonStela: typing.Type[MeeusMoonStela]
