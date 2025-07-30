
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.linear
import fr.cnes.sirius.patrius.math.optim
import fr.cnes.sirius.patrius.math.optim.nonlinear.vector.jacobian
import fr.cnes.sirius.patrius.math.random
import jpype
import typing



class ModelFunction(fr.cnes.sirius.patrius.math.optim.OptimizationData):
    """
    public class ModelFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.OptimizationData`
    
        Model (vector) function to be optimized.
    
        Since:
            3.1
    """
    def __init__(self, multivariateVectorFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction, typing.Callable]): ...
    def getModelFunction(self) -> fr.cnes.sirius.patrius.math.analysis.MultivariateVectorFunction:
        """
            Gets the model function to be optimized.
        
            Returns:
                the model function.
        
        
        """
        ...

class ModelFunctionJacobian(fr.cnes.sirius.patrius.math.optim.OptimizationData):
    """
    public class ModelFunctionJacobian extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.optim.OptimizationData`
    
        Jacobian of the model (vector) function to be optimized.
    
        Since:
            3.1
    """
    def __init__(self, multivariateMatrixFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.MultivariateMatrixFunction, typing.Callable]): ...
    def getModelFunctionJacobian(self) -> fr.cnes.sirius.patrius.math.analysis.MultivariateMatrixFunction:
        """
            Gets the Jacobian of the model function to be optimized.
        
            Returns:
                the model function Jacobian.
        
        
        """
        ...

class MultiStartMultivariateVectorOptimizer(fr.cnes.sirius.patrius.math.optim.BaseMultiStartMultivariateOptimizer[fr.cnes.sirius.patrius.math.optim.PointVectorValuePair]):
    def __init__(self, multivariateVectorOptimizer: 'MultivariateVectorOptimizer', int: int, randomVectorGenerator: typing.Union[fr.cnes.sirius.patrius.math.random.RandomVectorGenerator, typing.Callable]): ...
    def getOptima(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.optim.PointVectorValuePair]: ...

class MultivariateVectorOptimizer(fr.cnes.sirius.patrius.math.optim.BaseMultivariateOptimizer[fr.cnes.sirius.patrius.math.optim.PointVectorValuePair]):
    def getTarget(self) -> typing.MutableSequence[float]: ...
    def getTargetSize(self) -> int: ...
    def getWeight(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...
    def optimize(self, *optimizationData: fr.cnes.sirius.patrius.math.optim.OptimizationData) -> fr.cnes.sirius.patrius.math.optim.PointVectorValuePair: ...

class Target(fr.cnes.sirius.patrius.math.optim.OptimizationData):
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    def getTarget(self) -> typing.MutableSequence[float]: ...

class Weight(fr.cnes.sirius.patrius.math.optim.OptimizationData):
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, realMatrix: fr.cnes.sirius.patrius.math.linear.RealMatrix): ...
    def getWeight(self) -> fr.cnes.sirius.patrius.math.linear.RealMatrix: ...

class JacobianMultivariateVectorOptimizer(MultivariateVectorOptimizer):
    def optimize(self, *optimizationData: fr.cnes.sirius.patrius.math.optim.OptimizationData) -> fr.cnes.sirius.patrius.math.optim.PointVectorValuePair: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.nonlinear.vector")``.

    JacobianMultivariateVectorOptimizer: typing.Type[JacobianMultivariateVectorOptimizer]
    ModelFunction: typing.Type[ModelFunction]
    ModelFunctionJacobian: typing.Type[ModelFunctionJacobian]
    MultiStartMultivariateVectorOptimizer: typing.Type[MultiStartMultivariateVectorOptimizer]
    MultivariateVectorOptimizer: typing.Type[MultivariateVectorOptimizer]
    Target: typing.Type[Target]
    Weight: typing.Type[Weight]
    jacobian: fr.cnes.sirius.patrius.math.optim.nonlinear.vector.jacobian.__module_protocol__
