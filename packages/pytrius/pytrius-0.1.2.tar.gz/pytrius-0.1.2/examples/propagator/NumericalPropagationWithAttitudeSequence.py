import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

from fr.cnes.sirius.patrius.attitudes import  AttitudesSequence, ConstantAttitudeLaw
from fr.cnes.sirius.patrius.frames import FramesFactory
from fr.cnes.sirius.patrius.math.geometry.euclidean.threed import Rotation, RotationOrder
from fr.cnes.sirius.patrius.math.ode.nonstiff import ClassicalRungeKuttaIntegrator
from fr.cnes.sirius.patrius.math.util import FastMath
from fr.cnes.sirius.patrius.orbits import ApsisOrbit, OrbitType, PositionAngle
from fr.cnes.sirius.patrius.orbits.orbitalparameters import ApsisRadiusParameters
from fr.cnes.sirius.patrius.propagation import SpacecraftState
from fr.cnes.sirius.patrius.events.detectors import AOLDetector
from fr.cnes.sirius.patrius.events import EventDetector
from fr.cnes.sirius.patrius.propagation.numerical import NumericalPropagator
from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.patrius.utils import Constants


# Patrius Dataset initialization (needed for example to get the UTC time)
PatriusDataset.addResourcesFromPatriusDataset()

# Recovery of the UTC time scale using a "factory"
TUC = TimeScalesFactory.getUTC()

# Date of the orbit given in UTC time scale
date = AbsoluteDate("2010-01-01T12:00:00.000", TUC)

# Getting the frame which will define the orbit parameters
GCRF = FramesFactory.getGCRF()

# Initial orbit parameters
sma = 7200.e+3
exc = 0.01
per = sma * (1. - exc)
apo = sma * (1. + exc)
inc = FastMath.toRadians(98.)
pa = FastMath.toRadians(0.)
raan = FastMath.toRadians(0.)
anm = FastMath.toRadians(0.)
MU = Constants.WGS84_EARTH_MU

# Apsis radius parameters and initial orbit
par = ApsisRadiusParameters(per, apo, inc, pa, raan, anm, PositionAngle.MEAN, MU)
iniOrbit = ApsisOrbit(par, GCRF, date)

# Creating a spacecraft state
iniState = SpacecraftState(iniOrbit)

# Initialization of the Runge Kutta integrator with a 2 s step
pasRk = 2.0
integrator = ClassicalRungeKuttaIntegrator(pasRk)

# Initialization of the propagator
propagator = NumericalPropagator(integrator, iniState.getFrame(),
                                    OrbitType.CARTESIAN, PositionAngle.TRUE)
propagator.resetInitialState(iniState)

# SPECIFIC: Adding attitude sequence
seqAtt = AttitudesSequence()

# Laws to be taken into account in the sequence
law1 = ConstantAttitudeLaw(GCRF, Rotation(RotationOrder.ZYX, 0., 0., 0.))
law2 = ConstantAttitudeLaw(GCRF, Rotation(RotationOrder.ZYX, FastMath.toRadians(45.), 
                                            FastMath.toRadians(45.), FastMath.toRadians(45.)))

# Events that will switch from one law to another
maxCheck = 10.0
threshold = 1.e-3
event1 = AOLDetector(0.0, PositionAngle.MEAN, GCRF, maxCheck, threshold, EventDetector.Action.RESET_STATE)
event2 = AOLDetector(FastMath.toRadians(180.), PositionAngle.MEAN, GCRF, maxCheck, threshold, EventDetector.Action.RESET_STATE)

# Adding switches
seqAtt.addSwitchingCondition(law1, event1, True, False, law2)
seqAtt.addSwitchingCondition(law2, event2, True, False, law1)

propagator.setAttitudeProvider(seqAtt)
seqAtt.registerSwitchEvents(propagator)

# Propagating time
dt = 0.25 * iniOrbit.getKeplerianPeriod()
print(dt)
finalDate = date.shiftedBy(dt)
finalState = propagator.propagate(finalDate)
finalOrbit = finalState.getOrbit()

# Printing new date and true latitude argument
print("\nInitial true latitude argument = {:.2f} deg".format(FastMath.toDegrees(iniOrbit.getLv())))
print("New date = {}".format(finalOrbit.getDate().toString(TUC)))
print("True latitude argument = {:.2f} deg".format(FastMath.toDegrees(finalOrbit.getLv())))

# Printing attitude
psi = finalState.getAttitude().getRotation().getAngles(RotationOrder.ZYX)[0]
teta = finalState.getAttitude().getRotation().getAngles(RotationOrder.ZYX)[1]
phi = finalState.getAttitude().getRotation().getAngles(RotationOrder.ZYX)[2]
print("Psi / GCRF  = {:.2f} deg".format(FastMath.toDegrees(psi)))
print("Teta / GCRF = {:.2f} deg".format(FastMath.toDegrees(teta)))
print("Phi / GCRF  = {:.2f} deg".format(FastMath.toDegrees(phi)))