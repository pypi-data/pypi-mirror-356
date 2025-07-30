
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis.polynomials
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import typing



class IAUMODPrecessionConvention(java.lang.Enum['IAUMODPrecessionConvention']):
    """
    public enum IAUMODPrecessionConvention extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.frames.configuration.modprecession.IAUMODPrecessionConvention`>
    
        This class lists all the available precession conventions used in conjunction with MOD and Ecliptic MOD frames.
    
        Values from "Expressions for IAU 2000 precession quantities, N. Capitaine, P.T. Wallace, and J. Chapront, 2003".
    
        Since:
            4.13
    """
    IAU1976: typing.ClassVar['IAUMODPrecessionConvention'] = ...
    IAU2000: typing.ClassVar['IAUMODPrecessionConvention'] = ...
    def getObliquityCoefs(self) -> typing.MutableSequence[float]:
        """
            Returns the obliquity coefficients.
        
            Returns:
                the obliquity coefficients in radians
        
        
        """
        ...
    def getPrecessionThetaCoefs(self) -> typing.MutableSequence[float]:
        """
            Returns the precession coefficients (theta).
        
            Returns:
                the precession coefficients (theta) in radians
        
        
        """
        ...
    def getPrecessionZCoefs(self) -> typing.MutableSequence[float]:
        """
            Returns the precession coefficients (Z).
        
            Returns:
                the precession coefficients (zeta) in radians
        
        
        """
        ...
    def getPrecessionZetaCoefs(self) -> typing.MutableSequence[float]:
        """
            Returns the precession coefficients (zeta).
        
            Returns:
                the precession coefficients (zeta) in radians
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'IAUMODPrecessionConvention':
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
    def values() -> typing.MutableSequence['IAUMODPrecessionConvention']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (IAUMODPrecessionConvention c : IAUMODPrecessionConvention.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class MODPrecessionModel(java.io.Serializable):
    """
    public interface MODPrecessionModel extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface provides methods used to compute the GCRF/EME2000 to MOD and MOD to Ecliptic MOD transformations.
    
        Since:
            4.13
    """
    def getEarthObliquity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Getter for the Earth obliquity at provided date used in MOD to Ecliptic MOD transformation.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                the Earth obliquity at provided date used in MOD to Ecliptic MOD transformation
        
        
        """
        ...
    def getMODPrecession(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation:
        """
            Getter for the MOD precession transformation from GCRF/EME2000 to MOD at provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                the MOD precession rotation from GCRF/EME2000 to MOD at provided date
        
        
        """
        ...

class IAUMODPrecession(MODPrecessionModel):
    """
    public class IAUMODPrecession extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.frames.configuration.modprecession.MODPrecessionModel`
    
        This class implement the IAU Precession models for GCRF to MOD transformation.
    
        Since:
            4.13
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.frames.configuration.modprecession.IAUMODPrecessionConvention`, :meth:`~serialized`
    """
    def __init__(self, iAUMODPrecessionConvention: IAUMODPrecessionConvention, int: int, int2: int): ...
    def getConvention(self) -> IAUMODPrecessionConvention:
        """
            Returns the IAU convention.
        
            Returns:
                the IAU convention
        
        
        """
        ...
    def getEarthObliquity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Getter for the Earth obliquity at provided date used in MOD to Ecliptic MOD transformation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.modprecession.MODPrecessionModel.getEarthObliquity` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.modprecession.MODPrecessionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                the Earth obliquity at provided date used in MOD to Ecliptic MOD transformation
        
        
        """
        ...
    def getMODPrecession(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation:
        """
            Getter for the MOD precession transformation from GCRF/EME2000 to MOD at provided date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.frames.configuration.modprecession.MODPrecessionModel.getMODPrecession` in
                interface :class:`~fr.cnes.sirius.patrius.frames.configuration.modprecession.MODPrecessionModel`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
        
            Returns:
                the MOD precession rotation from GCRF/EME2000 to MOD at provided date
        
        
        """
        ...
    def getObliquityDegree(self) -> int:
        """
            Returns the obliquity polynomial development degree.
        
            Returns:
                the obliquity polynomial development degree
        
        
        """
        ...
    def getPolynomialObliquity(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction:
        """
            Returns the Obliquity polynomial.
        
            Returns:
                the Obliquity polynomial
        
        
        """
        ...
    def getPolynomialPrecessionTheta(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction:
        """
            Returns the Precession (Theta) polynomial.
        
            Returns:
                the Precession (Theta) polynomial
        
        
        """
        ...
    def getPolynomialPrecessionZ(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction:
        """
            Returns the Precession (Z) polynomial.
        
            Returns:
                the Precession (Z) polynomial
        
        
        """
        ...
    def getPolynomialPrecessionZeta(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction:
        """
            Returns the Precession (Zeta) polynomial.
        
            Returns:
                the Precession (Zeta) polynomial
        
        
        """
        ...
    def getPrecessionDegree(self) -> int:
        """
            Returns the obliquity polynomial development degree.
        
            Returns:
                the obliquity polynomial development degree
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.frames.configuration.modprecession")``.

    IAUMODPrecession: typing.Type[IAUMODPrecession]
    IAUMODPrecessionConvention: typing.Type[IAUMODPrecessionConvention]
    MODPrecessionModel: typing.Type[MODPrecessionModel]
