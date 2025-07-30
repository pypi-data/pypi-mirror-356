
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import jpype
import typing



class ApCoef:
    """
    public class ApCoef extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        /** Class Ap_coef Array containing the following magnetic values: 0 : daily AP 1 : 3 hr AP index for current time 2 : 3
        hr AP index for 3 hrs before current time 3 : 3 hr AP index for 6 hrs before current time 4 : 3 hr AP index for 9 hrs
        before current time 5 : Average of eight 3 hr AP indicies from 12 to 33 hrs prior to current time 6 : Average of eight 3
        hr AP indicies from 36 to 57 hrs prior to current time
    
        Since:
            1.2
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    def getAp(self) -> typing.MutableSequence[float]:
        """
            Getter for AP.
        
            Returns:
                the ap
        
        
        """
        ...
    @typing.overload
    def setAp(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Setter for AP.
        
            Parameters:
                ap (double[]): the ap to set
        
            Setter for a specific element of the AP array.
        
            Parameters:
                position (int): position in the array.
                value (int): new value.
        
        
        """
        ...
    @typing.overload
    def setAp(self, int: int, int2: int) -> None: ...

class Flags(java.io.Serializable):
    """
    public class Flags extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class Flags Switches: to turn on and off particular variations use these switches. 0 is off, 1 is on, and 2 is main
        effects off but cross terms on. Standard values are 0 for switch 0 and 1 for switches 1 to 23. The array "switches"
        needs to be set accordingly by the calling program. The arrays sw and swc are set internally. switches[i]: i -
        explanation ----------------- 0 - output in centimeters instead of meters 1 - F10.7 effect on mean 2 - time independent
        3 - symmetrical annual 4 - symmetrical semiannual 5 - asymmetrical annual 6 - asymmetrical semiannual 7 - diurnal 8 -
        semidiurnal 9 - daily ap [when this is set to -1 (!) the pointer ap_a in struct nrlmsise_input must point to a struct
        ap_array] 10 - all UT/long effects 11 - longitudinal 12 - UT and mixed UT/long 13 - mixed AP/UT/LONG 14 - terdiurnal 15
        - departures from diffusive equilibrium 16 - all TINF var 17 - all TLB var 18 - all TN1 var 19 - all S var 20 - all TN2
        var 21 - all NLB var 22 - all TN3 var 23 - turbo scale height var
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def bool(self, double: float) -> bool:
        """
            Return boolean from double.
        
            Parameters:
                fakeBool (double): double
        
            Returns:
                boolean from double
        
            Since:
                1.0
        
        
        """
        ...
    def getSw(self, int: int) -> float:
        """
            Getter for a particular element in the sw array.
        
            Parameters:
                position (int): position in the array
        
            Returns:
                the element at the given position
        
        
        """
        ...
    def getSwc(self, int: int) -> float:
        """
            Getter for a particular element in the swc array.
        
            Parameters:
                position (int): position in the array
        
            Returns:
                the element at the given position
        
        
        """
        ...
    def getSwitches(self) -> typing.MutableSequence[int]:
        """
            Getter for switches.
        
            Returns:
                the switches
        
        
        """
        ...
    @typing.overload
    def setSwitches(self, int: int, int2: int) -> None:
        """
            Setter for a specific element of the switches array.
        
            Parameters:
                position (int): position in the array
                value (int): new value.
        
        """
        ...
    @typing.overload
    def setSwitches(self, intArray: typing.Union[typing.List[int], jpype.JArray]) -> None:
        """
            Setter for switches.
        
            Parameters:
                switches (int[]): the switches to set
        
        
        """
        ...
    def tselec(self) -> None:
        """
            Prepare sw and swc.
        
        """
        ...

class Input:
    """
    public class Input extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class Input NOTES ON INPUT VARIABLES: UT, Local Time, and Longitude are used independently in the model and are not of
        equal importance for every situation. For the most physically realistic calculation these three variables should be
        consistent (lst=sec/3600 + g_long/15). The Equation of Time departures from the above formula for apparent local time
        can be included if available but are of minor importance. f107 and f107A values used to generate the model correspond to
        the 10.7 cm radio flux at the actual distance of the Earth from the Sun rather than the radio flux at 1 AU. The
        following site provides both classes of values: ftp://ftp.ngdc.noaa.gov/STP/SOLAR_DATA/SOLAR_RADIO/FLUX/ f107, f107A,
        and ap effects are neither large nor well established below 80 km and these parameters should be set to 150., 150., and
        4. respectively.
    
        Since:
            1.2
    """
    def __init__(self): ...
    def getAlt(self) -> float:
        """
            Getter for alt.
        
            Returns:
                the alt
        
        
        """
        ...
    def getAp(self) -> float:
        """
            Getter for ap.
        
            Returns:
                the ap
        
        
        """
        ...
    def getApA(self) -> ApCoef:
        """
            Getter for apA.
        
            Returns:
                the apA
        
        
        """
        ...
    def getDoy(self) -> int:
        """
            Getter for doy.
        
            Returns:
                the doy
        
        
        """
        ...
    def getF107(self) -> float:
        """
            Getter for f107.
        
            Returns:
                the f107
        
        
        """
        ...
    def getF107A(self) -> float:
        """
            Getter for f107A.
        
            Returns:
                the f107A
        
        
        """
        ...
    def getLst(self) -> float:
        """
            Getter for lst.
        
            Returns:
                the lst
        
        
        """
        ...
    def getSec(self) -> float:
        """
            Getter for sec.
        
            Returns:
                the sec
        
        
        """
        ...
    def getgLat(self) -> float:
        """
            Getter for gLat.
        
            Returns:
                the gLat
        
        
        """
        ...
    def getgLong(self) -> float:
        """
            Getter for gLong.
        
            Returns:
                the gLong
        
        
        """
        ...
    def setAlt(self, double: float) -> None:
        """
            Setter for alt.
        
            Parameters:
                alt (double): the alt to set
        
        
        """
        ...
    def setAp(self, double: float) -> None:
        """
            Setter for ap.
        
            Parameters:
                ap (double): the ap to set
        
        
        """
        ...
    @typing.overload
    def setApA(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None:
        """
            Setter for apA.
        
            Parameters:
                apA (:class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSIS2000.ApCoef`): the apA to set
        
            Setter for apA.
        
            Parameters:
                apA (double[]): geomagnetic coefficients.
        
        
        """
        ...
    @typing.overload
    def setApA(self, apCoef: ApCoef) -> None: ...
    def setDoy(self, int: int) -> None:
        """
            Setter for doy.
        
            Parameters:
                doy (int): the doy to set
        
        
        """
        ...
    def setF107(self, double: float) -> None:
        """
            Setter for f107.
        
            Parameters:
                f107 (double): the f107 to set
        
        
        """
        ...
    def setF107A(self, double: float) -> None:
        """
            Setter for f107A.
        
            Parameters:
                f107a (double): the f107A to set
        
        
        """
        ...
    def setLst(self, double: float) -> None:
        """
            Setter for lst.
        
            Parameters:
                lst (double): the lst to set
        
        
        """
        ...
    def setSec(self, double: float) -> None:
        """
            Setter for doy.
        
            Parameters:
                sec (double): the sec to set
        
        
        """
        ...
    def setgLat(self, double: float) -> None:
        """
            Setter for gLat.
        
            Parameters:
                gLat (double): the gLat to set
        
        
        """
        ...
    def setgLong(self, double: float) -> None:
        """
            Setter for gLong.
        
            Parameters:
                gLong (double): the gLong to set
        
        
        """
        ...

class NRLMSISE00(java.io.Serializable):
    """
    public final class NRLMSISE00 extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        NRLMSISE-00 atmospheric model.
    
    
        Methods of this class are adapted from the C source code of the NRLMSISE-00 model developed by Mike Picone, Alan Hedin,
        and Doug Drob, and implemented by Dominik Brodowski. The NRLMSISE-00 model was developed by Mike Picone, Alan Hedin, and
        Doug Drob. They also wrote a NRLMSISE-00 distribution package in FORTRAN which is available at
        http://uap-www.nrl.navy.mil/models_web/msis/msis_home.htm Dominik Brodowski implemented and maintains this C version.
        You can reach him at mail@brodo.de. See the file "DOCUMENTATION" for details, and check
        http://www.brodo.de/english/pub/nrlmsise/index.html for updated releases of this package.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def gtd7d(self, input: Input, flags: Flags, output: 'Output') -> None:
        """
            gtd7d.
        
        
            This subroutine provides Effective Total Mass Density for output d[5] which includes contributions from "anomalous
            oxygen" which can affect satellite drag above 500 km. See the section "output" for additional details.
        
            Parameters:
                input (:class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSIS2000.Input`): input
                flags (:class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSIS2000.Flags`): flags
                output (:class:`~fr.cnes.sirius.patrius.forces.atmospheres.MSIS2000.Output`): output
        
        
        """
        ...

class NRLMSISE00Data:
    """
    public final class NRLMSISE00Data extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        NRLMSIS00 data class
    
        Since:
            1.2
    """
    ...

class Output(java.io.Serializable):
    """
    public final class Output extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Class Output OUTPUT VARIABLES: d[0] - HE NUMBER DENSITY(CM-3) d[1] - O NUMBER DENSITY(CM-3) d[2] - N2 NUMBER
        DENSITY(CM-3) d[3] - O2 NUMBER DENSITY(CM-3) d[4] - AR NUMBER DENSITY(CM-3) d[5] - TOTAL MASS DENSITY(GM/CM3) [includes
        d[8] in td7d] d[6] - H NUMBER DENSITY(CM-3) d[7] - N NUMBER DENSITY(CM-3) d[8] - Anomalous oxygen NUMBER DENSITY(CM-3)
        t[0] - EXOSPHERIC TEMPERATURE t[1] - TEMPERATURE AT ALT O, H, and N are set to zero below 72.5 km t[0], Exospheric
        temperature, is set to global average for altitudes below 120 km. The 120 km gradient is left at global average value
        for altitudes below 72 km. d[5], TOTAL MASS DENSITY, is NOT the same for subroutines GTD7 and GTD7D SUBROUTINE GTD7 --
        d[5] is the sum of the mass densities of the species labeled by indices 0-4 and 6-7 in output variable d. This includes
        He, O, N2, O2, Ar, H, and N but does NOT include anomalous oxygen (species index 8). SUBROUTINE GTD7D -- d[5] is the
        "effective total mass density for drag" and is the sum of the mass densities of all species in this model, INCLUDING
        anomalous oxygen.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def getD(self, int: int) -> float:
        """
            Getter for density component.
        
            Parameters:
                i (int): index
        
            Returns:
                the ith density component
        
        
        """
        ...
    @typing.overload
    def getD(self) -> typing.MutableSequence[float]:
        """
            Getter for density (d).
        
            Returns:
                the d
        
        """
        ...
    @typing.overload
    def getT(self, int: int) -> float:
        """
            Getter for temperature component.
        
            Parameters:
                i (int): index
        
            Returns:
                the ith temperature component
        
        
        """
        ...
    @typing.overload
    def getT(self) -> typing.MutableSequence[float]:
        """
            Getter for temperature (t).
        
            Returns:
                the t
        
        """
        ...
    def setD(self, int: int, double: float) -> None:
        """
            Setter for ith density component.
        
            Parameters:
                i (int): index
                value (double): value to set
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.forces.atmospheres.MSIS2000")``.

    ApCoef: typing.Type[ApCoef]
    Flags: typing.Type[Flags]
    Input: typing.Type[Input]
    NRLMSISE00: typing.Type[NRLMSISE00]
    NRLMSISE00Data: typing.Type[NRLMSISE00Data]
    Output: typing.Type[Output]
