
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import typing



class GeoMagneticDataProvider:
    """
    public interface GeoMagneticDataProvider
    
        Interface for geomagnetic data provider.
    
    
    
        Since:
            2.1
    """
    def getModels(self) -> java.util.Collection['GeoMagneticField']: ...

class GeoMagneticElements(java.io.Serializable):
    """
    public class GeoMagneticElements extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Contains the elements to represent a magnetic field at a single point.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    def getDeclination(self) -> float:
        """
            Returns the declination of the magnetic field in degrees.
        
            Returns:
                the declination (dec) in degrees
        
        
        """
        ...
    def getFieldVector(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Returns the magnetic field vector in the topocentric frame (North=X, East=Y, Nadir=Z) in nTesla.
        
            Returns:
                the magnetic field vector in nTesla
        
        
        """
        ...
    def getHorizontalIntensity(self) -> float:
        """
            Returns the horizontal intensity of the magnetic field (= norm of the vector in the plane spanned by the x/y components
            of the field vector).
        
            Returns:
                the horizontal intensity in nTesla
        
        
        """
        ...
    def getInclination(self) -> float:
        """
            Returns the inclination of the magnetic field in degrees.
        
            Returns:
                the inclination (dip) in degrees
        
        
        """
        ...
    def getTotalIntensity(self) -> float:
        """
            Returns the total intensity of the magnetic field (= norm of the field vector).
        
            Returns:
                the total intensity in nTesla
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class GeoMagneticField:
    """
    public class GeoMagneticField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Used to calculate the geomagnetic field at a given ellipsoid point on earth. The calculation is estimated using
        spherical harmonic expansion of the geomagnetic potential with coefficients provided by an actual geomagnetic field
        model (e.g. IGRF, WMM).
    
        Based on original software written by Manoj Nair from the National Geophysical Data Center, NOAA, as part of the WMM
        2010 software release (WMM_SubLibrary.c)
    
        Also see:
            `World Magnetic Model Overview <http://www.ngdc.noaa.gov/geomag/WMM/DoDWMM.shtml>`, `WMM Software Downloads
            <http://www.ngdc.noaa.gov/geomag/WMM/soft.shtml>`
    """
    def __init__(self, string: str, double: float, int: int, int2: int, double2: float, double3: float): ...
    @typing.overload
    def calculateField(self, double: float, double2: float, double3: float) -> GeoMagneticElements:
        """
            Calculate the magnetic field at the specified latitude, longitude and height.
        
            Parameters:
                latitude (double): the latitude in decimal degrees
                longitude (double): the longitude in decimal degrees
                altitude (double): the altitude in kilometers above mean sea level
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.models.earth.GeoMagneticElements` at the given ellipsoid point
        
        """
        ...
    @typing.overload
    def calculateField(self, ellipsoidPoint: fr.cnes.sirius.patrius.bodies.EllipsoidPoint) -> GeoMagneticElements:
        """
            Calculate the magnetic field at the specified ellipsoid point identified by latitude, longitude and height.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.bodies.EllipsoidPoint`): ellipsoid point
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.models.earth.GeoMagneticElements` at the given ellipsoid point
        
        public :class:`~fr.cnes.sirius.patrius.models.earth.GeoMagneticElements` calculateField(:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D` point, :class:`~fr.cnes.sirius.patrius.frames.Frame` frame, :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` date) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Calculate the magnetic field at the specified point identified by the coordinates of the point and the reference point.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): cartesian point
                frame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): frame in which cartesian point is expressed
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date in which cartesian point is given
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.models.earth.GeoMagneticElements` at the given cartesian point
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if point cannot be converted to body frame if the specified year is outside the validity period if getDecimalYear()
                    error occurred
        
        
        """
        ...
    @typing.overload
    def calculateField(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> GeoMagneticElements: ...
    @typing.overload
    @staticmethod
    def getDecimalYear(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Utility function to get a decimal year for a given day.
        
            Parameters:
                day (int): the day (1-31)
                month (int): the month (1-12)
                year (int): the year
        
            Returns:
                the decimal year represented by the given day
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getDecimalYear(int: int, int2: int, int3: int) -> float: ...
    def getEpoch(self) -> float:
        """
            Getter for the epoch for this magnetic field model.
        
            Returns:
                the epoch
        
        
        """
        ...
    def getModelName(self) -> str:
        """
            Getter for the model name.
        
            Returns:
                the model name
        
        
        """
        ...
    def setMainFieldCoefficients(self, int: int, int2: int, double: float, double2: float) -> None:
        """
            Setter for the given main field coefficients.
        
            Parameters:
                n (int): the degree
                m (int): the order
                gnm (double): the g coefficient at position n,m
                hnm (double): the h coefficient at position n,m
        
        
        """
        ...
    def setSecularVariationCoefficients(self, int: int, int2: int, double: float, double2: float) -> None:
        """
            Setter for the given secular variation coefficients.
        
            Parameters:
                n (int): the degree
                m (int): the order
                dgnm (double): the dg coefficient at position n,m
                dhnm (double): the dh coefficient at position n,m
        
        
        """
        ...
    def supportsTimeTransform(self) -> bool:
        """
            Indicates whether this model supports time transformation or not.
        
            Returns:
                :code:`true` if this model can be transformed within its validity period, :code:`false` otherwise
        
        
        """
        ...
    @typing.overload
    def transformModel(self, double: float) -> 'GeoMagneticField': ...
    @typing.overload
    def transformModel(self, geoMagneticField: 'GeoMagneticField', double: float) -> 'GeoMagneticField': ...
    def validFrom(self) -> float:
        """
            Getter for the start of the validity period for this model.
        
            Returns:
                the validity start as decimal year
        
        
        """
        ...
    def validTo(self) -> float:
        """
            Getter for the end of the validity period for this model.
        
            Returns:
                the validity end as decimal year
        
        
        """
        ...

class GeoMagneticFieldFactory:
    @staticmethod
    def addDefaultGeoMagneticModelReader(fieldModel: 'GeoMagneticFieldFactory.FieldModel') -> None: ...
    @staticmethod
    def addGeoMagneticModelReader(fieldModel: 'GeoMagneticFieldFactory.FieldModel', geoMagneticModelReader: 'GeoMagneticModelReader') -> None: ...
    @staticmethod
    def clearGeoMagneticModelReaders() -> None: ...
    @staticmethod
    def clearModels() -> None: ...
    @typing.overload
    @staticmethod
    def getField(fieldModel: 'GeoMagneticFieldFactory.FieldModel', double: float) -> GeoMagneticField: ...
    @typing.overload
    @staticmethod
    def getField(fieldModel: 'GeoMagneticFieldFactory.FieldModel', absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> GeoMagneticField: ...
    @typing.overload
    @staticmethod
    def getIGRF(double: float) -> GeoMagneticField: ...
    @typing.overload
    @staticmethod
    def getIGRF(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> GeoMagneticField: ...
    @typing.overload
    @staticmethod
    def getWMM(double: float) -> GeoMagneticField: ...
    @typing.overload
    @staticmethod
    def getWMM(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> GeoMagneticField: ...
    class FieldModel(java.lang.Enum['GeoMagneticFieldFactory.FieldModel']):
        WMM: typing.ClassVar['GeoMagneticFieldFactory.FieldModel'] = ...
        IGRF: typing.ClassVar['GeoMagneticFieldFactory.FieldModel'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'GeoMagneticFieldFactory.FieldModel': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['GeoMagneticFieldFactory.FieldModel']: ...

class InterpolationTableLoader(fr.cnes.sirius.patrius.data.DataLoader):
    """
    public class InterpolationTableLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataLoader`
    
        Used to read an interpolation table from a data file.
    """
    def __init__(self): ...
    def getAbscissaGrid(self) -> typing.MutableSequence[float]:
        """
            Returns a copy of the abscissa grid for the interpolation function.
        
            Returns:
                the abscissa grid for the interpolation function, or :code:`null` if the file could not be read
        
        
        """
        ...
    def getOrdinateGrid(self) -> typing.MutableSequence[float]:
        """
            Returns a copy of the ordinate grid for the interpolation function.
        
            Returns:
                the ordinate grid for the interpolation function, or :code:`null` if the file could not be read
        
        
        """
        ...
    def getValuesSamples(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Returns a copy of the values samples for the interpolation function.
        
            Returns:
                the values samples for the interpolation function, or :code:`null` if the file could not be read
        
        
        """
        ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...
    def stillAcceptsData(self) -> bool:
        """
            Check if the loader still accepts new data.
        
            This method is used to speed up data loading by interrupting crawling the data sets as soon as a loader has found the
            data it was waiting for. For loaders that can merge data from any number of sources (for example JPL ephemerides or
            Earth Orientation Parameters that are split among several files), this method should always return true to make sure no
            data is left over.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.data.DataLoader.stillAcceptsData` in
                interface :class:`~fr.cnes.sirius.patrius.data.DataLoader`
        
            Returns:
                true while the loader still accepts new data
        
        
        """
        ...

class GeoMagneticModelReader(fr.cnes.sirius.patrius.data.DataLoader, GeoMagneticDataProvider):
    """
    public abstract class GeoMagneticModelReader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataLoader`, :class:`~fr.cnes.sirius.patrius.models.earth.GeoMagneticDataProvider`
    
        Loads geomagnetic field models from a given input stream. A stream may contain multiple models, the loader reads all
        available models in consecutive order.
    
        The format of the expected model file is the following:
    
        .. code-block: java
        
        
             {model name} {epoch} {nMax} {nMaxSec} {nMax3} {validity start}
             {validity end} {minAlt} {maxAlt} {model name} {line number}
         {n} {m} {gnm} {hnm} {dgnm} {dhnm} {model name} {line number}
         
    
        Example:
    
        .. code-block: java
        
        
            WMM2010  2010.00 12 12  0 2010.00 2015.00   -1.0  600.0          WMM2010   0
         1  0  -29496.6       0.0      11.6       0.0                        WMM2010   1
         1  1   -1586.3    4944.4      16.5     -25.9                        WMM2010   2
    """
    def getModels(self) -> java.util.Collection[GeoMagneticField]: ...
    def getSupportedNames(self) -> str:
        """
            Get the regular expression for supported files names.
        
            Returns:
                regular expression for supported files names
        
        
        """
        ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...
    def stillAcceptsData(self) -> bool:
        """
            Check if the loader still accepts new data.
        
            This method is used to speed up data loading by interrupting crawling the data sets as soon as a loader has found the
            data it was waiting for. For loaders that can merge data from any number of sources (for example JPL ephemerides or
            Earth Orientation Parameters that are split among several files), this method should always return true to make sure no
            data is left over.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.data.DataLoader.stillAcceptsData` in
                interface :class:`~fr.cnes.sirius.patrius.data.DataLoader`
        
            Returns:
                true while the loader still accepts new data
        
        
        """
        ...

class COFFileFormatReader(GeoMagneticModelReader):
    """
    public final class COFFileFormatReader extends :class:`~fr.cnes.sirius.patrius.models.earth.GeoMagneticModelReader`
    
        Reader for COF file formats for geomagnetic models.
    
        Since:
            2.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.models.earth.GeoMagneticModelReader`
    """
    def __init__(self, string: str): ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.models.earth")``.

    COFFileFormatReader: typing.Type[COFFileFormatReader]
    GeoMagneticDataProvider: typing.Type[GeoMagneticDataProvider]
    GeoMagneticElements: typing.Type[GeoMagneticElements]
    GeoMagneticField: typing.Type[GeoMagneticField]
    GeoMagneticFieldFactory: typing.Type[GeoMagneticFieldFactory]
    GeoMagneticModelReader: typing.Type[GeoMagneticModelReader]
    InterpolationTableLoader: typing.Type[InterpolationTableLoader]
