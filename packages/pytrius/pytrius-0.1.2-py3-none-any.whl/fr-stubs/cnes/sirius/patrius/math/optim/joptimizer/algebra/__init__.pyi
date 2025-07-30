
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.linear
import jpype
import typing



class AlgebraUtils:
    """
    public final class AlgebraUtils extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Algebraic utility operations.
    
        Since:
            4.6
    """
    @typing.overload
    @staticmethod
    def add(realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realMatrix2: fr.cnes.sirius.patrius.math.linear.RealMatrix, double: float) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns C = A + beta * B (linear combination). Useful in avoiding the need of the copy() in the colt api.
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix
                b (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix
                beta (double): constant
        
            Returns:
                C
        
            Returns v = v1 + c * v2 (linear combination). Useful in avoiding the need of the copy() in the colt api.
        
            Parameters:
                v1 (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): vector
                v2 (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): vector
                c (double): constant
        
            Returns:
                v
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def add(realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realVector2: fr.cnes.sirius.patrius.math.linear.RealVector, double: float) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    @staticmethod
    def checkRectangularShape(realMatrixArray: typing.Union[typing.List[typing.MutableSequence[fr.cnes.sirius.patrius.math.linear.RealMatrix]], jpype.JArray]) -> None:
        """
            Checks whether the given array is rectangular, that is, whether all rows have the same number of columns.
        
            Parameters:
                array (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`[][]): array
        
            Raises:
                : if the array is not rectangular.
        
        
        """
        ...
    @staticmethod
    def composeMatrix(realMatrixArray: typing.Union[typing.List[typing.MutableSequence[fr.cnes.sirius.patrius.math.linear.RealMatrix]], jpype.JArray]) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Constructs a block matrix made from the given parts. All matrices of a given column within ``parts`` must have the same
            number of columns. All matrices of a given row within ``parts`` must have the same number of rows. Otherwise an
            ``IllegalArgumentException`` is thrown. Note that ``null``s within ``parts[row,col]`` are an exception to this rule:
            they are ignored. Cells are copied. From https://github.com/kzn/colt/blob/master/src/cern/colt/matrix/
            DoubleFactory2D.java Extracted 17/11/2020
        
            Parameters:
                parts (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`[][]): matrices
        
            Returns:
                build matrix.
        
        
        """
        ...
    @staticmethod
    def diagonal(realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Constructs a new diagonal matrix whose diagonal elements are the elements of ``vector``. Cells values are copied. The
            new matrix is not a view.
        
            Parameters:
                vector (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): with the diagonal values
        
            Returns:
                a new matrix.
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def diagonalMatrixMult(realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Matrix-vector multiplication with diagonal matrix.
        
            Parameters:
                diagonalM (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): diagonal matrix M, in the form of a vector of its diagonal elements
                vector (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): vector
        
            Returns:
                M.x
        
            Return diagonalU.A with diagonalU diagonal.
        
            Parameters:
                diagonalU (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): matrix U, in the form of a vector of its diagonal elements
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix A
        
            Returns:
                U.A
        
            Return A.diagonalU with diagonalU diagonal.
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix A
                diagonalU (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): matrix U, in the form of a vector of its diagonal elements
        
            Returns:
                U.A
        
            Return diagonalU.A.diagonalV with diagonalU and diagonalV diagonal.
        
            Parameters:
                diagonalU (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): diagonal matrix U, in the form of a vector of its diagonal elements
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix A
                diagonalV (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): diagonal matrix V, in the form of a vector of its diagonal elements
        
            Returns:
                U.A.V
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def diagonalMatrixMult(realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    @typing.overload
    @staticmethod
    def diagonalMatrixMult(realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realVector2: fr.cnes.sirius.patrius.math.linear.RealVector) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    @typing.overload
    @staticmethod
    def diagonalMatrixMult(realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realVector2: fr.cnes.sirius.patrius.math.linear.RealVector) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...
    @staticmethod
    def fillSubdiagonalSymmetricMatrix(realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Given a symm matrix S that stores just its subdiagonal elements, reconstructs the full symmetric matrix.
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix
        
            Returns:
                full symmetric matrix
        
        
        """
        ...
    @staticmethod
    def getConditionNumberRange(realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, int: int) -> typing.MutableSequence[float]:
        """
            Returns a lower and an upper bound for the condition number
        
        
            kp(A) = Norm[A, p] / Norm[A^-1, p]
        
        
            where
        
        
            Norm[A, p] = sup ( Norm[A.x, p]/Norm[x, p] , x !=0 )
        
        
            for a matrix and
        
        
            Norm[x, 1] := Sum[MathLib.abs(x[i]), i]
        
        
            Norm[x, 2] := MathLib.sqrt(Sum[MathLib.pow(x[i], 2), i])
        
        
            Norm[x, 00] := Max[MathLib.abs(x[i]), i]
        
        
            for a vector.
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix you want the condition number of
                p (int): norm order (2 or Integer.MAX_VALUE)
        
            Returns:
                an array with the two bounds (lower and upper bound) See Ravindra S. Gajulapalli, Leon S. Lasdon "Scaling Sparse
                Matrices for Optimization Algorithms"
        
        
        """
        ...
    @staticmethod
    def randomValuesVector(int: int, double: float, double2: float, long: int) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Return a vector with random values
        
            Parameters:
                dim (int): dimension of the vector
                min (double): minimum value
                max (double): maximum value
                seed (`Long <http://docs.oracle.com/javase/8/docs/api/java/lang/Long.html?is-external=true>`): of the random number generator
        
            Returns:
                vector with random values
        
        
        """
        ...
    @staticmethod
    def replaceValues(realVector: fr.cnes.sirius.patrius.math.linear.RealVector, double: float, double2: float) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Return a new array with all the occurrences of oldValue replaced by newValue.
        
            Parameters:
                v (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): vector
                oldValue (double): value to be replaced
                newValue (double): value to replace with
        
            Returns:
                new array
        
        
        """
        ...
    @staticmethod
    def subdiagonalMultiply(realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realMatrix2: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Return the sub-diagonal result of the multiplication. If A is sparse, returns a sparse matrix (even if, generally
            speaking, the multiplication of two sparse matrices is not sparse) because the result is at least 50% (aside the
            diagonal elements) sparse.
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix
                b (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix
        
            Returns:
                sub-diagonal result of the multiplication
        
        
        """
        ...
    @staticmethod
    def zMult(realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realVector2: fr.cnes.sirius.patrius.math.linear.RealVector, double: float) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Returns v = A.a + beta*b. Useful in avoiding the need of the copy() in the colt api.
        
            Parameters:
                matA (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix A
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): vector
                b (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): vector
                beta (double): double
        
            Returns:
                v
        
        
        """
        ...
    @staticmethod
    def zMultTranspose(realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realVector2: fr.cnes.sirius.patrius.math.linear.RealVector, double: float) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Returns v = A[T].a + beta*b. Useful in avoiding the need of the copy() in the colt api.
        
            Parameters:
                matA (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix A
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): vector
                b (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): vector
                beta (double): constant
        
            Returns:
                v
        
        
        """
        ...

class CholeskyFactorization:
    """
    public final class CholeskyFactorization extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Cholesky L.L[T] factorization and inverse for symmetric and positive matrix: Q = L.L[T], L lower-triangular Just the
        subdiagonal elements of Q are used.
    
        The main difference with :class:`~fr.cnes.sirius.patrius.math.linear.CholeskyDecomposition` is that this implementation
        contains a rescaler :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.algebra.MatrixRescaler` in order to cope with
        badly conditioned matrices.
    
        Since:
            4.6
    """
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, matrixRescaler: 'MatrixRescaler'): ...
    @typing.overload
    def factorize(self) -> None: ...
    @typing.overload
    def factorize(self, boolean: bool) -> None: ...
    def getInverse(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Compute the inverse of the matrix.
        
            Returns:
                the inverse matrix Q
        
        
        """
        ...
    def getL(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the matrix L of the decomposition.
        
            L is an lower-triangular matrix
        
            Returns:
                the L matrix
        
        
        """
        ...
    def getLT(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the transpose of the matrix L of the decomposition.
        
            L :sup:`T` is an upper-triangular matrix
        
            Returns:
                the transpose of the matrix L of the decomposition
        
        
        """
        ...
    @typing.overload
    def solve(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Solver for system AX = b.
        
            Parameters:
                b (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): vector
        
            Returns:
                result X
        
            Solver for system AX = b.
        
            Parameters:
                b (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix
        
            Returns:
                result X
        
        
        """
        ...
    @typing.overload
    def solve(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> fr.cnes.sirius.patrius.math.linear.RealVector: ...

class MatrixRescaler:
    """
    public interface MatrixRescaler
    
        Interface for Matrix rescalers. Calculate the row and column scaling matrices R and T relative to a given matrix A
        (scaled A = R.A.T). They may be used, for instance, to scale the matrix prior to solving a corresponding set of linear
        equations.
    
        Since:
            4.6
    """
    def checkScaling(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realVector2: fr.cnes.sirius.patrius.math.linear.RealVector) -> bool:
        """
            Check if the scaling algorithm returned proper results.
        
            Parameters:
                aOriginal (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): the ORIGINAL (before scaling) matrix
                u (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): the return of the scaling algorithm
                v (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): the return of the scaling algorithm
        
            Returns:
                true/false
        
        
        """
        ...
    def getMatrixScalingFactors(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.linear.RealVector]:
        """
            Calculates the R and T scaling factors (matrices) for a generic matrix A so that A'(=scaled A) = R.A.T
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix A
        
            Returns:
                array with R,T
        
        
        """
        ...
    def getMatrixScalingFactorsSymm(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Calculates the R and T scaling factors (matrices) for a symmetric matrix A so that A'(=scaled A) = R.A.T
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix A
        
            Returns:
                array with R,T
        
        
        """
        ...

class Matrix1NornRescaler(MatrixRescaler):
    """
    public final class Matrix1NornRescaler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.algebra.MatrixRescaler`
    
        Calculates the matrix rescaling factors so that the 1-norm of each row and each column of the scaled matrix
        asymptotically converges to one.
    
        Since:
            4.6
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    def checkScaling(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realVector2: fr.cnes.sirius.patrius.math.linear.RealVector) -> bool:
        """
            Check if the scaling algorithm returned proper results. Note that AOriginal cannot be only subdiagonal filled, because
            this check is for both symm and bath notsymm matrices.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.optim.joptimizer.algebra.MatrixRescaler.checkScaling` in
                interface :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.algebra.MatrixRescaler`
        
            Parameters:
                aOriginal (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): the ORIGINAL (before scaling) matrix
                u (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): the return of the scaling algorithm
                v (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): the return of the scaling algorithm
        
            Returns:
                true if scaled
        
        
        """
        ...
    def getMatrixScalingFactors(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.linear.RealVector]:
        """
            Scaling factors for not singular matrices. See Daniel Ruiz, "A scaling algorithm to equilibrate both rows and columns
            norms in matrices" See Philip A. Knight, Daniel Ruiz, Bora Ucar "A Symmetry Preserving Algorithm for Matrix Scaling"
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.optim.joptimizer.algebra.MatrixRescaler.getMatrixScalingFactors` in
                interface :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.algebra.MatrixRescaler`
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix A
        
            Returns:
                array with R,T
        
        
        """
        ...
    def getMatrixScalingFactorsSymm(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Scaling factors for symmetric (not singular) matrices. Just the subdiagonal elements of the matrix are required. See
            Daniel Ruiz, "A scaling algorithm to equilibrate both rows and columns norms in matrices" See Philip A. Knight, Daniel
            Ruiz, Bora Ucar "A Symmetry Preserving Algorithm for Matrix Scaling"
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.optim.joptimizer.algebra.MatrixRescaler.getMatrixScalingFactorsSymm` in
                interface :class:`~fr.cnes.sirius.patrius.math.optim.joptimizer.algebra.MatrixRescaler`
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): matrix A
        
            Returns:
                array with R,T
        
        
        """
        ...
    @staticmethod
    def getRowInfinityNorm(realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, int: int) -> float:
        """
        
            Parameters:
                aSymm (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): symm matrix filled in its subdiagonal elements
                r (int): the index of the row
        
            Returns:
                infinity norm
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.joptimizer.algebra")``.

    AlgebraUtils: typing.Type[AlgebraUtils]
    CholeskyFactorization: typing.Type[CholeskyFactorization]
    Matrix1NornRescaler: typing.Type[Matrix1NornRescaler]
    MatrixRescaler: typing.Type[MatrixRescaler]
