
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.linear
import jpype
import typing



class ArrayUtils:
    @typing.overload
    @staticmethod
    def add(intArray: typing.Union[typing.List[int], jpype.JArray], int2: int) -> typing.MutableSequence[int]: ...
    @typing.overload
    @staticmethod
    def add(intArray: typing.Union[typing.List[int], jpype.JArray], int2: int, int3: int) -> typing.MutableSequence[int]: ...
    @staticmethod
    def contains(intArray: typing.Union[typing.List[int], jpype.JArray], int2: int) -> bool: ...
    @staticmethod
    def getArrayIndex(intArray: typing.Union[typing.List[int], jpype.JArray], int2: int) -> int: ...
    @staticmethod
    def getArrayMinIndex(intArray: typing.Union[typing.List[int], jpype.JArray]) -> int: ...
    @staticmethod
    def insert(int: int, intArray: typing.Union[typing.List[int], jpype.JArray], *int3: int) -> typing.MutableSequence[int]: ...
    @staticmethod
    def remove(object: typing.Any, int: int) -> typing.Any: ...
    @staticmethod
    def removeElements(intArray: typing.Union[typing.List[int], jpype.JArray], *int2: int) -> typing.MutableSequence[int]: ...

class Utils:
    """
    public final class Utils extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Utility class.
    
        Since:
            4.6
    """
    @typing.overload
    @staticmethod
    def calculateScaledResidual(realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realMatrix2: fr.cnes.sirius.patrius.math.linear.RealMatrix, realMatrix3: fr.cnes.sirius.patrius.math.linear.RealMatrix) -> float:
        """
            Calculate the scaled residual
        
        
            ||Ax-b||_oo/( ||A||_oo . ||x||_oo + ||b||_oo ), with
        
        
            ||x||_oo = max(||x[i]||)
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): A matrix
                x (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): X matrix
                b (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): B matrix
        
            Returns:
                scaled residual
        
            Calculate the scaled residual
        
        
            ||Ax-b||_oo/( ||A||_oo . ||x||_oo + ||b||_oo ), with
        
        
            ||x||_oo = max(||x[i]||)
        
            Parameters:
                a (:class:`~fr.cnes.sirius.patrius.math.linear.RealMatrix`): A matrix
                x (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): X matrix
                b (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): B matrix
        
            Returns:
                scaled residual
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def calculateScaledResidual(realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realVector2: fr.cnes.sirius.patrius.math.linear.RealVector) -> float: ...
    @staticmethod
    def getDoubleMachineEpsilon() -> float:
        """
            The smallest positive (epsilon) such that 1.0 + epsilon != 1.0.
        
            Returns:
                smallest positive (epsilon) such that 1.0 + epsilon != 1.0 See
                http://en.wikipedia.org/wiki/Machine_epsilon#Approximation_using_Java
        
        
        """
        ...
    @staticmethod
    def max(double: float, double2: float) -> float:
        """
            Returns max(a, b) or NaN if one value is a NaN.
        
            Parameters:
                a (double): a
                b (double): b
        
            Returns:
                max(a, b) or NaN if one value is a NaN
        
        
        """
        ...
    @staticmethod
    def min(double: float, double2: float) -> float:
        """
            Returns min(a, b) or NaN if one value is a NaN.
        
            Parameters:
                a (double): a
                b (double): b
        
            Returns:
                min(a, b) or NaN if one value is a NaN
        
        
        """
        ...
    @staticmethod
    def randomValuesMatrix(int: int, int2: int, double: float, double2: float, long: int) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns matrix filled with random values.
        
            Parameters:
                rows (int): number of rows
                cols (int): number of columns
                min (double): min
                max (double): max
                seed (`Long <http://docs.oracle.com/javase/8/docs/api/java/lang/Long.html?is-external=true>`): seed
        
            Returns:
                matrix filled with random values
        
        
        """
        ...
    @staticmethod
    def randomValuesPositiveMatrix(int: int, int2: int, double: float, double2: float, long: int) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns matrix filled with random positive values.
        
            Parameters:
                rows (int): number of rows
                cols (int): number of columns
                min (double): min
                max (double): max
                seed (`Long <http://docs.oracle.com/javase/8/docs/api/java/lang/Long.html?is-external=true>`): seed
        
            Returns:
                matrix filled with random positive values
        
            Also see:
                "http://mathworld.wolfram.com/PositiveDefiniteMatrix.html"
        
        
        """
        ...
    @staticmethod
    def replaceValues(doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, double3: float) -> typing.MutableSequence[float]:
        """
            Return a new array with all the occurrences of oldValue replaced by newValue.
        
            Parameters:
                v (double[]): array
                oldValue (double): old value
                newValue (double): new value
        
            Returns:
                updated array
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.joptimizer.util")``.

    ArrayUtils: typing.Type[ArrayUtils]
    Utils: typing.Type[Utils]
