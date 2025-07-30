
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.forces.atmospheres.MSIS2000
import fr.cnes.sirius.patrius.forces.atmospheres.solarActivity
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.time
import java.io
import jpype
import typing



class Atmosphere(java.io.Serializable):
    """
    public interface Atmosphere extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for atmospheric models.
    """
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def copy(self) -> 'Atmosphere':
        """
            A copy of the atmosphere. By default copy is deep. If not, atmosphere javadoc will specify which attribute is not fully
            copied. In that case, the attribute reference is passed.
        
            Returns:
                a atmosphere of the detector.
        
        
        """
        ...
    def getDensity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getSpeedOfSound(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getVelocity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class AtmosphereData(java.io.Serializable):
    """
    public class AtmosphereData extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Container for extended atmosphere data.
    
        Some atmosphere model do not provide all information. The list of available information is detailed for each atmosphere
        model.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    HYDROGEN_MASS: typing.ClassVar[float] = ...
    """
    public static final double HYDROGEN_MASS
    
        Hydrogen atomic mass.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float, double10: float, double11: float): ...
    def getDensity(self) -> float:
        """
            Returns the total density.
        
            Returns:
                the total density
        
        
        """
        ...
    def getDensityAnomalousOxygen(self) -> float:
        """
            Returns the anomalous oxygen density.
        
            Returns:
                the anomalous oxygen density
        
        
        """
        ...
    def getDensityAr(self) -> float:
        """
            Returns the Argon density.
        
            Returns:
                the Argon density
        
        
        """
        ...
    def getDensityH(self) -> float:
        """
            Returns the hydrogen density.
        
            Returns:
                the hydrogen density
        
        
        """
        ...
    def getDensityHe(self) -> float:
        """
            Return the Helium density.
        
            Returns:
                the Helium density
        
        
        """
        ...
    def getDensityN(self) -> float:
        """
            Returns the nitrogen density.
        
            Returns:
                the nitrogen density
        
        
        """
        ...
    def getDensityN2(self) -> float:
        """
            Returns the dinitrogen density.
        
            Returns:
                the dinitrogen density
        
        
        """
        ...
    def getDensityO(self) -> float:
        """
            Returns the Oxygen density.
        
            Returns:
                the Oxygen density
        
        
        """
        ...
    def getDensityO2(self) -> float:
        """
            Returns the dioxygen density.
        
            Returns:
                the dioxygen density
        
        
        """
        ...
    def getExosphericTemperature(self) -> float:
        """
            Returns the exospheric temperature.
        
            Returns:
                the exospheric temperature
        
        
        """
        ...
    def getLocalTemperature(self) -> float:
        """
            Returns the local temperature.
        
            Returns:
                the local temperature
        
        
        """
        ...
    def getMeanAtomicMass(self) -> float:
        """
            Returns the mean atomic mass or the molar mass.
        
            Returns:
                the mean atomic mass (in unit of hydrogen mass) or the molar mass (in kg). To get the mean atomic mass in kg, multiply
                it with :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.AtmosphereData.HYDROGEN_MASS`
        
        
        """
        ...

