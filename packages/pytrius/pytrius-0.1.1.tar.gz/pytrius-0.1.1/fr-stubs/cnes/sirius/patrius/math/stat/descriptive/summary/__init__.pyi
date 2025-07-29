
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.stat.descriptive
import java.io
import jpype
import typing



class Product(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable, fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation):
    """
    public class Product extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation`
    
        Returns the product of the available values.
    
        If there are no values in the dataset, then 1 is returned. If any of the values are :code:`NaN`, then :code:`NaN` is
        returned.
    
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, product: 'Product'): ...
    def clear(self) -> None:
        """
            Clears the internal state of the Statistic
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.clear` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.clear` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
        
        """
        ...
    @typing.overload
    def copy(self) -> 'Product':
        """
            Returns a copy of the statistic with the same internal state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.copy` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                a copy of the statistic
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(product: 'Product', product2: 'Product') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.summary.Product`): Product to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.summary.Product`): Product to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Returns the product of the entries in the specified portion of the input array, or :code:`Double.NaN` if the designated
            subarray is empty.
        
            Throws :code:`MathIllegalArgumentException` if the array is null.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                values (double[]): the input array
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the product of the values or 1 if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the array index parameters are not valid
        
            Also see:
        
        
            Returns the weighted product of the entries in the input array.
        
            Throws :code:`MathIllegalArgumentException` if any of the following are true:
        
              - the values array is null
              - the weights array is null
              - the weights array does not have the same length as the values array
              - the weights array contains one or more infinite values
              - the weights array contains one or more NaN values
              - the weights array contains negative values
        
        
            Uses the formula,
        
            .. code-block: java
            
            
                weighted product = ∏values[i] :sup:`weights[i]` 
             
            that is, the weights are applied as exponents when computing the weighted product.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation`
        
            Parameters:
                values (double[]): the input array
                weights (double[]): the weights array
        
            Returns:
                the product of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the parameters are not valid
        
            Since:
                2.1
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float:
        """
        
            Returns the weighted product of the entries in the specified portion of the input array, or :code:`Double.NaN` if the
            designated subarray is empty.
        
            Throws :code:`MathIllegalArgumentException` if any of the following are true:
        
              - the values array is null
              - the weights array is null
              - the weights array does not have the same length as the values array
              - the weights array contains one or more infinite values
              - the weights array contains one or more NaN values
              - the weights array contains negative values
              - the start and length arguments do not determine a valid array
        
        
            Uses the formula,
        
            .. code-block: java
            
            
                weighted product = ∏values[i] :sup:`weights[i]` 
             
            that is, the weights are applied as exponents when computing the weighted product.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.WeightedEvaluation`
        
            Parameters:
                values (double[]): the input array
                weights (double[]): the weights array
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the product of the values or 1 if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the parameters are not valid
        
            Since:
                2.1
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    def getN(self) -> int:
        """
            Returns the number of values that have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Returns:
                the number of values.
        
        
        """
        ...
    def getResult(self) -> float:
        """
            Returns the current value of the Statistic.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getResult` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.getResult` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                value of the statistic, :code:`Double.NaN` if it has been cleared or just instantiated.
        
        
        """
        ...
    def increment(self, double: float) -> None:
        """
            Updates the internal state of the statistic to reflect the addition of the new value.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.increment` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.increment` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                d (double): the new value.
        
        
        """
        ...

class Sum(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable):
    """
    public class Sum extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Returns the sum of the available values.
    
        If there are no values in the dataset, then 0 is returned. If any of the values are :code:`NaN`, then :code:`NaN` is
        returned.
    
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, sum: 'Sum'): ...
    def clear(self) -> None:
        """
            Clears the internal state of the Statistic
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.clear` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.clear` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
        
        """
        ...
    @typing.overload
    def copy(self) -> 'Sum':
        """
            Returns a copy of the statistic with the same internal state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.copy` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                a copy of the statistic
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(sum: 'Sum', sum2: 'Sum') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.summary.Sum`): Sum to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.summary.Sum`): Sum to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            The sum of the entries in the specified portion of the input array, or 0 if the designated subarray is empty.
        
            Throws :code:`MathIllegalArgumentException` if the array is null.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                values (double[]): the input array
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the sum of the values or 0 if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the array index parameters are not valid
        
            Also see:
        
            The weighted sum of the entries in the the input array.
        
            Throws :code:`MathIllegalArgumentException` if any of the following are true:
        
              - the values array is null
              - the weights array is null
              - the weights array does not have the same length as the values array
              - the weights array contains one or more infinite values
              - the weights array contains one or more NaN values
              - the weights array contains negative values
        
        
            Uses the formula,
        
            .. code-block: java
            
            
                weighted sum = Σ(values[i] * weights[i])
             
        
            Parameters:
                values (double[]): the input array
                weights (double[]): the weights array
        
            Returns:
                the sum of the values or Double.NaN if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the parameters are not valid
        
            Since:
                2.1
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float:
        """
            The weighted sum of the entries in the specified portion of the input array, or 0 if the designated subarray is empty.
        
            Throws :code:`MathIllegalArgumentException` if any of the following are true:
        
              - the values array is null
              - the weights array is null
              - the weights array does not have the same length as the values array
              - the weights array contains one or more infinite values
              - the weights array contains one or more NaN values
              - the weights array contains negative values
              - the start and length arguments do not determine a valid array
        
        
            Uses the formula,
        
            .. code-block: java
            
            
                weighted sum = Σ(values[i] * weights[i])
             
        
            Parameters:
                values (double[]): the input array
                weights (double[]): the weights array
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the sum of the values or 0 if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the parameters are not valid
        
            Since:
                2.1
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float: ...
    def getN(self) -> int:
        """
            Returns the number of values that have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Returns:
                the number of values.
        
        
        """
        ...
    def getResult(self) -> float:
        """
            Returns the current value of the Statistic.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getResult` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.getResult` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                value of the statistic, :code:`Double.NaN` if it has been cleared or just instantiated.
        
        
        """
        ...
    def increment(self, double: float) -> None:
        """
            Updates the internal state of the statistic to reflect the addition of the new value.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.increment` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.increment` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                d (double): the new value.
        
        
        """
        ...

