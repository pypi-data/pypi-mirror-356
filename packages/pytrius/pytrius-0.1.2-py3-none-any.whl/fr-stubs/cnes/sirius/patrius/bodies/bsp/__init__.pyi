
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.bodies.bsp.spice
import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.time
import java.io
import java.lang
import java.util
import typing



class BSPEphemerisLoader(fr.cnes.sirius.patrius.bodies.JPLEphemerisLoader, fr.cnes.sirius.patrius.data.DataLoader):
    """
    public class BSPEphemerisLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.bodies.JPLEphemerisLoader`, :class:`~fr.cnes.sirius.patrius.data.DataLoader`
    
        Loader for the SPICE BSP format (type 2 and 3). For more details about the SPICE BSP format, please read the CSPICE
        documentation here
    
        This reader implements the :class:`~fr.cnes.sirius.patrius.bodies.CelestialBodyEphemerisLoader` interface and develops
        its own loading methods.
    
    
        Since:
            4.11.1
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT_BSP_SUPPORTED_NAMES: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` DEFAULT_BSP_SUPPORTED_NAMES
    
        Default supported files name pattern for BSP files.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_SUN: typing.ClassVar[float] = ...
    """
    public static final double MU_SUN
    
        Mu Sun.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_MERCURY: typing.ClassVar[float] = ...
    """
    public static final double MU_MERCURY
    
        Mu Mercury.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_VENUS: typing.ClassVar[float] = ...
    """
    public static final double MU_VENUS
    
        Mu Venus.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_EARTH_MOON: typing.ClassVar[float] = ...
    """
    public static final double MU_EARTH_MOON
    
        Mu Earth Moon barycenter.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_EARTH: typing.ClassVar[float] = ...
    """
    public static final double MU_EARTH
    
        Mu Earth.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_MOON: typing.ClassVar[float] = ...
    """
    public static final double MU_MOON
    
        Mu Moon.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_MARS: typing.ClassVar[float] = ...
    """
    public static final double MU_MARS
    
        Mu Mars.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_JUPITER: typing.ClassVar[float] = ...
    """
    public static final double MU_JUPITER
    
        Mu Jupiter.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_SATURN: typing.ClassVar[float] = ...
    """
    public static final double MU_SATURN
    
        Mu Saturn.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_URANUS: typing.ClassVar[float] = ...
    """
    public static final double MU_URANUS
    
        Mu Uranus.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_NEPTUNE: typing.ClassVar[float] = ...
    """
    public static final double MU_NEPTUNE
    
        Mu Neptune.
    
        Also see:
            :meth:`~constant`
    
    
    """
    MU_PLUTO: typing.ClassVar[float] = ...
    """
    public static final double MU_PLUTO
    
        Mu Pluto.
    
        Also see:
            :meth:`~constant`
    
    
    """
    SPICE_J2000_EPOCH: typing.ClassVar[fr.cnes.sirius.patrius.time.AbsoluteDate] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.time.AbsoluteDate` SPICE_J2000_EPOCH
    
        The basic spatial reference system for SPICE is the J2000 system.
    
    
        This is an inertial reference frame in which the equations of motion for the solar system may be integrated.
    
    
        This reference frame is specified by the orientation of the earth's mean equator and equinox at a particular epoch ---
        the J2000 epoch.
    
    
        This epoch is Greenwich noon on January 1, 2000 Barycentric Dynamical Time (TDB).
    
    """
    def __init__(self, string: str): ...
    @staticmethod
    def addSpiceBodyMapping(map: typing.Union[java.util.Map[int, str], typing.Mapping[int, str]]) -> None: ...
    @staticmethod
    def clearSpiceBodyMapping() -> None:
        """
            Clear the SPICE Body mapping
        
        """
        ...
    def getBodyLink(self) -> str:
        """
            Returns the BSP body name linked to PATRIUS frame tree.
        
            Returns:
                the BSP body name linked to PATRIUS frame tree
        
        
        """
        ...
    def getConvention(self) -> 'BSPEphemerisLoader.SpiceJ2000ConventionEnum':
        """
            Getter for the Spice J2000 convention.
        
            Returns:
                the Spice J2000 convention
        
        
        """
        ...
    def getLoadedGravitationalCoefficient(self, predefinedEphemerisType: fr.cnes.sirius.patrius.bodies.PredefinedEphemerisType) -> float:
        """
            Get the gravitational coefficient of a body. These coefficient values are coming from here.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.bodies.JPLEphemerisLoader.getLoadedGravitationalCoefficient` in
                interface :class:`~fr.cnes.sirius.patrius.bodies.JPLEphemerisLoader`
        
            Parameters:
                body (:class:`~fr.cnes.sirius.patrius.bodies.PredefinedEphemerisType`): body for which the gravitational coefficient is requested
        
            Returns:
                gravitational coefficient in m :sup:`3` /s :sup:`2`
        
        
        """
        ...
    def linkFramesTrees(self, frame: fr.cnes.sirius.patrius.frames.Frame, string: str) -> None: ...
    def loadCelestialBodyEphemeris(self, string: str) -> fr.cnes.sirius.patrius.bodies.CelestialBodyEphemeris: ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...
    def setSPICEJ2000Convention(self, spiceJ2000ConventionEnum: 'BSPEphemerisLoader.SpiceJ2000ConventionEnum') -> None:
        """
            Setter for the Spice J2000 convention.
        
            Parameters:
                newConvention (:class:`~fr.cnes.sirius.patrius.bodies.bsp.BSPEphemerisLoader.SpiceJ2000ConventionEnum`): Spice J2000 convention
        
        
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
    class SpiceJ2000ConventionEnum(java.lang.Enum['BSPEphemerisLoader.SpiceJ2000ConventionEnum']):
        EME2000: typing.ClassVar['BSPEphemerisLoader.SpiceJ2000ConventionEnum'] = ...
        ICRF: typing.ClassVar['BSPEphemerisLoader.SpiceJ2000ConventionEnum'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'BSPEphemerisLoader.SpiceJ2000ConventionEnum': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['BSPEphemerisLoader.SpiceJ2000ConventionEnum']: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.bodies.bsp")``.

    BSPEphemerisLoader: typing.Type[BSPEphemerisLoader]
    spice: fr.cnes.sirius.patrius.bodies.bsp.spice.__module_protocol__
