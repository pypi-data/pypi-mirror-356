
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.analysis.differentiation
import fr.cnes.sirius.patrius.math.analysis.polynomials
import fr.cnes.sirius.patrius.math.complex
import java.io
import java.lang
import jpype
import typing



class AllowedSolution(java.lang.Enum['AllowedSolution']):
    """
    public enum AllowedSolution extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`>
    
        The kinds of solutions that a :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver` may accept
        as solutions. This basically controls whether or not under-approximations and over-approximations are allowed.
    
        If all solutions are accepted (:meth:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution.ANY_SIDE`), then the
        solution that the root-finding algorithm returns for a given root may be equal to the actual root, but it may also be an
        approximation that is slightly smaller or slightly larger than the actual root. Root-finding algorithms generally only
        guarantee that the returned solution is within the requested tolerances. In certain cases however, in particular for
        :class:`~fr.cnes.sirius.patrius.math.ode.events.EventHandler` of
        :class:`~fr.cnes.sirius.patrius.math.ode.ODEIntegrator`, it may be necessary to guarantee that a solution is returned
        that lies on a specific side the solution.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver`
    """
    ANY_SIDE: typing.ClassVar['AllowedSolution'] = ...
    LEFT_SIDE: typing.ClassVar['AllowedSolution'] = ...
    RIGHT_SIDE: typing.ClassVar['AllowedSolution'] = ...
    BELOW_SIDE: typing.ClassVar['AllowedSolution'] = ...
    ABOVE_SIDE: typing.ClassVar['AllowedSolution'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'AllowedSolution':
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
    def values() -> typing.MutableSequence['AllowedSolution']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (AllowedSolution c : AllowedSolution.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

_BaseUnivariateSolver__Func = typing.TypeVar('_BaseUnivariateSolver__Func', bound=fr.cnes.sirius.patrius.math.analysis.UnivariateFunction)  # <Func>
class BaseUnivariateSolver(typing.Generic[_BaseUnivariateSolver__Func]):
    """
    public interface BaseUnivariateSolver<Func extends :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`>
    
        Interface for (univariate real) rootfinding algorithms. Implementations will search for only one zero in the given
        interval. This class is not intended for use outside of the Apache Commons Math library, regular user should rely on
        more specific interfaces like :class:`~fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver`,
        :class:`~fr.cnes.sirius.patrius.math.analysis.solver.PolynomialSolver` or
        :class:`~fr.cnes.sirius.patrius.math.analysis.solver.UnivariateDifferentiableSolver`.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver`,
            :class:`~fr.cnes.sirius.patrius.math.analysis.solver.PolynomialSolver`,
            :class:`~fr.cnes.sirius.patrius.math.analysis.solver.UnivariateDifferentiableSolver`
    """
    def getAbsoluteAccuracy(self) -> float:
        """
            Get the absolute accuracy of the solver. Solutions returned by the solver should be accurate to this tolerance, i.e., if
            ε is the absolute accuracy of the solver and :code:`v` is a value returned by one of the :code:`solve` methods, then a
            root of the function should exist somewhere in the interval (:code:`v` - ε, :code:`v` + ε).
        
            Returns:
                the absolute accuracy.
        
        
        """
        ...
    def getEvaluations(self) -> int:
        """
            Get the number of evaluations of the objective function. The number of evaluations corresponds to the last call to the
            :code:`optimize` method. It is 0 if the method has not been called yet.
        
            Returns:
                the number of evaluations of the objective function.
        
        
        """
        ...
    def getFunctionValueAccuracy(self) -> float:
        """
            Get the function value accuracy of the solver. If :code:`v` is a value returned by the solver for a function :code:`f`,
            then by contract, :code:`|f(v)|` should be less than or equal to the function value accuracy configured for the solver.
        
            Returns:
                the function value accuracy.
        
        
        """
        ...
    def getMaxEvaluations(self) -> int:
        """
            Get the maximum number of function evaluations.
        
            Returns:
                the maximum number of function evaluations.
        
        
        """
        ...
    def getRelativeAccuracy(self) -> float:
        """
            Get the relative accuracy of the solver. The contract for relative accuracy is the same as
            :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.getAbsoluteAccuracy`, but using relative,
            rather than absolute error. If ρ is the relative accuracy configured for a solver and :code:`v` is a value returned,
            then a root of the function should exist somewhere in the interval (:code:`v` - ρ :code:`v`, :code:`v` + ρ :code:`v`).
        
            Returns:
                the relative accuracy.
        
        
        """
        ...
    @typing.overload
    def solve(self, int: int, func: _BaseUnivariateSolver__Func, double: float) -> float:
        """
            Solve for a zero root in the given interval. A solver may require that the interval brackets a single zero root. Solvers
            that do require bracketing should be able to handle the case where one of the endpoints is itself a root.
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`): Function to solve.
                min (double): Lower bound for the interval.
                max (double): Upper bound for the interval.
        
            Returns:
                a value where the function is zero.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the arguments do not satisfy the requirements specified by the solver.
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the allowed number of evaluations is exceeded.
        
            Solve for a zero in the given interval, start at :code:`startValue`. A solver may require that the interval brackets a
            single zero root. Solvers that do require bracketing should be able to handle the case where one of the endpoints is
            itself a root.
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`): Function to solve.
                min (double): Lower bound for the interval.
                max (double): Upper bound for the interval.
                startValue (double): Start value to use.
        
            Returns:
                a value where the function is zero.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the arguments do not satisfy the requirements specified by the solver.
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the allowed number of evaluations is exceeded.
        
            Solve for a zero in the vicinity of :code:`startValue`.
        
            Parameters:
                f (int): Function to solve.
                startValue (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`): Start value to use.
                maxEval (double): Maximum number of evaluations.
        
            Returns:
                a value where the function is zero.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the arguments do not satisfy the requirements specified by the solver.
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the allowed number of evaluations is exceeded.
        
        
        """
        ...
    @typing.overload
    def solve(self, int: int, func: _BaseUnivariateSolver__Func, double: float, double2: float) -> float: ...
    @typing.overload
    def solve(self, int: int, func: _BaseUnivariateSolver__Func, double: float, double2: float, double3: float) -> float: ...

class UnivariateSolverUtils:
    @typing.overload
    @staticmethod
    def bracket(univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, double3: float) -> typing.MutableSequence[float]: ...
    @typing.overload
    @staticmethod
    def bracket(univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, double3: float, int: int) -> typing.MutableSequence[float]: ...
    @staticmethod
    def forceSide(int: int, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], bracketedUnivariateSolver: 'BracketedUnivariateSolver'[typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable]], double: float, double2: float, double3: float, allowedSolution: AllowedSolution) -> float: ...
    @staticmethod
    def isBracketing(univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float) -> bool: ...
    @staticmethod
    def isSequence(double: float, double2: float, double3: float) -> bool: ...
    @staticmethod
    def midpoint(double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def solve(univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float) -> float: ...
    @typing.overload
    @staticmethod
    def solve(univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, double3: float) -> float: ...
    @staticmethod
    def verifyBracketing(univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float) -> None: ...
    @staticmethod
    def verifyInterval(double: float, double2: float) -> None: ...
    @staticmethod
    def verifyIntervalStrict(double: float, double2: float) -> None: ...
    @staticmethod
    def verifySequence(double: float, double2: float, double3: float) -> None: ...
    @staticmethod
    def verifySequenceStrict(double: float, double2: float, double3: float) -> None: ...

_BaseAbstractUnivariateSolver__F = typing.TypeVar('_BaseAbstractUnivariateSolver__F', bound=fr.cnes.sirius.patrius.math.analysis.UnivariateFunction)  # <F>
class BaseAbstractUnivariateSolver(BaseUnivariateSolver[_BaseAbstractUnivariateSolver__F], java.io.Serializable, typing.Generic[_BaseAbstractUnivariateSolver__F]):
    """
    public abstract class BaseAbstractUnivariateSolver<F extends :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`<F>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Provide a default implementation for several functions useful to generic solvers.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    def getAbsoluteAccuracy(self) -> float:
        """
            Get the absolute accuracy of the solver. Solutions returned by the solver should be accurate to this tolerance, i.e., if
            ε is the absolute accuracy of the solver and :code:`v` is a value returned by one of the :code:`solve` methods, then a
            root of the function should exist somewhere in the interval (:code:`v` - ε, :code:`v` + ε).
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.getAbsoluteAccuracy` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`
        
            Returns:
                the absolute accuracy.
        
        
        """
        ...
    def getEvaluations(self) -> int:
        """
            Get the number of evaluations of the objective function. The number of evaluations corresponds to the last call to the
            :code:`optimize` method. It is 0 if the method has not been called yet.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.getEvaluations` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`
        
            Returns:
                the number of evaluations of the objective function.
        
        
        """
        ...
    def getFunctionValueAccuracy(self) -> float:
        """
            Get the function value accuracy of the solver. If :code:`v` is a value returned by the solver for a function :code:`f`,
            then by contract, :code:`|f(v)|` should be less than or equal to the function value accuracy configured for the solver.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.getFunctionValueAccuracy` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`
        
            Returns:
                the function value accuracy.
        
        
        """
        ...
    def getMax(self) -> float:
        """
        
            Returns:
                the higher end of the search interval.
        
        
        """
        ...
    def getMaxEvaluations(self) -> int:
        """
            Get the maximum number of function evaluations.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.getMaxEvaluations` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`
        
            Returns:
                the maximum number of function evaluations.
        
        
        """
        ...
    def getMin(self) -> float:
        """
        
            Returns:
                the lower end of the search interval.
        
        
        """
        ...
    def getRelativeAccuracy(self) -> float:
        """
            Get the relative accuracy of the solver. The contract for relative accuracy is the same as
            :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.getAbsoluteAccuracy`, but using relative,
            rather than absolute error. If ρ is the relative accuracy configured for a solver and :code:`v` is a value returned,
            then a root of the function should exist somewhere in the interval (:code:`v` - ρ :code:`v`, :code:`v` + ρ :code:`v`).
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.getRelativeAccuracy` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`
        
            Returns:
                the relative accuracy.
        
        
        """
        ...
    def getStartValue(self) -> float:
        """
        
            Returns:
                the initial guess.
        
        
        """
        ...
    @typing.overload
    def solve(self, int: int, f: _BaseAbstractUnivariateSolver__F, double: float) -> float:
        """
            Solve for a zero in the given interval, start at :code:`startValue`. A solver may require that the interval brackets a
            single zero root. Solvers that do require bracketing should be able to handle the case where one of the endpoints is
            itself a root.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.solve` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseAbstractUnivariateSolver`): Function to solve.
                min (double): Lower bound for the interval.
                max (double): Upper bound for the interval.
                startValue (double): Start value to use.
        
            Returns:
                a value where the function is zero.
        
            Solve for a zero root in the given interval. A solver may require that the interval brackets a single zero root. Solvers
            that do require bracketing should be able to handle the case where one of the endpoints is itself a root.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.solve` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseAbstractUnivariateSolver`): Function to solve.
                min (double): Lower bound for the interval.
                max (double): Upper bound for the interval.
        
            Returns:
                a value where the function is zero.
        
            Solve for a zero in the vicinity of :code:`startValue`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.solve` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseAbstractUnivariateSolver`): Function to solve.
                startValue (double): Start value to use.
        
            Returns:
                a value where the function is zero.
        
        
        """
        ...
    @typing.overload
    def solve(self, int: int, f: _BaseAbstractUnivariateSolver__F, double: float, double2: float) -> float: ...
    @typing.overload
    def solve(self, int: int, f: _BaseAbstractUnivariateSolver__F, double: float, double2: float, double3: float) -> float: ...

_BracketedUnivariateSolver__Func = typing.TypeVar('_BracketedUnivariateSolver__Func', bound=fr.cnes.sirius.patrius.math.analysis.UnivariateFunction)  # <Func>
class BracketedUnivariateSolver(BaseUnivariateSolver[_BracketedUnivariateSolver__Func], typing.Generic[_BracketedUnivariateSolver__Func]):
    """
    public interface BracketedUnivariateSolver<Func extends :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`> extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`<Func>
    
        Interface for :class:`~fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver` that maintain a bracketed solution.
        There are several advantages to having such root-finding algorithms:
    
          - The bracketed solution guarantees that the root is kept within the interval. As such, these algorithms generally also
            guarantee convergence.
          - The bracketed solution means that we have the opportunity to only return roots that are greater than or equal to the
            actual root, or are less than or equal to the actual root. That is, we can control whether under-approximations and
            over-approximations are :class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`. Other root-finding
            algorithms can usually only guarantee that the solution (the root that was found) is around the actual root.
    
    
        For backwards compatibility, all root-finding algorithms must have
        :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution.ANY_SIDE` as default for the allowed solutions.
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`
    """
    @typing.overload
    def solve(self, int: int, func: _BracketedUnivariateSolver__Func, double: float) -> float:
        """
            Solve for a zero in the given interval. A solver may require that the interval brackets a single zero root. Solvers that
            do require bracketing should be able to handle the case where one of the endpoints is itself a root.
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver`): Function to solve.
                min (double): Lower bound for the interval.
                max (double): Upper bound for the interval.
                allowedSolution (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`): The kind of solutions that the root-finding algorithm may accept as solutions.
        
            Returns:
                A value where the function is zero.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the arguments do not satisfy the requirements specified by the solver.
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the allowed number of evaluations is exceeded.
        
            Solve for a zero in the given interval, start at :code:`startValue`. A solver may require that the interval brackets a
            single zero root. Solvers that do require bracketing should be able to handle the case where one of the endpoints is
            itself a root.
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver`): Function to solve.
                min (double): Lower bound for the interval.
                max (double): Upper bound for the interval.
                startValue (double): Start value to use.
                allowedSolution (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`): The kind of solutions that the root-finding algorithm may accept as solutions.
        
            Returns:
                A value where the function is zero.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the arguments do not satisfy the requirements specified by the solver.
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the allowed number of evaluations is exceeded.
        
        
        """
        ...
    @typing.overload
    def solve(self, int: int, func: _BracketedUnivariateSolver__Func, double: float, double2: float) -> float: ...
    @typing.overload
    def solve(self, int: int, func: _BracketedUnivariateSolver__Func, double: float, double2: float, double3: float) -> float: ...
    @typing.overload
    def solve(self, int: int, func: _BracketedUnivariateSolver__Func, double: float, double2: float, double3: float, allowedSolution: AllowedSolution) -> float: ...
    @typing.overload
    def solve(self, int: int, func: _BracketedUnivariateSolver__Func, double: float, double2: float, allowedSolution: AllowedSolution) -> float: ...

class PolynomialSolver(BaseUnivariateSolver[fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction]):
    """
    public interface PolynomialSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`<:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction`>
    
        Interface for (polynomial) root-finding algorithms. Implementations will search for only one zero in the given interval.
    
        Since:
            3.0
    """
    ...

class UnivariateDifferentiableSolver(BaseUnivariateSolver[fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction]):
    """
    public interface UnivariateDifferentiableSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`<:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`>
    
        Interface for (univariate real) rootfinding algorithms. Implementations will search for only one zero in the given
        interval.
    
        Since:
            3.1
    """
    ...

class UnivariateSolver(BaseUnivariateSolver[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction]):
    """
    public interface UnivariateSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`<:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`>
    
        Interface for (univariate real) root-finding algorithms. Implementations will search for only one zero in the given
        interval.
    """
    ...

class AbstractPolynomialSolver(BaseAbstractUnivariateSolver[fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction], PolynomialSolver):
    """
    public abstract class AbstractPolynomialSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseAbstractUnivariateSolver`<:class:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction`> implements :class:`~fr.cnes.sirius.patrius.math.analysis.solver.PolynomialSolver`
    
        Base class for solvers.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    ...

