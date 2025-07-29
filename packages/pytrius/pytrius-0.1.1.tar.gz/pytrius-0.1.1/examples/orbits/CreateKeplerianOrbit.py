import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.patrius.frames import FramesFactory
from fr.cnes.sirius.patrius.orbits import PositionAngle
from fr.cnes.sirius.patrius.orbits import KeplerianOrbit
from fr.cnes.sirius.patrius.math.util import FastMath
from fr.cnes.sirius.patrius.utils import Constants

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

# Patrius Dataset initialization (needed for example to get the UTC time)
PatriusDataset.addResourcesFromPatriusDataset() 

# Recovery of the UTC time scale using a "factory" (not to duplicate such unique object)
TUC = TimeScalesFactory.getUTC()

# Date of the orbit given in UTC time scale)
date = AbsoluteDate("2010-01-01T12:00:00.000", TUC)

# Getting the frame with wich will defined the orbit parameters
# As for time scale, we will use also a "factory".
GCRF = FramesFactory.getGCRF()

# Creation of a keplerian orbit
sma = 7200.e+3
exc = 0.01
inc = FastMath.toRadians(98.)
pa = FastMath.toRadians(0.)
raan = FastMath.toRadians(0.)
anm = FastMath.toRadians(0.)
MU = Constants.WGS84_EARTH_MU
iniOrbit = KeplerianOrbit(sma, exc, inc, pa, raan, anm, PositionAngle.MEAN, GCRF, date, MU)

# Printing the Keplerian period
print()
print(f"Tper = {iniOrbit.getKeplerianPeriod()} s")

# Propagating 100 s with a keplerian motion
dt = 100.
finalOrbit = iniOrbit.shiftedBy(dt)

# Printing date and latitude argument
print()
print(f"Initial true latitude argument = {FastMath.toDegrees(iniOrbit.getLv())} deg")
print(f"New date = {finalOrbit.getDate().toString(TUC)} deg")
print(f"True latitude argument = {FastMath.toDegrees(finalOrbit.getLv())} deg")