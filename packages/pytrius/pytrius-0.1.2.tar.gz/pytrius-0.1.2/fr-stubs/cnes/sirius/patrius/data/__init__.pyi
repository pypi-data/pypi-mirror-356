
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.net
import java.util
import java.util.regex
import jpype.protocol
import typing



class BodiesElements(java.io.Serializable):
    """
    public final class BodiesElements extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Elements of the bodies having an effect on nutation.
    
        This class is a simple placeholder, it does not provide any processing method.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float, double10: float, double11: float, double12: float, double13: float, double14: float): ...
    def getD(self) -> float:
        """
            Get the mean elongation of the Moon from the Sun.
        
            Returns:
                mean elongation of the Moon from the Sun.
        
        
        """
        ...
    def getF(self) -> float:
        """
            Get L - Ω where L is the mean longitude of the Moon.
        
            Returns:
                L - Ω
        
        
        """
        ...
    def getL(self) -> float:
        """
            Get the mean anomaly of the Moon.
        
            Returns:
                mean anomaly of the Moon
        
        
        """
        ...
    def getLE(self) -> float:
        """
            Get the mean Earth longitude.
        
            Returns:
                mean Earth longitude.
        
        
        """
        ...
    def getLJu(self) -> float:
        """
            Get the mean Jupiter longitude.
        
            Returns:
                mean Jupiter longitude.
        
        
        """
        ...
    def getLMa(self) -> float:
        """
            Get the mean Mars longitude.
        
            Returns:
                mean Mars longitude.
        
        
        """
        ...
    def getLMe(self) -> float:
        """
            Get the mean Mercury longitude.
        
            Returns:
                mean Mercury longitude.
        
        
        """
        ...
    def getLNe(self) -> float:
        """
            Get the mean Neptune longitude.
        
            Returns:
                mean Neptune longitude.
        
        
        """
        ...
    def getLPrime(self) -> float:
        """
            Get the mean anomaly of the Sun.
        
            Returns:
                mean anomaly of the Sun.
        
        
        """
        ...
    def getLSa(self) -> float:
        """
            Get the mean Saturn longitude.
        
            Returns:
                mean Saturn longitude.
        
        
        """
        ...
    def getLUr(self) -> float:
        """
            Get the mean Uranus longitude.
        
            Returns:
                mean Uranus longitude.
        
        
        """
        ...
    def getLVe(self) -> float:
        """
            Get the mean Venus longitude.
        
            Returns:
                mean Venus longitude.
        
        
        """
        ...
    def getOmega(self) -> float:
        """
            Get the mean longitude of the ascending node of the Moon.
        
            Returns:
                mean longitude of the ascending node of the Moon.
        
        
        """
        ...
    def getPa(self) -> float:
        """
            Get the general accumulated precession in longitude.
        
            Returns:
                general accumulated precession in longitude.
        
        
        """
        ...

class DataLoader:
    """
    public interface DataLoader
    
        Interface for loading data files from :class:`~fr.cnes.sirius.patrius.data.DataProvider`.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.data.DataProvider`
    """
    def loadData(self, inputStream: java.io.InputStream, string: str) -> None: ...
    def stillAcceptsData(self) -> bool:
        """
            Check if the loader still accepts new data.
        
            This method is used to speed up data loading by interrupting crawling the data sets as soon as a loader has found the
            data it was waiting for. For loaders that can merge data from any number of sources (for example JPL ephemerides or
            Earth Orientation Parameters that are split among several files), this method should always return true to make sure no
            data is left over.
        
            Returns:
                true while the loader still accepts new data
        
        
        """
        ...

class DataProvider(java.io.Serializable):
    """
    public interface DataProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for providing data files to :class:`~fr.cnes.sirius.patrius.data.DataLoader`.
    
        This interface defines a generic way to explore some collection holding data files and load some of them. The collection
        may be a list of resources in the classpath, a directories tree in filesystem, a zip or jar archive, a database, a
        connexion to a remote server ...
    
        The proper way to use this interface is to configure one or more implementations and register them in the
        :class:`~fr.cnes.sirius.patrius.data.DataProvidersManager`, or to let this manager use its default configuration. Once
        registered, they will be used automatically whenever some data needs to be loaded. This allow high level applications
        developers to customize Orekit data loading mechanism and get a tighter intergation of the library within their
        application.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.data.DataLoader`, :class:`~fr.cnes.sirius.patrius.data.DataProvidersManager`
    """
    GZIP_FILE_PATTERN: typing.ClassVar[java.util.regex.Pattern] = ...
    """
    static final `Pattern <http://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html?is-external=true>` GZIP_FILE_PATTERN
    
        Pattern for name of gzip files.
    
    """
    ZIP_ARCHIVE_PATTERN: typing.ClassVar[java.util.regex.Pattern] = ...
    """
    static final `Pattern <http://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html?is-external=true>` ZIP_ARCHIVE_PATTERN
    
        Pattern for name of zip/jar archives.
    
    """
    def feed(self, pattern: java.util.regex.Pattern, dataLoader: DataLoader) -> bool: ...

class DataProvidersManager(java.io.Serializable):
    """
    public final class DataProvidersManager extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Singleton class managing all supported :class:`~fr.cnes.sirius.patrius.data.DataProvider`.
    
        This class is the single point of access for all data loading features. It is used for example to load Earth Orientation
        Parameters used by IERS frames, to load UTC leap seconds used by time scales, to load planetary ephemerides ...
    
    
        It is user-customizable: users can add their own data providers at will. This allows them for example to use a database
        or an existing data loading library in order to embed an Orekit enabled application in a global system with its own data
        handling mechanisms. There is no upper limitation on the number of providers, but often each application will use only a
        few.
    
        If the list of providers is empty when attempting to :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.feed` a
        file loader, the :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.addDefaultProviders` method is called
        automatically to set up a default configuration. This default configuration contains one
        :class:`~fr.cnes.sirius.patrius.data.DataProvider` for each component of the path-like list specified by the java
        property :code:`orekit.data.path`. See the :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.feed` method
        documentation for further details. The default providers configuration is *not* set up if the list is not empty. If
        users want to have both the default providers and additional providers, they must call explicitly the
        :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.addDefaultProviders` method.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.data.DirectoryCrawler`, :class:`~fr.cnes.sirius.patrius.data.ClasspathCrawler`,
            :meth:`~serialized`
    """
    OREKIT_DATA_PATH: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` OREKIT_DATA_PATH
    
        Name of the property defining the root directories or zip/jar files path for default configuration.
    
        Also see:
            :meth:`~constant`
    
    
    """
    def addDefaultProviders(self) -> None: ...
    def addProvider(self, dataProvider: typing.Union[DataProvider, typing.Callable]) -> None:
        """
            Add a data provider to the supported list.
        
            Parameters:
                provider (:class:`~fr.cnes.sirius.patrius.data.DataProvider`): data provider to add
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.clearProviders`,
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.getProviders`
        
        
        """
        ...
    def clearLoadedDataNames(self) -> None:
        """
            Clear the set of data file names that have been loaded.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.getLoadedDataNames`
        
        
        """
        ...
    def clearProviders(self) -> None:
        """
            Remove all data providers.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.addProvider`,
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.removeProvider`,
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.isSupported`,
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.getProviders`
        
        
        """
        ...
    def feed(self, string: str, dataLoader: DataLoader) -> bool: ...
    @staticmethod
    def getInstance() -> 'DataProvidersManager':
        """
            Get the unique instance.
        
            Returns:
                unique instance of the manager.
        
        
        """
        ...
    def getLoadedDataNames(self) -> java.util.Set[str]: ...
    def getProviders(self) -> java.util.List[DataProvider]: ...
    def isSupported(self, dataProvider: typing.Union[DataProvider, typing.Callable]) -> bool:
        """
            Check if some provider is supported.
        
            Parameters:
                provider (:class:`~fr.cnes.sirius.patrius.data.DataProvider`): provider to check
        
            Returns:
                true if the specified provider instane is already in the supported list
        
            Since:
                5.1
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.addProvider`,
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.removeProvider`,
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.clearProviders`,
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.getProviders`
        
        
        """
        ...
    def removeProvider(self, dataProvider: typing.Union[DataProvider, typing.Callable]) -> DataProvider:
        """
            Remove one provider.
        
            Parameters:
                provider (:class:`~fr.cnes.sirius.patrius.data.DataProvider`): provider instance to remove
        
            Returns:
                instance removed (null if the provider was not already present)
        
            Since:
                5.1
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.addProvider`,
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.clearProviders`,
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.isSupported`,
                :meth:`~fr.cnes.sirius.patrius.data.DataProvidersManager.getProviders`
        
        
        """
        ...

class PATRIUSFileInputStream(java.io.FileInputStream):
    """
    public class PATRIUSFileInputStream extends `FileInputStream <http://docs.oracle.com/javase/8/docs/api/java/io/FileInputStream.html?is-external=true>`
    
        Extension of `null <http://docs.oracle.com/javase/8/docs/api/java/io/FileInputStream.html?is-external=true>` with file
        name storage.
    
        Since:
            4.11.1
    """
    def __init__(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath]): ...
    def getFile(self) -> java.io.File:
        """
            Returns the file associated to the stream.
        
            Returns:
                the file associated to the stream
        
        
        """
        ...

class PoissonSeries(java.io.Serializable):
    """
    public class PoissonSeries extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class representing a Poisson series for nutation or ephemeris computations.
    
        A Poisson series is composed of a time polynomial part and a non-polynomial part which consist in summation series. The
        :class:`~fr.cnes.sirius.patrius.data.SeriesTerm` are harmonic functions (combination of sines and cosines) of polynomial
        *arguments*. The polynomial arguments are combinations of luni-solar or planetary
        :class:`~fr.cnes.sirius.patrius.data.BodiesElements`.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.data.SeriesTerm`, :meth:`~serialized`
    """
    def __init__(self, inputStream: java.io.InputStream, double: float, string: str): ...
    @typing.overload
    def value(self, double: float, bodiesElements: BodiesElements) -> float:
        """
            Compute the value of the development for the current date.
        
            Parameters:
                t (double): current date
                elements (:class:`~fr.cnes.sirius.patrius.data.BodiesElements`): luni-solar and planetary elements for the current date
        
            Returns:
                current value of the development
        
            Compute the value of the development for the current date and its first time derivative.
        
            Parameters:
                t (double): current date
                elements (:class:`~fr.cnes.sirius.patrius.data.BodiesElements`): luni-solar and planetary elements for the current date
                elementsP (:class:`~fr.cnes.sirius.patrius.data.BodiesElements`): luni-solar and planetary time derivative elements for the current date
        
            Returns:
                current value of the development
        
        
        """
        ...
    @typing.overload
    def value(self, double: float, bodiesElements: BodiesElements, bodiesElements2: BodiesElements) -> typing.MutableSequence[float]: ...

class SeriesTerm(java.io.Serializable):
    """
    public abstract class SeriesTerm extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Base class for nutation series terms.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.data.PoissonSeries`, :meth:`~serialized`
    """
    @staticmethod
    def buildTerm(double: float, double2: float, int: int, int2: int, int3: int, int4: int, int5: int, int6: int, int7: int, int8: int, int9: int, int10: int, int11: int, int12: int, int13: int, int14: int) -> 'SeriesTerm':
        """
            Factory method for building the appropriate object.
        
            The method checks the null coefficients and build an instance of an appropriate type to avoid too many unnecessary
            multiplications by zero coefficients.
        
            Parameters:
                sinCoeff (double): coefficient for the sine of the argument
                cosCoeff (double): coefficient for the cosine of the argument
                cL (int): coefficient for mean anomaly of the Moon
                cLPrime (int): coefficient for mean anomaly of the Sun
                cF (int): coefficient for L - Ω where L is the mean longitude of the Moon
                cD (int): coefficient for mean elongation of the Moon from the Sun
                cOmega (int): coefficient for mean longitude of the ascending node of the Moon
                cMe (int): coefficient for mean Mercury longitude
                cVe (int): coefficient for mean Venus longitude
                cE (int): coefficient for mean Earth longitude
                cMa (int): coefficient for mean Mars longitude
                cJu (int): coefficient for mean Jupiter longitude
                cSa (int): coefficient for mean Saturn longitude
                cUr (int): coefficient for mean Uranus longitude
                cNe (int): coefficient for mean Neptune longitude
                cPa (int): coefficient for general accumulated precession in longitude
        
            Returns:
                a nutation serie term instance well suited for the set of coefficients
        
        
        """
        ...
    @typing.overload
    def value(self, bodiesElements: BodiesElements) -> float:
        """
            Compute the value of the term for the current date.
        
            Parameters:
                elements (:class:`~fr.cnes.sirius.patrius.data.BodiesElements`): luni-solar and planetary elements for the current date
        
            Returns:
                current value of the term
        
            Compute the value of the term for the current date and its first time derivative.
        
            Parameters:
                elements (:class:`~fr.cnes.sirius.patrius.data.BodiesElements`): luni-solar and planetary elements for the current date
                elementsP (:class:`~fr.cnes.sirius.patrius.data.BodiesElements`): luni-solar and planetary time derivative elements for the current date
        
            Returns:
                current value of the term
        
        
        """
        ...
    @typing.overload
    def value(self, bodiesElements: BodiesElements, bodiesElements2: BodiesElements) -> typing.MutableSequence[float]: ...

class ClasspathCrawler(DataProvider):
    """
    public class ClasspathCrawler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataProvider`
    
        Provider for data files stored as resources in the classpath.
    
        This class handles a list of data files or zip/jar archives located in the classpath. Since the classpath is not a tree
        structure the list elements cannot be whole directories recursively browsed as in
        :class:`~fr.cnes.sirius.patrius.data.DirectoryCrawler`, they must be data files or zip/jar archives.
    
        A typical use case is to put all data files in a single zip or jar archive and to build an instance of this class with
        the single name of this zip/jar archive. Two different instances may be used one for user or project specific data and
        another one for system-wide or general data.
    
        Gzip-compressed files are supported.
    
        Zip archives entries are supported recursively.
    
        This is a simple application of the :code:`visitor` design pattern for list browsing.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.data.DataProvidersManager`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, classLoader: java.lang.ClassLoader, *string: str): ...
    @typing.overload
    def __init__(self, *string: str): ...
    def feed(self, pattern: java.util.regex.Pattern, dataLoader: DataLoader) -> bool: ...