class AbstractUnivariateDifferentiableSolver(BaseAbstractUnivariateSolver[fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction], UnivariateDifferentiableSolver):
    """
    public abstract class AbstractUnivariateDifferentiableSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseAbstractUnivariateSolver`<:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`> implements :class:`~fr.cnes.sirius.patrius.math.analysis.solver.UnivariateDifferentiableSolver`
    
        Provide a default implementation for several functions useful to generic solvers.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    ...

class AbstractUnivariateSolver(BaseAbstractUnivariateSolver[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction], UnivariateSolver):
    """
    public abstract class AbstractUnivariateSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseAbstractUnivariateSolver`<:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`> implements :class:`~fr.cnes.sirius.patrius.math.analysis.solver.UnivariateSolver`
    
        Base class for solvers.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    ...

class BaseSecantSolver(AbstractUnivariateSolver, BracketedUnivariateSolver[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction]):
    """
    public abstract class BaseSecantSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.AbstractUnivariateSolver` implements :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver`<:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`>
    
        Base class for all bracketing *Secant*-based methods for root-finding (approximating a zero of a univariate real
        function).
    
        Implementation of the :class:`~fr.cnes.sirius.patrius.math.analysis.solver.RegulaFalsiSolver` and
        :class:`~fr.cnes.sirius.patrius.math.analysis.solver.IllinoisSolver` methods is based on the following article: M.
        Dowell and P. Jarratt, *A modified regula falsi method for computing the root of an equation*, BIT Numerical
        Mathematics, volume 11, number 2, pages 168-174, Springer, 1971.
    
        Implementation of the :class:`~fr.cnes.sirius.patrius.math.analysis.solver.PegasusSolver` method is based on the
        following article: M. Dowell and P. Jarratt, *The "Pegasus" method for computing the root of an equation*, BIT Numerical
        Mathematics, volume 12, number 4, pages 503-508, Springer, 1972.
    
        The :class:`~fr.cnes.sirius.patrius.math.analysis.solver.SecantSolver` method is *not* a bracketing method, so it is not
        implemented here. It has a separate implementation.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def solve(self, int: int, f: fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, double: float) -> float:
        """
            Solve for a zero in the given interval. A solver may require that the interval brackets a single zero root. Solvers that
            do require bracketing should be able to handle the case where one of the endpoints is itself a root.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver.solve` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver`
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Function to solve.
                min (double): Lower bound for the interval.
                max (double): Upper bound for the interval.
                allowedSolution (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`): The kind of solutions that the root-finding algorithm may accept as solutions.
        
            Returns:
                A value where the function is zero.
        
            Solve for a zero in the given interval, start at :code:`startValue`. A solver may require that the interval brackets a
            single zero root. Solvers that do require bracketing should be able to handle the case where one of the endpoints is
            itself a root.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver.solve` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver`
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Function to solve.
                min (double): Lower bound for the interval.
                max (double): Upper bound for the interval.
                startValue (double): Start value to use.
                allowedSolution (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`): The kind of solutions that the root-finding algorithm may accept as solutions.
        
            Returns:
                A value where the function is zero.
        
            Solve for a zero in the given interval, start at :code:`startValue`. A solver may require that the interval brackets a
            single zero root. Solvers that do require bracketing should be able to handle the case where one of the endpoints is
            itself a root.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.solve` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseAbstractUnivariateSolver.solve` in
                class :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseAbstractUnivariateSolver`
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Function to solve.
                min (double): Lower bound for the interval.
                max (double): Upper bound for the interval.
                startValue (double): Start value to use.
        
            Returns:
                a value where the function is zero.
        
        
        """
        ...
    @typing.overload
    def solve(self, int: int, f: fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, double: float, double2: float) -> float: ...
    @typing.overload
    def solve(self, int: int, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, double3: float) -> float: ...
    @typing.overload
    def solve(self, int: int, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, double3: float, allowedSolution: AllowedSolution) -> float: ...
    @typing.overload
    def solve(self, int: int, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, allowedSolution: AllowedSolution) -> float: ...

class BisectionSolver(AbstractUnivariateSolver):
    """
    public class BisectionSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.AbstractUnivariateSolver`
    
        Implements the ` bisection algorithm <http://mathworld.wolfram.com/Bisection.html>` for finding zeros of univariate real
        functions.
    
        The function should be continuous but not necessarily smooth.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...

