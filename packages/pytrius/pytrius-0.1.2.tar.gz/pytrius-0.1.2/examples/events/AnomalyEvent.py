import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.patrius.math.util import FastMath
from fr.cnes.sirius.patrius.orbits import PositionAngle
from fr.cnes.sirius.patrius.events import AbstractDetector
from fr.cnes.sirius.patrius.events.detectors import AnomalyDetector
from fr.cnes.sirius.patrius.events import EventDetector


# Creating a list of AnomalyDetectors
detector_list = []

# AOL event with default values
ano_event_1 = AnomalyDetector(PositionAngle.TRUE, FastMath.PI)
detector_list.append(ano_event_1)

# Same event with customized convergence values
max_check = 0.5 * AbstractDetector.DEFAULT_MAXCHECK
threshold = 2. * AbstractDetector.DEFAULT_THRESHOLD
ano_event_2 = AnomalyDetector(PositionAngle.TRUE, FastMath.PI, max_check, threshold)
detector_list.append(ano_event_2)

# Same event with customized convergence values and specifying the action
ano_event_3 = AnomalyDetector(PositionAngle.TRUE, FastMath.PI, max_check, threshold, EventDetector.Action.STOP)
detector_list.append(ano_event_3)

# Same event with customized convergence values, specifying action, and removing the event after occurrence
ano_event_4 = AnomalyDetector(PositionAngle.TRUE, FastMath.PI, max_check, threshold, EventDetector.Action.STOP, True)
detector_list.append(ano_event_4)

for anomaly_detector in detector_list:
    print("Anomaly of the event: {} deg".format(FastMath.toDegrees(anomaly_detector.getAnomaly())))
    print("Anomaly type of the event: {}".format(anomaly_detector.getAnomalyType()))
    print("Max check interval of the event: {} s".format(anomaly_detector.getMaxCheckInterval()))
    print("Threshold of the event: {} s".format(anomaly_detector.getThreshold()))
    print("Remove the event after occurring: {}".format(anomaly_detector.shouldBeRemoved()))
    print()
    print("Slope selection of the event: {}".format(anomaly_detector.getSlopeSelection()))
    print("Max iteration count of the event: {}".format(anomaly_detector.getMaxIterationCount()))
    print()