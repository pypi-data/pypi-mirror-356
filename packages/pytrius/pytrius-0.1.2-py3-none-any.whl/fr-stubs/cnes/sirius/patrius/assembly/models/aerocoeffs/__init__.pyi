
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.forces.atmospheres
import fr.cnes.sirius.patrius.math.analysis.interpolation
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.propagation
import java.lang
import java.util
import jpype
import typing



class AerodynamicCoefficient(fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction):
    """
    public interface AerodynamicCoefficient extends :class:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction`
    
        Interface for aerodynamic coefficients.
    
        Since:
            4.1
    """
    def getType(self) -> 'AerodynamicCoefficientType':
        """
            Returns type of aerodynamic coefficient.
        
            Returns:
                type of aerodynamic coefficient
        
        
        """
        ...

class AerodynamicCoefficientType(java.lang.Enum['AerodynamicCoefficientType']):
    """
    public enum AerodynamicCoefficientType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.assembly.models.aerocoeffs.AerodynamicCoefficientType`>
    
        Aerodynamic coefficient type.
    
        Since:
            4.1
    """
    CONSTANT: typing.ClassVar['AerodynamicCoefficientType'] = ...
    ALTITUDE: typing.ClassVar['AerodynamicCoefficientType'] = ...
    AOA: typing.ClassVar['AerodynamicCoefficientType'] = ...
    MACH: typing.ClassVar['AerodynamicCoefficientType'] = ...
    MACH_AND_AOA: typing.ClassVar['AerodynamicCoefficientType'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'AerodynamicCoefficientType':
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
    def values() -> typing.MutableSequence['AerodynamicCoefficientType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (AerodynamicCoefficientType c : AerodynamicCoefficientType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class AbstractAeroCoeff1D(AerodynamicCoefficient):
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    def getFunction(self) -> fr.cnes.sirius.patrius.math.analysis.interpolation.UniLinearIntervalsFunction: ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def getXArray(self) -> typing.MutableSequence[float]: ...
    def getYArray(self) -> typing.MutableSequence[float]: ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool: ...
    def supportsParameter(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool: ...
    def toString(self) -> str: ...
    def value(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...

class AeroCoeffByAoAAndMach(AerodynamicCoefficient):
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid): ...
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    def getAerodynamicCoefficientsArray(self) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getAoAArray(self) -> typing.MutableSequence[float]: ...
    def getFunction(self) -> fr.cnes.sirius.patrius.math.analysis.interpolation.BiLinearIntervalsFunction: ...
    def getMachArray(self) -> typing.MutableSequence[float]: ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def getType(self) -> AerodynamicCoefficientType: ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool: ...
    def supportsParameter(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool: ...
    def toString(self) -> str: ...
    def value(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...

class AeroCoeffConstant(AerodynamicCoefficient):
    """
    public class AeroCoeffConstant extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.models.aerocoeffs.AerodynamicCoefficient`
    
        Constant aerodynamic coefficient.
    
        Since:
            4.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Compute the derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction.derivativeValue` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): current state
        
            Returns:
                the derivative value
        
        
        """
        ...
    def getAerodynamicCoefficient(self) -> float:
        """
            Getter for the aerodynamic coefficient.
        
            Returns:
                the aerodynamic coefficient
        
        
        """
        ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def getType(self) -> AerodynamicCoefficientType:
        """
            Returns type of aerodynamic coefficient.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.models.aerocoeffs.AerodynamicCoefficient.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.models.aerocoeffs.AerodynamicCoefficient`
        
            Returns:
                type of aerodynamic coefficient
        
        
        """
        ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Tell if the function is differentiable by the given parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction.isDifferentiableBy` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): function parameter
        
            Returns:
                true if the function is differentiable by the given parameter.
        
        
        """
        ...
    def supportsParameter(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Check if a parameter is supported.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable.supportsParameter` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
        
            Parameters:
                param (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to check
        
            Returns:
                true if the parameter is supported
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def value(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Getting the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParameterizableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizableFunction`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the spacecraft state
        
            Returns:
                the value of the function.
        
        
        """
        ...

class AeroCoeffByAltitude(AbstractAeroCoeff1D):
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid): ...
    def getType(self) -> AerodynamicCoefficientType: ...

class AeroCoeffByAoA(AbstractAeroCoeff1D):
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid): ...
    @staticmethod
    def angleOfAttackFromSpacecraftState(spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, oneAxisEllipsoid: fr.cnes.sirius.patrius.bodies.OneAxisEllipsoid) -> float: ...
    def getType(self) -> AerodynamicCoefficientType: ...

class AeroCoeffByMach(AbstractAeroCoeff1D):
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere): ...
    def getType(self) -> AerodynamicCoefficientType: ...
    @staticmethod
    def machFromSpacecraftState(spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, atmosphere: fr.cnes.sirius.patrius.forces.atmospheres.Atmosphere) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.assembly.models.aerocoeffs")``.

    AbstractAeroCoeff1D: typing.Type[AbstractAeroCoeff1D]
    AeroCoeffByAltitude: typing.Type[AeroCoeffByAltitude]
    AeroCoeffByAoA: typing.Type[AeroCoeffByAoA]
    AeroCoeffByAoAAndMach: typing.Type[AeroCoeffByAoAAndMach]
    AeroCoeffByMach: typing.Type[AeroCoeffByMach]
    AeroCoeffConstant: typing.Type[AeroCoeffConstant]
    AerodynamicCoefficient: typing.Type[AerodynamicCoefficient]
    AerodynamicCoefficientType: typing.Type[AerodynamicCoefficientType]
