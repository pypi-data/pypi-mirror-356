
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math
import fr.cnes.sirius.patrius.math.analysis.solver
import java.lang
import typing



class BracketingNthOrderBrentSolverDFP:
    """
    public class BracketingNthOrderBrentSolverDFP extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class implements a modification of the ` Brent algorithm <http://mathworld.wolfram.com/BrentsMethod.html>`.
    
        The changes with respect to the original Brent algorithm are:
    
          - the returned value is chosen in the current interval according to user specified
            :class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`,
          - the maximal order for the invert polynomial root search is user-specified instead of being invert quadratic only
    
        The given interval must bracket the root.
    """
    def __init__(self, dfp: 'Dfp', dfp2: 'Dfp', dfp3: 'Dfp', int: int): ...
    def getAbsoluteAccuracy(self) -> 'Dfp':
        """
            Get the absolute accuracy.
        
            Returns:
                absolute accuracy
        
        
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
    def getFunctionValueAccuracy(self) -> 'Dfp':
        """
            Get the function accuracy.
        
            Returns:
                function accuracy
        
        
        """
        ...
    def getMaxEvaluations(self) -> int:
        """
            Get the maximal number of function evaluations.
        
            Returns:
                the maximal number of function evaluations.
        
        
        """
        ...
    def getMaximalOrder(self) -> int:
        """
            Get the maximal order.
        
            Returns:
                maximal order
        
        
        """
        ...
    def getRelativeAccuracy(self) -> 'Dfp':
        """
            Get the relative accuracy.
        
            Returns:
                relative accuracy
        
        
        """
        ...
    @typing.overload
    def solve(self, int: int, univariateDfpFunction: typing.Union['UnivariateDfpFunction', typing.Callable], dfp: 'Dfp', dfp2: 'Dfp', allowedSolution: fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution) -> 'Dfp':
        """
            Solve for a zero in the given interval. A solver may require that the interval brackets a single zero root. Solvers that
            do require bracketing should be able to handle the case where one of the endpoints is itself a root.
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.dfp.UnivariateDfpFunction`): Function to solve.
                min (:class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`): Lower bound for the interval.
                max (:class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`): Upper bound for the interval.
                allowedSolution (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`): The kind of solutions that the root-finding algorithm may accept as solutions.
        
            Returns:
                a value where the function is zero.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if f is null.
                :class:`~fr.cnes.sirius.patrius.math.exception.NoBracketingException`: if root cannot be bracketed
        
            Solve for a zero in the given interval, start at :code:`startValue`. A solver may require that the interval brackets a
            single zero root. Solvers that do require bracketing should be able to handle the case where one of the endpoints is
            itself a root.
        
            Parameters:
                maxEval (int): Maximum number of evaluations.
                f (:class:`~fr.cnes.sirius.patrius.math.dfp.UnivariateDfpFunction`): Function to solve.
                min (:class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`): Lower bound for the interval.
                max (:class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`): Upper bound for the interval.
                startValue (:class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`): Start value to use.
                allowedSolution (:class:`~fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution`): The kind of solutions that the root-finding algorithm may accept as solutions.
        
            Returns:
                a value where the function is zero.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if f is null.
                :class:`~fr.cnes.sirius.patrius.math.exception.NoBracketingException`: if root cannot be bracketed
        
        
        """
        ...
    @typing.overload
    def solve(self, int: int, univariateDfpFunction: typing.Union['UnivariateDfpFunction', typing.Callable], dfp: 'Dfp', dfp2: 'Dfp', dfp3: 'Dfp', allowedSolution: fr.cnes.sirius.patrius.math.analysis.solver.AllowedSolution) -> 'Dfp': ...

class Dfp(fr.cnes.sirius.patrius.math.FieldElement['Dfp']):
    RADIX: typing.ClassVar[int] = ...
    MIN_EXP: typing.ClassVar[int] = ...
    MAX_EXP: typing.ClassVar[int] = ...
    ERR_SCALE: typing.ClassVar[int] = ...
    FINITE: typing.ClassVar[int] = ...
    INFINITE: typing.ClassVar[int] = ...
    SNAN: typing.ClassVar[int] = ...
    QNAN: typing.ClassVar[int] = ...
    def __init__(self, dfp: 'Dfp'): ...
    def abs(self) -> 'Dfp': ...
    def add(self, dfp: 'Dfp') -> 'Dfp': ...
    def ceil(self) -> 'Dfp': ...
    def classify(self) -> int: ...
    @staticmethod
    def copysign(dfp: 'Dfp', dfp2: 'Dfp') -> 'Dfp': ...
    @typing.overload
    def divide(self, dfp: 'Dfp') -> 'Dfp': ...
    @typing.overload
    def divide(self, int: int) -> 'Dfp': ...
    def dotrap(self, int: int, string: str, dfp: 'Dfp', dfp2: 'Dfp') -> 'Dfp': ...
    def equals(self, object: typing.Any) -> bool: ...
    def floor(self) -> 'Dfp': ...
    def getField(self) -> 'DfpField': ...
    def getOne(self) -> 'Dfp': ...
    def getRadixDigits(self) -> int: ...
    def getTwo(self) -> 'Dfp': ...
    def getZero(self) -> 'Dfp': ...
    def greaterThan(self, dfp: 'Dfp') -> bool: ...
    def hashCode(self) -> int: ...
    def intValue(self) -> int: ...
    def isInfinite(self) -> bool: ...
    def isNaN(self) -> bool: ...
    def isZero(self) -> bool: ...
    def lessThan(self, dfp: 'Dfp') -> bool: ...
    def log10(self) -> int: ...
    def log10K(self) -> int: ...
    @typing.overload
    def multiply(self, dfp: 'Dfp') -> 'Dfp': ...
    @typing.overload
    def multiply(self, int: int) -> 'Dfp': ...
    def negate(self) -> 'Dfp': ...
    def negativeOrNull(self) -> bool: ...
    @typing.overload
    def newInstance(self) -> 'Dfp': ...
    @typing.overload
    def newInstance(self, byte: int) -> 'Dfp': ...
    @typing.overload
    def newInstance(self, byte: int, byte2: int) -> 'Dfp': ...
    @typing.overload
    def newInstance(self, double: float) -> 'Dfp': ...
    @typing.overload
    def newInstance(self, dfp: 'Dfp') -> 'Dfp': ...
    @typing.overload
    def newInstance(self, int: int) -> 'Dfp': ...
    @typing.overload
    def newInstance(self, string: str) -> 'Dfp': ...
    @typing.overload
    def newInstance(self, long: int) -> 'Dfp': ...
    def nextAfter(self, dfp: 'Dfp') -> 'Dfp': ...
    def positiveOrNull(self) -> bool: ...
    def power10(self, int: int) -> 'Dfp': ...
    def power10K(self, int: int) -> 'Dfp': ...
    def reciprocal(self) -> 'Dfp': ...
    def remainder(self, dfp: 'Dfp') -> 'Dfp': ...
    def rint(self) -> 'Dfp': ...
    def sqrt(self) -> 'Dfp': ...
    def strictlyNegative(self) -> bool: ...
    def strictlyPositive(self) -> bool: ...
    def subtract(self, dfp: 'Dfp') -> 'Dfp': ...
    def toDouble(self) -> float: ...
    def toSplitDouble(self) -> typing.MutableSequence[float]: ...
    def toString(self) -> str: ...
    def unequal(self, dfp: 'Dfp') -> bool: ...

class DfpField(fr.cnes.sirius.patrius.math.Field[Dfp]):
    FLAG_INVALID: typing.ClassVar[int] = ...
    FLAG_DIV_ZERO: typing.ClassVar[int] = ...
    FLAG_OVERFLOW: typing.ClassVar[int] = ...
    FLAG_UNDERFLOW: typing.ClassVar[int] = ...
    FLAG_INEXACT: typing.ClassVar[int] = ...
    def __init__(self, int: int): ...
    def clearIEEEFlags(self) -> None: ...
    @staticmethod
    def computeExp(dfp: Dfp, dfp2: Dfp) -> Dfp: ...
    @staticmethod
    def computeLn(dfp: Dfp, dfp2: Dfp, dfp3: Dfp) -> Dfp: ...
    def getE(self) -> Dfp: ...
    def getESplit(self) -> typing.MutableSequence[Dfp]: ...
    def getIEEEFlags(self) -> int: ...
    def getLn10(self) -> Dfp: ...
    def getLn2(self) -> Dfp: ...
    def getLn2Split(self) -> typing.MutableSequence[Dfp]: ...
    def getLn5(self) -> Dfp: ...
    def getLn5Split(self) -> typing.MutableSequence[Dfp]: ...
    def getOne(self) -> Dfp: ...
    def getPi(self) -> Dfp: ...
    def getPiSplit(self) -> typing.MutableSequence[Dfp]: ...
    def getRadixDigits(self) -> int: ...
    def getRoundingMode(self) -> 'DfpField.RoundingMode': ...
    def getRuntimeClass(self) -> typing.Type[fr.cnes.sirius.patrius.math.FieldElement[Dfp]]: ...
    def getSqr2(self) -> Dfp: ...
    def getSqr2Reciprocal(self) -> Dfp: ...
    def getSqr2Split(self) -> typing.MutableSequence[Dfp]: ...
    def getSqr3(self) -> Dfp: ...
    def getSqr3Reciprocal(self) -> Dfp: ...
    def getTwo(self) -> Dfp: ...
    def getZero(self) -> Dfp: ...
    @typing.overload
    def newDfp(self) -> Dfp: ...
    @typing.overload
    def newDfp(self, byte: int) -> Dfp: ...
    @typing.overload
    def newDfp(self, byte: int, byte2: int) -> Dfp: ...
    @typing.overload
    def newDfp(self, double: float) -> Dfp: ...
    @typing.overload
    def newDfp(self, dfp: Dfp) -> Dfp: ...
    @typing.overload
    def newDfp(self, int: int) -> Dfp: ...
    @typing.overload
    def newDfp(self, string: str) -> Dfp: ...
    @typing.overload
    def newDfp(self, long: int) -> Dfp: ...
    def setIEEEFlags(self, int: int) -> None: ...
    def setIEEEFlagsBits(self, int: int) -> None: ...
    def setRoundingMode(self, roundingMode: 'DfpField.RoundingMode') -> None: ...
    class RoundingMode(java.lang.Enum['DfpField.RoundingMode']):
        ROUND_DOWN: typing.ClassVar['DfpField.RoundingMode'] = ...
        ROUND_UP: typing.ClassVar['DfpField.RoundingMode'] = ...
        ROUND_HALF_UP: typing.ClassVar['DfpField.RoundingMode'] = ...
        ROUND_HALF_DOWN: typing.ClassVar['DfpField.RoundingMode'] = ...
        ROUND_HALF_EVEN: typing.ClassVar['DfpField.RoundingMode'] = ...
        ROUND_HALF_ODD: typing.ClassVar['DfpField.RoundingMode'] = ...
        ROUND_CEIL: typing.ClassVar['DfpField.RoundingMode'] = ...
        ROUND_FLOOR: typing.ClassVar['DfpField.RoundingMode'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'DfpField.RoundingMode': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['DfpField.RoundingMode']: ...

class DfpMath:
    @staticmethod
    def acos(dfp: Dfp) -> Dfp: ...
    @staticmethod
    def asin(dfp: Dfp) -> Dfp: ...
    @staticmethod
    def atan(dfp: Dfp) -> Dfp: ...
    @staticmethod
    def cos(dfp: Dfp) -> Dfp: ...
    @staticmethod
    def exp(dfp: Dfp) -> Dfp: ...
    @staticmethod
    def log(dfp: Dfp) -> Dfp: ...
    @typing.overload
    @staticmethod
    def pow(dfp: Dfp, dfp2: Dfp) -> Dfp: ...
    @typing.overload
    @staticmethod
    def pow(dfp: Dfp, int: int) -> Dfp: ...
    @staticmethod
    def sin(dfp: Dfp) -> Dfp: ...
    @staticmethod
    def tan(dfp: Dfp) -> Dfp: ...

class UnivariateDfpFunction:
    """
    public interface UnivariateDfpFunction
    
        An interface representing a univariate :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp` function.
    """
    def value(self, dfp: Dfp) -> Dfp:
        """
            Compute the value of the function.
        
            Parameters:
                x (:class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`): Point at which the function value should be computed.
        
            Returns:
                the value.
        
            Raises:
                : when the activated method itself can ascertain that preconditions, specified in the API expressed at the level of the
                    activated method, have been violated. In the vast majority of cases where Commons-Math throws IllegalArgumentException,
                    it is the result of argument checking of actual parameters immediately passed to a method.
        
        
        """
        ...

class DfpDec(Dfp):
    """
    public class DfpDec extends :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`
    
        Subclass of :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp` which hides the radix-10000 artifacts of the superclass. This
        should give outward appearances of being a decimal number with DIGITS*4-3 decimal digits. This class can be subclassed
        to appear to be an arbitrary number of decimal digits less than DIGITS*4-3.
    
        Since:
            2.2
    """
    def __init__(self, dfp: Dfp): ...
    @typing.overload
    def newInstance(self) -> Dfp:
        """
            Create an instance with a value of 0. Use this internally in preference to constructors to facilitate subclasses
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.newInstance` in class :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`
        
            Returns:
                a new instance with a value of 0
        
        """
        ...
    @typing.overload
    def newInstance(self, byte: int) -> Dfp:
        """
            Create an instance from a byte value.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.newInstance` in class :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`
        
            Parameters:
                x (byte): value to convert to an instance
        
            Returns:
                a new instance with value x
        
            Create an instance from an int value.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.newInstance` in class :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`
        
            Parameters:
                x (int): value to convert to an instance
        
            Returns:
                a new instance with value x
        
            Create an instance from a long value.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.newInstance` in class :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`
        
            Parameters:
                x (long): value to convert to an instance
        
            Returns:
                a new instance with value x
        
            Create an instance from a double value.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.newInstance` in class :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`
        
            Parameters:
                x (double): value to convert to an instance
        
            Returns:
                a new instance with value x
        
            Create an instance by copying an existing one. Use this internally in preference to constructors to facilitate
            subclasses.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.newInstance` in class :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`
        
            Parameters:
                d (:class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`): instance to copy
        
            Returns:
                a new instance with the same value as d
        
            Create an instance from a String representation. Use this internally in preference to constructors to facilitate
            subclasses.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.newInstance` in class :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`
        
            Parameters:
                s (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): string representation of the instance
        
            Returns:
                a new instance parsed from specified string
        
            Creates an instance with a non-finite value.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.newInstance` in class :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`
        
            Parameters:
                sign (byte): sign of the Dfp to create
                nans (byte): code of the value, must be one of :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.INFINITE`,
                    :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.SNAN`, :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.QNAN`
        
            Returns:
                a new instance with a non-finite value
        
        
        """
        ...
    @typing.overload
    def newInstance(self, byte: int, byte2: int) -> Dfp: ...
    @typing.overload
    def newInstance(self, double: float) -> Dfp: ...
    @typing.overload
    def newInstance(self, dfp: Dfp) -> Dfp: ...
    @typing.overload
    def newInstance(self, int: int) -> Dfp: ...
    @typing.overload
    def newInstance(self, string: str) -> Dfp: ...
    @typing.overload
    def newInstance(self, long: int) -> Dfp: ...
    def nextAfter(self, dfp: Dfp) -> Dfp:
        """
            Returns the next number greater than this one in the direction of x. If this==x then simply returns this.
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.dfp.Dfp.nextAfter` in class :class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`
        
            Parameters:
                x (:class:`~fr.cnes.sirius.patrius.math.dfp.Dfp`): direction where to look at
        
            Returns:
                closest number next to instance in the direction of x
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.dfp")``.

    BracketingNthOrderBrentSolverDFP: typing.Type[BracketingNthOrderBrentSolverDFP]
    Dfp: typing.Type[Dfp]
    DfpDec: typing.Type[DfpDec]
    DfpField: typing.Type[DfpField]
    DfpMath: typing.Type[DfpMath]
    UnivariateDfpFunction: typing.Type[UnivariateDfpFunction]
