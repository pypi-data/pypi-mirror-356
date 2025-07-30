
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.time
import fr.cnes.sirius.patrius.tools.cache
import fr.cnes.sirius.patrius.utils.serializablefunction
import java.io
import java.util
import java.util.function
import jpype
import typing



_FieldDescriptor__T = typing.TypeVar('_FieldDescriptor__T')  # <T>
class FieldDescriptor(java.io.Serializable, typing.Generic[_FieldDescriptor__T]):
    """
    public class FieldDescriptor<T> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Field descriptor.
    
        A field descriptor associates a name with a given class, and provides the means to generate custom string
        representations of any instance of this class.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, string: str, class_: typing.Type[_FieldDescriptor__T]): ...
    @typing.overload
    def __init__(self, string: str, class_: typing.Type[_FieldDescriptor__T], serializableFunction: typing.Union[fr.cnes.sirius.patrius.utils.serializablefunction.SerializableFunction[_FieldDescriptor__T, str], typing.Callable]): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Indicates whether some other object is "equal to" this one.
        
            This method only compares the name of the descriptor and the class of the described fields when checking if two
            :class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor` instances are equal or not. The function used to convert
            field values to strings is not taken into account.
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the reference object with which to compare
        
            Returns:
                :code:`true` if this object is the same as the provided object, :code:`false` otherwise
        
        
        """
        ...
    def getFieldClass(self) -> typing.Type[_FieldDescriptor__T]: ...
    def getName(self) -> str:
        """
            Gets the name of the descriptor.
        
            Returns:
                the name of the descriptor
        
        
        """
        ...
    def getPrintFunction(self) -> fr.cnes.sirius.patrius.utils.serializablefunction.SerializableFunction[_FieldDescriptor__T, str]: ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def printField(self, object: typing.Any) -> str:
        """
            Gets a string representation of a given field value.
        
            The string representation of the field value is generated using the printer function specified at construction. The
            standard :code:`toString` method is used instead if no function was specified, or if the class of the provided object
            does not match the class associated with this field descriptor.
        
            Parameters:
                value (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the field value
        
            Returns:
                a string representation of the specified field value
        
        
        """
        ...
    def setPrintFunction(self, serializableFunction: typing.Union[fr.cnes.sirius.patrius.utils.serializablefunction.SerializableFunction[_FieldDescriptor__T, str], typing.Callable]) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class IParameterizable(java.io.Serializable):
    """
    public interface IParameterizable extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface is used to handle a list of parameterizable parameters.
    """
    def getParameters(self) -> java.util.ArrayList['Parameter']: ...
    def supportsParameter(self, parameter: 'Parameter') -> bool:
        """
            Check if a parameter is supported.
        
            Parameters:
                param (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to check
        
            Returns:
                true if the parameter is supported
        
        
        """
        ...

class Parameter(java.io.Serializable):
    """
    public class Parameter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class links a value and a parameter descriptor which can contain any number of information of any type (like a
        name, a date, ...). This class is for example used when computing finite differences and derivatives of analytical
        functions.
    
        Note that while its reference cannot be changed once set (the attribute is :code:`final`), the parameter descriptor
        itself is possibly mutable (it can be set as immutable, but it is not a definitive property and it's not the case by
        default). Also note that it is possible for the parameter descriptor to be :code:`null` or empty (that is, not
        associated with any field). However, using parameters in such a state is strongly discouraged since it can potentially
        lead to errors if higher-level methods do not handle these cases properly.
    
        Since:
            2.3
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_VALUE_SEPARATOR: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_VALUE_SEPARATOR
    
        Default value separator for the :meth:`~fr.cnes.sirius.patrius.math.parameter.Parameter.toString` methods.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_NAME_SEPARATOR: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_NAME_SEPARATOR
    
        Default name separator for the :meth:`~fr.cnes.sirius.patrius.math.parameter.Parameter.toString` and
        :meth:`~fr.cnes.sirius.patrius.math.parameter.Parameter.getName` methods.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, parameterDescriptor: 'ParameterDescriptor', double: float): ...
    @typing.overload
    def __init__(self, string: str, double: float): ...
    def copy(self) -> 'Parameter':
        """
            Performs a shallow copy of this parameter (the references to the field descriptors and the mapped values are preserved).
        
            Returns:
                a shallow copy of this parameter
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
            Indicates whether some other object is "equal to" this one.
        
            This methods simply redirects to the `Object.equals(Object)
            <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true#equals-java.lang.Object->` method,
            which considers that two objects are equals if and only if they are the same instance. This default behavior is
            preserved on purpose for historical reasons, as other classes sometimes use the
            :class:`~fr.cnes.sirius.patrius.math.parameter.Parameter` class as key in their internal maps and rely on the fact that
            two separate :class:`~fr.cnes.sirius.patrius.math.parameter.Parameter` instances can never be equal.
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the reference object with which to compare
        
            Returns:
                :code:`true` if this object is the same as the provided object, :code:`false` otherwise
        
        
        """
        ...
    def getDescriptor(self) -> 'ParameterDescriptor':
        """
            Gets the parameter descriptor.
        
            Returns:
                the parameter descriptor
        
        
        """
        ...
    @typing.overload
    def getName(self) -> str:
        """
            Gets the parameter name, which is a concatenation of field values currently associated with the parameter descriptor
            (printed in reverse order by default).
        
            Returns:
                the parameter name
        
        """
        ...
    @typing.overload
    def getName(self, boolean: bool) -> str:
        """
            Gets the parameter name, which is a concatenation of field values currently associated with the parameter descriptor.
        
            Parameters:
                reverseOrder (boolean): whether or not the field values should be printed in reverse order
        
            Returns:
                the parameter name, or :code:`null` if the parameter descriptor associated with this parameter is :code:`null`
        
            Gets the parameter name, which is a concatenation of field values currently associated with the parameter descriptor
            (printed in reverse order by default).
        
            Parameters:
                separator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string used as separator between two field values
        
            Returns:
                the parameter name, or :code:`null` if the parameter descriptor associated with this parameter is :code:`null`
        
        """
        ...
    @typing.overload
    def getName(self, string: str) -> str: ...
    @typing.overload
    def getName(self, string: str, boolean: bool) -> str:
        """
            Gets the parameter name, which is a concatenation of field values currently associated with the parameter descriptor.
        
            Parameters:
                separator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string used as separator between two field values
                reverseOrder (boolean): whether or not the field values should be printed in reverse order
        
            Returns:
                the parameter name, or :code:`null` if the parameter descriptor associated with this parameter is :code:`null`
        
        
        """
        ...
    def getValue(self) -> float:
        """
            Gets the parameter value.
        
            Returns:
                the parameter value
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def setValue(self, double: float) -> None:
        """
            Sets the parameter value.
        
            Parameters:
                parameterValue (double): the new parameter value
        
        
        """
        ...
    @typing.overload
    def toString(self) -> str:
        """
            Gets a string representation of this parameter, which includes the name of this class, the name of the parameter and the
            parameter value.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this parameter
        
        """
        ...
    @typing.overload
    def toString(self, boolean: bool) -> str:
        """
            Gets a string representation of this parameter, which includes the name of this class, the name of the parameter and the
            parameter value.
        
            Parameters:
                reverseOrder (boolean): whether or not the associated field values should be printed in reverse order
        
            Returns:
                a string representation of this parameter
        
        """
        ...
    @typing.overload
    def toString(self, string: str, string2: str, boolean: bool, boolean2: bool) -> str:
        """
            Gets a string representation of this parameter, which includes the name of this class (if requested), the name of the
            parameter and the parameter value.
        
            Parameters:
                nameSeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to be used as separator when retrieving the name of the parameter
                valueSeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to be used as separator between the name of the parameter and its value
                printClassName (boolean): whether or not the name of this class should be printed
                reverseOrder (boolean): whether or not the associated field values should be printed in reverse order
        
            Returns:
                a string representation of this parameter
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.Parameter.getName`
        
        
        """
        ...

