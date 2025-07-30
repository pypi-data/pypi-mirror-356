import sys
import os
import unittest
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytrius
pytrius.initVM()

from pytrius.pyhelpers import JArray_double2D, clear_factories

from fr.cnes.sirius.patrius.time import TimeScalesFactory
from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

class TestPyHelpers(unittest.TestCase):

    def check_addResourcesFromPatriusDataset_valid():
        
        utc = TimeScalesFactory.getUTC()
        last_leap_second = utc.getLastKnownLeapSecond()

        return last_leap_second.getComponents(utc).getDate().getYear() >= 2016

    def test_setup_patrius_data_from_PatriusDataset(self):

        PatriusDataset.addResourcesFromPatriusDataset()
        assert TestPyHelpers.check_addResourcesFromPatriusDataset_valid()

        clear_factories()

    def test_JArray_double2D(self):
        np_array_expected = np.array([[5.0, 6.0],
                                    [7.0, 8.0]])
        jarray_2d = JArray_double2D(np_array_expected)
        np_array_actual = np.array(jarray_2d)
        assert np.all(np_array_expected == np_array_actual)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPyHelpers)
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
