
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.distribution
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.stat.descriptive
import java.io
import java.net
import java.util
import jpype
import jpype.protocol
import typing



class EmpiricalDistribution(fr.cnes.sirius.patrius.math.distribution.AbstractRealDistribution):
    DEFAULT_BIN_COUNT: typing.ClassVar[int] = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, randomGenerator: 'RandomGenerator'): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, randomGenerator: 'RandomGenerator'): ...
    def cumulativeProbability(self, double: float) -> float: ...
    def density(self, double: float) -> float: ...
    def getBinCount(self) -> int: ...
    def getBinStats(self) -> java.util.List[fr.cnes.sirius.patrius.math.stat.descriptive.SummaryStatistics]: ...
    def getGeneratorUpperBounds(self) -> typing.MutableSequence[float]: ...
    def getNextValue(self) -> float: ...
    def getNumericalMean(self) -> float: ...
    def getNumericalVariance(self) -> float: ...
    def getSampleStats(self) -> fr.cnes.sirius.patrius.math.stat.descriptive.StatisticalSummary: ...
    def getSupportLowerBound(self) -> float: ...
    def getSupportUpperBound(self) -> float: ...
    def getUpperBounds(self) -> typing.MutableSequence[float]: ...
    def inverseCumulativeProbability(self, double: float) -> float: ...
    def isLoaded(self) -> bool: ...
    def isSupportConnected(self) -> bool: ...
    def isSupportLowerBoundInclusive(self) -> bool: ...
    def isSupportUpperBoundInclusive(self) -> bool: ...
    @typing.overload
    def load(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    @typing.overload
    def load(self, file: typing.Union[java.io.File, jpype.protocol.SupportsPath]) -> None: ...
    @typing.overload
    def load(self, uRL: java.net.URL) -> None: ...
    @typing.overload
    def probability(self, double: float, double2: float) -> float: ...
    @typing.overload
    def probability(self, double: float) -> float: ...
    def reSeed(self, long: int) -> None: ...
    def reseedRandomGenerator(self, long: int) -> None: ...
    @typing.overload
    def sample(self) -> float: ...
    @typing.overload
    def sample(self, int: int) -> typing.MutableSequence[float]: ...

class NormalizedRandomGenerator:
    """
    public interface NormalizedRandomGenerator
    
        This interface represent a normalized random generator for scalars. Normalized generator provide null mean and unit
        standard deviation scalars.
    
        Since:
            1.2
    """
    def nextNormalizedDouble(self) -> float:
        """
            Generate a random scalar with null mean and unit standard deviation.
        
            This method does **not** specify the shape of the distribution, it is the implementing class that provides it. The only
            contract here is to generate numbers with null mean and unit standard deviation.
        
            Returns:
                a random scalar with null mean and unit standard deviation
        
        
        """
        ...

class RandomDataGenerator(java.io.Serializable):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, randomGenerator: 'RandomGenerator'): ...
    def getRan(self) -> 'RandomGenerator': ...
    def nextBeta(self, double: float, double2: float) -> float: ...
    def nextBinomial(self, int: int, double: float) -> int: ...
    def nextCauchy(self, double: float, double2: float) -> float: ...
    def nextChiSquare(self, double: float) -> float: ...
    def nextExponential(self, double: float) -> float: ...
    def nextF(self, double: float, double2: float) -> float: ...
    def nextGamma(self, double: float, double2: float) -> float: ...
    def nextGaussian(self, double: float, double2: float) -> float: ...
    def nextHexString(self, int: int) -> str: ...
    def nextHypergeometric(self, int: int, int2: int, int3: int) -> int: ...
    def nextInt(self, int: int, int2: int) -> int: ...
    def nextLong(self, long: int, long2: int) -> int: ...
    def nextPascal(self, int: int, double: float) -> int: ...
    def nextPermutation(self, int: int, int2: int) -> typing.MutableSequence[int]: ...
    def nextPoisson(self, double: float) -> int: ...
    def nextSample(self, collection: typing.Union[java.util.Collection[typing.Any], typing.Sequence[typing.Any], typing.Set[typing.Any]], int: int) -> typing.MutableSequence[typing.Any]: ...
    def nextSecureHexString(self, int: int) -> str: ...
    def nextSecureInt(self, int: int, int2: int) -> int: ...
    def nextSecureLong(self, long: int, long2: int) -> int: ...
    def nextT(self, double: float) -> float: ...
    @typing.overload
    def nextUniform(self, double: float, double2: float) -> float: ...
    @typing.overload
    def nextUniform(self, double: float, double2: float, boolean: bool) -> float: ...
    def nextWeibull(self, double: float, double2: float) -> float: ...
    def nextZipf(self, int: int, double: float) -> int: ...
    @typing.overload
    def reSeed(self) -> None: ...
    @typing.overload
    def reSeed(self, long: int) -> None: ...
    @typing.overload
    def reSeedSecure(self) -> None: ...
    @typing.overload
    def reSeedSecure(self, long: int) -> None: ...
    def setSecureAlgorithm(self, string: str, string2: str) -> None: ...

