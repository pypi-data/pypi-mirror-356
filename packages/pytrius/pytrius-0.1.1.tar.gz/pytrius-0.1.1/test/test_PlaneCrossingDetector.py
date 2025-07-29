import unittest
import math
import sys
import os

from jpype import JImplements, JOverride

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.patrius.events.detectors import NodeDetector
from fr.cnes.sirius.patrius.events import EventDetector
from fr.cnes.sirius.patrius.events.postprocessing import CodedEventsLogger, GenericCodingEventDetector
from fr.cnes.sirius.patrius.frames import Frame, FramesFactory
from fr.cnes.sirius.patrius.math.geometry.euclidean.threed import Vector3D
from fr.cnes.sirius.patrius.math.util import MathLib, Precision
from fr.cnes.sirius.patrius.orbits import EquatorialOrbit, KeplerianOrbit, PositionAngle
from fr.cnes.sirius.patrius.propagation.analytical import KeplerianPropagator
from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.patrius.events.detectors import PlaneCrossingDetector
from fr.cnes.sirius.patrius.utils import Constants

class TestPlaneCrossingDetector(unittest.TestCase):

#
#Tests the creation of a detector for a plane not containing the origin and not aligned with an axis, and the
#event dates are correctly aligned with the expected dates.
#
#@throws PropagationException
#
#
    
    def testOffsetInOriginDates(self):
        # Definition of the plane to be crossed
        referenceFrame= FramesFactory.getGCRF()
        point = Vector3D(0, 0, 2250e3 * math.sqrt(2))
        normalVector = Vector3D(0, 1, 1)

        # Creation of the plane crossing detector
        detector = PlaneCrossingDetector(point, normalVector, referenceFrame, EventDetector.Action.CONTINUE, EventDetector.Action.CONTINUE, False,
                False, PlaneCrossingDetector.DEFAULT_MAXCHECK, PlaneCrossingDetector.DEFAULT_THRESHOLD)

        # Creation of an equatorial circular such that the first crossing occurs after an eighth of the and
        # the second crossing a fourth of the period later.
        initialDate = AbsoluteDate(2008, 1, 1, TimeScalesFactory.getTAI())
        orbit = EquatorialOrbit(2 * 2250e3, 0, 0, 0, 0, 0, PositionAngle.TRUE, referenceFrame, initialDate, Constants.WGS84_EARTH_MU)

        # Retrieving the period of the orbit
        period = orbit.getKeplerianPeriod()
        
        # Expected crossing dates
        firstCrossingDate = initialDate.shiftedBy(period * 1 / 8)
        secondCrossingDate = initialDate.shiftedBy(period * 3 / 8)

        # Propagation of the with the detector and the results are retrieved
        propagator = KeplerianPropagator(orbit)
        propagator.addEventDetector(detector)
        codeur = GenericCodingEventDetector(detector, "Increasing", "Decreasing")
        logger = CodedEventsLogger()
        propagator.addEventDetector(logger.monitorDetector(codeur))

        propagator.propagate(initialDate.shiftedBy(period))
        detectedEvents = logger.getCodedEventsList()
        firstDetectedCrossingDate = detectedEvents.getList().get(0).getDate()
        secondDetectedCrossingDate = detectedEvents.getList().get(1).getDate()

        # Assertion of the results
        assert math.isclose(firstDetectedCrossingDate.getEpoch(), firstCrossingDate.getEpoch(),
            abs_tol=Precision.DOUBLE_COMPARISON_EPSILON)
        assert math.isclose(firstDetectedCrossingDate.getOffset(), firstCrossingDate.getOffset(),
            abs_tol=Precision.DOUBLE_COMPARISON_EPSILON)
        assert math.isclose(secondDetectedCrossingDate.getEpoch(), secondCrossingDate.getEpoch(),
            abs_tol=Precision.DOUBLE_COMPARISON_EPSILON)
        # The addition of normalization in detector impacts the detection
        assert math.isclose(secondDetectedCrossingDate.getOffset(), 0.5773589527731247,
            abs_tol=Precision.DOUBLE_COMPARISON_EPSILON)

    
    def testOffsetInOrigin(self):
        # Definition of the plane to be crossed
        referenceFrame= FramesFactory.getGCRF()
        point = Vector3D(0, 0, 2250.0)
        normalVector = Vector3D(0, 1, 1)
        normalVector2 = Vector3D(0, -1, -1)

        # Creation of the plane crossing detector
        detector = PlaneCrossingDetector(point, normalVector, referenceFrame, EventDetector.Action.CONTINUE, EventDetector.Action.CONTINUE, True, True,
                PlaneCrossingDetector.DEFAULT_MAXCHECK, PlaneCrossingDetector.DEFAULT_THRESHOLD)
        detector2 = PlaneCrossingDetector(point, normalVector2, referenceFrame, EventDetector.Action.CONTINUE, EventDetector.Action.CONTINUE, True,
                True,
                PlaneCrossingDetector.DEFAULT_MAXCHECK, PlaneCrossingDetector.DEFAULT_THRESHOLD)

        # Creation of an equatorial circular such that the altitude of the is the same as the altitude of
        # the point of the reference frame
        initialDate = AbsoluteDate(2008, 1, 1, TimeScalesFactory.getTAI())
        orbit = EquatorialOrbit(24400e3, 0, 0, 0, 0, 0, PositionAngle.TRUE, referenceFrame, initialDate,
            Constants.WGS84_EARTH_MU)
        propagator = KeplerianPropagator(orbit)
        propagator.addEventDetector(detector)
        codeur = GenericCodingEventDetector(detector, "Ascending", "Descending")
        logger = CodedEventsLogger()
        propagator.addEventDetector(logger.monitorDetector(codeur))

        propagator.addEventDetector(detector2)
        codeur2 = GenericCodingEventDetector(detector2, "Ascending", "Descending")
        logger2 = CodedEventsLogger()
        propagator.addEventDetector(logger2.monitorDetector(codeur2))

        propagator.propagate(initialDate.shiftedBy(3600 * 36))
        detectedEvents = logger.getCodedEventsList()
        detectedEvents2 = logger2.getCodedEventsList()
        for i in range(len(detectedEvents.getList())):
            assert abs(detectedEvents.getList().get(i).getDate()
                       .durationFrom(detectedEvents2.getList().get(i).getDate()))<Precision.DOUBLE_COMPARISON_EPSILON
            


