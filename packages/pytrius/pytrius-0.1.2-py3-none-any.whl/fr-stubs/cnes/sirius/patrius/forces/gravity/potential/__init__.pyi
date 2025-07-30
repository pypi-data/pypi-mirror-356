
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.data
import java.io
import typing



class GravityFieldFactory:
    ICGEM_FILENAME: typing.ClassVar[str] = ...
    SHM_FILENAME: typing.ClassVar[str] = ...
    EGM_FILENAME: typing.ClassVar[str] = ...
    GRGS_FILENAME: typing.ClassVar[str] = ...
    @staticmethod
    def addDefaultPotentialCoefficientsReaders() -> None: ...
    @staticmethod
    def addPotentialCoefficientsReader(potentialCoefficientsReader: 'PotentialCoefficientsReader') -> None: ...
    @staticmethod
    def clearPotentialCoefficientsReaders() -> None: ...
    @staticmethod
    def getPotentialProvider() -> 'PotentialCoefficientsProvider': ...

class PotentialCoefficientsProvider(java.io.Serializable):
    """
    public interface PotentialCoefficientsProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface used to provide gravity field coefficients.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.GravityFieldFactory`
    """
    def getAe(self) -> float:
        """
            Get the value of the central body reference radius.
        
            Returns:
                ae (m)
        
        
        """
        ...
    def getC(self, int: int, int2: int, boolean: bool) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getJ(self, boolean: bool, int: int) -> typing.MutableSequence[float]: ...
    def getMu(self) -> float:
        """
            Get the central body attraction coefficient.
        
            Returns:
                mu (m :sup:`3` /s :sup:`2` )
        
        
        """
        ...
    def getS(self, int: int, int2: int, boolean: bool) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getSigmaC(self, int: int, int2: int, boolean: bool) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getSigmaS(self, int: int, int2: int, boolean: bool) -> typing.MutableSequence[typing.MutableSequence[float]]: ...

class PotentialCoefficientsReader(fr.cnes.sirius.patrius.data.DataLoader, PotentialCoefficientsProvider):
    def __init__(self, string: str, boolean: bool, boolean2: bool): ...
    def getAe(self) -> float: ...
    def getC(self, int: int, int2: int, boolean: bool) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getJ(self, boolean: bool, int: int) -> typing.MutableSequence[float]: ...
    def getMu(self) -> float: ...
    def getS(self, int: int, int2: int, boolean: bool) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getSigmaC(self, int: int, int2: int, boolean: bool) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getSigmaS(self, int: int, int2: int, boolean: bool) -> typing.MutableSequence[typing.MutableSequence[float]]: ...
    def getSupportedNames(self) -> str: ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...
    def missingCoefficientsAllowed(self) -> bool: ...
    def stillAcceptsData(self) -> bool: ...

class EGMFormatReader(PotentialCoefficientsReader):
    """
    public class EGMFormatReader extends :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.PotentialCoefficientsReader`
    
        This reader is adapted to the EGM Format.
    
        The proper way to use this class is to call the
        :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.GravityFieldFactory` which will determine which reader to use
        with the selected potential coefficients file
    
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.GravityFieldFactory`, :meth:`~serialized`
    """
    def __init__(self, string: str, boolean: bool): ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...

class GRGSFormatReader(PotentialCoefficientsReader):
    @typing.overload
    def __init__(self, string: str, boolean: bool): ...
    @typing.overload
    def __init__(self, string: str, boolean: bool, boolean2: bool): ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...

class ICGEMFormatReader(PotentialCoefficientsReader):
    """
    public class ICGEMFormatReader extends :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.PotentialCoefficientsReader`
    
        Reader for the ICGEM gravity field format.
    
        This format is used to describe the gravity field of EIGEN models published by the GFZ Potsdam since 2004. It is
        described in Franz Barthelmes and Christoph Förste paper: `the ICGEM-format
        <http://op.gfz-potsdam.de/grace/results/grav/g005_ICGEM-Format.pdf>`.
    
        The proper way to use this class is to call the
        :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.GravityFieldFactory` which will determine which reader to use
        with the selected potential coefficients file
    
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.GravityFieldFactory`, :meth:`~serialized`
    """
    def __init__(self, string: str, boolean: bool): ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...

class SHMFormatReader(PotentialCoefficientsReader):
    """
    public class SHMFormatReader extends :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.PotentialCoefficientsReader`
    
        Reader for the SHM gravity field format.
    
        This format was used to describe the gravity field of EIGEN models published by the GFZ Potsdam up to 2003. It was then
        replaced by :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.ICGEMFormatReader`. The SHM format is described in
        ` Potsdam university website <http://www.gfz-potsdam.de/grace/results/>`.
    
        The proper way to use this class is to call the
        :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.GravityFieldFactory` which will determine which reader to use
        with the selected potential coefficients file
    
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.forces.gravity.potential.GravityFieldFactory`, :meth:`~serialized`
    """
    def __init__(self, string: str, boolean: bool): ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.gravity.potential")``.

    EGMFormatReader: typing.Type[EGMFormatReader]
    GRGSFormatReader: typing.Type[GRGSFormatReader]
    GravityFieldFactory: typing.Type[GravityFieldFactory]
    ICGEMFormatReader: typing.Type[ICGEMFormatReader]
    PotentialCoefficientsProvider: typing.Type[PotentialCoefficientsProvider]
    PotentialCoefficientsReader: typing.Type[PotentialCoefficientsReader]
    SHMFormatReader: typing.Type[SHMFormatReader]
