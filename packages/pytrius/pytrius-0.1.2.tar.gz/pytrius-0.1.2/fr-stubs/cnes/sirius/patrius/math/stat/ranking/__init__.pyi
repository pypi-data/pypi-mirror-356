
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.random
import java.lang
import jpype
import typing



class NaNStrategy(java.lang.Enum['NaNStrategy']):
    """
    public enum NaNStrategy extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.stat.ranking.NaNStrategy`>
    
        Strategies for handling NaN values in rank transformations.
    
          - MINIMAL - NaNs are treated as minimal in the ordering, equivalent to (that is, tied with)
            :code:`Double.NEGATIVE_INFINITY`.
          - MAXIMAL - NaNs are treated as maximal in the ordering, equivalent to :code:`Double.POSITIVE_INFINITY`
          - REMOVED - NaNs are removed before the rank transform is applied
          - FIXED - NaNs are left "in place," that is the rank transformation is applied to the other elements in the input array,
            but the NaN elements are returned unchanged.
          - FAILED - If any NaN is encountered in the input array, an appropriate exception is thrown
    
    
        Since:
            2.0
    """
    MINIMAL: typing.ClassVar['NaNStrategy'] = ...
    MAXIMAL: typing.ClassVar['NaNStrategy'] = ...
    REMOVED: typing.ClassVar['NaNStrategy'] = ...
    FIXED: typing.ClassVar['NaNStrategy'] = ...
    FAILED: typing.ClassVar['NaNStrategy'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'NaNStrategy':
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
    def values() -> typing.MutableSequence['NaNStrategy']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (NaNStrategy c : NaNStrategy.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class RankingAlgorithm:
    """
    public interface RankingAlgorithm
    
        Interface representing a rank transformation.
    
        Since:
            2.0
    """
    def rank(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
        
            Performs a rank transformation on the input data, returning an array of ranks.
        
            Ranks should be 1-based - that is, the smallest value returned in an array of ranks should be greater than or equal to
            one, rather than 0. Ranks should in general take integer values, though implementations may return averages or other
            floating point values to resolve ties in the input data.
        
            Parameters:
                data (double[]): array of data to be ranked
        
            Returns:
                an array of ranks corresponding to the elements of the input array
        
        
        """
        ...

class TiesStrategy(java.lang.Enum['TiesStrategy']):
    """
    public enum TiesStrategy extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.stat.ranking.TiesStrategy`>
    
        Strategies for handling tied values in rank transformations.
    
          - SEQUENTIAL - Ties are assigned ranks in order of occurrence in the original array, for example (1,3,4,3) is ranked as
            (1,2,4,3)
          - MINIMUM - Tied values are assigned the minimum applicable rank, or the rank of the first occurrence. For example,
            (1,3,4,3) is ranked as (1,2,4,2)
          - MAXIMUM - Tied values are assigned the maximum applicable rank, or the rank of the last occurrence. For example,
            (1,3,4,3) is ranked as (1,3,4,3)
          - AVERAGE - Tied values are assigned the average of the applicable ranks. For example, (1,3,4,3) is ranked as
            (1,2.5,4,2.5)
          - RANDOM - Tied values are assigned a random integer rank from among the applicable values. The assigned rank will always
            be an integer, (inclusively) between the values returned by the MINIMUM and MAXIMUM strategies.
    
    
        Since:
            2.0
    """
    SEQUENTIAL: typing.ClassVar['TiesStrategy'] = ...
    MINIMUM: typing.ClassVar['TiesStrategy'] = ...
    MAXIMUM: typing.ClassVar['TiesStrategy'] = ...
    AVERAGE: typing.ClassVar['TiesStrategy'] = ...
    RANDOM: typing.ClassVar['TiesStrategy'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'TiesStrategy':
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
    def values() -> typing.MutableSequence['TiesStrategy']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (TiesStrategy c : TiesStrategy.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class NaturalRanking(RankingAlgorithm):
    """
    public class NaturalRanking extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.stat.ranking.RankingAlgorithm`
    
    
        Ranking based on the natural ordering on doubles.
    
        NaNs are treated according to the configured :class:`~fr.cnes.sirius.patrius.math.stat.ranking.NaNStrategy` and ties are
        handled using the selected :class:`~fr.cnes.sirius.patrius.math.stat.ranking.TiesStrategy`. Configuration settings are
        supplied in optional constructor arguments. Defaults are
        :meth:`~fr.cnes.sirius.patrius.math.stat.ranking.NaNStrategy.FAILED` and
        :meth:`~fr.cnes.sirius.patrius.math.stat.ranking.TiesStrategy.AVERAGE`, respectively. When using
        :meth:`~fr.cnes.sirius.patrius.math.stat.ranking.TiesStrategy.RANDOM`, a
        :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator` may be supplied as a constructor argument.
    
        Examples:
    
        Since:
            2.0
    """
    DEFAULT_NAN_STRATEGY: typing.ClassVar[NaNStrategy] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.stat.ranking.NaNStrategy` DEFAULT_NAN_STRATEGY
    
        default NaN strategy
    
    """
    DEFAULT_TIES_STRATEGY: typing.ClassVar[TiesStrategy] = ...
    """
    public static final :class:`~fr.cnes.sirius.patrius.math.stat.ranking.TiesStrategy` DEFAULT_TIES_STRATEGY
    
        default ties strategy
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, randomGenerator: fr.cnes.sirius.patrius.math.random.RandomGenerator): ...
    @typing.overload
    def __init__(self, naNStrategy: NaNStrategy): ...
    @typing.overload
    def __init__(self, naNStrategy: NaNStrategy, randomGenerator: fr.cnes.sirius.patrius.math.random.RandomGenerator): ...
    @typing.overload
    def __init__(self, naNStrategy: NaNStrategy, tiesStrategy: TiesStrategy): ...
    @typing.overload
    def __init__(self, tiesStrategy: TiesStrategy): ...
    def getNanStrategy(self) -> NaNStrategy:
        """
            Return the NaNStrategy
        
            Returns:
                returns the NaNStrategy
        
        
        """
        ...
    def getTiesStrategy(self) -> TiesStrategy:
        """
            Return the TiesStrategy
        
            Returns:
                the TiesStrategy
        
        
        """
        ...
    def rank(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]:
        """
            Rank :code:`data` using the natural ordering on Doubles, with NaN values handled according to :code:`nanStrategy` and
            ties resolved using :code:`tiesStrategy.`
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.stat.ranking.RankingAlgorithm`
        
            Parameters:
                data (double[]): array to be ranked
        
            Returns:
                array of ranks
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NotANumberException`: if the selected :class:`~fr.cnes.sirius.patrius.math.stat.ranking.NaNStrategy` is :code:`FAILED` and a `null
                    <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true#NaN>` is encountered in the input data
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.stat.ranking")``.

    NaNStrategy: typing.Type[NaNStrategy]
    NaturalRanking: typing.Type[NaturalRanking]
    RankingAlgorithm: typing.Type[RankingAlgorithm]
    TiesStrategy: typing.Type[TiesStrategy]
