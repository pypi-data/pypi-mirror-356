
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.exception
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.optim
import fr.cnes.sirius.patrius.math.optim.nonlinear.scalar
import java.io
import java.lang
import java.util
import jpype
import typing



class LinearConstraint(java.io.Serializable):
    """
    public class LinearConstraint extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        A linear constraint for a linear optimization problem.
    
        A linear constraint has one of the forms:
    
          - c :sub:`1` x :sub:`1` + ... c :sub:`n` x :sub:`n` = v
          - c :sub:`1` x :sub:`1` + ... c :sub:`n` x :sub:`n` <= v
          - c :sub:`1` x :sub:`1` + ... c :sub:`n` x :sub:`n` >= v
          - l :sub:`1` x :sub:`1` + ... l :sub:`n` x :sub:`n` + l :sub:`cst` = r :sub:`1` x :sub:`1` + ... r :sub:`n` x :sub:`n` + r
            :sub:`cst`
          - l :sub:`1` x :sub:`1` + ... l :sub:`n` x :sub:`n` + l :sub:`cst` <= r :sub:`1` x :sub:`1` + ... r :sub:`n` x :sub:`n` +
            r :sub:`cst`
          - l :sub:`1` x :sub:`1` + ... l :sub:`n` x :sub:`n` + l :sub:`cst` >= r :sub:`1` x :sub:`1` + ... r :sub:`n` x :sub:`n` +
            r :sub:`cst`
    
        The c :sub:`i` , l :sub:`i` or r :sub:`i` are the coefficients of the constraints, the x :sub:`i` are the coordinates of
        the current point and v is the value of the constraint.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float, relationship: 'Relationship', doubleArray2: typing.Union[typing.List[float], jpype.JArray], double4: float): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], relationship: 'Relationship', double2: float): ...
    @typing.overload
    def __init__(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, double: float, relationship: 'Relationship', realVector2: fr.cnes.sirius.patrius.math.linear.RealVector, double2: float): ...
    @typing.overload
    def __init__(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, relationship: 'Relationship', double: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getCoefficients(self) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Gets the coefficients of the constraint (left hand side).
        
            Returns:
                the coefficients of the constraint (left hand side).
        
        
        """
        ...
    def getRelationship(self) -> 'Relationship':
        """
            Gets the relationship between left and right hand sides.
        
            Returns:
                the relationship between left and right hand sides.
        
        
        """
        ...
    def getValue(self) -> float:
        """
            Gets the value of the constraint (right hand side).
        
            Returns:
                the value of the constraint (right hand side).
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class LinearConstraintSet(fr.cnes.sirius.patrius.math.optim.OptimizationData):
    """
    public class LinearConstraintSet extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.OptimizationData`
    
        Class that represents a set of :class:`~fr.cnes.sirius.patrius.math.optim.linear.LinearConstraint`.
    
        Since:
            3.1
    """
    @typing.overload
    def __init__(self, *linearConstraint: LinearConstraint): ...
    @typing.overload
    def __init__(self, collection: typing.Union[java.util.Collection[LinearConstraint], typing.Sequence[LinearConstraint], typing.Set[LinearConstraint]]): ...
    def getConstraints(self) -> java.util.Collection[LinearConstraint]: ...

class LinearObjectiveFunction(fr.cnes.sirius.patrius.math.analysis.MultivariateFunction, fr.cnes.sirius.patrius.math.optim.OptimizationData, java.io.Serializable):
    """
    public class LinearObjectiveFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction`, :class:`~fr.cnes.sirius.patrius.math.optim.OptimizationData`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        An objective function for a linear optimization problem.
    
        A linear objective function has one the form:
    
        .. code-block: java
        
        
         c :sub:`1` x :sub:`1`  + ... c :sub:`n` x :sub:`n`  + d
         
        The c :sub:`i` and d are the coefficients of the equation, the x :sub:`i` are the coordinates of the current point.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float): ...
    @typing.overload
    def __init__(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector, double: float): ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getCoefficients(self) -> fr.cnes.sirius.patrius.math.linear.RealVector:
        """
            Gets the coefficients of the linear equation being optimized.
        
            Returns:
                coefficients of the linear equation being optimized.
        
        
        """
        ...
    def getConstantTerm(self) -> float:
        """
            Gets the constant of the linear equation being optimized.
        
            Returns:
                constant of the linear equation being optimized.
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @typing.overload
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Computes the value of the linear equation at the current point.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction`
        
            Parameters:
                point (double[]): Point at which linear equation must be evaluated.
        
            Returns:
                the value of the linear equation at the current point.
        
            Computes the value of the linear equation at the current point.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.linear.RealVector`): Point at which linear equation must be evaluated.
        
            Returns:
                the value of the linear equation at the current point.
        
        
        """
        ...
    @typing.overload
    def value(self, realVector: fr.cnes.sirius.patrius.math.linear.RealVector) -> float: ...

