
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.forces
import fr.cnes.sirius.patrius.forces.gravity.grid
import fr.cnes.sirius.patrius.forces.gravity.potential
import fr.cnes.sirius.patrius.forces.gravity.tides
import fr.cnes.sirius.patrius.forces.gravity.variations
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.analysis.polynomials
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import jpype
import typing



class AbstractBodyAttraction(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable, fr.cnes.sirius.patrius.forces.ForceModel, fr.cnes.sirius.patrius.forces.GradientModel):
    """
    public abstract class AbstractBodyAttraction extends :class:`~fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
    
        Abstract body attraction force model.
    
        Also see:
            :meth:`~serialized`
    """
    K_FACTOR: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` K_FACTOR
    
        Parameter name for central attraction coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, gravityModel: 'GravityModel', boolean: bool, double: float): ...
    @typing.overload
    def __init__(self, gravityModel: 'GravityModel', boolean: bool, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    @typing.overload
    def addDAccDParam(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    def addDAccDState(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    @typing.overload
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientPosition` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def computeGradientVelocity(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to velocity have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientVelocity` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def getEventsDetectors(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.events.EventDetector]:
        """
            Get the discrete events related to the model.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.ForceModel.getEventsDetectors` in
                interface :class:`~fr.cnes.sirius.patrius.forces.ForceModel`
        
            Returns:
                array of events detectors or null if the model is not related to any discrete events
        
        
        """
        ...
    def getGravityModel(self) -> 'GravityModel':
        """
            Get the gravitational attraction model.
        
            Returns:
                the gravitational attraction model
        
        
        """
        ...
    def getMultiplicativeFactor(self) -> float:
        """
            Get the force multiplicative factor.
        
            Returns:
                the force multiplicative factor
        
        
        """
        ...
    def getMultiplicativeFactorParameter(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Get the force multiplicative factor parameter
        
            Returns:
                the force multiplicative factor parameter
        
        
        """
        ...
    def setMultiplicativeFactor(self, double: float) -> None:
        """
            Set the multiplicative factor.
        
            Parameters:
                factor (double): the force multiplicative factor to set.
        
        
        """
        ...

class EarthGravitationalModelFactory:
    """
    public final class EarthGravitationalModelFactory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
    
        Factory class for earth gravitational model. This factory provides earth gravitational model by giving the potential
        file name, the degree and the order.
    
        Since:
            2.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.gravity.BalminoGravityModel`,
            :class:`~fr.cnes.sirius.patrius.forces.gravity.CunninghamGravityModel`,
            :class:`~fr.cnes.sirius.patrius.forces.gravity.DrozinerGravityModel`,
            :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.GravityFieldFactory`
    """
    @staticmethod
    def getBalmino(gravityFieldNames: 'EarthGravitationalModelFactory.GravityFieldNames', string: str, int: int, int2: int, boolean: bool) -> 'GravityModel': ...
    @staticmethod
    def getCunningham(gravityFieldNames: 'EarthGravitationalModelFactory.GravityFieldNames', string: str, int: int, int2: int, boolean: bool) -> 'GravityModel': ...
    @staticmethod
    def getDroziner(gravityFieldNames: 'EarthGravitationalModelFactory.GravityFieldNames', string: str, int: int, int2: int, boolean: bool) -> 'GravityModel': ...
    @typing.overload
    @staticmethod
    def getGravitationalModel(gravityFieldNames: 'EarthGravitationalModelFactory.GravityFieldNames', string: str, int: int, int2: int) -> 'GravityModel': ...
    @typing.overload
    @staticmethod
    def getGravitationalModel(gravityFieldNames: 'EarthGravitationalModelFactory.GravityFieldNames', string: str, int: int, int2: int, boolean: bool) -> 'GravityModel': ...
    class GravityFieldNames(java.lang.Enum['EarthGravitationalModelFactory.GravityFieldNames']):
        ICGEM: typing.ClassVar['EarthGravitationalModelFactory.GravityFieldNames'] = ...
        SHM: typing.ClassVar['EarthGravitationalModelFactory.GravityFieldNames'] = ...
        EGM: typing.ClassVar['EarthGravitationalModelFactory.GravityFieldNames'] = ...
        GRGS: typing.ClassVar['EarthGravitationalModelFactory.GravityFieldNames'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'EarthGravitationalModelFactory.GravityFieldNames': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['EarthGravitationalModelFactory.GravityFieldNames']: ...

class GravityModel(java.io.Serializable):
    """
    public interface GravityModel extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface represents a gravitational attraction model.
    
        Since:
            4.11
    """
    def computeAcceleration(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeDAccDPos(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getBodyFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the central body frame.
        
            Returns:
                the bodyFrame
        
        
        """
        ...
    def getMu(self) -> float:
        """
            Get the central attraction coefficient.
        
            Returns:
                central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
        
        """
        ...
    def setMu(self, double: float) -> None:
        """
            Set the central attraction coefficient.
        
            Parameters:
                muIn (double): the central attraction coefficient.
        
        
        """
        ...

class GravityToolbox:
    """
    public final class GravityToolbox extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Toolbox for tides.
    
        Since:
            1.2
    """
    @staticmethod
    def computeBalminoAcceleration(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double3: float, double4: float, int: int, int2: int, helmholtzPolynomial: fr.cnes.sirius.patrius.math.analysis.polynomials.HelmholtzPolynomial) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Method to compute the acceleration, from Balmino algorithm (see
            :class:`~fr.cnes.sirius.patrius.forces.gravity.BalminoGravityModel`).
        
            Parameters:
                positionInBodyFrame (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): Position of the spacecraft in the body frame
                coefficientsC (double[][]): array of "C" coeffs
                coefficientsS (double[][]): array of "S" coeffs
                muc (double): Central body attraction coefficient
                eqRadius (double): Reference equatorial radius of the potential
                degree (int): Number of zonal coefficients
                order (int): Number of tesseral coefficients
                helm (:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.HelmholtzPolynomial`): Helmholtz polynomial
        
            Returns:
                acceleration vector
        
        
        """
        ...
    @staticmethod
    def computeCunninghamAcceleration(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], int: int, int2: int, double4: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
        
            Method to compute the acceleration. This method has been implemented in order to validate the force model only. The
            reason is that for the validation context, we do not want to set up an instance of the SpacecraftState object to avoid
            the inertial frame of the spacecraft orbit.
            Method taken from :class:`~fr.cnes.sirius.patrius.forces.gravity.CunninghamGravityModel`
        
            Parameters:
                positionInBodyFrame (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): Position of the spacecraft in the body frame
                equatorialRadius (double): equatorial radius of earth
                coefC (double[][]): C coefficients array
                coefS (double[][]): S coefficients array
                degree (int): degree
                order (int): order
                mu (double): gravitation constant
        
            Returns:
                acceleration vector
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.forces.gravity.CunninghamGravityModel`
        
        
        """
        ...
    @staticmethod
    def computeDAccDPos(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, double2: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Compute the partial derivatives of the acceleration (Cunningham algorithm) with respect to the position.
        
            Parameters:
                positionInBodyFrame (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): Position of the spacecraft in the body frame
                equatorialRadius (double): equatorial radius
                mu (double): gravitational parameter
                c (double[][]): C coefficients
                s (double[][]): S coefficients
        
            Returns:
                array of the partial derivatives See the following article : "On the computation of spherical harmonic terms needed
                during the numerical integration of the orbital motion of an artifical satellite" , Leland E. Cunningham
        
        
        """
        ...
    @staticmethod
    def computeDrozinerAcceleration(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double3: float, double4: float, double5: float, int: int, int2: int) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @staticmethod
    def deNormalize(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Denormalize an array of coefficients.
        
            Parameters:
                tab (double[][]): normalized coefficients array
        
            Returns:
                unnormalized coefficients array
        
        
        """
        ...
    @staticmethod
    def normalize(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Normalize an array of coefficients.
        
            Parameters:
                tab (double[][]): normalized coefficients array
        
            Returns:
                unnormalized coefficients array
        
        
        """
        ...
    @staticmethod
    def unNormalize(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Unnormalize a coefficients array.
        
            Parameters:
                normalized (double[][]): normalized coefficients array
        
            Returns:
                unnormalized array
        
        
        """
        ...

class AbstractGravityModel(GravityModel):
    """
    public abstract class AbstractGravityModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel`
    
        This class represents a gravitational attraction model.
    
        Since:
            2.3
    
        Also see:
            :meth:`~serialized`
    """
    MU: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` MU
    
        Parameter name for central attraction coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def getBodyFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the central body frame.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel.getBodyFrame` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel`
        
            Returns:
                the bodyFrame
        
        
        """
        ...
    def getMu(self) -> float:
        """
            Get the central attraction coefficient.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel.getMu` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel`
        
            Returns:
                central attraction coefficient (m :sup:`3` /s :sup:`2` )
        
        
        """
        ...
    def getMuParameter(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Returns the gravitational coefficient as a parameter.
        
            Returns:
                the gravitational coefficient as a parameter
        
        
        """
        ...
    def setMu(self, double: float) -> None:
        """
            Set the central attraction coefficient.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel.setMu` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel`
        
            Parameters:
                muIn (double): the central attraction coefficient.
        
        
        """
        ...

class DirectBodyAttraction(AbstractBodyAttraction):
    """
    public class DirectBodyAttraction extends :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractBodyAttraction`
    
        Direct body attraction force model.
    
        The implementation of this class enables the computation of partial derivatives by finite differences with respect to
        the **central attraction coefficient**.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, gravityModel: GravityModel): ...
    @typing.overload
    def __init__(self, gravityModel: GravityModel, boolean: bool): ...
    @typing.overload
    def __init__(self, gravityModel: GravityModel, boolean: bool, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class ThirdBodyAttraction(AbstractBodyAttraction):
    """
    public class ThirdBodyAttraction extends :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractBodyAttraction`
    
        Third body attraction force model.
    
        The implementation of this class enables the computation of partial derivatives by finite differences with respect to
        the **central attraction coefficient**.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, gravityModel: GravityModel): ...
    @typing.overload
    def __init__(self, gravityModel: GravityModel, boolean: bool): ...
    @typing.overload
    def __init__(self, gravityModel: GravityModel, boolean: bool, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...

class AbstractHarmonicGravityModel(AbstractGravityModel):
    """
    public abstract class AbstractHarmonicGravityModel extends :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractGravityModel`
    
        This class represents a gravitational harmonic attraction model.
    
        Since:
            4.11
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def computeAcceleration(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeCentralTermDAccDPos(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computeDAccDPos(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computeNonCentralTermsDAccDPos(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def isCentralTermContributionApplied(self) -> bool:
        """
            Get the boolean for the central term contribution (true if the central term is considered, false if not).
        
            Returns:
                the boolean for the central term contribution (true if the central term is considered, false if not)
        
        
        """
        ...
    def setCentralTermContribution(self, boolean: bool) -> None:
        """
            Set the boolean for the central term contribution (true if the central term is considered, false if not).
        
            Parameters:
                centralTermContributionIn (boolean): the boolean for the central term contribution (true if the central term is considered, false if not).
        
        
        """
        ...

class BalminoGravityModel(AbstractHarmonicGravityModel):
    """
    public class BalminoGravityModel extends :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractHarmonicGravityModel`
    
        Computation of central body attraction with normalized coefficients and Helmholtz Polynomials.
    
        The algorithm implemented in this class has been designed by Balmino Georges (Observatoire Midi-Pyrénées/ Groupe de
        Recherche de Géodésie Spatiale (GRGS) / Centre National d’Etudes Spatiales (CNES), France) in his 1990 paper:
        *Non-singular formulation of the gravity vector and gravity gradient tensor in spherical harmonics.* (Manuscr. Geod.,
        Vol. 15, No. 1, p. 11 - 16, 02/1990). It uses normalized C and S coefficients for greater accuracy.
    
        Warning: using a 0x0 Earth potential model is equivalent to a simple Newtonian attraction. However computation times
        will be much slower since this case is not particularized and hence conversion from body frame (often ITRF) to
        integration frame is necessary.
    
        Since:
            2.1
    
        Also see:
            :meth:`~serialized`
    """
    RADIUS: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` RADIUS
    
        Parameter name for equatorial radius.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], int: int, int2: int): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], int: int, int2: int): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], int: int, int2: int, boolean: bool): ...
    def computeNonCentralTermsAcceleration(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeNonCentralTermsDAccDPos(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getAe(self) -> float:
        """
            Get the equatorial radius.
        
            Returns:
                equatorial radius (m)
        
        
        """
        ...
    def getC(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
        
            Returns:
                the normalized C coefficients.
        
        
        """
        ...
    def getS(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
        
            Returns:
                the normalized S coefficients.
        
        
        """
        ...
    def setAe(self, double: float) -> None:
        """
            Set the equatorial radius.
        
            Parameters:
                aeIn (double): the equatorial radius.
        
        
        """
        ...

class CunninghamGravityModel(AbstractHarmonicGravityModel):
    """
    public class CunninghamGravityModel extends :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractHarmonicGravityModel`
    
        This class represents the gravitational field of a celestial body.
    
        The algorithm implemented in this class has been designed by Leland E. Cunningham (Lockheed Missiles and Space Company,
        Sunnyvale and Astronomy Department University of California, Berkeley) in his 1969 paper: *On the computation of the
        spherical harmonic terms needed during the numerical integration of the orbital motion of an artificial satellite*
        (Celestial Mechanics 2, 1970).
    
        Warning: using a 0x0 Earth potential model is equivalent to a simple Newtonian attraction. However computation times
        will be much slower since this case is not particularized and hence conversion from body frame (often ITRF) to
        integration frame is necessary.
    
        Also see:
            :meth:`~serialized`
    """
    RADIUS: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` RADIUS
    
        Parameter name for equatorial radius.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], int: int, int2: int): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], int: int, int2: int): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], int: int, int2: int, boolean: bool): ...
    def computeNonCentralTermsAcceleration(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeNonCentralTermsDAccDPos(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getAe(self) -> float:
        """
            Get the equatorial radius.
        
            Returns:
                equatorial radius (m)
        
        
        """
        ...
    def getC(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
        
            Returns:
                the normalized C coefficients.
        
        
        """
        ...
    def getS(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
        
            Returns:
                the normalized S coefficients.
        
        
        """
        ...
    def setAe(self, double: float) -> None:
        """
            Set the equatorial radius.
        
            Parameters:
                aeIn (double): the equatorial radius.
        
        
        """
        ...

class DrozinerGravityModel(AbstractHarmonicGravityModel):
    """
    public class DrozinerGravityModel extends :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractHarmonicGravityModel`
    
        This class represents the gravitational field of a celestial body.
    
        The algorithm implemented in this class has been designed by Andrzej Droziner (Institute of Mathematical Machines,
        Warsaw) in his 1976 paper: *An algorithm for recurrent calculation of gravitational acceleration* (artificial
        satellites, Vol. 12, No 2, June 1977).
    
        The implementation of this class enables the computation of partial derivatives by finite differences with respect to
        the **central attraction coefficient**.
    
        Warning: using a 0x0 Earth potential model is equivalent to a simple Newtonian attraction. However computation times
        will be much slower since this case is not particularized and hence conversion from body frame (often ITRF) to
        integration frame is necessary.
    
        Also see:
            :meth:`~serialized`
    """
    RADIUS: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` RADIUS
    
        Parameter name for equatorial radius.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], boolean: bool): ...
    def computeDAccDPos(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def computeNonCentralTermsAcceleration(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeNonCentralTermsDAccDPos(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getAe(self) -> float:
        """
            Get the equatorial radius.
        
            Returns:
                equatorial radius (m)
        
        
        """
        ...
    def getC(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
        
            Returns:
                the normalized C coefficients.
        
        
        """
        ...
    def getS(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
        
            Returns:
                the normalized S coefficients.
        
        
        """
        ...
    def setAe(self, double: float) -> None:
        """
            Set the equatorial radius.
        
            Parameters:
                aeIn (double): the equatorial radius.
        
        
        """
        ...

class NewtonianGravityModel(AbstractHarmonicGravityModel):
    """
    public class NewtonianGravityModel extends :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractHarmonicGravityModel`
    
        Force model for Newtonian central body attraction.
    
        The implementation of this class enables the computation of partial derivatives with respect to the **central attraction
        coefficient**.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, boolean: bool): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, boolean: bool): ...
    def computeNonCentralTermsAcceleration(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeNonCentralTermsDAccDPos(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def setCentralTermContribution(self, boolean: bool) -> None:
        """
            Set the boolean for the central term contribution (true if the central term is considered, false if not).
        
            This class does not accept the desactivation of the central term since it only contains the central term.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.AbstractHarmonicGravityModel.setCentralTermContribution` in
                class :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractHarmonicGravityModel`
        
            Parameters:
                centralTermContributionIn (boolean): the boolean for the central term contribution (true if the central term is considered, false if not).
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.gravity")``.

    AbstractBodyAttraction: typing.Type[AbstractBodyAttraction]
    AbstractGravityModel: typing.Type[AbstractGravityModel]
    AbstractHarmonicGravityModel: typing.Type[AbstractHarmonicGravityModel]
    BalminoGravityModel: typing.Type[BalminoGravityModel]
    CunninghamGravityModel: typing.Type[CunninghamGravityModel]
    DirectBodyAttraction: typing.Type[DirectBodyAttraction]
    DrozinerGravityModel: typing.Type[DrozinerGravityModel]
    EarthGravitationalModelFactory: typing.Type[EarthGravitationalModelFactory]
    GravityModel: typing.Type[GravityModel]
    GravityToolbox: typing.Type[GravityToolbox]
    NewtonianGravityModel: typing.Type[NewtonianGravityModel]
    ThirdBodyAttraction: typing.Type[ThirdBodyAttraction]
    grid: fr.cnes.sirius.patrius.forces.gravity.grid.__module_protocol__
    potential: fr.cnes.sirius.patrius.forces.gravity.potential.__module_protocol__
    tides: fr.cnes.sirius.patrius.forces.gravity.tides.__module_protocol__
    variations: fr.cnes.sirius.patrius.forces.gravity.variations.__module_protocol__
