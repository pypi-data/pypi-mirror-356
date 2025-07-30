
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.analysis.differentiation
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.time
import typing



class OrientationFunction(fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction):
    """
    public interface OrientationFunction extends :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction`
    
        This interface is a time-dependent function representing a generic orientation.
    
        Since:
            1.3
    """
    def derivative(self) -> 'OrientationFunction':
        """
            Compute the :class:`~fr.cnes.sirius.patrius.attitudes.kinematics.OrientationFunction` representing the first derivative
            of the current orientation function components.
        
        
            The derivation can be analytical or numerical, depending on the current orientation function.
        
            Returns:
                a new :class:`~fr.cnes.sirius.patrius.attitudes.kinematics.OrientationFunction` containing the first derivative of the
                orientation function components.
        
        
        """
        ...
    def estimateRateFunction(self, double: float, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3DFunction:
        """
            Estimate the :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3DFunction` from the current
            :class:`~fr.cnes.sirius.patrius.attitudes.kinematics.OrientationFunction` using the
            :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.estimateRate` method.
        
            Parameters:
                dt (double): time elapsed between the dates of the two orientations
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): validity interval of the function (necessary for handling derivatives at boundaries)
        
            Returns:
                the spin function.
        
        
        """
        ...
    def getOrientation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation: ...

class AbstractOrientationFunction(OrientationFunction):
    """
    public abstract class AbstractOrientationFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.attitudes.kinematics.OrientationFunction`
    
        This abstract class is a time-dependent function representing an orientation.
    
        Since:
            1.3
    """
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, univariateVectorFunctionDifferentiator: typing.Union[fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateVectorFunctionDifferentiator, typing.Callable]): ...
    def derivative(self) -> OrientationFunction:
        """
            Compute the :class:`~fr.cnes.sirius.patrius.attitudes.kinematics.OrientationFunction` representing the first derivative
            of the current orientation function components.
        
        
            The differentiation is performed using a numerical differentiation method. This method can be overridden if an
            analytical differentiation should be performed instead.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.kinematics.OrientationFunction.derivative` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.kinematics.OrientationFunction`
        
            Returns:
                a new :class:`~fr.cnes.sirius.patrius.attitudes.kinematics.OrientationFunction` containing the first derivative of the
                orientation function components.
        
        
        """
        ...
    def estimateRate(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D: ...
    def estimateRateFunction(self, double: float, absoluteDateInterval: fr.cnes.sirius.patrius.time.AbsoluteDateInterval) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3DFunction:
        """
            Estimate the :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3DFunction` from the current
            :class:`~fr.cnes.sirius.patrius.attitudes.kinematics.OrientationFunction` using the
            :meth:`~fr.cnes.sirius.patrius.utils.AngularCoordinates.estimateRate` method.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.attitudes.kinematics.OrientationFunction.estimateRateFunction` in
                interface :class:`~fr.cnes.sirius.patrius.attitudes.kinematics.OrientationFunction`
        
            Parameters:
                dt (double): time elapsed between the dates of the two orientations
                interval (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDateInterval`): validity interval of the function (necessary for handling derivatives at boundaries)
        
            Returns:
                the spin function.
        
        
        """
        ...
    def getDifferentiator(self) -> fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateVectorFunctionDifferentiator:
        """
            Get the differentiator.
        
            Returns:
                the differentiator.
        
        
        """
        ...
    def getOrientation(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Rotation: ...
    def getSize(self) -> int:
        """
            Compute the size of the list of values of the function as created by the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction.value` method
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction.getSize` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction`
        
            Returns:
                the size of the values array
        
        
        """
        ...
    def getZeroDate(self) -> fr.cnes.sirius.patrius.time.AbsoluteDate:
        """
            Get the date at x = 0.
        
            Returns:
                the date at x = 0.
        
        
        """
        ...
    def value(self, double: float) -> typing.MutableSequence[float]:
        """
            Compute the quaternion components of the orientation at the (zero + x) date.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction`
        
            Parameters:
                x (double): the time from the date zero for which the function value should be computed
        
            Returns:
                the quaternion components representing the orientation at the given date.
        
            Raises:
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.attitudes.kinematics")``.

    AbstractOrientationFunction: typing.Type[AbstractOrientationFunction]
    OrientationFunction: typing.Type[OrientationFunction]
