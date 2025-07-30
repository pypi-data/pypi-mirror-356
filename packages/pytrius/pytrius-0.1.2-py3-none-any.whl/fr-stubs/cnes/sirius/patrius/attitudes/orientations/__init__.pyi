
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames.transformations
import fr.cnes.sirius.patrius.math.analysis.polynomials
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.time
import fr.cnes.sirius.patrius.utils.legs
import java.io
import typing



class OrientationAngleProvider(java.io.Serializable):
    """
    public interface OrientationAngleProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface represents an orientation angle provider model set. An orientation angle provider provides a way to
        compute an angle from a date and position-velocity local provider.
    
        Since:
            4.2
    """
    @staticmethod
    def build(univariateDateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction, typing.Callable]) -> 'OrientationAngleProvider':
        """
            Build an :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProvider` from this.
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction`): input function
        
            Returns:
                an orientation angle provider
        
        
        """
        ...
    def computeSpinByFD(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float: ...
    def computeSpinDerivativeByFD(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float: ...
    @staticmethod
    def computeSpinNumerical(double: float, double2: float, double3: float) -> float:
        """
            Computes the spin as a finite difference given two angles and the computation step between them.
        
            **WARNING** : It is considered that the difference between the two angle points used for the finite difference spin
            computation is never larger than π in the sense of the rotation
        
            Parameters:
                angle1 (double): Angle at t :sub:`1`
                angle2 (double): Angle at t :sub:`2`
                step (double): Computation step, elapsed time between t :sub:`1` and t :sub:`2`
        
            Returns:
                the Spin computed as finite difference
        
        
        """
        ...
    def getOrientationAngle(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...

class OrientationAngleTransform(fr.cnes.sirius.patrius.frames.transformations.TransformStateProvider):
    """
    public class OrientationAngleTransform extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.transformations.TransformStateProvider`
    
        One degree of liberty transform provider. It is defined by:
    
          - A reference transform which provides a reference orientation of the part
          - An axis which provides the rotation axis of the part
          -         An :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProvider` which provides an angle through time
    
    
        Since:
            4.4
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, transform: fr.cnes.sirius.patrius.frames.transformations.Transform, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, orientationAngleProvider: typing.Union[OrientationAngleProvider, typing.Callable]): ...
    def getAxis(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Returns the axis of the transform in the frame defined by the reference transform.
        
            Returns:
                the axis of the transform
        
        
        """
        ...
    def getOrientationAngleProvider(self) -> OrientationAngleProvider:
        """
            The orientation angle provider which provides an angle through time. The final transform is the reference transform +
            rotation around :meth:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleTransform.getAxis`.
        
            Returns:
                the orientation angle provider which provides an angle through time
        
        
        """
        ...
    def getReference(self) -> fr.cnes.sirius.patrius.frames.transformations.Transform:
        """
            Returns the reference transform. This is the transform return by the
            :meth:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleTransform.getTransform` method if the orientation
            angle is 0.
        
            Returns:
                the reference transform
        
        
        """
        ...
    def getTransform(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.frames.transformations.Transform: ...

class OrientationAngleLaw(OrientationAngleProvider):
    """
    public interface OrientationAngleLaw extends :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProvider`
    
        Interface that must be implemented by an orientation angle law, i.e. without an interval of validity.
    
        Since:
            4.2
    """
    ...

class OrientationAngleLeg(OrientationAngleProvider, fr.cnes.sirius.patrius.utils.legs.Leg):
    """
    public interface OrientationAngleLeg extends :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProvider`, :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
    
        Interface that must be implemented by an orientation angle provider which is also a leg, i.e. that has an interval of
        validity and a nature.
    
        Since:
            4.2
    """
    @staticmethod
    def build(univariateDateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction, typing.Callable], absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, string: str) -> 'OrientationAngleLeg':
        """
            Build an :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg` from this.
        
            Parameters:
                function (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction`): input function
                timeInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): leg's validity interval
                nature (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): leg nature
        
            Returns:
                an orientation angle leg
        
        
        """
        ...
    def computeSpinByFD(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float: ...
    def computeSpinDerivativeByFD(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> float: ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'OrientationAngleLeg':
        """
            Creates a new leg from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...

_OrientationAngleLegsSequence__L = typing.TypeVar('_OrientationAngleLegsSequence__L', bound=OrientationAngleLeg)  # <L>
class OrientationAngleLegsSequence(fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence[_OrientationAngleLegsSequence__L], OrientationAngleProvider, typing.Generic[_OrientationAngleLegsSequence__L]):
    """
    public class OrientationAngleLegsSequence<L extends :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg`> extends :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`<L> implements :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProvider`
    
        This class handles a sequence of one or several
        :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg`. This sequence can be handled as an
        :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence` of
        :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg`.
    
        Since:
            4.2
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_ORIENTATION_SEQUENCE_NATURE: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_ORIENTATION_SEQUENCE_NATURE
    
        Default nature.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'OrientationAngleLegsSequence'[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'OrientationAngleLegsSequence'[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def copy(self) -> fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence[_OrientationAngleLegsSequence__L]: ...
    def getNature(self) -> str:
        """
            Get the legs sequence nature.
        
            Returns:
                the nature
        
        
        """
        ...
    def getOrientationAngle(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Returns the time interval of the legs sequence.
        
            Null is returned if the sequence is empty.
        
            Warning: in case of sequences with holes, the sequence in the returned interval will not contain continuous data.
            Sequence is supposed to be continuous over time.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.getTimeInterval` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence.getTimeInterval` in
                class :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`
        
            Returns:
                the time interval of the legs sequence.
        
        
        """
        ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'OrientationAngleLegsSequence'[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'OrientationAngleLegsSequence'[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def head(self, l: _OrientationAngleLegsSequence__L) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'OrientationAngleLegsSequence'[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'OrientationAngleLegsSequence'[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'OrientationAngleLegsSequence'[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'OrientationAngleLegsSequence'[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def sub(self, l: _OrientationAngleLegsSequence__L, l2: _OrientationAngleLegsSequence__L) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'OrientationAngleLegsSequence'[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'OrientationAngleLegsSequence'[_OrientationAngleLegsSequence__L]: ...
    @typing.overload
    def tail(self, l: _OrientationAngleLegsSequence__L) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[_OrientationAngleLegsSequence__L]: ...
    def toPrettyString(self) -> str:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.toPrettyString` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.toPrettyString` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence.toPrettyString` in
                class :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`
        
            Returns:
                A nice :code:`String` representation.
        
        
        """
        ...

class AbstractOrientationAngleLeg(OrientationAngleLeg):
    """
    public abstract class AbstractOrientationAngleLeg extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg`
    
        This abstract class aims at defining all common features to classes representing the leg of an
        :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg`.
    
        Since:
            4.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval): ...
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, string: str): ...
    def getNature(self) -> str:
        """
            Returns the nature of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getNature` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                The “nature” of the leg.
        
        
        """
        ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Returns the time interval of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getTimeInterval` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                the time interval of the leg.
        
        
        """
        ...

class ConstantOrientationAngleLaw(OrientationAngleLaw):
    """
    public class ConstantOrientationAngleLaw extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLaw`
    
        This class aims at creating an orientation angle law whose orientation angle is constant.
    
        Since:
            4.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float): ...
    def getOrientationAngle(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...

class OrientationAngleProfile(OrientationAngleLeg):
    """
    public interface OrientationAngleProfile extends :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg`
    
        This interface gathers the classes that represents an orientation angle profile that can be harmonic or polynomial.
    
        Since:
            4.2
    """
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'OrientationAngleProfile':
        """
            Creates a new leg from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...

class AbstractOrientationAngleProfile(AbstractOrientationAngleLeg, OrientationAngleProfile):
    """
    public abstract class AbstractOrientationAngleProfile extends :class:`~fr.cnes.sirius.patrius.attitudes.orientations.AbstractOrientationAngleLeg` implements :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProfile`
    
        This abstract class aims at defining all common features to classes representing the angular velocities profile of an
        :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg`.
    
        Since:
            4.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval): ...
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, string: str): ...

class ConstantOrientationAngleLeg(AbstractOrientationAngleLeg):
    """
    public class ConstantOrientationAngleLeg extends :class:`~fr.cnes.sirius.patrius.attitudes.orientations.AbstractOrientationAngleLeg`
    
        This class aims at creation an orientation angle leg whose orientation angle is constant in its interval of validity.
    
        Since:
            4.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, double: float): ...
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, double: float, string: str): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'ConstantOrientationAngleLeg':
        """
            Creates a new leg from this one.
        
            Provided interval does not have to be included in current time interval.
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    def getOrientationAngle(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...

class OrientationAngleLawLeg(AbstractOrientationAngleLeg):
    """
    public class OrientationAngleLawLeg extends :class:`~fr.cnes.sirius.patrius.attitudes.orientations.AbstractOrientationAngleLeg`
    
        This class represents an :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLaw` on which an
        interval of validity is defined (whose borders are closed points).
    
        Since:
            4.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, orientationAngleLaw: typing.Union[OrientationAngleLaw, typing.Callable], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, orientationAngleLaw: typing.Union[OrientationAngleLaw, typing.Callable], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, string: str): ...
    @typing.overload
    def __init__(self, orientationAngleLaw: typing.Union[OrientationAngleLaw, typing.Callable], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, string: str, boolean: bool): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'OrientationAngleLawLeg':
        """
            Creates a new leg from this one.
        
            Provided interval does not have to be included in current time interval.
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    def getOrientationAngle(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...

class OrientationAngleProfileSequence(fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence[OrientationAngleProfile], OrientationAngleProfile):
    """
    public class OrientationAngleProfileSequence extends :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`<:class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProfile`> implements :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProfile`
    
        This class handles a sequence of one or several
        :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProfile`. This sequence can be handled as an
        :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence` of
        :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProfile`.
    
        Since:
            4.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'OrientationAngleProfileSequence':
        """
            Creates a new legs sequence from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleLeg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProfile.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.orientations.OrientationAngleProfile`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.copy` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence.copy` in
                class :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the legs sequence to create
        
            Returns:
                A new :code:`LegsSequence` valid on provided interval. Boundaries are not included in the new sequence.
        
            Creates a new legs sequence from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.copy` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence.copy` in
                class :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the legs sequence to create
                strict (boolean): true if boundaries shall not be included in the new sequence, false otherwise.
        
            Returns:
                A new :code:`LegsSequence` valid on provided interval
        
        
        """
        ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'OrientationAngleProfileSequence': ...
    @typing.overload
    def copy(self) -> fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    def getNature(self) -> str:
        """
            Returns the nature of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getNature` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                The “nature” of the leg.
        
        
        """
        ...
    def getOrientationAngle(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Returns the time interval of the legs sequence.
        
            Null is returned if the sequence is empty.
        
            Warning: in case of sequences with holes, the sequence in the returned interval will not contain continuous data.
            Sequence is supposed to be continuous.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getTimeInterval` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.getTimeInterval` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence.getTimeInterval` in
                class :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`
        
            Returns:
                the time interval of the legs sequence.
        
        
        """
        ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'OrientationAngleProfileSequence':
        """
            Returns a new sequence from the beginning to the given element.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.head` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence.head` in
                class :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`
        
            Parameters:
                toT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
                strict (boolean): true if boundary shall not be included in the extracted sequence, false otherwise.
        
            Returns:
                A new :code:`Sequence` object including all elements from the “beginning” to the given one (included only if
                :code:`strict` = false).
        
            Returns a new sequence from the beginning to the given element.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.head` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Parameters:
                toT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
        
            Returns:
                A new :code:`Sequence` object including all elements from the “beginning” to the given one (included).
        
        
        """
        ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'OrientationAngleProfileSequence': ...
    @typing.overload
    def head(self, l: fr.cnes.sirius.patrius.utils.legs.Leg) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'OrientationAngleProfileSequence':
        """
            Returns a new sequence extracted.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.sub` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence.sub` in
                class :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`
        
            Parameters:
                fromT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
                toT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
                strict (boolean): true if boundaries shall not be included in the extracted sequence, false otherwise.
        
            Returns:
                A new :code:`Sequence` object including all elements from the given one :code:`fromT` to the given one. Elements exactly
                on the interval boundaries are included only if :code:`strict` = false.
        
            Returns a new sequence extracted.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.sub` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Parameters:
                fromT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
                toT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
        
            Returns:
                A new :code:`Sequence` object including all elements from the given one :code:`fromT` to the given one :code:`toT` (both
                included).
        
            Returns a new sequence extracted.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.sub` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence.sub` in
                class :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): interval.
                strict (boolean): true if boundaries shall not be included in the extracted sequence, false otherwise.
        
            Returns:
                A new :code:`Sequence` object including all elements included in the :code:`interval` . Elements exactly on the interval
                boundaries are included only if :code:`strict` = false.
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'OrientationAngleProfileSequence': ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'OrientationAngleProfileSequence':
        """
            Returns a new sequence extracted.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.sub` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): interval.
        
            Returns:
                A new :code:`Sequence` object including all elements included in the :code:`interval` . Elements exactly on the interval
                boundaries are included.
        
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'OrientationAngleProfileSequence': ...
    @typing.overload
    def sub(self, l: fr.cnes.sirius.patrius.utils.legs.Leg, l2: fr.cnes.sirius.patrius.utils.legs.Leg) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'OrientationAngleProfileSequence':
        """
            Returns a new sequence from the given element to the end of the sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.tail` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence.tail` in
                class :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`
        
            Parameters:
                fromT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
                strict (boolean): true if boundary shall not be included in the extracted sequence, false otherwise.
        
            Returns:
                A new :code:`Sequence` object including all elements from the given one (included only if :code:`strict` = false) to the
                “end” of the sequence.
        
            Returns a new sequence from the given element to the end of the sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.tail` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Parameters:
                fromT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
        
            Returns:
                A new :code:`Sequence` object including all elements from the given one (included) to the “end” of the sequence.
        
        
        """
        ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'OrientationAngleProfileSequence': ...
    @typing.overload
    def tail(self, l: fr.cnes.sirius.patrius.utils.legs.Leg) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    def toPrettyString(self) -> str:
        """
            Returns a nice `null <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` representation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.toPrettyString` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.toPrettyString` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence.toPrettyString` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.TimeSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence.toPrettyString` in
                class :class:`~fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence`
        
            Returns:
                A nice :code:`String` representation.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.attitudes.orientations")``.

    AbstractOrientationAngleLeg: typing.Type[AbstractOrientationAngleLeg]
    AbstractOrientationAngleProfile: typing.Type[AbstractOrientationAngleProfile]
    ConstantOrientationAngleLaw: typing.Type[ConstantOrientationAngleLaw]
    ConstantOrientationAngleLeg: typing.Type[ConstantOrientationAngleLeg]
    OrientationAngleLaw: typing.Type[OrientationAngleLaw]
    OrientationAngleLawLeg: typing.Type[OrientationAngleLawLeg]
    OrientationAngleLeg: typing.Type[OrientationAngleLeg]
    OrientationAngleLegsSequence: typing.Type[OrientationAngleLegsSequence]
    OrientationAngleProfile: typing.Type[OrientationAngleProfile]
    OrientationAngleProfileSequence: typing.Type[OrientationAngleProfileSequence]
    OrientationAngleProvider: typing.Type[OrientationAngleProvider]
    OrientationAngleTransform: typing.Type[OrientationAngleTransform]
