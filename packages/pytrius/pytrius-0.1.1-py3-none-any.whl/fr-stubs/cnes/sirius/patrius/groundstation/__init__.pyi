
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.fieldsofview
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.time
import jpype
import typing



class GeometricStationAntenna(fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider):
    """
    public class GeometricStationAntenna extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
    
        Class representing an a geometric model for a ground station antenna.
    
    
        It is used in reverse station visibility event detection.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.events.detectors.StationToSatMutualVisibilityDetector`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, topocentricFrame: fr.cnes.sirius.patrius.frames.TopocentricFrame, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, topocentricFrame: fr.cnes.sirius.patrius.frames.TopocentricFrame, iFieldOfView: fr.cnes.sirius.patrius.fieldsofview.IFieldOfView): ...
    def getFOV(self) -> fr.cnes.sirius.patrius.fieldsofview.IFieldOfView:
        """
        
            Returns:
                the field of view
        
        
        """
        ...
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.Frame: ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getTopoFrame(self) -> fr.cnes.sirius.patrius.frames.TopocentricFrame:
        """
        
            Returns:
                the station topocentric frame
        
        
        """
        ...

class RFStationAntenna(fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider):
    """
    public class RFStationAntenna extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
    
        This class represents an RF antenna model for a ground station. It is used when calculating the RF link budget.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.models.RFLinkBudgetModel`, :meth:`~serialized`
    """
    def __init__(self, topocentricFrame: fr.cnes.sirius.patrius.frames.TopocentricFrame, double: float, double2: float, double3: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double6: float): ...
    def getAtmosphericLoss(self, double: float) -> float:
        """
            Gets the atmospheric loss using a spline interpolation.
        
        
            The atmospheric loss is a function of the ground station elevation.
        
            Parameters:
                elevation (double): ground station elevation [rad], in the range [-PI/2; PI/2].
        
            Returns:
                the atmospheric loss (iono+tropo+rain) for a given elevation [rad * dB].
        
        
        """
        ...
    def getCombinerLoss(self) -> float:
        """
            Returns loss due to the combiner of the antenna [dB].
        
            Returns:
                the loss due to the combiner of the antenna [dB].
        
        
        """
        ...
    def getEllipticityFactor(self) -> float:
        """
        
            Returns:
                the factor of ellipticity, used to calculate the polarisation losses of the antenna [dB].
        
        
        """
        ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Returns ground station topocentric frame.
        
            Returns:
                ground station topocentric frame.
        
        
        """
        ...
    def getGroundLoss(self) -> float:
        """
        
            Returns:
                the technological losses by the ground antenna [dB].
        
        
        """
        ...
    def getMeritFactor(self) -> float:
        """
        
            Returns:
                the factor of merit of the ground antenna (gain / noise temperature) [dB / K].
        
        
        """
        ...
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.Frame: ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getPointingLoss(self, double: float) -> float:
        """
            Gets the pointing loss using a spline interpolation.
        
        
            The pointing loss is a function of the ground station elevation.
        
            Parameters:
                elevation (double): ground station elevation [rad], in the range [-PI/2; PI/2].
        
            Returns:
                the pointing loss for a given elevation [rad * dB].
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.groundstation")``.

    GeometricStationAntenna: typing.Type[GeometricStationAntenna]
    RFStationAntenna: typing.Type[RFStationAntenna]
