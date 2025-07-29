
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.addons.patriusdataset.atmosphere
import fr.cnes.sirius.addons.patriusdataset.ephemerides
import fr.cnes.sirius.addons.patriusdataset.force-models
import java.io
import java.lang
import java.net
import java.util
import java.util.regex
import jpype.protocol
import typing



class PatriusDataset:
    """
    public final class PatriusDataset extends Object
    
        Helper class for adding patrius dataset resources to patrius with
        :meth:`~fr.cnes.sirius.addons.patriusdataset.PatriusDataset.addResourcesFromPatriusDataset` method
    
        Also see:
            :meth:`~fr.cnes.sirius.addons.patriusdataset.PatriusDataset.addResourcesFromPatriusDataset`
    """
    @typing.overload
    @staticmethod
    def addResourcesFromPatriusDataset() -> None:
        """
            Adds resources of patriusdataset found in the classpath to the Data Providers Manager
        """
        ...
    @typing.overload
    @staticmethod
    def addResourcesFromPatriusDataset(classLoader: java.lang.ClassLoader, uRLResolver: typing.Union['URLResolver', typing.Callable]) -> None:
        """
            Adds resources of patriusdataset found in the classpath to the Data Providers Manager
        
            Parameters:
                cl (ClassLoader): the class loader to use
                urlResolver (:class:`~fr.cnes.sirius.addons.patriusdataset.URLResolver`): the url resolver needed to transform classpath URL to native java classpath library, in non classic environments such as
                    OSGI
        
        
        If unset null, no resolver is used
        
            Also see:
                :class:`~fr.cnes.sirius.addons.patriusdataset.URLResolver`
        
            Adds resources of patriusdataset found in the classpath to the Data Providers Manager
        
            Parameters:
                cl (ClassLoader): the class loader to use
                urlResolver (:class:`~fr.cnes.sirius.addons.patriusdataset.URLResolver`): the url resolver needed to transform classpath URL to native java classpath library, in non classic environments such as
                    OSGI
        
        
        If unset null, no resolver is used
                resourcePath (String): the parent path of resources in classpath
                resourcePattern (Pattern): the pattern that must match file names of resources
        
            Also see:
                :class:`~fr.cnes.sirius.addons.patriusdataset.URLResolver`
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def addResourcesFromPatriusDataset(classLoader: java.lang.ClassLoader, uRLResolver: typing.Union['URLResolver', typing.Callable], string: str, pattern: java.util.regex.Pattern) -> None: ...

class ResourceList:
    """
    public final class ResourceList extends Object
    
        Helper class that get a list resources available in the classpath
    """
    FALLBACK_RESOURCES_LIST_PATH: typing.ClassVar[str] = ...
    """
    public static String FALLBACK_RESOURCES_LIST_PATH
    
    
    """
    @staticmethod
    def getResources(classLoader: java.lang.ClassLoader, uRL: java.net.URL, string: str, pattern: java.util.regex.Pattern) -> java.util.List[str]: ...
    @staticmethod
    def getResourcesArray(classLoader: java.lang.ClassLoader, uRLResolver: typing.Union['URLResolver', typing.Callable], string: str, pattern: java.util.regex.Pattern) -> typing.MutableSequence[str]: ...
    @typing.overload
    @staticmethod
    def getResourcesFromDirectory(file: typing.Union[java.io.File, jpype.protocol.SupportsPath], string: str, pattern: java.util.regex.Pattern) -> java.util.List[str]: ...
    @typing.overload
    @staticmethod
    def getResourcesFromDirectory(file: typing.Union[java.io.File, jpype.protocol.SupportsPath], pattern: java.util.regex.Pattern, int: int) -> java.util.List[str]: ...
    @staticmethod
    def getResourcesFromJarFile(file: typing.Union[java.io.File, jpype.protocol.SupportsPath], string: str, pattern: java.util.regex.Pattern) -> java.util.List[str]: ...
    @staticmethod
    def getResourcesList(classLoader: java.lang.ClassLoader, uRLResolver: typing.Union['URLResolver', typing.Callable], string: str, pattern: java.util.regex.Pattern) -> java.util.List[str]: ...

class URLResolver:
    """
    public interface URLResolver
    
        interface for URL resolver
    """
    def resolve(self, uRL: java.net.URL) -> java.net.URL: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.addons.patriusdataset")``.

    PatriusDataset: typing.Type[PatriusDataset]
    ResourceList: typing.Type[ResourceList]
    URLResolver: typing.Type[URLResolver]
    atmosphere: fr.cnes.sirius.addons.patriusdataset.atmosphere.__module_protocol__
    ephemerides: fr.cnes.sirius.addons.patriusdataset.ephemerides.__module_protocol__
    force-models: fr.cnes.sirius.addons.patriusdataset.force-models.__module_protocol__
