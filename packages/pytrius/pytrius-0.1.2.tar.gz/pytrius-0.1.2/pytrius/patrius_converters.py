"""
This file contains a number of tweaks in order to tune Patrius with jpype according to preferences.

It is assumed that the JVM is running.
Importing this file will automatically implement the changes.

"""

import datetime
import pytrius

from jpype._jcustomizer import JImplementationFor, JConversion
import _jpype

from jpype.types import JArray, JDouble

import os
dirpath = os.path.dirname(os.path.abspath(__file__))

from pytrius.pyhelpers import absolutedate_to_datetime, datetime_to_absolutedate

import numpy as np

# Change representation of object (__repr__) to include toString()
def _JObjectRepr(obj) -> str:
    """

    Function to generate the __repr__ string for objects in interactive mode

    """
    return f"<{obj.getClass().getSimpleName()}: {obj.toString()}>"


# Monkey patch the base class
_jpype._JObject.__repr__ = _JObjectRepr

# Create a top level function JArray_double to mimic JCC backend
pytrius.JArray_double = JArray(JDouble)


# Some helper methods on selected classes
@JImplementationFor("fr.cnes.sirius.patrius.time.AbsoluteDate")
class _JAbsoluteDate(object):
    """

    Decorator to define an implementation for the JAbsoluteDate class.

    """

    def to_datetime(self) -> datetime.datetime:
        """

        Returns: The AbsoluteDate as a Python datetime

        """
        return absolutedate_to_datetime(self)

    @JImplementationFor("double[][]")
    class _JDouble2DArray(object):
        """

        Decorator to define an implementation for the J2DArray class.

        """

        def to_numpy(self) -> np.ndarray:
            """
            Get the Java Double 2D Array as a Python numpy array

            Returns: the Double Array as numpy 2D array

            """
            return np.array(self)

        def __repr__(self):
            np_2darray_prettier = str(self.to_numpy()).replace('\n', ',')
            return f"<{self.getClass().getSimpleName()}: {np_2darray_prettier}>"

    @JImplementationFor("double[]")
    class _JDoubleArray(object):
        """
        
        Decorator to define an implementation for the JDoubleArray class.

        """
        def to_numpy(self):
            """

            Get the Java Double Array as a Python numpy array
            Returns: the Double Array as numpy array

            """
            return np.array(self)

        def __repr__(self):
            return f"<{self.getClass().getSimpleName()}: {self.to_numpy()}>"


# Conversions
@JConversion("fr.cnes.sirius.patrius.time.AbsoluteDate", instanceof=datetime.datetime)
def _JADConversion(jcls, obj: datetime):
    """
        
    Converts a Python datetime object to the Java AbsoluteDate type.
    
    Args:
        obj: The Python datetime object to convert.

    Returns:
        The corresponding Java AbsoluteDate object.

    """
    return datetime_to_absolutedate(obj)
