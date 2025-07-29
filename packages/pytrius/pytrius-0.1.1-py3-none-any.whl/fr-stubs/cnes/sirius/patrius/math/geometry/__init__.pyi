
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.geometry.euclidean
import fr.cnes.sirius.patrius.math.geometry.partitioning
import fr.cnes.sirius.patrius.math.linear
import java.io
import java.lang
import java.text
import java.util
import typing



class Space(java.io.Serializable):
    """
    public interface Space extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface represents a generic space, with affine and vectorial counterparts.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
    """
    def getDimension(self) -> int:
        """
            Get the dimension of the space.
        
            Returns:
                dimension of the space
        
        
        """
        ...
    def getSubSpace(self) -> 'Space':
        """
            Get the n-1 dimension subspace of this space.
        
            Returns:
                n-1 dimension sub-space of this space
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathUnsupportedOperationException`: for dimension-1 spaces which do not have sub-spaces
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.Space.getDimension`
        
        
        """
        ...

_Vector__S = typing.TypeVar('_Vector__S', bound=Space)  # <S>
class Vector(java.io.Serializable, typing.Generic[_Vector__S]):
    """
    public interface Vector<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`> extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface represents a generic vector in a vectorial space or a point in an affine space.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.geometry.Space`, :class:`~fr.cnes.sirius.patrius.math.geometry.Vector`
    """
    @typing.overload
    def add(self, double: float, vector: 'Vector'[_Vector__S]) -> 'Vector'[_Vector__S]: ...
    @typing.overload
    def add(self, vector: 'Vector'[_Vector__S]) -> 'Vector'[_Vector__S]: ...
    def distance(self, vector: 'Vector'[_Vector__S]) -> float: ...
    def distance1(self, vector: 'Vector'[_Vector__S]) -> float: ...
    def distanceInf(self, vector: 'Vector'[_Vector__S]) -> float: ...
    def distanceSq(self, vector: 'Vector'[_Vector__S]) -> float: ...
    def dotProduct(self, vector: 'Vector'[_Vector__S]) -> float: ...
    def getNorm(self) -> float:
        """
            Get the L :sub:`2` norm for the vector.
        
            Returns:
                Euclidean norm for the vector
        
        
        """
        ...
    def getNorm1(self) -> float:
        """
            Get the L :sub:`1` norm for the vector.
        
            Returns:
                L :sub:`1` norm for the vector
        
        
        """
        ...
    def getNormInf(self) -> float:
        """
            Get the L :sub:`∞` norm for the vector.
        
            Returns:
                L :sub:`∞` norm for the vector
        
        
        """
        ...
    def getNormSq(self) -> float:
        """
            Get the square of the norm for the vector.
        
            Returns:
                square of the Euclidean norm for the vector
        
        
        """
        ...
    def getRealVector(self) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Get a RealVector with identical data.
        
            Returns:
                the RealVector
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.math.linear.RealVector`
        
        
        """
        ...
    def getSpace(self) -> Space:
        """
            Get the space to which the vector belongs.
        
            Returns:
                containing space
        
        
        """
        ...
    def getZero(self) -> 'Vector'[_Vector__S]: ...
    def isInfinite(self) -> bool:
        """
            Returns true if any coordinate of this vector is infinite and none are NaN; false otherwise
        
            Returns:
                true if any coordinate of this vector is infinite and none are NaN; false otherwise
        
        
        """
        ...
    def isNaN(self) -> bool:
        """
            Returns true if any coordinate of this vector is NaN; false otherwise
        
            Returns:
                true if any coordinate of this vector is NaN; false otherwise
        
        
        """
        ...
    def negate(self) -> 'Vector'[_Vector__S]: ...
    def normalize(self) -> 'Vector'[_Vector__S]: ...
    def scalarMultiply(self, double: float) -> 'Vector'[_Vector__S]: ...
    @typing.overload
    def subtract(self, double: float, vector: 'Vector'[_Vector__S]) -> 'Vector'[_Vector__S]: ...
    @typing.overload
    def subtract(self, vector: 'Vector'[_Vector__S]) -> 'Vector'[_Vector__S]: ...
    def toString(self, numberFormat: java.text.NumberFormat) -> str:
        """
            Get a string representation of this vector.
        
            Parameters:
                format (`NumberFormat <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>`): the custom format for components
        
            Returns:
                a string representation of this vector
        
        
        """
        ...

_VectorFormat__S = typing.TypeVar('_VectorFormat__S', bound=Space)  # <S>
class VectorFormat(typing.Generic[_VectorFormat__S]):
    """
    public abstract class VectorFormat<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Formats a vector in components list format "{x; y; ...}".
    
        The prefix and suffix "{" and "}" and the separator "; " can be replaced by any user-defined strings. The number format
        for components can be configured.
    
        White space is ignored at parse time, even if it is in the prefix, suffix or separator specifications. So even if the
        default separator does include a space character that is used at format time, both input string "{1;1;1}" and " { 1 ; 1
        ; 1 } " will be parsed without error and the same vector will be returned. In the second case, however, the parse
        position after parsing will be just after the closing curly brace, i.e. just before the trailing space.
    
        Since:
            3.0
    """
    DEFAULT_PREFIX: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_PREFIX
    
        The default prefix: "{".
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_SUFFIX: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_SUFFIX
    
        The default suffix: "}".
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_SEPARATOR: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_SEPARATOR
    
        The default separator: ", ".
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def format(self, vector: Vector[_VectorFormat__S], stringBuffer: java.lang.StringBuffer, fieldPosition: java.text.FieldPosition) -> java.lang.StringBuffer:
        """
            Formats the coordinates of a :class:`~fr.cnes.sirius.patrius.math.geometry.Vector` to produce a string.
        
            Parameters:
                toAppendTo (`StringBuffer <http://docs.oracle.com/javase/8/docs/api/java/lang/StringBuffer.html?is-external=true>`): where the text is to be appended
                pos (`FieldPosition <http://docs.oracle.com/javase/8/docs/api/java/text/FieldPosition.html?is-external=true>`): On input: an alignment field, if desired. On output: the offsets of the alignment field
                coordinates (double...): coordinates of the object to format.
        
            Returns:
                the value passed in as toAppendTo.
        
        
        """
        ...
    @typing.overload
    def format(self, vector: Vector[_VectorFormat__S]) -> str: ...
    @staticmethod
    def getAvailableLocales() -> typing.MutableSequence[java.util.Locale]:
        """
            Get the set of locales for which point/vector formats are available.
        
            This is the same set as the `null
            <http://docs.oracle.com/javase/8/docs/api/java/text/NumberFormat.html?is-external=true>` set.
        
            Returns:
                available point/vector format locales.
        
        
        """
        ...
    def getFormat(self) -> java.text.NumberFormat:
        """
            Get the components format.
        
            Returns:
                components format.
        
        
        """
        ...
    def getPrefix(self) -> str:
        """
            Get the format prefix.
        
            Returns:
                format prefix.
        
        
        """
        ...
    def getSeparator(self) -> str:
        """
            Get the format separator between components.
        
            Returns:
                format separator.
        
        
        """
        ...
    def getSuffix(self) -> str:
        """
            Get the format suffix.
        
            Returns:
                format suffix.
        
        
        """
        ...
    @typing.overload
    def parse(self, string: str) -> Vector[_VectorFormat__S]: ...
    @typing.overload
    def parse(self, string: str, parsePosition: java.text.ParsePosition) -> Vector[_VectorFormat__S]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.geometry")``.

    Space: typing.Type[Space]
    Vector: typing.Type[Vector]
    VectorFormat: typing.Type[VectorFormat]
    euclidean: fr.cnes.sirius.patrius.math.geometry.euclidean.__module_protocol__
    partitioning: fr.cnes.sirius.patrius.math.geometry.partitioning.__module_protocol__
