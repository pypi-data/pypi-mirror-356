
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis.solver
import fr.cnes.sirius.patrius.math.exception
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.ode.events
import fr.cnes.sirius.patrius.math.ode.nonstiff
import fr.cnes.sirius.patrius.math.ode.sampling
import java.io
import java.util
import jpype
import typing



class ContinuousOutputModel(fr.cnes.sirius.patrius.math.ode.sampling.StepHandler, java.io.Serializable):
    """
    public class ContinuousOutputModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class stores all information provided by an ODE integrator during the integration process and build a continuous
        model of the solution from this.
    
        This class act as a step handler from the integrator point of view. It is called iteratively during the integration
        process and stores a copy of all steps information in a sorted collection for later use. Once the integration process is
        over, the user can use the :meth:`~fr.cnes.sirius.patrius.math.ode.ContinuousOutputModel.setInterpolatedTime` and
        :meth:`~fr.cnes.sirius.patrius.math.ode.ContinuousOutputModel.getInterpolatedState` to retrieve this information at any
        time. It is important to wait for the integration to be over before attempting to call
        :meth:`~fr.cnes.sirius.patrius.math.ode.ContinuousOutputModel.setInterpolatedTime` because some internal variables are
        set only once the last step has been handled.
    
        This is useful for example if the main loop of the user application should remain independent from the integration
        process or if one needs to mimic the behaviour of an analytical model despite a numerical model is used (i.e. one needs
        the ability to get the model value at any time or to navigate through the data).
    
        If problem modeling is done with several separate integration phases for contiguous intervals, the same
        ContinuousOutputModel can be used as step handler for all integration phases as long as they are performed in order and
        in the same direction. As an example, one can extrapolate the trajectory of a satellite with one model (i.e. one set of
        differential equations) up to the beginning of a maneuver, use another more complex model including thrusters modeling
        and accurate attitude control during the maneuver, and revert to the first model after the end of the maneuver. If the
        same continuous output model handles the steps of all integration phases, the user do not need to bother when the
        maneuver begins or ends, he has all the data available in a transparent manner.
    
        An important feature of this class is that it implements the :code:`Serializable` interface. This means that the result
        of an integration can be serialized and reused later (if stored into a persistent medium like a filesystem or a
        database) or elsewhere (if sent to another application). Only the result of the integration is stored, there is no
        reference to the integrated problem by itself.
    
        One should be aware that the amount of data stored in a ContinuousOutputModel instance can be important if the state
        vector is large, if the integration interval is long or if the steps are small (which can result from small tolerance
        settings in :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdaptiveStepsizeIntegrator`).
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`, :meth:`~serialized`
    """
    def __init__(self): ...
    def append(self, continuousOutputModel: 'ContinuousOutputModel') -> None:
        """
            Append another model at the end of the instance.
        
            Parameters:
                model (:class:`~fr.cnes.sirius.patrius.math.ode.ContinuousOutputModel`): model to add at the end of the instance
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the model to append is not compatible with the instance (dimension of the state vector, propagation direction, hole
                    between the dates)
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded during step finalization
        
        
        """
        ...
    def getFinalTime(self) -> float:
        """
            Get the final integration time.
        
            Returns:
                final integration time
        
        
        """
        ...
    def getInitialTime(self) -> float:
        """
            Get the initial integration time.
        
            Returns:
                initial integration time
        
        
        """
        ...
    def getInterpolatedState(self) -> typing.MutableSequence[float]:
        """
            Get the state vector of the interpolated point.
        
            Returns:
                state vector at time :meth:`~fr.cnes.sirius.patrius.math.ode.ContinuousOutputModel.getInterpolatedTime`
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
        
        
        """
        ...
    def getInterpolatedTime(self) -> float:
        """
            Get the time of the interpolated point. If
            :meth:`~fr.cnes.sirius.patrius.math.ode.ContinuousOutputModel.setInterpolatedTime` has not been called, it returns the
            final integration time.
        
            Returns:
                interpolation point time
        
        
        """
        ...
    def handleStep(self, stepInterpolator: fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator, boolean: bool) -> None:
        """
            Handle the last accepted step. A copy of the information provided by the last step is stored in the instance for later
            use.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler.handleStep` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`
        
            Parameters:
                interpolator (:class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepInterpolator`): interpolator for the last accepted step.
                isLast (boolean): true if the step is the last one
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded during step finalization
        
        
        """
        ...
    def init(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float) -> None:
        """
            Initialize step handler at the start of an ODE integration.
        
            This method is called once at the start of the integration. It may be used by the step handler to initialize some
            internal data if needed.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`
        
            Parameters:
                t0 (double): start value of the independent *time* variable
                y0 (double[]): array containing the start value of the state vector
                t (double): target time for the integration
        
        
        """
        ...
    def setInterpolatedTime(self, double: float) -> None:
        """
            Set the time of the interpolated point.
        
            This method should **not** be called before the integration is over because some internal variables are set only once
            the last step has been handled.
        
            Setting the time outside of the integration interval is now allowed (it was not allowed up to version 5.9 of Mantissa),
            but should be used with care since the accuracy of the interpolator will probably be very poor far from this interval.
            This allowance has been added to simplify implementation of search algorithms near the interval endpoints.
        
            Parameters:
                time (double): time of the interpolated point
        
        
        """
        ...

