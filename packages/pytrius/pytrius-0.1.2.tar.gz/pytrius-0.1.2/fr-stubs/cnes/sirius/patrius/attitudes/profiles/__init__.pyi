
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.analysis.polynomials
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.time
import fr.cnes.sirius.patrius.utils.legs
import java.io
import java.lang
import java.util
import typing



class AttitudeProfile(fr.cnes.sirius.patrius.attitudes.AttitudeLeg):
    """
    public interface AttitudeProfile extends :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
    
        Represents an attitude profile.
    
        Since:
            4.2
    """
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'AttitudeProfile':
        """
            Creates a new leg from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...

class AttitudeProfilesSequence(fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence[AttitudeProfile]):
    """
    public final class AttitudeProfilesSequence extends :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`<:class:`~fr.cnes.sirius.patrius.attitudes.profiles.AttitudeProfile`>
    
        This class handles a sequence of :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AttitudeProfile`.
    
        Since:
            4.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'AttitudeProfilesSequence':
        """
            Creates a new legs sequence from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.copy` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.copy` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the legs sequence to create
                strict (boolean): true if boundaries shall not be included in the new sequence, false otherwise.
        
            Returns:
                A new :code:`LegsSequence` valid on provided interval
        
            Creates a new legs sequence from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.copy` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.copy` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the legs sequence to create
        
            Returns:
                A new :code:`LegsSequence` valid on provided interval. Boundaries are not included in the new sequence.
        
        
        """
        ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'AttitudeProfilesSequence': ...
    @typing.overload
    def copy(self) -> fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Returns the time interval of the legs sequence.
        
            Null is returned if the sequence is empty.
        
            Warning: in case of sequences with holes, the sequence in the returned interval will not contain continuous data.
            Sequence is supposed to be continuous.
        
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
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'AttitudeProfilesSequence':
        """
            Returns a new sequence from the beginning to the given element.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.head` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.head` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
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
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.head` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                toT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
        
            Returns:
                A new :code:`Sequence` object including all elements from the “beginning” to the given one (included).
        
        
        """
        ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'AttitudeProfilesSequence': ...
    @typing.overload
    def head(self, l: fr.cnes.sirius.patrius.utils.legs.Leg) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.setSpinDerivativesComputation` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'AttitudeProfilesSequence':
        """
            Returns a new sequence extracted.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.sub` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
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
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
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
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): interval.
                strict (boolean): true if boundaries shall not be included in the extracted sequence, false otherwise.
        
            Returns:
                A new :code:`Sequence` object including all elements included in the :code:`interval` . Elements exactly on the interval
                boundaries are included only if :code:`strict` = false.
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'AttitudeProfilesSequence': ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'AttitudeProfilesSequence':
        """
            Returns a new sequence extracted.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.sub` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): interval.
        
            Returns:
                A new :code:`Sequence` object including all elements included in the :code:`interval` . Elements exactly on the interval
                boundaries are included.
        
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'AttitudeProfilesSequence': ...
    @typing.overload
    def sub(self, l: fr.cnes.sirius.patrius.utils.legs.Leg, l2: fr.cnes.sirius.patrius.utils.legs.Leg) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'AttitudeProfilesSequence':
        """
            Returns a new sequence from the given element to the end of the sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.tail` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.tail` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
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
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.tail` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                fromT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
        
            Returns:
                A new :code:`Sequence` object including all elements from the given one (included) to the “end” of the sequence.
        
        
        """
        ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'AttitudeProfilesSequence': ...
    @typing.overload
    def tail(self, l: fr.cnes.sirius.patrius.utils.legs.Leg) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
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

class QuaternionDatePolynomialSegment(java.io.Serializable):
    """
    public final class QuaternionDatePolynomialSegment extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class represents a quaternion polynomial guidance profile on a segment.
    
        Since:
            4.11
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, datePolynomialFunctionInterface: fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface, datePolynomialFunctionInterface2: fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface, datePolynomialFunctionInterface3: fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface, datePolynomialFunctionInterface4: fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool): ...
    def getOrientation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation:
        """
            Get the orientation from the quaternion polynomials at a given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the date at which we want to get the orientation from the quaternion polynomials
        
            Returns:
                the orientation from the quaternion polynomials at the given date
        
        
        """
        ...
    def getQ0Polynomial(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface:
        """
            Getter for the polynomial function of date representing the q0 quaternion component.
        
            Returns:
                the polynomial function of date representing the q0 quaternion component
        
        
        """
        ...
    def getQ1Polynomial(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface:
        """
            Getter for the polynomial function of date representing the q1 quaternion component.
        
            Returns:
                the polynomial function of date representing the q1 quaternion component
        
        
        """
        ...
    def getQ2Polynomial(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface:
        """
            Getter for the polynomial function of date representing the q2 quaternion component.
        
            Returns:
                the polynomial function of date representing the q2 quaternion component
        
        
        """
        ...
    def getQ3Polynomial(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.DatePolynomialFunctionInterface:
        """
            Getter for the polynomial function of date representing the q3 quaternion component.
        
            Returns:
                the polynomial function of date representing the q3 quaternion component
        
        
        """
        ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Get the time interval of the guidance profile segment.
        
            Returns:
                the time interval of the guidance profile segment
        
        
        """
        ...

class QuaternionPolynomialSegment(java.io.Serializable):
    """
    public final class QuaternionPolynomialSegment extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class represents a quaternion polynomial guidance profile on a segment.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, polynomialChebyshevFunction: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialChebyshevFunction, polynomialChebyshevFunction2: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialChebyshevFunction, polynomialChebyshevFunction3: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialChebyshevFunction, polynomialChebyshevFunction4: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialChebyshevFunction, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool): ...
    @typing.overload
    def __init__(self, polynomialFunction: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction2: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction3: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction4: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool): ...
    @typing.overload
    def __init__(self, polynomialFunction: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction2: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction3: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction4: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool): ...
    @typing.overload
    def __init__(self, polynomialFunctionLagrangeForm: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunctionLagrangeForm, polynomialFunctionLagrangeForm2: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunctionLagrangeForm, polynomialFunctionLagrangeForm3: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunctionLagrangeForm, polynomialFunctionLagrangeForm4: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunctionLagrangeForm, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool): ...
    @typing.overload
    def __init__(self, polynomialFunctionLagrangeForm: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunctionLagrangeForm, polynomialFunctionLagrangeForm2: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunctionLagrangeForm, polynomialFunctionLagrangeForm3: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunctionLagrangeForm, polynomialFunctionLagrangeForm4: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunctionLagrangeForm, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool): ...
    def getOrientation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation:
        """
            Get the orientation from the quaternion polynomials at a given date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the date
        
            Returns:
                the orientation at a given date
        
        
        """
        ...
    def getQ0Coefficients(self) -> typing.MutableSequence[float]:
        """
        
            Returns:
                the coefficients of the polynomial function representing q0.
        
        
        """
        ...
    def getQ1Coefficients(self) -> typing.MutableSequence[float]:
        """
        
            Returns:
                the coefficients of the polynomial function representing q1.
        
        
        """
        ...
    def getQ2Coefficients(self) -> typing.MutableSequence[float]:
        """
        
            Returns:
                the coefficients of the polynomial function representing q2.
        
        
        """
        ...
    def getQ3Coefficients(self) -> typing.MutableSequence[float]:
        """
        
            Returns:
                the coefficients of the polynomial function representing q3.
        
        
        """
        ...
    def getTimeInterval(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateInterval:
        """
            Get the time interval of the guidance profile segment.
        
            Returns:
                the time interval of the guidance profile segment.
        
        
        """
        ...

class TimeStampedRotation(fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, fr.cnes.sirius.patrius.time.TimeStamped):
    """
    public final class TimeStampedRotation extends :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
    
        :class:`~fr.cnes.sirius.patrius.time.TimeStamped` version of
        :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation`.
    
        Since:
            4.4
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation.equals` in
                class :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation`
        
        
        """
        ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                date attached to the object
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get the hash code for the time-stamped rotation object.
        
            Based on *Josh Bloch*'s ***Effective Java***, Item 8
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation.hashCode` in
                class :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation`
        
            Returns:
                the hash code
        
        
        """
        ...

