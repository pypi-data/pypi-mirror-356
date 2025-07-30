import unittest
import math
import sys
import os

from jpype import JImplements, JOverride

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytrius

pytrius.initVM()

from Utils import Utils

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

from fr.cnes.sirius.patrius.attitudes import  BodyCenterPointing, ConstantAttitudeLaw
from fr.cnes.sirius.patrius.frames import Frame, FramesFactory
from fr.cnes.sirius.patrius.math.geometry.euclidean.threed import Line, Rotation, Vector3D
from fr.cnes.sirius.patrius.math.util import MathLib
from fr.cnes.sirius.patrius.propagation import SimpleMassModel, SpacecraftState
from fr.cnes.sirius.patrius.propagation.analytical.tle import TLEPropagator, TLE
from fr.cnes.sirius.patrius.propagation.sampling import PatriusFixedStepHandler
from fr.cnes.sirius.patrius.time import AbsoluteDate
from fr.cnes.sirius.patrius.utils import Constants
from fr.cnes.sirius.patrius.utils.exception import PatriusException, PropagationException
from fr.cnes.sirius.patrius.utils import PatriusConfiguration


class TestTLEPropagator(unittest.TestCase):

    DEFAULT = "DEFAULT"
    mass = SimpleMassModel(1000.0, DEFAULT)

    PatriusDataset.addResourcesFromPatriusDataset()
    PatriusConfiguration.setPatriusCompatibilityMode(PatriusConfiguration.PatriusVersionCompatibility.NEW_MODELS)

    FramesFactory.setConfiguration(Utils.get_iers2003_configuration_woeop(True))

    line1 = "1 37753U 11036A   12090.13205652 -.00000006  00000-0  00000+0 0  2272"
    line2 = "2 37753  55.0032 176.5796 0004733  13.2285 346.8266  2.00565440  5153"
    tle = TLE(line1, line2)
    
    period = 717.97 * 60.0

    def testSlaveMode(self):

        propagator = TLEPropagator.selectExtrapolator(self.tle, None, self.mass)
        initDate = self.tle.getDate()
        initialState = propagator.getInitialState()

        # Simulate a full period of a GPS satellite
        finalState = propagator.propagate(initDate.shiftedBy(self.period))

        # Check results
        assert math.isclose(initialState.getA(), finalState.getA(), abs_tol=1e-1)
        assert math.isclose(initialState.getEquinoctialEx(), finalState.getEquinoctialEx(), abs_tol=1e-1)
        assert math.isclose(initialState.getEquinoctialEy(), finalState.getEquinoctialEy(), abs_tol=1e-1)
        assert math.isclose(initialState.getHx(), finalState.getHx(), abs_tol=1e-3)
        assert math.isclose(initialState.getHy(), finalState.getHy(), abs_tol=1e-3)
        assert math.isclose(initialState.getLM(), finalState.getLM(), abs_tol=1e-3)
        assert math.isclose(initialState.getMass("DEFAULT"), finalState.getMass("DEFAULT"), abs_tol=0)


    def testEphemerisMode(self):

        propagator = TLEPropagator.selectExtrapolator(self.tle)
        propagator.setEphemerisMode()

        initDate = self.tle.getDate()
        initialState = propagator.getInitialState()

        # Simulate a full period of a GPS satellite
        # -----------------------------------------
        endDate = initDate.shiftedBy(self.period)
        propagator.propagate(endDate)

        # get the ephemeris
        boundedProp = propagator.getGeneratedEphemeris()

        # get the initial state from the ephemeris and check if it is the same as
        # the initial state from the TLE
        boundedState = boundedProp.propagate(initDate)

        # Check results
        assert math.isclose(initialState.getA(), boundedState.getA(), abs_tol=0.)
        assert math.isclose(initialState.getEquinoctialEx(), boundedState.getEquinoctialEx(), abs_tol=0.)
        assert math.isclose(initialState.getEquinoctialEy(), boundedState.getEquinoctialEy(), abs_tol=0.)
        assert math.isclose(initialState.getHx(), boundedState.getHx(), abs_tol=0.)
        assert math.isclose(initialState.getHy(), boundedState.getHy(), abs_tol=0.)
        assert math.isclose(initialState.getLM(), boundedState.getLM(), abs_tol=1e-14)

        finalState = boundedProp.propagate(endDate)

        # Check results
        assert math.isclose(initialState.getA(), finalState.getA(), abs_tol=1e-1)
        assert math.isclose(initialState.getEquinoctialEx(), finalState.getEquinoctialEx(), abs_tol=1e-1)
        assert math.isclose(initialState.getEquinoctialEy(), finalState.getEquinoctialEy(), abs_tol=1e-1)
        assert math.isclose(initialState.getHx(), finalState.getHx(), abs_tol=1e-3)
        assert math.isclose(initialState.getHy(), finalState.getHy(), abs_tol=1e-3)
        assert math.isclose(initialState.getLM(), finalState.getLM(), abs_tol=1e-3)
    

    def testBodyCenterInPointingDirection(self):

        itrf = FramesFactory.getITRF()
        checker = DistanceChecker(itrf)

        # with Earth pointing attitude, distance should be small
        propagator = TLEPropagator.selectExtrapolator(self.tle,
                BodyCenterPointing(itrf), self.mass)
        propagator.setMasterMode(900.0, checker)
        propagator.propagate(self.tle.getDate().shiftedBy(self.period))
        assert math.isclose(0.0, checker.getMaxDistance(), abs_tol=6.0e-7)

        # results should be the same as previous
        propagator = TLEPropagator.selectExtrapolator(self.tle, BodyCenterPointing(itrf),
                BodyCenterPointing(itrf), self.mass)
        propagator.setMasterMode(900.0, checker)
        propagator.propagate(self.tle.getDate().shiftedBy(self.period))
        assert math.isclose(0.0, checker.getMaxDistance(), abs_tol=6.0e-7)

        # with default attitude mode, distance should be large
        propagator = TLEPropagator.selectExtrapolator(self.tle)
        propagator.setAttitudeProvider(ConstantAttitudeLaw(FramesFactory.getEME2000(),
                Rotation.IDENTITY))
        propagator.setMasterMode(900.0, checker)
        propagator.propagate(self.tle.getDate().shiftedBy(self.period))
        assert math.isclose(1.5219e7, checker.getMinDistance(), abs_tol=1000.0)
        assert math.isclose(2.6572e7, checker.getMaxDistance(), abs_tol=1000.0)


    
    def propagationWithMassChange(self):
        propagator = TLEPropagator.selectExtrapolator(self.tle, None, self.mass)
        initDate = self.tle.getDate()

        # Simulate a full period of a GPS satellite
        finalState = propagator.propagate(initDate.shiftedBy(self.period))

        # Get the initial state:
        state0 = propagator.getInitialState()
        # Check the value of the mass as an additional state (no maneuver --> it should not
        # have changed):
        assert math.isclose(state0.getMass(self.DEFAULT), finalState.getMass(self.DEFAULT), abs_tol=0.0)

        # Re-run the same test, adding an impulse maneuver to the propagator:
        self.mass = SimpleMassModel(1000.0, self.DEFAULT)
        propagator = TLEPropagator.selectExtrapolator(self.tle, ConstantAttitudeLaw(
                FramesFactory.getEME2000(), Rotation.IDENTITY), self.mass)
        # Get the initial state:
        state0 = propagator.getInitialState()
        # Change mass value
        self.mass.updateMass(self.DEFAULT, 800.)
        # Perform the propagation:
        stateEnd = propagator.propagate(initDate.shiftedBy(self.period))
        # Check mass value
        # Check the value of the mass as an additional state:
        assert math.isclose(800, stateEnd.getMass(self.DEFAULT), abs_tol=0.0)

