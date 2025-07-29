
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes.directions
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import java.io
import java.lang
import jpype
import typing



class AngularDistanceType(java.lang.Enum['AngularDistanceType']):
    """
    public enum AngularDistanceType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.fieldsofview.AngularDistanceType`>
    
        This enum defines different methods to compute the angular distance between a given direction in space and the border of
        the FOV.
    """
    MINIMAL: typing.ClassVar['AngularDistanceType'] = ...
    DIRECTIONAL: typing.ClassVar['AngularDistanceType'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'AngularDistanceType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                : if this enum type has no constant with the specified name
                : if the argument is null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['AngularDistanceType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (AngularDistanceType c : AngularDistanceType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class FieldAngularFace(java.io.Serializable):
    """
    public final class FieldAngularFace extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class represent a face of a pyramidal field of view. It can compute the minimal angle between it and a given
        direction.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    def computeMinAngle(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the minimal angle between this and a given direction. If the direction's dot product to the normal vector to
            the face (cross product v1*v2), the angle is positive, and negative otherwise.
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector
        
            Returns:
                the signed minimal angular distance to the facet
        
        
        """
        ...
    def isCloseToVend(self) -> bool:
        """
        
            Returns:
                true if the direction vector is closest to V2 once the min angle has been computed.
        
        
        """
        ...
    def isCloseToVstart(self) -> bool:
        """
        
            Returns:
                true if the direction vector is closest to V1 once the min angle has been computed.
        
        
        """
        ...

class IFieldOfView(java.io.Serializable):
    """
    public interface IFieldOfView extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This is the interface for all the field of view (circular, elliptic...). All of them can compute the angular distance to
        a given direction (Vector3D).
    
        Since:
            1.2
    """
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the angular distance between a vector and the border of the field. The result is positive if the direction is
            in the field, negative otherwise. For some of the fields (ComplexField), that value can be approximative : see
            particular javadoc of each class.
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                the angular distance
        
        
        """
        ...
    def getName(self) -> str:
        """
        
            Returns:
                the name of the field
        
        
        """
        ...
    def isInTheField(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool:
        """
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): a direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                true if the direction is in the field
        
        
        """
        ...

class AzimuthElevationField(IFieldOfView):
    """
    public class AzimuthElevationField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
    
    
        Field of view defined by an azimuth-elevation mask : the algorithms are from the Orekit
        :class:`~fr.cnes.sirius.patrius.events.detectors.GroundMaskElevationDetector` detector. The mask is defined by an
        azimuth-elevation array : the vertical is the Z axis of the local frame, the angle between the local north and the x
        axis must be given at construction.
    
    
        The angular distance to the field limit is not the exact shortest distance: it is the exact angular distance on the
        local meridian (difference of elevation of the target and the linear interpolated local elevation). Concerning the field
        of view, the limit between two consecutive points is NOT a great circle (i.e. planar) limit: it is linear in
        azimuth-elevation. The fields with planar limits are the Rectangle or Pyramidal fields.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double2: float, string: str): ...
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the angular distance between a vector and the border of the field. The result is positive if the direction is
            in the field, negative otherwise. This value is approximative, mostly when the mask has great elevation variations, but
            its sign is right.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getAngularDistance` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): Point Cartesian coordinates
        
            Returns:
                the angular distance
        
        
        """
        ...
    def getElevation(self, double: float) -> float:
        """
            Get the Mask interpolated Elevation for a given Azimuth : this algorithm is from the orekit's
            :class:`~fr.cnes.sirius.patrius.events.detectors.GroundMaskElevationDetector`
        
            Parameters:
                azimuth (double): azimuth (counted clockwise) (rad)
        
            Returns:
                elevation angle (rad)
        
        
        """
        ...
    def getFrameOrientation(self) -> float:
        """
            Returns the frame orientation.
        
            Returns:
                the frame orientation
        
        
        """
        ...
    def getName(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getName` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Returns:
                the name of the field
        
        
        """
        ...
    def isInTheField(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.isInTheField` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): a direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                true if the direction is in the field
        
        
        """
        ...
    def linear(self, double: float, double2: float, double3: float, double4: float, double5: float) -> float:
        """
            Linear interpolation for given point x between (xa, ya) and (xb, yb).
        
            Parameters:
                x (double): x
                xa (double): xa
                xb (double): xb
                ya (double): ya
                yb (double): yb
        
            Returns:
                linear interpolation for given point x between (xa, ya) and (xb, yb)
        
        
        """
        ...

