
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.forces.gravity
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.analysis.interpolation
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.time
import java.io
import jpype
import typing



class AttractionData(java.io.Serializable):
    """
    public class AttractionData extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Attraction data: 3D acceleration and potential for all grid points. Grid point can be expressed in any coordinates
        system defined by interface :class:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridSystem` (currently either in 3D
        coordinates or spherical coordinates).
    
        This class is to be used in conjunction with :class:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridGravityModel` for
        attraction force defined by a grid.
    
        Since:
            4.7
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, gridSystem: 'GridSystem', attractionDataPointArray: typing.Union[typing.List['AttractionDataPoint'], jpype.JArray]): ...
    def getCenterOfMass(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Returns the center of mass position of the body.
        
            Returns:
                the center of mass position of the body
        
        
        """
        ...
    def getData(self) -> typing.MutableSequence['AttractionDataPoint']:
        """
            Returns the attraction data points.
        
            Returns:
                the attraction data points
        
        
        """
        ...
    def getGM(self) -> float:
        """
            Returns the gravitational constant of the body.
        
            Returns:
                the gravitational constant of the body
        
        
        """
        ...
    def getGrid(self) -> 'GridSystem':
        """
            Returns the grid system.
        
            Returns:
                the grid system
        
        
        """
        ...
    def getMuParameter(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Returns the gravitational constant of the body as a parameter.
        
            Returns:
                the gravitational constant of the body as a parameter
        
        
        """
        ...
    def setGM(self, double: float) -> None:
        """
            Set the central attraction coefficient.
        
            Parameters:
                gmIn (double): the central attraction coefficient
        
        
        """
        ...

class AttractionDataPoint(java.io.Serializable):
    """
    public class AttractionDataPoint extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Attraction data: 3D acceleration and potential for one grid point. Grid point can be expressed either in 3D coordinates
        or in spherical coordinates.
    
        This class is to be used in conjunction with :class:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridGravityModel` for
        attraction force defined by a grid.
    
        Since:
            4.7
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, sphericalCoordinates: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.SphericalCoordinates, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    def getAcceleration(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Returns the XYZ acceleration.
        
            Returns:
                the XYZ acceleration
        
        
        """
        ...
    def getPosition(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Returns the position.
        
            Returns:
                the position
        
        
        """
        ...
    def getPotential(self) -> float:
        """
            Returns the potential.
        
            Returns:
                the potential
        
        
        """
        ...
    def getSphericalCoordinates(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.SphericalCoordinates:
        """
            Returns the spherical coordinates.
        
            Returns:
                the spherical coordinates or null if unused
        
        
        """
        ...

class GridAttractionProvider:
    """
    public interface GridAttractionProvider
    
        Generic grid attraction provider. This interface represents a grid attraction provider, i.e. a class which provides
        :class:`~fr.cnes.sirius.patrius.forces.gravity.grid.AttractionData` for gravity force models defined by a 3D grid.
    
        This class is to be used in conjunction with :class:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridGravityModel` for
        attraction data loading.
    
        Since:
            4.6
    """
    def getData(self) -> AttractionData:
        """
            Returns the read data.
        
            Returns:
                the read data
        
        
        """
        ...

class GridGravityModel(fr.cnes.sirius.patrius.forces.gravity.AbstractGravityModel):
    """
    public class GridGravityModel extends :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractGravityModel`
    
        Computation of central body attraction with a grid attraction model: attraction acceleration is given by
        :class:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridAttractionProvider` which provides for a set of coordinates the
        value of acceleration. Interpolation is performed within grid points using a
        :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.TrivariateGridInterpolator`. Computed acceleration excludes
        the central attraction force like the other :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractGravityModel`. If
        requested point is out of grid boundaries, a 2nd model (back-up model) is used for computing attraction force.
    
        Potential is also available using method :code:`#computePotential(SpacecraftState)`.
    
        Partial derivatives are not available.
    
        Since:
            4.7
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, gridAttractionProvider: typing.Union[GridAttractionProvider, typing.Callable], trivariateGridInterpolator: typing.Union[fr.cnes.sirius.patrius.math.analysis.interpolation.TrivariateGridInterpolator, typing.Callable], gravityModel: fr.cnes.sirius.patrius.forces.gravity.GravityModel, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    def computeAcceleration(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeDAccDPos(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computePotential(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getBackupModel(self) -> fr.cnes.sirius.patrius.forces.gravity.GravityModel:
        """
            Getter for the backup model
        
            Returns:
                the backup model
        
        
        """
        ...
    def getMu(self) -> float:
        """
            Get the central attraction coefficient..
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel.getMu` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.AbstractGravityModel.getMu` in
                class :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractGravityModel`
        
            Returns:
                central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
        
        """
        ...
    def setMu(self, double: float) -> None:
        """
            Set the central attraction coefficient..
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel.setMu` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.AbstractGravityModel.setMu` in
                class :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractGravityModel`
        
            Parameters:
                muIn (double): the central attraction coefficient.
        
        
        """
        ...

class GridSystem(java.io.Serializable):
    """
    public interface GridSystem extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Grid system. A grid system is a 3D grid which is used for attraction models defined by a grid. Grid contains 3D
        acceleration as well as force potential.
    
        This class is to be used in conjunction with :class:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridGravityModel` for
        attraction force defined by a grid.
    
        Since:
            4.7
    """
    def getAccXArray(self) -> typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]:
        """
            Returns X acceleration data array (values along ordinates).
        
            Returns:
                X acceleration data array (values along ordinates)
        
        
        """
        ...
    def getAccYArray(self) -> typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]:
        """
            Returns Y acceleration data array (values along ordinates).
        
            Returns:
                Y acceleration data array (values along ordinates)
        
        
        """
        ...
    def getAccZArray(self) -> typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]:
        """
            Returns Z acceleration data array (values along ordinates).
        
            Returns:
                Z acceleration data array (values along ordinates)
        
        
        """
        ...
    def getCoordinates(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> typing.MutableSequence[float]:
        """
            Returns coordinates in grid system for provided position.
        
            Parameters:
                position (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): position
        
            Returns:
                coordinates in grid system
        
        
        """
        ...
    def getPotentialArray(self) -> typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]:
        """
            Returns potential data array (values along ordinates).
        
            Returns:
                potential data array (values along ordinates)
        
        
        """
        ...
    def getXArray(self) -> typing.MutableSequence[float]:
        """
            Returns first abscissa data array.
        
            Returns:
                first abscissa data array
        
        
        """
        ...
    def getYArray(self) -> typing.MutableSequence[float]:
        """
            Returns second abscissa data array.
        
            Returns:
                second abscissa data array
        
        
        """
        ...
    def getZArray(self) -> typing.MutableSequence[float]:
        """
            Returns third abscissa data array.
        
            Returns:
                third abscissa data array
        
        
        """
        ...
    def isInsideGrid(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool:
        """
            Returns true if provided position is within grid, false otherwise.
        
            Parameters:
                position (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): position
        
            Returns:
                true if provided position is within grid, false otherwise
        
        
        """
        ...

class CartesianGridAttractionLoader(GridAttractionProvider):
    """
    public class CartesianGridAttractionLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridAttractionProvider`
    
        Grid attraction model loader. This loader only reads attraction model files defined with a cubic grid (X, Y, Z).
    
        Read data is considered to be in km.
    
        Since:
            4.7
    """
    def __init__(self, string: str): ...
    def getData(self) -> AttractionData:
        """
            Returns the read data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridAttractionProvider.getData` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridAttractionProvider`
        
            Returns:
                the read data
        
        
        """
        ...

class SphericalGridAttractionLoader(GridAttractionProvider):
    """
    public class SphericalGridAttractionLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridAttractionProvider`
    
        Grid attraction model loader. This loader only reads attraction model files defined with a spherical grid (altitude,
        longitude, latitude).
    
        Read data is considered to be in km and degrees.
    
        Since:
            4.7
    """
    def __init__(self, string: str): ...
    def getData(self) -> AttractionData:
        """
            Returns the read data.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridAttractionProvider.getData` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.grid.GridAttractionProvider`
        
            Returns:
                the read data
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.gravity.grid")``.

    AttractionData: typing.Type[AttractionData]
    AttractionDataPoint: typing.Type[AttractionDataPoint]
    CartesianGridAttractionLoader: typing.Type[CartesianGridAttractionLoader]
    GridAttractionProvider: typing.Type[GridAttractionProvider]
    GridGravityModel: typing.Type[GridGravityModel]
    GridSystem: typing.Type[GridSystem]
    SphericalGridAttractionLoader: typing.Type[SphericalGridAttractionLoader]
