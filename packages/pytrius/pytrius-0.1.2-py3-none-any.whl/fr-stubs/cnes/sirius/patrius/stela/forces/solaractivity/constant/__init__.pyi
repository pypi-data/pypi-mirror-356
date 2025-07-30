
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.forces.atmospheres.solarActivity
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.stela.forces.solaractivity
import fr.cnes.sirius.patrius.stela.spaceobject
import fr.cnes.sirius.patrius.time
import typing



class StelaConstantSolarActivity(fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.ConstantSolarActivity, fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity):
    """
    public class StelaConstantSolarActivity extends :class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.ConstantSolarActivity` implements :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity`
    
        Constant model of solar activity.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float): ...
    def copy(self) -> 'StelaConstantSolarActivity': ...
    def getSolActType(self) -> fr.cnes.sirius.patrius.stela.forces.solaractivity.StelaSolarActivityType:
        """
            Get solar activity type. It can be either constant or variable.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity.getSolActType` in
                interface :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity`
        
            Returns:
                solar activity type
        
        
        """
        ...
    def getSolarActivity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]: ...

class StelaLOSConstantSolarActivity(fr.cnes.sirius.patrius.stela.forces.solaractivity.AbstractStelaSolarActivity):
    """
    public class StelaLOSConstantSolarActivity extends :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.AbstractStelaSolarActivity`
    
        Mean constant model of solar activity. This solar activity uses calculated constant F107 depending on the orbit and the
        ballistic coefficient (see User guide for more information). This computation is performed using the method
        :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.constant.StelaLOSConstantSolarActivity.updateF107`. Resulting
        value is stored in
        :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.constant.StelaLOSConstantSolarActivity.losF107`.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def computeLosF107(self, stelaSpaceObject: fr.cnes.sirius.patrius.stela.spaceobject.StelaSpaceObject, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...
    def copy(self) -> 'StelaLOSConstantSolarActivity': ...
    def getAp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get Geomagnetic activity at a specified date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                geomagnetic activity
        
        
        """
        ...
    def getInstantFluxValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get Solar activity flux at a specified date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                solar activity daily flux
        
        
        """
        ...
    def getSolarActivity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]:
        """
            Get Solar activity coefficients at a specified date, in the following order: daily flux, mean flux, Ap1, Ap2, Ap3, Ap4,
            Ap5, Ap6, Ap7.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                solar activity coefficients (solar flux and geomagnetic activity)
        
        
        """
        ...
    def toString(self) -> str:
        """
            Get information of Solar Activity.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity.toString` in
                interface :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity`
        
            Overrides:
                 in class 
        
            Returns:
                a string with all solar activity
        
        
        """
        ...
    def updateF107(self, stelaSpaceObject: fr.cnes.sirius.patrius.stela.spaceobject.StelaSpaceObject, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.forces.solaractivity.constant")``.

    StelaConstantSolarActivity: typing.Type[StelaConstantSolarActivity]
    StelaLOSConstantSolarActivity: typing.Type[StelaLOSConstantSolarActivity]
