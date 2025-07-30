import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

from fr.cnes.sirius.patrius.attitudes.directions import CelestialBodyPolesAxisDirection
from fr.cnes.sirius.patrius.attitudes import TwoDirectionAttitudeLaw
from fr.cnes.sirius.patrius.bodies import MeeusSun
from fr.cnes.sirius.patrius.frames import FramesFactory
from fr.cnes.sirius.patrius.attitudes.directions import GenericTargetDirection
from fr.cnes.sirius.patrius.math.geometry.euclidean.threed import Rotation, RotationOrder, Vector3D
from fr.cnes.sirius.patrius.math.util import FastMath
from fr.cnes.sirius.patrius.orbits import KeplerianOrbit, PositionAngle
from fr.cnes.sirius.patrius.orbits.orbitalparameters import KeplerianParameters
from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.patrius.utils import Constants

# Patrius Dataset initialization (needed for example to get the UTC time
PatriusDataset.addResourcesFromPatriusDataset() 

# Recovery of the UTC time scale using a "factory" (not to duplicate such unique object)
TUC = TimeScalesFactory.getUTC()

# Date of the given in UTC time scale)
date = AbsoluteDate("2010-01-01T12:00:00.000", TUC)

# Getting the with wich will defined the parameters
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

# Using the Meeus model for the Sun.
sun = MeeusSun()

# Sun directions
dirSun = GenericTargetDirection(sun)
dirPole = CelestialBodyPolesAxisDirection(sun)

# Building an law
firstAxis = Vector3D(1., 0., 0.)
secondAxis = Vector3D(0., 1., 0.)
attitudeLaw = TwoDirectionAttitudeLaw(dirSun, dirPole, firstAxis, secondAxis)
att = attitudeLaw.getAttitude(iniOrbit)

# Printing attitude
psi  = att.getRotation().getAngles(RotationOrder.ZYX)[0]
teta = att.getRotation().getAngles(RotationOrder.ZYX)[1]

print("Psi  / GCRF  = {} deg".format(FastMath.toDegrees(psi)))
print("Teta / GCRF = {} deg".format(FastMath.toDegrees(teta)))

# Coordinates of the Sun vs GCRF at the same date
pv = sun.getPVCoordinates(date, GCRF)
sunPos = pv.getPosition()

# Direction of the Sun from the cdg of the satellite
satPos = iniOrbit.getPVCoordinates(GCRF).getPosition()
sunDir = Rotation(Vector3D.PLUS_I, sunPos.subtract(satPos))

psiSun  = sunDir.getAngles(RotationOrder.ZYX)[0]
tetaSun = sunDir.getAngles(RotationOrder.ZYX)[1]

print()
print("Psi  / GCRF  = {} deg".format(FastMath.toDegrees(psiSun)))
print("Teta / GCRF = {} deg".format(FastMath.toDegrees(tetaSun)))

print()
print("Delta Psi  = {} deg".format(FastMath.toDegrees(psiSun - psi)))
print("Delta Teta = {} deg".format(FastMath.toDegrees(tetaSun - teta)))
