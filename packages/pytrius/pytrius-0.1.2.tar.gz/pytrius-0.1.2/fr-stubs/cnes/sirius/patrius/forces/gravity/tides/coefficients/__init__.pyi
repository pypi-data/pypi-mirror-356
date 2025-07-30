
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.data
import java.io
import typing



class OceanTidesCoefficientsFactory:
    FES2004_FILENAME: typing.ClassVar[str] = ...
    @staticmethod
    def addDefaultOceanTidesCoefficientsReaders() -> None: ...
    @staticmethod
    def addOceanTidesCoefficientsReader(oceanTidesCoefficientsReader: 'OceanTidesCoefficientsReader') -> None: ...
    @staticmethod
    def clearOceanTidesCoefficientsReaders() -> None: ...
    @staticmethod
    def getCoefficientsProvider() -> 'OceanTidesCoefficientsProvider': ...

class OceanTidesCoefficientsProvider(java.io.Serializable):
    """
    public interface OceanTidesCoefficientsProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for ocean tides coefficients provider.
    
    
        The proper way to use this it to call the
        :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsFactory.getCoefficientsProvider`
        method. Indeed, the :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsFactory`
        will determine the best reader to use, depending on file available in the file system.
    
        Since:
            1.2
    """
    def getCpmEpm(self, double: float, int: int, int2: int) -> typing.MutableSequence[float]:
        """
            Get the C :sub:`lm` :sup:`±` and ε :sub:`lm` :sup:`±` for given wave
        
            Parameters:
                nDoodson (double): doodson number doodson number
                l (int): order
                m (int): degree
        
            Returns:
                double[4] array containing {C :sub:`lm` :sup:`+` , C :sub:`lm` :sup:`-` , ε :sub:`lm` :sup:`+` , ε :sub:`lm` :sup:`-` }
        
        
        """
        ...
    def getCpmSpm(self, double: float, int: int, int2: int) -> typing.MutableSequence[float]:
        """
            Get the C :sub:`lm` :sup:`±` and S :sub:`lm` :sup:`±` for given wave
        
            Parameters:
                nDoodson (double): doodson number
                l (int): order
                m (int): degree
        
            Returns:
                double[4] array containing {C :sub:`lm` :sup:`+` , C :sub:`lm` :sup:`-` , S :sub:`lm` :sup:`+` , S :sub:`lm` :sup:`-` }
        
        
        """
        ...
    def getDoodsonNumbers(self) -> typing.MutableSequence[float]:
        """
            Get available Doodson numbers
        
            Returns:
                array of Doodson numbers
        
        
        """
        ...
    def getMaxDegree(self, double: float, int: int) -> int:
        """
            Get maximum degree for given wave and order
        
            Parameters:
                doodson (double): number
                order (int): of wave
        
            Returns:
                Max degree for given wave
        
        
        """
        ...
    def getMaxOrder(self, double: float) -> int:
        """
            Get maximum order for given wave
        
            Parameters:
                doodson (double): number
        
            Returns:
                Max order for given wave
        
        
        """
        ...
    def getMinDegree(self, double: float, int: int) -> int:
        """
            Get min degree for given wave and order
        
            Parameters:
                doodson (double): number
                order (int): of wave
        
            Returns:
                Min degree for given wave
        
        
        """
        ...

class OceanTidesCoefficientsSet:
    """
    public final class OceanTidesCoefficientsSet extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Represents a line from the ocean tides data file.
    
    
        The proper way to use this it to call the
        :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsFactory.getCoefficientsProvider`
        method. Indeed, the :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsFactory`
        will determine the best reader to use, depending on file available in the file system.
    
        Since:
            1.2
    """
    def __init__(self, double: float, int: int, int2: int, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float): ...
    def code(self) -> float:
        """
            Get a hashcode for this set.
        
            Returns:
                hashcode
        
        
        """
        ...
    @staticmethod
    def computeCode(double: float, int: int, int2: int) -> float:
        """
            Computes code of data set. Assigns a unique `null
            <http://docs.oracle.com/javase/8/docs/api/java/lang/Integer.html?is-external=true>` to a
            :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsSet` depending on Doodson
            number, degree and order.
        
            Parameters:
                doodson (double): doodson number
                l (int): degree
                m (int): order
        
            Returns:
                code
        
        
        """
        ...
    def getCcm(self) -> float:
        """
        
            Returns:
                C :sub:`lm` :sup:`-`
        
        
        """
        ...
    def getCcp(self) -> float:
        """
        
            Returns:
                C :sub:`lm` :sup:`+`
        
        
        """
        ...
    def getCm(self) -> float:
        """
        
            Returns:
                C :sub:`lm` :sup:`-`
        
        
        """
        ...
    def getCp(self) -> float:
        """
        
            Returns:
                C :sub:`lm` :sup:`+`
        
        
        """
        ...
    def getCsm(self) -> float:
        """
        
            Returns:
                S :sub:`lm` :sup:`-`
        
        
        """
        ...
    def getCsp(self) -> float:
        """
        
            Returns:
                S :sub:`lm` :sup:`+`
        
        
        """
        ...
    def getDegree(self) -> int:
        """
        
            Returns:
                the degree
        
        
        """
        ...
    def getDoodson(self) -> float:
        """
        
            Returns:
                the doodson number
        
        
        """
        ...
    def getEm(self) -> float:
        """
        
            Returns:
                ε :sub:`lm` :sup:`-`
        
        
        """
        ...
    def getEp(self) -> float:
        """
        
            Returns:
                ε :sub:`lm` :sup:`+`
        
        
        """
        ...
    def getOrder(self) -> int:
        """
        
            Returns:
                the order
        
        
        """
        ...