class DirectoryCrawler(DataProvider):
    """
    public class DirectoryCrawler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataProvider`
    
        Provider for data files stored in a directories tree on filesystem.
    
        This class handles data files recursively starting from a root directories tree. The organization of files in the
        directories is free. There may be sub-directories to any level. All sub-directories are browsed and all terminal files
        are checked for loading.
    
        Gzip-compressed files are supported.
    
        Zip archives entries are supported recursively.
    
        This is a simple application of the :code:`visitor` design pattern for directory hierarchy crawling.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.data.DataProvidersManager`, :meth:`~serialized`
    """
    def __init__(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath]): ...
    def feed(self, pattern: java.util.regex.Pattern, dataLoader: DataLoader) -> bool: ...

class NetworkCrawler(DataProvider):
    """
    public class NetworkCrawler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataProvider`
    
        Provider for data files directly fetched from network.
    
        This class handles a list of URLs pointing to data files or zip/jar on the net. Since the net is not a tree structure
        the list elements cannot be top elements recursively browsed as in
        :class:`~fr.cnes.sirius.patrius.data.DirectoryCrawler`, they must be data files or zip/jar archives.
    
        The files fetched from network can be locally cached on disk. This prevents too frequent network access if the URLs are
        remote ones (for example original internet URLs).
    
        If the URL points to a remote server (typically on the web) on the other side of a proxy server, you need to configure
        the networking layer of your application to use the proxy. For a typical authenticating proxy as used in many corporate
        environments, this can be done as follows using for example the AuthenticatorDialog graphical authenticator class that
        can be found in the tests directories:
    
        .. code-block: java
        
        
         System.setProperty("http.proxyHost", "proxy.your.domain.com");
         System.setProperty("http.proxyPort", "8080");
         System.setProperty("http.nonProxyHosts", "localhost|*.your.domain.com");
         Authenticator.setDefault(new AuthenticatorDialog());
         
    
        Gzip-compressed files are supported.
    
        Zip archives entries are supported recursively.
    
        This is a simple application of the :code:`visitor` design pattern for list browsing.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.data.DataProvidersManager`, :meth:`~serialized`
    """
    def __init__(self, *uRL: java.net.URL): ...
    def feed(self, pattern: java.util.regex.Pattern, dataLoader: DataLoader) -> bool: ...
    def setTimeout(self, int: int) -> None:
        """
            Set the timeout for connection.
        
            Parameters:
                timeoutIn (int): connection timeout in milliseconds
        
        
        """
        ...