class BooleanField(IFieldOfView):
    """
    public final class BooleanField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
    
        This class describes a boolean field of view that combines two existing fields with a "AND" or "OR" boolean combination.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`, :meth:`~serialized`
    """
    def __init__(self, string: str, iFieldOfView: IFieldOfView, iFieldOfView2: IFieldOfView, booleanCombination: 'BooleanField.BooleanCombination'): ...
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the angular distance between a vector and the border of the field. The result is positive if the direction is
            in the field, negative otherwise. In some cases, this value can be approximative : in the "OR" case, inside of the
            field, and in the "AND" case ouside of it.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getAngularDistance` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the tropocentric coordinate system of the object)
        
            Returns:
                the angular distance
        
        
        """
        ...
    def getName(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getName` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Returns:
                the name of the field
        
        
        """
        ...
    def isInTheField(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.isInTheField` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): a direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                true if the direction is in the field
        
        
        """
        ...
    class BooleanCombination(java.lang.Enum['BooleanField.BooleanCombination']):
        AND: typing.ClassVar['BooleanField.BooleanCombination'] = ...
        OR: typing.ClassVar['BooleanField.BooleanCombination'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'BooleanField.BooleanCombination': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['BooleanField.BooleanCombination']: ...

class IGeometricFieldOfView(IFieldOfView):
    """
    public interface IGeometricFieldOfView extends :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
    
        This interface specifies the generic concept of :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView` with conical
        shapes based on a polygonal section. For such models, a main direction can be defined as the
        :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`, from the center of the FOV, passing through
        the center of each section of the cone.
    
        Since:
            4.14
    """
    @typing.overload
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, angularDistanceType: AngularDistanceType) -> float:
        """
            Computes the angular distance between a vector and the border of the field. The result is positive if the direction is
            in the field, negative otherwise.
        
            Several methods can be defined for the computation. The user can choose the more appropriate one from the enum
            :class:`~fr.cnes.sirius.patrius.fieldsofview.AngularDistanceType`.
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the topocentric coordinate system of the object)
                type (:class:`~fr.cnes.sirius.patrius.fieldsofview.AngularDistanceType`): Defines the method to compute the distance from the enum
                    :class:`~fr.cnes.sirius.patrius.fieldsofview.AngularDistanceType`
        
            Returns:
                the angular distance
        
        """
        ...
    @typing.overload
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the angular distance between a vector and the border of the field. The result is positive if the direction is
            in the field, negative otherwise.
        
            For a geometric FOV, the distance can be computed in several ways. This signature uses the
            :meth:`~fr.cnes.sirius.patrius.fieldsofview.AngularDistanceType.MINIMAL` method by default.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getAngularDistance` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                the angular distance
        
        
        """
        ...
    def getAngularOpening(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Get the angular opening of the Field Of View (FOV) over a given direction. Considering the half-plane containing both
            the main direction of the FOV and the input direction, the angular opening is defined as the angle between the main
            direction and the intersection of the FOV border with the half-plane.
        
            Parameters:
                directionIn (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                the angular opening along the input direction
        
        
        """
        ...
    def getMainDirection(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the main direction of the geometrical FOV. For every orthogonal section of the FOV, the main direction contains the
            center of such section.
        
            Returns:
                The main direction of the FOV
        
        
        """
        ...

class InvertField(IFieldOfView):
    """
    public final class InvertField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
    
        This field of view contains an existing field and inverts it.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`, :meth:`~serialized`
    """
    def __init__(self, string: str, iFieldOfView: IFieldOfView): ...
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the angular distance between a vector and the border of the field. The result is positive if the direction is
            in the field, negative otherwise. This "invert" field simply invert the value given by the origin field.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getAngularDistance` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the tropocentric coordinate system of the object)
        
            Returns:
                the angular distance
        
        
        """
        ...
    def getName(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getName` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Returns:
                the name of the field
        
        
        """
        ...
    def isInTheField(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.isInTheField` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): a direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                true if the direction is in the field
        
        
        """
        ...

class OmnidirectionalField(IFieldOfView):
    """
    public final class OmnidirectionalField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
    
        This class describes an omnidirectional field of view : any vector is in it, the angular distance is always 1
        (positive).
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`, :meth:`~serialized`
    """
    def __init__(self, string: str): ...
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            this method has no sense in the case of an omnidirectional field. The convention for all other fields to return a
            positive value if then vector is in the field : this method always return 1, all vectors being in it.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getAngularDistance` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (unused)
        
            Returns:
                always 1.0
        
        
        """
        ...
    def getName(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getName` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Returns:
                the name of the field
        
        
        """
        ...
    def isInTheField(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool:
        """
            Any vector being in the field, this method always return true
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.isInTheField` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (unused)
        
            Returns:
                always true
        
        
        """
        ...

class PyramidalField(IFieldOfView):
    """
    public final class PyramidalField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
    
        This class describes a pyramidal field of view defined a list of vectors (its edges) cone, to be used in "instruments"
        part properties. It implements the IFieldOfView interface and so provides the associated services.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, string: str, vector3DArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D], jpype.JArray]): ...
    @typing.overload
    def __init__(self, string: str, vector3DArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D], jpype.JArray], boolean: bool): ...
    def computeSideDirections(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> typing.MutableSequence[fr.cnes.sirius.patrius.attitudes.directions.IDirection]:
        """
            Retrieve the directions delimiting the pyramidal field of view.
        
            Parameters:
                frame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the reference frame in which the vectors will be defined as constant
        
            Returns:
                the directions delimiting the pyramidal field of view.
        
        
        """
        ...
    @typing.overload
    def equals(self, pyramidalField: 'PyramidalField', double: float) -> bool:
        """
            Check the equality between this and a provided :class:`~fr.cnes.sirius.patrius.fieldsofview.PyramidalField`. The side
            axis are assumed to be sorted in the same order. To be equal, both objects must have the same number of side axis and
            side axis at same index position must be colinear within a given tolerance.
        
            Parameters:
                otherFov (:class:`~fr.cnes.sirius.patrius.fieldsofview.PyramidalField`): the other pyramidal field
                angularTol (double): the numerical tolerance to check the colinearity between side axis
        
            Returns:
                :code:`true` if both pyramidal field are equal within the tolerance
        
        
        """
        ...
    @typing.overload
    def equals(self, object: typing.Any) -> bool: ...
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the angular distance between a vector and the border of the field. The result is positive if the direction is
            in the field, negative otherwise. For some of the fields (ComplexField), that value can be approximative : see
            particular javadoc of each class.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getAngularDistance` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                the angular distance
        
        
        """
        ...
    def getComplementaryFieldOfView(self) -> 'PyramidalField':
        """
            Build the complementary field of view of this. The side axis are sorted in reverse order.
        
            Returns:
                the complementary field of view
        
        
        """
        ...
    def getIntersectionWith(self, pyramidalField: 'PyramidalField') -> 'PyramidalField': ...
    def getName(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getName` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Returns:
                the name of the field
        
        
        """
        ...
    def getSideAxis(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D]:
        """
            Get the side axis of the field of view.
        
            Returns:
                the side axis of the field of view
        
        
        """
        ...
    def getUnionWith(self, pyramidalField: 'PyramidalField') -> 'PyramidalField': ...
    def isConvex(self) -> bool:
        """
            Indicates whether or not this field of view is convex.
        
            Returns:
                :code:`true` if this field is convex
        
        
        """
        ...
    @typing.overload
    def isInTheField(self, pyramidalField: 'PyramidalField') -> bool:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.isInTheField` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): a direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                true if the direction is in the field
        
            Indicates whether or not the provided :class:`~fr.cnes.sirius.patrius.fieldsofview.PyramidalField` is included in this
            one. The condition is respected if every side axis of the other field of view are contained in this one and if every
            side axis of this one are outside the other pyramidal field.
        
            Note: The second condition is verified only if this field of view is not convex.
        
            Note: By convention the result is true if the provided :class:`~fr.cnes.sirius.patrius.fieldsofview.PyramidalField` is
            null.
        
            Parameters:
                otherFov (:class:`~fr.cnes.sirius.patrius.fieldsofview.PyramidalField`): the other field of view.
        
            Returns:
                :code:`true` if this field of view contains the other one
        
        
        """
        ...
    @typing.overload
    def isInTheField(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool: ...
    def isPyramidalFieldWithIntersectingFaces(self) -> bool:
        """
            Indicates whether or not the faces of this field intersect each other.
        
            Returns:
                :code:`true` if the faces of this field intersect each other
        
        
        """
        ...
    def turnClockwise(self) -> bool:
        """
            Assess if the side axes of the entered field of view turn clockwise or counter-clockwise, from a sensor's/user's point
            of view.
        
        
            Calculation is perfomed only once for a field, meaning that it is performed if it has never been, and returns the
            previously calculated result otherwise.
        
        
            Field's attribute clockwiseAlreadyAssessed is updated for this purpose.
        
        
            This algorithm relies on the hypothesis that the faces of this field of view do not cross each other, so this field of
            view is expected to be well-formed.
        
            Returns:
                true if the field of view turns clockwise, false if counter-clockwise
        
        
        """
        ...

class SectorField(IFieldOfView):
    """
    public class SectorField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
    
    
        This class defines a "sector" field of view. This field is a min/max longitude and min/max latitude aperture on the unit
        sphere. It is defined by three vectors : the local "north pole" vector for this sphere, the min latitude - min longitude
        point vector (V1) and the max latitude - max longitude point vector (V2).
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`, :meth:`~serialized`
    """
    def __init__(self, string: str, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the angular distance between a vector and the border of the field. The result is positive if the direction is
            in the field, negative otherwise. For some of the fields (ComplexField), that value can be approximative : see
            particular javadoc of each class.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getAngularDistance` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                the angular distance
        
        
        """
        ...
    def getName(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getName` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Returns:
                the name of the field
        
        
        """
        ...
    def isInTheField(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.isInTheField` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): a direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                true if the direction is in the field
        
        
        """
        ...

class CircularField(IGeometricFieldOfView):
    """
    public final class CircularField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView`
    
        This class describes a right circular field of view to be used in "instruments" part properties. It implements the
        IFieldOfView interface and so provides the associated services.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`, :meth:`~serialized`
    """
    def __init__(self, string: str, double: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the angular distance between a vector and the border of the field. The result is positive if the direction is
            in the field, negative otherwise.
        
            Several methods can be defined for the computation. The user can choose the more appropriate one from the enum
            :class:`~fr.cnes.sirius.patrius.fieldsofview.AngularDistanceType`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView.getAngularDistance` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the topocentric coordinate system of the object)
                method (:class:`~fr.cnes.sirius.patrius.fieldsofview.AngularDistanceType`): Defines the method to compute the distance from the enum
                    :class:`~fr.cnes.sirius.patrius.fieldsofview.AngularDistanceType`
        
            Returns:
                the angular distance
        
        
        """
        ...
    @typing.overload
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, angularDistanceType: AngularDistanceType) -> float: ...
    def getAngularOpening(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Get the angular opening of the Field Of View (FOV) over a given direction. Considering the half-plane containing both
            the main direction of the FOV and the input direction, the angular opening is defined as the angle between the main
            direction and the intersection of the FOV border with the half-plane.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView.getAngularOpening` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView`
        
            Parameters:
                directionIn (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                the angular opening along the input direction
        
        
        """
        ...
    def getHalfAngularAperture(self) -> float:
        """
            Returns the half-aperture.
        
            Returns:
                the half-aperture
        
        
        """
        ...
    def getMainDirection(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the main direction of the geometrical FOV. For every orthogonal section of the FOV, the main direction contains the
            center of such section.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView.getMainDirection` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView`
        
            Returns:
                The main direction of the FOV
        
        
        """
        ...
    def getName(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getName` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Returns:
                the name of the field
        
        
        """
        ...
    def isInTheField(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.isInTheField` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): a direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                true if the direction is in the field
        
        
        """
        ...

class EllipticField(IGeometricFieldOfView):
    """
    public final class EllipticField extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView`
    
        This class describes an elliptic field of view to be used in "instruments" part properties. It implements the
        IFieldOfView interface and provides the associated services.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`, :meth:`~serialized`
    """
    def __init__(self, string: str, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, double2: float): ...
    @typing.overload
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the angular distance between a vector and the border of the field. The result is positive if the direction is
            in the field, negative otherwise.
        
            Several methods can be defined for the computation. The user can choose the more appropriate one from the enum
            :class:`~fr.cnes.sirius.patrius.fieldsofview.AngularDistanceType`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView.getAngularDistance` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the topocentric coordinate system of the object)
                method (:class:`~fr.cnes.sirius.patrius.fieldsofview.AngularDistanceType`): Defines the method to compute the distance from the enum
                    :class:`~fr.cnes.sirius.patrius.fieldsofview.AngularDistanceType`
        
            Returns:
                the angular distance
        
        
        """
        ...
    @typing.overload
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, angularDistanceType: AngularDistanceType) -> float: ...
    def getAngularOpening(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Get the angular opening of the Field Of View (FOV) over a given direction. Considering the half-plane containing both
            the main direction of the FOV and the input direction, the angular opening is defined as the angle between the main
            direction and the intersection of the FOV border with the half-plane.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView.getAngularOpening` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView`
        
            Parameters:
                directionIn (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                the angular opening along the input direction
        
        
        """
        ...
    def getMainDirection(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the main direction of the geometrical FOV. For every orthogonal section of the FOV, the main direction contains the
            center of such section.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView.getMainDirection` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IGeometricFieldOfView`
        
            Returns:
                The main direction of the FOV
        
        
        """
        ...
    def getName(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.getName` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Returns:
                the name of the field
        
        
        """
        ...
    def isInTheField(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView.isInTheField` in
                interface :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): a direction vector (expressed in the topocentric coordinate system of the object)
        
            Returns:
                true if the direction is in the field
        
        
        """
        ...
    def toString(self) -> str:
        """
            Get a representation for this infinite oblique circular cone. The given parameters are in the same order as in the
            constructor.
        
            Overrides:
                 in class 
        
            Returns:
                a representation for this infinite oblique circular cone
        
        
        """
        ...

class RectangleField(IGeometricFieldOfView):
    def __init__(self, string: str, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, double2: float): ...
    @typing.overload
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float: ...
    @typing.overload
    def getAngularDistance(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, angularDistanceType: AngularDistanceType) -> float: ...
    def getAngularOpening(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float: ...
    def getMainDirection(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getName(self) -> str: ...
    def getSideAxis(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D]: ...
    def getU(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getV(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getW(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def intersectUSide(self, double: float) -> bool: ...
    def isInTheField(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> bool: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.fieldsofview")``.

    AngularDistanceType: typing.Type[AngularDistanceType]
    AzimuthElevationField: typing.Type[AzimuthElevationField]
    BooleanField: typing.Type[BooleanField]
    CircularField: typing.Type[CircularField]
    EllipticField: typing.Type[EllipticField]
    FieldAngularFace: typing.Type[FieldAngularFace]
    IFieldOfView: typing.Type[IFieldOfView]
    IGeometricFieldOfView: typing.Type[IGeometricFieldOfView]
    InvertField: typing.Type[InvertField]
    OmnidirectionalField: typing.Type[OmnidirectionalField]
    PyramidalField: typing.Type[PyramidalField]
    RectangleField: typing.Type[RectangleField]
    SectorField: typing.Type[SectorField]