class DTMInputParameters(java.io.Serializable):
    """
    public interface DTMInputParameters extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Container for solar activity data, compatible with all DTM Atmosphere models. This model needs mean and instantaneous
        solar flux and geomagnetic incides to compute the local density. Mean solar flux is (for the moment) represented by the
        F10.7 indices. Instantaneous flux can be set to the mean value if the data is not available. Geomagnetic acivity is
        represented by the Kp indice, which goes from 1 (very low activity) to 9 (high activity).
    
        All needed solar activity data can be found on the ` NOAA (National Oceanic and Atmospheric Administration) website.
        <http://sec.noaa.gov/Data/index.html>`
    """
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def get24HoursKp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getInstantFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range maximum date.
        
            Returns:
                the maximum date.
        
        
        """
        ...
    def getMeanFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range minimum date.
        
            Returns:
                the minimum date.
        
        
        """
        ...
    def getThreeHourlyKP(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...

class JB2006InputParameters(java.io.Serializable):
    """
    public interface JB2006InputParameters extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for solar activity and magnetic activity data.
    """
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def getAp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getF10(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getF10B(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range maximum date.
        
            Returns:
                the maximum date.
        
        
        """
        ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range minimum date.
        
            Returns:
                the minimum date.
        
        
        """
        ...
    def getS10(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getS10B(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getXM10(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getXM10B(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...

class MSISE2000InputParameters(java.io.Serializable):
    """
    public interface MSISE2000InputParameters extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Container for solar activity data, compatible with :class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSISE2000`
        Atmosphere model. This model needs mean and instantaneous solar flux and geomagnetic incides to compute the local
        density.
    
        Since:
            2.1
    """
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def getApValues(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]: ...
    def getInstantFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMaxDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range maximum date.
        
            Returns:
                the maximum date.
        
        
        """
        ...
    def getMeanFlux(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getMinDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Gets the available data range minimum date.
        
            Returns:
                the minimum date.
        
        
        """
        ...

class ExtendedAtmosphere(Atmosphere):
    """
    public interface ExtendedAtmosphere extends :class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`
    
        Interface for extended atmosphere. This interface provides more detailed atmospheric data such as partial densities.
    
        Since:
            3.3
    """
    def getData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> AtmosphereData: ...

class HarrisPriester(Atmosphere):
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape, double: float): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double2: float): ...
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def copy(self) -> Atmosphere: ...
    @typing.overload
    def getDensity(self, double: float, double2: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double3: float) -> float: ...
    @typing.overload
    def getDensity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getMaxAlt(self) -> float: ...
    def getMinAlt(self) -> float: ...
    def getSpeedOfSound(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getTabDensity(self) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getVelocity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class JB2006(Atmosphere):
    """
    public class JB2006 extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`
    
        This is the realization of the Jacchia-Bowman 2006 atmospheric model.
    
        It is described in the paper:
    
    
        `A New Empirical Thermospheric Density Model JB2006 Using New Solar Indices
        <http://sol.spacenvironment.net/~JB2006/pubs/JB2006_AIAA-6166_model.pdf>`
    
    
        *Bruce R. Bowman, W. Kent Tobiska and Frank A. Marcos*
    
    
        AIAA 2006-6166
    
    
    
        Two computation methods are proposed to the user:
    
          - one OREKIT independent and compliant with initial FORTRAN routine entry values:
            :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.JB2006.getDensity`
          - one compliant with OREKIT Atmosphere interface, necessary to the :class:`~fr.cnes.sirius.patrius.forces.drag.DragForce`
            computation.
    
    
        This model provides dense output for any position with altitude larger than 90km. Output data are :
    
          - Exospheric Temperature above Input Position (deg K)
          - Temperature at Input Position (deg K)
          - Total Mass-Density at Input Position (kg/m :sup:`3` )
    
    
        The model needs geographical and time information to compute general values, but also needs space weather data : mean
        and daily solar flux, retrieved threw different indices, and planetary geomagnetic indices.
    
    
        More information on these indices can be found on the ` official JB2006 website.
        <http://sol.spacenvironment.net/~JB2006/JB2006_index.html>`
    
        This class is restricted to be used with :class:`~fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape`.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, jB2006InputParameters: JB2006InputParameters, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape): ...
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def copy(self) -> Atmosphere:
        """
            A copy of the atmosphere. By default copy is deep. If not, atmosphere javadoc will specify which attribute is not fully
            copied. In that case, the attribute reference is passed.
        
            The following attributes are not deeply copied:
        
              - inputParams: :class:`~fr.cnes.sirius.patrius.forces.atmospheres.JB2006InputParameters`
              - sun: :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
              - earth: :class:`~fr.cnes.sirius.patrius.bodies.BodyShape`
        
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere.copy` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`
        
            Returns:
                a atmosphere of the detector.
        
        
        """
        ...
    @typing.overload
    def getDensity(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float, double10: float, double11: float, double12: float, double13: float) -> float:
        """
            Get the local density with initial entries.
        
            Parameters:
                dateMJD (double): date and time, in modified julian days and fraction
                sunRA (double): Right Ascension of Sun (radians)
                sunDecli (double): Declination of Sun (radians)
                satLon (double): Right Ascension of position (radians)
                satLat (double): Geocentric latitude of position (radians)
                satAlt (double): Height of position (m)
                f10 (double): 10.7-cm Solar flux (1e :sup:`-22` *Watt/(m :sup:`2` *Hertz)). Tabular time 1.0 day earlier
                f10B (double): 10.7-cm Solar Flux, averaged 81-day centered on the input time
                ap (double): Geomagnetic planetary 3-hour index A :sub:`p` for a tabular time 6.7 hours earlier
                s10 (double): EUV index (26-34 nm) scaled to F10. Tabular time 1 day earlier.
                s10B (double): UV 81-day averaged centered index
                xm10 (double): MG2 index scaled to F10
                xm10B (double): MG2 81-day ave. centered index. Tabular time 5.0 days earlier.
        
            Returns:
                total mass-Density at input position (kg/m :sup:`3` )
        
        public double getDensity(:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` date, :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D` position, :class:`~fr.cnes.sirius.patrius.frames.Frame` frame) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Get the local density.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere.getDensity` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                position (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): current position in frame
                frame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the frame in which is defined the position
        
            Returns:
                local density (kg/m :sup:`3` )
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if date is out of range of solar activity
        
        
        """
        ...
    @typing.overload
    def getDensity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getExosphericTemp(self) -> float:
        """
            Get the exospheric temperature above input position.
            :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.JB2006.getDensity` **must** be called before calling this function.
        
            Returns:
                the exospheric temperature (deg K)
        
        
        """
        ...
    def getLocalTemp(self) -> float:
        """
            Get the temperature at input position. :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.JB2006.getDensity` **must** be
            called before calling this function.
        
            Returns:
                the local temperature (deg K)
        
        
        """
        ...
    def getSpeedOfSound(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getVelocity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class SimpleExponentialAtmosphere(Atmosphere):
    """
    public class SimpleExponentialAtmosphere extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`
    
        Simple exponential atmospheric model.
    
        This model represents a simple atmosphere with an exponential density and rigidly bound to the underlying rotating body.
    
        This class is restricted to be used with :class:`~fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape`.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape, double: float, double2: float, double3: float): ...
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            This methods throws an exception if the user did not provide solar activity on the provided interval [start, end]. All
            models should implement their own method since the required data interval depends on the model.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere.checkSolarActivityData` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`
        
            Parameters:
                start (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): range start date
                end (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): range end date
        
        
        """
        ...
    def copy(self) -> Atmosphere:
        """
            A copy of the atmosphere. By default copy is deep. If not, atmosphere javadoc will specify which attribute is not fully
            copied. In that case, the attribute reference is passed.
        
            The following attributes are not deeply copied:
        
              - shape: :class:`~fr.cnes.sirius.patrius.bodies.BodyShape`
        
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere.copy` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`
        
            Returns:
                a atmosphere of the detector.
        
        
        """
        ...
    def getDensity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getH0(self) -> float:
        """
            Getter for the Altitude of reference (m).
        
            Returns:
                the Altitude of reference (m)
        
        
        """
        ...
    def getHscale(self) -> float:
        """
            Getter for the Scale factor (m).
        
            Returns:
                the Scale factor (m)
        
        
        """
        ...
    def getRho0(self) -> float:
        """
            Getter for the Density at the altitude h0.
        
            Returns:
                the Density at the altitude h0
        
        
        """
        ...
    def getShape(self) -> fr.cnes.sirius.patrius.bodies.BodyShape:
        """
            Getter for the Body shape model.
        
            Returns:
                the Body shape model
        
        
        """
        ...
    def getSpeedOfSound(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float:
        """
            Get the local speed of sound.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere.getSpeedOfSound` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): current date
                position (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): current position in frame
                frame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the frame in which is defined the position
        
            Returns:
                speed of sound (m/s)
        
        
        """
        ...
    def getVelocity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class US76(Atmosphere):
    def __init__(self, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape): ...
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def copy(self) -> Atmosphere: ...
    def getDensity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getEarthBody(self) -> fr.cnes.sirius.patrius.bodies.BodyShape: ...
    def getPress(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getSpeedOfSound(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getTemp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getVelocity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class AbstractDTM(ExtendedAtmosphere):
    HYDROGEN: typing.ClassVar[int] = ...
    HELIUM: typing.ClassVar[int] = ...
    ATOMIC_OXYGEN: typing.ClassVar[int] = ...
    MOLECULAR_NITROGEN: typing.ClassVar[int] = ...
    MOLECULAR_OXYGEN: typing.ClassVar[int] = ...
    ATOMIC_NITROGEN: typing.ClassVar[int] = ...
    def __init__(self, dTMInputParameters: DTMInputParameters, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape, string: str): ...
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def copy(self) -> Atmosphere: ...
    def getData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> AtmosphereData: ...
    def getDensity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getEarth(self) -> fr.cnes.sirius.patrius.bodies.BodyShape: ...
    def getParameters(self) -> DTMInputParameters: ...
    def getSpeedOfSound(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getSun(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider: ...
    def getVelocity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class MSISE2000(ExtendedAtmosphere):
    """
    public class MSISE2000 extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.atmospheres.ExtendedAtmosphere`
    
        This class implements the MSIS00 atmospheric model.
    
    
        It is an interface layer between the :class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSIS2000.NRLMSISE00` class -
        adapted from Fortran - and the SIRIUS data structures.
    
        **Warning**: this model is not continuous. There is a discontinuity every day (at 0h in UTC time scale). Discontinuities
        are however very small (1E-3 on a relative scale).
    
        This class is restricted to be used with :class:`~fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape`.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, mSISE2000InputParameters: MSISE2000InputParameters, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider): ...
    def checkSolarActivityData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def copy(self) -> Atmosphere:
        """
            A copy of the atmosphere. By default copy is deep. If not, atmosphere javadoc will specify which attribute is not fully
            copied. In that case, the attribute reference is passed.
        
            The following attributes are not deeply copied:
        
              - inputParams: :class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSISE2000InputParameters`
              - sun: :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
              - earth: :class:`~fr.cnes.sirius.patrius.bodies.BodyShape`
        
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere.copy` in
                interface :class:`~fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere`
        
            Returns:
                a atmosphere of the detector.
        
        
        """
        ...
    def getData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> AtmosphereData: ...
    def getDensity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getEarthBody(self) -> fr.cnes.sirius.patrius.bodies.BodyShape:
        """
            Getter for the earth body.
        
            Returns:
                the earth body
        
        
        """
        ...
    def getParameters(self) -> MSISE2000InputParameters:
        """
            Getter for the solar parameters.
        
            Returns:
                the solar parameters
        
        
        """
        ...
    def getPressure(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getSpeedOfSound(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getSun(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
            Getter for the Sun.
        
            Returns:
                the Sun
        
        
        """
        ...
    def getVelocity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...

class DTM2000(AbstractDTM):
    def __init__(self, dTMInputParameters: DTMInputParameters, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape): ...
    def copy(self) -> Atmosphere: ...

class DTM2012(AbstractDTM):
    @typing.overload
    def __init__(self, dTMInputParameters: DTMInputParameters, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape): ...
    @typing.overload
    def __init__(self, dTMInputParameters: DTMInputParameters, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape, string: str): ...
    def copy(self) -> Atmosphere: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.atmospheres")``.

    AbstractDTM: typing.Type[AbstractDTM]
    Atmosphere: typing.Type[Atmosphere]
    AtmosphereData: typing.Type[AtmosphereData]
    DTM2000: typing.Type[DTM2000]
    DTM2012: typing.Type[DTM2012]
    DTMInputParameters: typing.Type[DTMInputParameters]
    ExtendedAtmosphere: typing.Type[ExtendedAtmosphere]
    HarrisPriester: typing.Type[HarrisPriester]
    JB2006: typing.Type[JB2006]
    JB2006InputParameters: typing.Type[JB2006InputParameters]
    MSISE2000: typing.Type[MSISE2000]
    MSISE2000InputParameters: typing.Type[MSISE2000InputParameters]
    SimpleExponentialAtmosphere: typing.Type[SimpleExponentialAtmosphere]
    US76: typing.Type[US76]
    MSIS2000: fr.cnes.sirius.patrius.forces.atmospheres.MSIS2000.__module_protocol__
    solarActivity: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.__module_protocol__
