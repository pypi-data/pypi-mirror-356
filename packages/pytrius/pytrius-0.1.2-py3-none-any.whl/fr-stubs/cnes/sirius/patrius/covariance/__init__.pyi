
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



_AbstractOrbitalCovariance__T = typing.TypeVar('_AbstractOrbitalCovariance__T', bound='AbstractOrbitalCovariance')  # <T>
class AbstractOrbitalCovariance(fr.cnes.sirius.patrius.time.TimeStamped, java.io.Serializable, typing.Generic[_AbstractOrbitalCovariance__T]):
    """
    public abstract class AbstractOrbitalCovariance<T extends AbstractOrbitalCovariance<T>> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Abstract representation of an orbital covariance.
    
        An orbital covariance associates a :class:`~fr.cnes.sirius.patrius.covariance.Covariance` instance with a given date and
        the frame, orbit type (Cartesian, Keplerian, etc) and position angle type (mean, true, eccentric) in which it is
        expressed.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, covariance: 'Covariance', frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle): ...
    @typing.overload
    def __init__(self, symmetricPositiveMatrix: fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix, frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getCovariance(self) -> 'Covariance':
        """
            Gets the covariance.
        
            Returns:
                the covariance
        
        
        """
        ...
    def getCovarianceMatrix(self) -> fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix:
        """
            Gets the covariance matrix.
        
            Returns:
                the covariance matrix
        
        
        """
        ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Gets the frame of the covariance.
        
            Returns:
                the frame of the covariance
        
        
        """
        ...
    def getOrbitType(self) -> fr.cnes.sirius.patrius.orbits.OrbitType:
        """
            Gets the orbit type of covariance.
        
            Returns:
                the orbit type of covariance
        
        
        """
        ...
    def getParameterDescriptors(self) -> java.util.List[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor]: ...
    def getPositionAngle(self) -> fr.cnes.sirius.patrius.orbits.PositionAngle:
        """
            Gets the position angle type of the covariance.
        
            Returns:
                the position angle type of the covariance
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @typing.overload
    def toString(self) -> str:
        """
            Returns a string representation of this orbital covariance which includes its date, frame, orbit type and position angle
            type, the associated parameter descriptors, but not the covariance matrix.
        
            The date is represented in the TAI time scale.
        
            Overrides:
                 in class 
        
            Returns:
                a string representation of the orbital covariance
        
        """
        ...
    @typing.overload
    def toString(self, realMatrixFormat: fr.cnes.sirius.patrius.math.linear.RealMatrixFormat) -> str:
        """
            Returns a string representation of this orbital covariance which includes its date, frame, orbit type and position angle
            type, the associated parameter descriptors, and the covariance matrix if the provided format is not :code:`null`.
        
            The date is represented in the TAI time scale.
        
            Parameters:
                realMatrixFormat (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrixFormat`): the format used to represent the covariance matrix
        
            Returns:
                a string representation of the orbital covariance
        
            Returns a string representation of this orbital covariance which includes its date, frame, orbit type and position angle
            type, the associated parameter descriptors, and the covariance matrix if the provided format is not :code:`null`.
        
            Parameters:
                realMatrixFormat (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrixFormat`): the format used to represent the covariance matrix
                timeScale (:class:`~fr.cnes.sirius.patrius.time.TimeScale`): the time scale used to represent the date
        
            Returns:
                a string representation of the orbital covariance
        
        """
        ...
    @typing.overload
    def toString(self, realMatrixFormat: fr.cnes.sirius.patrius.math.linear.RealMatrixFormat, timeScale: fr.cnes.sirius.patrius.time.TimeScale) -> str: ...
    @typing.overload
    def toString(self, realMatrixFormat: fr.cnes.sirius.patrius.math.linear.RealMatrixFormat, timeScale: fr.cnes.sirius.patrius.time.TimeScale, string: str, string2: str, boolean: bool, boolean2: bool) -> str:
        """
            Returns a string representation of this instance which includes the name of the class (if requested), the names of the
            associated parameter descriptors and the the covariance matrix (if the specified matrix format is not :code:`null`).
        
            Parameters:
                realMatrixFormat (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrixFormat`): the format used to represent the covariance matrix
                timeScale (:class:`~fr.cnes.sirius.patrius.time.TimeScale`): the time scale used to represent the date
                nameSeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to use as a separator between the names of the parameter descriptors
                fieldSeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to use as a separator between the field values of a parameter descriptor
                printClassName (boolean): whether or not the name of this class should be printed
                reverseOrder (boolean): whether or not the field values of each parameter descriptor should be printed in reverse order
        
            Returns:
                string representation of this instance
        
        
        """
        ...
    @typing.overload
    def transformTo(self, frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> _AbstractOrbitalCovariance__T: ...
    @typing.overload
    def transformTo(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> _AbstractOrbitalCovariance__T: ...
    @typing.overload
    def transformTo(self, frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType) -> _AbstractOrbitalCovariance__T: ...
    @typing.overload
    def transformTo(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, lOFType: fr.cnes.sirius.patrius.frames.LOFType, boolean: bool) -> _AbstractOrbitalCovariance__T: ...
    @typing.overload
    def transformTo(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType) -> _AbstractOrbitalCovariance__T: ...
    @typing.overload
    def transformTo(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> _AbstractOrbitalCovariance__T: ...
    @typing.overload
    def transformTo(self, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> _AbstractOrbitalCovariance__T: ...

class Covariance(java.io.Serializable):
    """
    public class Covariance extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Covariance representation.
    
        The covariance matrix is stored in a :class:`~fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix` object.
    
    
        The covariance columns/rows are described by a list of parameter descriptors.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, symmetricPositiveMatrix: fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix): ...
    @typing.overload
    def __init__(self, symmetricPositiveMatrix: fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix, collection: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor], typing.Sequence[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor], typing.Set[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor]]): ...
    def add(self, symmetricPositiveMatrix: fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix) -> 'Covariance':
        """
            Adds the symmetric positive semi-definite matrix M to this covariance matrix and returns a new
            :class:`~fr.cnes.sirius.patrius.covariance.Covariance` instance associated with the computed matrix and the same
            parameter descriptors.
        
            Parameters:
                m (:class:`~fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix`): the covariance matrix M to be added
        
            Returns:
                a new :class:`~fr.cnes.sirius.patrius.covariance.Covariance` instance whose matrix is the sum of the two covariance
                matrices
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the matrix M is @:code:`null`
                :class:`~fr.cnes.sirius.patrius.math.linear.MatrixDimensionMismatchException`: if the two matrices are not addition compatible
        
        
        """
        ...
    def copy(self) -> 'Covariance':
        """
            Gets a copy of this :class:`~fr.cnes.sirius.patrius.covariance.Covariance` instance.
        
            This method performs a shallow copy of the parameter descriptors list and a deep copy of the covariance matrix.
        
            Returns:
                a copy of this :class:`~fr.cnes.sirius.patrius.covariance.Covariance` instance
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor.copy`
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @typing.overload
    def getCorrelationCoefficient(self, parameterDescriptor: fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor, parameterDescriptor2: fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor) -> float:
        """
            Gets the correlation coefficient ρ :sub:`i,j` for the specified row and column indexes.
        
            If i is equal to j, ρ :sub:`i,j` is equal to 1 by definition. Otherwise, ρ :sub:`i,j` is equal to C :sub:`i,j` / (σ
            :sub:`i` *σ :sub:`j` ). If the division cannot be computed because σ :sub:`i` *σ :sub:`j` is too small, ρ :sub:`i,j`
            is set to 0.
        
            Parameters:
                row (int): the row index
                column (int): the column index
        
            Returns:
                the correlation coefficient for the specified row and column
        
            Raises:
                : if one of the provided row/column indexes is not valid
        
            Gets the correlation coefficient ρ :sub:`i,j` associated with the specified parameter descriptors, the first parameter*
            descriptor being mapped to the rows of the covariance matrix (index "i"), while the second parameter descriptor is
            mapped to the columns of the covariance matrix (index "j").
        
            If i is equal to j, ρ :sub:`i,j` is equal to 1 by definition. Otherwise, ρ :sub:`i,j` is equal to C :sub:`i,j` / (σ
            :sub:`i` *σ :sub:`j` ). If the division cannot be computed because σ :sub:`i` *σ :sub:`j` is too small, ρ :sub:`i,j`
            is set to 0.
        
            Parameters:
                parameterDescriptor1 (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the first parameter descriptor
                parameterDescriptor2 (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the second parameter descriptor
        
            Returns:
                the correlation coefficient associated with the provided parameter descriptors
        
            Raises:
                : if one of the parameter descriptors is not associated with this covariance matrix
        
        
        """
        ...
    @typing.overload
    def getCorrelationCoefficient(self, int: int, int2: int) -> float: ...
    def getCorrelationCoefficientsMatrix(self) -> fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix:
        """
            Gets the correlation matrix.
        
            The correlation matrix is a symmetric positive matrix which contains the correlation coefficients of this covariance
            matrix. The correlation coefficients for the diagonal elements are equal to 1 by definition. For off-diagonal elements,
            they are equal to C :sub:`i,j` /σ :sub:`i` σ :sub:`j` , where σ :sub:`i` and σ :sub:`j` are the standard deviations
            for the i :sup:`th` and j :sup:`th` elements.
        
            Returns:
                the correlation coefficients matrix
        
        
        """
        ...
    def getCovarianceMatrix(self) -> fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix:
        """
            Gets the covariance matrix.
        
            A covariance matrix is symmetric positive semi-definite by definition. Whether these properties are actually respected
            depends on the implementation of :class:`~fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix` used to store the
            matrix.
        
            *Note that this method provides a direct access to the covariance matrix stored internally, which is possibly mutable.*
        
            Returns:
                the covariance matrix
        
        
        """
        ...
    @typing.overload
    def getMahalanobisDistance(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> float:
        """
            Gets the Mahalanobis distance of a point with respect to this covariance matrix, assuming its mean value is zero.
        
            The Mahalanobis distance is defined by:
        
        
            dM(P) = sqrt(P :sup:`T` x C :sup:`-1` x P)
        
        
            with P the point and C the covariance matrix (centered on 0).
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): the point P
        
            Returns:
                the Mahalanobis distance of the provided point with respect to this covariance matrix
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.linear.SingularMatrixException`: if the covariance matrix is singular
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the provided vector do not have the same size as the covariance matrix
                : if the computed Mahalanobis distance is negative
        
            Also see:
                Mahalanobis distance (wikipedia)
        
            Gets the Mahalanobis distance of a point with respect to this covariance matrix.
        
            The Mahalanobis distance is defined by:
        
        
            dM(P,M) = sqrt((P-M) :sup:`T` x C :sup:`-1` x (P-M))
        
        
            with P the point and C the covariance matrix centered on M.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): the point
                mean (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): the mean value of the covariance
        
            Returns:
                the Mahalanobis distance of the provided point with respect to this covariance matrix
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.linear.SingularMatrixException`: if the covariance matrix is singular
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the provided vectors have different sizes, or if they do not have the same size as the covariance matrix
                : if the computed Mahalanobis distance is negative
        
            Also see:
                Mahalanobis distance (wikipedia)
        
        
        """
        ...
    @typing.overload
    def getMahalanobisDistance(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realVector2: fr.cnes.sirius.patrius.math.linear.RealVector) -> float: ...
    def getParameterDescriptor(self, int: int) -> fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor:
        """
            Gets the parameter descriptors associated with the specified row/column of the covariance matrix.
        
            *Note that this method provides a direct access to the parameter descriptors stored internally, which are mutable.*
        
            Parameters:
                index (int): the row/column index of the parameter descriptor to be retrieved
        
            Returns:
                the parameter descriptors associated with the covariance matrix
        
        
        """
        ...
    def getParameterDescriptors(self) -> java.util.List[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor]: ...
    def getSize(self) -> int:
        """
            Gets the size of the covariance matrix.
        
            Returns:
                the size of the covariance matrix
        
        
        """
        ...
    @typing.overload
    def getStandardDeviation(self, parameterDescriptor: fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor) -> float:
        """
            Gets the standard deviation σ :sub:`i`  = sqrt(C :sub:`i,i` ) for the specified row/column index.
        
            Parameters:
                index (int): the row/column index
        
            Returns:
                the standard deviation for the specified row/column index
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if the provided index is not valid
        
            Gets the standard deviation σ :sub:`i`  = sqrt(C :sub:`i,i` ) associated with the specified parameter descriptor.
        
            Parameters:
                parameterDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the parameter descriptor
        
            Returns:
                the standard deviation of the specified parameter descriptor
        
            Raises:
                : if the parameter descriptor is not associated with this covariance matrix
        
        
        """
        ...
    @typing.overload
    def getStandardDeviation(self, int: int) -> float: ...
    def getStandardDeviationMatrix(self) -> fr.cnes.sirius.patrius.math.linear.DiagonalMatrix:
        """
            Gets the standard deviation matrix.
        
            The standard deviation matrix is a diagonal matrix which contains the square root of the diagonal elements of this
            covariance matrix.
        
            Returns:
                the standard deviation matrix
        
        
        """
        ...
    @typing.overload
    def getSubCovariance(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> 'Covariance':
        """
            Extracts the parts of the covariance associated with the specified row/column indices.
        
            This method extracts the specified rows/columns associated in order to build a new
            :class:`~fr.cnes.sirius.patrius.covariance.Covariance` instance. The provided index array may contain duplicates, but an
            exception will be thrown if it any of the indices is not a valid row/column index. This method can be used to extract
            any submatrix and/or to perform a symmetric reordering of the rows/columns of the covariance matrix.
        
            **Important:**
        
        
            Since a parameter descriptor cannot be associated with multiple rows/columns of the covariance, the provided index array
            must not contain any duplicate (an exception will be thrown if that occurs).
        
            Parameters:
                indices (int[]): the indices of the rows/columns to be extracted
        
            Returns:
                the part of the covariance associated with the specified indices
        
            Raises:
                : if one of the specified indices is not a valid row/column index for this covariance matrix, or the provided index array
                    contains any duplicate
        
        public :class:`~fr.cnes.sirius.patrius.covariance.Covariance` getSubCovariance(`Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`> selectedParameterDescriptors)
        
            Extracts the parts of the covariance associated with the specified parameter descriptors.
        
            This method extracts the rows/columns associated with the specified parameter descriptors in order to build a new
            :class:`~fr.cnes.sirius.patrius.covariance.Covariance` instance. The provided collection may contain duplicates, but an
            exception will be thrown if any of the parameter descriptors is not associated with this covariance. This method can be
            used to extract any submatrix and/or to perform a symmetric reordering of the rows/columns of the covariance matrix.
        
            **Important:**
        
        
            Since a parameter descriptor cannot be associated with multiple rows/columns of the covariance matrix, the provided
            collection must not contain any duplicate (an exception will be thrown if that occurs).
        
            Parameters:
                selectedParameterDescriptors (`Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`> selectedParameterDescriptors): the parameter descriptors associated with the rows/columns to be extracted
        
            Returns:
                the part of the covariance associated with the specified parameter descriptors
        
            Raises:
                : if one of the provided parameter descriptors is not associated with this covariance matrix, or if the provided
                    collection contains any duplicate
        
        
        """
        ...
    @typing.overload
    def getSubCovariance(self, collection: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor], typing.Sequence[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor], typing.Set[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor]]) -> 'Covariance': ...
    @typing.overload
    def getVariance(self, parameterDescriptor: fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor) -> float:
        """
            Gets the variance σ :sub:`i`  = C :sub:`i,i` for the specified row/column index.
        
            Parameters:
                index (int): the row/column index
        
            Returns:
                the variance for the specified row/column index
        
            Raises:
                : if the provided index is not valid
        
            Gets the variance σ :sub:`i`  = C :sub:`i,i` associated with the specified parameter descriptor.
        
            Parameters:
                parameterDescriptor (:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`): the parameter descriptor
        
            Returns:
                the variance for the specified parameter descriptor
        
            Raises:
                : if the provided collection is :code:`null` or if the parameter descriptor is not associated with this covariance matrix
        
        
        """
        ...
    @typing.overload
    def getVariance(self, int: int) -> float: ...
    def getVarianceMatrix(self) -> fr.cnes.sirius.patrius.math.linear.DiagonalMatrix:
        """
            Gets the variance matrix.
        
            The variance matrix is a diagonal matrix which contains the diagonal elements of the covariance matrix.
        
            Returns:
                the variance matrix
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def positiveScalarMultiply(self, double: float) -> 'Covariance':
        """
            Multiplies this covariance matrix by a positive scalar.
        
            Parameters:
                d (double): the scalar by which the matrix is multiplied (≥0)
        
            Returns:
                this covariance matrix multiplied by the provided scalar
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NotPositiveException`: if the provided scalar is negative
        
        
        """
        ...
    @typing.overload
    def quadraticMultiplication(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> 'Covariance':
        """
            Gets the result of the quadratic multiplication M×C×M :sup:`T` , where C is this covariance matrix and M is the
            provided matrix, and associates the computed matrix with default parameter descriptors.
        
            Parameters:
                m (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): the matrix M
        
            Returns:
                M×C×M :sup:`T`
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the matrix M is @:code:`null`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if this matrix and the matrices M and M :sup:`T` are not multiplication compatible
        
            Gets the result of the quadratic multiplication M×C×M :sup:`T` , where C is this covariance matrix and M or M :sup:`T`
            is the provided matrix, and associates the computed matrix with default parameter descriptors.
        
            Parameters:
                m (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): the matrix M
                isTranspose (boolean): if :code:`true`, assume the matrix provided is M :sup:`T` , otherwise assume it is M
        
            Returns:
                M×C×M :sup:`T`
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the matrix M is @:code:`null`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if this matrix and the matrices M and M :sup:`T` are not multiplication compatible
        
        public :class:`~fr.cnes.sirius.patrius.covariance.Covariance` quadraticMultiplication(:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix` m, `Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`> newParameterDescriptors)
        
            Gets the result of the quadratic multiplication M×C×M :sup:`T` , where C is this covariance matrix and M is the
            provided matrix, and associates the computed matrix with the specified parameter descriptors.
        
            Parameters:
                m (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): the matrix M
                newParameterDescriptors (`Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`> newParameterDescriptors): the parameter descriptors to be associated with the computed covariance matrix
        
            Returns:
                M×C×M :sup:`T`
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the matrix M is @:code:`null`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if this matrix and the matrices M and M :sup:`T` are not multiplication compatible
                : if the number of parameter descriptors does not match the size of the covariance matrix, or if the collection of
                    parameter descriptors contains any duplicate
        
        public :class:`~fr.cnes.sirius.patrius.covariance.Covariance` quadraticMultiplication(:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix` m, `Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`> newParameterDescriptors, boolean isTranspose)
        
            Gets the result of the quadratic multiplication M×C×M :sup:`T` , where C is this covariance matrix and M or M :sup:`T`
            is the provided matrix, and associates the computed matrix with the specified parameter descriptors.
        
            Parameters:
                m (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): the matrix M
                newParameterDescriptors (`Collection <http://docs.oracle.com/javase/8/docs/api/java/util/Collection.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor`> newParameterDescriptors): the parameter descriptors to be associated with the computed covariance matrix
                isTranspose (boolean): if :code:`true`, assume the matrix provided is M :sup:`T` , otherwise assume it is M
        
            Returns:
                M×C×M :sup:`T`
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the matrix M is @:code:`null`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if this matrix and the matrix M or M :sup:`T` is not multiplication compatible
                : if the provided matrix M is :code:`null`, if the number of parameter descriptors does not match the size of the
                    covariance matrix, or if the collection of parameter descriptors contains any duplicate
        
        
        """
        ...
    @typing.overload
    def quadraticMultiplication(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, boolean: bool) -> 'Covariance': ...
    @typing.overload
    def quadraticMultiplication(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, collection: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor], typing.Sequence[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor], typing.Set[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor]]) -> 'Covariance': ...
    @typing.overload
    def quadraticMultiplication(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, collection: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor], typing.Sequence[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor], typing.Set[fr.cnes.sirius.patrius.math.parameter.ParameterDescriptor]], boolean: bool) -> 'Covariance': ...
    @typing.overload
    def toString(self) -> str:
        """
            Returns a string representation of this instance which includes the name of the class and the names of the associated
            parameter descriptors (the covariance matrix itself is not printed).
        
            Overrides:
                 in class 
        
            Returns:
                string representation of this instance
        
        """
        ...
    @typing.overload
    def toString(self, realMatrixFormat: fr.cnes.sirius.patrius.math.linear.RealMatrixFormat) -> str:
        """
            Returns a string representation of this instance which includes the name of the class (if requested), the names of the
            associated parameter descriptors and the the covariance matrix (if the specified matrix format is not :code:`null`).
        
            Parameters:
                realMatrixFormat (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrixFormat`): the format to use when printing the covariance matrix
        
            Returns:
                string representation of this instance
        
        """
        ...
    @typing.overload
    def toString(self, realMatrixFormat: fr.cnes.sirius.patrius.math.linear.RealMatrixFormat, string: str, string2: str, boolean: bool, boolean2: bool) -> str:
        """
            Returns a string representation of this instance which includes the name of the class (if requested), the names of the
            associated parameter descriptors and the the covariance matrix (if the specified matrix format is not :code:`null`).
        
            Parameters:
                realMatrixFormat (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrixFormat`): the format to use when printing the covariance matrix
                nameSeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to use as a separator between the names of the parameter descriptors
                fieldSeparator (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the string to use as a separator between the field values of a parameter descriptor
                printClassName (boolean): whether or not the name of this class should be printed
                reverseOrder (boolean): whether or not the field values of each parameter descriptor should be printed in reverse order
        
            Returns:
                string representation of this instance
        
        
        """
        ...

class MultiOrbitalCovarianceProvider(java.io.Serializable):
    """
    public interface MultiOrbitalCovarianceProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for :class:`~fr.cnes.sirius.patrius.covariance.MultiOrbitalCovariance` providers.
    
        This interface can be used by any class used for multi orbital covariance computation.
    """
    def getMultiOrbitalCovariance(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'MultiOrbitalCovariance': ...
    def getOrbitalCovarianceProvider(self, int: int) -> 'OrbitalCovarianceProvider':
        """
            Getter for an orbital covariance provider extracting information from this multi orbital covariance.
        
            Parameters:
                index (int): The index of the spacecraft to be extracted
        
            Returns:
                the orbital covariance provider of the required spacecraft
        
        
        """
        ...

class OrbitalCovarianceProvider(fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider):
    """
    public interface OrbitalCovarianceProvider extends :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider`
    
        Interface for :class:`~fr.cnes.sirius.patrius.covariance.OrbitalCovariance` providers.
    
        This interface can be used by any class used for orbital covariance computation
    
        Since:
            4.13
    """
    def getOrbitalCovariance(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'OrbitalCovariance': ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...

class BasicMultiOrbitalCovarianceProvider(MultiOrbitalCovarianceProvider):
    """
    public class BasicMultiOrbitalCovarianceProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.covariance.MultiOrbitalCovarianceProvider`
    
        This class implements :class:`~fr.cnes.sirius.patrius.covariance.MultiOrbitalCovarianceProvider` by transforming an
        initial covariance with the partial derivatives of a spacecraft state providers.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, covariance: Covariance, map: typing.Union[java.util.Map[fr.cnes.sirius.patrius.propagation.SpacecraftStateProvider, fr.cnes.sirius.patrius.propagation.numerical.JacobiansMapper], typing.Mapping[fr.cnes.sirius.patrius.propagation.SpacecraftStateProvider, fr.cnes.sirius.patrius.propagation.numerical.JacobiansMapper]]): ...
    def getMultiOrbitalCovariance(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'MultiOrbitalCovariance': ...
    def getOrbitalCovarianceProvider(self, int: int) -> OrbitalCovarianceProvider:
        """
            Getter for an orbital covariance provider extracting information from this multi orbital covariance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.covariance.MultiOrbitalCovarianceProvider.getOrbitalCovarianceProvider` in
                interface :class:`~fr.cnes.sirius.patrius.covariance.MultiOrbitalCovarianceProvider`
        
            Parameters:
                index (int): The index of the spacecraft to be extracted
        
            Returns:
                the orbital covariance provider of the required spacecraft
        
        
        """
        ...

class BasicOrbitalCovarianceProvider(OrbitalCovarianceProvider):
    """
    public class BasicOrbitalCovarianceProvider extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.covariance.OrbitalCovarianceProvider`
    
        This class implements OrbitalCovarianceProvider by transforming an initial covariance with the partial derivatives of a
        spacecraft state provider.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, covariance: Covariance, spacecraftStateProvider: fr.cnes.sirius.patrius.propagation.SpacecraftStateProvider, jacobiansMapper: fr.cnes.sirius.patrius.propagation.numerical.JacobiansMapper): ...
    def getNativeFrame(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.frames.Frame: ...
    def getOrbitalCovariance(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> 'OrbitalCovariance': ...

class MultiOrbitalCovariance(AbstractOrbitalCovariance['MultiOrbitalCovariance']):
    @typing.overload
    def __init__(self, covariance: Covariance, collection: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.orbits.Orbit], typing.Sequence[fr.cnes.sirius.patrius.orbits.Orbit], typing.Set[fr.cnes.sirius.patrius.orbits.Orbit]], intArray: typing.Union[typing.List[int], jpype.JArray], frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle): ...
    @typing.overload
    def __init__(self, symmetricPositiveMatrix: fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix, collection: typing.Union[java.util.Collection[fr.cnes.sirius.patrius.orbits.Orbit], typing.Sequence[fr.cnes.sirius.patrius.orbits.Orbit], typing.Set[fr.cnes.sirius.patrius.orbits.Orbit]], intArray: typing.Union[typing.List[int], jpype.JArray], frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle): ...
    def copy(self) -> 'MultiOrbitalCovariance': ...
    def equals(self, object: typing.Any) -> bool: ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate: ...
    def getOrbit(self, int: int) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    @typing.overload
    def getOrbitalCovariance(self, int: int) -> 'OrbitalCovariance': ...
    @typing.overload
    def getOrbitalCovariance(self, int: int, boolean: bool) -> 'OrbitalCovariance': ...
    def getOrbits(self) -> java.util.List[fr.cnes.sirius.patrius.orbits.Orbit]: ...
    def getRelativeCovariance(self, int: int, int2: int) -> Covariance: ...
    def getRelativeCovarianceMatrix(self, int: int, int2: int) -> fr.cnes.sirius.patrius.math.linear.ArrayRowSymmetricPositiveMatrix: ...
    def hashCode(self) -> int: ...
    def shiftedBy(self, double: float) -> 'MultiOrbitalCovariance': ...
    @typing.overload
    def transformTo(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, lOFType: fr.cnes.sirius.patrius.frames.LOFType, boolean: bool) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> 'MultiOrbitalCovariance': ...
    @typing.overload
    def transformTo(self, int: int, lOFType: fr.cnes.sirius.patrius.frames.LOFType, boolean: bool) -> 'MultiOrbitalCovariance': ...

class OrbitalCovariance(AbstractOrbitalCovariance['OrbitalCovariance']):
    """
    public class OrbitalCovariance extends :class:`~fr.cnes.sirius.patrius.covariance.AbstractOrbitalCovariance`<:class:`~fr.cnes.sirius.patrius.covariance.OrbitalCovariance`>
    
        Orbital covariance associated with a single orbit.
    
        This class associates a :class:`~fr.cnes.sirius.patrius.covariance.Covariance` instance with a given orbit, its date
        being the date of definition of the orbital covariance. The frame, orbit type (Cartesian, Keplerian, etc) and position
        angle type (mean, true, eccentric) in which it is expressed can also be specified at construction if they are not the
        frame, orbit type and position angle type of the associated orbit.
    
        The covariance matrix must be at least six by six, where the first six rows/columns represent the uncertainty on the
        orbital parameters and the remaining ones represent the uncertainty on the additional parameters. The parameter
        descriptors of these first six rows/columns must be associated to an
        :meth:`~fr.cnes.sirius.patrius.math.parameter.StandardFieldDescriptors.ORBITAL_COORDINATE`, and this descriptor must be
        mapped to a valid :class:`~fr.cnes.sirius.patrius.orbits.orbitalparameters.OrbitalCoordinate` (one with the expected
        orbit type and state vector index).
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, covariance: Covariance, orbit: fr.cnes.sirius.patrius.orbits.Orbit): ...
    @typing.overload
    def __init__(self, covariance: Covariance, orbit: fr.cnes.sirius.patrius.orbits.Orbit, frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle): ...
    @typing.overload
    def __init__(self, covariance: Covariance, orbit: fr.cnes.sirius.patrius.orbits.Orbit, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle): ...
    @typing.overload
    def __init__(self, symmetricPositiveMatrix: fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix, orbit: fr.cnes.sirius.patrius.orbits.Orbit): ...
    @typing.overload
    def __init__(self, symmetricPositiveMatrix: fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix, orbit: fr.cnes.sirius.patrius.orbits.Orbit, frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle): ...
    @typing.overload
    def __init__(self, symmetricPositiveMatrix: fr.cnes.sirius.patrius.math.linear.SymmetricPositiveMatrix, orbit: fr.cnes.sirius.patrius.orbits.Orbit, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle): ...
    def copy(self) -> 'OrbitalCovariance':
        """
            Gets a copy of this orbital covariance.
        
            This method performs a shallow copy of the associated covariance (shallow copy of the parameter descriptors list, deep
            copy of the covariance matrix). The orbit, frame, orbit type and position angle type are all passed by reference since
            they are immutable.
        
            Returns:
                a copy of this orbital covariance
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.covariance.Covariance.copy`
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.covariance.AbstractOrbitalCovariance.equals` in
                class :class:`~fr.cnes.sirius.patrius.covariance.AbstractOrbitalCovariance`
        
        
        """
        ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date.
        
            Returns:
                date attached to the object
        
        
        """
        ...
    def getOrbit(self) -> fr.cnes.sirius.patrius.orbits.Orbit:
        """
            Gets the orbit associated with the covariance.
        
            Returns:
                the orbit associated with the covariance
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.covariance.AbstractOrbitalCovariance.hashCode` in
                class :class:`~fr.cnes.sirius.patrius.covariance.AbstractOrbitalCovariance`
        
        
        """
        ...
    def shiftedBy(self, double: float) -> 'OrbitalCovariance': ...
    @typing.overload
    def transformTo(self, frame: fr.cnes.sirius.patrius.frames.Frame) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, lOFType: fr.cnes.sirius.patrius.frames.LOFType, boolean: bool) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> AbstractOrbitalCovariance: ...
    @typing.overload
    def transformTo(self, frame: fr.cnes.sirius.patrius.frames.Frame, orbitType: fr.cnes.sirius.patrius.orbits.OrbitType, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle) -> 'OrbitalCovariance': ...
    @typing.overload
    def transformTo(self, lOFType: fr.cnes.sirius.patrius.frames.LOFType, boolean: bool) -> 'OrbitalCovariance': ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.covariance")``.

    AbstractOrbitalCovariance: typing.Type[AbstractOrbitalCovariance]
    BasicMultiOrbitalCovarianceProvider: typing.Type[BasicMultiOrbitalCovarianceProvider]
    BasicOrbitalCovarianceProvider: typing.Type[BasicOrbitalCovarianceProvider]
    Covariance: typing.Type[Covariance]
    MultiOrbitalCovariance: typing.Type[MultiOrbitalCovariance]
    MultiOrbitalCovarianceProvider: typing.Type[MultiOrbitalCovarianceProvider]
    OrbitalCovariance: typing.Type[OrbitalCovariance]
    OrbitalCovarianceProvider: typing.Type[OrbitalCovarianceProvider]
