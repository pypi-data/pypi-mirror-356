import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytrius
pytrius.initVM()

from pytrius.pyhelpers import JArray_double2D, absolutedate_to_datetime, JArray_double1D

from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
import numpy as np
from datetime import datetime

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

PatriusDataset.addResourcesFromPatriusDataset()

class TestPatriusConverters(unittest.TestCase):

    def test_absolute_date_to_datetime_converter(self):
        abs_date = AbsoluteDate(2020, 2, 15, 19, 57, 42.698723, TimeScalesFactory.getUTC())
        py_datetime = absolutedate_to_datetime(abs_date)
        assert abs_date.to_datetime() == py_datetime

    def test_JConversion_datetime_to_absolute_date(self):
        py_datetime_expected = datetime(2020, 2, 15, 19, 57, 42, 698723)
        abs_date = AbsoluteDate(py_datetime_expected, 0.0) # This implicitly calls the _JADConversion function in patrius_converters.py
        py_datetime_actual = absolutedate_to_datetime(abs_date)
        assert py_datetime_actual == py_datetime_expected

    def test_repr(self):
        utc_timescale = TimeScalesFactory.getUTC()
        assert utc_timescale.__repr__() == "<UTCScale: UTC>"

    def test_2darray_converter(self):
        np_array_expected = np.array([[5.0, 6.0],
                                    [7.0, 8.0]])
        jarray_2d = JArray_double2D(np_array_expected)

        np_array_actual = jarray_2d.to_numpy()
        assert np.all(np_array_actual == np_array_expected)

    def test_2darray_repr(self):
        np_array_expected = np.array([[5.0, 6.0],
                                    [7.0, 8.0]])
        jarray_2d = JArray_double2D(np_array_expected)
        assert jarray_2d.__repr__() == "<double[][]: [[5. 6.], [7. 8.]]>"

    def test_1darray_converter(self):
        np_array_expected = np.array([1.0, 2.0, 3.0])
        jarray = JArray_double1D(np_array_expected)
        np_array_actual = jarray.to_numpy()
        assert np.all(np_array_actual == np_array_expected)

    def test_1darray_repr(self):
        np_array_expected = np.array([1.0, 2.0, 3.0])
        jarray = JArray_double1D(np_array_expected)
        assert jarray.__repr__() == "<double[]: [1. 2. 3.]>"

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPatriusConverters)
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
