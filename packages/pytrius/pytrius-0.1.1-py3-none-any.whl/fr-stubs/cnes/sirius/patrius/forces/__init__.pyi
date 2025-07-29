
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.forces.atmospheres
import fr.cnes.sirius.patrius.forces.atmospheres.solarActivity
import fr.cnes.sirius.patrius.forces.drag
import fr.cnes.sirius.patrius.forces.gravity
import fr.cnes.sirius.patrius.forces.gravity.tides
import fr.cnes.sirius.patrius.forces.maneuvers
import fr.cnes.sirius.patrius.forces.radiation
import fr.cnes.sirius.patrius.forces.relativistic
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.time
import java.util
import jpype
import typing



class ForceModel(fr.cnes.sirius.patrius.math.parameter.IParameterizable):
    """
    public interface ForceModel extends :class:`~fr.cnes.sirius.patrius.math.parameter.IParameterizable`
    
        This interface represents a force modifying spacecraft motion.
    
        Objects implementing this interface are intended to be added to a
        :class:`~fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator` before the propagation is started.
    
        The propagator will call at each step the :meth:`~fr.cnes.sirius.patrius.forces.ForceModel.addContribution` method. The
        force model instance will extract all the state data it needs (date,position, velocity, frame, attitude, mass) from the
        first parameter. From these state data, it will compute the perturbing acceleration. It will then add this acceleration
        to the second parameter which will take thins contribution into account and will use the Gauss equations to evaluate its
        impact on the global state derivative.
    
        Force models which create discontinuous acceleration patterns (typically for maneuvers start/stop or solar eclipses
        entry/exit) must provide one or more :class:`~fr.cnes.sirius.patrius.events.EventDetector` to the propagator thanks to
        their :meth:`~fr.cnes.sirius.patrius.forces.ForceModel.getEventsDetectors` method. This method is called once just
        before propagation starts. The events states will be checked by the propagator to ensure accurate propagation and proper
        events handling.
    """
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getEventsDetectors(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.events.EventDetector]:
        """
            Get the discrete events related to the model.
        
            Returns:
                array of events detectors or null if the model is not related to any discrete events
        
        
        """
        ...