class EquationsMapper(java.io.Serializable):
    """
    public class EquationsMapper extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class mapping the part of a complete state or derivative that pertains to a specific differential equation.
    
        Instances of this class are guaranteed to be immutable.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.SecondaryEquations`, :meth:`~serialized`
    """
    def __init__(self, int: int, int2: int): ...
    def extractEquationData(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Extract equation data from a complete state or derivative array.
        
            Parameters:
                complete (double[]): complete state or derivative array from which equation data should be retrieved
                equationData (double[]): placeholder where to put equation data
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the dimension of the equation data does not match the mapper dimension
        
        
        """
        ...
    def getDimension(self) -> int:
        """
            Get the dimension of the secondary state parameters.
        
            Returns:
                dimension of the secondary state parameters
        
        
        """
        ...
    def getFirstIndex(self) -> int:
        """
            Get the index of the first equation element in complete state arrays.
        
            Returns:
                index of the first equation element in complete state arrays
        
        
        """
        ...
    def insertEquationData(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Insert equation data into a complete state or derivative array.
        
            Parameters:
                equationData (double[]): equation data to be inserted into the complete array
                complete (double[]): placeholder where to put equation data (only the part corresponding to the equation will be overwritten)
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the dimension of the equation data does not match the mapper dimension
        
        
        """
        ...

class ExpandableStatefulODE:
    """
    public class ExpandableStatefulODE extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class represents a combined set of first order differential equations, with at least a primary set of equations
        expandable by some sets of secondary equations.
    
        One typical use case is the computation of the Jacobian matrix for some ODE. In this case, the primary set of equations
        corresponds to the raw ODE, and we add to this set another bunch of secondary equations which represent the Jacobian
        matrix of the primary set.
    
        We want the integrator to use *only* the primary set to estimate the errors and hence the step sizes. It should *not*
        use the secondary equations in this computation. The :class:`~fr.cnes.sirius.patrius.math.ode.AbstractIntegrator` will
        be able to know where the primary set ends and so where the secondary sets begin.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`,
            :class:`~fr.cnes.sirius.patrius.math.ode.JacobianMatrices`
    """
    def __init__(self, firstOrderDifferentialEquations: 'FirstOrderDifferentialEquations'): ...
    def addSecondaryEquations(self, secondaryEquations: 'SecondaryEquations') -> int:
        """
            Add a set of secondary equations to be integrated along with the primary set.
        
            Parameters:
                secondary (:class:`~fr.cnes.sirius.patrius.math.ode.SecondaryEquations`): secondary equations set
        
            Returns:
                index of the secondary equation in the expanded state
        
        
        """
        ...
    def computeDerivatives(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Get the current time derivative of the complete state vector.
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the complete state vector
                yDot (double[]): placeholder array where to put the time derivative of the complete state vector
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if arrays dimensions do not match equations settings
        
        
        """
        ...
    def getCompleteState(self) -> typing.MutableSequence[float]:
        """
            Get the complete current state.
        
            Returns:
                complete current state
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the dimension of the complete state does not match the complete equations sets dimension
        
        
        """
        ...
    def getPrimary(self) -> 'FirstOrderDifferentialEquations':
        """
            Get the primary set of differential equations.
        
            Returns:
                primary set of differential equations
        
        
        """
        ...
    def getPrimaryMapper(self) -> EquationsMapper:
        """
            Get an equations mapper for the primary equations set.
        
            Returns:
                mapper for the primary set
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE.getSecondaryMappers`
        
        
        """
        ...
    def getPrimaryState(self) -> typing.MutableSequence[float]:
        """
            Get primary part of the current state.
        
            Returns:
                primary part of the current state
        
        
        """
        ...
    def getPrimaryStateDot(self) -> typing.MutableSequence[float]:
        """
            Get primary part of the current state derivative.
        
            Returns:
                primary part of the current state derivative
        
        
        """
        ...
    def getSecondaryMappers(self) -> typing.MutableSequence[EquationsMapper]:
        """
            Get the equations mappers for the secondary equations sets.
        
            Returns:
                equations mappers for the secondary equations sets
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE.getPrimaryMapper`
        
        
        """
        ...
    def getSecondaryState(self, int: int) -> typing.MutableSequence[float]:
        """
            Get secondary part of the current state.
        
            Parameters:
                index (int): index of the part to set as returned by
                    :meth:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE.addSecondaryEquations`
        
            Returns:
                secondary part of the current state
        
        
        """
        ...
    def getSecondaryStateDot(self, int: int) -> typing.MutableSequence[float]:
        """
            Get secondary part of the current state derivative.
        
            Parameters:
                index (int): index of the part to set as returned by
                    :meth:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE.addSecondaryEquations`
        
            Returns:
                secondary part of the current state derivative
        
        
        """
        ...
    def getTime(self) -> float:
        """
            Get current time.
        
            Returns:
                current time
        
        
        """
        ...
    def getTotalDimension(self) -> int:
        """
            Return the dimension of the complete set of equations.
        
            The complete set of equations correspond to the primary set plus all secondary sets.
        
            Returns:
                dimension of the complete set of equations
        
        
        """
        ...
    def setCompleteState(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set the complete current state.
        
            Parameters:
                completeState (double[]): complete current state to copy data from
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the dimension of the complete state does not match the complete equations sets dimension
        
        
        """
        ...
    def setPrimaryState(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set primary part of the current state.
        
            Parameters:
                primaryStateIn (double[]): primary part of the current state
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the dimension of the array does not match the primary set
        
        
        """
        ...
    def setSecondaryState(self, int: int, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set secondary part of the current state.
        
            Parameters:
                index (int): index of the part to set as returned by
                    :meth:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE.addSecondaryEquations`
                secondaryState (double[]): secondary part of the current state
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the dimension of the partial state does not match the selected equations set dimension
        
        
        """
        ...
    def setTime(self, double: float) -> None:
        """
            Set current time.
        
            Parameters:
                timeIn (double): current time
        
        
        """
        ...

class FirstOrderDifferentialEquations:
    """
    public interface FirstOrderDifferentialEquations
    
        This interface represents a first order differential equations set.
    
        This interface should be implemented by all real first order differential equation problems before they can be handled
        by the integrators null method.
    
        A first order differential equations problem, as seen by an integrator is the time derivative :code:`dY/dt` of a state
        vector :code:`Y`, both being one dimensional arrays. From the integrator point of view, this derivative depends only on
        the current time :code:`t` and on the state vector :code:`Y`.
    
        For real problems, the derivative depends also on parameters that do not belong to the state vector (dynamical model
        constants for example). These constants are completely outside of the scope of this interface, the classes that
        implement it are allowed to handle them as they want.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderConverter`,
            :class:`~fr.cnes.sirius.patrius.math.ode.SecondOrderDifferentialEquations`
    """
    def computeDerivatives(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Get the current time derivative of the state vector.
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector
                yDot (double[]): placeholder array where to put the time derivative of the state vector
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if arrays dimensions do not match equations settings
        
        
        """
        ...
    def getDimension(self) -> int:
        """
            Get the dimension of the problem.
        
            Returns:
                dimension of the problem
        
        
        """
        ...

class JacobianMatrices:
    """
    public class JacobianMatrices extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class defines a set of :class:`~fr.cnes.sirius.patrius.math.ode.SecondaryEquations` to compute the Jacobian
        matrices with respect to the initial state vector and, if any, to some parameters of the primary ODE set.
    
        It is intended to be packed into an :class:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE` in conjunction with
        a primary set of ODE, which may be:
    
          - a :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`
          - a :class:`~fr.cnes.sirius.patrius.math.ode.MainStateJacobianProvider`
    
        In order to compute Jacobian matrices with respect to some parameters of the primary ODE set, the following parameter
        Jacobian providers may be set:
    
          - a :class:`~fr.cnes.sirius.patrius.math.ode.ParameterJacobianProvider`
          - a :class:`~fr.cnes.sirius.patrius.math.ode.ParameterizedODE`
    
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE`,
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`,
            :class:`~fr.cnes.sirius.patrius.math.ode.MainStateJacobianProvider`,
            :class:`~fr.cnes.sirius.patrius.math.ode.ParameterJacobianProvider`,
            :class:`~fr.cnes.sirius.patrius.math.ode.ParameterizedODE`
    """
    @typing.overload
    def __init__(self, firstOrderDifferentialEquations: FirstOrderDifferentialEquations, doubleArray: typing.Union[typing.List[float], jpype.JArray], *string: str): ...
    @typing.overload
    def __init__(self, mainStateJacobianProvider: 'MainStateJacobianProvider', *string: str): ...
    def addParameterJacobianProvider(self, parameterJacobianProvider: 'ParameterJacobianProvider') -> None:
        """
            Add a parameter Jacobian provider.
        
            Parameters:
                provider (:class:`~fr.cnes.sirius.patrius.math.ode.ParameterJacobianProvider`): the parameter Jacobian provider to compute exactly the parameter Jacobian matrix
        
        
        """
        ...
    def getCurrentMainSetJacobian(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None:
        """
            Get the current value of the Jacobian matrix with respect to state.
        
            Parameters:
                dYdY0 (double[][]): current Jacobian matrix with respect to state.
        
        
        """
        ...
    def getCurrentParameterJacobian(self, string: str, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Get the current value of the Jacobian matrix with respect to one parameter.
        
            Parameters:
                pName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of the parameter for the computed Jacobian matrix
                dYdP (double[]): current Jacobian matrix with respect to the named parameter
        
        
        """
        ...
    def registerVariationalEquations(self, expandableStatefulODE: ExpandableStatefulODE) -> None:
        """
            Register the variational equations for the Jacobians matrices to the expandable set.
        
            Parameters:
                expandable (:class:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE`): expandable set into which variational equations should be registered
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the dimension of the partial state does not match the selected equations set dimension
                :class:`~fr.cnes.sirius.patrius.math.ode.JacobianMatrices.MismatchedEquations`: if the primary set of the expandable set does not match the one used to build the instance
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE.addSecondaryEquations`
        
        
        """
        ...
    def setInitialMainStateJacobian(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None:
        """
            Set the initial value of the Jacobian matrix with respect to state.
        
            If this method is not called, the initial value of the Jacobian matrix with respect to state is set to identity.
        
            Parameters:
                dYdY0 (double[][]): initial Jacobian matrix w.r.t. state
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if matrix dimensions are incorrect
        
        
        """
        ...
    def setInitialParameterJacobian(self, string: str, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Set the initial value of a column of the Jacobian matrix with respect to one parameter.
        
            If this method is not called for some parameter, the initial value of the column of the Jacobian matrix with respect to
            this parameter is set to zero.
        
            Parameters:
                pName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): parameter name
                dYdP (double[]): initial Jacobian column vector with respect to the parameter
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.ode.UnknownParameterException`: if a parameter is not supported
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the column vector does not match state dimension
        
        
        """
        ...
    def setParameterStep(self, string: str, double: float) -> None:
        """
            Set the step associated to a parameter in order to compute by finite difference the Jacobian matrix.
        
            Needed if and only if the primary ODE set is a :class:`~fr.cnes.sirius.patrius.math.ode.ParameterizedODE`.
        
            Given a non zero parameter value pval for the parameter, a reasonable value for such a step is :code:`pval *
            FastMath.sqrt(Precision.EPSILON)`.
        
            A zero value for such a step doesn't enable to compute the parameter Jacobian matrix.
        
            Parameters:
                parameter (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): parameter to consider for Jacobian processing
                hP (double): step for Jacobian finite difference computation w.r.t. the specified parameter
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.ode.UnknownParameterException`: if the parameter is not supported
        
            Also see:
                :class:`~fr.cnes.sirius.patrius.math.ode.ParameterizedODE`
        
        
        """
        ...
    def setParameterizedODE(self, parameterizedODE: 'ParameterizedODE') -> None:
        """
            Set a parameter Jacobian provider.
        
            Parameters:
                parameterizedOde (:class:`~fr.cnes.sirius.patrius.math.ode.ParameterizedODE`): the parameterized ODE to compute the parameter Jacobian matrix using finite differences
        
        
        """
        ...
    class MismatchedEquations(fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException):
        def __init__(self): ...

class MultistepIntegrator(fr.cnes.sirius.patrius.math.ode.nonstiff.AdaptiveStepsizeIntegrator):
    """
    public abstract class MultistepIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdaptiveStepsizeIntegrator`
    
        This class is the base class for multistep integrators for Ordinary Differential Equations.
    
        We define scaled derivatives s :sub:`i` (n) at step n as:
    
        .. code-block: java
        
        
         s :sub:`1` (n) = h y' :sub:`n`  for first derivative
         s :sub:`2` (n) = h :sup:`2` /2 y'' :sub:`n`  for second derivative
         s :sub:`3` (n) = h :sup:`3` /6 y''' :sub:`n`  for third derivative
         ...
         s :sub:`k` (n) = h :sup:`k` /k! y :sup:`(k)`  :sub:`n`  for k :sup:`th`  derivative
         
    
        Rather than storing several previous steps separately, this implementation uses the Nordsieck vector with higher degrees
        scaled derivatives all taken at the same step (y :sub:`n` , s :sub:`1` (n) and r :sub:`n` ) where r :sub:`n` is defined
        as:
    
        .. code-block: java
        
        
         r :sub:`n`  = [ s :sub:`2` (n), s :sub:`3` (n) ... s :sub:`k` (n) ] :sup:`T` 
         
        (we omit the k index in the notation for clarity)
    
        Multistep integrators with Nordsieck representation are highly sensitive to large step changes because when the step is
        multiplied by factor a, the k :sup:`th` component of the Nordsieck vector is multiplied by a :sup:`k` and the last
        components are the least accurate ones. The default max growth factor is therefore set to a quite low value: 2
        :sup:`1/order` .
    
        Since:
            2.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsBashforthIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.nonstiff.AdamsMoultonIntegrator`, :meth:`~serialized`
    """
    def getMaxGrowth(self) -> float:
        """
            Get the maximal growth factor for stepsize control.
        
            Returns:
                maximal growth factor
        
        
        """
        ...
    def getMinReduction(self) -> float:
        """
            Get the minimal reduction factor for stepsize control.
        
            Returns:
                minimal reduction factor
        
        
        """
        ...
    def getSafety(self) -> float:
        """
            Get the safety factor for stepsize control.
        
            Returns:
                safety factor
        
        
        """
        ...
    def getStarterIntegrator(self) -> 'ODEIntegrator':
        """
            Get the starter integrator.
        
            Returns:
                starter integrator
        
        
        """
        ...
    def setMaxGrowth(self, double: float) -> None:
        """
            Set the maximal growth factor for stepsize control.
        
            Parameters:
                maxGrowthIn (double): maximal growth factor
        
        
        """
        ...
    def setMinReduction(self, double: float) -> None:
        """
            Set the minimal reduction factor for stepsize control.
        
            Parameters:
                minReductionIn (double): minimal reduction factor
        
        
        """
        ...
    def setSafety(self, double: float) -> None:
        """
            Set the safety factor for stepsize control.
        
            Parameters:
                safetyIn (double): safety factor
        
        
        """
        ...
    def setStarterIntegrator(self, firstOrderIntegrator: 'FirstOrderIntegrator') -> None:
        """
            Set the starter integrator.
        
            The various step and event handlers for this starter integrator will be managed automatically by the multi-step
            integrator. Any user configuration for these elements will be cleared before use.
        
            Parameters:
                starterIntegrator (:class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator`): starter integrator
        
        
        """
        ...
    class NordsieckTransformer:
        def initializeHighOrderDerivatives(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> fr.cnes.sirius.patrius.math.linear.Array2DRowRealMatrix: ...

class ODEIntegrator:
    """
    public interface ODEIntegrator
    
        This interface defines the common parts shared by integrators for first and second order differential equations.
    
        Since:
            2.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.SecondOrderIntegrator`
    """
    @typing.overload
    def addEventHandler(self, eventHandler: fr.cnes.sirius.patrius.math.ode.events.EventHandler, double: float, double2: float, int: int) -> None:
        """
            Add an event handler to the integrator. Uses a default
            :class:`~fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver` with an absolute accuracy equal to the given
            convergence threshold, as root-finding algorithm to detect the state events.
        
            Parameters:
                handler (:class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`): event handler
                maxCheckInterval (double): maximal time interval between switching function checks (this interval prevents missing sign changes in case the
                    integration steps becomes very large)
                convergence (double): convergence threshold in the event time search
                maxIterationCount (int): upper limit of the iteration count in the event time search
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.getEventHandlers`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.clearEventHandlers`
        
            Add an event handler to the integrator.
        
            Parameters:
                handler (:class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`): event handler
                maxCheckInterval (double): maximal time interval between switching function checks (this interval prevents missing sign changes in case the
                    integration steps becomes very large)
                convergence (double): convergence threshold in the event time search
                maxIterationCount (int): upper limit of the iteration count in the event time search
                solver (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver`): The root-finding algorithm to use to detect the state events.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.getEventHandlers`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.clearEventHandlers`
        
        
        """
        ...
    @typing.overload
    def addEventHandler(self, eventHandler: fr.cnes.sirius.patrius.math.ode.events.EventHandler, double: float, double2: float, int: int, univariateSolver: fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver) -> None: ...
    def addStepHandler(self, stepHandler: fr.cnes.sirius.patrius.math.ode.sampling.StepHandler) -> None:
        """
            Add a step handler to this integrator.
        
            The handler will be called by the integrator for each accepted step.
        
            Parameters:
                handler (:class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`): handler for the accepted steps
        
            Since:
                2.0
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.getStepHandlers`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.clearStepHandlers`
        
        
        """
        ...
    def clearEventHandlers(self) -> None:
        """
            Remove all the event handlers that have been added to the integrator.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.addEventHandler`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.getEventHandlers`
        
        
        """
        ...
    def clearStepHandlers(self) -> None:
        """
            Remove all the step handlers that have been added to the integrator.
        
            Since:
                2.0
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.addStepHandler`,
                :meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.getStepHandlers`
        
        
        """
        ...
    def getCurrentSignedStepsize(self) -> float:
        """
            Get the current signed value of the integration stepsize.
        
            This method can be called during integration (typically by the object implementing the
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations` problem) if the signed value of the current
            stepsize that is tried is needed.
        
            The result is undefined if the method is called outside of calls to :code:`integrate`.
        
            Returns:
                current signed value of the stepsize
        
        
        """
        ...
    def getCurrentStepStart(self) -> float:
        """
            Get the current value of the step start time t :sub:`i` .
        
            This method can be called during integration (typically by the object implementing the
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations` problem) if the value of the current step that
            is attempted is needed.
        
            The result is undefined if the method is called outside of calls to :code:`integrate`.
        
            Returns:
                current value of the step start time t :sub:`i`
        
        
        """
        ...
    def getEvaluations(self) -> int:
        """
            Get the number of evaluations of the differential equations function.
        
            The number of evaluations corresponds to the last call to the :code:`integrate` method. It is 0 if the method has not
            been called yet.
        
            Returns:
                number of evaluations of the differential equations function
        
        
        """
        ...
    def getEventHandlers(self) -> java.util.Collection[fr.cnes.sirius.patrius.math.ode.events.EventHandler]: ...
    def getMaxEvaluations(self) -> int:
        """
            Get the maximal number of functions evaluations.
        
            Returns:
                maximal number of functions evaluations
        
        
        """
        ...
    def getName(self) -> str:
        """
            Get the name of the method.
        
            Returns:
                name of the method
        
        
        """
        ...
    def getStepHandlers(self) -> java.util.Collection[fr.cnes.sirius.patrius.math.ode.sampling.StepHandler]: ...
    def handleLastStep(self, boolean: bool) -> None:
        """
            Setter for last step status. If true, last step will be handled as such and step handlers will be informed via the
            "isLast" boolean otherwise step handlers are not informed. By default last step is handled as such. this setter is used
            for numerical roundoff errors purpose.
        
            Parameters:
                handleLastStep (boolean): true if last step should be handled as such and step handlers should be informed
        
        
        """
        ...
    def setMaxEvaluations(self, int: int) -> None:
        """
            Set the maximal number of differential equations function evaluations.
        
            The purpose of this method is to avoid infinite loops which can occur for example when stringent error constraints are
            set or when lots of discrete events are triggered, thus leading to many rejected steps.
        
            Parameters:
                maxEvaluations (int): maximal number of function evaluations (negative values are silently converted to maximal integer value, thus
                    representing almost unlimited evaluations)
        
        
        """
        ...

class Parameterizable:
    """
    public interface Parameterizable
    
        This interface enables to process any parameterizable object.
    
        Since:
            3.0
    """
    def getParametersNames(self) -> java.util.Collection[str]: ...
    def isSupported(self, string: str) -> bool:
        """
            Check if a parameter is supported.
        
            Supported parameters are those listed by :meth:`~fr.cnes.sirius.patrius.math.ode.Parameterizable.getParametersNames`.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): parameter name to check
        
            Returns:
                true if the parameter is supported
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.Parameterizable.getParametersNames`
        
        
        """
        ...

class SecondOrderDifferentialEquations:
    """
    public interface SecondOrderDifferentialEquations
    
        This interface represents a second order differential equations set.
    
        This interface should be implemented by all real second order differential equation problems before they can be handled
        by the integrators null method.
    
        A second order differential equations problem, as seen by an integrator is the second time derivative :code:`d2Y/dt^2`
        of a state vector :code:`Y`, both being one dimensional arrays. From the integrator point of view, this derivative
        depends only on the current time :code:`t`, on the state vector :code:`Y` and on the first time derivative of the state
        vector.
    
        For real problems, the derivative depends also on parameters that do not belong to the state vector (dynamical model
        constants for example). These constants are completely outside of the scope of this interface, the classes that
        implement it are allowed to handle them as they want.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.SecondOrderIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderConverter`,
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`
    """
    def computeSecondDerivatives(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Get the current time derivative of the state vector.
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector
                yDot (double[]): array containing the current value of the first derivative of the state vector
                yDDot (double[]): placeholder array where to put the second time derivative of the state vector
        
        
        """
        ...
    def getDimension(self) -> int:
        """
            Get the dimension of the problem.
        
            Returns:
                dimension of the problem
        
        
        """
        ...

class SecondaryEquations:
    """
    public interface SecondaryEquations
    
        This interface allows users to add secondary differential equations to a primary set of differential equations.
    
        In some cases users may need to integrate some problem-specific equations along with a primary set of differential
        equations. One example is optimal control where adjoined parameters linked to the minimized hamiltonian must be
        integrated.
    
        This interface allows users to add such equations to a primary set of
        :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations` thanks to the
        :meth:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE.addSecondaryEquations` method.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.ExpandableStatefulODE`
    """
    def computeDerivatives(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray], doubleArray4: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Compute the derivatives related to the secondary state parameters.
        
            Parameters:
                t (double): current value of the independent *time* variable
                primary (double[]): array containing the current value of the primary state vector
                primaryDot (double[]): array containing the derivative of the primary state vector
                secondary (double[]): array containing the current value of the secondary state vector
                secondaryDot (double[]): placeholder array where to put the derivative of the secondary state vector
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if arrays dimensions do not match equations settings
        
        
        """
        ...
    def getDimension(self) -> int:
        """
            Get the dimension of the secondary state parameters.
        
            Returns:
                dimension of the secondary state parameters
        
        
        """
        ...

class UnknownParameterException(fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException):
    """
    public class UnknownParameterException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`
    
        Exception to be thrown when a parameter is unknown.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, string: str): ...
    def getName(self) -> str:
        """
        
            Returns:
                the name of the unknown parameter.
        
        
        """
        ...

class AbstractParameterizable(Parameterizable):
    """
    public abstract class AbstractParameterizable extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.ode.Parameterizable`
    
        This abstract class provides boilerplate parameters list.
    
        Since:
            3.0
    """
    def complainIfNotSupported(self, string: str) -> None:
        """
            Check if a parameter is supported and throw an IllegalArgumentException if not.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of the parameter to check
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.ode.UnknownParameterException`: if the parameter is not supported
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.AbstractParameterizable.isSupported`
        
        
        """
        ...
    def getParametersNames(self) -> java.util.Collection[str]: ...
    def isSupported(self, string: str) -> bool:
        """
            Check if a parameter is supported.
        
            Supported parameters are those listed by :meth:`~fr.cnes.sirius.patrius.math.ode.Parameterizable.getParametersNames`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.Parameterizable.isSupported` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.Parameterizable`
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): parameter name to check
        
            Returns:
                true if the parameter is supported
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.ode.Parameterizable.getParametersNames`
        
        
        """
        ...

class FirstOrderConverter(FirstOrderDifferentialEquations):
    """
    public class FirstOrderConverter extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`
    
        This class converts second order differential equations to first order ones.
    
        This class is a wrapper around a :class:`~fr.cnes.sirius.patrius.math.ode.SecondOrderDifferentialEquations` which allow
        to use a :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator` to integrate it.
    
        The transformation is done by changing the n dimension state vector to a 2n dimension vector, where the first n
        components are the initial state variables and the n last components are their first time derivative. The first time
        derivative of this state vector then really contains both the first and second time derivative of the initial state
        vector, which can be handled by the underlying second order equations set.
    
        One should be aware that the data is duplicated during the transformation process and that for each call to null, this
        wrapper does copy 4n scalars : 2n before the call to null in order to dispatch the y state vector into z and zDot, and
        2n after the call to gather zDot and zDDot into yDot. Since the underlying problem by itself perhaps also needs to copy
        data and dispatch the arrays into domain objects, this has an impact on both memory and CPU usage. The only way to avoid
        this duplication is to perform the transformation at the problem level, i.e. to implement the problem as a first order
        one and then avoid using this class.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderIntegrator`,
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`,
            :class:`~fr.cnes.sirius.patrius.math.ode.SecondOrderDifferentialEquations`
    """
    def __init__(self, secondOrderDifferentialEquations: SecondOrderDifferentialEquations): ...
    def computeDerivatives(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Get the current time derivative of the state vector.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the state vector
                yDot (double[]): placeholder array where to put the time derivative of the state vector
        
        
        """
        ...
    def getDimension(self) -> int:
        """
            Get the dimension of the problem.
        
            The dimension of the first order problem is twice the dimension of the underlying second order problem.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations.getDimension` in
                interface :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`
        
            Returns:
                dimension of the problem
        
        
        """
        ...

class FirstOrderIntegrator(ODEIntegrator, java.io.Serializable):
    """
    public interface FirstOrderIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This interface represents a first order integrator for differential equations.
    
        The classes which are devoted to solve first order differential equations should implement this interface. The problems
        which can be handled should implement the :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`
        interface.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`,
            :class:`~fr.cnes.sirius.patrius.math.ode.sampling.StepHandler`,
            :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler`
    """
    def integrate(self, firstOrderDifferentialEquations: FirstOrderDifferentialEquations, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Integrate the differential equations up to the given time.
        
            This method solves an Initial Value Problem (IVP).
        
            Since this method stores some internal state variables made available in its public interface during integration
            (:meth:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator.getCurrentSignedStepsize`), it is *not* thread-safe.
        
            Parameters:
                equations (:class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`): differential equations to integrate
                t0 (double): initial time
                y0 (double[]): initial value of the state vector at t0
                t (double): target time for the integration (can be set to a value smaller than :code:`t0` for backward integration)
                y (double[]): placeholder where to put the state vector at each successful step (and hence at the end of integration), can be the same
                    object as y0
        
            Returns:
                stop time, will be the same as target time if integration reached its target, but may be different if some
                :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler` stops it at some point.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if arrays dimension do not match equations settings
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if integration step is too small
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
                :class:`~fr.cnes.sirius.patrius.math.exception.NoBracketingException`: if the location of an event cannot be bracketed
        
        
        """
        ...

class MainStateJacobianProvider(FirstOrderDifferentialEquations):
    """
    public interface MainStateJacobianProvider extends :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations`
    
        Interface expanding :class:`~fr.cnes.sirius.patrius.math.ode.FirstOrderDifferentialEquations` in order to compute
        exactly the main state jacobian matrix for :class:`~fr.cnes.sirius.patrius.math.ode.JacobianMatrices`.
    
        Since:
            3.0
    """
    def computeMainStateJacobian(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> None:
        """
            Compute the jacobian matrix of ODE with respect to main state.
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the main state vector
                yDot (double[]): array containing the current value of the time derivative of the main state vector
                dFdY (double[][]): placeholder array where to put the jacobian matrix of the ODE w.r.t. the main state vector
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if arrays dimensions do not match equations settings
        
        
        """
        ...

class ParameterJacobianProvider(Parameterizable):
    """
    public interface ParameterJacobianProvider extends :class:`~fr.cnes.sirius.patrius.math.ode.Parameterizable`
    
        Interface to compute exactly Jacobian matrix for some parameter when computing
        :class:`~fr.cnes.sirius.patrius.math.ode.JacobianMatrices`.
    
        Since:
            3.0
    """
    def computeParameterJacobian(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], string: str, doubleArray3: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Compute the Jacobian matrix of ODE with respect to one parameter.
        
            If the parameter does not belong to the collection returned by
            :meth:`~fr.cnes.sirius.patrius.math.ode.Parameterizable.getParametersNames`, the Jacobian will be set to 0, but no
            errors will be triggered.
        
            Parameters:
                t (double): current value of the independent *time* variable
                y (double[]): array containing the current value of the main state vector
                yDot (double[]): array containing the current value of the time derivative of the main state vector
                paramName (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): name of the parameter to consider
                dFdP (double[]): placeholder array where to put the Jacobian matrix of the ODE with respect to the parameter
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MaxCountExceededException`: if the number of functions evaluations is exceeded
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if arrays dimensions do not match equations settings
                :class:`~fr.cnes.sirius.patrius.math.ode.UnknownParameterException`: if the parameter is not supported
        
        
        """
        ...

class ParameterizedODE(Parameterizable):
    """
    public interface ParameterizedODE extends :class:`~fr.cnes.sirius.patrius.math.ode.Parameterizable`
    
        Interface to compute by finite difference Jacobian matrix for some parameter when computing
        :class:`~fr.cnes.sirius.patrius.math.ode.JacobianMatrices`.
    
        Since:
            3.0
    """
    def getParameter(self, string: str) -> float:
        """
            Get parameter value from its name.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): parameter name
        
            Returns:
                parameter value
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.ode.UnknownParameterException`: if parameter is not supported
        
        
        """
        ...
    def setParameter(self, string: str, double: float) -> None:
        """
            Set the value for a given parameter.
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): parameter name
                value (double): parameter value
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.ode.UnknownParameterException`: if parameter is not supported
        
        
        """
        ...

class SecondOrderIntegrator(ODEIntegrator):
    """
    public interface SecondOrderIntegrator extends :class:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator`
    
        This interface represents a second order integrator for differential equations.
    
        The classes which are devoted to solve second order differential equations should implement this interface. The problems
        which can be handled should implement the :class:`~fr.cnes.sirius.patrius.math.ode.SecondOrderDifferentialEquations`
        interface.
    
        Since:
            1.2
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.ode.SecondOrderDifferentialEquations`
    """
    def integrate(self, secondOrderDifferentialEquations: SecondOrderDifferentialEquations, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], double4: float, doubleArray3: typing.Union[typing.List[float], jpype.JArray], doubleArray4: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Integrate the differential equations up to the given time
        
            Parameters:
                equations (:class:`~fr.cnes.sirius.patrius.math.ode.SecondOrderDifferentialEquations`): differential equations to integrate
                t0 (double): initial time
                y0 (double[]): initial value of the state vector at t0
                yDot0 (double[]): initial value of the first derivative of the state vector at t0
                t (double): target time for the integration (can be set to a value smaller thant :code:`t0` for backward integration)
                y (double[]): placeholder where to put the state vector at each successful step (and hence at the end of integration), can be the same
                    object as y0
                yDot (double[]): placeholder where to put the first derivative of the state vector at time t, can be the same object as yDot0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`: if the integrator cannot perform integration
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if integration parameters are wrong (typically too small integration span)
        
        
        """
        ...

class AbstractIntegrator(java.util.Observable, FirstOrderIntegrator):
    def __init__(self, string: str): ...
    @typing.overload
    def addEventHandler(self, eventHandler: fr.cnes.sirius.patrius.math.ode.events.EventHandler, double: float, double2: float, int: int) -> None: ...
    @typing.overload
    def addEventHandler(self, eventHandler: fr.cnes.sirius.patrius.math.ode.events.EventHandler, double: float, double2: float, int: int, univariateSolver: fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver) -> None: ...
    def addStepHandler(self, stepHandler: fr.cnes.sirius.patrius.math.ode.sampling.StepHandler) -> None: ...
    def clearEventHandlers(self) -> None: ...
    def clearStepHandlers(self) -> None: ...
    def computeDerivatives(self, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def getCurrentSignedStepsize(self) -> float: ...
    def getCurrentStepStart(self) -> float: ...
    def getEvaluations(self) -> int: ...
    def getEventHandlers(self) -> java.util.Collection[fr.cnes.sirius.patrius.math.ode.events.EventHandler]: ...
    def getMaxEvaluations(self) -> int: ...
    def getName(self) -> str: ...
    def getStepHandlers(self) -> java.util.Collection[fr.cnes.sirius.patrius.math.ode.sampling.StepHandler]: ...
    def handleLastStep(self, boolean: bool) -> None: ...
    @typing.overload
    def integrate(self, expandableStatefulODE: ExpandableStatefulODE, double: float) -> None: ...
    @typing.overload
    def integrate(self, firstOrderDifferentialEquations: FirstOrderDifferentialEquations, double: float, doubleArray: typing.Union[typing.List[float], jpype.JArray], double3: float, doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    def removeEventState(self, eventState: fr.cnes.sirius.patrius.math.ode.events.EventState) -> None: ...
    def setMaxEvaluations(self, int: int) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.ode")``.

    AbstractIntegrator: typing.Type[AbstractIntegrator]
    AbstractParameterizable: typing.Type[AbstractParameterizable]
    ContinuousOutputModel: typing.Type[ContinuousOutputModel]
    EquationsMapper: typing.Type[EquationsMapper]
    ExpandableStatefulODE: typing.Type[ExpandableStatefulODE]
    FirstOrderConverter: typing.Type[FirstOrderConverter]
    FirstOrderDifferentialEquations: typing.Type[FirstOrderDifferentialEquations]
    FirstOrderIntegrator: typing.Type[FirstOrderIntegrator]
    JacobianMatrices: typing.Type[JacobianMatrices]
    MainStateJacobianProvider: typing.Type[MainStateJacobianProvider]
    MultistepIntegrator: typing.Type[MultistepIntegrator]
    ODEIntegrator: typing.Type[ODEIntegrator]
    ParameterJacobianProvider: typing.Type[ParameterJacobianProvider]
    Parameterizable: typing.Type[Parameterizable]
    ParameterizedODE: typing.Type[ParameterizedODE]
    SecondOrderDifferentialEquations: typing.Type[SecondOrderDifferentialEquations]
    SecondOrderIntegrator: typing.Type[SecondOrderIntegrator]
    SecondaryEquations: typing.Type[SecondaryEquations]
    UnknownParameterException: typing.Type[UnknownParameterException]
    events: fr.cnes.sirius.patrius.math.ode.events.__module_protocol__
    nonstiff: fr.cnes.sirius.patrius.math.ode.nonstiff.__module_protocol__
    sampling: fr.cnes.sirius.patrius.math.ode.sampling.__module_protocol__