class ParameterDescriptor(java.io.Serializable):
    """
    public class ParameterDescriptor extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Parameter descriptor.
    
        Also see:
            :meth:`~serialized`
    """
    ___init___1__T = typing.TypeVar('___init___1__T')  # <T>
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, fieldDescriptor: FieldDescriptor[___init___1__T], t: ___init___1__T): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[FieldDescriptor[typing.Any], typing.Any], typing.Mapping[FieldDescriptor[typing.Any], typing.Any]]): ...
    _addField__T = typing.TypeVar('_addField__T')  # <T>
    def addField(self, fieldDescriptor: FieldDescriptor[_addField__T], t: _addField__T) -> _addField__T: ...
    _addFieldIfAbsent__T = typing.TypeVar('_addFieldIfAbsent__T')  # <T>
    def addFieldIfAbsent(self, fieldDescriptor: FieldDescriptor[_addFieldIfAbsent__T], t: _addFieldIfAbsent__T) -> _addFieldIfAbsent__T: ...
    def addUntypedField(self, fieldDescriptor: FieldDescriptor[typing.Any], object: typing.Any) -> typing.Any:
        """
            Adds a single field descriptor with this parameter descriptor and maps it to the specified value (stored values are
            overwritten when a field descriptor is already associated with this instance).
        
            **Important:** the provided value must be assignable to the class specified by the field descriptor. An exception will
            be automatically thrown if that is not the case.
        
            Parameters:
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?> fieldDescriptor): the field descriptor to add
                fieldValue (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the value to be associated with the specified field descriptor
        
            Returns:
                the value which was previously mapped to the provided field descriptor, or :code:`null` if this field descriptor was not
                already associated with this parameter descriptor
        
            Raises:
                : if this parameter descriptor is currently immutable
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the provided field descriptor or field value is :code:`null`
                : if the provided field value cannot be cast to the class specified by the field descriptor
        
        
        """
        ...
    def addUntypedFields(self, map: typing.Union[java.util.Map[FieldDescriptor[typing.Any], typing.Any], typing.Mapping[FieldDescriptor[typing.Any], typing.Any]]) -> None: ...
    @typing.overload
    @staticmethod
    def areEqual(parameterDescriptor: 'ParameterDescriptor', parameterDescriptor2: 'ParameterDescriptor', fieldDescriptor: FieldDescriptor[typing.Any]) -> bool:
        """
            Checks if two parameter descriptors are equal with respect to a given field descriptor.
        
            This method considers that two :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` instances are equal
            if the specified field descriptor is mapped to the same value in both instances, or if it is not associated with either
            of the instances.
        
            Parameters:
                parameterDescriptor1 (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the first parameter descriptor
                parameterDescriptor2 (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the second parameter descriptor
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?> fieldDescriptor): the field descriptor to check
        
            Returns:
                :code:`true` if the specified field descriptor is mapped to the same value in both parameter descriptors, :code:`false`
                otherwise
        
        public static boolean areEqual(:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` parameterDescriptor1, :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` parameterDescriptor2, :class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?>... fieldDescriptors)
        
            Checks if two parameter descriptors are equal with respect to multiple field descriptors.
        
            This method considers that two :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` instances are equal
            if the specified field descriptors are mapped to the same values in both instances, or if they are not associated with
            either of the instances.
        
            Parameters:
                parameterDescriptor1 (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the first parameter descriptor
                parameterDescriptor2 (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the second parameter descriptor
                fieldDescriptors (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?>...): the field descriptors to check
        
            Returns:
                :code:`true` if the specified field descriptors are mapped to the same values in both parameter descriptors,
                :code:`false` otherwise
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the provided field descriptor array is :code:`null`
        
        public static boolean areEqual(:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` parameterDescriptor1, :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` parameterDescriptor2, `Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?>> fieldDescriptors)
        
            Checks if two parameter descriptors are equal with respect to multiple field descriptors.
        
            This method considers that two :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` instances are equal
            if the specified field descriptors are mapped to the same values in both instances, or if they are not associated with
            either of the instances.
        
            Parameters:
                parameterDescriptor1 (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the first parameter descriptor
                parameterDescriptor2 (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the second parameter descriptor
                fieldDescriptors (`Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?>>): the field descriptors to check
        
            Returns:
                :code:`true` if the specified field descriptors are mapped to the same values in both parameter descriptors,
                :code:`false` otherwise
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the provided field descriptor collection is :code:`null`
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def areEqual(parameterDescriptor: 'ParameterDescriptor', parameterDescriptor2: 'ParameterDescriptor', *fieldDescriptor: FieldDescriptor[typing.Any]) -> bool: ...
    @typing.overload
    @staticmethod
    def areEqual(parameterDescriptor: 'ParameterDescriptor', parameterDescriptor2: 'ParameterDescriptor', collection: typing.Union[java.util.Collection[FieldDescriptor[typing.Any]], typing.Sequence[FieldDescriptor[typing.Any]], typing.Set[FieldDescriptor[typing.Any]]]) -> bool: ...
    def clear(self) -> None:
        """
            Removes all the fields currently associated with this parameter descriptor.
        
        """
        ...
    @typing.overload
    def contains(self, fieldDescriptor: FieldDescriptor[typing.Any]) -> bool:
        """
            Checks if a field descriptor is currently associated with this parameter descriptor.
        
            Parameters:
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?> fieldDescriptor): the field descriptor to check
        
            Returns:
                :code:`true` if the provided field descriptor is associated with this parameter descriptor, :code:`false` otherwise
        
        """
        ...
    @typing.overload
    def contains(self, fieldDescriptor: FieldDescriptor[typing.Any], object: typing.Any) -> bool:
        """
            Checks if a field descriptor is currently associated with this parameter descriptor and mapped to a given value.
        
            Parameters:
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?> fieldDescriptor): the field descriptor to check
                fieldValue (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the value expected to be mapped to the provided field descriptor
        
            Returns:
                :code:`true` if the provided field descriptor is associated with this parameter descriptor and mapped to the specified
                value, :code:`false` otherwise
        
        
        """
        ...
    def copy(self) -> 'ParameterDescriptor':
        """
            Performs a shallow copy of the parameter descriptor (the references to the field descriptors and the mapped values are
            preserved).
        
            Returns:
                a shallow copy of this parameter descriptor
        
        
        """
        ...
    @typing.overload
    def equals(self, parameterDescriptor: 'ParameterDescriptor', fieldDescriptor: FieldDescriptor[typing.Any]) -> bool:
        """
            Checks if this parameter descriptor is equal to another one with respect to a given field descriptor.
        
            This method considers that two :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` instances are equal
            if the specified field descriptor is mapped to the same value in both instances, or if it is not associated with either
            of the instances.
        
            Parameters:
                parameterDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the parameter descriptor to compare this instance with
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?> fieldDescriptor): the field descriptor to check
        
            Returns:
                :code:`true` if the specified field descriptor is mapped to the same value in both parameter descriptors, :code:`false`
                otherwise
        
        public boolean equals(:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` parameterDescriptor, :class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?>... fieldDescriptors)
        
            Checks if this parameter descriptor is equal to another one with respect to multiple field descriptors.
        
            This method considers that two :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` instances are equal
            if the specified field descriptors are mapped to the same values in both instances, or if they are not associated with
            either of the instances.
        
            Parameters:
                parameterDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the parameter descriptor to compare this instance with
                fieldDescriptors (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?>...): the field descriptors to check
        
            Returns:
                :code:`true` if the specified field descriptors are mapped to the same values in both parameter descriptors,
                :code:`false` otherwise
        
        public boolean equals(:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` parameterDescriptor, `Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?>> fieldDescriptors)
        
            Checks if this parameter descriptor is equal to another one with respect to multiple field descriptors.
        
            This method considers that two :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` instances are equal
            if the specified field descriptors are mapped to the same values in both instances, or if they are not associated with
            either of the instances.
        
            Parameters:
                parameterDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the parameter descriptor to compare this instance with
                fieldDescriptors (`Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?>>): the field descriptors to check
        
            Returns:
                :code:`true` if the specified field descriptors are mapped to the same values in both parameter descriptors,
                :code:`false` otherwise
        
        
        """
        ...
    @typing.overload
    def equals(self, parameterDescriptor: 'ParameterDescriptor', *fieldDescriptor: FieldDescriptor[typing.Any]) -> bool: ...
    @typing.overload
    def equals(self, parameterDescriptor: 'ParameterDescriptor', collection: typing.Union[java.util.Collection[FieldDescriptor[typing.Any]], typing.Sequence[FieldDescriptor[typing.Any]], typing.Set[FieldDescriptor[typing.Any]]]) -> bool: ...
    @typing.overload
    def equals(self, object: typing.Any) -> bool:
        """
            Indicates whether some other object is "equal to" this one.
        
            This method only compares the associated field descriptors and the values mapped to them when checking if two
            :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` instances are equal or not. The order in which the
            field descriptors are stored and their mutability are not taken into account.
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the reference object with which to compare
        
            Returns:
                :code:`true` if this object is the same as the provided object, :code:`false` otherwise
        
        """
        ...
    @typing.overload
    def extractSubset(self, *fieldDescriptor: FieldDescriptor[typing.Any]) -> 'ParameterDescriptor': ...
    @typing.overload
    def extractSubset(self, collection: typing.Union[java.util.Collection[FieldDescriptor[typing.Any]], typing.Sequence[FieldDescriptor[typing.Any]], typing.Set[FieldDescriptor[typing.Any]]]) -> 'ParameterDescriptor': ...
    def getAssociatedFieldDescriptors(self) -> java.util.Set[FieldDescriptor[typing.Any]]: ...
    def getAssociatedFields(self) -> java.util.Map[FieldDescriptor[typing.Any], typing.Any]: ...
    _getFieldValue__T = typing.TypeVar('_getFieldValue__T')  # <T>
    def getFieldValue(self, fieldDescriptor: FieldDescriptor[_getFieldValue__T]) -> _getFieldValue__T:
        """
            Gets the value currently mapped to a given field descriptor.
        
            Parameters:
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<T> fieldDescriptor): the field descriptor
        
            Returns:
                the value mapped to the specified field descriptor, or :code:`null` if the field descriptor is not associated with this
                parameter descriptor
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the provided field descriptor is :code:`null`
        
        
        """
        ...
    @typing.overload
    def getName(self) -> str:
        """
            Gets the name of this parameter descriptor, which is comprised of the associated field values separated by an underscore
            (printed in reverse order by default).
        
            Returns:
                the name of this parameter descriptor
        
        """
        ...
    @typing.overload
    def getName(self, boolean: bool) -> str:
        """
            Gets the name of this parameter descriptor, which is comprised of the associated field values separated by an
            underscore.
        
            Parameters:
                reverseOrder (boolean): whether or not the field values should be printed in reverse order
        
            Returns:
                the name of this parameter descriptor
        
            Gets the name of this parameter descriptor, which is comprised of the associated field values separated by the specified
            string (printed in reverse order by default).
        
            Parameters:
                separator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string used as separator between two field values
        
            Returns:
                the name of this parameter descriptor
        
        """
        ...
    @typing.overload
    def getName(self, string: str) -> str: ...
    @typing.overload
    def getName(self, string: str, boolean: bool) -> str:
        """
            Gets the name of this parameter descriptor, which is comprised of the associated field values separated by the specified
            string.
        
            Parameters:
                separator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string used as separator between two field values
                reverseOrder (boolean): whether or not the field values should be printed in reverse order
        
            Returns:
                the name of this parameter descriptor
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def intersectionWith(self, parameterDescriptor: 'ParameterDescriptor') -> 'ParameterDescriptor':
        """
            Extracts the field descriptors associated with both this parameter descriptor and the one provided, and which are mapped
            to the same value.
        
            Parameters:
                descriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the other parameter descriptor
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` instance resulting from the intersection
        
        
        """
        ...
    def isEmpty(self) -> bool:
        """
            Checks whether this parameter descriptor is currently associated with anything or not.
        
            Returns:
                :code:`true` if this parameter descriptor is not associated with anything, :code:`false` otherwise
        
        
        """
        ...
    def isMutable(self) -> bool:
        """
            Checks if this parameter descriptor is currently mutable or not.
        
            The mutability of this parameter descriptor can be enabled or disabled at will through the
            :meth:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor.setMutability` method. Methods updating a parameter
            descriptor should always check its mutability beforehand.
        
            Returns:
                :code:`true` if this parameter descriptor is currently mutable, :code:`false` otherwise
        
        
        """
        ...
    def mergeWith(self, parameterDescriptor: 'ParameterDescriptor') -> 'ParameterDescriptor':
        """
            Merges this parameter descriptor with another one.
        
            The field descriptors of both this instance and the one provided are kept. When a field descriptor is associated with
            both instances, the provided parameter descriptor takes precedence and replaces the currently mapped value.
        
            Parameters:
                descriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the other parameter descriptor
        
            Returns:
                the :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor` instance resulting from the merging process
        
        
        """
        ...
    _removeField_0__T = typing.TypeVar('_removeField_0__T')  # <T>
    _removeField_1__T = typing.TypeVar('_removeField_1__T')  # <T>
    @typing.overload
    def removeField(self, fieldDescriptor: FieldDescriptor[_removeField_0__T], t: _removeField_0__T) -> bool:
        """
            Removes a given field descriptor from this parameter descriptor if it is currently mapped to the specified value.
        
            Parameters:
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<T> fieldDescriptor): the field descriptor to be removed
                fieldValue (T): the value expected to be mapped with the specified field descriptor
        
            Returns:
                :code:`true` if the specified field descriptor and its mapped value were removed, :code:`false` otherwise
        
            Raises:
                : if this parameter descriptor is currently immutable
        
        
        """
        ...
    @typing.overload
    def removeField(self, fieldDescriptor: FieldDescriptor[_removeField_1__T]) -> _removeField_1__T:
        """
            Removes a given field descriptor from this parameter descriptor.
        
            Parameters:
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<T> fieldDescriptor): the field descriptor to be removed
        
            Returns:
                the value which was previously mapped to the provided field descriptor, or :code:`null` if this field descriptor was not
                associated with this parameter descriptor
        
            Raises:
                : if this parameter descriptor is currently immutable
        
        """
        ...
    def removeUntypedField(self, fieldDescriptor: FieldDescriptor[typing.Any], object: typing.Any) -> bool:
        """
            Removes a given field descriptor from this parameter descriptor if it is currently mapped to the specified value.
        
            Parameters:
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?> fieldDescriptor): the field descriptor to be removed
                fieldValue (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the value expected to be mapped with the specified field descriptor
        
            Returns:
                :code:`true` if the specified field descriptor and its mapped value were removed, :code:`false` otherwise
        
            Raises:
                : if this parameter descriptor is currently immutable
        
        
        """
        ...
    @typing.overload
    def removeUntypedFields(self, *fieldDescriptor: FieldDescriptor[typing.Any]) -> None: ...
    @typing.overload
    def removeUntypedFields(self, collection: typing.Union[java.util.Collection[FieldDescriptor[typing.Any]], typing.Sequence[FieldDescriptor[typing.Any]], typing.Set[FieldDescriptor[typing.Any]]]) -> None: ...
    _replaceField_0__T = typing.TypeVar('_replaceField_0__T')  # <T>
    _replaceField_1__T = typing.TypeVar('_replaceField_1__T')  # <T>
    @typing.overload
    def replaceField(self, fieldDescriptor: FieldDescriptor[_replaceField_0__T], t: _replaceField_0__T, t2: _replaceField_0__T) -> bool:
        """
            Replaces the value mapped to a given field descriptor if it is currently associated with this parameter descriptor and
            mapped to the specified value.
        
            Parameters:
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<T> fieldDescriptor): the field descriptor whose mapped value is to be replaced
                oldFieldValue (T): the value expected to be mapped to the specified field descriptor
                newFieldValue (T): the new value to be mapped to the specified field descriptor
        
            Returns:
                :code:`true` if the value mapped to the specified field descriptor was replaced, :code:`false` otherwise
        
            Raises:
                : if this parameter descriptor is currently immutable
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the new field value is :code:`null`
        
        
        """
        ...
    @typing.overload
    def replaceField(self, fieldDescriptor: FieldDescriptor[_replaceField_1__T], t: _replaceField_1__T) -> _replaceField_1__T:
        """
            Replaces the value mapped to a given field descriptor if it is currently associated with this parameter descriptor.
        
            Parameters:
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<T> fieldDescriptor): the field descriptor whose mapped value is to be replaced
                fieldValue (T): the new value to be mapped to the specified field descriptor
        
            Returns:
                the value which was previously mapped to the provided field descriptor, or :code:`null` if this field descriptor is not
                associated with this parameter descriptor
        
            Raises:
                : if this parameter descriptor is currently immutable
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the new field value is :code:`null`
        
        """
        ...
    @typing.overload
    def replaceUntypedField(self, fieldDescriptor: FieldDescriptor[typing.Any], object: typing.Any, object2: typing.Any) -> bool:
        """
            Replaces the value mapped to a given field descriptor if it is currently associated with this parameter descriptor and
            mapped to the specified value.
        
            **Important:** the provided values must be assignable to the class specified by the field descriptor. An exception will
            be automatically thrown if that is not the case.
        
            Parameters:
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?> fieldDescriptor): the field descriptor whose mapped value is to be replaced
                oldFieldValue (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the value expected to be mapped to the specified field descriptor
                newFieldValue (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the new value to be mapped to the specified field descriptor
        
            Returns:
                :code:`true` if the value mapped to the specified field descriptor was replaced, :code:`false` otherwise
        
            Raises:
                : if this parameter descriptor is currently immutable
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the new field value is :code:`null`
                : if the new field value cannot be cast to the class specified by the field descriptor
        
        
        """
        ...
    @typing.overload
    def replaceUntypedField(self, fieldDescriptor: FieldDescriptor[typing.Any], object: typing.Any) -> typing.Any:
        """
            Replaces the value mapped to a given field descriptor if it is currently associated with this parameter descriptor.
        
            **Important:** the provided value must be assignable to the class specified by the field descriptor. An exception will
            be automatically thrown if that is not the case.
        
            Parameters:
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?> fieldDescriptor): the field descriptor whose mapped value is to be replaced
                fieldValue (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): the new value to be mapped to the specified field descriptor
        
            Returns:
                the value which was previously mapped to the provided field descriptor, or :code:`null` if this field descriptor is not
                associated with this parameter descriptor
        
            Raises:
                : if this parameter descriptor is currently immutable
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the new field value is :code:`null`
                : if the new field value cannot be cast to the class specified by the field descriptor
        
        """
        ...
    def setMutability(self, boolean: bool) -> 'ParameterDescriptor':
        """
            Enables or disables the mutability of this parameter descriptor.
        
            Parameters:
                enabled (boolean): whether or not to allow this parameter descriptor to be mutable
        
            Returns:
                this parameter descriptor (for chaining)
        
        
        """
        ...
    @typing.overload
    def toString(self) -> str:
        """
            Gets a string representation of this parameter descriptor which includes the name of this class, the name of associated
            the field descriptors and their mapped values (printed in  reverse order by default).
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of this parameter descriptor
        
        """
        ...
    @typing.overload
    def toString(self, boolean: bool) -> str:
        """
            Gets a string representation of this parameter descriptor which includes the name of this class, the name of associated
            the field descriptors and their mapped values.
        
            Parameters:
                reverseOrder (boolean): whether or not the field descriptors and their mapped values should be printed in reverse order
        
            Returns:
                a string representation of this parameter descriptor
        
        """
        ...
    @typing.overload
    def toString(self, string: str, string2: str, boolean: bool, boolean2: bool, boolean3: bool, boolean4: bool) -> str:
        """
            Gets a string representation of this parameter descriptor.
        
            Parameters:
                keySeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string used as separator between a key and its mapped value
                entrySeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string used as separator between two entries
                printClassName (boolean): whether or not the name of this class should be printed
                printFieldName (boolean): whether or not the name associated with the field descriptors should be printed
                printFieldValue (boolean): whether or not the values mapped to the field descriptors should be printed
                reverseOrder (boolean): whether or not the field descriptors and their mapped values should be printed in reverse order
        
            Returns:
                a string representation of this parameter descriptor
        
        
        """
        ...

