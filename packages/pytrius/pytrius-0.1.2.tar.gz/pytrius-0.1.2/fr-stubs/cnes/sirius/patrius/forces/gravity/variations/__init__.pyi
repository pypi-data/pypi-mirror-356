
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.forces.gravity
import fr.cnes.sirius.patrius.forces.gravity.tides
import fr.cnes.sirius.patrius.forces.gravity.variations.coefficients
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.time
import typing



class VariablePotentialGravityModel(fr.cnes.sirius.patrius.forces.gravity.AbstractHarmonicGravityModel, fr.cnes.sirius.patrius.forces.gravity.tides.PotentialTimeVariations):
    """
    public class VariablePotentialGravityModel extends :class:`~fr.cnes.sirius.patrius.forces.gravity.AbstractHarmonicGravityModel` implements :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.PotentialTimeVariations`
    
        This class represents a variable gravity field. It computes a static potential and a time variable potential. The C and
        S coefficients array are computed according to the algorithm given by
    
        Since:
            1.3
    
        Also see:
            `GRACE / LAGEOS variable model <http://grgs.obs-mip.fr/grace/variable-models-grace-lageos/formats>`, :meth:`~serialized`
    """
    RADIUS: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` RADIUS
    
        Parameter name for equatorial radius.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, variablePotentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider, int: int, int2: int): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, variablePotentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider, int: int, int2: int, int3: int, int4: int): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, variablePotentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider, int: int, int2: int, int3: int, int4: int, boolean: bool): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, variablePotentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider, int: int, int2: int, int3: int, int4: int, int5: int, int6: int, boolean: bool): ...
    @typing.overload
    def __init__(self, frame: fr.cnes.sirius.patrius.frames.Frame, variablePotentialCoefficientsProvider: fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider, int: int, int2: int, int3: int, int4: int, int5: int, int6: int, boolean: bool, boolean2: bool): ...
    def computeNonCentralTermsAcceleration(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeNonCentralTermsDAccDPos(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getAe(self) -> float:
        """
            Get the equatorial radius.
        
            Returns:
                equatorial radius (m)
        
        
        """
        ...
    def setAe(self, double: float) -> None:
        """
            Set the equatorial radius.
        
            Parameters:
                aeIn (double): the equatorial radius.
        
        
        """
        ...
    def updateCoefficientsCandS(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Update the C and the S coefficients for acceleration computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.PotentialTimeVariations.updateCoefficientsCandS` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.PotentialTimeVariations`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): : date
        
        
        """
        ...
    def updateCoefficientsCandSPD(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Update the C and the S coefficients for partial derivatives computation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.PotentialTimeVariations.updateCoefficientsCandSPD` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.PotentialTimeVariations`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): : date
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.gravity.variations")``.

    VariablePotentialGravityModel: typing.Type[VariablePotentialGravityModel]
    coefficients: fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.__module_protocol__
