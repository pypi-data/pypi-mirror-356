
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.stela.bodies
import fr.cnes.sirius.patrius.stela.forces
import fr.cnes.sirius.patrius.stela.orbits
import fr.cnes.sirius.patrius.stela.propagation
import fr.cnes.sirius.patrius.stela.spaceobject
import jpype
import typing



class JavaMathAdapter:
    """
    public final class JavaMathAdapter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Math adapter class.
    
        Since:
            1.3
    """
    @staticmethod
    def binomialCoefficientGeneric(int: int, int2: int) -> float:
        """
            Compute the Binomial Coefficient, "a choose b", the number of b-element subsets that can be selected from an a-element
            set. This formula can be used with negative a values.
        
            Parameters:
                a (int): the size of the set
                b (int): the size of the subsets
        
            Returns:
                a choose b
        
        
        """
        ...
    @staticmethod
    def matrixAdd(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @staticmethod
    def matrixMultiply(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Multiply 2 matrix.
        
            Parameters:
                m1 (double[][]): first Matrix
                m2 (double[][]): second matrix
        
            Returns:
                the products
        
        
        """
        ...
    @staticmethod
    def matrixToVector(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], int: int) -> None:
        """
            Copy a matrix into a vector, column per column.
        
            Parameters:
                matrix (double[][]): matrix from which the data is read
                vector (double[]): vector in which the data is put
                offset (int): offset after which the data will be put in the vector thrown if dimensions mismatch
        
        
        """
        ...
    @staticmethod
    def matrixTranspose(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Transpose a matrix.
        
            Parameters:
                m (double[][]): the matrix.
        
            Returns:
                Matrix transposed.
        
        
        """
        ...
    @staticmethod
    def matrixVectorMultiply(doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Multiply matrix with a vector.
        
            Parameters:
                m (double[][]): the matrix
                v (double[]): the vector
        
            Returns:
                Products with matrix and vector
        
        
        """
        ...
    @staticmethod
    def mod(double: float, double2: float) -> float:
        """
            Computes "x" modulo "mod".
        
            Parameters:
                x (double): value to modulate
                mod (double): modulo (for instance π)
        
            Returns:
                "x" modulo "mod"
        
        
        """
        ...
    @staticmethod
    def negate(doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Invert a vector.
        
            Parameters:
                v (double[]): vector
        
            Returns:
                -v
        
        
        """
        ...
    @staticmethod
    def roundAngleInRadians(double: float) -> float:
        """
            Round angle in radians [ 0; 2*PI [.
        
            Parameters:
                angle (double): the angle to round
        
            Returns:
                the rounded angle
        
        
        """
        ...
    @staticmethod
    def scalarMultiply(double: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Return coef * matrix.
        
            Parameters:
                coef (double): a coefficent
                matrix (double[][]): a matrix
        
            Returns:
                a matrix resulting from the operation coef * matrix.
        
        
        """
        ...
    @staticmethod
    def threeDMatrixVectorMultiply(doubleArray: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    @staticmethod
    def vectorToMatrix(doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None:
        """
            Copy a vector into a matrix, column per column.
        
            Parameters:
                vector (double[]): vector to be copied
                matrix (double[][]): matrix where to put the data
        
        
        """
        ...

class PerigeeAltitudeDetector(fr.cnes.sirius.patrius.events.AbstractDetector):
    """
    public class PerigeeAltitudeDetector extends :class:`~fr.cnes.sirius.patrius.events.AbstractDetector`
    
        Finder for satellite altitude crossing events in Semi-analytical theory.
    
        This class finds altitude events (i.e. satellite crossing a predefined altitude level above ground). The altitude
        computed here is the one of the osculating perigee
    
        The default implementation behavior is to :meth:`~fr.cnes.sirius.patrius.events.EventDetector.Action.CONTINUE`
        propagation when ascending and to :meth:`~fr.cnes.sirius.patrius.events.EventDetector.Action.STOP` propagation when
        descending. This can be changed by overriding the
        :meth:`~fr.cnes.sirius.patrius.stela.PerigeeAltitudeDetector.eventOccurred` method in a derived class.
    
        Since:
            1.3
    
        Also see:
            :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.addEventDetector`,
            :class:`~fr.cnes.sirius.patrius.events.detectors.AltitudeDetector`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, action: fr.cnes.sirius.patrius.events.EventDetector.Action, action2: fr.cnes.sirius.patrius.events.EventDetector.Action): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, action: fr.cnes.sirius.patrius.events.EventDetector.Action, action2: fr.cnes.sirius.patrius.events.EventDetector.Action, boolean: bool, boolean2: bool): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter, action: fr.cnes.sirius.patrius.events.EventDetector.Action, action2: fr.cnes.sirius.patrius.events.EventDetector.Action): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, orbitNatureConverter: fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter, action: fr.cnes.sirius.patrius.events.EventDetector.Action, action2: fr.cnes.sirius.patrius.events.EventDetector.Action, boolean: bool, boolean2: bool): ...
    def copy(self) -> fr.cnes.sirius.patrius.events.EventDetector:
        """
            A copy of the detector. By default copy is deep. If not, detector javadoc will specify which attribute is not fully
            copied. In that case, the attribute reference is passed.
        
            The following attributes are not deeply copied:
        
              - orbitConverter: :class:`~fr.cnes.sirius.patrius.stela.orbits.OrbitNatureConverter`
        
        
            Returns:
                a copy of the detector.
        
        
        """
        ...
    def eventOccurred(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool, boolean2: bool) -> fr.cnes.sirius.patrius.events.EventDetector.Action: ...
    def g(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    def getAltitude(self) -> float:
        """
            Get the threshold altitude value.
        
            Returns:
                the threshold altitude value (m)
        
        
        """
        ...
    def getEarthRadius(self) -> float:
        """
            Get the earth radius.
        
            Returns:
                the body shape
        
        
        """
        ...

class StelaSpacecraftFactory:
    """
    public final class StelaSpacecraftFactory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Utility class to build Stela spacecrafts
    
        Since:
            1.3
    """
    @staticmethod
    def createStelaCompatibleSpacecraft(string: str, double: float, double2: float, double3: float, double4: float, double5: float) -> fr.cnes.sirius.patrius.assembly.Assembly: ...
    @staticmethod
    def createStelaRadiativeSpacecraft(string: str, double: float, double2: float, double3: float) -> fr.cnes.sirius.patrius.assembly.Assembly: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.stela")``.

    JavaMathAdapter: typing.Type[JavaMathAdapter]
    PerigeeAltitudeDetector: typing.Type[PerigeeAltitudeDetector]
    StelaSpacecraftFactory: typing.Type[StelaSpacecraftFactory]
    bodies: fr.cnes.sirius.patrius.stela.bodies.__module_protocol__
    forces: fr.cnes.sirius.patrius.stela.forces.__module_protocol__
    orbits: fr.cnes.sirius.patrius.stela.orbits.__module_protocol__
    propagation: fr.cnes.sirius.patrius.stela.propagation.__module_protocol__
    spaceobject: fr.cnes.sirius.patrius.stela.spaceobject.__module_protocol__