class BracketingNthOrderBrentSolver(AbstractUnivariateSolver, BracketedUnivariateSolver[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction]):
    """
    public class BracketingNthOrderBrentSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.AbstractUnivariateSolver` implements :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver`<:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`>
    
        This class implements a modification of the ` Brent algorithm <http://mathworld.wolfram.com/BrentsMethod.html>`.
    
        The changes with respect to the original Brent algorithm are:
    
          - the returned value is chosen in the current interval according to user specified
            :class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`,
          - the maximal order for the invert polynomial root search is user-specified instead of being invert quadratic only
    
        The given interval must bracket the root.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, int: int): ...
    @typing.overload
    def __init__(self, double: float, double2: float, int: int): ...
    @typing.overload
    def __init__(self, double: float, int: int): ...
    def getMaximalOrder(self) -> int:
        """
            Get the maximal order.
        
            Returns:
                maximal order
        
        
        """
        ...
    @typing.overload
    def solve(self, int: int, f: fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, double: float) -> float:
        """
            Solve for a zero in the given interval. A solver may require that the interval brackets a single zero root. Solvers that
            do require bracketing should be able to handle the case where one of the endpoints is itself a root.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver.solve` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver`
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Function to solve.
                min (double): Lower bound for the interval.
                max (double): Upper bound for the interval.
                allowedSolution (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`): The kind of solutions that the root-finding algorithm may accept as solutions.
        
            Returns:
                A value where the function is zero.
        
            Solve for a zero in the given interval, start at :code:`startValue`. A solver may require that the interval brackets a
            single zero root. Solvers that do require bracketing should be able to handle the case where one of the endpoints is
            itself a root.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver.solve` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BracketedUnivariateSolver`
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`): Function to solve.
                min (double): Lower bound for the interval.
                max (double): Upper bound for the interval.
                startValue (double): Start value to use.
                allowedSolution (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`): The kind of solutions that the root-finding algorithm may accept as solutions.
        
            Returns:
                A value where the function is zero.
        
        
        """
        ...
    @typing.overload
    def solve(self, int: int, f: fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, double: float, double2: float) -> float: ...
    @typing.overload
    def solve(self, int: int, f: fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, double: float, double2: float, double3: float) -> float: ...
    @typing.overload
    def solve(self, int: int, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, double3: float, allowedSolution: AllowedSolution) -> float: ...
    @typing.overload
    def solve(self, int: int, univariateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, typing.Callable], double: float, double2: float, allowedSolution: AllowedSolution) -> float: ...

class BrentSolver(AbstractUnivariateSolver):
    """
    public class BrentSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.AbstractUnivariateSolver`
    
        This class implements the ` Brent algorithm <http://mathworld.wolfram.com/BrentsMethod.html>` for finding zeros of real
        univariate functions. The function should be continuous but not necessarily smooth. The :code:`solve` method returns a
        zero :code:`x` of the function :code:`f` in the given interval :code:`[a, b]` to within a tolerance :code:`6 eps abs(x)
        + t` where :code:`eps` is the relative accuracy and :code:`t` is the absolute accuracy. The given interval must bracket
        the root.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...

class LaguerreSolver(AbstractPolynomialSolver):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...
    def doSolve(self) -> float: ...
    def solveAllComplex(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.complex.Complex]: ...
    def solveComplex(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], double2: float) -> fr.cnes.sirius.patrius.math.complex.Complex: ...

