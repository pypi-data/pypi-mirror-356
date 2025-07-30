
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import typing



class AbstractTLEFitter:
    """
    public abstract class AbstractTLEFitter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Abstract class for TLE/Orbit fitting.
    
        Two-Line Elements are tightly linked to the SGP4/SDP4 propagation models. They cannot be used with other models and do
        not represent osculating orbits. When conversion is needed, the model must be considered and conversion must be done by
        some fitting method on a sufficient time range.
    
        This base class factor the common code for such conversions. Different implementations correspond to different fitting
        algorithms.
    
        Since:
            6.0
    """
    def getRMS(self) -> float:
        """
            Get Root Mean Square of the fitting.
        
            Returns:
                rms
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.analytical.tle.AbstractTLEFitter.toTLE`
        
        protected double getRMS(double[] parameters) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Get the RMS for a given position/velocity/B* parameters set.
        
            Parameters:
                parameters (double[]): position/velocity/B* parameters set
        
            Returns:
                RMS
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if position/velocity cannot be computed at some date
        
            Also see:
        
        
        """
        ...
    def getTLE(self) -> 'TLE':
        """
            Get the fitted Two-Lines Elements.
        
            Returns:
                fitted Two-Lines Elements
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.propagation.analytical.tle.AbstractTLEFitter.toTLE`
        
        protected :class:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLE` getTLE(double[] parameters) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Get the TLE for a given position/velocity/B* parameters set.
        
            Parameters:
                parameters (double[]): position/velocity/B* parameters set
        
            Returns:
                TLE
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: thrown if inclination is negative
        
        
        """
        ...
    def toTLE(self, list: java.util.List[fr.cnes.sirius.patrius.propagation.SpacecraftState], double: float, boolean: bool, boolean2: bool) -> 'TLE': ...