class ParameterUtils:
    """
    public final class ParameterUtils extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This utility class defines static methods to manage :class:`~fr.cnes.sirius.patrius.math.parameter.Parameter` and
        :class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`.
    """
    _addFieldIfAbsentToParameterDescriptors__T = typing.TypeVar('_addFieldIfAbsentToParameterDescriptors__T')  # <T>
    @staticmethod
    def addFieldIfAbsentToParameterDescriptors(collection: typing.Union[java.util.Collection[ParameterDescriptor], typing.Sequence[ParameterDescriptor], typing.Set[ParameterDescriptor]], fieldDescriptor: FieldDescriptor[_addFieldIfAbsentToParameterDescriptors__T], t: _addFieldIfAbsentToParameterDescriptors__T) -> java.util.Set[ParameterDescriptor]: ...
    _addFieldIfAbsentToParameters_0__T = typing.TypeVar('_addFieldIfAbsentToParameters_0__T')  # <T>
    _addFieldIfAbsentToParameters_1__T = typing.TypeVar('_addFieldIfAbsentToParameters_1__T')  # <T>
    @typing.overload
    @staticmethod
    def addFieldIfAbsentToParameters(iParameterizable: IParameterizable, fieldDescriptor: FieldDescriptor[_addFieldIfAbsentToParameters_0__T], t: _addFieldIfAbsentToParameters_0__T) -> java.util.Set[Parameter]: ...
    @typing.overload
    @staticmethod
    def addFieldIfAbsentToParameters(collection: typing.Union[java.util.Collection[Parameter], typing.Sequence[Parameter], typing.Set[Parameter]], fieldDescriptor: FieldDescriptor[_addFieldIfAbsentToParameters_1__T], t: _addFieldIfAbsentToParameters_1__T) -> java.util.Set[Parameter]: ...
    _addFieldToParameterDescriptors__T = typing.TypeVar('_addFieldToParameterDescriptors__T')  # <T>
    @staticmethod
    def addFieldToParameterDescriptors(collection: typing.Union[java.util.Collection[ParameterDescriptor], typing.Sequence[ParameterDescriptor], typing.Set[ParameterDescriptor]], fieldDescriptor: FieldDescriptor[_addFieldToParameterDescriptors__T], t: _addFieldToParameterDescriptors__T) -> java.util.Map[ParameterDescriptor, _addFieldToParameterDescriptors__T]: ...
    _addFieldToParameters_0__T = typing.TypeVar('_addFieldToParameters_0__T')  # <T>
    _addFieldToParameters_1__T = typing.TypeVar('_addFieldToParameters_1__T')  # <T>
    @typing.overload
    @staticmethod
    def addFieldToParameters(iParameterizable: IParameterizable, fieldDescriptor: FieldDescriptor[_addFieldToParameters_0__T], t: _addFieldToParameters_0__T) -> java.util.Map[Parameter, _addFieldToParameters_0__T]: ...
    @typing.overload
    @staticmethod
    def addFieldToParameters(collection: typing.Union[java.util.Collection[Parameter], typing.Sequence[Parameter], typing.Set[Parameter]], fieldDescriptor: FieldDescriptor[_addFieldToParameters_1__T], t: _addFieldToParameters_1__T) -> java.util.Map[Parameter, _addFieldToParameters_1__T]: ...
    @typing.overload
    @staticmethod
    def buildDefaultParameterDescriptors(int: int) -> java.util.List[ParameterDescriptor]: ...
    @typing.overload
    @staticmethod
    def buildDefaultParameterDescriptors(int: int, int2: int) -> java.util.List[ParameterDescriptor]: ...
    @staticmethod
    def buildOrbitalParameterDescriptors(orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> java.util.List[ParameterDescriptor]: ...
    @staticmethod
    def buildOrbitalParameters(orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> java.util.List[Parameter]: ...
    @staticmethod
    def concatenateParameterDescriptorNames(collection: typing.Union[java.util.Collection[ParameterDescriptor], typing.Sequence[ParameterDescriptor], typing.Set[ParameterDescriptor]], string: str, string2: str, boolean: bool) -> str: ...
    @staticmethod
    def concatenateParameterNames(collection: typing.Union[java.util.Collection[Parameter], typing.Sequence[Parameter], typing.Set[Parameter]], string: str, string2: str, boolean: bool) -> str: ...
    _extractParameterDescriptors_2__T = typing.TypeVar('_extractParameterDescriptors_2__T')  # <T>
    @typing.overload
    @staticmethod
    def extractParameterDescriptors(collection: typing.Union[java.util.Collection[Parameter], typing.Sequence[Parameter], typing.Set[Parameter]]) -> java.util.List[ParameterDescriptor]: ...
    @typing.overload
    @staticmethod
    def extractParameterDescriptors(collection: typing.Union[java.util.Collection[ParameterDescriptor], typing.Sequence[ParameterDescriptor], typing.Set[ParameterDescriptor]], fieldDescriptor: FieldDescriptor[typing.Any]) -> java.util.List[ParameterDescriptor]: ...
    @typing.overload
    @staticmethod
    def extractParameterDescriptors(collection: typing.Union[java.util.Collection[ParameterDescriptor], typing.Sequence[ParameterDescriptor], typing.Set[ParameterDescriptor]], fieldDescriptor: FieldDescriptor[_extractParameterDescriptors_2__T], predicate: typing.Union[java.util.function.Predicate[_extractParameterDescriptors_2__T], typing.Callable[[_extractParameterDescriptors_2__T], bool]]) -> java.util.List[ParameterDescriptor]: ...
    _extractParameters_1__T = typing.TypeVar('_extractParameters_1__T')  # <T>
    @typing.overload
    @staticmethod
    def extractParameters(collection: typing.Union[java.util.Collection[Parameter], typing.Sequence[Parameter], typing.Set[Parameter]], fieldDescriptor: FieldDescriptor[typing.Any]) -> java.util.List[Parameter]: ...
    @typing.overload
    @staticmethod
    def extractParameters(collection: typing.Union[java.util.Collection[Parameter], typing.Sequence[Parameter], typing.Set[Parameter]], fieldDescriptor: FieldDescriptor[_extractParameters_1__T], predicate: typing.Union[java.util.function.Predicate[_extractParameters_1__T], typing.Callable[[_extractParameters_1__T], bool]]) -> java.util.List[Parameter]: ...
    @typing.overload
    @staticmethod
    def removeFieldFromParameters(iParameterizable: IParameterizable, fieldDescriptor: FieldDescriptor[typing.Any]) -> None:
        """
            Removes a given field descriptor from the parameters of a parameterizable object.
        
            Note that this method will not have any effect if
            :meth:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable.getParameters` provides a copy of the parameters stored
            by the class implementing the :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable` interface (instead of a
            direct access to their reference).
        
            Parameters:
                parameterizable (:class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`): the parameterizable object whose parameters are to be updated
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?> fieldDescriptor): the field descriptor to be removed
        
        public static void removeFieldFromParameters(`Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`> parameters, :class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?> fieldDescriptor)
        
            Removes a given field descriptor from multiple parameters.
        
            Parameters:
                parameters (`Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`> parameters): the parameters whose parameter descriptor is to be updated
                fieldDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<?> fieldDescriptor): the field descriptor to be removed
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def removeFieldFromParameters(collection: typing.Union[java.util.Collection[Parameter], typing.Sequence[Parameter], typing.Set[Parameter]], fieldDescriptor: FieldDescriptor[typing.Any]) -> None: ...

class StandardFieldDescriptors:
    """
    public final class StandardFieldDescriptors extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Standard field descriptors.
    """
    PARAMETER_NAME: typing.ClassVar[FieldDescriptor] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`> PARAMETER_NAME
    
        Field descriptor to associate with the name of a parameter.
    
    """
    FORCE_MODEL: typing.ClassVar[FieldDescriptor] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<`Class <http://docs.oracle.com/javase/8/docs/api/java/lang/Class.html?is-external=true>`<? extends :class:`~fr.cnes.sirius.patrius.forces.ForceModel`>> FORCE_MODEL
    
        Field descriptor to associate with a force model.
    
    """
    GRAVITY_MODEL: typing.ClassVar[FieldDescriptor] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<`Class <http://docs.oracle.com/javase/8/docs/api/java/lang/Class.html?is-external=true>`<? extends :class:`~fr.cnes.sirius.patrius.forces.gravity.GravityModel`>> GRAVITY_MODEL
    
        Field descriptor to associate with a gravitational attraction model.
    
    """
    DATE: typing.ClassVar[FieldDescriptor] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`> DATE
    
        Field descriptor to associate with a date.
    
    """
    DATE_INTERVAL: typing.ClassVar[FieldDescriptor] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`> DATE_INTERVAL
    
        Field descriptor to associate with a date interval.
    
    """
    ORBITAL_COORDINATE: typing.ClassVar[FieldDescriptor] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.parameter.FieldDescriptor`<:class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate`> ORBITAL_COORDINATE
    
        Field descriptor to associate with an orbital coordinate.
    
    """

class IJacobiansParameterizable(IParameterizable):
    """
    public interface IJacobiansParameterizable extends :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
    
        This class is used to define jacobian function parameters.
    
        Since:
            2.3
    """
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def supportsJacobianParameter(self, parameter: Parameter) -> bool:
        """
            Check if a jacobian parameter is supported.
        
            Parameters:
                param (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to check
        
            Returns:
                true if the parameter is supported.
        
        
        """
        ...

class IParameterizableFunction(IParameterizable):
    """
    public interface IParameterizableFunction extends :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
    
    
        This class is used to define a parameterizable function. This function is composed of Parameter such as : f(t) = a * t +
        b, with a and b Parameter
    
        The method :meth:`~fr.cnes.sirius.patrius.math.parameter.IParameterizableFunction.value` return the value of the
        function depending on the spacecraft state state
    
        Since:
            2.3
    """
    def value(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Getting the value of the function.
        
            Parameters:
                state (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the spacecraft state
        
            Returns:
                the value of the function.
        
        
        """
        ...

class Parameterizable(IParameterizable):
    """
    public class Parameterizable extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
    
        Simple class providing a list and method for handling :class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`.
    
        Since:
            2.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, *iParamDiffFunction: 'IParamDiffFunction'): ...
    @typing.overload
    def __init__(self, *parameter: Parameter): ...
    @typing.overload
    def __init__(self, arrayList: java.util.ArrayList[Parameter]): ...
    def getParameters(self) -> java.util.ArrayList[Parameter]: ...
    def supportsParameter(self, parameter: Parameter) -> bool:
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

class IParamDiffFunction(IParameterizableFunction):
    """
    public interface IParamDiffFunction extends :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizableFunction`
    
        This class is used to define a derivative function parameterizable.
    
        Since:
            2.3
    """
    def derivativeValue(self, parameter: Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Compute the derivative value with respect to the input parameter.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): current state
        
            Returns:
                the derivative value
        
        
        """
        ...
    def isDifferentiableBy(self, parameter: Parameter) -> bool:
        """
            Tell if the function is differentiable by the given parameter.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): function parameter
        
            Returns:
                true if the function is differentiable by the given parameter.
        
        
        """
        ...

class JacobiansParameterizable(Parameterizable, IJacobiansParameterizable):
    """
    public abstract class JacobiansParameterizable extends :class:`~fr.cnes.sirius.patrius.math.parameter.Parameterizable` implements :class:`~fr.cnes.sirius.patrius.math.parameter.IJacobiansParameterizable`
    
    
        Abstract class to define generic function of :class:`~fr.cnes.sirius.patrius.math.parameter.IJacobiansParameterizable`.
    
        Since:
            2.3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, *iParamDiffFunction: IParamDiffFunction): ...
    @typing.overload
    def __init__(self, *parameter: Parameter): ...
    @typing.overload
    def __init__(self, arrayList: java.util.ArrayList[Parameter]): ...
    def supportsJacobianParameter(self, parameter: Parameter) -> bool:
        """
            Check if a jacobian parameter is supported.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IJacobiansParameterizable.supportsJacobianParameter` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IJacobiansParameterizable`
        
            Parameters:
                param (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to check
        
            Returns:
                true if the parameter is supported.
        
        
        """
        ...

class IntervalsFunction(Parameterizable, IParamDiffFunction):
    @typing.overload
    def __init__(self, collection: typing.Union[java.util.Collection[IParamDiffFunction], typing.Sequence[IParamDiffFunction], typing.Set[IParamDiffFunction]], collection2: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.time.AbsoluteDateInterval], typing.Sequence[fr.cnes.sirius.patrius.time.AbsoluteDateInterval], typing.Set[fr.cnes.sirius.patrius.time.AbsoluteDateInterval]]): ...
    @typing.overload
    def __init__(self, collection: typing.Union[java.util.Collection[IParamDiffFunction], typing.Sequence[IParamDiffFunction], typing.Set[IParamDiffFunction]], collection2: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.time.AbsoluteDateInterval], typing.Sequence[fr.cnes.sirius.patrius.time.AbsoluteDateInterval], typing.Set[fr.cnes.sirius.patrius.time.AbsoluteDateInterval]], boolean: bool): ...
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, IParamDiffFunction], typing.Mapping[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, IParamDiffFunction]]): ...
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, IParamDiffFunction], typing.Mapping[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, IParamDiffFunction]], boolean: bool): ...
    def derivativeValue(self, parameter: Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    @typing.overload
    def getEntry(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.tools.cache.CacheEntry[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, IParamDiffFunction]: ...
    @typing.overload
    def getEntry(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool) -> fr.cnes.sirius.patrius.tools.cache.CacheEntry[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, IParamDiffFunction]: ...
    def getFunctions(self) -> java.util.List[IParamDiffFunction]: ...
    def getIntervalFunctionAssociation(self) -> java.util.Map[fr.cnes.sirius.patrius.time.AbsoluteDateInterval, IParamDiffFunction]: ...
    def getIntervals(self) -> fr.cnes.sirius.patrius.time.AbsoluteDateIntervalsList: ...
    def isDifferentiableBy(self, parameter: Parameter) -> bool: ...
    def toString(self) -> str: ...
    def value(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...

class LinearCombinationFunction(IParamDiffFunction):
    @typing.overload
    def __init__(self, collection: typing.Union[java.util.Collection[typing.Union[java.util.function.Function[fr.cnes.sirius.patrius.propagation.SpacecraftState, float], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], float]]], typing.Sequence[typing.Union[java.util.function.Function[fr.cnes.sirius.patrius.propagation.SpacecraftState, float], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], float]]], typing.Set[typing.Union[java.util.function.Function[fr.cnes.sirius.patrius.propagation.SpacecraftState, float], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], float]]]]): ...
    @typing.overload
    def __init__(self, map: typing.Union[java.util.Map[Parameter, typing.Union[java.util.function.Function[fr.cnes.sirius.patrius.propagation.SpacecraftState, float], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], float]]], typing.Mapping[Parameter, typing.Union[java.util.function.Function[fr.cnes.sirius.patrius.propagation.SpacecraftState, float], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], float]]]]): ...
    def derivativeValue(self, parameter: Parameter, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    def getParameters(self) -> java.util.ArrayList[Parameter]: ...
    def isDifferentiableBy(self, parameter: Parameter) -> bool: ...
    def supportsParameter(self, parameter: Parameter) -> bool: ...
    def value(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...

class ConstantFunction(LinearCombinationFunction):
    """
    public class ConstantFunction extends :class:`~fr.cnes.sirius.patrius.math.parameter.LinearCombinationFunction`
    
        This class is used to define a constant parameterizable function.
    
        This function is serializable.
    
        Since:
            2.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, parameter: Parameter): ...
    @typing.overload
    def __init__(self, string: str, double: float): ...
    def getParameter(self) -> Parameter:
        """
            Getter for the parameter associated to this constant function.
        
            Returns:
                the parameter
        
        
        """
        ...
    def getParameters(self) -> java.util.ArrayList[Parameter]: ...
    def toString(self) -> str:
        """
            Getter for a String representation of this function.
        
            Overrides:
                 in class 
        
            Returns:
                a String representation of this function
        
        
        """
        ...
    @typing.overload
    def value(self) -> float:
        """
            Value of the parameter.
        
            Returns:
                the value of the parameter parameter as double
        
        
        """
        ...
    @typing.overload
    def value(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...

class LinearFunction(LinearCombinationFunction):
    """
    public class LinearFunction extends :class:`~fr.cnes.sirius.patrius.math.parameter.LinearCombinationFunction`
    
        This class is used to define parameterizable linear function: *f = a0 + a1 * (t - t0)*.
    
        This function is serializable.
    
        Since:
            2.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, parameter: Parameter, parameter2: Parameter): ...
    def getParameters(self) -> java.util.ArrayList[Parameter]: ...
    def toString(self) -> str:
        """
            Getter for a String representation of this function.
        
            Overrides:
                 in class 
        
            Returns:
                a String representation of this function
        
        
        """
        ...

class NthOrderPolynomialFunction(LinearCombinationFunction):
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, *double: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, *parameter: Parameter): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, int: int): ...
    def getParameters(self) -> java.util.ArrayList[Parameter]: ...
    def toString(self) -> str: ...

class PiecewiseFunction(IntervalsFunction):
    """
    public class PiecewiseFunction extends :class:`~fr.cnes.sirius.patrius.math.parameter.IntervalsFunction`
    
        This class is used to define parameterizable piecewize function.
    
        It is defined by a collection of :class:`~fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction`, each sub function
        applying to a certain interval defined by the first date of the interval.
    
        First interval from PAST_INFINITY to the first date.
    
    
        Last interval from the last date to FUTURE_INFINITY.
    
    
        The interval structure is defined as [k, k+1[ (first bracket closed, second opened).
    
        Each function parameters descriptor is enriched with a
        :meth:`~fr.cnes.sirius.patrius.math.parameter.StandardFieldDescriptors.DATE_INTERVAL` corresponding to the interval
        where the parameter is defined.
    
        Since:
            2.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, collection: typing.Union[java.util.Collection[IParamDiffFunction], typing.Sequence[IParamDiffFunction], typing.Set[IParamDiffFunction]], collection2: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.time.AbsoluteDate], typing.Sequence[fr.cnes.sirius.patrius.time.AbsoluteDate], typing.Set[fr.cnes.sirius.patrius.time.AbsoluteDate]]): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.parameter")``.

    ConstantFunction: typing.Type[ConstantFunction]
    FieldDescriptor: typing.Type[FieldDescriptor]
    IJacobiansParameterizable: typing.Type[IJacobiansParameterizable]
    IParamDiffFunction: typing.Type[IParamDiffFunction]
    IParameterizable: typing.Type[IParameterizable]
    IParameterizableFunction: typing.Type[IParameterizableFunction]
    IntervalsFunction: typing.Type[IntervalsFunction]
    JacobiansParameterizable: typing.Type[JacobiansParameterizable]
    LinearCombinationFunction: typing.Type[LinearCombinationFunction]
    LinearFunction: typing.Type[LinearFunction]
    NthOrderPolynomialFunction: typing.Type[NthOrderPolynomialFunction]
    Parameter: typing.Type[Parameter]
    ParameterDescriptor: typing.Type[ParameterDescriptor]
    ParameterUtils: typing.Type[ParameterUtils]
    Parameterizable: typing.Type[Parameterizable]
    PiecewiseFunction: typing.Type[PiecewiseFunction]
    StandardFieldDescriptors: typing.Type[StandardFieldDescriptors]
