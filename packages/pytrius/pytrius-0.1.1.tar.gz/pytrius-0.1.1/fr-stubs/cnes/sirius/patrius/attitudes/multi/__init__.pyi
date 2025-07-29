
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import typing



class MultiAttitudeProvider(java.io.Serializable):
    """
    public interface MultiAttitudeProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface represents an attitude provider for multi-satellites models.
    
        An attitude provider provides a way to compute an :class:`~fr.cnes.sirius.patrius.attitudes.Attitude` from an date and
        several position-velocity provider.
    
        It is particularly useful if attitude of one satellite depends on PV of other satellites which themselves depend on
        other satellites PV.
    
        Since:
            4.2
    """
    @typing.overload
    def getAttitude(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.orbits.Orbit], typing.Mapping[str, fr.cnes.sirius.patrius.orbits.Orbit]]) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider], typing.Mapping[str, fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider]], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...

class MultiAttitudeProviderWrapper(MultiAttitudeProvider):
    """
    public class MultiAttitudeProviderWrapper extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider`
    
        Wrapper of attitude provider to make it compatible with
        :class:`~fr.cnes.sirius.patrius.attitudes.multi.MultiAttitudeProvider`.
    
        Since:
            4.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, string: str): ...
    @typing.overload
    def getAttitude(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.orbits.Orbit], typing.Mapping[str, fr.cnes.sirius.patrius.orbits.Orbit]]) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    @typing.overload
    def getAttitude(self, map: typing.Union[java.util.Map[str, fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider], typing.Mapping[str, fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider]], absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.attitudes.Attitude: ...
    def getAttitudeProvider(self) -> fr.cnes.sirius.patrius.attitudes.AttitudeProvider:
        """
            Returns the AttitudeProvider.
        
            Returns:
                the AttitudeProvider
        
        
        """
        ...
    def getID(self) -> str:
        """
            Returns the ID of the spacecraft associated with the AttitudeProvider.
        
            Returns:
                the ID of the spacecraft associated with the AttitudeProvider
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.attitudes.multi")``.

    MultiAttitudeProvider: typing.Type[MultiAttitudeProvider]
    MultiAttitudeProviderWrapper: typing.Type[MultiAttitudeProviderWrapper]