class TLE(fr.cnes.sirius.patrius.time.TimeStamped, java.io.Serializable):
    """
    public class TLE extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.time.TimeStamped`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class is a container for a single set of TLE data.
    
        TLE sets can be built either by providing directly the two lines, in which case parsing is performed internally or by
        providing the already parsed elements.
    
        TLE are not transparently convertible to :class:`~fr.cnes.sirius.patrius.orbits.Orbit` instances. They are significant
        only with respect to their dedicated :class:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLEPropagator`, which
        also computes position and velocity coordinates. Any attempt to directly use orbital parameters like
        :meth:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLE.getE`,
        :meth:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLE.getI`, etc. without any reference to the
        :class:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLEPropagator` is prone to errors.
    
        More information on the TLE format can be found on the `CelesTrak website. <http://www.celestrak.com/>`
    
        Also see:
            :meth:`~serialized`
    """
    DEFAULT: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT
    
        Identifier for default type of ephemeris (SGP4/SDP4).
    
        Also see:
            :meth:`~constant`
    
    
    """
    SGP: typing.ClassVar[int] = ...
    """
    public static final int SGP
    
        Identifier for SGP type of ephemeris.
    
        Also see:
            :meth:`~constant`
    
    
    """
    SGP4: typing.ClassVar[int] = ...
    """
    public static final int SGP4
    
        Identifier for SGP4 type of ephemeris.
    
        Also see:
            :meth:`~constant`
    
    
    """
    SDP4: typing.ClassVar[int] = ...
    """
    public static final int SDP4
    
        Identifier for SDP4 type of ephemeris.
    
        Also see:
            :meth:`~constant`
    
    
    """
    SGP8: typing.ClassVar[int] = ...
    """
    public static final int SGP8
    
        Identifier for SGP8 type of ephemeris.
    
        Also see:
            :meth:`~constant`
    
    
    """
    SDP8: typing.ClassVar[int] = ...
    """
    public static final int SDP8
    
        Identifier for SDP8 type of ephemeris.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, int: int, char: str, int2: int, int3: int, string: str, int4: int, int5: int, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, int6: int, double9: float): ...
    @typing.overload
    def __init__(self, string: str, string2: str): ...
    def equals(self, object: typing.Any) -> bool:
        """
            Test for the equality of two TLE objects.
        
            TLE objects are considered equals if they have the same attributes
        
            Overrides:
                 in class 
        
            Parameters:
                object (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): Object to test for equality to this
        
            Returns:
                true if two TLE are equal
        
        
        """
        ...
    def getBStar(self) -> float:
        """
            Get the ballistic coefficient.
        
            Returns:
                bStar
        
        
        """
        ...
    def getClassification(self) -> str:
        """
            Get the classification.
        
            Returns:
                classification
        
        
        """
        ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the TLE current date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.time.TimeStamped.getDate` in interface :class:`~fr.cnes.sirius.patrius.time.TimeStamped`
        
            Returns:
                the epoch
        
        
        """
        ...
    def getE(self) -> float:
        """
            Get the eccentricity.
        
            Returns:
                the eccentricity
        
        
        """
        ...
    def getElementNumber(self) -> int:
        """
            Get the element number.
        
            Returns:
                the element number
        
        
        """
        ...
    def getEphemerisType(self) -> int:
        """
            Get the type of ephemeris.
        
            Returns:
                the ephemeris type (one of :meth:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLE.DEFAULT`,
                :meth:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLE.SGP`,
                :meth:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLE.SGP4`,
                :meth:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLE.SGP8`,
                :meth:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLE.SDP4`,
                :meth:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLE.SDP8`)
        
        
        """
        ...
    def getI(self) -> float:
        """
            Get the inclination in [0, π].
        
            Returns:
                the inclination (rad)
        
        
        """
        ...
    def getLaunchNumber(self) -> int:
        """
            Get the launch number.
        
            Returns:
                the launch number
        
        
        """
        ...
    def getLaunchPiece(self) -> str:
        """
            Get the launch piece.
        
            Returns:
                the launch piece
        
        
        """
        ...
    def getLaunchYear(self) -> int:
        """
            Get the launch year.
        
            Returns:
                the launch year
        
        
        """
        ...
    def getLine1(self) -> str: ...
    def getLine2(self) -> str:
        """
            Get the second line.
        
            Returns:
                second line
        
        
        """
        ...
    def getMeanAnomaly(self) -> float:
        """
            Get the mean anomaly in [0, 2π].
        
            Returns:
                the mean anomaly (rad)
        
        
        """
        ...
    def getMeanMotion(self) -> float:
        """
            Get the mean motion.
        
            Returns:
                the mean motion (rad/s)
        
        
        """
        ...
    def getMeanMotionFirstDerivative(self) -> float:
        """
            Get the mean motion first derivative.
        
            Returns:
                the mean motion first derivative (rad/s :sup:`2` )
        
        
        """
        ...
    def getMeanMotionSecondDerivative(self) -> float:
        """
            Get the mean motion second derivative.
        
            Returns:
                the mean motion second derivative (rad/s :sup:`3` )
        
        
        """
        ...
    def getPerigeeArgument(self) -> float:
        """
            Get the argument of perigee in [0, 2π].
        
            Returns:
                omega (rad)
        
        
        """
        ...
    def getRaan(self) -> float:
        """
            Get Right Ascension of the Ascending node in [0, 2π].
        
            Returns:
                the raan (rad)
        
        
        """
        ...
    def getRevolutionNumberAtEpoch(self) -> int:
        """
            Get the revolution number.
        
            Returns:
                the revolutionNumberAtEpoch
        
        
        """
        ...
    def getSatelliteNumber(self) -> int:
        """
            Get the satellite id.
        
            Returns:
                the satellite number
        
        
        """
        ...
    def hashCode(self) -> int:
        """
            Get a hashCode for the TLE.
        
            Overrides:
                 in class 
        
            Returns:
                a hash code value for this object
        
        
        """
        ...
    @staticmethod
    def isFormatOK(string: str, string2: str) -> bool: ...
    def toString(self) -> str:
        """
            Get a string representation of this TLE set.
        
            The representation is simply the two lines separated by the platform line separator.
        
            Overrides:
                 in class 
        
            Returns:
                string representation of this TLE set
        
        
        """
        ...

class TLEConstants:
    """
    public class TLEConstants extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Constants necessary to TLE propagation. This constants are used in the WGS-72 model, compliant with NORAD
        implementations.
    """
    ONE_THIRD: typing.ClassVar[float] = ...
    """
    public static final double ONE_THIRD
    
        Constant 1.0 / 3.0.
    
        Also see:
            :meth:`~constant`
    
    
    """
    TWO_THIRD: typing.ClassVar[float] = ...
    """
    public static final double TWO_THIRD
    
        Constant 2.0 / 3.0.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EARTH_RADIUS: typing.ClassVar[float] = ...
    """
    public static final double EARTH_RADIUS
    
        Earth radius in km.
    
        Also see:
            :meth:`~constant`
    
    
    """
    NORMALIZED_EQUATORIAL_RADIUS: typing.ClassVar[float] = ...
    """
    public static final double NORMALIZED_EQUATORIAL_RADIUS
    
        Equatorial radius rescaled (1.0).
    
        Also see:
            :meth:`~constant`
    
    
    """
    MINUTES_PER_DAY: typing.ClassVar[float] = ...
    """
    public static final double MINUTES_PER_DAY
    
        Time units per julian day.
    
        Also see:
            :meth:`~constant`
    
    
    """
    XKE: typing.ClassVar[float] = ...
    """
    public static final double XKE
    
        Potential perturbation coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    XJ3: typing.ClassVar[float] = ...
    """
    public static final double XJ3
    
        Potential perturbation coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    XJ2: typing.ClassVar[float] = ...
    """
    public static final double XJ2
    
        Potential perturbation coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    XJ4: typing.ClassVar[float] = ...
    """
    public static final double XJ4
    
        Potential perturbation coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    CK2: typing.ClassVar[float] = ...
    """
    public static final double CK2
    
        Potential perturbation coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    CK4: typing.ClassVar[float] = ...
    """
    public static final double CK4
    
        Potential perturbation coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    S: typing.ClassVar[float] = ...
    """
    public static final double S
    
        Potential perturbation coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    QOMS2T: typing.ClassVar[float] = ...
    """
    public static final double QOMS2T
    
        Potential perturbation coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    A3OVK2: typing.ClassVar[float] = ...
    """
    public static final double A3OVK2
    
        Potential perturbation coefficient.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...

class TLEPropagator(fr.cnes.sirius.patrius.propagation.AbstractPropagator):
    """
    public abstract class TLEPropagator extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`
    
        This class provides elements to propagate TLE's.
    
        The models used are SGP4 and SDP4, initially proposed by NORAD as the unique convenient propagator for TLE's. Inputs and
        outputs of this propagator are only suited for NORAD two lines elements sets, since it uses estimations and mean values
        appropriate for TLE's only.
    
        Deep- or near- space propagator is selected internally according to NORAD recommendations so that the user has not to
        worry about the used computation methods. One instance is created for each TLE (this instance can only be get using
        :meth:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLEPropagator.selectExtrapolator` method, and can compute
        :class:`~fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates` at any time. Maximum accuracy is guaranteed in a 24h
        range period before and after the provided TLE epoch (of course this accuracy is not really measurable nor predictable:
        according to `CelesTrak <http://www.celestrak.com/>`, the precision is close to one kilometer and error won't probably
        rise above 2 km).
    
        This implementation is largely inspired from the paper and source code `Revisiting Spacetrack Report #3
        <http://www.celestrak.com/publications/AIAA/2006-6753/>` and is fully compliant with its results and tests cases.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLE`, :meth:`~serialized`
    """
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the frame in which the orbit is propagated.
        
            4 cases are possible:
        
              - The propagation frame has been defined (using :code:`#setOrbitFrame(Frame)`): it is returned.
              - The propagation frame has not been defined and the initial state has been provided and is expressed in a pseudo-inertial
                frame: the initial state frame is returned.
              - The propagation frame has not been defined and the initial state has been provided and is not expressed in a
                pseudo-inertial frame: null is returned.
              - The propagation frame has not been defined and the initial state has not been provided: null is returned.
        
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.getFrame` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.Propagator`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator.getFrame` in
                class :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`
        
            Returns:
                frame in which the orbit is propagated
        
        
        """
        ...
    @typing.overload
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, frame: fr.cnes.sirius.patrius.frames.Frame) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    @typing.overload
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def getTLE(self) -> TLE:
        """
            Get the underlying TLE.
        
            Returns:
                underlying TLE
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def selectExtrapolator(tLE: TLE) -> 'TLEPropagator': ...
    @typing.overload
    @staticmethod
    def selectExtrapolator(tLE: TLE, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider) -> 'TLEPropagator': ...
    @typing.overload
    @staticmethod
    def selectExtrapolator(tLE: TLE, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider) -> 'TLEPropagator': ...

