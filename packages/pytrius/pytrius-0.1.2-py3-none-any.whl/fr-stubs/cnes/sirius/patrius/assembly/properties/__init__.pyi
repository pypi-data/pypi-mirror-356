
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly
import fr.cnes.sirius.patrius.assembly.models.cook
import fr.cnes.sirius.patrius.assembly.properties.features
import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.fieldsofview
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import java.io
import jpype
import typing



class AeroApplicationPoint(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public class AeroApplicationPoint extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class represents a drag application point property
    
        Since:
            2.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.models.AeroWrenchModel`, :class:`~fr.cnes.sirius.patrius.wrenches.DragWrench`,
            :meth:`~serialized`
    """
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    def getApplicationPoint(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the application point in the given frame at the given date.
        
            Returns:
                the application point of drag forces
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class AeroCrossSectionProperty(fr.cnes.sirius.patrius.math.parameter.Parameterizable, fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public class AeroCrossSectionProperty extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class is a cross section property providing the cross section of shapes such as sphere, cylinder or parallelepiped.
        This cross section is to be used in aero models for drag force computation.
    
        Since:
            3.4
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_C_X: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_C_X
    
        Default normal force coefficient value.
    
        Also see:
            :meth:`~constant`
    
    
    """
    C_X: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` C_X
    
        Default drag force coefficient parameter name.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable]): ...
    @typing.overload
    def __init__(self, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable], double: float): ...
    @typing.overload
    def __init__(self, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable], iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction): ...
    @typing.overload
    def __init__(self, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable], parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def getCrossSection(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, frame2: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getDragForce(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction:
        """
            Get the drag force coefficient parametrizable function.
        
            Returns:
                force coefficient parametrizable function
        
        
        """
        ...
    def getDragForceDerivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Get the drag force coefficient derivative value with respect to the given parameter.
        
            Parameters:
                parameter (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): the parameter
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the current state
        
            Returns:
                the drag force coefficient derivative value
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class AeroFacetProperty(fr.cnes.sirius.patrius.math.parameter.Parameterizable, fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public final class AeroFacetProperty extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class is a facet property to use with the aerodynamic part property for the PATRIUS assembly.
    
    
        This property is meant to be used in a LEO average precision aerodynamic context. See the CNES TTVS book (2002 edition :
        Volume 3, Module XII, $2.4.1.2 ) for information.
    
    
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_C_N: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_C_N
    
        Default normal force coefficient value.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_C_T: typing.ClassVar[float] = ...
    """
    public static final double DEFAULT_C_T
    
        Default tangential force coefficient value.
    
        Also see:
            :meth:`~constant`
    
    
    """
    C_N: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` C_N
    
        Default normal force coefficient parameter name.
    
        Also see:
            :meth:`~constant`
    
    
    """
    C_T: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` C_T
    
        Default tangential force coefficient parameter name.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, facet: fr.cnes.sirius.patrius.assembly.properties.features.Facet): ...
    @typing.overload
    def __init__(self, facet: fr.cnes.sirius.patrius.assembly.properties.features.Facet, double: float, double2: float): ...
    @typing.overload
    def __init__(self, facet: fr.cnes.sirius.patrius.assembly.properties.features.Facet, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction2: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction): ...
    @typing.overload
    def __init__(self, facet: fr.cnes.sirius.patrius.assembly.properties.features.Facet, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def getFacet(self) -> fr.cnes.sirius.patrius.assembly.properties.features.Facet:
        """
            Get the facet.
        
            Returns:
                the facet
        
        
        """
        ...
    def getNormalCoef(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction:
        """
            Get the normal force parametrizable function.
        
            Returns:
                normal force parametrizable function
        
        
        """
        ...
    def getTangentialCoef(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction:
        """
            Get the normal force parametrizable function.
        
            Returns:
                normal force parametrizable function
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class AeroGlobalProperty(fr.cnes.sirius.patrius.math.parameter.Parameterizable, fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public class AeroGlobalProperty extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class is a cross section property providing the cross section of shapes such as sphere, cylinder or parallelepiped.
        This cross section is to be used in :class:`~fr.cnes.sirius.patrius.assembly.models.DragLiftModel` model for drag and
        lift computation.
    
        Since:
            3.4
    
        Also see:
            :meth:`~serialized`
    """
    C_X: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` C_X
    
        Default drag force coefficient parameter name.
    
        Also see:
            :meth:`~constant`
    
    
    """
    C_Z: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` C_Z
    
        Default lift coefficient parameter name.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, double: float, double2: float, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable]): ...
    @typing.overload
    def __init__(self, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction2: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable]): ...
    def getCrossSection(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Compute the cross section of main shape using the relative velocity in the part (having the aero property) frame as the
            direction to provider to the
            :meth:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider.getCrossSection`.
        
            Parameters:
                velocityPartFrame (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the spacecraft velocity relative to the atmosphere in part frame
        
            Returns:
                the cross section of the main shape.
        
        
        """
        ...
    def getDragCoef(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction:
        """
            Get the drag coefficient.
        
            Returns:
                the drag coefficient
        
        
        """
        ...
    def getLiftCoef(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction:
        """
            Get the lift coefficient.
        
            Returns:
                the lift coefficient
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class AeroProperty(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public final class AeroProperty extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        Aero property.
    
        This property has to be applied to Main part only.
    
        Since:
            3.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, alphaProvider: typing.Union[fr.cnes.sirius.patrius.assembly.models.cook.AlphaProvider, typing.Callable]): ...
    def getAlpha(self) -> fr.cnes.sirius.patrius.assembly.models.cook.AlphaProvider:
        """
            Getter for the alpha.
        
            Returns:
                the alpha
        
        
        """
        ...
    def getEpsilon(self) -> float:
        """
            Getter for the specular reemission percentage.
        
            Returns:
                the specular reemission percentage
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...
    def getWallTemperature(self) -> float:
        """
            Getter for the wall temperature.
        
            Returns:
                the wall temperature
        
        
        """
        ...

class CrossSectionProviderProperty(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public final class CrossSectionProviderProperty extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class is a part property for the PATRIUS assembly. It is the geometric cross section provider of a part.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider`, :meth:`~serialized`
    """
    def __init__(self, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable]): ...
    def getCrossSection(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the cross section of the geometry from a direction defined by a Vector3D.
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector
        
            Returns:
                the cross section
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class GeometricProperty(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public final class GeometricProperty extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class defines the Geometric Property to be used with :class:`~fr.cnes.sirius.patrius.assembly.Assembly`.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, solidShape: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.SolidShape): ...
    def getShape(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.SolidShape:
        """
        
            Returns:
                the shape
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class IInertiaProperty(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public interface IInertiaProperty extends :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This is the interface for all inertia properties : those properties can provide the inertia matrix, mass and mass center
        of the part, and the frame in which the vector and the matrix are expressed. The inertia matrix is the one at the mass
        center of the part.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    """
    def getInertiaMatrix(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D:
        """
        
            Returns:
                the inertia matrix at the mass center of the part.
        
        
        """
        ...
    def getMass(self) -> float:
        """
        
            Returns:
                the mass of the considered part.
        
        
        """
        ...
    def getMassCenter(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
        
            Returns:
                the position of the mass center in the reference frame
        
        
        """
        ...
    def getMassProperty(self) -> 'MassProperty':
        """
        
            Returns:
                the mass property
        
        
        """
        ...

class MassEquation(fr.cnes.sirius.patrius.propagation.numerical.AdditionalEquations):
    PREFIX: typing.ClassVar[str] = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: str): ...
    def addMassDerivative(self, double: float) -> None: ...
    def buildAdditionalState(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    def computeDerivatives(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def computeSecondDerivatives(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> typing.MutableSequence[float]: ...
    def extractY(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    def extractYDot(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @staticmethod
    def genName(string: str) -> str: ...
    def getFirstOrderDimension(self) -> int: ...
    def getName(self) -> str: ...
    def getSecondOrderDimension(self) -> int: ...
    def readExternal(self, objectInput: java.io.ObjectInput) -> None: ...
    def setMassDerivativeZero(self) -> None: ...
    def writeExternal(self, objectOutput: java.io.ObjectOutput) -> None: ...

class MassProperty(fr.cnes.sirius.patrius.math.parameter.Parameterizable, fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public final class MassProperty extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class is a part property for the PATRIUS assembly. It is the mass property of a part.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def getMass(self) -> float:
        """
            Gets the mass of the part.
        
            Returns:
                the mass
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...
    def updateMass(self, double: float) -> None: ...

class PropulsiveProperty(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public final class PropulsiveProperty extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        Propulsive property : gathers all thrust properties.
    
        Since:
            3.4
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, propulsiveProperty: 'PropulsiveProperty'): ...
    @typing.overload
    def __init__(self, iDependentVariable: typing.Union[fr.cnes.sirius.patrius.math.analysis.IDependentVariable[fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], float]], iDependentVariable2: typing.Union[fr.cnes.sirius.patrius.math.analysis.IDependentVariable[fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], float]]): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    @typing.overload
    def getIsp(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Getter for isp (s) as function of input :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`.
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the spacecraft state
        
            Returns:
                the isp (s)
        
        
        """
        ...
    @typing.overload
    def getIsp(self) -> fr.cnes.sirius.patrius.math.analysis.IDependentVariable[fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    def getIspParam(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Getter for the isp as an :class:`~fr.cnes.sirius.patrius.math.parameter.Parameter` object.
        
            Will return NaN if ISP has been defined as variable.
        
            Returns:
                the isp
        
        
        """
        ...
    def getPartName(self) -> str:
        """
            Getter for the part name owning the property.
        
            Returns:
                the part name owning the property
        
        
        """
        ...
    @typing.overload
    def getThrust(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Getter for thrust force (N) as function of input :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`.
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the spacecraft state
        
            Returns:
                the thrust (N)
        
        
        """
        ...
    @typing.overload
    def getThrust(self) -> fr.cnes.sirius.patrius.math.analysis.IDependentVariable[fr.cnes.sirius.patrius.propagation.SpacecraftState]: ...
    def getThrustParam(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Getter for the thrust force as an :class:`~fr.cnes.sirius.patrius.math.parameter.Parameter` object.
        
            Will return NaN if thrust has been defined as variable.
        
            Returns:
                the thrust force
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...
    def setPartName(self, string: str) -> None:
        """
            Setter for the part name owning the property. **Warning**: this setter should not be used. It is used internally in
            PATRIUS.
        
            Parameters:
                nameIn (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the part name owning the property
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class RFAntennaProperty(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public class RFAntennaProperty extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class represents an RF antenna property for a part of the assembly. This property is used when calculating the RF
        link budget.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`,
            :class:`~fr.cnes.sirius.patrius.assembly.models.RFLinkBudgetModel`, :meth:`~serialized`
    """
    def __init__(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray4: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double6: float, double7: float, double8: float, double9: float): ...
    def getBitRate(self) -> float:
        """
        
            Returns:
                the bit rate for nominal mode [bps].
        
        
        """
        ...
    def getCircuitLoss(self) -> float:
        """
        
            Returns:
                the losses between TX and antenna [dB].
        
        
        """
        ...
    def getEllipticity(self, double: float, double2: float) -> float:
        """
            Gets the factor of ellipticity using a spline interpolation.
        
        
            The ellipticity factor is a function of the station direction (ellipticity = F(polarAngle, azimuth)) and is used to
            calculate the polarisation losses of the antenna.
        
            Parameters:
                polarAngle (double): the polar angle of the ground station direction in the antenna frame [0, PI].
                azimuth (double): the azimuth of the ground station direction in the antenna frame [0, 2PI].
        
            Returns:
                the ellipticity factor for the specified ground station direction [dB].
        
        
        """
        ...
    def getFrequency(self) -> float:
        """
        
            Returns:
                the emission frequency [Hz].
        
        
        """
        ...
    def getGain(self, double: float, double2: float) -> float:
        """
            Gets the antenna gain using a spline interpolation.
        
        
            The antenna gain is a function of the station direction (gain = F(polarAngle, azimuth)).
        
            Parameters:
                polarAngle (double): the polar angle of the ground station direction in the antenna frame [0, PI].
                azimuth (double): the azimuth of the ground station direction in the antenna frame [0, 2PI].
        
            Returns:
                the antenna gain for the specified ground station direction [dB].
        
        
        """
        ...
    def getOutputPower(self) -> float:
        """
        
            Returns:
                the amplifier output power [dB].
        
        
        """
        ...
    def getTechnoLoss(self) -> float:
        """
        
            Returns:
                the technological losses by the satellite transmitter [dB].
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class RadiativeApplicationPoint(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public class RadiativeApplicationPoint extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class represents a radiative application point property
    
        Since:
            2.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.models.DirectRadiativeWrenchModel`,
            :class:`~fr.cnes.sirius.patrius.wrenches.SolarRadiationWrench`, :meth:`~serialized`
    """
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    def getApplicationPoint(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the application point in the part frame
        
            Returns:
                the application point of radiative forces
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class RadiativeCrossSectionProperty(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public class RadiativeCrossSectionProperty extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class is a cross section property providing the cross section of shapes such as sphere, cylinder or parallelepiped.
        This cross section is to be used in radiative models for SRP force computation.
    
        Since:
            3.4
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, crossSectionProvider: typing.Union[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, typing.Callable]): ...
    def getCrossSection(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class RadiativeFacetProperty(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public final class RadiativeFacetProperty extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class is a part property for the PATRIUS assembly. It allows the radiative model to use a part with this property.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, facet: fr.cnes.sirius.patrius.assembly.properties.features.Facet): ...
    def getFacet(self) -> fr.cnes.sirius.patrius.assembly.properties.features.Facet:
        """
            Get the facet.
        
            Returns:
                the facet
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class RadiativeIRProperty(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public final class RadiativeIRProperty extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class is a part property for the PATRIUS assembly. It is the radiative property of a part. Three optical
        coefficients are defined in the infrared domain.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    ABSORPTION_COEFFICIENT: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` ABSORPTION_COEFFICIENT
    
        Parameter name for absorption coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    SPECULAR_COEFFICIENT: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` SPECULAR_COEFFICIENT
    
        Parameter name for reflection coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DIFFUSION_COEFFICIENT: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DIFFUSION_COEFFICIENT
    
        Parameter name for diffusion coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def getAbsorptionCoef(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Get the parameter representing the absorption coefficient of the part.
        
            Returns:
                the parameter representing the absorption coefficient
        
        
        """
        ...
    def getDiffuseReflectionCoef(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Get the parameter representing the diffuse reflection coefficient of the part.
        
            Returns:
                the parameter representing the diffuse reflection coefficient
        
        
        """
        ...
    def getSpecularReflectionCoef(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Get the parameter representing the specular reflection coefficient of the part.
        
            Returns:
                the parameter representing the specular reflection coefficient
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class RadiativeProperty(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public final class RadiativeProperty extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class is a part property for the PATRIUS assembly. It is the radiative property of a part. Three optical
        coefficients are defined in the visible domain (for absorption, specular reflection and diffuse reflection).
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    ABSORPTION_COEFFICIENT: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` ABSORPTION_COEFFICIENT
    
        Parameter name for absorption coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    SPECULAR_COEFFICIENT: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` SPECULAR_COEFFICIENT
    
        Parameter name for reflection coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DIFFUSION_COEFFICIENT: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DIFFUSION_COEFFICIENT
    
        Parameter name for diffusion coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def getAbsorptionRatio(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Get the parameter representing the ratio of light absorbed: Ka = α.
        
            Returns:
                the parameter representing the absorption ratio coefficient
        
        
        """
        ...
    def getDiffuseReflectionRatio(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Get the parameter representing the ratio of light subjected to diffuse reflectance : Kd = (1 - α) (1 - τ).
        
            Returns:
                the parameter representing the diffuse reflection ratio coefficient
        
        
        """
        ...
    def getSpecularReflectionRatio(self) -> fr.cnes.sirius.patrius.math.parameter.Parameter:
        """
            Get the parameter representing the ratio of light subjected to specular reflectance : Ks = (1 - α) τ.
        
            Returns:
                the parameter representing the specular reflection ratio coefficient
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class SensorProperty(fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public final class SensorProperty extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        This class represents a generic sensor property for a part of the assembly. This sensor is defined by a sight axis and
        some optional features : a target, some fields of view and inhibition.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`, :class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`,
            :meth:`~serialized`
    """
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    def getInSightAxis(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
        
            Returns:
                the main sight axis (in the part's frame)
        
        
        """
        ...
    def getInhibitionFields(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.fieldsofview.IFieldOfView]:
        """
        
            Returns:
                the inhibition fields array (in the part's frame)
        
        
        """
        ...
    def getInhibitionTargets(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider]:
        """
        
            Returns:
                the inhibition targets array
        
        
        """
        ...
    def getInhibitionTargetsRadiuses(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.bodies.ApparentRadiusProvider]:
        """
        
            Returns:
                the inhibition targets radiuses
        
        
        """
        ...
    def getMainField(self) -> fr.cnes.sirius.patrius.fieldsofview.IFieldOfView:
        """
        
            Returns:
                the main field of view (in the part's frame)
        
        
        """
        ...
    def getMainTarget(self) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider:
        """
        
            Returns:
                the main target center
        
        
        """
        ...
    def getMainTargetRadius(self) -> fr.cnes.sirius.patrius.bodies.ApparentRadiusProvider:
        """
        
            Returns:
                the main target radius
        
        
        """
        ...
    def getReferenceAxis(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D]:
        """
        
            Returns:
                the reference axis array (in the part's frame)
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...
    def setInhibitionFieldsAndTargets(self, iFieldOfViewArray: typing.Union[typing.List[fr.cnes.sirius.patrius.fieldsofview.IFieldOfView], jpype.JArray], pVCoordinatesProviderArray: typing.Union[typing.List[fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider], jpype.JArray], apparentRadiusProviderArray: typing.Union[typing.List[fr.cnes.sirius.patrius.bodies.ApparentRadiusProvider], jpype.JArray]) -> None:
        """
            Sets the arrays of inhibition fields and the associated targets : the two array must have the same length.
        
            Parameters:
                fields (:class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`[]): the inhibition fields
                targets (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`[]): the targets associated to those fields
                targetRadiuses (:class:`~fr.cnes.sirius.patrius.bodies.ApparentRadiusProvider`[]): the radiuses of the target objects
        
        
        """
        ...
    def setMainFieldOfView(self, iFieldOfView: fr.cnes.sirius.patrius.fieldsofview.IFieldOfView) -> None:
        """
            Sets the main field of view of this sensor
        
            Parameters:
                field (:class:`~fr.cnes.sirius.patrius.fieldsofview.IFieldOfView`): the new main field of view
        
        
        """
        ...
    def setMainTarget(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, apparentRadiusProvider: typing.Union[fr.cnes.sirius.patrius.bodies.ApparentRadiusProvider, typing.Callable]) -> None:
        """
            Sets the main target of the sensor
        
            Parameters:
                target (:class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`): the new main target center
                radius (:class:`~fr.cnes.sirius.patrius.bodies.ApparentRadiusProvider`): the target's radius (set 0.0 for to create a simple point target)
        
        
        """
        ...
    def setReferenceAxis(self, vector3DArray: typing.Union[typing.List[fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D], jpype.JArray]) -> None:
        """
            Sets the reference axis
        
            Parameters:
                refAxis (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`[]): the axis array
        
        
        """
        ...

class TankProperty(fr.cnes.sirius.patrius.math.parameter.Parameterizable, fr.cnes.sirius.patrius.assembly.IPartProperty):
    """
    public final class TankProperty extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
    
        Tank property: gathers all properties of a fuel tank.
    
    
    
        Warning: a part should either have a MassProperty or a TankProperty, never both
    
        Since:
            3.4
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, tankProperty: 'TankProperty'): ...
    def getMass(self) -> float:
        """
            Getter for the mass.
        
            Returns:
                tank mass
        
        
        """
        ...
    def getMassProperty(self) -> MassProperty:
        """
            Getter for the underlying mass property.
        
            Returns:
                the underlying mass property
        
        
        """
        ...
    def getPartName(self) -> str:
        """
            Getter for the part name owning the property.
        
            Returns:
                the part name owning the property
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...
    def setPartName(self, string: str) -> None:
        """
            Setter for the part name owning the property. **Warning**: this setter should not be used. It is used internally in
            PATRIUS.
        
            Parameters:
                nameIn (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the part name owning the property
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class AbstractInertiaProperty(IInertiaProperty):
    """
    public abstract class AbstractInertiaProperty extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`
    
        This class is the abstract class for all inertia properties : those properties can provide the inertia matrix and mass
        center of the part. All of them shall extend it to assure they have the same "PropertyType"
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`, :meth:`~serialized`
    """
    def getInertiaMatrix(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty.getInertiaMatrix` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`
        
            Returns:
                the inertia matrix at the mass center of the part.
        
        
        """
        ...
    def getMass(self) -> float:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty.getMass` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`
        
            Returns:
                the mass of the considered part.
        
        
        """
        ...
    def getMassCenter(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty.getMassCenter` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`
        
            Returns:
                the position of the mass center in the reference frame
        
        
        """
        ...
    def getMassProperty(self) -> MassProperty:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty.getMassProperty` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`
        
            Returns:
                the mass property
        
        
        """
        ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...
    def setInertiaMatrix(self, matrix3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D) -> None:
        """
            Sets the inertia matrix
        
            Parameters:
                inertiaMatrix (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D`): the new inetria matrix
        
        
        """
        ...
    def setMassCenter(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> None:
        """
            Sets the mass center.
        
            Parameters:
                massCenter (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the new mass center
        
        
        """
        ...

class AeroSphereProperty(AeroCrossSectionProperty):
    """
    public final class AeroSphereProperty extends :class:`~fr.cnes.sirius.patrius.assembly.properties.AeroCrossSectionProperty`
    
        This class is a sphere property to use with the aerodynamic part property for the PATRIUS assembly.
    
    
        This property is meant to be used in a LEO average precision aerodynamic context. See the CNES TTVS book (2002 edition :
        Volume 3, Module XII, $2.4.1.2 ) for information.
    
    
    
        Note that the use of this class implies a constant area which may not be suited for some application such as reentry.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D): ...
    @typing.overload
    def __init__(self, double: float, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction): ...
    @typing.overload
    def __init__(self, double: float, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, double: float): ...
    def getCrossSection(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, frame2: fr.cnes.sirius.patrius.frames.Frame) -> float:
        """
            Compute the cross section of main shape using the relative velocity in the part (having the aero property) frame as the
            direction to provider to the
            :meth:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider.getCrossSection`.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.AeroCrossSectionProperty.getCrossSection` in
                class :class:`~fr.cnes.sirius.patrius.assembly.properties.AeroCrossSectionProperty`
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the current state of the spacecraft
                relativeVelocity (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the spacecraft velocity relative to the atmosphere in state frame.
                mainPartFrame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): main frame
                partFrame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): frame of part owning the property
        
            Returns:
                the cross section of the main shape.
        
        
        """
        ...
    def getSphereArea(self) -> float:
        """
            Get the sphere area.
        
            Returns:
                the sphere area (m :sup:`2` )
        
        
        """
        ...
    def getSphereRadius(self) -> float: ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.AeroCrossSectionProperty.getType` in
                class :class:`~fr.cnes.sirius.patrius.assembly.properties.AeroCrossSectionProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class RadiativeSphereProperty(RadiativeCrossSectionProperty):
    """
    public final class RadiativeSphereProperty extends :class:`~fr.cnes.sirius.patrius.assembly.properties.RadiativeCrossSectionProperty`
    
        This class is a part property for the PATRIUS assembly. It allows the radiative model to use the part with this
        property.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    def getCrossSection(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def getSphereArea(self) -> float:
        """
            Get the sphere area.
        
            Returns:
                the sphere area (m :sup:`2` )
        
        
        """
        ...
    def getSphereRadius(self) -> float: ...
    def getType(self) -> fr.cnes.sirius.patrius.assembly.PropertyType:
        """
            Get the type of the property.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.IPartProperty.getType` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.IPartProperty`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.RadiativeCrossSectionProperty.getType` in
                class :class:`~fr.cnes.sirius.patrius.assembly.properties.RadiativeCrossSectionProperty`
        
            Returns:
                the type of the property (see PropertyType enumeration)
        
        
        """
        ...

class InertiaCylinderProperty(AbstractInertiaProperty):
    """
    public final class InertiaCylinderProperty extends :class:`~fr.cnes.sirius.patrius.assembly.properties.AbstractInertiaProperty`
    
        Inertia property for a cylinder part. The (0, 0, 0) point of the given frame is the center of a basis of the cylinder.
        Its axis is Z, and it is oriented on the positive values.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`, :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, massProperty: MassProperty): ...
    def getInertiaMatrix(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty.getInertiaMatrix` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.AbstractInertiaProperty.getInertiaMatrix` in
                class :class:`~fr.cnes.sirius.patrius.assembly.properties.AbstractInertiaProperty`
        
            Returns:
                the inertia matrix at the mass center of the part.
        
        
        """
        ...

class InertiaParallelepipedProperty(AbstractInertiaProperty):
    """
    public final class InertiaParallelepipedProperty extends :class:`~fr.cnes.sirius.patrius.assembly.properties.AbstractInertiaProperty`
    
        Inertia property for a parallelepipedic part. The center of the parallelepiped is the (0, 0, 0) point in the given
        frame.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`, :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, massProperty: MassProperty): ...
    def getInertiaMatrix(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty.getInertiaMatrix` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.AbstractInertiaProperty.getInertiaMatrix` in
                class :class:`~fr.cnes.sirius.patrius.assembly.properties.AbstractInertiaProperty`
        
            Returns:
                the inertia matrix at the mass center of the part.
        
        
        """
        ...

class InertiaSimpleProperty(AbstractInertiaProperty):
    """
    public class InertiaSimpleProperty extends :class:`~fr.cnes.sirius.patrius.assembly.properties.AbstractInertiaProperty`
    
        This class is a simple inertia property that can be added to a part. The mass center and inertia matrix are simply given
        by the user in the constructor. They also can be set later.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, matrix3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D, massProperty: MassProperty): ...
    @typing.overload
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, matrix3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, massProperty: MassProperty): ...

class InertiaSphereProperty(AbstractInertiaProperty):
    """
    public final class InertiaSphereProperty extends :class:`~fr.cnes.sirius.patrius.assembly.properties.AbstractInertiaProperty`
    
        Inertia property for a spherical part. The center of the part is the (0, 0, 0) point in the given frame.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`, :meth:`~serialized`
    """
    def __init__(self, double: float, massProperty: MassProperty): ...
    def getInertiaMatrix(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Matrix3D:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty.getInertiaMatrix` in
                interface :class:`~fr.cnes.sirius.patrius.assembly.properties.IInertiaProperty`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.assembly.properties.AbstractInertiaProperty.getInertiaMatrix` in
                class :class:`~fr.cnes.sirius.patrius.assembly.properties.AbstractInertiaProperty`
        
            Returns:
                the inertia matrix at the mass center of the part.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.assembly.properties")``.

    AbstractInertiaProperty: typing.Type[AbstractInertiaProperty]
    AeroApplicationPoint: typing.Type[AeroApplicationPoint]
    AeroCrossSectionProperty: typing.Type[AeroCrossSectionProperty]
    AeroFacetProperty: typing.Type[AeroFacetProperty]
    AeroGlobalProperty: typing.Type[AeroGlobalProperty]
    AeroProperty: typing.Type[AeroProperty]
    AeroSphereProperty: typing.Type[AeroSphereProperty]
    CrossSectionProviderProperty: typing.Type[CrossSectionProviderProperty]
    GeometricProperty: typing.Type[GeometricProperty]
    IInertiaProperty: typing.Type[IInertiaProperty]
    InertiaCylinderProperty: typing.Type[InertiaCylinderProperty]
    InertiaParallelepipedProperty: typing.Type[InertiaParallelepipedProperty]
    InertiaSimpleProperty: typing.Type[InertiaSimpleProperty]
    InertiaSphereProperty: typing.Type[InertiaSphereProperty]
    MassEquation: typing.Type[MassEquation]
    MassProperty: typing.Type[MassProperty]
    PropulsiveProperty: typing.Type[PropulsiveProperty]
    RFAntennaProperty: typing.Type[RFAntennaProperty]
    RadiativeApplicationPoint: typing.Type[RadiativeApplicationPoint]
    RadiativeCrossSectionProperty: typing.Type[RadiativeCrossSectionProperty]
    RadiativeFacetProperty: typing.Type[RadiativeFacetProperty]
    RadiativeIRProperty: typing.Type[RadiativeIRProperty]
    RadiativeProperty: typing.Type[RadiativeProperty]
    RadiativeSphereProperty: typing.Type[RadiativeSphereProperty]
    SensorProperty: typing.Type[SensorProperty]
    TankProperty: typing.Type[TankProperty]
    features: fr.cnes.sirius.patrius.assembly.properties.features.__module_protocol__
