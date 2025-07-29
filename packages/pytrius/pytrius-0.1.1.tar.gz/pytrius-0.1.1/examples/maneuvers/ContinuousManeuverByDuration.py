import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.patrius.assembly import AssemblyBuilder
from fr.cnes.sirius.patrius.frames import LOFType
from fr.cnes.sirius.patrius.assembly.models import MassModel
from fr.cnes.sirius.patrius.assembly.properties import MassProperty
from fr.cnes.sirius.patrius.forces.maneuvers import ContinuousThrustManeuver
from fr.cnes.sirius.patrius.assembly.properties import TankProperty, PropulsiveProperty
from fr.cnes.sirius.patrius.frames.transformations import Transform
from fr.cnes.sirius.patrius.math.geometry.euclidean.threed import Vector3D
from fr.cnes.sirius.patrius.math.util import FastMath

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

# Patrius Dataset initialization (needed for example to get the UTC time)
PatriusDataset.addResourcesFromPatriusDataset() 

# Recovery of the UTC time scale using a "factory" (not to duplicate such unique object)
TUC = TimeScalesFactory.getUTC()

# Creating a mass model with a main part and with a tank
builder = AssemblyBuilder()

# Main part (dry mass)
dryMass = 1000.
builder.addMainPart("MAIN")
builder.addProperty(MassProperty(dryMass), "MAIN")

# Tank part (ergols mass)
builder.addPart("TANK", "MAIN", Transform.IDENTITY)
ergolsMass = 100.
tank = TankProperty(ergolsMass)
builder.addProperty(tank, "TANK")

# Engine part
builder.addPart("PROP", "MAIN", Transform.IDENTITY)
isp = 300.
thrust = 400.
prop = PropulsiveProperty(thrust, isp) # au lieu de PropulsiveProperty("PROP", thrust, isp)
builder.addProperty(prop, "PROP")

assembly = builder.returnAssembly()
mm = MassModel(assembly)

# SPECIFIC
# Duration of the maneuver to get a 20 m/s boost
startDate = AbsoluteDate("2010-01-01T12:00:00.000", TUC)
G0 = 9.80665
duration = G0*isp*mm.getTotalMass()*(1. - FastMath.exp(-20/(G0*isp)))/thrust
# Direction of the thrust in the X vehicle axis
direction = Vector3D(1., 0., 0.)
# Creation of the continuous thrust maneuver
man = ContinuousThrustManeuver(startDate, duration, prop, direction, mm, tank, LOFType.TNW)

print(f"End of the thrust: {man.getEndDate()}")
print(f"Duration of the thrust: {duration} s")
print(f"Duration of the thrust: {man.getEndDate().durationFrom(startDate)} s")
# The getFrame() method is returning "null" as a LOF frame is not define as a frame.
# Nevertheless, an attitude law will not be mandatory when propagating the orbit.
print(f"Maneuver frame: {man.getFrame()}")