class LinearOptimizer(fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.MultivariateOptimizer):
    def optimize(self, *optimizationData: fr.cnes.sirius.patrius.math.optim.OptimizationData) -> fr.cnes.sirius.patrius.math.optim.PointValuePair: ...

class NoFeasibleSolutionException(fr.cnes.sirius.patrius.math.exception.MathIllegalStateException):
    """
    public class NoFeasibleSolutionException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`
    
        This class represents exceptions thrown by optimizers when no solution fulfills the constraints.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...

class NonNegativeConstraint(fr.cnes.sirius.patrius.math.optim.OptimizationData):
    """
    public class NonNegativeConstraint extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.OptimizationData`
    
        A constraint for a linear optimization problem indicating whether all variables must be restricted to non-negative
        values.
    
        Since:
            3.1
    """
    def __init__(self, boolean: bool): ...
    def isRestrictedToNonNegative(self) -> bool:
        """
            Indicates whether all the variables must be restricted to non-negative values.
        
            Returns:
                :code:`true` if all the variables must be positive.
        
        
        """
        ...

class Relationship(java.lang.Enum['Relationship']):
    """
    public enum Relationship extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.optim.linear.Relationship`>
    
        Types of relationships between two cells in a Solver
        :class:`~fr.cnes.sirius.patrius.math.optim.linear.LinearConstraint`.
    
        Since:
            2.0
    """
    EQ: typing.ClassVar['Relationship'] = ...
    LEQ: typing.ClassVar['Relationship'] = ...
    GEQ: typing.ClassVar['Relationship'] = ...
    def oppositeRelationship(self) -> 'Relationship':
        """
            Gets the relationship obtained when multiplying all coefficients by -1.
        
            Returns:
                the opposite relationship.
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'Relationship':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                : if this enum type has no constant with the specified name
                : if the argument is null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['Relationship']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (Relationship c : Relationship.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class UnboundedSolutionException(fr.cnes.sirius.patrius.math.exception.MathIllegalStateException):
    """
    public class UnboundedSolutionException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalStateException`
    
        This class represents exceptions thrown by optimizers when a solution escapes to infinity.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...

class SimplexSolver(LinearOptimizer):
    """
    public class SimplexSolver extends :class:`~fr.cnes.sirius.patrius.math.optim.linear.LinearOptimizer`
    
        Solves a linear problem using the "Two-Phase Simplex" method.
    
        Since:
            2.0
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, int: int): ...
    def doOptimize(self) -> fr.cnes.sirius.patrius.math.optim.PointValuePair:
        """
            Performs the bulk of the optimization algorithm.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.optim.BaseOptimizer.doOptimize` in
                class :class:`~fr.cnes.sirius.patrius.math.optim.BaseOptimizer`
        
            Returns:
                the point/value pair giving the optimal value of the objective function.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.linear")``.

    LinearConstraint: typing.Type[LinearConstraint]
    LinearConstraintSet: typing.Type[LinearConstraintSet]
    LinearObjectiveFunction: typing.Type[LinearObjectiveFunction]
    LinearOptimizer: typing.Type[LinearOptimizer]
    NoFeasibleSolutionException: typing.Type[NoFeasibleSolutionException]
    NonNegativeConstraint: typing.Type[NonNegativeConstraint]
    Relationship: typing.Type[Relationship]
    SimplexSolver: typing.Type[SimplexSolver]
    UnboundedSolutionException: typing.Type[UnboundedSolutionException]