@JImplements(PatriusFixedStepHandler)
class DistanceChecker:
        def __init__(self, itrf: Frame):
            self.itrf = itrf
            self.minDistance = float('inf')  # Initialize to positive infinity
            self.maxDistance = float('-inf')  # Initialize to negative infinity

        def getMinDistance(self):
            return self.minDistance

        def getMaxDistance(self):
            return self.maxDistance
        
        @JOverride
        def init(self, s0: SpacecraftState, t: AbsoluteDate):
            # Reset min and max distances at the beginning
            self.minDistance = float('inf')
            self.maxDistance = float('-inf')

        @JOverride
        def handleStep(self, currentState: SpacecraftState, isLast: bool):
            try:
                # Get satellite attitude rotation, i.e., rotation from inertial frame to satellite frame
                rotSat = currentState.getAttitude().getRotation()

                # Transform Z axis from satellite frame to inertial frame
                zSat = rotSat.applyTo(Vector3D.PLUS_K)

                # Transform Z axis from inertial frame to ITRF
                transform = currentState.getFrame().getTransformTo(self.itrf, currentState.getDate())
                zSatITRF = transform.transformVector(zSat)

                # Transform satellite position/velocity from inertial frame to ITRF
                pvSatITRF = transform.transformPVCoordinates(currentState.getPVCoordinates())

                # Line containing satellite point and following pointing direction
                pointingLine = Line(pvSatITRF.getPosition(), pvSatITRF.getPosition().add(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, zSatITRF))

                # Calculate distance from the satellite to the point of interest
                distance = pointingLine.distance(Vector3D.ZERO)

                # Update min and max distances
                self.minDistance = MathLib.min(self.minDistance, distance)
                self.maxDistance = MathLib.max(self.maxDistance, distance)

            except PatriusException as oe:
                raise PropagationException(oe)
    

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTLEPropagator)
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