class ZipJarCrawler(DataProvider):
    """
    public class ZipJarCrawler extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.data.DataProvider`
    
        Helper class for loading data files from a zip/jar archive.
    
        This class browses all entries in a zip/jar archive in filesystem or in classpath.
    
        The organization of entries within the archive is unspecified. All entries are checked in turn. If several entries of
        the archive are supported by the data loader, all of them will be loaded.
    
        Gzip-compressed files are supported.
    
        Zip archives entries are supported recursively.
    
        This is a simple application of the :code:`visitor` design pattern for zip entries browsing.
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.data.DataProvidersManager`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath]): ...
    @typing.overload
    def __init__(self, classLoader: java.lang.ClassLoader, string: str): ...
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, uRL: java.net.URL): ...
    def feed(self, pattern: java.util.regex.Pattern, dataLoader: DataLoader) -> bool: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.data")``.

    BodiesElements: typing.Type[BodiesElements]
    ClasspathCrawler: typing.Type[ClasspathCrawler]
    DataLoader: typing.Type[DataLoader]
    DataProvider: typing.Type[DataProvider]
    DataProvidersManager: typing.Type[DataProvidersManager]
    DirectoryCrawler: typing.Type[DirectoryCrawler]
    NetworkCrawler: typing.Type[NetworkCrawler]
    PATRIUSFileInputStream: typing.Type[PATRIUSFileInputStream]
    PoissonSeries: typing.Type[PoissonSeries]
    SeriesTerm: typing.Type[SeriesTerm]
    ZipJarCrawler: typing.Type[ZipJarCrawler]
