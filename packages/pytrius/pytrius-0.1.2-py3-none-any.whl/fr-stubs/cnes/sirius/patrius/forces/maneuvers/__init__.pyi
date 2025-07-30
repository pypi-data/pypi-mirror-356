
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly.properties
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.forces
import fr.cnes.sirius.patrius.forces.maneuvers.orbman
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.parameter
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.propagation.analytical
import fr.cnes.sirius.patrius.propagation.numerical
import fr.cnes.sirius.patrius.propagation.sampling
import fr.cnes.sirius.patrius.time
import java.io
import java.util
import jpype
import typing



class ConstantThrustError(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable, fr.cnes.sirius.patrius.forces.ForceModel, fr.cnes.sirius.patrius.forces.GradientModel):
    """
    public final class ConstantThrustError extends :class:`~fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
    
    
        This class is a model of the error of a simple maneuver with constant thrust.
    
        The architecture of this force model is similar to ConstantThrustManeuver class.
    
        The maneuver is associated to two triggering :class:`~fr.cnes.sirius.patrius.events.EventDetector` (one to start the
        thrust, the other one to stop the thrust): the maneuver is triggered **only if** the underlying event generates a
        :meth:`~fr.cnes.sirius.patrius.events.EventDetector.Action.STOP` event, in which case this class will generate a
        :meth:`~fr.cnes.sirius.patrius.events.EventDetector.Action.RESET_STATE` event (the stop event from the underlying object
        is therefore filtered out).
    
        Since:
            2.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, frame: fr.cnes.sirius.patrius.frames.Frame, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction2: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction3: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, lOFType: fr.cnes.sirius.patrius.frames.LOFType, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction2: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction3: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, lOFType: fr.cnes.sirius.patrius.frames.LOFType, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction2: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction3: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, frame: fr.cnes.sirius.patrius.frames.Frame, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, frame: fr.cnes.sirius.patrius.frames.Frame, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, frame: fr.cnes.sirius.patrius.frames.Frame, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction2: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction3: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, frame: fr.cnes.sirius.patrius.frames.Frame, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter4: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter5: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter6: fr.cnes.sirius.patrius.math.parameter.Parameter, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, lOFType: fr.cnes.sirius.patrius.frames.LOFType, double2: float, double3: float, double4: float): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, lOFType: fr.cnes.sirius.patrius.frames.LOFType, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, lOFType: fr.cnes.sirius.patrius.frames.LOFType, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction2: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction3: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, lOFType: fr.cnes.sirius.patrius.frames.LOFType, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, lOFType: fr.cnes.sirius.patrius.frames.LOFType, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter4: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter5: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter6: fr.cnes.sirius.patrius.math.parameter.Parameter, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, iParamDiffFunction: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction2: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction, iParamDiffFunction3: fr.cnes.sirius.patrius.math.parameter.IParamDiffFunction): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter2: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter3: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter4: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter5: fr.cnes.sirius.patrius.math.parameter.Parameter, parameter6: fr.cnes.sirius.patrius.math.parameter.Parameter, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientPosition` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def computeGradientVelocity(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to velocity have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientVelocity` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def getEndDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Return the maneuver stop date (if a date or a :class:`~fr.cnes.sirius.patrius.events.detectors.DateDetector` as been
            provided).
        
            Returns:
                the maneuver stop date if a date or a :class:`~fr.cnes.sirius.patrius.events.detectors.DateDetector` as been provided,
                null otherwise.
        
        
        """
        ...
    def getEventsDetectors(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.events.EventDetector]:
        """
            Get the discrete events related to the model.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.ForceModel.getEventsDetectors` in
                interface :class:`~fr.cnes.sirius.patrius.forces.ForceModel`
        
            Returns:
                array of events detectors or null if the model is not related to any discrete events
        
        
        """
        ...
    def getStartDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Return the maneuver start date (if a date or a :class:`~fr.cnes.sirius.patrius.events.detectors.DateDetector` as been
            provided).
        
            Returns:
                the maneuver start date if a date or a :class:`~fr.cnes.sirius.patrius.events.detectors.DateDetector` as been provided,
                null otherwise.
        
        
        """
        ...
    def isFiring(self) -> bool:
        """
            Returns maneuver status (firing or not).
        
            Used in conjunction with :meth:`~fr.cnes.sirius.patrius.forces.maneuvers.ConstantThrustError.setFiring`, the user can
            stop/restart a propagation during a maneuver.
        
            Returns:
                true if maneuver is thrust firing.
        
        
        """
        ...
    def setFiring(self, boolean: bool) -> None:
        """
            Set maneuver status. This method is meant to be used if the propagation starts during a maneuver. As a result thrust
            will be firing at the beginning of the propagation and stops when crossing stop event.
        
            Used in conjunction with :meth:`~fr.cnes.sirius.patrius.forces.maneuvers.ConstantThrustError.isFiring`, the user can
            stop/restart a propagation during a maneuver.
        
            Parameters:
                isFiring (boolean): true if propagation should start during the maneuver
        
        
        """
        ...

class GatesModel:
    """
    public class GatesModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class implements a variation of the model proposed by C.R. Gates to represent the uncertainty on a maneuver's
        magnitude and direction.
    
        The model implemented here differs from the one proposed by Gates in a few ways. Although no mention of it is made in
        the paper, the formulation proposed by Gates seems to rely on the small angles hypothesis. This is not the case of the
        formulation used here. In addition, this class only implements the shutoff error and the pointing error, that is, the
        errors on the maneuver's magnitude and direction which are proportional to ΔV. The uncertainty on the maneuver's
        direction is modeled as a spherical Gaussian distribution around the ΔV vector, while the uncertainty on the maneuver's
        magnitude is assumed to follow an uncorrelated Gaussian distribution.
    
        Note that although the uncertainty on the maneuver's magnitude and direction is defined using the target ΔV vector, the
        latter is generally not the mean of the distribution (this is only the case if there is no uncertainty on the maneuver's
        direction). The mean perturbed maneuver can be computed using
        :meth:`~fr.cnes.sirius.patrius.forces.maneuvers.GatesModel.getMeanDeltaV` or
        :meth:`~fr.cnes.sirius.patrius.forces.maneuvers.GatesModel.getMeanDeltaV`.
    
        **See:**
    
    
        *A Simplified Model of Midcourse Maneuver Execution Errors*
    
    
        by C.R. Gates
    
    
        Technical Report n°32-504, October 15, 1963
    
    
        Jet Propulsion Laboratory (JPL)
    
    
        California Institute of Technology, Pasadena, California.
    
        Since:
            4.7
    """
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def getCovarianceMatrix3x3(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.linear.SymmetricMatrix:
        """
            Computes the covariance matrix modeling the uncertainty on a maneuver's magnitude and direction.
        
            This methods assumes the uncertainty on the maneuver's direction follows a spherical Gaussian distribution around the
            provided ΔV vector. The uncertainty on the maneuver's magnitude is assumed to follow an uncorrelated Gaussian
            distribution. Both uncertainties are proportional to the norm of ΔV.
        
            Parameters:
                deltaV (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the maneuver's ΔV (in any frame)
        
            Returns:
                a 3-by-3 covariance matrix modeling the uncertainty on the maneuver's magnitude and direction (in the same frame as ΔV)
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the norm of the provided ΔV vector is close to zero (<:meth:`~fr.cnes.sirius.patrius.math.util.Precision.EPSILON`),
                    but not exactly equal to zero
        
            Computes the covariance matrix modeling the uncertainty on a maneuver's magnitude and direction.
        
            This methods assumes the uncertainty on the maneuver's direction follows a spherical Gaussian distribution around the
            provided ΔV vector. The uncertainty on the maneuver's magnitude is assumed to follow an uncorrelated Gaussian
            distribution. Both uncertainties are proportional to the norm of ΔV.
        
            Parameters:
                deltaV (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the maneuver's ΔV (in any frame)
                sigmaMagnitude (double): the standard deviation on the magnitude (in percents)
                sigmaDirection (double): the standard deviation on the direction (in radians)
        
            Returns:
                a 3-by-3 covariance matrix modeling the uncertainty on the maneuver's magnitude and direction (in the same frame as ΔV)
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the norm of the provided ΔV vector is close to zero (<:meth:`~fr.cnes.sirius.patrius.math.util.Precision.EPSILON`),
                    but not exactly equal to zero
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getCovarianceMatrix3x3(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, double2: float) -> fr.cnes.sirius.patrius.math.linear.SymmetricMatrix: ...
    @typing.overload
    def getCovarianceMatrix6x6(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.linear.SymmetricMatrix:
        """
            Computes the covariance matrix modeling the uncertainty on an object's position and velocity induced by the uncertainty
            on a maneuver's magnitude and direction.
        
            This methods assumes the uncertainty on the maneuver's direction follows a spherical Gaussian distribution around the
            provided ΔV vector. The uncertainty on the maneuver's magnitude is assumed to follow an uncorrelated Gaussian
            distribution. Both uncertainties are proportional to the norm of ΔV.
        
            Parameters:
                deltaV (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the maneuver's ΔV (in any frame)
        
            Returns:
                a 6-by-6 covariance matrix modeling the uncertainty on an object's position and velocity induced by the uncertainty on
                the maneuver's magnitude and direction (in the same frame as ΔV)
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the norm of the provided ΔV vector is close to zero (<:meth:`~fr.cnes.sirius.patrius.math.util.Precision.EPSILON`),
                    but not exactly equal to zero
        
            Computes the covariance matrix modeling the uncertainty on an object's position and velocity induced by the uncertainty
            on a maneuver's magnitude and direction.
        
            This methods assumes the uncertainty on the maneuver's direction follows a spherical Gaussian distribution around the
            provided ΔV vector. The uncertainty on the maneuver's magnitude is assumed to follow an uncorrelated Gaussian
            distribution. Both uncertainties are proportional to the norm of ΔV.
        
            Parameters:
                deltaV (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the maneuver's ΔV (in any frame)
                sigmaMagnitude (double): the standard deviation on the magnitude (in percents)
                sigmaDirection (double): the standard deviation on the direction (in radians)
        
            Returns:
                a 6-by-6 covariance matrix modeling the uncertainty on an object's position and velocity induced by the uncertainty on
                the maneuver's magnitude and direction (in the same frame as ΔV)
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the norm of the provided ΔV vector is close to zero (<:meth:`~fr.cnes.sirius.patrius.math.util.Precision.EPSILON`),
                    but not exactly equal to zero
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getCovarianceMatrix6x6(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, double2: float) -> fr.cnes.sirius.patrius.math.linear.SymmetricMatrix: ...
    @typing.overload
    def getMeanDeltaV(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Computes the mean ΔV vector of the distribution modeling the uncertainty on a maneuver's magnitude and direction.
        
            This methods assumes the uncertainty on the maneuver's direction follows a spherical Gaussian distribution around the
            provided ΔV vector. The uncertainty on the maneuver's magnitude is assumed to follow an uncorrelated Gaussian
            distribution. Both uncertainties are proportional to the norm of ΔV.
        
            Parameters:
                deltaV (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the maneuver's ΔV (in any frame)
        
            Returns:
                the mean ΔV vector of the distribution modeling the uncertainty on a maneuver's magnitude and direction.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the norm of the provided ΔV vector is close to zero (<:meth:`~fr.cnes.sirius.patrius.math.util.Precision.EPSILON`),
                    but not exactly equal to zero
        
            Computes the mean ΔV vector of the distribution modeling the uncertainty on a maneuver's magnitude and direction.
        
            This methods assumes the uncertainty on the maneuver's direction follows a spherical Gaussian distribution around the
            provided ΔV vector. The uncertainty on the maneuver's magnitude is assumed to follow an uncorrelated Gaussian
            distribution. Both uncertainties are proportional to the norm of ΔV.
        
            Parameters:
                deltaV (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the maneuver's ΔV (in any frame)
                sigmaDirection (double): the standard deviation on the direction (in radians)
        
            Returns:
                the mean ΔV vector of the distribution modeling the uncertainty on a maneuver's magnitude and direction
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathArithmeticException`: if the norm of the provided ΔV vector is close to zero (<:meth:`~fr.cnes.sirius.patrius.math.util.Precision.EPSILON`),
                    but not exactly equal to zero
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def getMeanDeltaV(vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def getSigmaDirection(self) -> float:
        """
            Gets the standard deviation σ :sub:`D` on the direction (in radians).
        
            This parameter defines the pointing error, which is orthogonal to ΔV and proportional to its norm.
        
        
            Such an error would result from imperfect angular orientation of the thrust vector.
        
            Returns:
                the standard deviation on the direction (in radians)
        
        
        """
        ...
    def getSigmaMagnitude(self) -> float:
        """
            Gets the standard deviation σ :sub:`M` on the magnitude (in percent).
        
            This parameter defines the shutoff error, which is in the direction of ΔV and is proportional to its norm.
        
        
            Such an error would result from scale-factor errors in the shutoff system.
        
            Returns:
                the standard deviation on the magnitude (in percent)
        
        
        """
        ...

class Maneuver:
    """
    public interface Maneuver
    
        Interface for maneuvers.
    
        Since:
            4.1
    """
    ...

class ManeuversSequence:
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def add(self, continuousThrustManeuver: 'ContinuousThrustManeuver') -> bool: ...
    @typing.overload
    def add(self, impulseManeuver: 'ImpulseManeuver') -> bool: ...
    def applyTo(self, numericalPropagator: fr.cnes.sirius.patrius.propagation.numerical.NumericalPropagator) -> None: ...
    def getConstraintContinuous(self) -> float: ...
    def getConstraintImpulsive(self) -> float: ...
    def getContinueManeuversList(self) -> java.util.Set['ContinuousThrustManeuver']: ...
    def getImpulseManeuversList(self) -> java.util.Set['ImpulseManeuver']: ...
    def getManeuversList(self) -> java.util.List[Maneuver]: ...
    def getSize(self) -> int: ...
    @typing.overload
    def remove(self, continuousThrustManeuver: 'ContinuousThrustManeuver') -> bool: ...
    @typing.overload
    def remove(self, impulseManeuver: 'ImpulseManeuver') -> bool: ...

class SmallManeuverAnalyticalModel(fr.cnes.sirius.patrius.propagation.analytical.AdapterPropagator.DifferentialEffect, java.io.Serializable):
    """
    public class SmallManeuverAnalyticalModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.propagation.analytical.AdapterPropagator.DifferentialEffect`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Analytical model for small maneuvers.
    
        The aim of this model is to compute quickly the effect at date t :sub:`1` of a small maneuver performed at an earlier
        date t :sub:`0` . Both the direct effect of the maneuver and the Jacobian of this effect with respect to maneuver
        parameters are available.
    
        These effect are computed analytically using two Jacobian matrices:
    
          1.  J :sub:`0` : Jacobian of Keplerian or equinoctial elements with respect to cartesian parameters at date t :sub:`0`
          2.  J :sub:`1/0` : Jacobian of Keplerian or equinoctial elements at date t :sub:`1` with respect to Keplerian or equinoctial
            elements at date t :sub:`0`
    
    
        The second Jacobian, J :sub:`1/0` , is computed using a simple Keplerian model, i.e. it is the identity except for the
        mean motion row which also includes an off-diagonal element due to semi-major axis change.
    
        The orbital elements change at date t :sub:`1` can be added to orbital elements extracted from state, and the final
        elements taking account the changes are then converted back to appropriate type, which may be different from Keplerian
        or equinoctial elements.
    
        Note that this model takes *only* Keplerian effects into account. This means that using only this class to compute an
        inclination maneuver in Low Earth Orbit will *not* change ascending node drift rate despite inclination has changed (the
        same would be true for a semi-major axis change of course). In order to take this drift into account, an instance of
        :class:`~fr.cnes.sirius.patrius.propagation.analytical.J2DifferentialEffect` must be used together with an instance of
        this class.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, frame: fr.cnes.sirius.patrius.frames.Frame, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, string: str): ...
    @typing.overload
    def __init__(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, string: str): ...
    @typing.overload
    def apply(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit:
        """
            Compute the effect of the maneuver on an orbit.
        
            Parameters:
                orbit1 (:class:`~fr.cnes.sirius.patrius.orbits.Orbit`): original orbit at t :sub:`1` , without maneuver
        
            Returns:
                orbit at t :sub:`1` , taking the maneuver into account if t :sub:`1` > t :sub:`0`
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.forces.maneuvers.SmallManeuverAnalyticalModel.apply`, null
        
        public :class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState` apply(:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState` state1) throws :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`
        
            Compute the effect of the maneuver on a spacecraft state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.analytical.AdapterPropagator.DifferentialEffect.apply` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.analytical.AdapterPropagator.DifferentialEffect`
        
            Parameters:
                state1 (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): original spacecraft state at t :sub:`1` , without maneuver
        
            Returns:
                spacecraft state at t :sub:`1` , taking the maneuver into account if t :sub:`1` > t :sub:`0`
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.utils.exception.PatriusException`: if no attitude information is defined
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.forces.maneuvers.SmallManeuverAnalyticalModel.apply`, null
        
        
        """
        ...
    @typing.overload
    def apply(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def getDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date of the maneuver.
        
            Returns:
                date of the maneuver
        
        
        """
        ...
    def getInertialDV(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the inertial velocity increment of the maneuver.
        
            Returns:
                velocity increment in a state-dependent inertial frame
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.forces.maneuvers.SmallManeuverAnalyticalModel.getInertialFrame`
        
        
        """
        ...
    def getInertialFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the inertial frame in which the velocity increment is defined.
        
            Returns:
                inertial frame in which the velocity increment is defined
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.forces.maneuvers.SmallManeuverAnalyticalModel.getInertialDV`
        
        
        """
        ...
    def getJacobian(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit, positionAngle: fr.cnes.sirius.patrius.orbits.PositionAngle, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def updateMass(self, double: float) -> float:
        """
            Update a spacecraft mass due to maneuver.
        
            Parameters:
                mass (double): masse before maneuver
        
            Returns:
                mass after maneuver
        
        
        """
        ...

class ContinuousThrustManeuver(fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable, fr.cnes.sirius.patrius.forces.ForceModel, fr.cnes.sirius.patrius.forces.GradientModel, Maneuver, fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler):
    """
    public class ContinuousThrustManeuver extends :class:`~fr.cnes.sirius.patrius.math.parameter.JacobiansParameterizable` implements :class:`~fr.cnes.sirius.patrius.forces.ForceModel`, :class:`~fr.cnes.sirius.patrius.forces.GradientModel`, :class:`~fr.cnes.sirius.patrius.forces.maneuvers.Maneuver`, :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler`
    
        This class implements a thrust (constant or variable).
    
        The maneuver is defined by a direction in satellite frame or in a frame defined by user or in a LOF with type defined by
        user. In first case, the current attitude of the spacecraft, defined by the current spacecraft state, will be used to
        convert the thrust inDirection in satellite frame into inertial frame when inDirection is defined in satellite frame. A
        typical case for tangential maneuvers is to use a :class:`~fr.cnes.sirius.patrius.attitudes.LofOffset` attitude provider
        for state propagation and a velocity increment along the +X satellite axis.
    
        The implementation of this class enables the computation of partial derivatives by finite differences with respect to
        **thrust** and **flow rate** if they have been defined as constant (partial derivatives are not available if parameters
        are not constant).
    
        The maneuver is associated to two triggering :class:`~fr.cnes.sirius.patrius.events.EventDetector` (one to start the
        thrust, the other one to stop the thrust): the maneuver is triggered **only if** the underlying event generates a
        :meth:`~fr.cnes.sirius.patrius.events.EventDetector.Action.STOP` event, in which case this class will generate a
        :meth:`~fr.cnes.sirius.patrius.events.EventDetector.Action.RESET_STATE` event (the stop event from the underlying object
        is therefore filtered out).
    
        Note: including this force in a numerical propagator with adaptive step-size integrator may require to set up a small
        lower bound for step-size (such as 1E-8s) since force discontinuity may cause difficulties to the integrator when the
        maneuver stops.
    
        Warning: if variable ISP and thrust are used (using
        :class:`~fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty`), ISP and thrust parameters cannot be used (set
        as NaN) and partial derivatives cannot be computed.
    
        Also see:
            :meth:`~serialized`
    """
    THRUST: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` THRUST
    
        Parameter name for thrust.
    
        Also see:
            :meth:`~constant`
    
    
    """
    FLOW_RATE: typing.ClassVar[str] = ...
    """
    public static final `String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>` FLOW_RATE
    
        Parameter name for flow rate.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, iDependentVectorVariable: typing.Union[fr.cnes.sirius.patrius.math.analysis.IDependentVectorVariable[fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D]], massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, iDependentVectorVariable: typing.Union[fr.cnes.sirius.patrius.math.analysis.IDependentVectorVariable[fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D]], massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, iDependentVectorVariable: typing.Union[fr.cnes.sirius.patrius.math.analysis.IDependentVectorVariable[fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D]], massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, lOFType: fr.cnes.sirius.patrius.frames.LOFType): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, eventDetector2: fr.cnes.sirius.patrius.events.EventDetector, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, lOFType: fr.cnes.sirius.patrius.frames.LOFType): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, iDependentVectorVariable: typing.Union[fr.cnes.sirius.patrius.math.analysis.IDependentVectorVariable[fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D]], massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, iDependentVectorVariable: typing.Union[fr.cnes.sirius.patrius.math.analysis.IDependentVectorVariable[fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D]], massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, iDependentVectorVariable: typing.Union[fr.cnes.sirius.patrius.math.analysis.IDependentVectorVariable[fr.cnes.sirius.patrius.propagation.SpacecraftState], typing.Callable[[fr.cnes.sirius.patrius.propagation.SpacecraftState], fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D]], massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, lOFType: fr.cnes.sirius.patrius.frames.LOFType): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, frame: fr.cnes.sirius.patrius.frames.Frame): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, lOFType: fr.cnes.sirius.patrius.frames.LOFType): ...
    def addContribution(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, timeDerivativesEquations: fr.cnes.sirius.patrius.propagation.numerical.TimeDerivativesEquations) -> None: ...
    def addDAccDParam(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, parameter: fr.cnes.sirius.patrius.math.parameter.Parameter, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def addDAccDState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None: ...
    def checkData(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None: ...
    def computeAcceleration(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def computeGradientPosition(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to position have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientPosition` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def computeGradientVelocity(self) -> bool:
        """
            This method returns true if the acceleration partial derivatives with respect to velocity have to be computed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.GradientModel.computeGradientVelocity` in
                interface :class:`~fr.cnes.sirius.patrius.forces.GradientModel`
        
            Returns:
                true if the derivatives have to be computed, false otherwise
        
        
        """
        ...
    def getDirection(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the thrust direction.
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the current state information: date, kinematics, attitude. Unused in case of constant maneuver.
        
            Returns:
                the thrust direction.
        
        
        """
        ...
    def getEndDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Return the maneuver stop date (if a date or a :class:`~fr.cnes.sirius.patrius.events.detectors.DateDetector` as been
            provided).
        
            Returns:
                the maneuver stop date if a date or a :class:`~fr.cnes.sirius.patrius.events.detectors.DateDetector` as been provided,
                null otherwise.
        
        
        """
        ...
    def getEventsDetectors(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.events.EventDetector]:
        """
            Get the discrete events related to the model.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.forces.ForceModel.getEventsDetectors` in
                interface :class:`~fr.cnes.sirius.patrius.forces.ForceModel`
        
            Returns:
                array of events detectors or null if the model is not related to any discrete events
        
        
        """
        ...
    def getFlowRate(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Get the flow rate.
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the current state information: date, kinematics, attitude
        
            Returns:
                flow rate (negative, kg/s).
        
        
        """
        ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the frame of the acceleration inDirection. Null if the thrust is expressed in the satellite frame or in a local
            orbital frame.
        
            Returns:
                the frame of the acceleration
        
        
        """
        ...
    @typing.overload
    def getISP(self) -> float:
        """
            Get the specific impulse.
        
            Warning: if a variable ISP has been used, NaN will be returned.
        
            Returns:
                specific impulse (s).
        
        
        """
        ...
    @typing.overload
    def getISP(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Get the specific impulse.
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the current state information: date, kinematics, attitude. Unused in case of constant maneuver.
        
            Returns:
                specific impulse (s).
        
        """
        ...
    def getLofType(self) -> fr.cnes.sirius.patrius.frames.LOFType:
        """
        
            Returns:
                the lofType
        
        
        """
        ...
    def getMassModel(self) -> fr.cnes.sirius.patrius.propagation.MassProvider:
        """
        
            Returns:
                the massModel
        
        
        """
        ...
    def getPropulsiveProperty(self) -> fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty:
        """
            Get the propulsive property.
        
            Returns:
                propulsive property
        
        
        """
        ...
    def getStartDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Return the maneuver start date (if a date or a :class:`~fr.cnes.sirius.patrius.events.detectors.DateDetector` as been
            provided).
        
            Returns:
                the maneuver start date if a date or a :class:`~fr.cnes.sirius.patrius.events.detectors.DateDetector` as been provided,
                null otherwise.
        
        
        """
        ...
    def getTankProperty(self) -> fr.cnes.sirius.patrius.assembly.properties.TankProperty:
        """
            Get the tank property.
        
            Returns:
                tank property
        
        
        """
        ...
    def getThrust(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float:
        """
            Get the thrust.
        
            Parameters:
                s (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): the current state information: date, kinematics, attitude. Unused in case of constant maneuver.
        
            Returns:
                thrust force (N).
        
        
        """
        ...
    def getUsedDV(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the maneuver instantaneous consumption deltaV.
        
            Returns:
                maneuver instantaneous consumption deltaV in maneuver frame (inertial, LOF or satellite)
        
        
        """
        ...
    def handleStep(self, patriusStepInterpolator: fr.cnes.sirius.patrius.propagation.sampling.PatriusStepInterpolator, boolean: bool) -> None: ...
    def init(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Initialize step handler at the start of a propagation.
        
            This method is called once at the start of the propagation. It may be used by the step handler to initialize some
            internal data if needed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler.init` in
                interface :class:`~fr.cnes.sirius.patrius.propagation.sampling.PatriusStepHandler`
        
            Parameters:
                s0 (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): initial state
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): target time for the integration
        
        
        """
        ...
    def isFiring(self) -> bool:
        """
            Returns maneuver status (firing or not).
        
            Used in conjunction with :meth:`~fr.cnes.sirius.patrius.forces.maneuvers.ContinuousThrustManeuver.setFiring`, the user
            can stop/restart a propagation during a maneuver.
        
            Returns:
                true if maneuver is thrust firing.
        
        
        """
        ...
    def setFiring(self, boolean: bool) -> None:
        """
            Set maneuver status. This method is meant to be used if the propagation starts during a maneuver. As a result thrust
            will be firing at the beginning of the propagation and stops when crossing stop event.
        
            Used in conjunction with :meth:`~fr.cnes.sirius.patrius.forces.maneuvers.ContinuousThrustManeuver.isFiring`, the user
            can stop/restart a propagation during a maneuver.
        
            Parameters:
                isFiring (boolean): true if propagation should start during the maneuver
        
        
        """
        ...

class ImpulseManeuver(fr.cnes.sirius.patrius.events.AbstractDetector, Maneuver):
    """
    public class ImpulseManeuver extends :class:`~fr.cnes.sirius.patrius.events.AbstractDetector` implements :class:`~fr.cnes.sirius.patrius.forces.maneuvers.Maneuver`
    
        Impulse maneuver model.
    
        This class implements an impulse maneuver as a discrete event that can be provided to any
        :class:`~fr.cnes.sirius.patrius.propagation.Propagator`.
    
        The impulse maneuver is associated to a triggering :class:`~fr.cnes.sirius.patrius.events.EventDetector`: the maneuver
        is triggered **only if** the underlying event generates a
        :meth:`~fr.cnes.sirius.patrius.events.EventDetector.Action.STOP` event, in which case this class will generate a
        :meth:`~fr.cnes.sirius.patrius.events.EventDetector.Action.RESET_STATE` event (the stop event from the underlying object
        is therefore filtered out). In the simple cases, the underlying event detector may be a basic
        :class:`~fr.cnes.sirius.patrius.events.detectors.DateDetector`, but it can also be a more elaborate
        :class:`~fr.cnes.sirius.patrius.events.detectors.ApsideDetector` for apogee maneuvers for example.
    
        The maneuver is defined by a single velocity increment satellite frame or in a frame defined by user or in a LOF with
        type defined by user. The current attitude of the spacecraft, defined by the current spacecraft state, will be used to
        compute the velocity direction in inertial frame when direction is defined in satellite frame. A typical case for
        tangential maneuvers is to use a :class:`~fr.cnes.sirius.patrius.attitudes.LofOffset` attitude provider for state
        propagation and a velocity increment along the +X satellite axis.
    
        Beware that the triggering event detector must behave properly both before and after maneuver. If for example a node
        detector is used to trigger an inclination maneuver and the maneuver change the orbit to an equatorial one, the node
        detector will fail just after the maneuver, being unable to find a node on an equatorial orbit! This is a real case that
        has been encountered during validation ...
    
        Also see:
            :meth:`~fr.cnes.sirius.patrius.propagation.Propagator.addEventDetector`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, string: str): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, string: str, lOFType: fr.cnes.sirius.patrius.frames.LOFType): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty, lOFType: fr.cnes.sirius.patrius.frames.LOFType): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, double: float, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, string: str): ...
    @typing.overload
    def __init__(self, eventDetector: fr.cnes.sirius.patrius.events.EventDetector, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, frame: fr.cnes.sirius.patrius.frames.Frame, propulsiveProperty: fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty, massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, tankProperty: fr.cnes.sirius.patrius.assembly.properties.TankProperty): ...
    def copy(self) -> 'ImpulseManeuver':
        """
            A copy of the detector. By default copy is deep. If not, detector javadoc will specify which attribute is not fully
            copied. In that case, the attribute reference is passed.
        
            The following attributes are not deeply copied:
        
              - mass: :class:`~fr.cnes.sirius.patrius.propagation.MassProvider`
              - frame: :class:`~fr.cnes.sirius.patrius.frames.Frame`
        
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.copy` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Returns:
                a copy of the detector.
        
        
        """
        ...
    def eventOccurred(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, boolean: bool, boolean2: bool) -> fr.cnes.sirius.patrius.events.EventDetector.Action: ...
    def g(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> float: ...
    def getDeltaVSat(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the velocity increment in satellite frame.
        
            Returns:
                velocity increment in satellite frame
        
        
        """
        ...
    def getFrame(self) -> fr.cnes.sirius.patrius.frames.Frame:
        """
            Get the frame of the velocity increment. Null if the velocity increment is expressed by default in the satellite frame.
        
            Returns:
                the frame
        
        
        """
        ...
    def getIsp(self) -> float:
        """
            Get the specific impulse.
        
            Warning: if a variable ISP has been used, NaN will be returned.
        
            Returns:
                specific impulse
        
        
        """
        ...
    def getLofType(self) -> fr.cnes.sirius.patrius.frames.LOFType:
        """
        
            Returns:
                the lofType
        
        
        """
        ...
    def getMassProvider(self) -> fr.cnes.sirius.patrius.propagation.MassProvider:
        """
            Returns the mass provider.
        
            Returns:
                the mass provider
        
        
        """
        ...
    def getMaxCheckInterval(self) -> float:
        """
            Get maximal time interval between switching function checks.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.getMaxCheckInterval` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.events.AbstractDetector.getMaxCheckInterval` in
                class :class:`~fr.cnes.sirius.patrius.events.AbstractDetector`
        
            Returns:
                maximal time interval (s) between switching function checks
        
        
        """
        ...
    def getMaxIterationCount(self) -> int:
        """
            Get maximal number of iterations in the event time search.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.getMaxIterationCount` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.events.AbstractDetector.getMaxIterationCount` in
                class :class:`~fr.cnes.sirius.patrius.events.AbstractDetector`
        
            Returns:
                maximal number of iterations in the event time search
        
        
        """
        ...
    def getPropulsiveProperty(self) -> fr.cnes.sirius.patrius.assembly.properties.PropulsiveProperty:
        """
            Get the propulsive property.
        
            Returns:
                propulsive property
        
        
        """
        ...
    def getSlopeSelection(self) -> int:
        """
            Get the parameter in charge of the selection of detected events by the slope of the g-function..
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.getSlopeSelection` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.events.AbstractDetector.getSlopeSelection` in
                class :class:`~fr.cnes.sirius.patrius.events.AbstractDetector`
        
            Returns:
                EventDetector.INCREASING (0): events related to the increasing g-function;
        
        
                EventDetector.DECREASING (1): events related to the decreasing g-function;
        
        
                EventDetector.INCREASING_DECREASING (2): events related to both increasing and decreasing g-function.
        
        
        """
        ...
    def getTankProperty(self) -> fr.cnes.sirius.patrius.assembly.properties.TankProperty:
        """
            Get the tank property.
        
            Returns:
                tank property
        
        
        """
        ...
    def getThreshold(self) -> float:
        """
            Get the convergence threshold in the event time search.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.getThreshold` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.events.AbstractDetector.getThreshold` in
                class :class:`~fr.cnes.sirius.patrius.events.AbstractDetector`
        
            Returns:
                convergence threshold (s)
        
        
        """
        ...
    def getTrigger(self) -> fr.cnes.sirius.patrius.events.EventDetector:
        """
            Get the triggering event.
        
            Returns:
                triggering event
        
        
        """
        ...
    def getUsedDV(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Get the maneuver instantaneous consumption deltaV.
        
            Returns:
                the maneuver instantaneous consumption deltaV in maneuver frame (inertial, LOF or satellite)
        
        
        """
        ...
    def hasFired(self) -> bool:
        """
            Return the hasFired variable. False when the maneuver hasn't occurred, true otherwise.
        
            Returns:
                true is the maneuver has been performed, false otherwise
        
        
        """
        ...
    def init(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> None:
        """
            Initialize event handler at the start of a propagation.
        
            This method is called once at the start of the propagation. It may be used by the event handler to initialize some
            internal data if needed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.init` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.events.AbstractDetector.init` in
                class :class:`~fr.cnes.sirius.patrius.events.AbstractDetector`
        
            Parameters:
                s0 (:class:`~fr.cnes.sirius.patrius.propagation.SpacecraftState`): initial state
                t (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): target time for the integration
        
        
        """
        ...
    def resetState(self, spacecraftState: fr.cnes.sirius.patrius.propagation.SpacecraftState) -> fr.cnes.sirius.patrius.propagation.SpacecraftState: ...
    def shouldBeRemoved(self) -> bool:
        """
            This method is called after :meth:`~fr.cnes.sirius.patrius.events.EventDetector.eventOccurred` has been triggered. It
            returns true if the current detector should be removed after first event detection. **WARNING:** this method can be
            called only once a event has been triggered. Before, the value is not available.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.events.EventDetector.shouldBeRemoved` in
                interface :class:`~fr.cnes.sirius.patrius.events.EventDetector`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.events.AbstractDetector.shouldBeRemoved` in
                class :class:`~fr.cnes.sirius.patrius.events.AbstractDetector`
        
            Returns:
                true if the current detector should be removed after first event detection
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.maneuvers")``.

    ConstantThrustError: typing.Type[ConstantThrustError]
    ContinuousThrustManeuver: typing.Type[ContinuousThrustManeuver]
    GatesModel: typing.Type[GatesModel]
    ImpulseManeuver: typing.Type[ImpulseManeuver]
    Maneuver: typing.Type[Maneuver]
    ManeuversSequence: typing.Type[ManeuversSequence]
    SmallManeuverAnalyticalModel: typing.Type[SmallManeuverAnalyticalModel]
    orbman: fr.cnes.sirius.patrius.forces.maneuvers.orbman.__module_protocol__
