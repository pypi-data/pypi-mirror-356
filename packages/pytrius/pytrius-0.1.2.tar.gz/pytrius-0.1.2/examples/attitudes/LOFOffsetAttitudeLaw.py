import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

from fr.cnes.sirius.patrius.attitudes import LofOffset
from fr.cnes.sirius.patrius.frames import LOFType
from fr.cnes.sirius.patrius.frames import FramesFactory
from fr.cnes.sirius.patrius.math.geometry.euclidean.threed import RotationOrder, Vector3D
from fr.cnes.sirius.patrius.math.util import FastMath
from fr.cnes.sirius.patrius.orbits import KeplerianOrbit, PositionAngle
from fr.cnes.sirius.patrius.orbits.orbitalparameters import KeplerianParameters
from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.patrius.utils import Constants

PatriusDataset.addResourcesFromPatriusDataset() 
  
# Recovery of the UTC time scale using a "factory" (not to duplicate such unique object)
TUC = TimeScalesFactory.getUTC()

# Date of the orbit given in UTC time scale)
date = AbsoluteDate("2010-01-01T12:00:00.000", TUC)

# Getting the with wich will defined the orbit parameters
# As for time scale, we will use also a "factory".
GCRF = FramesFactory.getGCRF()

# Initial orbit
sma = 7200.e+3
exc = 0.01
inc = FastMath.toRadians(98.)
pa = FastMath.toRadians(0.)
raan = FastMath.toRadians(0.)
anm = FastMath.toRadians(0.)
MU = Constants.WGS84_EARTH_MU

par = KeplerianParameters(sma, exc, inc, pa, raan, anm, PositionAngle.MEAN, MU)
iniOrbit = KeplerianOrbit(par, GCRF, date)

# Building a first law
attitudeLaw0= LofOffset(LOFType.TNW)
att0 = attitudeLaw0.getAttitude(iniOrbit)

# Building a second law with a 45 deg rotation on Z axis
psi  = FastMath.toRadians(45.)
teta = 0.
phi  = 0.
attitudeLaw = LofOffset(LOFType.TNW, RotationOrder.ZYX, psi, teta, phi)
att = attitudeLaw.getAttitude(iniOrbit)

# Rotation of the X axis
vec0 = att0.getRotation().applyTo(Vector3D.PLUS_I)
vec  = att.getRotation().applyTo(Vector3D.PLUS_I)
cos = vec.dotProduct(vec0)
ang = FastMath.acos(cos)
print("{} deg".format(FastMath.toDegrees(ang)))


# Rotation of the Y axis
vec0 = att0.getRotation().applyTo(Vector3D.PLUS_J)
vec  = att.getRotation().applyTo(Vector3D.PLUS_J)
cos = vec.dotProduct(vec0)
ang = FastMath.acos(cos)
print("{} deg".format(FastMath.toDegrees(ang)))

# Z axis comparison
vec0 = att0.getRotation().applyTo(Vector3D.PLUS_K)
vec  = att.getRotation().applyTo(Vector3D.PLUS_K)
dVec = vec.subtract(vec0)
norm = dVec.getNorm()
print(norm)