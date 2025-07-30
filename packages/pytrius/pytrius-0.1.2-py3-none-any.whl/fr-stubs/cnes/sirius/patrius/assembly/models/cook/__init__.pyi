
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly.properties.features
import fr.cnes.sirius.patrius.forces.atmospheres
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.propagation
import java.io
import java.util
import typing



class AlphaProvider(java.io.Serializable):
    """
    public interface AlphaProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for alpha (energy accomodation coefficient).
    
        Since:
            3.3
    """
    def getAlpha(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Return alpha (energy accomodation coefficient) value.
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
            Returns:
                alpha value
        
        
        """
        ...

class CnCookModel(fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction):
    """
    public class CnCookModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction`
    
        This class implements Cook normal coefficient to a facet.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, extendedAtmosphere: fr.cnes.sirius.patrius.forces.atmospheres.ExtendedAtmosphere, facet: fr.cnes.sirius.patrius.assembly.properties.features.Facet, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, double2: float): ...
    @typing.overload
    def __init__(self, extendedAtmosphere: fr.cnes.sirius.patrius.forces.atmospheres.ExtendedAtmosphere, facet: fr.cnes.sirius.patrius.assembly.properties.features.Facet, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, wallGasTemperatureProvider: typing.Union['WallGasTemperatureProvider', typing.Callable]): ...
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Compute the derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction.derivativeValue` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): current state
        
            Returns:
                the derivative value
        
        
        """
        ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
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

class CtCookModel(fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction):
    """
    public class CtCookModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction`
    
        This class implements Cook tangential coefficient to a facet.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, extendedAtmosphere: fr.cnes.sirius.patrius.forces.atmospheres.ExtendedAtmosphere, facet: fr.cnes.sirius.patrius.assembly.properties.features.Facet, frame: fr.cnes.sirius.patrius.frames.Frame, double: float): ...
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Compute the derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction.derivativeValue` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): current state
        
            Returns:
                the derivative value
        
        
        """
        ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
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

class WallGasTemperatureProvider(java.io.Serializable):
    """
    public interface WallGasTemperatureProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Wall gas temperature provider.
    
        Since:
            3.3
    """
    def getWallGasTemperature(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float) -> float:
        """
            Compute wall gas temperature.
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
                relativeVelocity (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): relative velocity with respect to gas
                theta (double): angle between facet and relative velocity (atmosphere / satellite)
        
            Returns:
                atmosphericTemperature atmospheric temperature
        
        
        """
        ...

class AlphaConstant(AlphaProvider):
    """
    public class AlphaConstant extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.models.cook.AlphaProvider`
    
        Constant alpha (energy accomodation coefficient).
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float): ...
    def getAlpha(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Return alpha (energy accomodation coefficient) value.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.models.cook.AlphaProvider.getAlpha` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.models.cook.AlphaProvider`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
            Returns:
                alpha value
        
        
        """
        ...

class AlphaCookModel(AlphaProvider):
    """
    public class AlphaCookModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.models.cook.AlphaProvider`
    
        Alpha (energy accomodation coefficient) following Cook model.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, extendedAtmosphere: fr.cnes.sirius.patrius.forces.atmospheres.ExtendedAtmosphere, double: float, double2: float): ...
    def getAlpha(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Return alpha (energy accomodation coefficient) value.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.models.cook.AlphaProvider.getAlpha` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.models.cook.AlphaProvider`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
        
            Returns:
                alpha value
        
        
        """
        ...

class ConstantWallGasTemperature(WallGasTemperatureProvider):
    """
    public class ConstantWallGasTemperature extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.models.cook.WallGasTemperatureProvider`
    
        Constant wall gas temperature.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float): ...
    def getWallGasTemperature(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float) -> float:
        """
            Compute wall gas temperature.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.models.cook.WallGasTemperatureProvider.getWallGasTemperature` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.models.cook.WallGasTemperatureProvider`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
                relativeVelocity (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): relative velocity with respect to gas
                theta (double): angle between facet and relative velocity (atmosphere / satellite)
        
            Returns:
                atmosphericTemperature atmospheric temperature
        
        
        """
        ...

class CookWallGasTemperature(WallGasTemperatureProvider):
    """
    public class CookWallGasTemperature extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.models.cook.WallGasTemperatureProvider`
    
        Wall gas temperature following Cook model.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, extendedAtmosphere: fr.cnes.sirius.patrius.forces.atmospheres.ExtendedAtmosphere, alphaProvider: typing.Union[AlphaProvider, typing.Callable], double: float): ...
    def getWallGasTemperature(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float) -> float:
        """
            Compute wall gas temperature.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.models.cook.WallGasTemperatureProvider.getWallGasTemperature` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.models.cook.WallGasTemperatureProvider`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
                relativeVelocity (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): relative velocity with respect to gas
                theta (double): angle between facet and relative velocity (atmosphere / satellite)
        
            Returns:
                atmosphericTemperature atmospheric temperature
        
        
        """
        ...

class GinsWallGasTemperature(WallGasTemperatureProvider):
    """
    public class GinsWallGasTemperature extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.models.cook.WallGasTemperatureProvider`
    
        Wall gas temperature following Cook model adapted to GINS.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, extendedAtmosphere: fr.cnes.sirius.patrius.forces.atmospheres.ExtendedAtmosphere, alphaProvider: typing.Union[AlphaProvider, typing.Callable], double: float): ...
    def getWallGasTemperature(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float) -> float:
        """
            Compute wall gas temperature.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.models.cook.WallGasTemperatureProvider.getWallGasTemperature` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.models.cook.WallGasTemperatureProvider`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): spacecraft state
                relativeVelocity (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): relative velocity with respect to gas
                theta (double): angle between facet and relative velocity (atmosphere / satellite)
        
            Returns:
                atmosphericTemperature atmospheric temperature
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.assembly.models.cook")``.

    AlphaConstant: typing.Type[AlphaConstant]
    AlphaCookModel: typing.Type[AlphaCookModel]
    AlphaProvider: typing.Type[AlphaProvider]
    CnCookModel: typing.Type[CnCookModel]
    ConstantWallGasTemperature: typing.Type[ConstantWallGasTemperature]
    CookWallGasTemperature: typing.Type[CookWallGasTemperature]
    CtCookModel: typing.Type[CtCookModel]
    GinsWallGasTemperature: typing.Type[GinsWallGasTemperature]
    WallGasTemperatureProvider: typing.Type[WallGasTemperatureProvider]
