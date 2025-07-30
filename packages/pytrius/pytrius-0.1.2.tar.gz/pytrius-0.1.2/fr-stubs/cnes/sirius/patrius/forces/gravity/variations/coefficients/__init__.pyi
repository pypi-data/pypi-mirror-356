
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import jpype
import typing



class VariableGravityFieldFactory:
    GRGSRL02_FILENAME: typing.ClassVar[str] = ...
    @staticmethod
    def addDefaultVariablePotentialCoefficientsReaders() -> None: ...
    @staticmethod
    def addVariablePotentialCoefficientsReader(variablePotentialCoefficientsReader: 'VariablePotentialCoefficientsReader') -> None: ...
    @staticmethod
    def clearVariablePotentialCoefficientsReaders() -> None: ...
    @staticmethod
    def getVariablePotentialProvider() -> 'VariablePotentialCoefficientsProvider': ...

class VariablePotentialCoefficientsProvider:
    """
    public interface VariablePotentialCoefficientsProvider
    
        Interface used to provide gravity field coefficients.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariableGravityFieldFactory`
    """
    def getAe(self) -> float:
        """
            Get the value of the central body reference radius.
        
            Returns:
                ae (m)
        
        
        """
        ...
    def getData(self) -> java.util.Map[int, java.util.Map[int, 'VariablePotentialCoefficientsSet']]: ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the reference date of the file
        
            Returns:
                reference date of gravity file
        
        
        """
        ...
    def getMaxDegree(self) -> int:
        """
            Get the max degree available
        
            Returns:
                max degree
        
        
        """
        ...
    def getMu(self) -> float:
        """
            Get the central body attraction coefficient.
        
            Returns:
                mu (m :sup:`3` /s :sup:`2` )
        
        
        """
        ...

class VariablePotentialCoefficientsSet(java.io.Serializable):
    """
    public class VariablePotentialCoefficientsSet extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Represents a variable potential coefficients set for a given degree and order.
    
        Since:
            1.3
    
        Also see:
            :code:`http://grgs.obs-mip.fr/grace/variable-models-grace-lageos/formats}`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, int: int, int2: int, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float, double10: float, double11: float, double12: float): ...
    @typing.overload
    def __init__(self, int: int, int2: int, double: float, double2: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    def computeCDriftComponent(self, double: float) -> float:
        """
            Compute the normalized drift component of the C coefficient
        
            Parameters:
                driftFunction (double): between two dates value
        
            Returns:
                double C drift component
        
        
        """
        ...
    def computeCPeriodicComponent(self, double: float, double2: float, double3: float, double4: float) -> float:
        """
            Compute the normalized periodic component of the C coefficient
        
            Parameters:
                sin2Pi (double): sinus(2*pi*time) component
                cos2Pi (double): cosinus(2*pi*time) component
                sin4Pi (double): sinus(4*pi*time) component
                cos4Pi (double): cosinus(4*pi*time) component
        
            Returns:
                double C periodic component
        
        
        """
        ...
    @staticmethod
    def computeDriftFunction(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Compute drift function to provide to :code:`#computeCDriftComponent` or :code:`#computeSDriftComponent`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): final date
                refDate (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): starting date
        
            Returns:
                double drift function
        
        
        """
        ...
    @staticmethod
    def computePeriodicFunctions(absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]:
        """
            Compute periodic functions to provide to :code:`#computeCPeriodicComponent` or :code:`#computeSPeriodicComponent`
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): choosen date
        
            Returns:
                double[] Values of sin2Pi, cos2Pi, sin4Pi, cos4Pi for the provided date
        
        
        """
        ...
    def computeSDriftComponent(self, double: float) -> float:
        """
            Compute the normalized drift component of the S coefficient
        
            Parameters:
                driftFunction (double): between two dates value
        
            Returns:
                double S drift component
        
        
        """
        ...
    def computeSPeriodicComponent(self, double: float, double2: float, double3: float, double4: float) -> float:
        """
            Compute the normalized periodic component of the S coefficient
        
            Parameters:
                sin2Pi (double): sinus(2*pi*time) component
                cos2Pi (double): cosinus(2*pi*time) component
                sin4Pi (double): sinus(4*pi*time) component
                cos4Pi (double): cosinus(4*pi*time) component
        
            Returns:
                double S periodic component
        
        
        """
        ...
    def getCoefC(self) -> float:
        """
            Getter for normalized coefC
        
            Returns:
                the coefC
        
        
        """
        ...
    def getCoefCCos1A(self) -> float:
        """
            Getter for normalized coefCCos1A
        
            Returns:
                the coefCCos1A
        
        
        """
        ...
    def getCoefCCos2A(self) -> float:
        """
            Getter for normalized coefCCos2A
        
            Returns:
                the coefCCos2A
        
        
        """
        ...
    def getCoefCDrift(self) -> float:
        """
            Getter for normalized coefCDrift
        
            Returns:
                the coefCDrift
        
        
        """
        ...
    def getCoefCSin1A(self) -> float:
        """
            Getter for normalized coefCSin1A
        
            Returns:
                the coefCSin1A
        
        
        """
        ...
    def getCoefCSin2A(self) -> float:
        """
            Getter for normalized coefCSin2A
        
            Returns:
                the coefCSin2A
        
        
        """
        ...
    def getCoefS(self) -> float:
        """
            Getter for normalized coefS
        
            Returns:
                the coefS
        
        
        """
        ...
    def getCoefSCos1A(self) -> float:
        """
            Getter for normalized coefSCos1A
        
            Returns:
                the coefSCos1A
        
        
        """
        ...
    def getCoefSCos2A(self) -> float:
        """
            Getter for normalized coefSCos2A
        
            Returns:
                the coefSCos2A
        
        
        """
        ...
    def getCoefSDrift(self) -> float:
        """
            Getter for normalized coefSDrift
        
            Returns:
                the coefSDrift
        
        
        """
        ...
    def getCoefSSin1A(self) -> float:
        """
            Getter for normalized coefSSin1A
        
            Returns:
                the coefSSin1A
        
        
        """
        ...
    def getCoefSSin2A(self) -> float:
        """
            Getter for normalized coefSSin2A
        
            Returns:
                the coefSSin2A
        
        
        """
        ...
    def getDegree(self) -> int:
        """
        
            Returns:
                the degree of the set
        
        
        """
        ...
    def getOrder(self) -> int:
        """
        
            Returns:
                the order of the set
        
        
        """
        ...
    @staticmethod
    def getPeriodicComputationMethod() -> 'VariablePotentialCoefficientsSet.PeriodicComputationMethod':
        """
            Getter for periodicComputationMethod
        
            Returns:
                the periodicComputationMethod
        
        
        """
        ...
    @staticmethod
    def setPeriodicComputationMethod(periodicComputationMethod: 'VariablePotentialCoefficientsSet.PeriodicComputationMethod') -> None:
        """
            Setter for periodicComputationMethod
        
            Parameters:
                periodicComputationMethod (:class:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsSet.PeriodicComputationMethod`): the periodicComputationMethod to set
        
        
        """
        ...
    class PeriodicComputationMethod(java.lang.Enum['VariablePotentialCoefficientsSet.PeriodicComputationMethod']):
        HOMOGENEOUS: typing.ClassVar['VariablePotentialCoefficientsSet.PeriodicComputationMethod'] = ...
        LEAP_YEAR: typing.ClassVar['VariablePotentialCoefficientsSet.PeriodicComputationMethod'] = ...
        def computeElapsedPeriodic(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
        def isLeapYear(self, int: int) -> bool: ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'VariablePotentialCoefficientsSet.PeriodicComputationMethod': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['VariablePotentialCoefficientsSet.PeriodicComputationMethod']: ...

class VariablePotentialCoefficientsReader(fr.cnes.sirius.patrius.data.DataLoader, VariablePotentialCoefficientsProvider):
    """
    public abstract class VariablePotentialCoefficientsReader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataLoader`, :class:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider`
    
        Abstract class representing a variable potential coefficients file reader. No actual "file reading" takes place in this
        class, as the loadData method is delegated to sub-classes, but this class handles all the data structures and answers
        the :class:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider`
        interface.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariableGravityFieldFactory`
    """
    def getAe(self) -> float:
        """
            Get the value of the central body reference radius.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider.getAe` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider`
        
            Returns:
                ae (m)
        
        
        """
        ...
    def getData(self) -> java.util.Map[int, java.util.Map[int, VariablePotentialCoefficientsSet]]: ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Description copied from
            interface: :meth:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider.getDate`
            Get the reference date of the file
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider.getDate` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider`
        
            Returns:
                the reference year of the file
        
        
        """
        ...
    def getMaxDegree(self) -> int:
        """
            Get the max degree available
        
            Specified by:
                
                meth:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider.getMaxDegree` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider`
        
            Returns:
                max degree
        
        
        """
        ...
    def getMu(self) -> float:
        """
            Get the central body attraction coefficient.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider.getMu` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsProvider`
        
            Returns:
                mu (m :sup:`3` /s :sup:`2` )
        
        
        """
        ...
    def getSupportedNames(self) -> str:
        """
            Get the regular expression for supported files names.
        
            Returns:
                regular expression for supported files names
        
        
        """
        ...
    def stillAcceptsData(self) -> bool:
        """
            Check if the loader still accepts new data.
        
            This method is used to speed up data loading by interrupting crawling the data sets as soon as a loader has found the
            data it was waiting for. For loaders that can merge data from any number of sources (for example JPL ephemerides or
            Earth Orientation Parameters that are split among several files), this method should always return true to make sure no
            data is left over.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.data.DataLoader.stillAcceptsData` in
                interface :class:`~fr.cnes.sirius.patrius.data.DataLoader`
        
            Returns:
                true while the loader still accepts new data
        
        
        """
        ...

class GRGSRL02FormatReader(VariablePotentialCoefficientsReader):
    """
    public class GRGSRL02FormatReader extends :class:`~fr.cnes.sirius.patrius.forces.gravity.variations.coefficients.VariablePotentialCoefficientsReader`
    
        Reader for the GRGS RL02 gravity field format.
    
        Since:
            1.3
    """
    def __init__(self, string: str): ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.gravity.variations.coefficients")``.

    GRGSRL02FormatReader: typing.Type[GRGSRL02FormatReader]
    VariableGravityFieldFactory: typing.Type[VariableGravityFieldFactory]
    VariablePotentialCoefficientsProvider: typing.Type[VariablePotentialCoefficientsProvider]
    VariablePotentialCoefficientsReader: typing.Type[VariablePotentialCoefficientsReader]
    VariablePotentialCoefficientsSet: typing.Type[VariablePotentialCoefficientsSet]