class TLESeries(fr.cnes.sirius.patrius.data.DataLoader, java.io.Serializable):
    """
    public class TLESeries extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataLoader`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class reads and handles series of TLEs for one space object.
    
        TLE data is read using the standard Orekit mechanism based on a configured
        :class:`~fr.cnes.sirius.patrius.data.DataProvidersManager`. This means TLE data may be retrieved from many different
        storage media (local disk files, remote servers, database ...).
    
        This class provides bounded ephemerides by finding the best initial TLE to propagate and then handling the propagation.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.analytical.tle.TLE`,
            :class:`~fr.cnes.sirius.patrius.data.DataProvidersManager`, :meth:`~serialized`
    """
    def __init__(self, string: str, boolean: bool): ...
    def getAvailableSatelliteNumbers(self) -> java.util.Set[int]: ...
    def getClosestTLE(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> TLE:
        """
            Get the closest TLE to the selected date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the date
        
            Returns:
                the TLE that will suit the most for propagation.
        
        
        """
        ...
    def getFirst(self) -> TLE:
        """
            Get the first TLE.
        
            Returns:
                first TLE
        
        
        """
        ...
    def getFirstDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the start date of the series.
        
            Returns:
                the first date
        
        
        """
        ...
    def getLast(self) -> TLE:
        """
            Get the last TLE.
        
            Returns:
                last TLE
        
        
        """
        ...
    def getLastDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the last date of the series.
        
            Returns:
                the end date
        
        
        """
        ...
    def getPVCoordinates(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates: ...
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...
    @typing.overload
    def loadTLEData(self) -> None: ...
    @typing.overload
    def loadTLEData(self, int: int) -> None: ...
    @typing.overload
    def loadTLEData(self, int: int, int2: int, string: str) -> None: ...
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

class DifferentialOrbitConverter(AbstractTLEFitter):
    """
    public class DifferentialOrbitConverter extends :class:`~fr.cnes.sirius.patrius.propagation.analytical.tle.AbstractTLEFitter`
    
        Orbit converter for Two-Lines Elements using differential algorithm.
    
        Since:
            6.0
    """
    def __init__(self, int: int, int2: int, char: str, int3: int, int4: int, string: str, int5: int, int6: int): ...

class LevenbergMarquardtOrbitConverter(AbstractTLEFitter):
    """
    public class LevenbergMarquardtOrbitConverter extends :class:`~fr.cnes.sirius.patrius.propagation.analytical.tle.AbstractTLEFitter`
    
        Orbit converter for Two-Lines Elements using differential algorithm.
    
        Since:
            6.0
    """
    def __init__(self, int: int, int2: int, char: str, int3: int, int4: int, string: str, int5: int, int6: int): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation.analytical.tle")``.

    AbstractTLEFitter: typing.Type[AbstractTLEFitter]
    DifferentialOrbitConverter: typing.Type[DifferentialOrbitConverter]
    LevenbergMarquardtOrbitConverter: typing.Type[LevenbergMarquardtOrbitConverter]
    TLE: typing.Type[TLE]
    TLEConstants: typing.Type[TLEConstants]
    TLEPropagator: typing.Type[TLEPropagator]
    TLESeries: typing.Type[TLESeries]
