import sys
import os

from jpype import JImplements, JOverride

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.patrius.events import EventDetector
from fr.cnes.sirius.patrius.propagation import SpacecraftState
from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.patrius.events.detectors import PlaneCrossingDetector

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

@JImplements(EventDetector)
class EventUsingEventDetector:
    
    def __init__(self, date):
        """
        Constructor
        :param date: AbsoluteDate when the event will occur.
        """
        self.date = date
    
    @JOverride
    def eventOccurred(self, s, increasing, forward):
        """
        Action when the event occurs.
        :param s: SpacecraftState
        :param increasing: Boolean for increasing
        :param forward: Boolean for forward propagation
        :return: Action to perform after the event occurs (STOP here)
        """
        return EventDetector.Action.STOP
    
    @JOverride
    def g(self, s: SpacecraftState):
        """
        Detection function that calculates the difference in time
        from the event date.
        :param s: SpacecraftState
        :return: Time difference
        """
        return s.getDate().durationFrom(self.date)
    
    @JOverride
    def getMaxCheckInterval(self):
        """
        Get the maximum check interval.
        :return: Maximum check interval (default value here)
        """
        return PlaneCrossingDetector.DEFAULT_MAXCHECK
    
    @JOverride
    def getMaxIterationCount(self):
        """
        Get the maximum number of iterations.
        :return: Max iteration count (20 here)
        """
        return 20
    
    @JOverride
    def getSlopeSelection(self):
        """
        Get the slope selection for event detection.
        :return: INCREASING/DECREASING slope detection
        """
        return EventDetector.INCREASING_DECREASING
    
    @JOverride
    def getThreshold(self):
        """
        Get the threshold for the event detection.
        :return: Default threshold value
        """
        return PlaneCrossingDetector.DEFAULT_THRESHOLD
    
    @JOverride
    def init(self, s0, t):
        """
        Initialization (nothing specific to do here).
        :param s0: Initial SpacecraftState
        :param t: AbsoluteDate for initialization
        """
        pass
    
    @JOverride
    def resetState(self, oldState):
        """
        Reset spacecraft state (no reset needed here).
        :param oldState: Old SpacecraftState
        :return: Old SpacecraftState (no changes)
        """
        return oldState
    
    @JOverride
    def shouldBeRemoved(self):
        """
        Check if the event should be removed after occurrence.
        :return: False (no removal)
        """
        return False
    
    @JOverride
    def copy(self):
        """
        Copy the event detector with a new date.
        :return: New EventUsingEventDetector with copied date
        """
        newDate = AbsoluteDate(self.date, 0.0)
        return EventUsingEventDetector(newDate)
    
    @JOverride
    def filterEvent(self, state, increasing, forward):
        """
        Filtering function for events.
        :param state: SpacecraftState
        :param increasing: Boolean for increasing
        :param forward: Boolean for forward propagation
        :return: False (no filtering needed)
        """
        return False
    
    @staticmethod
    def main():
        """
        Main method to demonstrate the event detector.
        """
        # Initialize the UTC time scale

        # Patrius Dataset initialization (needed for example to get the UTC time)
        PatriusDataset.addResourcesFromPatriusDataset() 

        TUC = TimeScalesFactory.getUTC()
        
        # Create an absolute date
        date = AbsoluteDate("2010-01-01T12:00:00.000", TUC)
        
        # Create the event detector
        event = EventUsingEventDetector(date)
        
        # Print details about the event
        print("Max check interval of the event: {} s".format(event.getMaxCheckInterval()))
        print("Threshold of the event: {} s".format(event.getThreshold()))
        print("Remove the event after occurring: {}".format(event.shouldBeRemoved()))


# Call the main function
if __name__ == "__main__":
    EventUsingEventDetector.main()