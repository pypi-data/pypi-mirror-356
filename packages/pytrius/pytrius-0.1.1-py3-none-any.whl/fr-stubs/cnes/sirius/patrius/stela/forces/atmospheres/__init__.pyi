
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.forces.atmospheres
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.analysis.interpolation
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.stela.forces.solaractivity
import fr.cnes.sirius.patrius.time
import java.io
import typing



class Jacchia77(fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere):
    """
    public class Jacchia77 extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`
    
    
        This class implements the Jaccia77 atmospheric model.
    
        This class is restricted to be used with :class:`~fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape`.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, iStelaSolarActivity: fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def copy(self) -> fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere:
        """
            A copy of the atmosphere. By default copy is deep. If not, atmosphere javadoc will specify which attribute is not fully
            copied. In that case, the attribute reference is passed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere.copy` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`
        
            Returns:
                a atmosphere of the detector.
        
        
        """
        ...
    def getData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> 'JacchiaOutput': ...
    def getDensity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getEarthBody(self) -> fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape:
        """
            Getter for the earth body.
        
            Returns:
                the earth body
        
        
        """
        ...
    def getMeanMolarMass(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getSolarActivity(self) -> fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity:
        """
            Getter for the solar activity.
        
            Returns:
                the solar activity
        
        
        """
        ...
    def getSpeedOfSound(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getSun(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Getter for the sun.
        
            Returns:
                the sun
        
        
        """
        ...
    def getTemperature(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getVelocity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class Jacchia77Data(java.io.Serializable):
    """
    public final class Jacchia77Data extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class implements the Jaccia77 atmospheric model data and functions.
    
        The constants used in the equations relative to this model are stored in this class.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    AP_KP_TABLE: typing.ClassVar[typing.MutableSequence[typing.MutableSequence[float]]] = ...
    """
    public static final double[][] AP_KP_TABLE
    
        Table used for Ap/Kp conversion.
    
    """
    AP_FUNCTION: typing.ClassVar[fr.cnes.sirius.patrius.math.analysis.interpolation.UniLinearIntervalsFunction] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UniLinearIntervalsFunction` AP_FUNCTION
    
        1D interpolator for Ap/Kp conversion table.
    
    """
    ALT_TABLE: typing.ClassVar[typing.MutableSequence[float]] = ...
    """
    public static final double[] ALT_TABLE
    
        Altitudes table for density logarithm interpolation.
    
    """
    TEMP_TABLE: typing.ClassVar[typing.MutableSequence[float]] = ...
    """
    public static final double[] TEMP_TABLE
    
        Temperatures table for density logarithm interpolation.
    
    """
    def __init__(self): ...
    def getMeanMolarMassFunction(self) -> fr.cnes.sirius.patrius.math.analysis.interpolation.BiLinearIntervalsFunction:
        """
            Getter for the 2D interpolator for mean molar mass map.
        
            Returns:
                the 2D interpolator for mean molar mass map
        
        
        """
        ...
    def getRhoFunction(self) -> fr.cnes.sirius.patrius.math.analysis.interpolation.BiLinearIntervalsFunction:
        """
            Getter for the 2D interpolator for density map.
        
            Returns:
                the 2D interpolator for density map
        
        
        """
        ...
    def getTempFunction(self) -> fr.cnes.sirius.patrius.math.analysis.interpolation.BiLinearIntervalsFunction:
        """
            Getter for the 2D interpolator for temperature map.
        
            Returns:
                the 2D interpolator for temperature map
        
        
        """
        ...
    def initTempWmMaps(self) -> None:
        """
            Initialization of temperature and mean molar mass interpolation maps.
        
        """
        ...

class JacchiaOutput(java.io.Serializable):
    """
    public class JacchiaOutput extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Atmospheric model output specialized for the :class:`~fr.cnes.sirius.patrius.stela.forces.atmospheres.Jacchia77` model.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float): ...
    def getDensity(self) -> float:
        """
            Getter for the atmospheric density.
        
            Returns:
                the atmospheric density (kg/m3)
        
        
        """
        ...
    def getMeanMolarMass(self) -> float:
        """
            Getter for the atmospheric mean molar mass.
        
            Returns:
                the atmospheric mean molar mass (kg/mol)
        
        
        """
        ...
    def getTemperature(self) -> float:
        """
            Getter for the atmospheric temperature.
        
            Returns:
                the atmospheric temperature (K)
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.forces.atmospheres")``.

    Jacchia77: typing.Type[Jacchia77]
    Jacchia77Data: typing.Type[Jacchia77Data]
    JacchiaOutput: typing.Type[JacchiaOutput]
