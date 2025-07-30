
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.linear
import java.lang
import java.util
import jpype
import typing



class FIRFilter:
    """
    public final class FIRFilter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class implements a digital FIR filter.
    """
    def __init__(self, filterType: 'FIRFilter.FilterType', dataTypeArray: typing.Union[typing.List['FIRFilter.DataType'], jpype.JArray], list: java.util.List[float], double: float): ...
    def compute(self, univariateVectorFunction: fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction, double: float) -> typing.MutableSequence[float]:
        """
            Computes the filtered value of the given function at the given computation point. Angular values are normalized to [-PI,
            PI) before being returned.
        
            Parameters:
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction`): vectorial function to filter
                x0 (double): computation point
        
            Returns:
                the filtered value of the function at given computation point
        
        
        """
        ...
    def getNbPointsAfter(self) -> int:
        """
            Getter for the number of points after the computation date to be used by the filter.
        
            Returns:
                the number of points after the computation date to be used by the filter
        
        
        """
        ...
    def getNbPointsBefore(self) -> int:
        """
            Getter for the number of points before the computation date to be used by the filter.
        
            Returns:
                the number of points before the computation date to be used by the filter
        
        
        """
        ...
    def getSamplingStep(self) -> float:
        """
            Getter for sampling step of the filter.
        
            Returns:
                the sampling step of the filter
        
        
        """
        ...
    class DataType(java.lang.Enum['FIRFilter.DataType']):
        ANGULAR: typing.ClassVar['FIRFilter.DataType'] = ...
        OTHER: typing.ClassVar['FIRFilter.DataType'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'FIRFilter.DataType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['FIRFilter.DataType']: ...
    class FilterType(java.lang.Enum['FIRFilter.FilterType']):
        CAUSAL: typing.ClassVar['FIRFilter.FilterType'] = ...
        LINEAR: typing.ClassVar['FIRFilter.FilterType'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'FIRFilter.FilterType': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['FIRFilter.FilterType']: ...

class KalmanFilter:
    """
    public class KalmanFilter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Implementation of a Kalman filter to estimate the state *x :sub:`k`* of a discrete-time controlled process that is
        governed by the linear stochastic difference equation:
    
        .. code-block: java
        
        
         *x :sub:`k`* = **A***x :sub:`k-1`* + **B***u :sub:`k-1`* + *w :sub:`k-1`*
         
        with a measurement *x :sub:`k`* that is
    
        .. code-block: java
        
        
         *z :sub:`k`* = **H***x :sub:`k`* + *v :sub:`k`*.
         
    
        The random variables *w :sub:`k`* and *v :sub:`k`* represent the process and measurement noise and are assumed to be
        independent of each other and distributed with normal probability (white noise).
    
        The Kalman filter cycle involves the following steps:
    
          1.  predict: project the current state estimate ahead in time
          2.  correct: adjust the projected estimate by an actual measurement
    
    
        The Kalman filter is initialized with a :class:`~fr.cnes.sirius.patrius.math.filter.ProcessModel` and a
        :class:`~fr.cnes.sirius.patrius.math.filter.MeasurementModel`, which contain the corresponding transformation and noise
        covariance matrices. The parameter names used in the respective models correspond to the following names commonly used
        in the mathematical literature:
    
          - A - state transition matrix
          - B - control input matrix
          - H - measurement matrix
          - Q - process noise covariance matrix
          - R - measurement noise covariance matrix
          - P - error covariance matrix
    
    
        Since:
            3.0
    
        Also see:
            `Kalman filter resources <http://www.cs.unc.edu/~welch/kalman/>`, `An introduction to the Kalman filter by Greg Welch
            and Gary Bishop <http://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf>`, ` Kalman filter example by Dan Simon
            <http://academic.csuohio.edu/simond/courses/eec644/kalman.pdf>`,
            :class:`~fr.cnes.sirius.patrius.math.filter.ProcessModel`, :class:`~fr.cnes.sirius.patrius.math.filter.MeasurementModel`
    """
    def __init__(self, processModel: 'ProcessModel', measurementModel: 'MeasurementModel'): ...
    @typing.overload
    def correct(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Correct the current state estimate with an actual measurement.
        
            Parameters:
                z (double[]): the measurement vector
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the measurement vector is :code:`null`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the dimension of the measurement vector does not fit
                :class:`~fr.cnes.sirius.patrius.math.linear.SingularMatrixException`: if the covariance matrix could not be inverted
        
            Correct the current state estimate with an actual measurement.
        
            Parameters:
                z (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): the measurement vector
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the measurement vector is :code:`null`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the dimension of the measurement vector does not fit
                :class:`~fr.cnes.sirius.patrius.math.linear.SingularMatrixException`: if the covariance matrix could not be inverted
        
        
        """
        ...
    @typing.overload
    def correct(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...
    def getErrorCovariance(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Returns the current error covariance matrix.
        
            Returns:
                the error covariance matrix
        
        
        """
        ...
    def getErrorCovarianceMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns a copy of the current error covariance matrix.
        
            Returns:
                the error covariance matrix
        
        
        """
        ...
    def getMeasurementDimension(self) -> int:
        """
            Returns the dimension of the measurement vector.
        
            Returns:
                the measurement vector dimension
        
        
        """
        ...
    def getStateDimension(self) -> int:
        """
            Returns the dimension of the state estimation vector.
        
            Returns:
                the state dimension
        
        
        """
        ...
    def getStateEstimation(self) -> typing.MutableSequence[float]:
        """
            Returns the current state estimation vector.
        
            Returns:
                the state estimation vector
        
        
        """
        ...
    def getStateEstimationVector(self) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Returns a copy of the current state estimation vector.
        
            Returns:
                the state estimation vector
        
        
        """
        ...
    @typing.overload
    def predict(self) -> None:
        """
            Predict the internal state estimation one time step ahead.
        """
        ...
    @typing.overload
    def predict(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Predict the internal state estimation one time step ahead.
        
            Parameters:
                u (double[]): the control vector
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the dimension of the control vector does not fit
        
            Predict the internal state estimation one time step ahead.
        
            Parameters:
                u (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): the control vector
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the dimension of the control vector does not match
        
        
        """
        ...
    @typing.overload
    def predict(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> None: ...

class MeasurementModel:
    """
    public interface MeasurementModel
    
        Defines the measurement model for the use with a :class:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter`.
    
        Since:
            3.0
    """
    def getMeasurementMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the measurement matrix.
        
            Returns:
                the measurement matrix
        
        
        """
        ...
    def getMeasurementNoise(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the measurement noise matrix. This method is called by the
            :class:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter` every correction step, so implementations of this interface
            may return a modified measurement noise depending on the current iteration step.
        
            Returns:
                the measurement noise matrix
        
            Also see:
                null, :meth:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter.correct`
        
        
        """
        ...

class ProcessModel:
    """
    public interface ProcessModel
    
        Defines the process dynamics model for the use with a :class:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter`.
    
        Since:
            3.0
    """
    def getControlMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the control matrix.
        
            Returns:
                the control matrix
        
        
        """
        ...
    def getInitialErrorCovariance(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the initial error covariance matrix.
        
            **Note:** if the return value is zero, the Kalman filter will initialize the error covariance with the process noise
            matrix.
        
            Returns:
                the initial error covariance matrix
        
        
        """
        ...
    def getInitialStateEstimate(self) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Returns the initial state estimation vector.
        
            **Note:** if the return value is zero, the Kalman filter will initialize the state estimation with a zero vector.
        
            Returns:
                the initial state estimation vector
        
        
        """
        ...
    def getProcessNoise(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the process noise matrix. This method is called by the :class:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter`
            every prediction step, so implementations of this interface may return a modified process noise depending on the current
            iteration step.
        
            Returns:
                the process noise matrix
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter.predict`, null,
                :meth:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter.predict`
        
        
        """
        ...
    def getStateTransitionMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the state transition matrix.
        
            Returns:
                the state transition matrix
        
        
        """
        ...

class DefaultMeasurementModel(MeasurementModel):
    """
    public class DefaultMeasurementModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.filter.MeasurementModel`
    
        Default implementation of a :class:`~fr.cnes.sirius.patrius.math.filter.MeasurementModel` for the use with a
        :class:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter`.
    
        Since:
            3.0
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realMatrix2: fr.cnes.sirius.patrius.math.linear.RealMatrix): ...
    def getMeasurementMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the measurement matrix.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.filter.MeasurementModel.getMeasurementMatrix` in
                interface :class:`~fr.cnes.sirius.patrius.math.filter.MeasurementModel`
        
            Returns:
                the measurement matrix
        
        
        """
        ...
    def getMeasurementNoise(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the measurement noise matrix. This method is called by the
            :class:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter` every correction step, so implementations of this interface
            may return a modified measurement noise depending on the current iteration step.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.filter.MeasurementModel.getMeasurementNoise` in
                interface :class:`~fr.cnes.sirius.patrius.math.filter.MeasurementModel`
        
            Returns:
                the measurement noise matrix
        
            Also see:
                null, :meth:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter.correct`
        
        
        """
        ...

class DefaultProcessModel(ProcessModel):
    """
    public class DefaultProcessModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.filter.ProcessModel`
    
        Default implementation of a :class:`~fr.cnes.sirius.patrius.math.filter.ProcessModel` for the use with a
        :class:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter`.
    
        Since:
            3.0
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray4: typing.Union[typing.List[float], jpype.JArray], doubleArray5: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, realMatrix2: fr.cnes.sirius.patrius.math.linear.RealMatrix, realMatrix3: fr.cnes.sirius.patrius.math.linear.RealMatrix, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, realMatrix4: fr.cnes.sirius.patrius.math.linear.RealMatrix): ...
    def getControlMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the control matrix.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.filter.ProcessModel.getControlMatrix` in
                interface :class:`~fr.cnes.sirius.patrius.math.filter.ProcessModel`
        
            Returns:
                the control matrix
        
        
        """
        ...
    def getInitialErrorCovariance(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the initial error covariance matrix.
        
            **Note:** if the return value is zero, the Kalman filter will initialize the error covariance with the process noise
            matrix.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.filter.ProcessModel.getInitialErrorCovariance` in
                interface :class:`~fr.cnes.sirius.patrius.math.filter.ProcessModel`
        
            Returns:
                the initial error covariance matrix
        
        
        """
        ...
    def getInitialStateEstimate(self) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Returns the initial state estimation vector.
        
            **Note:** if the return value is zero, the Kalman filter will initialize the state estimation with a zero vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.filter.ProcessModel.getInitialStateEstimate` in
                interface :class:`~fr.cnes.sirius.patrius.math.filter.ProcessModel`
        
            Returns:
                the initial state estimation vector
        
        
        """
        ...
    def getProcessNoise(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the process noise matrix. This method is called by the :class:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter`
            every prediction step, so implementations of this interface may return a modified process noise depending on the current
            iteration step.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.filter.ProcessModel.getProcessNoise` in
                interface :class:`~fr.cnes.sirius.patrius.math.filter.ProcessModel`
        
            Returns:
                the process noise matrix
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter.predict`, null,
                :meth:`~fr.cnes.sirius.patrius.math.filter.KalmanFilter.predict`
        
        
        """
        ...
    def getStateTransitionMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Returns the state transition matrix.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.filter.ProcessModel.getStateTransitionMatrix` in
                interface :class:`~fr.cnes.sirius.patrius.math.filter.ProcessModel`
        
            Returns:
                the state transition matrix
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.filter")``.

    DefaultMeasurementModel: typing.Type[DefaultMeasurementModel]
    DefaultProcessModel: typing.Type[DefaultProcessModel]
    FIRFilter: typing.Type[FIRFilter]
    KalmanFilter: typing.Type[KalmanFilter]
    MeasurementModel: typing.Type[MeasurementModel]
    ProcessModel: typing.Type[ProcessModel]