class ForceModelsData:
    """
    public class ForceModelsData extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class gathering force models in one single class. This class be used then to configure a propagator and modify/retrieve
        forces one by one.
    
        Since:
            4.1
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, forceModel: ForceModel, solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider, solarRadiationPressure: fr.cnes.sirius.patrius.forces.radiation.SolarRadiationPressure, rediffusedRadiationPressure: fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationPressure, thirdBodyAttraction: fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction, thirdBodyAttraction2: fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction, thirdBodyAttraction3: fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction, thirdBodyAttraction4: fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction, thirdBodyAttraction5: fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction, oceanTides: fr.cnes.sirius.patrius.forces.gravity.tides.OceanTides, terrestrialTides: fr.cnes.sirius.patrius.forces.gravity.tides.TerrestrialTides, dragForce: fr.cnes.sirius.patrius.forces.drag.DragForce, coriolisRelativisticEffect: fr.cnes.sirius.patrius.forces.relativistic.CoriolisRelativisticEffect, lenseThirringRelativisticEffect: fr.cnes.sirius.patrius.forces.relativistic.LenseThirringRelativisticEffect, schwarzschildRelativisticEffect: fr.cnes.sirius.patrius.forces.relativistic.SchwarzschildRelativisticEffect): ...
    def getCoriolisRelativisticEffect(self) -> fr.cnes.sirius.patrius.forces.relativistic.CoriolisRelativisticEffect:
        """
        
            Returns:
                the Coriolis relativistic effect
        
        
        """
        ...
    def getDragForce(self) -> fr.cnes.sirius.patrius.forces.drag.DragForce:
        """
        
            Returns:
                the drag force
        
        
        """
        ...
    def getEarthPotentialAttractionModel(self) -> ForceModel:
        """
        
            Returns:
                the Earth potential model
        
        
        """
        ...
    def getForceModelsList(self) -> java.util.List[ForceModel]: ...
    def getJupiterThirdBodyAttraction(self) -> fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction:
        """
        
            Returns:
                the Jupiter attraction
        
        
        """
        ...
    def getLenseThirringRelativisticEffect(self) -> fr.cnes.sirius.patrius.forces.relativistic.LenseThirringRelativisticEffect:
        """
        
            Returns:
                the Lense Thirring relativistic effect
        
        
        """
        ...
    def getMarsThirdBodyAttraction(self) -> fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction:
        """
        
            Returns:
                the Mars attraction
        
        
        """
        ...
    def getMoonThirdBodyAttraction(self) -> fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction:
        """
        
            Returns:
                the Moon attraction
        
        
        """
        ...
    def getOceanTides(self) -> fr.cnes.sirius.patrius.forces.gravity.tides.OceanTides:
        """
        
            Returns:
                the oceanic tides
        
        
        """
        ...
    def getRediffusedRadiationPressure(self) -> fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationPressure:
        """
        
            Returns:
                the rediffused radiation pressure
        
        
        """
        ...
    def getSchwarzschildRelativisticEffect(self) -> fr.cnes.sirius.patrius.forces.relativistic.SchwarzschildRelativisticEffect:
        """
        
            Returns:
                the Schwarzschild relativistic effect
        
        
        """
        ...
    def getSolarActivityDataProvider(self) -> fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider:
        """
        
            Returns:
                the solar activity data provider
        
        
        """
        ...
    def getSolarRadiationPressure(self) -> fr.cnes.sirius.patrius.forces.radiation.SolarRadiationPressure:
        """
        
            Returns:
                the solar radiation pressure
        
        
        """
        ...
    def getSunThirdBodyAttraction(self) -> fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction:
        """
        
            Returns:
                the Sun attraction
        
        
        """
        ...
    def getTerrestrialTides(self) -> fr.cnes.sirius.patrius.forces.gravity.tides.TerrestrialTides:
        """
        
            Returns:
                the terrestrial tides
        
        
        """
        ...
    def getVenusThirdBodyAttraction(self) -> fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction:
        """
        
            Returns:
                the Venus attraction
        
        
        """
        ...
    def setCoriolisRelativisticEffect(self, coriolisRelativisticEffect: fr.cnes.sirius.patrius.forces.relativistic.CoriolisRelativisticEffect) -> None:
        """
        
            Parameters:
                coriolisRelativisticEffectIn (:class:`~fr.cnes.sirius.patrius.forces.relativistic.CoriolisRelativisticEffect`): the Coriolis relativistic effect to set
        
        
        """
        ...
    def setDragForce(self, dragForce: fr.cnes.sirius.patrius.forces.drag.DragForce) -> None:
        """
        
            Parameters:
                dragForceIn (:class:`~fr.cnes.sirius.patrius.forces.drag.DragForce`): the drag force to set
        
        
        """
        ...
    def setEarthPotentialAttractionModel(self, forceModel: ForceModel) -> None:
        """
        
            Parameters:
                earthPotentialAttractionModelIn (:class:`~fr.cnes.sirius.patrius.forces.ForceModel`): the Earth potential model to set
        
        
        """
        ...
    def setJupiterThirdBodyAttraction(self, thirdBodyAttraction: fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction) -> None:
        """
        
            Parameters:
                jupiterThirdBodyAttractionIn (:class:`~fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction`): the Jupiter attraction to set
        
        
        """
        ...
    def setLenseThirringRelativisticEffect(self, lenseThirringRelativisticEffect: fr.cnes.sirius.patrius.forces.relativistic.LenseThirringRelativisticEffect) -> None:
        """
        
            Parameters:
                lenseThirring (:class:`~fr.cnes.sirius.patrius.forces.relativistic.LenseThirringRelativisticEffect`): the Lense Thirring relativistic effect to set
        
        
        """
        ...
    def setMarsThirdBodyAttraction(self, thirdBodyAttraction: fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction) -> None:
        """
        
            Parameters:
                marsThirdBodyAttractionIn (:class:`~fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction`): the Mars attraction to set
        
        
        """
        ...
    def setMoonThirdBodyAttraction(self, thirdBodyAttraction: fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction) -> None:
        """
        
            Parameters:
                moonThirdBodyAttractionIn (:class:`~fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction`): the Moon attraction to set
        
        
        """
        ...
    def setOceanTides(self, oceanTides: fr.cnes.sirius.patrius.forces.gravity.tides.OceanTides) -> None:
        """
        
            Parameters:
                oceanTidesIn (:class:`~fr.cnes.sirius.patrius.forces.gravity.tides.OceanTides`): the oceanic tides to set
        
        
        """
        ...
    def setRediffusedRadiationPressure(self, rediffusedRadiationPressure: fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationPressure) -> None:
        """
        
            Parameters:
                rediffusedRadiationPressureIn (:class:`~fr.cnes.sirius.patrius.forces.radiation.RediffusedRadiationPressure`): the rediffused radiation pressure to set
        
        
        """
        ...
    def setSchwarzschildRelativisticEffect(self, schwarzschildRelativisticEffect: fr.cnes.sirius.patrius.forces.relativistic.SchwarzschildRelativisticEffect) -> None:
        """
        
            Parameters:
                schwarzschildRelativistic (:class:`~fr.cnes.sirius.patrius.forces.relativistic.SchwarzschildRelativisticEffect`): the Schwarzschild relativistic effect to set
        
        
        """
        ...
    def setSolarActivityDataProvider(self, solarActivityDataProvider: fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider) -> None:
        """
        
            Parameters:
                solarActivityDataProviderIn (:class:`~fr.cnes.sirius.patrius.forces.atmospheres.solarActivity.SolarActivityDataProvider`): the solar activity data provider to set
        
        
        """
        ...
    def setSolarRadiationPressure(self, solarRadiationPressure: fr.cnes.sirius.patrius.forces.radiation.SolarRadiationPressure) -> None:
        """
        
            Parameters:
                srp (:class:`~fr.cnes.sirius.patrius.forces.radiation.SolarRadiationPressure`): the solar radiation pressure to set
        
        
        """
        ...
    def setSunThirdBodyAttraction(self, thirdBodyAttraction: fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction) -> None:
        """
        
            Parameters:
                sunThirdBodyAttractionIn (:class:`~fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction`): the Sun attraction to set
        
        
        """
        ...
    def setTerrestrialTides(self, terrestrialTides: fr.cnes.sirius.patrius.forces.gravity.tides.TerrestrialTides) -> None:
        """
        
            Parameters:
                terrestrialTidesIn (:class:`~fr.cnes.sirius.patrius.forces.gravity.tides.TerrestrialTides`): the terrestrial tides to set
        
        
        """
        ...
    def setVenusThirdBodyAttraction(self, thirdBodyAttraction: fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction) -> None:
        """
        
            Parameters:
                venusThirdBodyAttractionIn (:class:`~fr.cnes.sirius.patrius.forces.gravity.ThirdBodyAttraction`): the Venus attraction to set
        
        
        """
        ...
    def updateAssembly(self, assembly: fr.cnes.sirius.patrius.assembly.Assembly) -> None: ...

class GradientModel:
    """
    public interface GradientModel
    
        Interface for gradient model.
    
        Gradient model provide information on partial derivatives computation.
    """
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def computeGradientVelocity(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to velocity have to be computed.
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...

class EmpiricalForce(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable, ForceModel, GradientModel):
    AX_COEFFICIENT: typing.ClassVar[str] = ...
    AY_COEFFICIENT: typing.ClassVar[str] = ...
    AZ_COEFFICIENT: typing.ClassVar[str] = ...
    BX_COEFFICIENT: typing.ClassVar[str] = ...
    BY_COEFFICIENT: typing.ClassVar[str] = ...
    BZ_COEFFICIENT: typing.ClassVar[str] = ...
    CX_COEFFICIENT: typing.ClassVar[str] = ...
    CY_COEFFICIENT: typing.ClassVar[str] = ...
    CZ_COEFFICIENT: typing.ClassVar[str] = ...
    @typing.overload
    def __init__(self, int: int, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D4: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, int: int, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D2: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D3: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, vector3D4: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, lOFType: fr.cnes.sirius.patrius.frames.LOFType): ...
    @typing.overload
    def __init__(self, int: int, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction2: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction3: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction4: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction5: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction6: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction7: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction8: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction9: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, int: int, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction2: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction3: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction4: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction5: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction6: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction7: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction8: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction9: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, lOFType: fr.cnes.sirius.patrius.frames.LOFType): ...
    @typing.overload
    def __init__(self, int: int, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter4: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter5: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter6: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter7: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter8: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter9: fr.cnes.sirius.patrius.math.parameter.Parameter, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, int: int, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter4: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter5: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter6: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter7: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter8: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter9: fr.cnes.sirius.patrius.math.parameter.Parameter, lOFType: fr.cnes.sirius.patrius.frames.LOFType): ...
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    @typing.overload
    def computeAcceleration(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, localOrbitalFrame: fr.cnes.sirius.patrius.frames.LocalOrbitalFrame, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    @typing.overload
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeCosSin(self, pVCoordinates: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinates, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> typing.MutableSequence[float]: ...
    def computeGradientPosition(self) -> bool: ...
    def computeGradientVelocity(self) -> bool: ...
    def getAx(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction: ...
    def getAy(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction: ...
    def getAz(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction: ...
    def getBx(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction: ...
    def getBy(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction: ...
    def getBz(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction: ...
    def getCx(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction: ...
    def getCy(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction: ...
    def getCz(self) -> fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction: ...
    def getEventsDetectors(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.events.EventDetector]: ...
    def getLocalFrame(self) -> fr.cnes.sirius.patrius.frames.Frame: ...
    def getVectorS(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces")``.

    EmpiricalForce: typing.Type[EmpiricalForce]
    ForceModel: typing.Type[ForceModel]
    ForceModelsData: typing.Type[ForceModelsData]
    GradientModel: typing.Type[GradientModel]
    atmospheres: fr.cnes.sirius.patrius.forces.atmospheres.__module_protocol__
    drag: fr.cnes.sirius.patrius.forces.drag.__module_protocol__
    gravity: fr.cnes.sirius.patrius.forces.gravity.__module_protocol__
    maneuvers: fr.cnes.sirius.patrius.forces.maneuvers.__module_protocol__
    radiation: fr.cnes.sirius.patrius.forces.radiation.__module_protocol__
    relativistic: fr.cnes.sirius.patrius.forces.relativistic.__module_protocol__
