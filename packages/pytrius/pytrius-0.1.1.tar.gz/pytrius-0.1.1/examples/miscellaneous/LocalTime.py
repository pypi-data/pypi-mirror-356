import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

from fr.cnes.sirius.patrius.bodies import MeeusSun
from fr.cnes.sirius.patrius.frames import FramesFactory
from fr.cnes.sirius.patrius.math.util import FastMath
from fr.cnes.sirius.patrius.orbits import ApsisOrbit, PositionAngle
from fr.cnes.sirius.patrius.orbits.orbitalparameters import ApsisRadiusParameters
from fr.cnes.sirius.patrius.time import AbsoluteDate, LocalTimeAngle, TimeScalesFactory
from fr.cnes.sirius.patrius.utils import Constants



# Patrius Dataset initialization (needed for example to get the UTC time
PatriusDataset.addResourcesFromPatriusDataset() 

# Recovery of the UTC time scale using a "factory" (not to duplicate such unique object)
TUC = TimeScalesFactory.getUTC()

# Date of the orbit given in UTC time scale)
date = AbsoluteDate("2000-06-21T12:00:00.000", TUC)

# Getting the frame with wich will defined the orbit parameters
# As for time scale, we will use also a "factory".
CIRF = FramesFactory.getCIRF()

# Initial orbit
sma = 7200.e+3
exc = 0.01
per = sma*(1.-exc)
apo = sma*(1.+exc)
inc = FastMath.toRadians(98.)
pa = FastMath.toRadians(0.)
raan = FastMath.toRadians(90.)
anm = FastMath.toRadians(0.)
MU = Constants.WGS84_EARTH_MU

par = ApsisRadiusParameters(per, apo, inc, pa, raan, anm, PositionAngle.MEAN, MU)
iniOrbit = ApsisOrbit(par, CIRF, date)

# Sun ephemeris
sunEphemeris = MeeusSun()

# Local times
localTime = LocalTimeAngle(sunEphemeris)

tlt = localTime.computeTrueLocalTimeAngle(iniOrbit)
mlt = localTime.computeMeanLocalTimeAngle(iniOrbit)

def angle_to_hour(angle: float) -> float:
    """
    Method to transform local time given as an angle to local time in hours.

    :param angle: local time as an angle (radians)
    :return: local time in hours
    """
    hour = 12.0 + angle * 12.0 / FastMath.PI
    return hour

print("TLT = {} h ({} deg)".format(angle_to_hour(tlt), FastMath.toDegrees(tlt)))
print("MLT = {} h ({} deg)".format(angle_to_hour(mlt), FastMath.toDegrees(mlt)))
