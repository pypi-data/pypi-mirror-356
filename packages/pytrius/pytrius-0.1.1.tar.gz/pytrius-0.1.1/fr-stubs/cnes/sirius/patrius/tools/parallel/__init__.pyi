
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util.concurrent
import typing



class ParallelException(java.lang.RuntimeException):
    """
    public class ParallelException extends `RuntimeException <http://docs.oracle.com/javase/8/docs/api/java/lang/RuntimeException.html?is-external=true>`
    
        Extends RuntimeException for this package.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, string: str): ...
    @typing.overload
    def __init__(self, string: str, throwable: java.lang.Throwable): ...
    @typing.overload
    def __init__(self, throwable: java.lang.Throwable): ...

class ParallelResult:
    """
    public interface ParallelResult
    
        Holds results for a ParallelTask implementation.
    
        Since:
            1.2
    """
    def getDataAsArray(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Gets the result data as an array of arrays.
        
            Returns:
                an array of arrays of doubles
        
        
        """
        ...
    def resultEquals(self, parallelResult: 'ParallelResult') -> bool:
        """
            Equals-like method for ParallelResult instances. Unlike the regular equals() method, this forces the implementation to
            provide an explicit implementation.
        
            Parameters:
                other (:class:`~fr.cnes.sirius.patrius.tools.parallel.ParallelResult`): other parallel result
        
            Returns:
                true when the two implementations are equal, false otherwise
        
        
        """
        ...

class ParallelRunner:
    """
    public class ParallelRunner extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Runner for parallel tests written as ParallelTask instances.
    
        Since:
            1.2
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    def addTask(self, parallelTaskFactory: 'ParallelTaskFactory'[typing.Any], int: int) -> None:
        """
            Adds a new task factory, with the number of instances it should provide, OR updates the number of instances if the task
            factory was added before. The task factory provides ParallelTask instances. Each instance will be run once and produce a
            result.
        
            Parameters:
                taskFactory (:class:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTaskFactory`<?> taskFactory): the task factory
                nbRuns (int): the number of instances to create, equal to the number of "runs" for the matching ParallelTask class.
        
        
        """
        ...
    def getResultSummary(self) -> str:
        """
            Gets the result summary.
        
            Returns:
                the result summary (empty string if called too early)
        
        
        """
        ...
    def resizeThreadPool(self, int: int) -> None:
        """
            Resizes the thread pool.
        
            Parameters:
                thPoolSize (int): new thread pool size
        
        
        """
        ...
    def runAll(self) -> bool: ...

class ParallelTask(java.util.concurrent.Callable[ParallelResult]):
    """
    public interface ParallelTask extends `Callable <http://docs.oracle.com/javase/8/docs/api/java/util/concurrent/Callable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.tools.parallel.ParallelResult`>
    
        A ParallelTask instance is meant to be run once by the ParallelRunner in a multithreaded context.
    
        Since:
            1.2
    """
    def call(self) -> ParallelResult:
        """
        
            Specified by:
                 in interface 
        
        
        """
        ...
    def getResult(self) -> ParallelResult:
        """
            Asynchronous getter for the results. Is meant to be called after call to call(), and call() has ended. Otherwise
            behavior is unpredictable.
        
            Returns:
                the same ParallelResult object already returned by call()
        
        
        """
        ...
    def getTaskInfo(self) -> str:
        """
            Returns human-readable info on the status of the task. Is intended to change depending on the current state of the task.
        
            Returns:
                the status of the task.
        
        
        """
        ...
    def getTaskLabel(self) -> str:
        """
            Returns a label identifying the task "class". It's the same for all instances of the task.
        
            Returns:
                the task label
        
        
        """
        ...

_ParallelTaskFactory__T = typing.TypeVar('_ParallelTaskFactory__T', bound=ParallelTask)  # <T>
class ParallelTaskFactory(typing.Generic[_ParallelTaskFactory__T]):
    """
    public interface ParallelTaskFactory<T extends :class:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask`>
    
        A ParallelTaskFactory is used to create ParallelTask instances.
    
        Since:
            1.2
    """
    def newInstance(self) -> _ParallelTaskFactory__T:
        """
            Factory method providing new instances of T.
        
            Returns:
                a new ParallelType implementation instance.
        
        
        """
        ...
    def reset(self) -> None:
        """
            Reset method, if the factory maintains a state for the tasks.
        
        """
        ...

class AbstractSimpleParallelTaskImpl(ParallelTask):
    """
    public abstract class AbstractSimpleParallelTaskImpl extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask`
    
        Simple, abstract implementation for a ParallelTask. Serves as a base for generic, simple implementations of
        ParallelTask, or as a starting example for other implementations. Provides simple implementations for
        :meth:`~fr.cnes.sirius.patrius.tools.parallel.AbstractSimpleParallelTaskImpl.getTaskLabel` and
        :meth:`~fr.cnes.sirius.patrius.tools.parallel.AbstractSimpleParallelTaskImpl.getTaskInfo`, which may be enough for most
        cases. The developer extending this class only needs to provide the
        :meth:`~fr.cnes.sirius.patrius.tools.parallel.AbstractSimpleParallelTaskImpl.callImpl` method.
    
        Since:
            1.2
    """
    def call(self) -> ParallelResult:
        """
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask.call` in
                interface :class:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask`
        
            Specified by:
                 in interface 
        
        
        """
        ...
    def getId(self) -> int:
        """
        
            Returns:
                the id
        
        
        """
        ...
    def getResult(self) -> ParallelResult:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask.getResult`
            Asynchronous getter for the results. Is meant to be called after call to call(), and call() has ended. Otherwise
            behavior is unpredictable.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask.getResult` in
                interface :class:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask`
        
            Returns:
                the same ParallelResult object already returned by call()
        
        
        """
        ...
    def getTaskInfo(self) -> str:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask.getTaskInfo`
            Returns human-readable info on the status of the task. Is intended to change depending on the current state of the task.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask.getTaskInfo` in
                interface :class:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask`
        
            Returns:
                the status of the task.
        
        
        """
        ...
    def getTaskLabel(self) -> str:
        """
            Description copied from interface: :meth:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask.getTaskLabel`
            Returns a label identifying the task "class". It's the same for all instances of the task.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask.getTaskLabel` in
                interface :class:`~fr.cnes.sirius.patrius.tools.parallel.ParallelTask`
        
            Returns:
                the task label
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.tools.parallel")``.

    AbstractSimpleParallelTaskImpl: typing.Type[AbstractSimpleParallelTaskImpl]
    ParallelException: typing.Type[ParallelException]
    ParallelResult: typing.Type[ParallelResult]
    ParallelRunner: typing.Type[ParallelRunner]
    ParallelTask: typing.Type[ParallelTask]
    ParallelTaskFactory: typing.Type[ParallelTaskFactory]
