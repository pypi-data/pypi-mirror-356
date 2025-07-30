import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.patrius.assembly import AssemblyBuilder
from fr.cnes.sirius.patrius.events.detectors import AnomalyDetector
from fr.cnes.sirius.patrius.frames import LOFType
from fr.cnes.sirius.patrius.assembly.models import MassModel
from fr.cnes.sirius.patrius.assembly.properties import MassProperty
from fr.cnes.sirius.patrius.orbits import PositionAngle
from fr.cnes.sirius.patrius.forces.maneuvers import ImpulseManeuver
from fr.cnes.sirius.patrius.frames.transformations import Transform
from fr.cnes.sirius.patrius.math.geometry.euclidean.threed import Vector3D
from fr.cnes.sirius.patrius.math.util import FastMath

# Creating a mass model with a main part and with a tank
builder = AssemblyBuilder()

# Main part (dry mass)
dryMass = 1000.
builder.addMainPart("MAIN")
builder.addProperty(MassProperty(dryMass), "MAIN")

# Tank part (ergols mass)
ergolsMass = 100.
builder.addPart("TANK", "MAIN", Transform.IDENTITY)
builder.addProperty(MassProperty(ergolsMass), "TANK")

assembly = builder.returnAssembly()
mm = MassModel(assembly)

# Event corresponding to the criteria to trigger the impulsive maneuver
# (when the S/C is at the apogee)
event = AnomalyDetector(PositionAngle.TRUE, FastMath.PI)

# Creation of the impulsive maneuver (20 m/s int the x vehicle direction)
deltaV = Vector3D(20., 0., 0.)
isp = 300.
# SPECIFIC
imp = ImpulseManeuver(event, deltaV, isp, mm, "TANK", LOFType.TNW)
# SPECIFIC

print(f"DV components: {imp.getDeltaVSat()}")
# The getFrame() method is returning "None" as a LOF frame is not defined as a frame.
# Nevertheless, an attitude law will not be mandatory when propagating the orbit.
print(f"Maneuver frame: {imp.getFrame()}")
