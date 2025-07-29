import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.addons.patriusdataset import PatriusDataset


# Patrius Dataset initialization (needed for example to get the UTC time)
PatriusDataset.addResourcesFromPatriusDataset()

# Recovery of the UTC time scale using a "factory" (not to duplicate such unique object)
TUC = TimeScalesFactory.getUTC()

# Date of the orbit (given in UTC time scale)
date = AbsoluteDate("2010-01-01T12:00:00.000", TUC)

# Other way to initialize the absolute date
date_bis = AbsoluteDate(2010, 1, 1, 12, 0, 0., TUC)
print("Comparison between both dates = {} s".format(date_bis.compareTo(date)))

# Printing date in TUC and TAI scale (by default)
print()
print(date.toString(TUC))
print(date.toString())

# Creation of another date by shifting a previous one
other_date = date.shiftedBy(100.)
print()
print(other_date.toString(TUC))

# Gap between two dates
gap = other_date.durationFrom(date)
print()
print("Gap between both dates = {} s".format(gap))
