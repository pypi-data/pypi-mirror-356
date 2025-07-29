import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory


# Patrius Dataset initialization (needed for example to get the UTC time)
PatriusDataset.addResourcesFromPatriusDataset() 

# Recovery of the UTC time scale using a "factory" (not to duplicate such unique object)
TUC = TimeScalesFactory.getUTC()

# Date of the orbit (given in UTC time scale)
date = AbsoluteDate("2010-01-01T12:00:00.000", TUC)

# Printing date in TUC and TAI scale (by default)
print()
print("{}".format(date.toString(TUC)))
print("{}".format(date.toString()))

dateJJ = date.toCNESJulianDate(TUC)        
print()
print("{}".format(dateJJ))

# Other way to initialize the absolute date
dateBis = AbsoluteDate(dateJJ, TUC)
print()
print("Comparison between both dates = {} s".format(dateBis.compareTo(date)))