#
#Compares a and an equivalent for event detection.
#
#@throws PropagationException
#
    
    def testComparisonWithNodeDetector(self):
        referenceFrame = FramesFactory.getGCRF()

        # Test with propagation
        detector = NodeDetector(referenceFrame, NodeDetector.DEFAULT_MAXCHECK,
            PlaneCrossingDetector.DEFAULT_THRESHOLD, EventDetector.Action.CONTINUE, EventDetector.Action.CONTINUE)
        assert detector.getNormalVector() == Vector3D.PLUS_K

        initialDate = AbsoluteDate(2008, 1, 1, TimeScalesFactory.getTAI())
        initialOrbit = KeplerianOrbit(24400e3, 0.72, MathLib.toRadians(5), MathLib.toRadians(180),
            MathLib.toRadians(2), MathLib.toRadians(180), PositionAngle.TRUE, FramesFactory.getGCRF(), initialDate,
            Constants.WGS84_EARTH_MU)
        propagator = KeplerianPropagator(initialOrbit)


        # Equivalent PlaneCrossing Detector
        point = Vector3D.ZERO
        normalVector = Vector3D.PLUS_K
        detectorEquivalent = PlaneCrossingDetector(point, normalVector, referenceFrame, EventDetector.Action.CONTINUE, EventDetector.Action.CONTINUE, False,
                False, PlaneCrossingDetector.DEFAULT_MAXCHECK, PlaneCrossingDetector.DEFAULT_THRESHOLD)

        # Comparison and display of the results obtained with the and the Equivalent detector built using
        # its parent class
        propagator.addEventDetector(detector)
        propagator.addEventDetector(detectorEquivalent)
        codeur = GenericCodingEventDetector(detector, "Ascending", "Descending")
        logger = CodedEventsLogger()
        propagator.addEventDetector(logger.monitorDetector(codeur))

        propagator.addEventDetector(detectorEquivalent)
        codeur2 = GenericCodingEventDetector(detectorEquivalent, "Ascending",
            "Descending")
        logger2 = CodedEventsLogger()
        propagator.addEventDetector(logger2.monitorDetector(codeur2))

        propagator.propagate(initialDate.shiftedBy(3600 * 36))
        detectedEvents = logger.getCodedEventsList()
        detectedEvents2 = logger2.getCodedEventsList()
        for i in range(len(detectedEvents.getList())):
            assert abs(detectedEvents.getList().get(i).getDate()
                       .durationFrom(detectedEvents2.getList().get(i).getDate())) < Precision.DOUBLE_COMPARISON_EPSILON
        

    
    def testEventOccured(self):
        # Builds the PlaneCrossingDetector
        point = Vector3D.ZERO
        normalVector = Vector3D.PLUS_K
        referenceFrame = FramesFactory.getGCRF()
        detector = PlaneCrossingDetector(normalVector, referenceFrame,
            PlaneCrossingDetector.INCREASING, EventDetector.Action.STOP, False, PlaneCrossingDetector.DEFAULT_MAXCHECK,
            PlaneCrossingDetector.DEFAULT_THRESHOLD)
        # Builds the for propagation
        initialDate = AbsoluteDate(2008, 1, 1, TimeScalesFactory.getTAI())
        initialOrbit = KeplerianOrbit(24400e3, 0.72, MathLib.toRadians(5), MathLib.toRadians(180),
            MathLib.toRadians(2), MathLib.toRadians(180), PositionAngle.TRUE, referenceFrame, initialDate,
            Constants.WGS84_EARTH_MU)
        propagator = KeplerianPropagator(initialOrbit)

        propagator.addEventDetector(detector)
        finalState = propagator.propagate(initialDate.shiftedBy(36 * 3600))
        action = detector.eventOccurred(finalState, True, True)
        assert EventDetector.Action.STOP == action


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPlaneCrossingDetector)
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
