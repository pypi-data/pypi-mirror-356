import sys
import os

from jpype import JImplements, JOverride

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.patrius.frames import FramesFactory
from fr.cnes.sirius.patrius.math.util import FastMath

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

# Patrius Dataset initialization (needed for example to get the UTC time)
PatriusDataset.addResourcesFromPatriusDataset() 

# GCRF frame
gcrf = FramesFactory.getGCRF()

# Recovery of the UTC time scale using a "factory" (not to duplicate such unique object)
TUC = TimeScalesFactory.getUTC()

# Date of the orbit given in UTC time scale)
date = AbsoluteDate("2010-01-01T12:00:00.000", TUC)

# H0-n : n = 9s and reference longitude = 5 degrees
h0n = FramesFactory.getH0MinusN("Test", date, 9, FastMath.toRadians(5.))

# Printing informaton
print()
print("GCRF name: {}".format(gcrf.getName()))
print("H0-n name: {}".format(h0n.getName()))
