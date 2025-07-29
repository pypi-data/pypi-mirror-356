import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import numpy as np

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius
pytrius.initVM()

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

from fr.cnes.sirius.patrius.time import AbsoluteDate
from fr.cnes.sirius.patrius.utils import Constants
from fr.cnes.sirius.patrius.frames import FramesFactory
from fr.cnes.sirius.patrius.math.util import MathLib
from fr.cnes.sirius.patrius.bodies import OneAxisEllipsoid
from fr.cnes.sirius.patrius.propagation.analytical.tle import TLE, TLEPropagator


# Patrius Dataset initialization (needed for example to get the UTC time)
PatriusDataset.addResourcesFromPatriusDataset()

tle = TLE("1 25544U 98067A   18155.13777713  .00014923  00000-0  26896-3 0  9997",
                "2 25544  51.6376  11.7370 0001938 182.3055 323.8206 15.49999521513135")
date: AbsoluteDate = tle.getDate()

propagator = TLEPropagator.selectExtrapolator(tle)

# Time span for ground track propagation (e.g., one full orbit period)
orbit_period = 92.9*60
time_step = 60 
current_time = date
end_time = date.shiftedBy(20*orbit_period)

# Initialize time and arrays to store lat/lon
lats = []
lons = []

earthShape = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, Constants.WGS84_EARTH_FLATTENING, FramesFactory.getITRF(), "earth")

while current_time.compareTo(end_time) <= 0:

    # Propagation
    state = propagator.propagate(current_time)
    satPos = state.getPVCoordinates(earthShape.getBodyFrame()).getPosition()
    point = earthShape.buildPoint(satPos, earthShape.getBodyFrame(), state.getDate(), "")

    # Get the latitude and longitude coordinates
    lat = point.getLLHCoordinates().getLatitude()
    lon = point.getLLHCoordinates().getLongitude()

    # Store values in degrees
    lats.append(MathLib.toDegrees(lat))
    lons.append(MathLib.toDegrees(lon))

    # Increment time
    current_time = current_time.shiftedBy(time_step)

# Plot the ground track
plt.figure(figsize=(10, 6))
m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=84,\
            llcrnrlon=-180, urcrnrlon=180, resolution='c')
m.drawcoastlines()
m.fillcontinents(color='k',lake_color='w')
m.drawmapboundary(fill_color='w') 

m.drawparallels(np.arange(-90.,91.,30.),labels=[1, 0, 0, 0], fontsize=10)
m.drawmeridians(np.arange(-180.,181.,60.), labels=[0, 0, 0, 1], fontsize=10)

x, y = m(lons, lats)
m.plot(x, y, '.', lw=1, color='r')

plt.title("ISS Ground Track")
plt.show()