import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

from fr.cnes.sirius.patrius.frames import FramesFactory
from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.patrius.bodies import CelestialBodyFactory, JPLCelestialBodyLoader, PredefinedEphemerisType


# Patrius Dataset initialization
PatriusDataset.addResourcesFromPatriusDataset()

# String array for file names
file_names = ["unxp.*.405", "unxp.*.406"]

# Data for Sun coordinates output
tuc = TimeScalesFactory.getUTC()
date = AbsoluteDate("2010-01-01T12:00:00.000", tuc)
icrf = FramesFactory.getICRF()

for file_name in file_names:
    loader = JPLCelestialBodyLoader(file_name, PredefinedEphemerisType.SUN)

    CelestialBodyFactory.clearCelestialBodyLoaders()
    CelestialBodyFactory.addCelestialBodyLoader(CelestialBodyFactory.SUN, loader)

    # Using the loading theory
    sun = loader.loadCelestialBody(CelestialBodyFactory.SUN)

    # Coordinates of the Sun at a given date and reference frame
    pv = sun.getPVCoordinates(date, icrf)

    print("")
    print(pv.getPosition().getX())
    print(pv.getPosition().getY())
    print(pv.getPosition().getZ())