class AbstractAttitudeProfile(AttitudeProfile):
    """
    public abstract class AbstractAttitudeProfile extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AttitudeProfile`
    
        This class provides implementations for classes implementing
        :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AttitudeProfile`.
    
        Since:
            4.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval): ...
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, double: float): ...
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, string: str): ...
    @typing.overload
    def __init__(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, string: str, double: float): ...
    def checkDate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def getNature(self) -> str:
        """
            Returns the nature of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getNature` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Returns:
                The “nature” of the leg.
        
        
        """
        ...
    def getSpinDeltaT(self) -> float:
        """
            Returns the delta-t used for spin computation by finite differences.
        
            Returns:
                the delta-t used for spin computation by finite differences
        
        
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

class AngularVelocitiesPolynomialProfile(fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence['AngularVelocitiesPolynomialProfileLeg'], AttitudeProfile):
    """
    public class AngularVelocitiesPolynomialProfile extends :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`<:class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfileLeg`> implements :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AttitudeProfile`
    
    
        An attitude angular velocities profile sequence, whose x-y-z components are represented with polynomial functions.
    
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, list: java.util.List['AngularVelocitiesPolynomialProfileLeg']): ...
    @typing.overload
    def __init__(self, list: java.util.List['AngularVelocitiesPolynomialProfileLeg'], string: str): ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'AngularVelocitiesPolynomialProfile':
        """
            Creates a new legs sequence from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AttitudeProfile.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AttitudeProfile`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.copy` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.copy` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the legs sequence to create
        
            Returns:
                A new :code:`LegsSequence` valid on provided interval. Boundaries are not included in the new sequence.
        
            Creates a new legs sequence from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.copy` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.copy` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the legs sequence to create
                strict (boolean): true if boundaries shall not be included in the new sequence, false otherwise.
        
            Returns:
                A new :code:`LegsSequence` valid on provided interval
        
        
        """
        ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'AngularVelocitiesPolynomialProfile': ...
    @typing.overload
    def copy(self) -> fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
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
    def getXCoefficients(self) -> java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, typing.MutableSequence[float]]: ...
    def getYCoefficients(self) -> java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, typing.MutableSequence[float]]: ...
    def getZCoefficients(self) -> java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, typing.MutableSequence[float]]: ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'AngularVelocitiesPolynomialProfile':
        """
            Returns a new sequence from the beginning to the given element.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.head` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.head` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
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
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.head` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                toT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
        
            Returns:
                A new :code:`Sequence` object including all elements from the “beginning” to the given one (included).
        
        
        """
        ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'AngularVelocitiesPolynomialProfile': ...
    @typing.overload
    def head(self, l: fr.cnes.sirius.patrius.utils.legs.Leg) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider.setSpinDerivativesComputation` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeProvider`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.setSpinDerivativesComputation` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'AngularVelocitiesPolynomialProfile':
        """
            Returns a new sequence extracted.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.sub` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
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
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
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
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): interval.
                strict (boolean): true if boundaries shall not be included in the extracted sequence, false otherwise.
        
            Returns:
                A new :code:`Sequence` object including all elements included in the :code:`interval` . Elements exactly on the interval
                boundaries are included only if :code:`strict` = false.
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'AngularVelocitiesPolynomialProfile': ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'AngularVelocitiesPolynomialProfile':
        """
            Returns a new sequence extracted.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.sub` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): interval.
        
            Returns:
                A new :code:`Sequence` object including all elements included in the :code:`interval` . Elements exactly on the interval
                boundaries are included.
        
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'AngularVelocitiesPolynomialProfile': ...
    @typing.overload
    def sub(self, l: fr.cnes.sirius.patrius.utils.legs.Leg, l2: fr.cnes.sirius.patrius.utils.legs.Leg) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'AngularVelocitiesPolynomialProfile':
        """
            Returns a new sequence from the given element to the end of the sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.tail` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.tail` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
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
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence.tail` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.StrictAttitudeLegsSequence`
        
            Parameters:
                fromT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
        
            Returns:
                A new :code:`Sequence` object including all elements from the given one (included) to the “end” of the sequence.
        
        
        """
        ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'AngularVelocitiesPolynomialProfile': ...
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

class AbstractAngularVelocitiesAttitudeProfile(AbstractAttitudeProfile):
    """
    public abstract class AbstractAngularVelocitiesAttitudeProfile extends :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AbstractAttitudeProfile`
    
    
        An attitude profile which is defined by its angular velocity whose x-y-z components are represented with an underlying
        :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3DFunction`. The attitude orientation is computed
        integrating that angular velocity.
    
        Since:
            4.4
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, vector3DFunction: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3DFunction, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, angularVelocityIntegrationType: 'AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType', double: float, int: int, string: str): ...
    @typing.overload
    def __init__(self, vector3DFunction: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3DFunction, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, angularVelocityIntegrationType: 'AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType', double: float, string: str): ...
    def clearCache(self) -> None:
        """
            Removes all of the elements from the orientation rotation cache
        
        """
        ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...
    class AngularVelocityIntegrationType(java.lang.Enum['AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType']):
        WILCOX_1: typing.ClassVar['AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType'] = ...
        WILCOX_2: typing.ClassVar['AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType'] = ...
        WILCOX_3: typing.ClassVar['AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType'] = ...
        WILCOX_4: typing.ClassVar['AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType'] = ...
        EDWARDS: typing.ClassVar['AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType']: ...

