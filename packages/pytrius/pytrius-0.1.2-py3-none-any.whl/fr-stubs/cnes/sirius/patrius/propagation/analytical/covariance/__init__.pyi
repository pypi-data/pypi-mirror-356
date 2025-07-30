
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.time
import jpype
import typing



class CovarianceInterpolation:
    """
    public class CovarianceInterpolation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class allows the interpolation of a covariance matrix at a date t in [t :sub:`1` , t :sub:`2` ] using the
        surrounding covariances matrices Cov :sub:`t1` Cov :sub:`t2` . The interpolated covariance matrix is computed using a
        polynomial approximation of the transition matrix.
    
        Since:
            2.3
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], int: int, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double3: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, realMatrix2: fr.cnes.sirius.patrius.math.linear.RealMatrix, int: int, orbit: fr.cnes.sirius.patrius.orbits.Orbit, double: float): ...
    @staticmethod
    def createDiagonalArray(int: int, double: float) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Creates a diagonal square matrix of dimension dim equals to coef * identity (dim)
        
            Parameters:
                dim (int): : dimension of the square matrix
                coef (double): : value of all the diagonal coefficients of the matrix
        
            Returns:
                matrix : a Array2DRowRealMatrix square diagonal matrix proportional to identity
        
        
        """
        ...
    @staticmethod
    def createDiagonalMatrix(int: int, double: float) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Creates a diagonal square matrix of dimension dim equals to coef * identity (dim)
        
            Parameters:
                dim (int): : dimension of the square matrix
                coef (double): : value of all the diagonal coefficients of the matrix
        
            Returns:
                matrix : a Array2DRowRealMatrix square diagonal matrix proportional to identity
        
        
        """
        ...
    def getFirstCovarianceMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
        
            Returns:
                the first covariance matrix covarianceMatrix1
        
        
        """
        ...
    def getMu(self) -> float:
        """
        
            Returns:
                the standard gravitational parameter
        
        
        """
        ...
    def getOrbit(self) -> fr.cnes.sirius.patrius.orbits.Orbit:
        """
        
            Returns:
                the orbit
        
        
        """
        ...
    def getPolynomialOrder(self) -> int:
        """
        
            Returns:
                the polynomial order
        
        
        """
        ...
    def getSecondCovarianceMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
        
            Returns:
                the second covariance matrix covarianceMatrix1
        
        
        """
        ...
    def getT1(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
        
            Returns:
                beginning interpolation date t1
        
        
        """
        ...
    def getT2(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
        
            Returns:
                ending interpolation date t2
        
        
        """
        ...
    def interpolate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def interpolateArray(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def setFirstCovarianceMatrix(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Allows to change the CovarianceMatrix standing for the lower bound of the interpolation interval, associated with t1. If
            do so, the computation of the approximated transition matrix A has to be done again, since A is considered constant on
            [t1,t2] if multiple calls to method interpolate(AbsoluteDate) are made.
        
            Parameters:
                covMatrix (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): the new covariance matrix covarianceMatrix1
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): : setting date for the new covariance matrix
        
        
        """
        ...
    def setMu(self, double: float) -> None:
        """
            Allows to change the value of the gravitational parameter. If do so, the computation of the approximated transition
            matrix A has to be done again, since A depends on mu.
        
            Parameters:
                newMu (double): the mu value to set
        
        
        """
        ...
    def setOrbit(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> None:
        """
            Allows to change the orbit. If do so, the computation of the approximated transition matrix A has to be done again,
            since A depends on the PV coordinates extracted from orbit.
        
            Parameters:
                newOrbit (:class:`~fr.cnes.sirius.patrius.orbits.Orbit`): the orbit to set
        
        
        """
        ...
    def setPolynomialOrder(self, int: int) -> None:
        """
        
            Parameters:
                order (int): the polynomial order to set
        
        
        """
        ...
    def setSecondCovarianceMatrix(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Allows to change the CovarianceMatrix standing for the upper bound of the interpolation interval, associated with t2. If
            do so, the computation of the approximated transition matrix A has to be done again, since A is considered constant on
            [t1,t2] if multiple calls to method interpolate(AbsoluteDate) are made.
        
            Parameters:
                covMatrix (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): the new covariance matrix covarianceMatrix2
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): : setting date for the new covariance matrix
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation.analytical.covariance")``.

    CovarianceInterpolation: typing.Type[CovarianceInterpolation]
