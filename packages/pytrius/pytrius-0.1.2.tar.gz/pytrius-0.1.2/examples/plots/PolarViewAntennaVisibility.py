import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius
pytrius.initVM()

from fr.cnes.sirius.patrius.utils import Constants
from fr.cnes.sirius.patrius.bodies import EllipsoidPoint
from fr.cnes.sirius.patrius.frames import FramesFactory, TopocentricFrame
from fr.cnes.sirius.patrius.math.util import MathLib, FastMath
from fr.cnes.sirius.patrius.bodies import OneAxisEllipsoid

# Create figure
plt.figure(figsize=(12, 7))

# Set up Basemap (Mercator projection)
m = Basemap(projection='npaeqd',boundinglat=-30,lon_0=355,resolution='l')


# Draw map details
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='lightgray', lake_color='aqua')
m.drawmapboundary(fill_color='aqua')
m.drawparallels(np.arange(-90., 91., 30.), labels=[1, 0, 0, 0], fontsize=9)
m.drawmeridians(np.arange(-180., 181., 60.), labels=[0, 0, 0, 1], fontsize=9)

colors = ['r', 'g', 'b']  # Colors for each station

# Initialize Earth ellipsoid
earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS,
                         Constants.WGS84_EARTH_FLATTENING,
                         FramesFactory.getITRF())

# Define ILRS tracking stations
ilrs = [
    TopocentricFrame(
        EllipsoidPoint(earth, earth.getLLHCoordinatesSystem(),
                       MathLib.toRadians(-25.8897), MathLib.toRadians(27.6861), 1406.822, ""),
        "Hartebeesthoek"),
    TopocentricFrame(
        EllipsoidPoint(earth, earth.getLLHCoordinatesSystem(),
                       MathLib.toRadians(39.0206), MathLib.toRadians(-76.82769), 64.0, ""),
        "Greenbelt"),
    TopocentricFrame(
        EllipsoidPoint(earth, earth.getLLHCoordinatesSystem(),
                       MathLib.toRadians(39.6069), MathLib.toRadians(115.8920), 82.300, ""),
        "Beijing")
]

# Plot visibility regions and stations
for idx, station in enumerate(ilrs):
    lat_points = []
    lon_points = []

    altitude = 500000  # Start at 500 km
    while altitude < 2000000:  # Up to 2000 km
        azimuth = 0.0
        while azimuth < 2 * FastMath.PI:
            p = station.computeLimitVisibilityPoint(
                Constants.WGS84_EARTH_EQUATORIAL_RADIUS + altitude,
                azimuth,
                MathLib.toRadians(5.0)
            )
            llh = p.getLLHCoordinates()
            lat = MathLib.toDegrees(llh.getLatitude())
            lon = MathLib.toDegrees(llh.getLongitude())

            lat_points.append(lat)
            lon_points.append(lon)
            azimuth += 0.05
        altitude += 150000

    # Convert points to map coordinates and plot
    x, y = m(lon_points, lat_points)
    m.plot(x, y, '.', color=colors[idx], markersize=2, alpha=0.6)

    # Plot station location
    origin = station.getFrameOrigin().getLLHCoordinates()
    lat_sta = MathLib.toDegrees(origin.getLatitude())
    lon_sta = MathLib.toDegrees(origin.getLongitude())
    x_sta, y_sta = m(lon_sta, lat_sta)
    m.plot(x_sta, y_sta, 'x', color=colors[idx], label=station.getName(), markersize=6, markeredgewidth=5)

# Finalize plot
plt.title("ILRS Station Visibility Limit Points", fontsize=14)
plt.legend(loc='lower left', fontsize=10)
plt.tight_layout()
plt.show()
