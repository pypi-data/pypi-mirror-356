
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.forces.atmospheres.solarActivity
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import typing



class AbstractIonosphericCorrectionFactory:
    """
    public abstract class AbstractIonosphericCorrectionFactory extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Ionospheric correction model factory.
    
        This class can initialize and store in cache
        :class:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.IonosphericCorrection` correction models.
    
        The ionospheric corrections models are organized within a `null
        <http://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ConcurrentHashMap.html?is-external=true>` to assure
        multi-thread usage safety.
    """
    def __init__(self): ...
    def getIonoCorrection(self, topocentricFrame: fr.cnes.sirius.patrius.frames.TopocentricFrame) -> 'IonosphericCorrection':
        """
            Getter for an ionospheric correction model.
        
            This method looks if the asking model is already initialized.
        
        
            If it's the case the model is directly returned, otherwise the model is initialized, stored and returned.
        
            Parameters:
                topoFrame (:class:`~fr.cnes.sirius.patrius.frames.TopocentricFrame`): Topocentric frame associated to the ionospheric correction
        
            Returns:
                the ionospheric correction model
        
        
        """
        ...

class IonosphericCorrection(fr.cnes.sirius.patrius.math.parameter.IParameterizable):
    """
    public interface IonosphericCorrection extends :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
    
        Interface for all the signal propagation corrections due to the ionosphere : computation of the electronic content.
    
        Since:
            1.3
    """
    def computeSignalDelay(self, double: float, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float:
        """
            Compute the derivative value with respect to the input parameter.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the current date
                satellite (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the satellite position
                satFrame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the satellite position frame
        
            Returns:
                the derivative value
        
        
        """
        ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Tell if the function is differentiable by the given parameter.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): function parameter
        
            Returns:
                true if the function is differentiable by the given parameter.
        
        
        """
        ...

class R12Provider(java.io.Serializable):
    """
    public interface R12Provider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        R12 value provider for the Bent model.
    
        Since:
            1.3
    """
    def getR12(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...

class USKProvider(java.io.Serializable):
    """
    public interface USKProvider extends `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Interface for the providers of USK data for the Bent ionospheric correction.
    
        Since:
            1.3
    """
    def getData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> 'USKData': ...

class USKData: ...

class BentModel(IonosphericCorrection):
    """
    public class BentModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.IonosphericCorrection`
    
        Bent model for the electronic content used in ionospheric corrections. This class was directly lifted from FORTRAN 90
        code. For debugging ease reasons, and for lack of knowlegde on the original code, the ported code is as close as
        possible to the original, which means it's rather unreadable as it is.
    
        This class is restricted to be used with :class:`~fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape`.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.IonosphericCorrection`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, r12Provider: typing.Union[R12Provider, typing.Callable], solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider, uSKProvider: typing.Union[USKProvider, typing.Callable], ellipsoidBodyShape: fr.cnes.sirius.patrius.bodies.EllipsoidBodyShape, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, r12Provider: typing.Union[R12Provider, typing.Callable], solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider, uSKProvider: typing.Union[USKProvider, typing.Callable], topocentricFrame: fr.cnes.sirius.patrius.frames.TopocentricFrame): ...
    def computeElectronicCont(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def computeSignalDelay(self, double: float, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float: ...
    def derivativeValue(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame) -> float:
        """
            Compute the derivative value with respect to the input parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.IonosphericCorrection.derivativeValue` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.IonosphericCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): the current date
                satellite (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the satellite position
                satFrame (:class:`~fr.cnes.sirius.patrius.frames.Frame`): the satellite position frame
        
            Returns:
                the derivative value
        
        
        """
        ...
    def getParameters(self) -> java.util.ArrayList[fr.cnes.sirius.patrius.math.parameter.Parameter]: ...
    def isDifferentiableBy(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Tell if the function is differentiable by the given parameter.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.IonosphericCorrection.isDifferentiableBy` in
                interface :class:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.IonosphericCorrection`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): function parameter
        
            Returns:
                true if the function is differentiable by the given parameter.
        
        
        """
        ...
    def supportsParameter(self, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter) -> bool:
        """
            Check if a parameter is supported.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable.supportsParameter` in
                interface :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
        
            Parameters:
                param (:class:`~fr.cnes.sirius.patrius.math.parameter.Parameter`): parameter to check
        
            Returns:
                true if the parameter is supported
        
        
        """
        ...

class BentModelFactory(AbstractIonosphericCorrectionFactory):
    """
    public class BentModelFactory extends :class:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.AbstractIonosphericCorrectionFactory`
    
        This class describes the ionospheric correction factory around the
        :class:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.BentModel`.
    """
    def __init__(self, r12Provider: typing.Union[R12Provider, typing.Callable], solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider, uSKProvider: typing.Union[USKProvider, typing.Callable]): ...

class R12Loader(R12Provider, fr.cnes.sirius.patrius.data.DataLoader):
    """
    public final class R12Loader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.R12Provider`, :class:`~fr.cnes.sirius.patrius.data.DataLoader`
    
        Data loader for the R12 values.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str): ...
    def getR12(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
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

class USKLoader(USKProvider, fr.cnes.sirius.patrius.data.DataLoader):
    """
    public final class USKLoader extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.signalpropagation.ionosphere.USKProvider`, :class:`~fr.cnes.sirius.patrius.data.DataLoader`
    
        Reader for the USK data file (file of the "NEWUSK" type). Note : the code is ported from Fortran and not optimized.
        Since the file is not big, and its format is not meant to change often, it was decided an optimization pass was not
        needed.
    
        Since:
            1.3
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str): ...
    def getData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float) -> USKData: ...
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


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.signalpropagation.ionosphere")``.

    AbstractIonosphericCorrectionFactory: typing.Type[AbstractIonosphericCorrectionFactory]
    BentModel: typing.Type[BentModel]
    BentModelFactory: typing.Type[BentModelFactory]
    IonosphericCorrection: typing.Type[IonosphericCorrection]
    R12Loader: typing.Type[R12Loader]
    R12Provider: typing.Type[R12Provider]
    USKData: typing.Type[USKData]
    USKLoader: typing.Type[USKLoader]
    USKProvider: typing.Type[USKProvider]