class RandomGenerator:
    """
    public interface RandomGenerator
    
        Interface extracted from :code:`java.util.Random`. This interface is implemented by
        :class:`~fr.cnes.sirius.patrius.math.random.AbstractRandomGenerator`.
    
        Since:
            1.1
    """
    def nextBoolean(self) -> bool:
        """
            Returns the next pseudorandom, uniformly distributed :code:`boolean` value from this random number generator's sequence.
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`boolean` value from this random number generator's sequence
        
        
        """
        ...
    def nextBytes(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> None:
        """
            Generates random bytes and places them into a user-supplied byte array. The number of random bytes produced is equal to
            the length of the byte array.
        
            Parameters:
                bytes (byte[]): the non-null byte array in which to put the random bytes
        
        
        """
        ...
    def nextDouble(self) -> float:
        """
            Returns the next pseudorandom, uniformly distributed :code:`double` value between :code:`0.0` and :code:`1.0` from this
            random number generator's sequence.
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`double` value between :code:`0.0` and :code:`1.0` from this random
                number generator's sequence
        
        
        """
        ...
    def nextFloat(self) -> float:
        """
            Returns the next pseudorandom, uniformly distributed :code:`float` value between :code:`0.0` and :code:`1.0` from this
            random number generator's sequence.
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`float` value between :code:`0.0` and :code:`1.0` from this random
                number generator's sequence
        
        
        """
        ...
    def nextGaussian(self) -> float:
        """
            Returns the next pseudorandom, Gaussian ("normally") distributed :code:`double` value with mean :code:`0.0` and standard
            deviation :code:`1.0` from this random number generator's sequence.
        
            Returns:
                the next pseudorandom, Gaussian ("normally") distributed :code:`double` value with mean :code:`0.0` and standard
                deviation :code:`1.0` from this random number generator's sequence
        
        
        """
        ...
    @typing.overload
    def nextInt(self) -> int:
        """
            Returns the next pseudorandom, uniformly distributed :code:`int` value from this random number generator's sequence. All
            2:sup:`32` possible ``int`` values should be produced with (approximately) equal probability.
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`int` value from this random number generator's sequence
        
        """
        ...
    @typing.overload
    def nextInt(self, int: int) -> int:
        """
            Returns a pseudorandom, uniformly distributed ``int`` value between 0 (inclusive) and the specified value (exclusive),
            drawn from this random number generator's sequence.
        
            Parameters:
                n (int): the bound on the random number to be returned. Must be positive.
        
            Returns:
                a pseudorandom, uniformly distributed ``int`` value between 0 (inclusive) and n (exclusive).
        
            Raises:
                : if n is not positive.
        
        
        """
        ...
    def nextLong(self) -> int:
        """
            Returns the next pseudorandom, uniformly distributed :code:`long` value from this random number generator's sequence.
            All 2:sup:`64` possible ``long`` values should be produced with (approximately) equal probability.
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`long` value from this random number generator's sequence
        
        
        """
        ...
    @typing.overload
    def setSeed(self, int: int) -> None:
        """
            Sets the seed of the underlying random number generator using an :code:`int` seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Parameters:
                seed (int): the seed value
        
            Sets the seed of the underlying random number generator using an :code:`int` array seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Parameters:
                seed (int[]): the seed value
        
            Sets the seed of the underlying random number generator using a :code:`long` seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Parameters:
                seed (long): the seed value
        
        
        """
        ...
    @typing.overload
    def setSeed(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> None: ...
    @typing.overload
    def setSeed(self, long: int) -> None: ...

class RandomVectorGenerator:
    """
    public interface RandomVectorGenerator
    
        This interface represents a random generator for whole vectors.
    
        Since:
            1.2
    """
    def nextVector(self) -> typing.MutableSequence[float]:
        """
            Generate a random vector.
        
            Returns:
                a random vector as an array of double.
        
        
        """
        ...

class ValueServer:
    """
    public class ValueServer extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Generates values for use in simulation applications.
    
        How values are generated is determined by the :code:`mode` property.
    
        Supported :code:`mode` values are:
    
          - DIGEST_MODE -- uses an empirical distribution
          - REPLAY_MODE -- replays data from :code:`valuesFileURL`
          - UNIFORM_MODE -- generates uniformly distributed random values with mean = :code:`mu`
          - EXPONENTIAL_MODE -- generates exponentially distributed random values with mean = :code:`mu`
          - GAUSSIAN_MODE -- generates Gaussian distributed random values with mean = :code:`mu` and standard deviation =
            :code:`sigma`
          - CONSTANT_MODE -- returns :code:`mu` every time.
    """
    DIGEST_MODE: typing.ClassVar[int] = ...
    """
    public static final int DIGEST_MODE
    
        Use empirical distribution.
    
        Also see:
            :meth:`~constant`
    
    
    """
    REPLAY_MODE: typing.ClassVar[int] = ...
    """
    public static final int REPLAY_MODE
    
        Replay data from valuesFilePath.
    
        Also see:
            :meth:`~constant`
    
    
    """
    UNIFORM_MODE: typing.ClassVar[int] = ...
    """
    public static final int UNIFORM_MODE
    
        Uniform random deviates with mean = μ.
    
        Also see:
            :meth:`~constant`
    
    
    """
    EXPONENTIAL_MODE: typing.ClassVar[int] = ...
    """
    public static final int EXPONENTIAL_MODE
    
        Exponential random deviates with mean = μ.
    
        Also see:
            :meth:`~constant`
    
    
    """
    GAUSSIAN_MODE: typing.ClassVar[int] = ...
    """
    public static final int GAUSSIAN_MODE
    
        Gaussian random deviates with mean = μ, std dev = σ.
    
        Also see:
            :meth:`~constant`
    
    
    """
    CONSTANT_MODE: typing.ClassVar[int] = ...
    """
    public static final int CONSTANT_MODE
    
        Always return mu
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, randomGenerator: RandomGenerator): ...
    def closeReplayFile(self) -> None: ...
    @typing.overload
    def computeDistribution(self) -> None: ...
    @typing.overload
    def computeDistribution(self, int: int) -> None: ...
    @typing.overload
    def fill(self, int: int) -> typing.MutableSequence[float]: ...
    @typing.overload
    def fill(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def getEmpiricalDistribution(self) -> EmpiricalDistribution:
        """
            Returns the :class:`~fr.cnes.sirius.patrius.math.random.EmpiricalDistribution` used when operating in
            :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.DIGEST_MODE`.
        
            Returns:
                EmpircalDistribution built by :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.computeDistribution`
        
        
        """
        ...
    def getMode(self) -> int:
        """
            Returns the data generation mode. See :class:`~fr.cnes.sirius.patrius.math.random.ValueServer` for description of the
            valid values of this property.
        
            Returns:
                Value of property mode.
        
        
        """
        ...
    def getMu(self) -> float:
        """
            Returns the mean used when operating in :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.GAUSSIAN_MODE`,
            :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.EXPONENTIAL_MODE` or
            :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.UNIFORM_MODE`. When operating in
            :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.CONSTANT_MODE`, this is the constant value always returned.
            Calling :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.computeDistribution` sets this value to the overall mean
            of the values in the :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.getValuesFileURL`.
        
            Returns:
                Mean used in data generation.
        
        
        """
        ...
    def getNext(self) -> float: ...
    def getSigma(self) -> float:
        """
            Returns the standard deviation used when operating in
            :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.GAUSSIAN_MODE`. Calling
            :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.computeDistribution` sets this value to the overall standard
            deviation of the values in the :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.getValuesFileURL`. This property
            has no effect when the data generation mode is not
            :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.GAUSSIAN_MODE`.
        
            Returns:
                Standard deviation used when operating in :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.GAUSSIAN_MODE`.
        
        
        """
        ...
    def getValuesFileURL(self) -> java.net.URL:
        """
            Returns the URL for the file used to build the empirical distribution when using
            :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.DIGEST_MODE`.
        
            Returns:
                Values file URL.
        
        
        """
        ...
    def reSeed(self, long: int) -> None:
        """
            Reseeds the random data generator.
        
            Parameters:
                seed (long): Value with which to reseed the :class:`~fr.cnes.sirius.patrius.math.random.RandomDataGenerator` used to generate random
                    data.
        
        
        """
        ...
    def resetReplayFile(self) -> None: ...
    def setMode(self, int: int) -> None:
        """
            Sets the data generation mode.
        
            Parameters:
                modeIn (int): New value of the data generation mode.
        
        
        """
        ...
    def setMu(self, double: float) -> None:
        """
            Sets the :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.getMu` used in data generation. Note that calling this
            method after :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.computeDistribution` has been called will have no
            effect on data generated in :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.DIGEST_MODE`.
        
            Parameters:
                muIn (double): new Mean value.
        
        
        """
        ...
    def setSigma(self, double: float) -> None:
        """
            Sets the :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.getSigma` used in
            :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.GAUSSIAN_MODE`.
        
            Parameters:
                sigmaIn (double): New standard deviation.
        
        
        """
        ...
    @typing.overload
    def setValuesFileURL(self, string: str) -> None:
        """
            Sets the the :meth:`~fr.cnes.sirius.patrius.math.random.ValueServer.getValuesFileURL`.
        
            The values file *must* be an ASCII text file containing one valid numeric entry per line.
        
            Parameters:
                url (`URL <http://docs.oracle.com/javase/8/docs/api/java/net/URL.html?is-external=true>`): URL of the values file.
        
        
        """
        ...
    @typing.overload
    def setValuesFileURL(self, uRL: java.net.URL) -> None: ...

class AbstractRandomGenerator(RandomGenerator):
    def __init__(self): ...
    def clear(self) -> None: ...
    def nextBoolean(self) -> bool: ...
    def nextBytes(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> None: ...
    def nextDouble(self) -> float: ...
    def nextFloat(self) -> float: ...
    def nextGaussian(self) -> float: ...
    @typing.overload
    def nextInt(self) -> int: ...
    @typing.overload
    def nextInt(self, int: int) -> int: ...
    def nextLong(self) -> int: ...
    @typing.overload
    def setSeed(self, long: int) -> None: ...
    @typing.overload
    def setSeed(self, int: int) -> None: ...
    @typing.overload
    def setSeed(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> None: ...

class BitsStreamGenerator(RandomGenerator, java.io.Serializable):
    """
    public abstract class BitsStreamGenerator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Base class for random number generators that generates bits streams.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def clear(self) -> None:
        """
            Clears the cache used by the default implementation of
            :meth:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator.nextGaussianDouble`.
        
        """
        ...
    def nextBoolean(self) -> bool:
        """
            Returns the next pseudorandom, uniformly distributed :code:`boolean` value from this random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextBoolean` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`boolean` value from this random number generator's sequence
        
        
        """
        ...
    def nextBytes(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> None:
        """
            Generates random bytes and places them into a user-supplied byte array. The number of random bytes produced is equal to
            the length of the byte array.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                bytes (byte[]): the non-null byte array in which to put the random bytes
        
        
        """
        ...
    def nextDouble(self) -> float:
        """
            Returns the next pseudorandom, uniformly distributed :code:`double` value between :code:`0.0` and :code:`1.0` from this
            random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextDouble` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`double` value between :code:`0.0` and :code:`1.0` from this random
                number generator's sequence
        
        
        """
        ...
    def nextFloat(self) -> float:
        """
            Returns the next pseudorandom, uniformly distributed :code:`float` value between :code:`0.0` and :code:`1.0` from this
            random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextFloat` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`float` value between :code:`0.0` and :code:`1.0` from this random
                number generator's sequence
        
        
        """
        ...
    def nextGaussian(self) -> float:
        """
            Returns the next pseudorandom, Gaussian ("normally") distributed :code:`double` value with mean :code:`0.0` and standard
            deviation :code:`1.0` from this random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextGaussian` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, Gaussian ("normally") distributed :code:`double` value with mean :code:`0.0` and standard
                deviation :code:`1.0` from this random number generator's sequence
        
        
        """
        ...
    @typing.overload
    def nextInt(self) -> int:
        """
            Returns the next pseudorandom, uniformly distributed :code:`int` value from this random number generator's sequence. All
            2:sup:`32` possible ``int`` values should be produced with (approximately) equal probability.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextInt` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`int` value from this random number generator's sequence
        
        """
        ...
    @typing.overload
    def nextInt(self, int: int) -> int:
        """
            Returns a pseudorandom, uniformly distributed ``int`` value between 0 (inclusive) and the specified value (exclusive),
            drawn from this random number generator's sequence.
        
            This default implementation is copied from Apache Harmony java.util.Random (r929253).
        
            Implementation notes:
        
              - If n is a power of 2, this method returns :code:`(int) ((n * (long) next(31)) >> 31)`.
              - If n is not a power of 2, what is returned is :code:`next(31) % n` with :code:`next(31)` values rejected (i.e.
                regenerated) until a value that is larger than the remainder of :code:`Integer.MAX_VALUE / n` is generated. Rejection of
                this initial segment is necessary to ensure a uniform distribution.
        
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextInt` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                n (int): the bound on the random number to be returned. Must be positive.
        
            Returns:
                a pseudorandom, uniformly distributed ``int`` value between 0 (inclusive) and n (exclusive).
        
        
        """
        ...
    def nextLong(self) -> int:
        """
            Returns the next pseudorandom, uniformly distributed :code:`long` value from this random number generator's sequence.
            All 2:sup:`64` possible ``long`` values should be produced with (approximately) equal probability.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextLong` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`long` value from this random number generator's sequence
        
        
        """
        ...
    @typing.overload
    def setSeed(self, int: int) -> None:
        """
            Sets the seed of the underlying random number generator using an :code:`int` seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.setSeed` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                seed (int): the seed value
        
            Sets the seed of the underlying random number generator using an :code:`int` array seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                seed (int[]): the seed value
        
            Sets the seed of the underlying random number generator using a :code:`long` seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.setSeed` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                seed (long): the seed value
        
        
        """
        ...
    @typing.overload
    def setSeed(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> None: ...
    @typing.overload
    def setSeed(self, long: int) -> None: ...

class CorrelatedRandomVectorGenerator(RandomVectorGenerator):
    """
    public class CorrelatedRandomVectorGenerator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator`
    
        A :class:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator` that generates vectors with with correlated
        components.
    
        Random vectors with correlated components are built by combining the uncorrelated components of another random vector in
        such a way that the resulting correlations are the ones specified by a positive definite covariance matrix.
    
        The main use for correlated random vector generation is for Monte-Carlo simulation of physical problems with several
        variables, for example to generate error vectors to be added to a nominal vector. A particularly interesting case is
        when the generated vector should be drawn from a ` Multivariate Normal Distribution
        <http://en.wikipedia.org/wiki/Multivariate_normal_distribution>`. The approach using a Cholesky decomposition is quite
        usual in this case. However, it can be extended to other cases as long as the underlying random generator provides
        :class:`~fr.cnes.sirius.patrius.math.random.NormalizedRandomGenerator` like
        :class:`~fr.cnes.sirius.patrius.math.random.GaussianRandomGenerator` or
        :class:`~fr.cnes.sirius.patrius.math.random.UniformRandomGenerator`.
    
        Sometimes, the covariance matrix for a given simulation is not strictly positive definite. This means that the
        correlations are not all independent from each other. In this case, however, the non strictly positive elements found
        during the Cholesky decomposition of the covariance matrix should not be negative either, they should be null. Another
        non-conventional extension handling this case is used here. Rather than computing :code:`C = U :sup:`T` .U` where
        :code:`C` is the covariance matrix and :code:`U` is an upper-triangular matrix, we compute :code:`C = B.B :sup:`T``
        where :code:`B` is a rectangular matrix having more rows than columns. The number of columns of :code:`B` is the rank of
        the covariance matrix, and it is the dimension of the uncorrelated random vector that is needed to compute the component
        of the correlated vector. This class handles this situation automatically.
    
        Since:
            1.2
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, double2: float, normalizedRandomGenerator: typing.Union[NormalizedRandomGenerator, typing.Callable]): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, double: float, normalizedRandomGenerator: typing.Union[NormalizedRandomGenerator, typing.Callable]): ...
    def getGenerator(self) -> NormalizedRandomGenerator:
        """
            Get the underlying normalized components generator.
        
            Returns:
                underlying uncorrelated components generator
        
        
        """
        ...
    def getRank(self) -> int:
        """
            Get the rank of the covariance matrix. The rank is the number of independent rows in the covariance matrix, it is also
            the number of columns of the root matrix.
        
            Returns:
                rank of the square matrix.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.random.CorrelatedRandomVectorGenerator.getRootMatrix`
        
        
        """
        ...
    def getRootMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Get the root of the covariance matrix. The root is the rectangular matrix :code:`B` such that the covariance matrix is
            equal to :code:`B.B :sup:`T``
        
            Returns:
                root of the square matrix
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.random.CorrelatedRandomVectorGenerator.getRank`
        
        
        """
        ...
    def nextVector(self) -> typing.MutableSequence[float]:
        """
            Generate a correlated random vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator.nextVector` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator`
        
            Returns:
                a random vector as an array of double. The returned array is created at each call, the caller can do what it wants with
                it.
        
        
        """
        ...

class GaussianRandomGenerator(NormalizedRandomGenerator):
    """
    public class GaussianRandomGenerator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.random.NormalizedRandomGenerator`
    
        This class is a gaussian normalized random generator for scalars.
    
        This class is a simple wrapper around the :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextGaussian`
        method.
    
        Since:
            1.2
    """
    def __init__(self, randomGenerator: RandomGenerator): ...
    def nextNormalizedDouble(self) -> float:
        """
            Generate a random scalar with null mean and unit standard deviation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.NormalizedRandomGenerator.nextNormalizedDouble` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.NormalizedRandomGenerator`
        
            Returns:
                a random scalar with null mean and unit standard deviation
        
        
        """
        ...

class JDKRandomGenerator(java.util.Random, RandomGenerator):
    """
    public class JDKRandomGenerator extends `Random <http://docs.oracle.com/javase/8/docs/api/java/util/Random.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
    
        Extension of :code:`java.util.Random` to implement :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def setSeed(self, long: int) -> None:
        """
            Sets the seed of the underlying random number generator using an :code:`int` seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.setSeed` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                seed (int): the seed value
        
            Sets the seed of the underlying random number generator using an :code:`int` array seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                seed (int[]): the seed value
        
        
        """
        ...
    @typing.overload
    def setSeed(self, int: int) -> None: ...
    @typing.overload
    def setSeed(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> None: ...

class RandomAdaptor(java.util.Random, RandomGenerator):
    """
    public class RandomAdaptor extends `Random <http://docs.oracle.com/javase/8/docs/api/java/util/Random.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
    
        Extension of :code:`java.util.Random` wrapping a :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`.
    
        Since:
            1.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, randomGenerator: RandomGenerator): ...
    @staticmethod
    def createAdaptor(randomGenerator: RandomGenerator) -> java.util.Random:
        """
            Factory method to create a :code:`Random` using the supplied :code:`RandomGenerator`.
        
            Parameters:
                randomGenerator (:class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`): wrapped RandomGenerator instance
        
            Returns:
                a Random instance wrapping the RandomGenerator
        
        
        """
        ...
    def nextBoolean(self) -> bool:
        """
            Returns the next pseudorandom, uniformly distributed :code:`boolean` value from this random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextBoolean` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Overrides:
                 in class 
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`boolean` value from this random number generator's sequence
        
        
        """
        ...
    def nextBytes(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> None:
        """
            Generates random bytes and places them into a user-supplied byte array. The number of random bytes produced is equal to
            the length of the byte array.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Overrides:
                 in class 
        
            Parameters:
                bytes (byte[]): the non-null byte array in which to put the random bytes
        
        
        """
        ...
    @typing.overload
    def nextDouble(self, double: float) -> float: ...
    @typing.overload
    def nextDouble(self, double: float, double2: float) -> float: ...
    @typing.overload
    def nextDouble(self) -> float:
        """
            Returns the next pseudorandom, uniformly distributed :code:`double` value between :code:`0.0` and :code:`1.0` from this
            random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextDouble` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Overrides:
                 in class 
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`double` value between :code:`0.0` and :code:`1.0` from this random
                number generator's sequence
        
        
        """
        ...
    @typing.overload
    def nextFloat(self, float: float) -> float: ...
    @typing.overload
    def nextFloat(self, float: float, float2: float) -> float: ...
    @typing.overload
    def nextFloat(self) -> float:
        """
            Returns the next pseudorandom, uniformly distributed :code:`float` value between :code:`0.0` and :code:`1.0` from this
            random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextFloat` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Overrides:
                 in class 
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`float` value between :code:`0.0` and :code:`1.0` from this random
                number generator's sequence
        
        
        """
        ...
    @typing.overload
    def nextGaussian(self, double: float, double2: float) -> float: ...
    @typing.overload
    def nextGaussian(self) -> float:
        """
            Returns the next pseudorandom, Gaussian ("normally") distributed :code:`double` value with mean :code:`0.0` and standard
            deviation :code:`1.0` from this random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextGaussian` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Overrides:
                 in class 
        
            Returns:
                the next pseudorandom, Gaussian ("normally") distributed :code:`double` value with mean :code:`0.0` and standard
                deviation :code:`1.0` from this random number generator's sequence
        
        
        """
        ...
    @typing.overload
    def nextInt(self, int: int, int2: int) -> int: ...
    @typing.overload
    def nextInt(self) -> int:
        """
            Returns the next pseudorandom, uniformly distributed :code:`int` value from this random number generator's sequence. All
            2:sup:`32` possible ``int`` values should be produced with (approximately) equal probability.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextInt` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Overrides:
                 in class 
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`int` value from this random number generator's sequence
        
        """
        ...
    @typing.overload
    def nextInt(self, int: int) -> int:
        """
            Returns a pseudorandom, uniformly distributed ``int`` value between 0 (inclusive) and the specified value (exclusive),
            drawn from this random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextInt` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Overrides:
                 in class 
        
            Parameters:
                n (int): the bound on the random number to be returned. Must be positive.
        
            Returns:
                a pseudorandom, uniformly distributed ``int`` value between 0 (inclusive) and n (exclusive).
        
            Raises:
                : if n is not positive.
        
        
        """
        ...
    @typing.overload
    def nextLong(self, long: int) -> int: ...
    @typing.overload
    def nextLong(self, long: int, long2: int) -> int: ...
    @typing.overload
    def nextLong(self) -> int:
        """
            Returns the next pseudorandom, uniformly distributed :code:`long` value from this random number generator's sequence.
            All 2:sup:`64` possible ``long`` values should be produced with (approximately) equal probability.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextLong` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Overrides:
                 in class 
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`long` value from this random number generator's sequence
        
        
        """
        ...
    @typing.overload
    def setSeed(self, int: int) -> None:
        """
            Sets the seed of the underlying random number generator using an :code:`int` seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.setSeed` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                seed (int): the seed value
        
            Sets the seed of the underlying random number generator using an :code:`int` array seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                seed (int[]): the seed value
        
            Sets the seed of the underlying random number generator using a :code:`long` seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.setSeed` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Overrides:
                 in class 
        
            Parameters:
                seed (long): the seed value
        
        
        """
        ...
    @typing.overload
    def setSeed(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> None: ...
    @typing.overload
    def setSeed(self, long: int) -> None: ...

class StableRandomGenerator(NormalizedRandomGenerator):
    """
    public class StableRandomGenerator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.random.NormalizedRandomGenerator`
    
    
        This class provides a stable normalized random generator. It samples from a stable distribution with location parameter
        0 and scale 1.
    
        The implementation uses the Chambers-Mallows-Stuck method as described in *Handbook of computational statistics:
        concepts and methods* by James E. Gentle, Wolfgang Härdle, Yuichi Mori.
    
        Since:
            3.0
    """
    def __init__(self, randomGenerator: RandomGenerator, double: float, double2: float): ...
    def nextNormalizedDouble(self) -> float:
        """
            Generate a random scalar with zero location and unit scale.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.NormalizedRandomGenerator.nextNormalizedDouble` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.NormalizedRandomGenerator`
        
            Returns:
                a random scalar with zero location and unit scale
        
        
        """
        ...

class SynchronizedRandomGenerator(RandomGenerator):
    """
    public class SynchronizedRandomGenerator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
    
        Any :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator` implementation can be thread-safe if it is used through
        an instance of this class. This is achieved by enclosing calls to the methods of the actual generator inside the
        overridden :code:`synchronized` methods of this class.
    
        Since:
            3.1
    """
    def __init__(self, randomGenerator: RandomGenerator): ...
    def nextBoolean(self) -> bool:
        """
            Returns the next pseudorandom, uniformly distributed :code:`boolean` value from this random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextBoolean` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`boolean` value from this random number generator's sequence
        
        
        """
        ...
    def nextBytes(self, byteArray: typing.Union[typing.List[int], jpype.JArray, bytes]) -> None:
        """
            Generates random bytes and places them into a user-supplied byte array. The number of random bytes produced is equal to
            the length of the byte array.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                bytes (byte[]): the non-null byte array in which to put the random bytes
        
        
        """
        ...
    def nextDouble(self) -> float:
        """
            Returns the next pseudorandom, uniformly distributed :code:`double` value between :code:`0.0` and :code:`1.0` from this
            random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextDouble` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`double` value between :code:`0.0` and :code:`1.0` from this random
                number generator's sequence
        
        
        """
        ...
    def nextFloat(self) -> float:
        """
            Returns the next pseudorandom, uniformly distributed :code:`float` value between :code:`0.0` and :code:`1.0` from this
            random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextFloat` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`float` value between :code:`0.0` and :code:`1.0` from this random
                number generator's sequence
        
        
        """
        ...
    def nextGaussian(self) -> float:
        """
            Returns the next pseudorandom, Gaussian ("normally") distributed :code:`double` value with mean :code:`0.0` and standard
            deviation :code:`1.0` from this random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextGaussian` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, Gaussian ("normally") distributed :code:`double` value with mean :code:`0.0` and standard
                deviation :code:`1.0` from this random number generator's sequence
        
        
        """
        ...
    @typing.overload
    def nextInt(self) -> int:
        """
            Returns the next pseudorandom, uniformly distributed :code:`int` value from this random number generator's sequence. All
            2:sup:`32` possible ``int`` values should be produced with (approximately) equal probability.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextInt` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`int` value from this random number generator's sequence
        
        """
        ...
    @typing.overload
    def nextInt(self, int: int) -> int:
        """
            Returns a pseudorandom, uniformly distributed ``int`` value between 0 (inclusive) and the specified value (exclusive),
            drawn from this random number generator's sequence.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextInt` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                n (int): the bound on the random number to be returned. Must be positive.
        
            Returns:
                a pseudorandom, uniformly distributed ``int`` value between 0 (inclusive) and n (exclusive).
        
        
        """
        ...
    def nextLong(self) -> int:
        """
            Returns the next pseudorandom, uniformly distributed :code:`long` value from this random number generator's sequence.
            All 2:sup:`64` possible ``long`` values should be produced with (approximately) equal probability.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.nextLong` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Returns:
                the next pseudorandom, uniformly distributed :code:`long` value from this random number generator's sequence
        
        
        """
        ...
    @typing.overload
    def setSeed(self, int: int) -> None:
        """
            Sets the seed of the underlying random number generator using an :code:`int` seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.setSeed` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                seed (int): the seed value
        
            Sets the seed of the underlying random number generator using an :code:`int` array seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                seed (int[]): the seed value
        
            Sets the seed of the underlying random number generator using a :code:`long` seed.
        
            Sequences of values generated starting with the same seeds should be identical.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.setSeed` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Parameters:
                seed (long): the seed value
        
        
        """
        ...
    @typing.overload
    def setSeed(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> None: ...
    @typing.overload
    def setSeed(self, long: int) -> None: ...

class UncorrelatedRandomVectorGenerator(RandomVectorGenerator):
    """
    public class UncorrelatedRandomVectorGenerator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator`
    
        A :class:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator` that generates vectors with uncorrelated
        components. Components of generated vectors follow (independent) Gaussian distributions, with parameters supplied in the
        constructor.
    
        Since:
            1.2
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], normalizedRandomGenerator: typing.Union[NormalizedRandomGenerator, typing.Callable]): ...
    @typing.overload
    def __init__(self, int: int, normalizedRandomGenerator: typing.Union[NormalizedRandomGenerator, typing.Callable]): ...
    def nextVector(self) -> typing.MutableSequence[float]:
        """
            Generate an uncorrelated random vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator.nextVector` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator`
        
            Returns:
                a random vector as a newly built array of double
        
        
        """
        ...

class UniformRandomGenerator(NormalizedRandomGenerator):
    def __init__(self, randomGenerator: RandomGenerator): ...
    def nextNormalizedDouble(self) -> float: ...

class UniformlyCorrelatedRandomVectorGenerator(RandomVectorGenerator):
    """
    public class UniformlyCorrelatedRandomVectorGenerator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator`
    
        A :class:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator` that generates vectors with with correlated
        components.
    
        Random vectors with correlated components are built by combining the uncorrelated components of another random vector in
        such a way that the resulting correlations are the ones specified by a positive definite correlation matrix.
    
        The main use for correlated random vector generation is for Monte-Carlo simulation of physical problems with several
        variables, for example to generate error vectors to be added to a nominal vector. A particularly interesting case is
        when the generated vector should be drawn from a ` Multivariate Normal Distribution
        <http://en.wikipedia.org/wiki/Multivariate_normal_distribution>`. The approach using a Cholesky decomposition is quite
        usual in this case. However, it can be extended to other cases as long as the underlying random generator provides
        :class:`~fr.cnes.sirius.patrius.math.random.NormalizedRandomGenerator` like
        :class:`~fr.cnes.sirius.patrius.math.random.GaussianRandomGenerator` or
        :class:`~fr.cnes.sirius.patrius.math.random.UniformRandomGenerator`.
    
        Sometimes, the covariance matrix for a given simulation is not strictly positive definite. This means that the
        correlations are not all independent from each other. In this case, however, the non strictly positive elements found
        during the Cholesky decomposition of the covariance matrix should not be negative either, they should be null. Another
        non-conventional extension handling this case is used here. Rather than computing :code:`C = U :sup:`T` .U` where
        :code:`C` is the covariance matrix and :code:`U` is an upper-triangular matrix, we compute :code:`C = B.B :sup:`T``
        where :code:`B` is a rectangular matrix having more rows than columns. The number of columns of :code:`B` is the rank of
        the covariance matrix, and it is the dimension of the uncorrelated random vector that is needed to compute the component
        of the correlated vector. This class handles this situation automatically.
    
        Since:
            3.0
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, double2: float, normalizedRandomGenerator: typing.Union[NormalizedRandomGenerator, typing.Callable]): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix, double: float, normalizedRandomGenerator: typing.Union[NormalizedRandomGenerator, typing.Callable]): ...
    def getGenerator(self) -> NormalizedRandomGenerator:
        """
            Get the underlying normalized components generator.
        
            Returns:
                underlying uncorrelated components generator
        
        
        """
        ...
    def getRank(self) -> int:
        """
            Get the rank of the covariance matrix. The rank is the number of independent rows in the covariance matrix, it is also
            the number of columns of the root matrix.
        
            Returns:
                rank of the square matrix.
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.random.UniformlyCorrelatedRandomVectorGenerator.getRootMatrix`
        
        
        """
        ...
    def getRootMatrix(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix:
        """
            Get the root of the **correlation** matrix. The root is the rectangular matrix :code:`B` such that the **correlation**
            matrix is equal to :code:`B.B :sup:`T``
        
            Returns:
                root of the **correlation** matrix
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.random.UniformlyCorrelatedRandomVectorGenerator.getRank`
        
        
        """
        ...
    def getStandardDeviationVector(self) -> typing.MutableSequence[float]:
        """
            Get the standard deviation vector. The standard deviation vector is square root of the covariance diagonal elements.
        
            Returns:
                standard deviation vector
        
        
        """
        ...
    def nextVector(self) -> typing.MutableSequence[float]:
        """
            Generate a correlated random vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator.nextVector` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator`
        
            Returns:
                a random vector as an array of double. The returned array is created at each call, the caller can do what it wants with
                it.
        
        
        """
        ...

class UnitSphereRandomVectorGenerator(RandomVectorGenerator):
    """
    public class UnitSphereRandomVectorGenerator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator`
    
        Generate random vectors isotropically located on the surface of a sphere.
    
        Since:
            2.1
    """
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, randomGenerator: RandomGenerator): ...
    def nextVector(self) -> typing.MutableSequence[float]:
        """
            Generate a random vector.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator.nextVector` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomVectorGenerator`
        
            Returns:
                a random vector as an array of double.
        
        
        """
        ...

class AbstractWell(BitsStreamGenerator):
    """
    public abstract class AbstractWell extends :class:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator`
    
        This abstract class implements the WELL class of pseudo-random number generator from François Panneton, Pierre L'Ecuyer
        and Makoto Matsumoto.
    
        This generator is described in a paper by François Panneton, Pierre L'Ecuyer and Makoto Matsumoto `Improved Long-Period
        Generators Based on Linear Recurrences Modulo 2 <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf>` ACM
        Transactions on Mathematical Software, 32, 1 (2006). The errata for the paper are in `wellrng-errata.txt
        <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng-errata.txt>`.
    
        Since:
            2.2
    
        Also see:
            `WELL Random number generator <http://www.iro.umontreal.ca/~panneton/WELLRNG.html>`, :meth:`~serialized`
    """
    @typing.overload
    def setSeed(self, int: int) -> None:
        """
            Reinitialize the generator as if just built with the given int seed.
        
            The state of the generator is exactly the same as a new generator built with the same seed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.setSeed` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator.setSeed` in
                class :class:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator`
        
            Parameters:
                seed (int): the initial seed (32 bits integer)
        
            Reinitialize the generator as if just built with the given int array seed.
        
            The state of the generator is exactly the same as a new generator built with the same seed.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Specified by:
                 in class :class:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator`
        
            Parameters:
                seed (int[]): the initial seed (32 bits integers array). If null the seed of the generator will be the system time plus the system
                    identity hash code of the instance.
        
            Reinitialize the generator as if just built with the given long seed.
        
            The state of the generator is exactly the same as a new generator built with the same seed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.setSeed` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator.setSeed` in
                class :class:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator`
        
            Parameters:
                seed (long): the initial seed (64 bits integer)
        
        
        """
        ...
    @typing.overload
    def setSeed(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> None: ...
    @typing.overload
    def setSeed(self, long: int) -> None: ...

class ISAACRandom(BitsStreamGenerator):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, intArray: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, long: int): ...
    @typing.overload
    def setSeed(self, int: int) -> None: ...
    @typing.overload
    def setSeed(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> None: ...
    @typing.overload
    def setSeed(self, long: int) -> None: ...

class MersenneTwister(BitsStreamGenerator):
    """
    public class MersenneTwister extends :class:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator`
    
        This class implements a powerful pseudo-random number generator developed by Makoto Matsumoto and Takuji Nishimura
        during 1996-1997.
    
        This generator features an extremely long period (2 :sup:`19937` -1) and 623-dimensional equidistribution up to 32 bits
        accuracy. The home page for this generator is located at ` http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/emt.html
        <http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/emt.html>`.
    
        This generator is described in a paper by Makoto Matsumoto and Takuji Nishimura in 1998: `Mersenne Twister: A
        623-Dimensionally Equidistributed Uniform Pseudo-Random Number Generator
        <http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/ARTICLES/mt.pdf>`, ACM Transactions on Modeling and Computer
        Simulation, Vol. 8, No. 1, January 1998, pp 3--30
    
        This class is mainly a Java port of the 2002-01-26 version of the generator written in C by Makoto Matsumoto and Takuji
        Nishimura. Here is their original copyright:
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, intArray: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, long: int): ...
    @typing.overload
    def setSeed(self, int: int) -> None:
        """
            Reinitialize the generator as if just built with the given int seed.
        
            The state of the generator is exactly the same as a new generator built with the same seed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.setSeed` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator.setSeed` in
                class :class:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator`
        
            Parameters:
                seed (int): the initial seed (32 bits integer)
        
            Reinitialize the generator as if just built with the given int array seed.
        
            The state of the generator is exactly the same as a new generator built with the same seed.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Specified by:
                 in class :class:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator`
        
            Parameters:
                seed (int[]): the initial seed (32 bits integers array), if null the seed of the generator will be the current system time plus the
                    system identity hash code of this instance
        
            Reinitialize the generator as if just built with the given long seed.
        
            The state of the generator is exactly the same as a new generator built with the same seed.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.RandomGenerator.setSeed` in
                interface :class:`~fr.cnes.sirius.patrius.math.random.RandomGenerator`
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator.setSeed` in
                class :class:`~fr.cnes.sirius.patrius.math.random.BitsStreamGenerator`
        
            Parameters:
                seed (long): the initial seed (64 bits integer)
        
        
        """
        ...
    @typing.overload
    def setSeed(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> None: ...
    @typing.overload
    def setSeed(self, long: int) -> None: ...

class Well1024a(AbstractWell):
    """
    public class Well1024a extends :class:`~fr.cnes.sirius.patrius.math.random.AbstractWell`
    
        This class implements the WELL1024a pseudo-random number generator from François Panneton, Pierre L'Ecuyer and Makoto
        Matsumoto.
    
        This generator is described in a paper by François Panneton, Pierre L'Ecuyer and Makoto Matsumoto `Improved Long-Period
        Generators Based on Linear Recurrences Modulo 2 <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf>` ACM
        Transactions on Mathematical Software, 32, 1 (2006). The errata for the paper are in `wellrng-errata.txt
        <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng-errata.txt>`.
    
        Since:
            2.2
    
        Also see:
            `WELL Random number generator <http://www.iro.umontreal.ca/~panneton/WELLRNG.html>`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, intArray: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, long: int): ...

class Well19937a(AbstractWell):
    """
    public class Well19937a extends :class:`~fr.cnes.sirius.patrius.math.random.AbstractWell`
    
        This class implements the WELL19937a pseudo-random number generator from François Panneton, Pierre L'Ecuyer and Makoto
        Matsumoto.
    
        This generator is described in a paper by François Panneton, Pierre L'Ecuyer and Makoto Matsumoto `Improved Long-Period
        Generators Based on Linear Recurrences Modulo 2 <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf>` ACM
        Transactions on Mathematical Software, 32, 1 (2006). The errata for the paper are in `wellrng-errata.txt
        <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng-errata.txt>`.
    
        Since:
            2.2
    
        Also see:
            `WELL Random number generator <http://www.iro.umontreal.ca/~panneton/WELLRNG.html>`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, intArray: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, long: int): ...

class Well19937c(AbstractWell):
    """
    public class Well19937c extends :class:`~fr.cnes.sirius.patrius.math.random.AbstractWell`
    
        This class implements the WELL19937c pseudo-random number generator from François Panneton, Pierre L'Ecuyer and Makoto
        Matsumoto.
    
        This generator is described in a paper by François Panneton, Pierre L'Ecuyer and Makoto Matsumoto `Improved Long-Period
        Generators Based on Linear Recurrences Modulo 2 <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf>` ACM
        Transactions on Mathematical Software, 32, 1 (2006). The errata for the paper are in `wellrng-errata.txt
        <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng-errata.txt>`.
    
        Since:
            2.2
    
        Also see:
            `WELL Random number generator <http://www.iro.umontreal.ca/~panneton/WELLRNG.html>`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, intArray: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, long: int): ...

class Well44497a(AbstractWell):
    """
    public class Well44497a extends :class:`~fr.cnes.sirius.patrius.math.random.AbstractWell`
    
        This class implements the WELL44497a pseudo-random number generator from François Panneton, Pierre L'Ecuyer and Makoto
        Matsumoto.
    
        This generator is described in a paper by François Panneton, Pierre L'Ecuyer and Makoto Matsumoto `Improved Long-Period
        Generators Based on Linear Recurrences Modulo 2 <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf>` ACM
        Transactions on Mathematical Software, 32, 1 (2006). The errata for the paper are in `wellrng-errata.txt
        <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng-errata.txt>`.
    
        Since:
            2.2
    
        Also see:
            `WELL Random number generator <http://www.iro.umontreal.ca/~panneton/WELLRNG.html>`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, intArray: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, long: int): ...

class Well44497b(AbstractWell):
    """
    public class Well44497b extends :class:`~fr.cnes.sirius.patrius.math.random.AbstractWell`
    
        This class implements the WELL44497b pseudo-random number generator from François Panneton, Pierre L'Ecuyer and Makoto
        Matsumoto.
    
        This generator is described in a paper by François Panneton, Pierre L'Ecuyer and Makoto Matsumoto `Improved Long-Period
        Generators Based on Linear Recurrences Modulo 2 <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf>` ACM
        Transactions on Mathematical Software, 32, 1 (2006). The errata for the paper are in `wellrng-errata.txt
        <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng-errata.txt>`.
    
        Since:
            2.2
    
        Also see:
            `WELL Random number generator <http://www.iro.umontreal.ca/~panneton/WELLRNG.html>`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, intArray: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, long: int): ...

class Well512a(AbstractWell):
    """
    public class Well512a extends :class:`~fr.cnes.sirius.patrius.math.random.AbstractWell`
    
        This class implements the WELL512a pseudo-random number generator from François Panneton, Pierre L'Ecuyer and Makoto
        Matsumoto.
    
        This generator is described in a paper by François Panneton, Pierre L'Ecuyer and Makoto Matsumoto `Improved Long-Period
        Generators Based on Linear Recurrences Modulo 2 <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf>` ACM
        Transactions on Mathematical Software, 32, 1 (2006). The errata for the paper are in `wellrng-errata.txt
        <http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng-errata.txt>`.
    
        Since:
            2.2
    
        Also see:
            `WELL Random number generator <http://www.iro.umontreal.ca/~panneton/WELLRNG.html>`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, intArray: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, long: int): ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.random")``.

    AbstractRandomGenerator: typing.Type[AbstractRandomGenerator]
    AbstractWell: typing.Type[AbstractWell]
    BitsStreamGenerator: typing.Type[BitsStreamGenerator]
    CorrelatedRandomVectorGenerator: typing.Type[CorrelatedRandomVectorGenerator]
    EmpiricalDistribution: typing.Type[EmpiricalDistribution]
    GaussianRandomGenerator: typing.Type[GaussianRandomGenerator]
    ISAACRandom: typing.Type[ISAACRandom]
    JDKRandomGenerator: typing.Type[JDKRandomGenerator]
    MersenneTwister: typing.Type[MersenneTwister]
    NormalizedRandomGenerator: typing.Type[NormalizedRandomGenerator]
    RandomAdaptor: typing.Type[RandomAdaptor]
    RandomDataGenerator: typing.Type[RandomDataGenerator]
    RandomGenerator: typing.Type[RandomGenerator]
    RandomVectorGenerator: typing.Type[RandomVectorGenerator]
    StableRandomGenerator: typing.Type[StableRandomGenerator]
    SynchronizedRandomGenerator: typing.Type[SynchronizedRandomGenerator]
    UncorrelatedRandomVectorGenerator: typing.Type[UncorrelatedRandomVectorGenerator]
    UniformRandomGenerator: typing.Type[UniformRandomGenerator]
    UniformlyCorrelatedRandomVectorGenerator: typing.Type[UniformlyCorrelatedRandomVectorGenerator]
    UnitSphereRandomVectorGenerator: typing.Type[UnitSphereRandomVectorGenerator]
    ValueServer: typing.Type[ValueServer]
    Well1024a: typing.Type[Well1024a]
    Well19937a: typing.Type[Well19937a]
    Well19937c: typing.Type[Well19937c]
    Well44497a: typing.Type[Well44497a]
    Well44497b: typing.Type[Well44497b]
    Well512a: typing.Type[Well512a]