class AngularVelocitiesPolynomialSlew(AngularVelocitiesPolynomialProfile, fr.cnes.sirius.patrius.attitudes.Slew):
    """
    public class AngularVelocitiesPolynomialSlew extends :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile` implements :class:`~fr.cnes.sirius.patrius.attitudes.Slew`
    
    
        An attitude angular velocities profile slew, whose x-y-z components are represented with polynomial functions.
    
    
        Since:
            4.5
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, list: java.util.List['AngularVelocitiesPolynomialProfileLeg']): ...
    @typing.overload
    def __init__(self, list: java.util.List['AngularVelocitiesPolynomialProfileLeg'], string: str): ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'AngularVelocitiesPolynomialSlew':
        """
            Creates a new legs sequence from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.AttitudeLeg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AttitudeProfile.copy` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AttitudeProfile`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.Slew.copy` in interface :class:`~fr.cnes.sirius.patrius.attitudes.Slew`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.copy` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.copy` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile.copy` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the legs sequence to create
        
            Returns:
                A new :code:`LegsSequence` valid on provided interval. Boundaries are not included in the new sequence.
        
            Creates a new legs sequence from this one.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.copy` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile.copy` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile`
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the legs sequence to create
                strict (boolean): true if boundaries shall not be included in the new sequence, false otherwise.
        
            Returns:
                A new :code:`LegsSequence` valid on provided interval
        
        
        """
        ...
    @typing.overload
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'AngularVelocitiesPolynomialSlew': ...
    @typing.overload
    def copy(self) -> fr.cnes.sirius.patrius.utils.legs.StrictLegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'AngularVelocitiesPolynomialSlew':
        """
            Returns a new sequence from the beginning to the given element.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.head` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile.head` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile`
        
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
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile.head` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile`
        
            Parameters:
                toT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
        
            Returns:
                A new :code:`Sequence` object including all elements from the “beginning” to the given one (included).
        
        
        """
        ...
    @typing.overload
    def head(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'AngularVelocitiesPolynomialSlew': ...
    @typing.overload
    def head(self, l: fr.cnes.sirius.patrius.utils.legs.Leg) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'AngularVelocitiesPolynomialSlew':
        """
            Returns a new sequence extracted.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.sub` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile`
        
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
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile`
        
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
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile`
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): interval.
                strict (boolean): true if boundaries shall not be included in the extracted sequence, false otherwise.
        
            Returns:
                A new :code:`Sequence` object including all elements included in the :code:`interval` . Elements exactly on the interval
                boundaries are included only if :code:`strict` = false.
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'AngularVelocitiesPolynomialSlew': ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'AngularVelocitiesPolynomialSlew':
        """
            Returns a new sequence extracted.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.sub` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile.sub` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile`
        
            Parameters:
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): interval.
        
            Returns:
                A new :code:`Sequence` object including all elements included in the :code:`interval` . Elements exactly on the interval
                boundaries are included.
        
        
        """
        ...
    @typing.overload
    def sub(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, boolean: bool) -> 'AngularVelocitiesPolynomialSlew': ...
    @typing.overload
    def sub(self, l: fr.cnes.sirius.patrius.utils.legs.Leg, l2: fr.cnes.sirius.patrius.utils.legs.Leg) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'AngularVelocitiesPolynomialSlew':
        """
            Returns a new sequence from the given element to the end of the sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence.tail` in
                interface :class:`~fr.cnes.sirius.patrius.utils.legs.LegsSequence`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile.tail` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile`
        
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
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile.tail` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AngularVelocitiesPolynomialProfile`
        
            Parameters:
                fromT (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): Any element of this sequence.
        
            Returns:
                A new :code:`Sequence` object including all elements from the given one (included) to the “end” of the sequence.
        
        
        """
        ...
    @typing.overload
    def tail(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> 'AngularVelocitiesPolynomialSlew': ...
    @typing.overload
    def tail(self, l: fr.cnes.sirius.patrius.utils.legs.Leg) -> fr.cnes.sirius.patrius.utils.legs.LegsSequence[fr.cnes.sirius.patrius.utils.legs.Leg]: ...

class QuaternionDatePolynomialProfile(AbstractAttitudeProfile):
    """
    public class QuaternionDatePolynomialProfile extends :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AbstractAttitudeProfile`
    
        Represents a quaternion guidance profile, computed with polynomial functions.
    
        Since:
            4.11
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, list: java.util.List[QuaternionDatePolynomialSegment]): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, list: java.util.List[QuaternionDatePolynomialSegment], double: float): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, list: java.util.List[QuaternionDatePolynomialSegment], string: str): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, list: java.util.List[QuaternionDatePolynomialSegment], string: str, double: float): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'QuaternionDatePolynomialProfile':
        """
            Creates a new leg from this one.
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    def getReferenceFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Returns the reference frame of the polynomial functions.
        
            Returns:
                the reference frame of the polynomial functions
        
        
        """
        ...
    def getSegment(self, int: int) -> QuaternionDatePolynomialSegment:
        """
            Return an individual segment of the list, specified by the index.
        
            Parameters:
                indexSegment (int): index of the segment
        
            Returns:
                the individual segment
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if the index of the segment is not compatible with the segments list size
        
        
        """
        ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...
    def size(self) -> int:
        """
            Return the size of the segments list.
        
            Returns:
                the size of the segments list
        
        
        """
        ...

class QuaternionHarmonicProfile(AbstractAttitudeProfile):
    """
    public final class QuaternionHarmonicProfile extends :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AbstractAttitudeProfile`
    
        Represents a quaternion guidance profile, calculated with Fourier series.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, fourierSeries: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries2: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries3: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries4: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, fourierSeries: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries2: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries3: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries4: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, double: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame, fourierSeries: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries2: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries3: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries4: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, string: str, double: float): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'QuaternionHarmonicProfile':
        """
            Creates a new leg from this one.
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    def getAngularFrequencies(self) -> typing.MutableSequence[float]:
        """
        
            Returns:
                the angular frequencies of the four Fourier series representing q0, q1, q2 qnd q3.
        
        
        """
        ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    def getConstants(self) -> typing.MutableSequence[float]:
        """
        
            Returns:
                the a0 coefficients of the four Fourier series representing q0, q1, q2 qnd q3.
        
        
        """
        ...
    def getCosArrays(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
        
            Returns:
                the a coefficients of the four Fourier series representing q0, q1, q2 qnd q3.
        
        
        """
        ...
    def getNature(self) -> str:
        """
            Returns the nature of the leg.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.utils.legs.Leg.getNature` in interface :class:`~fr.cnes.sirius.patrius.utils.legs.Leg`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.attitudes.profiles.AbstractAttitudeProfile.getNature` in
                class :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AbstractAttitudeProfile`
        
            Returns:
                The “nature” of the leg.
        
        
        """
        ...
    def getQ0FourierSeries(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries:
        """
        
            Returns:
                the Fourier series representing the q0 quaternion component.
        
        
        """
        ...
    def getQ1FourierSeries(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries:
        """
        
            Returns:
                the Fourier series representing the q1 quaternion component.
        
        
        """
        ...
    def getQ2FourierSeries(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries:
        """
        
            Returns:
                the Fourier series representing the q2 quaternion component.
        
        
        """
        ...
    def getQ3FourierSeries(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries:
        """
        
            Returns:
                the Fourier series representing the q3 quaternion component.
        
        
        """
        ...
    def getSinArrays(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
        
            Returns:
                the b coefficients of the four Fourier series representing q0, q1, q2 qnd q3.
        
        
        """
        ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...

class QuaternionPolynomialProfile(AbstractAttitudeProfile):
    """
    public class QuaternionPolynomialProfile extends :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AbstractAttitudeProfile`
    
        Represents a quaternion guidance profile, calculated with polynomial functions
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, list: java.util.List[QuaternionPolynomialSegment]): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, list: java.util.List[QuaternionPolynomialSegment], double: float): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, list: java.util.List[QuaternionPolynomialSegment], string: str): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, list: java.util.List[QuaternionPolynomialSegment], string: str, double: float): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'QuaternionPolynomialProfile':
        """
            Creates a new leg from this one.
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    @typing.overload
    def getAttitude(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    def getQ0Coefficients(self) -> java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, typing.MutableSequence[float]]: ...
    def getQ1Coefficients(self) -> java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, typing.MutableSequence[float]]: ...
    def getQ2Coefficients(self) -> java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, typing.MutableSequence[float]]: ...
    def getQ3Coefficients(self) -> java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, typing.MutableSequence[float]]: ...
    def getReferenceFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Returns the reference frame of the polynomial functions.
        
            Returns:
                the reference frame of the polynomial functions
        
        
        """
        ...
    def setSpinDerivativesComputation(self, boolean: bool) -> None:
        """
            Method to activate spin derivative computation.
        
            Parameters:
                computeSpinDerivatives (boolean): true if spin derivatives should be computed
        
        
        """
        ...

class AngularVelocitiesHarmonicProfile(AbstractAngularVelocitiesAttitudeProfile):
    """
    public class AngularVelocitiesHarmonicProfile extends :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AbstractAngularVelocitiesAttitudeProfile`
    
    
        An attitude angular velocities profile, whose x-y-z components are represented with Fourier series.
    
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, fourierSeries: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries2: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries3: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, angularVelocityIntegrationType: AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType, double: float): ...
    @typing.overload
    def __init__(self, fourierSeries: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries2: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries3: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, angularVelocityIntegrationType: AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType, double: float, int: int): ...
    @typing.overload
    def __init__(self, fourierSeries: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries2: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries3: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, angularVelocityIntegrationType: AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType, double: float, int: int, string: str): ...
    @typing.overload
    def __init__(self, fourierSeries: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries2: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, fourierSeries3: fr.cnes.sirius.patrius.math.analysis.polynomials.FourierSeries, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, angularVelocityIntegrationType: AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType, double: float, string: str): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'AngularVelocitiesHarmonicProfile':
        """
            Creates a new leg from this one.
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    def getAngularFrequencies(self) -> typing.MutableSequence[float]:
        """
            Gets the angular frequencies of the three Fourier series representing x, y and z.
        
            Returns:
                the angular frequencies
        
        
        """
        ...
    def getConstants(self) -> typing.MutableSequence[float]:
        """
            Gets the :code:`a0` coefficients of the three Fourier series representing x, y and z.
        
            Returns:
                the :code:`a0` coefficients
        
        
        """
        ...
    def getCosArrays(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Gets the :code:`a` coefficients of the three Fourier series representing x, y and z.
        
            Returns:
                the :code:`a` coefficients of the three Fourier series representing x, y and z.
        
        
        """
        ...
    def getSinArrays(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Gets the :code:`b` coefficients of the three Fourier series representing x, y and z.
        
            Returns:
                the :code:`b` coefficients of the three Fourier series representing x, y and z.
        
        
        """
        ...
    def getSize(self) -> int:
        """
            Gets the size of the Fourierseries3DFunction, ie 3.
        
            Returns:
                3.
        
        
        """
        ...

class AngularVelocitiesPolynomialProfileLeg(AbstractAngularVelocitiesAttitudeProfile):
    """
    public class AngularVelocitiesPolynomialProfileLeg extends :class:`~fr.cnes.sirius.patrius.attitudes.profiles.AbstractAngularVelocitiesAttitudeProfile`
    
    
        An attitude angular velocities profile leg, whose x-y-z components are represented with polynomial functions.
    
    
        Since:
            4.4
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, polynomialFunction: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction2: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction3: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, angularVelocityIntegrationType: AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType, double: float): ...
    @typing.overload
    def __init__(self, polynomialFunction: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction2: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction3: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, angularVelocityIntegrationType: AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType, double: float, int: int): ...
    @typing.overload
    def __init__(self, polynomialFunction: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction2: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction3: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, angularVelocityIntegrationType: AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType, double: float, int: int, string: str): ...
    @typing.overload
    def __init__(self, polynomialFunction: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction2: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, polynomialFunction3: fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval, rotation: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, angularVelocityIntegrationType: AbstractAngularVelocitiesAttitudeProfile.AngularVelocityIntegrationType, double: float, string: str): ...
    def copy(self, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> 'AngularVelocitiesPolynomialProfileLeg':
        """
            Creates a new leg from this one.
        
            Parameters:
                newInterval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): The time interval of the leg to create
        
            Returns:
                A new :code:`Leg` valid on provided interval
        
        
        """
        ...
    def getDateZero(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date zero of the polynomial functions.
        
            Returns:
                the date zero of the polynomial functions.
        
        
        """
        ...
    def getSize(self) -> int:
        """
            Gets the size of the Fourierseries3DFunction, ie 3.
        
            Returns:
                3.
        
        
        """
        ...
    def getXCoefficients(self) -> typing.MutableSequence[float]:
        """
            Gets the coefficients of the polynomial function representing x angular rate.
        
            Returns:
                the coefficients of the polynomial function representing x
        
        
        """
        ...
    def getYCoefficients(self) -> typing.MutableSequence[float]:
        """
            Gets the coefficients of the polynomial function representing y angular rate.
        
            Returns:
                the coefficients of the polynomial function representing y
        
        
        """
        ...
    def getZCoefficients(self) -> typing.MutableSequence[float]:
        """
            Gets the coefficients of the polynomial function representing z angular rate.
        
            Returns:
                the coefficients of the polynomial function representing z
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.attitudes.profiles")``.

    AbstractAngularVelocitiesAttitudeProfile: typing.Type[AbstractAngularVelocitiesAttitudeProfile]
    AbstractAttitudeProfile: typing.Type[AbstractAttitudeProfile]
    AngularVelocitiesHarmonicProfile: typing.Type[AngularVelocitiesHarmonicProfile]
    AngularVelocitiesPolynomialProfile: typing.Type[AngularVelocitiesPolynomialProfile]
    AngularVelocitiesPolynomialProfileLeg: typing.Type[AngularVelocitiesPolynomialProfileLeg]
    AngularVelocitiesPolynomialSlew: typing.Type[AngularVelocitiesPolynomialSlew]
    AttitudeProfile: typing.Type[AttitudeProfile]
    AttitudeProfilesSequence: typing.Type[AttitudeProfilesSequence]
    QuaternionDatePolynomialProfile: typing.Type[QuaternionDatePolynomialProfile]
    QuaternionDatePolynomialSegment: typing.Type[QuaternionDatePolynomialSegment]
    QuaternionHarmonicProfile: typing.Type[QuaternionHarmonicProfile]
    QuaternionPolynomialProfile: typing.Type[QuaternionPolynomialProfile]
    QuaternionPolynomialSegment: typing.Type[QuaternionPolynomialSegment]
    TimeStampedRotation: typing.Type[TimeStampedRotation]
