
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.stela.forces.solaractivity.constant
import fr.cnes.sirius.patrius.stela.forces.solaractivity.variable
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import typing



class IStelaSolarActivity(java.io.Serializable):
    """
    public interface IStelaSolarActivity extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for Stela solar activity models.
    
        Since:
            4.16
    """
    def copy(self) -> 'IStelaSolarActivity': ...
    def getAp(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getInstantFluxValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def getSolActType(self) -> 'StelaSolarActivityType':
        """
            Get solar activity type. It can be either constant or variable.
        
            Returns:
                solar activity type
        
        
        """
        ...
    def getSolarActivity(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]: ...
    def setConstantAP(self, double: float) -> None: ...
    def setConstantF107(self, double: float) -> None: ...
    def toString(self) -> str:
        """
            Get information of Solar Activity.
        
            Overrides:
                 in class 
        
            Returns:
                a string with all solar activity
        
        
        """
        ...

class StelaSolarActivityType(java.lang.Enum['StelaSolarActivityType']):
    """
    public enum StelaSolarActivityType extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.StelaSolarActivityType`>
    
        Solar activity type enumeration
    
        Since:
            4.16
    """
    CONSTANT: typing.ClassVar['StelaSolarActivityType'] = ...
    MEAN_CONSTANT: typing.ClassVar['StelaSolarActivityType'] = ...
    VARIABLE: typing.ClassVar['StelaSolarActivityType'] = ...
    VARIABLE_DISPERSED: typing.ClassVar['StelaSolarActivityType'] = ...
    RANDOM_CYCLES: typing.ClassVar['StelaSolarActivityType'] = ...
    MIXED_3DATE_RANGES: typing.ClassVar['StelaSolarActivityType'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'StelaSolarActivityType':
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
    def values() -> typing.MutableSequence['StelaSolarActivityType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (StelaSolarActivityType c : StelaSolarActivityType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class AbstractStelaSolarActivity(IStelaSolarActivity):
    """
    public abstract class AbstractStelaSolarActivity extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity`
    
        Solar activity abstract class.
    
        Since:
            4.16
    
        Also see:
            :meth:`~serialized`
    """
    def getSolActType(self) -> StelaSolarActivityType:
        """
            Get solar activity type. It can be either constant or variable.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity.getSolActType` in
                interface :class:`~fr.cnes.sirius.patrius.stela.forces.solaractivity.IStelaSolarActivity`
        
            Returns:
                solar activity type
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela.forces.solaractivity")``.

    AbstractStelaSolarActivity: typing.Type[AbstractStelaSolarActivity]
    IStelaSolarActivity: typing.Type[IStelaSolarActivity]
    StelaSolarActivityType: typing.Type[StelaSolarActivityType]
    constant: fr.cnes.sirius.patrius.stela.forces.solaractivity.constant.__module_protocol__
    variable: fr.cnes.sirius.patrius.stela.forces.solaractivity.variable.__module_protocol__