class SumOfLogs(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable):
    """
    public class SumOfLogs extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Returns the sum of the natural logs for this collection of values.
    
        Uses :meth:`~fr.cnes.sirius.patrius.math.util.MathLib.log` to compute the logs. Therefore,
    
          - If any of values are < 0, the result is :code:`NaN.`
          - If all values are non-negative and less than :code:`Double.POSITIVE_INFINITY`, but at least one value is 0, the result
            is :code:`Double.NEGATIVE_INFINITY.`
          - If both :code:`Double.POSITIVE_INFINITY` and :code:`Double.NEGATIVE_INFINITY` are among the values, the result is
            :code:`NaN.`
    
    
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, sumOfLogs: 'SumOfLogs'): ...
    def clear(self) -> None:
        """
            Clears the internal state of the Statistic
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.clear` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.clear` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
        
        """
        ...
    @typing.overload
    def copy(self) -> 'SumOfLogs':
        """
            Returns a copy of the statistic with the same internal state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.copy` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                a copy of the statistic
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(sumOfLogs: 'SumOfLogs', sumOfLogs2: 'SumOfLogs') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.summary.SumOfLogs`): SumOfLogs to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.summary.SumOfLogs`): SumOfLogs to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float:
        """
            Returns the sum of the natural logs of the entries in the specified portion of the input array, or :code:`Double.NaN` if
            the designated subarray is empty.
        
            Throws :code:`MathIllegalArgumentException` if the array is null.
        
            See :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.summary.SumOfLogs`.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                values (double[]): the input array
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the sum of the natural logs of the values or 0 if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the array index parameters are not valid
        
            Also see:
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of values that have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Returns:
                the number of values.
        
        
        """
        ...
    def getResult(self) -> float:
        """
            Returns the current value of the Statistic.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getResult` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.getResult` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                value of the statistic, :code:`Double.NaN` if it has been cleared or just instantiated.
        
        
        """
        ...
    def increment(self, double: float) -> None:
        """
            Updates the internal state of the statistic to reflect the addition of the new value.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.increment` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.increment` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                d (double): the new value.
        
        
        """
        ...

class SumOfSquares(fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic, java.io.Serializable):
    """
    public class SumOfSquares extends :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Returns the sum of the squares of the available values.
    
        If there are no values in the dataset, then 0 is returned. If any of the values are :code:`NaN`, then :code:`NaN` is
        returned.
    
        **Note that this implementation is not synchronized.** If multiple threads access an instance of this class
        concurrently, and at least one of the threads invokes the :code:`increment()` or :code:`clear()` method, it must be
        synchronized externally.
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, sumOfSquares: 'SumOfSquares'): ...
    def clear(self) -> None:
        """
            Clears the internal state of the Statistic
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.clear` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.clear` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
        
        """
        ...
    @typing.overload
    def copy(self) -> 'SumOfSquares':
        """
            Returns a copy of the statistic with the same internal state.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic.copy` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.copy` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                a copy of the statistic
        
        """
        ...
    @typing.overload
    @staticmethod
    def copy(sumOfSquares: 'SumOfSquares', sumOfSquares2: 'SumOfSquares') -> None:
        """
            Copies source to dest.
        
            Neither source nor dest can be null.
        
            Parameters:
                source (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.summary.SumOfSquares`): SumOfSquares to copy
                dest (:class:`~fr.cnes.sirius.patrius.math.stat.descriptive.summary.SumOfSquares`): SumOfSquares to copy to
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if either source or dest is null
        
        
        """
        ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float: ...
    @typing.overload
    def evaluate(self) -> float: ...
    @typing.overload
    def evaluate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int) -> float:
        """
            Returns the sum of the squares of the entries in the specified portion of the input array, or :code:`Double.NaN` if the
            designated subarray is empty.
        
            Throws :code:`MathIllegalArgumentException` if the array is null.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.UnivariateStatistic`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.util.MathArrays.Function`
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                values (double[]): the input array
                begin (int): index of the first array element to include
                length (int): the number of elements to include
        
            Returns:
                the sum of the squares of the values or 0 if length = 0
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the array is null or the array index parameters are not valid
        
            Also see:
        
        
        """
        ...
    def getN(self) -> int:
        """
            Returns the number of values that have been added.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getN` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Returns:
                the number of values.
        
        
        """
        ...
    def getResult(self) -> float:
        """
            Returns the current value of the Statistic.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.getResult` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.getResult` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Returns:
                value of the statistic, :code:`Double.NaN` if it has been cleared or just instantiated.
        
        
        """
        ...
    def increment(self, double: float) -> None:
        """
            Updates the internal state of the statistic to reflect the addition of the new value.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic.increment` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.StorelessUnivariateStatistic`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic.increment` in
                class :class:`~fr.cnes.sirius.patrius.math.stat.descriptive.AbstractStorelessUnivariateStatistic`
        
            Parameters:
                d (double): the new value.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.stat.descriptive.summary")``.

    Product: typing.Type[Product]
    Sum: typing.Type[Sum]
    SumOfLogs: typing.Type[SumOfLogs]
    SumOfSquares: typing.Type[SumOfSquares]
