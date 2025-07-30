
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.math.analysis.polynomials
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.time
import java.io
import jpype
import typing



class AbstractDateIntervalFunction(fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction):
    @typing.overload
    def __init__(self, abstractDateIntervalFunction: 'AbstractDateIntervalFunction'): ...
    @typing.overload
    def __init__(self, absoluteDateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.time.AbsoluteDate], jpype.JArray]): ...
    def getDateIntervals(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.time.AbsoluteDate]: ...

class Analytical2DOrbitModel(java.io.Serializable, fr.cnes.sirius.patrius.propagation.MeanOsculatingElementsProvider):
    """
    public class Analytical2DOrbitModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`, :class:`~fr.cnes.sirius.patrius.propagation.MeanOsculatingElementsProvider`
    
        This class represents an analytical 2D orbit model, it is made of 6 parameter models, one per adapted circular
        parameter.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.analytical.twod.Analytical2DParameterModel`,
            :class:`~fr.cnes.sirius.patrius.propagation.analytical.twod.Analytical2DPropagator`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, analytical2DParameterModel: 'Analytical2DParameterModel', analytical2DParameterModel2: 'Analytical2DParameterModel', analytical2DParameterModel3: 'Analytical2DParameterModel', analytical2DParameterModel4: 'Analytical2DParameterModel', analytical2DParameterModel5: 'Analytical2DParameterModel', analytical2DParameterModel6: 'Analytical2DParameterModel', double: float): ...
    @typing.overload
    def __init__(self, analytical2DParameterModel: 'Analytical2DParameterModel', analytical2DParameterModel2: 'Analytical2DParameterModel', analytical2DParameterModel3: 'Analytical2DParameterModel', analytical2DParameterModel4: 'Analytical2DParameterModel', analytical2DParameterModel5: 'Analytical2DParameterModel', analytical2DParameterModel6: 'Analytical2DParameterModel', massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, double: float): ...
    @typing.overload
    def __init__(self, analytical2DParameterModel: 'Analytical2DParameterModel', analytical2DParameterModel2: 'Analytical2DParameterModel', analytical2DParameterModel3: 'Analytical2DParameterModel', analytical2DParameterModel4: 'Analytical2DParameterModel', analytical2DParameterModel5: 'Analytical2DParameterModel', analytical2DParameterModel6: 'Analytical2DParameterModel', intArray: typing.Union[typing.List[int], jpype.JArray], double: float): ...
    @typing.overload
    def __init__(self, analytical2DParameterModel: 'Analytical2DParameterModel', analytical2DParameterModel2: 'Analytical2DParameterModel', analytical2DParameterModel3: 'Analytical2DParameterModel', analytical2DParameterModel4: 'Analytical2DParameterModel', analytical2DParameterModel5: 'Analytical2DParameterModel', analytical2DParameterModel6: 'Analytical2DParameterModel', intArray: typing.Union[typing.List[int], jpype.JArray], massProvider: fr.cnes.sirius.patrius.propagation.MassProvider, double: float): ...
    def getAolModel(self) -> 'Analytical2DParameterModel':
        """
            Get the argument of latitude parameter model.
        
            Returns:
                the parameter model
        
        
        """
        ...
    def getDevelopmentOrders(self) -> typing.MutableSequence[int]:
        """
            Return the array with models trigonometric orders. These orders are ordered as per : [a, ex, ey, i, lna, alpha].
        
            Returns:
                array with models trigonometric orders
        
        
        """
        ...
    def getExModel(self) -> 'Analytical2DParameterModel':
        """
            Get the x eccentricity component parameter model.
        
            Returns:
                the parameter model
        
        
        """
        ...
    def getEyModel(self) -> 'Analytical2DParameterModel':
        """
            Get the y eccentricity component parameter model.
        
            Returns:
                the parameter model
        
        
        """
        ...
    def getIncModel(self) -> 'Analytical2DParameterModel':
        """
            Get the inclination parameter model.
        
            Returns:
                the parameter model
        
        
        """
        ...
    def getLnaModel(self) -> 'Analytical2DParameterModel':
        """
            Get the longitude of ascending node parameter model.
        
            Returns:
                the parameter model
        
        
        """
        ...
    def getMassModel(self) -> fr.cnes.sirius.patrius.propagation.MassProvider:
        """
            Returns the spacecraft mass model.
        
            Returns:
                the mass model
        
        
        """
        ...
    def getMaxOrders(self) -> typing.MutableSequence[int]:
        """
            Return the array with the highest trigonometric orders available. These orders are ordered as per : [a, ex, ey, i, lna,
            alpha].
        
            Returns:
                array with highest orders
        
        
        """
        ...
    def getMu(self) -> float:
        """
            Returns the standard gravitational parameter.
        
            Returns:
                mu
        
        
        """
        ...
    def getParameterModels(self) -> typing.MutableSequence['Analytical2DParameterModel']:
        """
            Get the array of parameter models.
        
            Returns:
                [sma, ex, ey, inc, lna, aol]
        
        
        """
        ...
    def getSmaModel(self) -> 'Analytical2DParameterModel':
        """
            Get the semi major axis parameter model.
        
            Returns:
                the parameter model
        
        
        """
        ...
    def mean2osc(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def osc2mean(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def propagateMeanOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    @typing.overload
    def propagateModel(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> typing.MutableSequence[float]: ...
    @typing.overload
    def propagateModel(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, intArray: typing.Union[typing.List[int], jpype.JArray]) -> typing.MutableSequence[float]: ...
    def setThreshold(self, double: float) -> None:
        """
            Setter for relative convergence threshold for osculating to mean conversion used by method
            :meth:`~fr.cnes.sirius.patrius.propagation.analytical.twod.Analytical2DOrbitModel.osc2mean`.
        
            Parameters:
                newThreshold (double): new relative threshold
        
        
        """
        ...

class Analytical2DParameterModel(java.io.Serializable):
    """
    public class Analytical2DParameterModel extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class represents an analytical 2D orbital parameter model. The adapted circular parameter represented by this model
        is decomposed into a linear and a trigonometric part.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.analytical.twod.Analytical2DOrbitModel`,
            :class:`~fr.cnes.sirius.patrius.propagation.analytical.twod.Analytical2DPropagator`, :meth:`~serialized`
    """
    def __init__(self, univariateDateFunction: typing.Union[fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction, typing.Callable], doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    def getCenteredModel(self) -> fr.cnes.sirius.patrius.math.analysis.polynomials.UnivariateDateFunction:
        """
            Get model for centered part of analytical model.
        
            Returns:
                model for centered part of analytical model
        
        
        """
        ...
    def getCenteredValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float:
        """
            Get the centered value of the model.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): a date
        
            Returns:
                centered value of the model
        
        
        """
        ...
    def getMaxTrigonometricOrder(self) -> int:
        """
            Return the highest trigonometric order.
        
            Returns:
                highest trigonometric order
        
        
        """
        ...
    def getOneHarmonicValue(self, double: float, double2: float, int: int) -> float:
        """
            Get the value of the nth trigonometric contribution.
        
            Parameters:
                pso (double): centered value of mean aol
                lna (double): centered value of the longitude of ascending node
                order (int): order of the development
        
            Returns:
                the value of the nth harmonic contribution
        
        
        """
        ...
    def getTrigonometricCoefficients(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Returns the trigonometric coefficients array.
        
            Returns:
                the trigonometric coefficients array
        
        
        """
        ...
    @typing.overload
    def getTrigonometricValue(self, double: float, double2: float) -> float:
        """
            Get the value of the trigonometric contribution with maximum order.
        
            Parameters:
                pso (double): centered latitude argument
                lna (double): longitude of ascending node
        
            Returns:
                the value of the trigonometric contribution
        
            Get the value of the trigonometric contribution up to provided order.
        
            Parameters:
                pso (double): centered latitude argument
                lna (double): longitude of ascending node
                order (int): trigonometric order of the development
        
            Returns:
                the value of the trigonometric contribution
        
        
        """
        ...
    @typing.overload
    def getTrigonometricValue(self, double: float, double2: float, int: int) -> float: ...
    @typing.overload
    def getValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float) -> float:
        """
            Get the value of the model at provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
                pso (double): centered latitude argument
                lna (double): longitude of ascending node
        
            Returns:
                the value of the model at provided date
        
            Get the value of the model at provided date.
        
            Parameters:
                date (:class:`~fr.cnes.sirius.patrius.time.AbsoluteDate`): date
                pso (double): centered latitude argument
                lna (double): longitude of ascending node
                order (int): order of the trigonometric development
        
            Returns:
                the value of the model at provided date
        
        
        """
        ...
    @typing.overload
    def getValue(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, double: float, double2: float, int: int) -> float: ...

class Analytical2DPropagator(fr.cnes.sirius.patrius.propagation.AbstractPropagator, fr.cnes.sirius.patrius.propagation.MeanOsculatingElementsProvider):
    """
    public class Analytical2DPropagator extends :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator` implements :class:`~fr.cnes.sirius.patrius.propagation.MeanOsculatingElementsProvider`
    
        This class propagates an analytical 2D orbit model and extends the
        :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator` class. Thus, this propagator can handle events and all
        functionalities of the :class:`~fr.cnes.sirius.patrius.propagation.AbstractPropagator`.
    
        Since:
            1.3
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.propagation.analytical.twod.Analytical2DOrbitModel`,
            :class:`~fr.cnes.sirius.patrius.propagation.analytical.twod.Analytical2DParameterModel`, :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, analytical2DOrbitModel: Analytical2DOrbitModel, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, analytical2DOrbitModel: Analytical2DOrbitModel, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, intArray: typing.Union[typing.List[int], jpype.JArray]): ...
    @typing.overload
    def __init__(self, analytical2DOrbitModel: Analytical2DOrbitModel, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, analytical2DOrbitModel: Analytical2DOrbitModel, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, intArray: typing.Union[typing.List[int], jpype.JArray]): ...
    def mean2osc(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def osc2mean(self, orbit: fr.cnes.sirius.patrius.orbits.Orbit) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def propagateMeanOrbit(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.orbits.Orbit: ...
    def setThreshold(self, double: float) -> None:
        """
            Setter for relative convergence threshold for osculating to mean conversion used by method
            :meth:`~fr.cnes.sirius.patrius.propagation.analytical.twod.Analytical2DPropagator.osc2mean`.
        
            Parameters:
                newThreshold (double): new relative threshold
        
        
        """
        ...

class DateIntervalLinearFunction(AbstractDateIntervalFunction):
    @typing.overload
    def __init__(self, double: float, absoluteDateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.time.AbsoluteDate], jpype.JArray], doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, dateIntervalLinearFunction: 'DateIntervalLinearFunction'): ...
    def getX0(self) -> float: ...
    def getxDotIntervals(self) -> typing.MutableSequence[float]: ...
    def value(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...

class DateIntervalParabolicFunction(AbstractDateIntervalFunction):
    @typing.overload
    def __init__(self, double: float, double2: float, absoluteDateArray: typing.Union[typing.List[fr.cnes.sirius.patrius.time.AbsoluteDate], jpype.JArray], doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, dateIntervalParabolicFunction: 'DateIntervalParabolicFunction'): ...
    def getX0(self) -> float: ...
    def getxDot0(self) -> float: ...
    def getxDotDotIntervals(self) -> typing.MutableSequence[float]: ...
    def value(self, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.propagation.analytical.twod")``.

    AbstractDateIntervalFunction: typing.Type[AbstractDateIntervalFunction]
    Analytical2DOrbitModel: typing.Type[Analytical2DOrbitModel]
    Analytical2DParameterModel: typing.Type[Analytical2DParameterModel]
    Analytical2DPropagator: typing.Type[Analytical2DPropagator]
    DateIntervalLinearFunction: typing.Type[DateIntervalLinearFunction]
    DateIntervalParabolicFunction: typing.Type[DateIntervalParabolicFunction]
