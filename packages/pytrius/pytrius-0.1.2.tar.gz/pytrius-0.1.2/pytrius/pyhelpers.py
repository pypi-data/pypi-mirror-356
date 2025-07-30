"""

This document contains classes that are useful for using the patrius
library in Python.

"""

# encoding: utf-8

#   Copyright 2014 SSC
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from datetime import datetime

import math
import numpy as np
import numpy.typing as npt

from jpype.types import JArray, JDouble

from fr.cnes.sirius.patrius.time import TimeScalesFactory, AbsoluteDate
from fr.cnes.sirius.patrius.bodies import CelestialBodyFactory
from fr.cnes.sirius.patrius.frames import FramesFactory
from java.lang.reflect import Modifier
from java.util import Map

def clear_factory_maps(factory_class):
    """
    Clears all static `Map` fields in the given factory class.

    This function iterates through the declared fields of the factory class,
    checks if they are static and of type `Map`, and clears their contents.

    Args:
        factory_class: The class whose static `Map` fields will be cleared.
    """
    for field in factory_class.getDeclaredFields():
        if Modifier.isStatic(field.getModifiers()) and Map.class_.isAssignableFrom(field.getType()):
            field.setAccessible(True)
            field.get(None).clear()

def clear_factories():
    """ Clears the CelestialBodyFactory and the FramesFactory."""
    clear_factory_maps(CelestialBodyFactory.class_)
    CelestialBodyFactory.clearCelestialBodyLoaders()
    clear_factory_maps(FramesFactory.class_)


def absolutedate_to_datetime(patrius_absolutedate: AbsoluteDate) -> datetime:
    """ Converts from patrius.AbsoluteDate objects
    to python datetime objects (utc)"""

    utc = TimeScalesFactory.getUTC()
    or_comp = patrius_absolutedate.getComponents(utc)
    or_date = or_comp.getDate()
    or_time = or_comp.getTime()
    seconds = or_time.getSecond()
    return datetime(or_date.getYear(),
                    or_date.getMonth(),
                    or_date.getDay(),
                    or_time.getHour(),
                    or_time.getMinute(),
                    int(math.floor(seconds)),
                    int(1000000.0 * (seconds - math.floor(seconds))))


def datetime_to_absolutedate(dt_date: datetime) -> AbsoluteDate:
    """ 
    
    Converts from python datetime objects (utc)
    to patrius.AbsoluteDate objects.

    Args:
        dt_date (datetime): python datetime object to convert

    Returns:
        AbsoluteDate: time in patrius format
        
    """

    utc = TimeScalesFactory.getUTC()
    return AbsoluteDate(dt_date.year,
                        dt_date.month,
                        dt_date.day,
                        dt_date.hour,
                        dt_date.minute,
                        dt_date.second + dt_date.microsecond / 1000000.,
                        utc)

def np_to_JArray_double(array: npt.NDArray[np.float64]) -> JArray:
    """
    Converts a N-dimensional numpy array of doubles to a JArray of doubles
    Inspired from
        https://github.com/jpype-project/jpype/
        blob/653ccffd1df46e4d472217d77f592326ae3d3690
        /test/jpypetest/test_buffer.py#L187
    """
    return JArray(JDouble, array.ndim)(array)


def JArray_double2D(array: npt.NDArray[np.float64]) -> JArray:
    """
    This function name is kept for backwards compatibility 
    but it actually just calls np_to_JArray_double
    """
    return np_to_JArray_double(array=array)


def JArray_double1D(array: npt.NDArray[np.float64]) -> JArray:
    """
    This function just calls np_to_JArray_double to convert a 1D numpy array to a JArray
    """
    return np_to_JArray_double(array=array)
