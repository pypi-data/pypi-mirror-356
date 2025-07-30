
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly.properties
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.forces.maneuvers
import fr.cnes.sirius.patrius.propagation
import typing



class ImpulseParKepManeuver:
    """
    public interface ImpulseParKepManeuver
    
        Generic interface which offers an unique service to compute a DV from a SpacecraftState object.
    
        Since:
            4.4
    """
    def computeDV(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...

class ImpulseDaManeuver(fr.cnes.sirius.patrius.forces.maneuvers.ImpulseManeuver, ImpulseParKepManeuver):
    """
    public class ImpulseDaManeuver extends :class:`~fr.cnes.sirius.patrius.forces.maneuvers.ImpulseManeuver` implements :class:`~fr.cnes.sirius.patrius.forces.maneuvers.orbman.ImpulseParKepManeuver`
    
        Class defining an impulsive maneuver with a semi-major axis increment as input.
    
        Since:
            4.4
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, double: float, double2: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, string: str): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, double: float, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty): ...
    def computeDV(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None:
        """
            Method to compute the DV thanks to Keplerian parameters included in the Spacecraft state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.maneuvers.orbman.ImpulseParKepManeuver.computeDV` in
                interface :class:`~fr.cnes.sirius.patrius.forces.maneuvers.orbman.ImpulseParKepManeuver`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): S/C state
        
        
        """
        ...
    def getDa(self) -> float:
        """
            Getter for semi-major axis increment.
        
            Returns:
                semi-major axis increment
        
        
        """
        ...
    def resetState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...

class ImpulseDeManeuver(fr.cnes.sirius.patrius.forces.maneuvers.ImpulseManeuver, ImpulseParKepManeuver):
    """
    public class ImpulseDeManeuver extends :class:`~fr.cnes.sirius.patrius.forces.maneuvers.ImpulseManeuver` implements :class:`~fr.cnes.sirius.patrius.forces.maneuvers.orbman.ImpulseParKepManeuver`
    
        Class defining an impulsive maneuver with an eccentricity and a semi major axis increment as input.
    
        Since:
            4.4
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, double: float, double2: float, double3: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, string: str, boolean: bool): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, double: float, double2: float, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, boolean: bool): ...
    def computeDV(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    def getDa(self) -> float:
        """
            Getter for semi-major axis increment.
        
            Returns:
                semi-major axis increment
        
        
        """
        ...
    def getDe(self) -> float:
        """
            Getter for eccentricity axis increment.
        
            Returns:
                eccentricity axis increment
        
        
        """
        ...
    def resetState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...

class ImpulseDiManeuver(fr.cnes.sirius.patrius.forces.maneuvers.ImpulseManeuver, ImpulseParKepManeuver):
    """
    public class ImpulseDiManeuver extends :class:`~fr.cnes.sirius.patrius.forces.maneuvers.ImpulseManeuver` implements :class:`~fr.cnes.sirius.patrius.forces.maneuvers.orbman.ImpulseParKepManeuver`
    
        Class defining an impulsive maneuver with a inclination and eventually a semi major axis increment as input.
    
        Since:
            4.4
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, double: float, double2: float, double3: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, string: str, boolean: bool): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, double: float, double2: float, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, boolean: bool): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, double: float, double2: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, string: str, boolean: bool): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, double: float, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, boolean: bool): ...
    def computeDV(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    def getDa(self) -> float:
        """
            Getter for semi-major axis increment.
        
            Returns:
                semi-major axis increment
        
        
        """
        ...
    def getDi(self) -> float:
        """
            Getter for inclination increment.
        
            Returns:
                inclination increment
        
        
        """
        ...
    def resetState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.maneuvers.orbman")``.

    ImpulseDaManeuver: typing.Type[ImpulseDaManeuver]
    ImpulseDeManeuver: typing.Type[ImpulseDeManeuver]
    ImpulseDiManeuver: typing.Type[ImpulseDiManeuver]
    ImpulseParKepManeuver: typing.Type[ImpulseParKepManeuver]
