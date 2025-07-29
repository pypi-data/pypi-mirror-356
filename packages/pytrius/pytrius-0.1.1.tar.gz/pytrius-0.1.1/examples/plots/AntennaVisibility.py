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

# Initialize map (Mercator projection, adjust as needed)
plt.figure(figsize=(10, 6))
m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=85,
            llcrnrlon=-180, urcrnrlon=180, resolution='c')

m.drawcoastlines()
m.fillcontinents(color='lightgray', lake_color='aqua')
m.drawmapboundary(fill_color='aqua')

# Draw parallels and meridians with labels
m.drawparallels(np.arange(-90., 91., 30.), labels=[1, 0, 0, 0], fontsize=10)
m.drawmeridians(np.arange(-180., 181., 60.), labels=[0, 0, 0, 1], fontsize=10)

colors = ['r', 'g', 'b']  # Different colors for stations

# Initialize Earth ellipsoid
earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS,
                         Constants.WGS84_EARTH_FLATTENING,
                         FramesFactory.getITRF())

# Define stations as TopocentricFrames
ilrs = [
    TopocentricFrame(
        EllipsoidPoint(earth, earth.getLLHCoordinatesSystem(),
                       MathLib.toRadians(-25.8897),
                       MathLib.toRadians(27.6861),
                       1406.822, ""),
        "Hartebeesthoek"),
    TopocentricFrame(
        EllipsoidPoint(earth, earth.getLLHCoordinatesSystem(),
                       MathLib.toRadians(39.0206),
                       MathLib.toRadians(-76.82769),
                       64.0, ""),
        "Greenbelt"),
    TopocentricFrame(
        EllipsoidPoint(earth, earth.getLLHCoordinatesSystem(),
                       MathLib.toRadians(39.6069),
                       MathLib.toRadians(115.8920),
                       82.300, ""),
        "Beijing")
]

for idx, station in enumerate(ilrs):
    lat_points = []
    lon_points = []

    altitude = 500000
    while altitude < 2000000:
        azimuth = 0.0
        while azimuth < 2 * FastMath.PI:
            p = station.computeLimitVisibilityPoint(
                Constants.WGS84_EARTH_EQUATORIAL_RADIUS + altitude,
                azimuth,
                MathLib.toRadians(5.0)
            )

            # Extract lat/lon from the point (in radians)
            llh = p.getLLHCoordinates()
            lat = MathLib.toDegrees(llh.getLatitude())
            lon = MathLib.toDegrees(llh.getLongitude())

            lat_points.append(lat)
            lon_points.append(lon)

            azimuth += 0.05
        altitude += 150000

    # Convert lat/lon to map projection coords
    x, y = m(lon_points, lat_points)
    x_sta, y_sta = m(MathLib.toDegrees(station.getFrameOrigin().getLLHCoordinates().getLongitude()), MathLib.toDegrees(station.getFrameOrigin().getLLHCoordinates().getLatitude()))
    m.plot(x, y, '.', color=colors[idx], markersize=2)
    m.plot(x_sta, y_sta, 'x', color=colors[idx], label=station.getName(), markersize=5)

plt.title("Visibility Limit Points for ILRS Stations wrt different altitudes")
plt.legend()
plt.show()