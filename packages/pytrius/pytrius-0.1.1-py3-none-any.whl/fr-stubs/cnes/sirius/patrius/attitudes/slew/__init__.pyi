
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.orbits.pvcoordinates
import fr.cnes.sirius.patrius.time
import java.io
import jpype
import typing



class ConstantSpinSlewComputer(java.io.Serializable):
    """
    public class ConstantSpinSlewComputer extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        Class for constant spin slew computation with angular velocity constraint. Computation of slew returns a
        :class:`~fr.cnes.sirius.patrius.attitudes.ConstantSpinSlew`.
    
        The Constant spin slew is a "simple" slew that computes the attitude of the satellite using a spherical interpolation of
        the quaternions representing the starting and ending attitudes.
    
    
        Like all the other attitude legs, its interval of validity has closed endpoints.
    
        Since:
            4.5
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float): ...
    @typing.overload
    def __init__(self, double: float, string: str): ...
    def compute(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.attitudes.ConstantSpinSlew: ...

class IsisSpinBiasSlewComputer:
    """
    public class IsisSpinBiasSlewComputer extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class for ISIS spin bias slew computation: slew with trapezoidal angular velocity profile calculated in GCRF.
        Computation of slew returns a :class:`~fr.cnes.sirius.patrius.attitudes.TabulatedSlew`.
    
        Since:
            4.5
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double6: float, double7: float, double8: float, doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double10: float, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double6: float, double7: float, double8: float, doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double10: float, int: int, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double6: float, double7: float, double8: float, doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double10: float, int: int, string: str, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double6: float, double7: float, double8: float, doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double10: float, int: int, string: str, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate, boolean: bool): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double6: float, double7: float, double8: float, doubleArray2: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], double10: float, string: str, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate): ...
    def computeAnalytical(self) -> fr.cnes.sirius.patrius.attitudes.TabulatedSlew: ...
    def computeNumerical(self) -> fr.cnes.sirius.patrius.attitudes.TabulatedSlew: ...
    def getDuration(self) -> float:
        """
            Getter for the duration of the slew
        
            Returns:
                the duration of the slew
        
        
        """
        ...

class TwoSpinBiasSlewComputer(java.io.Serializable):
    """
    public class TwoSpinBiasSlewComputer extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
    
        Class for two spin bias slew computation. Computation of slew returns a
        :class:`~fr.cnes.sirius.patrius.attitudes.TabulatedSlew`.
    
        The two spin bias slew computes the attitude of the satellite from initial and final attitude laws, the parameters of
        the two angular velocity fields, plus the time step as well as the stabilization margin.
    
    
        The angular velocity depends on the value of the slew angle.
    
    
        Like all the other attitude legs, its interval of validity has closed endpoints.
    
        Since:
            4.5
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float, double7: float, double8: float, double9: float, string: str): ...
    def compute(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> fr.cnes.sirius.patrius.attitudes.TabulatedSlew: ...
    def computeDuration(self, pVCoordinatesProvider: fr.cnes.sirius.patrius.orbits.pvcoordinates.PVCoordinatesProvider, attitudeProvider: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate: fr.cnes.sirius.patrius.time.AbsoluteDate, attitudeProvider2: fr.cnes.sirius.patrius.attitudes.AttitudeProvider, absoluteDate2: fr.cnes.sirius.patrius.time.AbsoluteDate) -> float: ...
    def computeMaxDuration(self) -> float:
        """
            Estimate the maximum duration of the slew, before computing it.
        
            Returns:
                the estimated maximum duration of the slew.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.attitudes.slew")``.

    ConstantSpinSlewComputer: typing.Type[ConstantSpinSlewComputer]
    IsisSpinBiasSlewComputer: typing.Type[IsisSpinBiasSlewComputer]
    TwoSpinBiasSlewComputer: typing.Type[TwoSpinBiasSlewComputer]
