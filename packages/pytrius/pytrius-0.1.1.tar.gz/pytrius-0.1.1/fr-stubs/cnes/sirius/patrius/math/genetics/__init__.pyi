
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.exception
import fr.cnes.sirius.patrius.math.exception.util
import fr.cnes.sirius.patrius.math.random
import java.lang
import java.util
import java.util.concurrent
import jpype
import typing



class ChromosomePair:
    """
    public class ChromosomePair extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        A pair of :class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome` objects.
    
        Since:
            2.0
    """
    def __init__(self, chromosome: 'Chromosome', chromosome2: 'Chromosome'): ...
    def getFirst(self) -> 'Chromosome':
        """
            Access the first chromosome.
        
            Returns:
                the first chromosome.
        
        
        """
        ...
    def getSecond(self) -> 'Chromosome':
        """
            Access the second chromosome.
        
            Returns:
                the second chromosome.
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class CrossoverPolicy:
    """
    public interface CrossoverPolicy
    
        Policy used to create a pair of new chromosomes by performing a crossover operation on a source pair of chromosomes.
    
        Since:
            2.0
    """
    def crossover(self, chromosome: 'Chromosome', chromosome2: 'Chromosome') -> ChromosomePair:
        """
            Perform a crossover operation on the given chromosomes.
        
            Parameters:
                first (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the first chromosome.
                second (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the second chromosome.
        
            Returns:
                the pair of new chromosomes that resulted from the crossover.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the given chromosomes are not compatible with this :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`
        
        
        """
        ...

class Fitness:
    """
    public interface Fitness
    
        Fitness of a chromosome.
    
        Since:
            2.0
    """
    def fitness(self) -> float:
        """
            Compute the fitness. This is usually very time-consuming, so the value should be cached.
        
            Returns:
                fitness
        
        
        """
        ...

class GeneticAlgorithm:
    def __init__(self, crossoverPolicy: typing.Union[CrossoverPolicy, typing.Callable], double: float, mutationPolicy: typing.Union['MutationPolicy', typing.Callable], double2: float, selectionPolicy: typing.Union['SelectionPolicy', typing.Callable]): ...
    def evolve(self, population: 'Population', stoppingCondition: typing.Union['StoppingCondition', typing.Callable]) -> 'Population': ...
    def getCrossoverPolicy(self) -> CrossoverPolicy: ...
    def getCrossoverRate(self) -> float: ...
    def getGenerationsEvolved(self) -> int: ...
    def getMutationPolicy(self) -> 'MutationPolicy': ...
    def getMutationRate(self) -> float: ...
    @staticmethod
    def getRandomGenerator() -> fr.cnes.sirius.patrius.math.random.RandomGenerator: ...
    def getSelectionPolicy(self) -> 'SelectionPolicy': ...
    def nextGeneration(self, population: 'Population') -> 'Population': ...
    @staticmethod
    def setRandomGenerator(randomGenerator: fr.cnes.sirius.patrius.math.random.RandomGenerator) -> None: ...

class InvalidRepresentationException(fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException):
    """
    public class InvalidRepresentationException extends :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`
    
        Exception indicating that the representation of a chromosome is not valid.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, localizable: fr.cnes.sirius.patrius.math.exception.util.Localizable, *object: typing.Any): ...

class MutationPolicy:
    """
    public interface MutationPolicy
    
        Algorithm used to mutate a chromosome.
    
        Since:
            2.0
    """
    def mutate(self, chromosome: 'Chromosome') -> 'Chromosome':
        """
            Mutate the given chromosome.
        
            Parameters:
                original (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the original chromosome.
        
            Returns:
                the mutated chromosome.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the given chromosome is not compatible with this :class:`~fr.cnes.sirius.patrius.math.genetics.MutationPolicy`
        
        
        """
        ...

_PermutationChromosome__T = typing.TypeVar('_PermutationChromosome__T')  # <T>
class PermutationChromosome(typing.Generic[_PermutationChromosome__T]):
    """
    public interface PermutationChromosome<T>
    
        Interface indicating that the chromosome represents a permutation of objects.
    
        Since:
            2.0
    """
    def decode(self, list: java.util.List[_PermutationChromosome__T]) -> java.util.List[_PermutationChromosome__T]: ...

class Population(java.lang.Iterable['Chromosome']):
    """
    public interface Population extends `Iterable <http://docs.oracle.com/javase/8/docs/api/java/lang/Iterable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`>
    
        A collection of chromosomes that facilitates generational evolution.
    
        Since:
            2.0
    """
    def addChromosome(self, chromosome: 'Chromosome') -> None:
        """
            Add the given chromosome to the population.
        
            Parameters:
                chromosome (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the chromosome to add.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooLargeException`: if the population would exceed the population limit when adding this chromosome
        
        
        """
        ...
    def getFittestChromosome(self) -> 'Chromosome':
        """
            Access the fittest chromosome in this population.
        
            Returns:
                the fittest chromosome.
        
        
        """
        ...
    def getPopulationLimit(self) -> int:
        """
            Access the maximum population size.
        
            Returns:
                the maximum population size.
        
        
        """
        ...
    def getPopulationSize(self) -> int:
        """
            Access the current population size.
        
            Returns:
                the current population size.
        
        
        """
        ...
    def nextGeneration(self) -> 'Population':
        """
            Start the population for the next generation.
        
            Returns:
                the beginnings of the next generation.
        
        
        """
        ...

class SelectionPolicy:
    """
    public interface SelectionPolicy
    
        Algorithm used to select a chromosome pair from a population.
    
        Since:
            2.0
    """
    def select(self, population: Population) -> ChromosomePair:
        """
            Select two chromosomes from the population.
        
            Parameters:
                population (:class:`~fr.cnes.sirius.patrius.math.genetics.Population`): the population from which the chromosomes are choosen.
        
            Returns:
                the selected chromosomes.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the population is not compatible with this :class:`~fr.cnes.sirius.patrius.math.genetics.SelectionPolicy`
        
        
        """
        ...

class StoppingCondition:
    """
    public interface StoppingCondition
    
        Algorithm used to determine when to stop evolution.
    
        Since:
            2.0
    """
    def isSatisfied(self, population: Population) -> bool:
        """
            Determine whether or not the given population satisfies the stopping condition.
        
            Parameters:
                population (:class:`~fr.cnes.sirius.patrius.math.genetics.Population`): the population to test.
        
            Returns:
                :code:`true` if this stopping condition is met by the given population, :code:`false` otherwise.
        
        
        """
        ...

class BinaryMutation(MutationPolicy):
    """
    public class BinaryMutation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.genetics.MutationPolicy`
    
        Mutation for :class:`~fr.cnes.sirius.patrius.math.genetics.BinaryChromosome`s. Randomly changes one gene.
    
        Since:
            2.0
    """
    def __init__(self): ...
    def mutate(self, chromosome: 'Chromosome') -> 'Chromosome':
        """
            Mutate the given chromosome. Randomly changes one gene.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.MutationPolicy.mutate` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.MutationPolicy`
        
            Parameters:
                original (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the original chromosome.
        
            Returns:
                the mutated chromosome.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if :code:`original` is not an instance of :class:`~fr.cnes.sirius.patrius.math.genetics.BinaryChromosome`.
        
        
        """
        ...

class Chromosome(java.lang.Comparable['Chromosome'], Fitness):
    """
    public abstract class Chromosome extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`>, :class:`~fr.cnes.sirius.patrius.math.genetics.Fitness`
    
        Individual in a population. Chromosomes are compared based on their fitness.
    
        The chromosomes are IMMUTABLE, and so their fitness is also immutable and therefore it can be cached.
    
        Since:
            2.0
    """
    def __init__(self): ...
    def compareTo(self, chromosome: 'Chromosome') -> int:
        """
            Compares two chromosomes based on their fitness. The bigger the fitness, the better the chromosome.
        
            Specified by:
                 in interface 
        
            Parameters:
                another (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): another chromosome to compare
        
            Returns:
        
                  - -1 if :code:`another` is better than :code:`this`
                  - 1 if :code:`another` is worse than :code:`this`
                  - 0 if the two chromosomes have the same fitness
        
        
        
        """
        ...
    def getFitness(self) -> float:
        """
            Access the fitness of this chromosome. The bigger the fitness, the better the chromosome.
        
            Computation of fitness is usually very time-consuming task, therefore the fitness is cached.
        
            Returns:
                the fitness
        
        
        """
        ...
    def searchForFitnessUpdate(self, population: Population) -> None:
        """
            Searches the population for a chromosome representing the same solution, and if it finds one, updates the fitness to its
            value.
        
            Parameters:
                population (:class:`~fr.cnes.sirius.patrius.math.genetics.Population`): Population to search
        
        
        """
        ...

_CycleCrossover__T = typing.TypeVar('_CycleCrossover__T')  # <T>
class CycleCrossover(CrossoverPolicy, typing.Generic[_CycleCrossover__T]):
    """
    public class CycleCrossover<T> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`
    
        Cycle Crossover [CX] builds offspring from **ordered** chromosomes by identifying cycles between two parent chromosomes.
        To form the children, the cycles are copied from the respective parents.
    
        To form a cycle the following procedure is applied:
    
          1.  start with the first gene of parent 1
          2.  look at the gene at the same position of parent 2
          3.  go to the position with the same gene in parent 1
          4.  add this gene index to the cycle
          5.  repeat the steps 2-5 until we arrive at the starting gene of this cycle
    
        The indices that form a cycle are then used to form the children in alternating order, i.e. in cycle 1, the genes of
        parent 1 are copied to child 1, while in cycle 2 the genes of parent 1 are copied to child 2, and so forth ...
        Example (zero-start cycle):
    
        .. code-block: java
        
        
         p1 = (8 4 7 3 6 2 5 1 9 0)    X   c1 = (8 1 2 3 4 5 6 7 9 0)
         p2 = (0 1 2 3 4 5 6 7 8 9)    X   c2 = (0 4 7 3 6 2 5 1 8 9)
         
         cycle 1: 8 0 9
         cycle 2: 4 1 7 2 5 6
         cycle 3: 3
         
        This policy works only on :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`, and therefore it is
        parameterized by T. Moreover, the chromosomes must have same lengths.
    
        Since:
            3.1
    
        Also see:
            ` Cycle Crossover Operator
            <http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/CycleCrossoverOperator.aspx>`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...
    def crossover(self, chromosome: Chromosome, chromosome2: Chromosome) -> ChromosomePair:
        """
            Perform a crossover operation on the given chromosomes.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy.crossover` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`
        
            Parameters:
                first (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the first chromosome.
                second (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the second chromosome.
        
            Returns:
                the pair of new chromosomes that resulted from the crossover.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the chromosomes are not an instance of :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the length of the two chromosomes is different
        
        
        """
        ...
    def isRandomStart(self) -> bool:
        """
            Returns whether the starting index is chosen randomly or set to zero.
        
            Returns:
                :code:`true` if the starting index is chosen randomly, :code:`false` otherwise
        
        
        """
        ...

class FixedElapsedTime(StoppingCondition):
    """
    public class FixedElapsedTime extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.genetics.StoppingCondition`
    
        Stops after a fixed amount of time has elapsed.
    
        The first time :meth:`~fr.cnes.sirius.patrius.math.genetics.FixedElapsedTime.isSatisfied` is invoked, the end time of
        the evolution is determined based on the provided :code:`maxTime` value. Once the elapsed time reaches the configured
        :code:`maxTime` value, :meth:`~fr.cnes.sirius.patrius.math.genetics.FixedElapsedTime.isSatisfied` returns true.
    
        Since:
            3.1
    """
    @typing.overload
    def __init__(self, long: int): ...
    @typing.overload
    def __init__(self, long: int, timeUnit: java.util.concurrent.TimeUnit): ...
    def isSatisfied(self, population: Population) -> bool:
        """
            Determine whether or not the maximum allowed time has passed. The termination time is determined after the first
            generation.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.StoppingCondition.isSatisfied` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.StoppingCondition`
        
            Parameters:
                population (:class:`~fr.cnes.sirius.patrius.math.genetics.Population`): ignored (no impact on result)
        
            Returns:
                :code:`true` IFF the maximum allowed time period has elapsed
        
        
        """
        ...

class FixedGenerationCount(StoppingCondition):
    """
    public class FixedGenerationCount extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.genetics.StoppingCondition`
    
        Stops after a fixed number of generations. Each time
        :meth:`~fr.cnes.sirius.patrius.math.genetics.FixedGenerationCount.isSatisfied` is invoked, a generation counter is
        incremented. Once the counter reaches the configured :code:`maxGenerations` value,
        :meth:`~fr.cnes.sirius.patrius.math.genetics.FixedGenerationCount.isSatisfied` returns true.
    
        Since:
            2.0
    """
    def __init__(self, int: int): ...
    def getNumGenerations(self) -> int:
        """
            Returns the number of generations that have already passed.
        
            Returns:
                the number of generations that have passed
        
        
        """
        ...
    def isSatisfied(self, population: Population) -> bool:
        """
            Determine whether or not the given number of generations have passed. Increments the number of generations counter if
            the maximum has not been reached.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.StoppingCondition.isSatisfied` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.StoppingCondition`
        
            Parameters:
                population (:class:`~fr.cnes.sirius.patrius.math.genetics.Population`): ignored (no impact on result)
        
            Returns:
                :code:`true` IFF the maximum number of generations has been exceeded
        
        
        """
        ...

class ListPopulation(Population):
    """
    public abstract class ListPopulation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.genetics.Population`
    
        Population of chromosomes represented by a `null
        <http://docs.oracle.com/javase/8/docs/api/java/util/List.html?is-external=true>`.
    
        Since:
            2.0
    """
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, list: java.util.List[Chromosome], int: int): ...
    def addChromosome(self, chromosome: Chromosome) -> None:
        """
            Add the given chromosome to the population.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.Population.addChromosome` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.Population`
        
            Parameters:
                chromosome (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the chromosome to add.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooLargeException`: if the population would exceed the :code:`populationLimit` after adding this chromosome
        
        
        """
        ...
    def addChromosomes(self, collection: typing.Union[java.util.Collection[Chromosome], typing.Sequence[Chromosome], typing.Set[Chromosome]]) -> None: ...
    def getChromosomes(self) -> java.util.List[Chromosome]: ...
    def getFittestChromosome(self) -> Chromosome:
        """
            Access the fittest chromosome in this population.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.Population.getFittestChromosome` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.Population`
        
            Returns:
                the fittest chromosome.
        
        
        """
        ...
    def getPopulationLimit(self) -> int:
        """
            Access the maximum population size.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.Population.getPopulationLimit` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.Population`
        
            Returns:
                the maximum population size.
        
        
        """
        ...
    def getPopulationSize(self) -> int:
        """
            Access the current population size.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.Population.getPopulationSize` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.Population`
        
            Returns:
                the current population size.
        
        
        """
        ...
    def iterator(self) -> java.util.Iterator[Chromosome]: ...
    def setPopulationLimit(self, int: int) -> None:
        """
            Sets the maximal population size.
        
            Parameters:
                populationLimitIn (int): maximal population size.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NotPositiveException`: if the population limit is not a positive number (< 1)
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the new population size is smaller than the current number of chromosomes in the population
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

_NPointCrossover__T = typing.TypeVar('_NPointCrossover__T')  # <T>
class NPointCrossover(CrossoverPolicy, typing.Generic[_NPointCrossover__T]):
    """
    public class NPointCrossover<T> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`
    
        N-point crossover policy. For each iteration a random crossover point is selected and the first part from each parent is
        copied to the corresponding child, and the second parts are copied crosswise. Example (2-point crossover):
    
        .. code-block: java
        
        
         -C- denotes a crossover point
                   -C-       -C-                         -C-        -C-
         p1 = (1 0  | 1 0 0 1 | 0 1 1)    X    p2 = (0 1  | 1 0 1 0  | 1 1 1)
              \----/ \-------/ \-----/              \----/ \--------/ \-----/
                ||      (*)       ||                  ||      (**)       ||
                VV      (**)      VV                  VV      (*)        VV
              /----\ /--------\ /-----\             /----\ /--------\ /-----\
         c1 = (1 0  | 1 0 1 0  | 0 1 1)    X   c2 = (0 1  | 1 0 0 1  | 0 1 1)
         
        This policy works only on :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`, and therefore it is
        parameterized by T. Moreover, the chromosomes must have same lengths.
    
        Since:
            3.1
    """
    def __init__(self, int: int): ...
    def crossover(self, chromosome: Chromosome, chromosome2: Chromosome) -> ChromosomePair:
        """
            Performs a N-point crossover. N random crossover points are selected and are used to divide the parent chromosomes into
            segments. The segments are copied in alternate order from the two parents to the corresponding child chromosomes.
            Example (2-point crossover):
        
            .. code-block: java
            
            
             -C- denotes a crossover point
                       -C-       -C-                         -C-        -C-
             p1 = (1 0  | 1 0 0 1 | 0 1 1)    X    p2 = (0 1  | 1 0 1 0  | 1 1 1)
                  \----/ \-------/ \-----/              \----/ \--------/ \-----/
                    ||      (*)       ||                  ||      (**)       ||
                    VV      (**)      VV                  VV      (*)        VV
                  /----\ /--------\ /-----\             /----\ /--------\ /-----\
             c1 = (1 0  | 1 0 1 0  | 0 1 1)    X   c2 = (0 1  | 1 0 0 1  | 0 1 1)
             
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy.crossover` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`
        
            Parameters:
                first (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): first parent (p1)
                second (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): second parent (p2)
        
            Returns:
                pair of two children (c1,c2)
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: iff one of the chromosomes is not an instance of :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the length of the two chromosomes is different
        
        
        """
        ...
    def getCrossoverPoints(self) -> int:
        """
            Returns the number of crossover points used by this :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`.
        
            Returns:
                the number of crossover points
        
        
        """
        ...

_OnePointCrossover__T = typing.TypeVar('_OnePointCrossover__T')  # <T>
class OnePointCrossover(CrossoverPolicy, typing.Generic[_OnePointCrossover__T]):
    """
    public class OnePointCrossover<T> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`
    
        One point crossover policy. A random crossover point is selected and the first part from each parent is copied to the
        corresponding child, and the second parts are copied crosswise. Example:
    
        .. code-block: java
        
        
         -C- denotes a crossover point
                           -C-                                 -C-
         p1 = (1 0 1 0 0 1  | 0 1 1)    X    p2 = (0 1 1 0 1 0  | 1 1 1)
              \------------/ \-----/              \------------/ \-----/
                    ||         (*)                       ||        (**)
                    VV         (**)                      VV        (*)
              /------------\ /-----\              /------------\ /-----\
         c1 = (1 0 1 0 0 1  | 1 1 1)    X    c2 = (0 1 1 0 1 0  | 0 1 1)
         
        This policy works only on :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`, and therefore it is
        parameterized by T. Moreover, the chromosomes must have same lengths.
    
        Since:
            2.0
    """
    def __init__(self): ...
    def crossover(self, chromosome: Chromosome, chromosome2: Chromosome) -> ChromosomePair:
        """
            Performs one point crossover. A random crossover point is selected and the first part from each parent is copied to the
            corresponding child, and the second parts are copied crosswise. Example:
        
            .. code-block: java
            
            
             -C- denotes a crossover point
                               -C-                                 -C-
             p1 = (1 0 1 0 0 1  | 0 1 1)    X    p2 = (0 1 1 0 1 0  | 1 1 1)
                  \------------/ \-----/              \------------/ \-----/
                        ||         (*)                       ||        (**)
                        VV         (**)                      VV        (*)
                  /------------\ /-----\              /------------\ /-----\
             c1 = (1 0 1 0 0 1  | 1 1 1)    X    c2 = (0 1 1 0 1 0  | 0 1 1)
             
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy.crossover` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`
        
            Parameters:
                first (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): first parent (p1)
                second (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): second parent (p2)
        
            Returns:
                pair of two children (c1,c2)
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: iff one of the chromosomes is not an instance of :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the length of the two chromosomes is different
        
        
        """
        ...

_OrderedCrossover__T = typing.TypeVar('_OrderedCrossover__T')  # <T>
class OrderedCrossover(CrossoverPolicy, typing.Generic[_OrderedCrossover__T]):
    """
    public class OrderedCrossover<T> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`
    
        Order 1 Crossover [OX1] builds offspring from **ordered** chromosomes by copying a consecutive slice from one parent,
        and filling up the remaining genes from the other parent as they appear.
    
        This policy works by applying the following rules:
    
          1.  select a random slice of consecutive genes from parent 1
          2.  copy the slice to child 1 and mark out the genes in parent 2
          3.  starting from the right side of the slice, copy genes from parent 2 as they appear to child 1 if they are not yet marked
            out.
    
    
        Example (random sublist from index 3 to 7, underlined):
    
        .. code-block: java
        
        
         p1 = (8 4 7 3 6 2 5 1 9 0)   X   c1 = (0 4 7 3 6 2 5 1 8 9)
                     ---------                        ---------
         p2 = (0 1 2 3 4 5 6 7 8 9)   X   c2 = (8 1 2 3 4 5 6 7 9 0)
         
    
        This policy works only on :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`, and therefore it is
        parameterized by T. Moreover, the chromosomes must have same lengths.
    
        Since:
            3.1
    
        Also see:
            ` Order 1 Crossover Operator
            <http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/Order1CrossoverOperator.aspx>`
    """
    def __init__(self): ...
    def crossover(self, chromosome: Chromosome, chromosome2: Chromosome) -> ChromosomePair:
        """
            Perform a crossover operation on the given chromosomes.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy.crossover` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`
        
            Parameters:
                first (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the first chromosome.
                second (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the second chromosome.
        
            Returns:
                the pair of new chromosomes that resulted from the crossover.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: iff one of the chromosomes is not an instance of :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the length of the two chromosomes is different
        
        
        """
        ...

class RandomKeyMutation(MutationPolicy):
    """
    public class RandomKeyMutation extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.genetics.MutationPolicy`
    
        Mutation operator for :class:`~fr.cnes.sirius.patrius.math.genetics.RandomKey`s. Changes a randomly chosen element of
        the array representation to a random value uniformly distributed in [0,1].
    
        Since:
            2.0
    """
    def __init__(self): ...
    def mutate(self, chromosome: Chromosome) -> Chromosome:
        """
            Mutate the given chromosome.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.MutationPolicy.mutate` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.MutationPolicy`
        
            Parameters:
                original (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the original chromosome.
        
            Returns:
                the mutated chromosome.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if :code:`original` is not a :class:`~fr.cnes.sirius.patrius.math.genetics.RandomKey` instance
        
        
        """
        ...

class TournamentSelection(SelectionPolicy):
    """
    public class TournamentSelection extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.genetics.SelectionPolicy`
    
        Tournament selection scheme. Each of the two selected chromosomes is selected based on n-ary tournament -- this is done
        by drawing :meth:`~fr.cnes.sirius.patrius.math.genetics.TournamentSelection.arity` random chromosomes without
        replacement from the population, and then selecting the fittest chromosome among them.
    
        Since:
            2.0
    """
    def __init__(self, int: int): ...
    def getArity(self) -> int:
        """
            Gets the arity (number of chromosomes drawn to the tournament).
        
            Returns:
                arity of the tournament
        
        
        """
        ...
    def select(self, population: Population) -> ChromosomePair:
        """
            Select two chromosomes from the population. Each of the two selected chromosomes is selected based on n-ary tournament
            -- this is done by drawing :meth:`~fr.cnes.sirius.patrius.math.genetics.TournamentSelection.arity` random chromosomes
            without replacement from the population, and then selecting the fittest chromosome among them.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.SelectionPolicy.select` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.SelectionPolicy`
        
            Parameters:
                population (:class:`~fr.cnes.sirius.patrius.math.genetics.Population`): the population from which the chromosomes are chosen.
        
            Returns:
                the selected chromosomes.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the tournament arity is bigger than the population size
        
        
        """
        ...
    def setArity(self, int: int) -> None:
        """
            Sets the arity (number of chromosomes drawn to the tournament).
        
            Parameters:
                arityIn (int): arity of the tournament
        
        
        """
        ...

_UniformCrossover__T = typing.TypeVar('_UniformCrossover__T')  # <T>
class UniformCrossover(CrossoverPolicy, typing.Generic[_UniformCrossover__T]):
    """
    public class UniformCrossover<T> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`
    
        Perform Uniform Crossover [UX] on the specified chromosomes. A fixed mixing ratio is used to combine genes from the
        first and second parents, e.g. using a ratio of 0.5 would result in approximately 50% of genes coming from each parent.
        This is typically a poor method of crossover, but empirical evidence suggests that it is more exploratory and results in
        a larger part of the problem space being searched.
    
        This crossover policy evaluates each gene of the parent chromosomes by chosing a uniform random number :code:`p` in the
        range [0, 1]. If :code:`p` < :code:`ratio`, the parent genes are swapped. This means with a ratio of 0.7, 30% of the
        genes from the first parent and 70% from the second parent will be selected for the first offspring (and vice versa for
        the second offspring).
    
        This policy works only on :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`, and therefore it is
        parameterized by T. Moreover, the chromosomes must have same lengths.
    
        Since:
            3.1
    
        Also see:
            `Crossover techniques (Wikipedia) <http://en.wikipedia.org/wiki/Crossover_%28genetic_algorithm%29>`, `Crossover
            (Obitko.com) <http://www.obitko.com/tutorials/genetic-algorithms/crossover-mutation.php>`, `Uniform crossover
            <http://www.tomaszgwiazda.com/uniformX.htm>`
    """
    def __init__(self, double: float): ...
    def crossover(self, chromosome: Chromosome, chromosome2: Chromosome) -> ChromosomePair:
        """
            Perform a crossover operation on the given chromosomes.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy.crossover` in
                interface :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`
        
            Parameters:
                first (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the first chromosome.
                second (:class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`): the second chromosome.
        
            Returns:
                the pair of new chromosomes that resulted from the crossover.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: iff one of the chromosomes is not an instance of :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the length of the two chromosomes is different
        
        
        """
        ...
    def getRatio(self) -> float:
        """
            Returns the mixing ratio used by this :class:`~fr.cnes.sirius.patrius.math.genetics.CrossoverPolicy`.
        
            Returns:
                the mixing ratio
        
        
        """
        ...

_AbstractListChromosome__T = typing.TypeVar('_AbstractListChromosome__T')  # <T>
class AbstractListChromosome(Chromosome, typing.Generic[_AbstractListChromosome__T]):
    """
    public abstract class AbstractListChromosome<T> extends :class:`~fr.cnes.sirius.patrius.math.genetics.Chromosome`
    
        Chromosome represented by an immutable list of a fixed length.
    
        Since:
            2.0
    """
    @typing.overload
    def __init__(self, tArray: typing.Union[typing.List[_AbstractListChromosome__T], jpype.JArray]): ...
    @typing.overload
    def __init__(self, list: java.util.List[_AbstractListChromosome__T]): ...
    def getLength(self) -> int:
        """
            Returns the length of the chromosome.
        
            Returns:
                the length of the chromosome
        
        
        """
        ...
    def newFixedLengthChromosome(self, list: java.util.List[_AbstractListChromosome__T]) -> 'AbstractListChromosome'[_AbstractListChromosome__T]: ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class ElitisticListPopulation(ListPopulation):
    """
    public class ElitisticListPopulation extends :class:`~fr.cnes.sirius.patrius.math.genetics.ListPopulation`
    
        Population of chromosomes which uses elitism (certain percentage of the best chromosomes is directly copied to the next
        generation).
    
        Since:
            2.0
    """
    @typing.overload
    def __init__(self, int: int, double: float): ...
    @typing.overload
    def __init__(self, list: java.util.List[Chromosome], int: int, double: float): ...
    def getElitismRate(self) -> float:
        """
            Access the elitism rate.
        
            Returns:
                the elitism rate
        
        
        """
        ...
    def nextGeneration(self) -> Population:
        """
            Start the population for the next generation. The
            :meth:`~fr.cnes.sirius.patrius.math.genetics.ElitisticListPopulation.elitismRate` percents of the best chromosomes are
            directly copied to the next generation.
        
            Returns:
                the beginnings of the next generation.
        
        
        """
        ...
    def setElitismRate(self, double: float) -> None:
        """
            Sets the elitism rate, i.e. how many best chromosomes will be directly transferred to the next generation [in %].
        
            Parameters:
                elitismRateIn (double): how many best chromosomes will be directly transferred to the next generation [in %]
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if the elitism rate is outside the [0, 1] range
        
        
        """
        ...

class BinaryChromosome(AbstractListChromosome[int]):
    """
    public abstract class BinaryChromosome extends :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`<`Integer <http://docs.oracle.com/javase/8/docs/api/java/lang/Integer.html?is-external=true>`>
    
        Chromosome represented by a vector of 0s and 1s.
    
        Since:
            2.0
    """
    @typing.overload
    def __init__(self, integerArray: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, list: java.util.List[int]): ...
    @staticmethod
    def randomBinaryRepresentation(int: int) -> java.util.List[int]: ...

_RandomKey__T = typing.TypeVar('_RandomKey__T')  # <T>
class RandomKey(AbstractListChromosome[float], PermutationChromosome[_RandomKey__T], typing.Generic[_RandomKey__T]):
    """
    public abstract class RandomKey<T> extends :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`<`Double <http://docs.oracle.com/javase/8/docs/api/java/lang/Double.html?is-external=true>`> implements :class:`~fr.cnes.sirius.patrius.math.genetics.PermutationChromosome`<T>
    
        Random Key chromosome is used for permutation representation. It is a vector of a fixed length of real numbers in [0,1]
        interval. The index of the i-th smallest value in the vector represents an i-th member of the permutation.
    
        For example, the random key [0.2, 0.3, 0.8, 0.1] corresponds to the permutation of indices (3,0,1,2). If the original
        (unpermuted) sequence would be (a,b,c,d), this would mean the sequence (d,a,b,c).
    
        With this representation, common operators like n-point crossover can be used, because any such chromosome represents a
        valid permutation.
    
        Since the chromosome (and thus its arrayRepresentation) is immutable, the array representation is sorted only once in
        the constructor.
    
        For details, see:
    
          - Bean, J.C.: Genetic algorithms and random keys for sequencing and optimization. ORSA Journal on Computing 6 (1994)
            154-160
          - Rothlauf, F.: Representations for Genetic and Evolutionary Algorithms. Volume 104 of Studies in Fuzziness and Soft
            Computing. Physica-Verlag, Heidelberg (2002)
    
    
        Since:
            2.0
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, list: java.util.List[float]): ...
    _comparatorPermutation__S = typing.TypeVar('_comparatorPermutation__S')  # <S>
    @staticmethod
    def comparatorPermutation(list: java.util.List[_comparatorPermutation__S], comparator: typing.Union[java.util.Comparator[_comparatorPermutation__S], typing.Callable[[_comparatorPermutation__S, _comparatorPermutation__S], int]]) -> java.util.List[float]: ...
    def decode(self, list: java.util.List[_RandomKey__T]) -> java.util.List[_RandomKey__T]: ...
    @staticmethod
    def identityPermutation(int: int) -> java.util.List[float]: ...
    _inducedPermutation__S = typing.TypeVar('_inducedPermutation__S')  # <S>
    @staticmethod
    def inducedPermutation(list: java.util.List[_inducedPermutation__S], list2: java.util.List[_inducedPermutation__S]) -> java.util.List[float]: ...
    @staticmethod
    def randomPermutation(int: int) -> java.util.List[float]: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome.toString` in
                class :class:`~fr.cnes.sirius.patrius.math.genetics.AbstractListChromosome`
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.genetics")``.

    AbstractListChromosome: typing.Type[AbstractListChromosome]
    BinaryChromosome: typing.Type[BinaryChromosome]
    BinaryMutation: typing.Type[BinaryMutation]
    Chromosome: typing.Type[Chromosome]
    ChromosomePair: typing.Type[ChromosomePair]
    CrossoverPolicy: typing.Type[CrossoverPolicy]
    CycleCrossover: typing.Type[CycleCrossover]
    ElitisticListPopulation: typing.Type[ElitisticListPopulation]
    Fitness: typing.Type[Fitness]
    FixedElapsedTime: typing.Type[FixedElapsedTime]
    FixedGenerationCount: typing.Type[FixedGenerationCount]
    GeneticAlgorithm: typing.Type[GeneticAlgorithm]
    InvalidRepresentationException: typing.Type[InvalidRepresentationException]
    ListPopulation: typing.Type[ListPopulation]
    MutationPolicy: typing.Type[MutationPolicy]
    NPointCrossover: typing.Type[NPointCrossover]
    OnePointCrossover: typing.Type[OnePointCrossover]
    OrderedCrossover: typing.Type[OrderedCrossover]
    PermutationChromosome: typing.Type[PermutationChromosome]
    Population: typing.Type[Population]
    RandomKey: typing.Type[RandomKey]
    RandomKeyMutation: typing.Type[RandomKeyMutation]
    SelectionPolicy: typing.Type[SelectionPolicy]
    StoppingCondition: typing.Type[StoppingCondition]
    TournamentSelection: typing.Type[TournamentSelection]
    UniformCrossover: typing.Type[UniformCrossover]
