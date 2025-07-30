
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import java.util
import typing



class LebedevFunction:
    """
    public interface LebedevFunction
    
        An interface representing a Lebedev function (i.e. a function taking a LebedevGridPoint as argument).
    
        Since:
            4.1
    """
    def value(self, lebedevGridPoint: 'LebedevGridPoint') -> float:
        """
            Compute the value of the function at the given grid point.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.analysis.integration.sphere.lebedev.LebedevGridPoint`): the grid point at which the function must be evaluated
        
            Returns:
                the function value for the given grid point
        
        
        """
        ...

class LebedevGrid:
    @typing.overload
    def __init__(self, lebedevGrid: 'LebedevGrid'): ...
    @typing.overload
    def __init__(self, list: java.util.List['LebedevGridPoint']): ...
    @typing.overload
    def getDuplicates(self, lebedevGrid: 'LebedevGrid', double: float) -> java.util.List['LebedevGridPoint']: ...
    @typing.overload
    def getDuplicates(self, list: java.util.List['LebedevGridPoint'], double: float) -> java.util.List['LebedevGridPoint']: ...
    def getPoints(self) -> java.util.List['LebedevGridPoint']: ...
    def getSize(self) -> int: ...
    def getTotalWeight(self) -> float: ...

class LebedevGridPoint:
    """
    public class LebedevGridPoint extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Lebedev grid point.
    
        Since:
            4.0
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float): ...
    def getPhi(self) -> float:
        """
            Gets the azimuth angle between 0° (included) and 360° (excluded).
        
            Returns:
                the azimuth angle
        
        
        """
        ...
    def getRadius(self) -> float:
        """
            Gets the radius.
        
            Returns:
                the radius
        
        
        """
        ...
    def getTheta(self) -> float:
        """
            Gets the inclination angle between 0° (included) and 180° (included).
        
            Returns:
                the inclination angle
        
        
        """
        ...
    def getWeight(self) -> float:
        """
            Gets the weight associated to the point for Lebedev's rule.
        
            Returns:
                the weight associated to the point
        
        
        """
        ...
    def getX(self) -> float:
        """
            Gets the coordinate of the point on the 1st axis.
        
            Returns:
                the x coordinate of the point
        
        
        """
        ...
    def getXYZ(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
            Gets the Cartesian coordinates of the point.
        
            Returns:
                the Cartesian coordinates of the point
        
        
        """
        ...
    def getY(self) -> float:
        """
            Gets the coordinate of the point on the 2nd axis.
        
            Returns:
                the y coordinate of the point
        
        
        """
        ...
    def getZ(self) -> float:
        """
            Gets the coordinate of the point on the 3rd axis.
        
            Returns:
                the z coordinate of the point
        
        
        """
        ...
    def isSamePoint(self, lebedevGridPoint: 'LebedevGridPoint', double: float) -> bool:
        """
            Compare to another point.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.analysis.integration.sphere.lebedev.LebedevGridPoint`): point
                absolutePrecision (double): precision
        
            Returns:
                true if same point
        
        
        """
        ...

class LebedevIntegrator:
    """
    public class LebedevIntegrator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Lebedev integrator.
    
        Since:
            4.0
    """
    def __init__(self): ...
    def getEvaluations(self) -> int:
        """
            Return the current number of function evaluations.
        
            Returns:
                the current number of function evaluations
        
        
        """
        ...
    def integrate(self, int: int, lebedevFunction: typing.Union[LebedevFunction, typing.Callable], lebedevGrid: LebedevGrid) -> float:
        """
            Integration.
        
            Parameters:
                maxEval (int): maximum number of evaluations
                f (:class:`~fr.cnes.sirius.patrius.math.analysis.integration.sphere.lebedev.LebedevFunction`): function to integrate
                gridIn (:class:`~fr.cnes.sirius.patrius.math.analysis.integration.sphere.lebedev.LebedevGrid`): grid
        
            Returns:
                integrated function
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.analysis.integration.sphere.lebedev")``.

    LebedevFunction: typing.Type[LebedevFunction]
    LebedevGrid: typing.Type[LebedevGrid]
    LebedevGridPoint: typing.Type[LebedevGridPoint]
    LebedevIntegrator: typing.Type[LebedevIntegrator]