class MullerSolver(AbstractUnivariateSolver):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...

class MullerSolver2(AbstractUnivariateSolver):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...

class NewtonRaphsonSolver(AbstractUnivariateDifferentiableSolver):
    """
    public class NewtonRaphsonSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.AbstractUnivariateDifferentiableSolver`
    
        Implements ` Newton's Method <http://mathworld.wolfram.com/NewtonsMethod.html>` for finding zeros of real univariate
        differentiable functions.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def solve(self, int: int, f: fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, double: float) -> float:
        """
            Find a zero near the midpoint of :code:`min` and :code:`max`.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver.solve` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseUnivariateSolver`
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseAbstractUnivariateSolver.solve` in
                class :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseAbstractUnivariateSolver`
        
            Parameters:
                f (int): Function to solve.
                min (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`): Lower bound for the interval.
                max (double): Upper bound for the interval.
                maxEval (double): Maximum number of evaluations.
        
            Returns:
                the value where the function is zero.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.TooManyEvaluationsException`: if the maximum evaluation count is exceeded.
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooLargeException`: if :code:`min >= max`.
        
        
        """
        ...
    @typing.overload
    def solve(self, int: int, f: fr.cnes.sirius.patrius.math.analysis.UnivariateFunction, double: float, double2: float, double3: float) -> float: ...
    @typing.overload
    def solve(self, int: int, univariateDifferentiableFunction: fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction, double: float, double2: float) -> float: ...

class RiddersSolver(AbstractUnivariateSolver):
    """
    public class RiddersSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.AbstractUnivariateSolver`
    
        Implements the ` Ridders' Method <http://mathworld.wolfram.com/RiddersMethod.html>` for root finding of real univariate
        functions. For reference, see C. Ridders, *A new algorithm for computing a single root of a real continuous function*,
        IEEE Transactions on Circuits and Systems, 26 (1979), 979 - 980.
    
        The function should be continuous but not necessarily smooth.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...

class SecantSolver(AbstractUnivariateSolver):
    """
    public class SecantSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.AbstractUnivariateSolver`
    
        Implements the *Secant* method for root-finding (approximating a zero of a univariate real function). The solution that
        is maintained is not bracketed, and as such convergence is not guaranteed.
    
        Implementation based on the following article: M. Dowell and P. Jarratt, *A modified regula falsi method for computing
        the root of an equation*, BIT Numerical Mathematics, volume 11, number 2, pages 168-174, Springer, 1971.
    
        Note that since release 3.0 this class implements the actual *Secant* algorithm, and not a modified one. As such, the
        3.0 version is not backwards compatible with previous versions. To use an algorithm similar to the pre-3.0 releases, use
        the :class:`~fr.cnes.sirius.patrius.math.analysis.solver.IllinoisSolver` algorithm or the
        :class:`~fr.cnes.sirius.patrius.math.analysis.solver.PegasusSolver` algorithm.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...

class IllinoisSolver(BaseSecantSolver):
    """
    public class IllinoisSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseSecantSolver`
    
        Implements the *Illinois* method for root-finding (approximating a zero of a univariate real function). It is a modified
        :class:`~fr.cnes.sirius.patrius.math.analysis.solver.RegulaFalsiSolver` method.
    
        Like the *Regula Falsi* method, convergence is guaranteed by maintaining a bracketed solution. The *Illinois* method
        however, should converge much faster than the original *Regula Falsi* method. Furthermore, this implementation of the
        *Illinois* method should not suffer from the same implementation issues as the *Regula Falsi* method, which may fail to
        convergence in certain cases.
    
        The *Illinois* method assumes that the function is continuous, but not necessarily smooth.
    
        Implementation based on the following article: M. Dowell and P. Jarratt, *A modified regula falsi method for computing
        the root of an equation*, BIT Numerical Mathematics, volume 11, number 2, pages 168-174, Springer, 1971.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...

class PegasusSolver(BaseSecantSolver):
    """
    public class PegasusSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseSecantSolver`
    
        Implements the *Pegasus* method for root-finding (approximating a zero of a univariate real function). It is a modified
        :class:`~fr.cnes.sirius.patrius.math.analysis.solver.RegulaFalsiSolver` method.
    
        Like the *Regula Falsi* method, convergence is guaranteed by maintaining a bracketed solution. The *Pegasus* method
        however, should converge much faster than the original *Regula Falsi* method. Furthermore, this implementation of the
        *Pegasus* method should not suffer from the same implementation issues as the *Regula Falsi* method, which may fail to
        convergence in certain cases. Also, the *Pegasus* method should converge faster than the
        :class:`~fr.cnes.sirius.patrius.math.analysis.solver.IllinoisSolver` method, another *Regula Falsi*-based method.
    
        The *Pegasus* method assumes that the function is continuous, but not necessarily smooth.
    
        Implementation based on the following article: M. Dowell and P. Jarratt, *The "Pegasus" method for computing the root of
        an equation*, BIT Numerical Mathematics, volume 12, number 4, pages 503-508, Springer, 1972.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...

class RegulaFalsiSolver(BaseSecantSolver):
    """
    public class RegulaFalsiSolver extends :class:`~fr.cnes.sirius.patrius.math.analysis.solver.BaseSecantSolver`
    
        Implements the *Regula Falsi* or *False position* method for root-finding (approximating a zero of a univariate real
        function). It is a modified :class:`~fr.cnes.sirius.patrius.math.analysis.solver.SecantSolver` method.
    
        The *Regula Falsi* method is included for completeness, for testing purposes, for educational purposes, for comparison
        to other algorithms, etc. It is however **not** intended to be used for actual problems, as one of the bounds often
        remains fixed, resulting in very slow convergence. Instead, one of the well-known modified *Regula Falsi* algorithms can
        be used (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.IllinoisSolver` or
        :class:`~fr.cnes.sirius.patrius.math.analysis.solver.PegasusSolver`). These two algorithms solve the fundamental issues
        of the original *Regula Falsi* algorithm, and greatly out-performs it for most, if not all, (practical) functions.
    
        Unlike the *Secant* method, the *Regula Falsi* guarantees convergence, by maintaining a bracketed solution. Note
        however, that due to the finite/limited precision of Java's `null
        <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>` type, which is used in this
        implementation, the algorithm may get stuck in a situation where it no longer makes any progress. Such cases are
        detected and result in a :code:`ConvergenceException` exception being thrown. In other words, the algorithm
        theoretically guarantees convergence, but the implementation does not.
    
        The *Regula Falsi* method assumes that the function is continuous, but not necessarily smooth.
    
        Implementation based on the following article: M. Dowell and P. Jarratt, *A modified regula falsi method for computing
        the root of an equation*, BIT Numerical Mathematics, volume 11, number 2, pages 168-174, Springer, 1971.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.analysis.solver")``.

    AbstractPolynomialSolver: typing.Type[AbstractPolynomialSolver]
    AbstractUnivariateDifferentiableSolver: typing.Type[AbstractUnivariateDifferentiableSolver]
    AbstractUnivariateSolver: typing.Type[AbstractUnivariateSolver]
    AllowedSolution: typing.Type[AllowedSolution]
    BaseAbstractUnivariateSolver: typing.Type[BaseAbstractUnivariateSolver]
    BaseSecantSolver: typing.Type[BaseSecantSolver]
    BaseUnivariateSolver: typing.Type[BaseUnivariateSolver]
    BisectionSolver: typing.Type[BisectionSolver]
    BracketedUnivariateSolver: typing.Type[BracketedUnivariateSolver]
    BracketingNthOrderBrentSolver: typing.Type[BracketingNthOrderBrentSolver]
    BrentSolver: typing.Type[BrentSolver]
    IllinoisSolver: typing.Type[IllinoisSolver]
    LaguerreSolver: typing.Type[LaguerreSolver]
    MullerSolver: typing.Type[MullerSolver]
    MullerSolver2: typing.Type[MullerSolver2]
    NewtonRaphsonSolver: typing.Type[NewtonRaphsonSolver]
    PegasusSolver: typing.Type[PegasusSolver]
    PolynomialSolver: typing.Type[PolynomialSolver]
    RegulaFalsiSolver: typing.Type[RegulaFalsiSolver]
    RiddersSolver: typing.Type[RiddersSolver]
    SecantSolver: typing.Type[SecantSolver]
    UnivariateDifferentiableSolver: typing.Type[UnivariateDifferentiableSolver]
    UnivariateSolver: typing.Type[UnivariateSolver]
    UnivariateSolverUtils: typing.Type[UnivariateSolverUtils]