class OceanTidesCoefficientsReader(fr.cnes.sirius.patrius.data.DataLoader, OceanTidesCoefficientsProvider):
    """
    public abstract class OceanTidesCoefficientsReader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataLoader`, :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
    
        This abstract class represents a Ocean Tides Coefficients file reader.
    
        For any format specific reader of ocean tides coefficients file, this interface represents all the methods that should
        be implemented by a reader.
    
    
        The proper way to use this it to call the
        :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsFactory.getCoefficientsProvider`
        method. Indeed, the :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsFactory`
        will determine the best reader to use, depending on file available in the file system.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsFactory`, :meth:`~serialized`
    """
    def getCpmEpm(self, double: float, int: int, int2: int) -> typing.MutableSequence[float]:
        """
            Get the C :sub:`lm` :sup:`±` and ε :sub:`lm` :sup:`±` for given wave
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getCpmEpm` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Parameters:
                nDoodson (double): doodson number doodson number
                l (int): order
                m (int): degree
        
            Returns:
                double[4] array containing {C :sub:`lm` :sup:`+` , C :sub:`lm` :sup:`-` , ε :sub:`lm` :sup:`+` , ε :sub:`lm` :sup:`-` }
        
        
        """
        ...
    def getCpmSpm(self, double: float, int: int, int2: int) -> typing.MutableSequence[float]:
        """
            Get the C :sub:`lm` :sup:`±` and S :sub:`lm` :sup:`±` for given wave
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getCpmSpm` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Parameters:
                nDoodson (double): doodson number
                l (int): order
                m (int): degree
        
            Returns:
                double[4] array containing {C :sub:`lm` :sup:`+` , C :sub:`lm` :sup:`-` , S :sub:`lm` :sup:`+` , S :sub:`lm` :sup:`-` }
        
        
        """
        ...
    def getDoodsonNumbers(self) -> typing.MutableSequence[float]:
        """
            Get available Doodson numbers
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getDoodsonNumbers` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Returns:
                array of Doodson numbers
        
        
        """
        ...
    def getMaxDegree(self, double: float, int: int) -> int:
        """
            Get maximum degree for given wave and order
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getMaxDegree` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Parameters:
                doodson (double): number
                order (int): of wave
        
            Returns:
                Max degree for given wave
        
        
        """
        ...
    def getMaxOrder(self, double: float) -> int:
        """
            Get maximum order for given wave
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getMaxOrder` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Parameters:
                doodson (double): number
        
            Returns:
                Max order for given wave
        
        
        """
        ...
    def getMinDegree(self, double: float, int: int) -> int:
        """
            Get min degree for given wave and order
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider.getMinDegree` in
                interface :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsProvider`
        
            Parameters:
                doodson (double): number
                order (int): of wave
        
            Returns:
                Min degree for given wave
        
        
        """
        ...
    def getSupportedNames(self) -> str:
        """
            Get the regular expression for supported files names.
        
            Returns:
                regular expression for supported files names
        
        
        """
        ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...
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

class FES2004FormatReader(OceanTidesCoefficientsReader):
    """
    public class FES2004FormatReader extends :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsReader`
    
        Reader for FES2004 formats.
    
    
        The proper way to use this it to call the
        :meth:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsFactory.getCoefficientsProvider`
        method. Indeed, the :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsFactory`
        will determine the best reader to use, depending on file available in the file system.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.gravity.tides.coefficients.OceanTidesCoefficientsReader`, :meth:`~serialized`
    """
    def __init__(self, string: str): ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.gravity.tides.coefficients")``.

    FES2004FormatReader: typing.Type[FES2004FormatReader]
    OceanTidesCoefficientsFactory: typing.Type[OceanTidesCoefficientsFactory]
    OceanTidesCoefficientsProvider: typing.Type[OceanTidesCoefficientsProvider]
    OceanTidesCoefficientsReader: typing.Type[OceanTidesCoefficientsReader]
    OceanTidesCoefficientsSet: typing.Type[OceanTidesCoefficientsSet]
