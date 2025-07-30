import unittest
import math
import sys
import os

from jpype import JImplements, JOverride

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytrius

pytrius.initVM()

from Validate import Validate
from Utils import Utils

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

from fr.cnes.sirius.patrius.bodies import EllipsoidPoint, OneAxisEllipsoid
from fr.cnes.sirius.patrius.frames import FramesFactory, TopocentricFrame
from fr.cnes.sirius.patrius.math.geometry.euclidean.threed import Vector3D
from fr.cnes.sirius.patrius.math.util import FastMath, MathLib, MathUtils, Precision
from fr.cnes.sirius.patrius.orbits.pvcoordinates import CardanMountPV, PVCoordinates, TopocentricPV
from fr.cnes.sirius.patrius.time import AbsoluteDate, DateComponents, TimeComponents, TimeScalesFactory


class TestTopocentricFrame(unittest.TestCase):

    northFrame = "north topocentric frame"
    epsilonTest = 1.e-12

    # Epsilon used for distance comparison. */
    epsilonDistance = epsilonTest

    # Epsilon used for velocity comparison. */
    epsilonVelocity = epsilonTest

    # Epsilon used for angular velocity comparison. */
    epsilonAngVelocity = epsilonTest * 1e5

    # Epsilon used for distance comparison. */
    epsilonAngle = epsilonTest

    # Non regression Epsilon */
    epsilonNonReg = Precision.DOUBLE_COMPARISON_EPSILON

    PatriusDataset.addResourcesFromPatriusDataset()


    def setUp(self):

        self.validate = Validate(TopocentricFrame)
        FramesFactory.setConfiguration(Utils.get_IERS2003_configuration(True))
        self.frameITRF2005 = FramesFactory.getITRF()
        self.earthSpheric = OneAxisEllipsoid(6378136.460, 0.0, self.frameITRF2005)
        self.date = AbsoluteDate(DateComponents(2008, 4, 7), TimeComponents.H00, TimeScalesFactory.getUTC())


    def tearDown(self):
        # after the tests
        self.date = None
        self.frameITRF2005 = None
        self.earthSpheric = None


    def testTransformFromPVToTopocentric(self) :

        # North topocentric frame
        point = EllipsoidPoint(self.earthSpheric, self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(43.604482), MathLib.toRadians(1.443962), 0., "")
        topoNorth = TopocentricFrame(point, 0., self.northFrame)

        # Cartesian coordinates expressed in the North topocentric frame
        position = Vector3D(100, -65, 35)
        velocity = Vector3D(-23, -86, 12)
        pv = PVCoordinates(position, velocity)

        # Conversion from Cartesian coordinates (position and velocity) to topocentric coordinates
        topoCoordPV = topoNorth.transformFromPVToTopocentric(pv, topoNorth, self.date)

        # elevation angle
        self.validate.assert_equals_with_relative_tolerance(topoCoordPV.getElevation(), 0.2854416884751322,
            self.epsilonNonReg,
            0.285441688475132, self.epsilonAngle, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(topoNorth.getElevation(pv.getPosition(), topoNorth, self.date),
            0.2854416884751322, self.epsilonNonReg, 0.285441688475132, self.epsilonAngle, "elevation deviation")
        # azimuth angle (the reference gives the bearing : azimuth = 2PI - bearing)
        self.validate.assert_equals_with_relative_tolerance(topoCoordPV.getAzimuth(), 0.5763752205911837,
            self.epsilonNonReg,
            MathUtils.TWO_PI - 5.70681008658840, self.epsilonAngle, "azimuth deviation")
        self.validate.assert_equals_with_relative_tolerance(topoNorth.getAzimuth(pv.getPosition(), topoNorth, self.date),
            0.5763752205911837, self.epsilonNonReg, MathUtils.TWO_PI - 5.70681008658840, self.epsilonAngle,
            "azimuth deviation")
        # distance from the center of the frame
        self.validate.assert_equals_with_relative_tolerance(topoCoordPV.getRange(), 124.29802894656054, self.epsilonNonReg,
            124.298028946561, self.epsilonDistance, "range deviation")
        self.validate.assert_equals_with_relative_tolerance(topoNorth.getRange(pv.getPosition(), topoNorth, self.date),
            124.29802894656054, self.epsilonNonReg, 124.298028946561, self.epsilonDistance, "range deviation")

        # elevation rate
        self.validate.assert_equals_with_relative_tolerance(topoCoordPV.getElevationRate(), 0.030145982450162066,
            self.epsilonNonReg,
            0.0301459824501621, self.epsilonAngle, "elevation rate deviation")
        self.validate.assert_equals_with_relative_tolerance(topoNorth.getElevationRate(pv, topoNorth, self.date),
                0.030145982450162066, self.epsilonNonReg, 0.0301459824501621, self.epsilonAngle,
                "elevation rate deviation")
        # azimuth rate
        self.validate.assert_equals_with_relative_tolerance(topoCoordPV.getAzimuthRate(), 0.7096660808435853,
            self.epsilonNonReg,
            0.709666080843585, self.epsilonAngle, "azimuth rate deviation")
        self.validate.assert_equals_with_relative_tolerance(topoNorth.getAzimuthRate(pv, topoNorth, self.date),
            0.7096660808435853,
            self.epsilonNonReg, 0.709666080843585, self.epsilonAngle, "azimuth rate deviation")
        # range rate
        self.validate.assert_equals_with_relative_tolerance(topoCoordPV.getRangeRate(), 29.84761730690871,
            self.epsilonNonReg,
            29.8476173069087, self.epsilonDistance, "range rate deviation")
        self.validate.assert_equals_with_relative_tolerance(topoNorth.getRangeRate(pv, topoNorth, self.date),
            29.84761730690871,
            self.epsilonNonReg, 29.8476173069087, self.epsilonDistance, "range rate deviation")

        # Conversion from Cartesian coordinates (only the position) to topocentric coordinates
        topoCoordPosition = topoNorth.transformFromPositionToTopocentric(pv.getPosition(),
            topoNorth, self.date)

        # elevation angle
        self.validate.assert_equals_with_relative_tolerance(topoCoordPosition.getElevation(), 0.2854416884751322,
            self.epsilonNonReg,
            0.285441688475132, self.epsilonAngle, "elevation deviation")
        # azimuth angle (the reference gives the bearing : azimuth = 2PI - bearing)
        self.validate.assert_equals_with_relative_tolerance(topoCoordPosition.getAzimuth(), 0.5763752205911837,
            self.epsilonNonReg,
            MathUtils.TWO_PI - 5.70681008658840, self.epsilonAngle, "azimuth deviation")
        # distance from the center of the frame
        self.validate.assert_equals_with_relative_tolerance(topoCoordPosition.getRange(), 124.29802894656054,
            self.epsilonNonReg,
            124.298028946561, self.epsilonDistance, "range deviation")

    
    def testTransformFromTopocentricToPV(self) :

        # North topocentric frame
        point = EllipsoidPoint(self.earthSpheric, self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(43.604482), MathLib.toRadians(1.443962), 0., "")
        topoNorth = TopocentricFrame(point, 0., self.northFrame)

        # Topocentric coordinates
        topoCoord = TopocentricPV(0.285441688475, MathUtils.TWO_PI - 5.70681008659,
            124.298028947, 0.0301459824502, 0.709666080844, 29.8476173069)

        # Conversion from topocentric coordinates to pv coordinates
        pv = topoNorth.transformFromTopocentricToPV(topoCoord)

        # x component
        self.validate.assert_equals_with_relative_tolerance(pv.getPosition().getX(), 100.00000000046127,
            self.epsilonNonReg,
            100.000000000461, self.epsilonDistance, "x component")
        # y component
        self.validate.assert_equals_with_relative_tolerance(pv.getPosition().getY(), -65.0000000000726, self.epsilonNonReg,
            -65.0000000000726, self.epsilonDistance, "y component")
        # z component
        self.validate.assert_equals_with_relative_tolerance(pv.getPosition().getZ(), 35.00000000010798, self.epsilonNonReg,
            35.0000000001080, self.epsilonDistance, "z component")
        # x dot component
        self.validate.assert_equals_with_relative_tolerance(pv.getVelocity().getX(), -23.000000000064393,
            self.epsilonNonReg,
            -23.0000000000644, self.epsilonDistance, "x dot component")
        # y dot compoment
        self.validate.assert_equals_with_relative_tolerance(pv.getVelocity().getY(), -86.00000000032543,
            self.epsilonNonReg,
            -86.0000000003254, self.epsilonDistance, "y dot component")
        # z dot component
        self.validate.assert_equals_with_relative_tolerance(pv.getVelocity().getZ(), 12.000000000011138,
            self.epsilonNonReg,
            12.0000000000111, self.epsilonDistance, "z dot component")

        # Conversion from topocentric coordinates to position coordinates
        position = topoNorth.transformFromTopocentricToPosition(topoCoord.getTopocentricPosition())

        # x component
        self.validate.assert_equals_with_relative_tolerance(position.getX(), 100.00000000046127, self.epsilonNonReg,
            100.000000000461, self.epsilonDistance, "x component")
        # y component
        self.validate.assert_equals_with_relative_tolerance(position.getY(), -65.0000000000726, self.epsilonNonReg,
            -65.0000000000726, self.epsilonDistance, "y component")
        # z component
        self.validate.assert_equals_with_relative_tolerance(position.getZ(), 35.00000000010798, self.epsilonNonReg,
            35.0000000001080,
            self.epsilonDistance, "z component")
        
    
    def testTransformationPVtoCardan(self) :

        # Reference Inputs
        XRef = 100
        YRef = -65
        ZRef = 35
        XRateRef = -23
        YRateRef = -86
        ZRateRef = 12

        # Reference Outputs
        XangleRef = 1.076854957875316
        YangleRef = 0.9348634533745954
        rangeRef = 124.29802894656054
        XangleRateRef = 0.4091743119266047
        YangleRateRef = -0.6368236827766715
        rangeRateRef = 29.84761730690871

        # Non regression
        XangleNReg = 1.0768549578753155
        YangleNReg = 0.9348634533745958
        rangeNReg = 124.29802894656054
        XangleRateNReg = 0.4091743119266055
        YangleRateNReg = -0.6368236827766712
        rangeRateNReg = 29.84761730690871

        XangleNReg1 = 1.0768549578753155
        YangleNReg1 = 0.9348634533745958
        XangleRateNReg1 = 0.4091743119266055
        YangleRateNReg1 = -0.6368236827766712

        # North topocentric frame
        point = EllipsoidPoint(self.earthSpheric, self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(43.604482), MathLib.toRadians(1.443962), 0., "")
        topoNorth = TopocentricFrame(point, 0., self.northFrame)

        # Cartesian coordinates expressed in the North topocentric frame
        position = Vector3D(XRef, YRef, ZRef)
        velocity = Vector3D(XRateRef, YRateRef, ZRateRef)
        pv = PVCoordinates(position, velocity)

        # Conversion from Cartesian coordinates (position and velocity) to topocentric coordinates
        cardanCoordPV = topoNorth.transformFromPVToCardan(pv, topoNorth, self.date)

        # Computed results
        Xangle = cardanCoordPV.getXangle()
        Yangle = cardanCoordPV.getYangle()
        range = cardanCoordPV.getRange()
        XangleRate = cardanCoordPV.getXangleRate()
        YangleRate = cardanCoordPV.getYangleRate()
        rangeRate = cardanCoordPV.getRangeRate()

        # Values
        self.validate.assert_equals_with_relative_tolerance(Xangle, XangleNReg, self.epsilonNonReg,
            XangleRef, self.epsilonAngle, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(Yangle, YangleNReg, self.epsilonNonReg,
            YangleRef, self.epsilonAngle, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(range, rangeNReg, self.epsilonNonReg,
            rangeRef, self.epsilonDistance, "elevation deviation")

        # Rates
        self.validate.assert_equals_with_relative_tolerance(XangleRate, XangleRateNReg, self.epsilonNonReg,
            XangleRateRef, self.epsilonAngVelocity, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(YangleRate, YangleRateNReg, self.epsilonNonReg,
            YangleRateRef, self.epsilonAngVelocity, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(rangeRate, rangeRateNReg, self.epsilonNonReg,
            rangeRateRef, self.epsilonVelocity, "elevation deviation")

        Xangle = topoNorth.getXangleCardan(position, topoNorth, self.date)
        Yangle = topoNorth.getYangleCardan(position, topoNorth, self.date)
        XangleRate = topoNorth.getXangleCardanRate(pv, topoNorth, self.date)
        YangleRate = topoNorth.getYangleCardanRate(pv, topoNorth, self.date)

        # Rates
        self.validate.assert_equals_with_relative_tolerance(Xangle, XangleNReg1, self.epsilonNonReg,
            XangleRef, self.epsilonAngle, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(Yangle, YangleNReg1, self.epsilonNonReg,
            YangleRef, self.epsilonAngle, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(XangleRate, XangleRateNReg1, self.epsilonNonReg,
            XangleRateRef, self.epsilonAngVelocity, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(YangleRate, YangleRateNReg1, self.epsilonNonReg,
            YangleRateRef, self.epsilonAngVelocity, "elevation deviation")

    
    def testTransformationCardantoPV(self) :

        # Reference Inputs
        Xangle = -1.076854957875316
        Yangle = 0.9348634533745954
        range = 124.29802894656054
        XangleRate = -0.4091743119266047
        YangleRate = -0.6368236827766715
        rangeRate = 29.84761730690871

        # Reference outputs
        XRef = 99.99999999999996
        YRef = 65.00000000000007
        ZRef = 35.0
        XRateRef = -23.00000000000006
        YRateRef = 85.99999999999999
        ZRateRef = 12.0

        # Non regression
        XNReg = 99.99999999999996
        YNReg = 65.00000000000007
        ZNReg = 34.999999999999986
        XRateNReg = -23.000000000000068
        YRateNReg = 86.00000000000001
        ZRateNReg = 11.999999999999995

         #
         # TEST
         # 

        # North topocentric frame
        point = EllipsoidPoint(self.earthSpheric, self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(43.604482), MathLib.toRadians(1.443962), 0., "")
        topoNorth = TopocentricFrame(point, 0., self.northFrame)

        # Cartesian coordinates expressed in the North topocentric frame
        cPV = CardanMountPV(Xangle, Yangle, range, XangleRate, YangleRate, rangeRate)

        # Conversion from Cartesian coordinates (position and velocity) to topocentric coordinates
        CoordPV = topoNorth.transformFromCardanToPV(cPV)

        # Computed results
        myPosition = CoordPV.getPosition()
        myVelocity = CoordPV.getVelocity()
        x = myPosition.getX()
        y = myPosition.getY()
        z = myPosition.getZ()
        xd = myVelocity.getX()
        yd = myVelocity.getY()
        zd = myVelocity.getZ()

        # Values
        self.validate.assert_equals_with_relative_tolerance(x, XNReg, self.epsilonNonReg,
            XRef, self.epsilonDistance, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(y, YNReg, self.epsilonNonReg,
            YRef, self.epsilonDistance, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(z, ZNReg, self.epsilonNonReg,
            ZRef, self.epsilonDistance, "elevation deviation")

        # Rates
        self.validate.assert_equals_with_relative_tolerance(xd, XRateNReg, self.epsilonNonReg,
            XRateRef, self.epsilonVelocity, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(yd, YRateNReg, self.epsilonNonReg,
            YRateRef, self.epsilonVelocity, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(zd, ZRateNReg, self.epsilonNonReg,
            ZRateRef, self.epsilonVelocity, "elevation deviation")

    
    def testTransformationPVToCardan(self) :

        # Reference Inputs
        XRef = 100
        YRef = 50
        ZRef = 0
        XRateRef = -23
        YRateRef = -86
        ZRateRef = 12

        # Reference Outputs
        XangleRef = -FastMath.PI / 2
        YangleRef = 1.1071487177940904
        rangeRef = 111.80339887498948
        XangleRateRef = 0.24
        YangleRateRef = 0.596
        rangeRateRef = -59.03219460599445

        # Non regression
        XangleNReg = -1.5707963267948966
        YangleNReg = 1.1071487177940906
        rangeNReg = 111.80339887498948
        XangleRateNReg = 0.24
        YangleRateNReg = 0.596
        rangeRateNReg = -59.03219460599445

         #
         # TEST
         # 

        # North topocentric frame
        point = EllipsoidPoint(self.earthSpheric, self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(43.604482), MathLib.toRadians(1.443962), 0., "")
        topoNor = TopocentricFrame(point, 0., self.northFrame)

        # Cartesian coordinates expressed in the North topocentric frame
        position = Vector3D(XRef, YRef, ZRef)
        velocity = Vector3D(XRateRef, YRateRef, ZRateRef)
        cPV = PVCoordinates(position, velocity)

        # Conversion from Cartesian coordinates (position and velocity) to topocentric coordinates
        cardanCoordPV = topoNor.transformFromPVToCardan(cPV, topoNor, self.date)

        # Computed results
        Xangle = cardanCoordPV.getXangle()
        Yangle = cardanCoordPV.getYangle()
        range = cardanCoordPV.getRange()
        XangleRate = cardanCoordPV.getXangleRate()
        YangleRate = cardanCoordPV.getYangleRate()
        rangeRate = cardanCoordPV.getRangeRate()

        # Values
        self.validate.assert_equals_with_relative_tolerance(Xangle, XangleNReg, self.epsilonNonReg,
            XangleRef, self.epsilonAngle, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(Yangle, YangleNReg, self.epsilonNonReg,
            YangleRef, self.epsilonAngle, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(range, rangeNReg, self.epsilonNonReg,
            rangeRef, self.epsilonDistance, "elevation deviation")

        # Rates
        self.validate.assert_equals_with_relative_tolerance(XangleRate, XangleRateNReg, self.epsilonNonReg,
            XangleRateRef, self.epsilonAngVelocity, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(YangleRate, YangleRateNReg, self.epsilonNonReg,
            YangleRateRef, self.epsilonAngVelocity, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(rangeRate, rangeRateNReg, self.epsilonNonReg,
            rangeRateRef, self.epsilonVelocity, "elevation deviation")


    def testTransformationPositionToCardan(self) :

        # Reference Inputs
        XRef = 100
        YRef = -65
        ZRef = 35
        XRateRef = -23
        YRateRef = -86
        ZRateRef = 12

        # Reference Outputs
        XangleRef = 1.076854957875316
        YangleRef = 0.9348634533745954
        rangeRef = 124.29802894656054
        XangleRateRef = 0.4091743119266047
        YangleRateRef = -0.6368236827766715
        rangeRateRef = 29.84761730690871

        # Non regression
        XangleNReg = 1.0768549578753155
        YangleNReg = 0.9348634533745958
        rangeNReg = 124.29802894656054
        XangleRateNReg = 0.4091743119266055
        YangleRateNReg = -0.6368236827766712
        rangeRateNReg = 29.84761730690871

        # North topocentric frame
        point = EllipsoidPoint(self.earthSpheric, self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(43.604482), MathLib.toRadians(1.443962), 0., "")
        topoNorth = TopocentricFrame(point, 0., self.northFrame)

        # Cartesian coordinates expressed in the North topocentric frame
        pos = Vector3D(XRef, YRef, ZRef)
        vel = Vector3D(XRateRef, YRateRef, ZRateRef)
        pv = PVCoordinates(pos, vel)

        # Conversion from Cartesian coordinates (position and velocity) to topocentric coordinates
        cardanCoordPV = topoNorth.transformFromPVToCardan(pv, topoNorth, self.date)

        # Computed results
        Xangle = cardanCoordPV.getXangle()
        Yangle = cardanCoordPV.getYangle()
        range = cardanCoordPV.getRange()
        XangleRate = cardanCoordPV.getXangleRate()
        YangleRate = cardanCoordPV.getYangleRate()
        rangeRate = cardanCoordPV.getRangeRate()

        # Values
        self.validate.assert_equals_with_relative_tolerance(Xangle, XangleNReg, self.epsilonNonReg,
            XangleRef, self.epsilonAngle, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(Yangle, YangleNReg, self.epsilonNonReg,
            YangleRef, self.epsilonAngle, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(range, rangeNReg, self.epsilonNonReg,
            rangeRef, self.epsilonDistance, "elevation deviation")

        # Rates
        self.validate.assert_equals_with_relative_tolerance(XangleRate, XangleRateNReg, self.epsilonNonReg,
            XangleRateRef, self.epsilonAngVelocity, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(YangleRate, YangleRateNReg, self.epsilonNonReg,
            YangleRateRef, self.epsilonAngVelocity, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(rangeRate, rangeRateNReg, self.epsilonNonReg,
            rangeRateRef, self.epsilonVelocity, "elevation deviation")

    
    def testTransformationCardanToPosition(self) :

        # Reference Inputs
        Xangle = -1.076854957875316
        Yangle = 0.9348634533745954
        range = 124.29802894656054
        XangleRate = -0.4091743119266047
        YangleRate = -0.6368236827766715
        rangeRate = 29.84761730690871

        # Reference outputs
        XRef = 99.99999999999996
        YRef = 65.00000000000007
        ZRef = 35.0
        XRateRef = -23.00000000000006
        YRateRef = 85.99999999999999
        ZRateRef = 12.0

         #
         # TEST
         # 

        # North topocentric frame
        point = EllipsoidPoint(self.earthSpheric, self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(43.604482), MathLib.toRadians(1.443962), 0., "")
        topoNorth = TopocentricFrame(point, 0., self.northFrame)

        # Cartesian coordinates expressed in the North topocentric frame
        cPV = CardanMountPV(Xangle, Yangle, range, XangleRate, YangleRate, rangeRate)

        # Conversion from Cartesian coordinates (position and velocity) to topocentric coordinates
        CoordPV = topoNorth.transformFromCardanToPV(cPV)

        # Computed results
        myPosition = CoordPV.getPosition()
        myVelocity = CoordPV.getVelocity()
        x = myPosition.getX()
        y = myPosition.getY()
        z = myPosition.getZ()
        xd = myVelocity.getX()
        yd = myVelocity.getY()
        zd = myVelocity.getZ()

        # Values
        self.validate.assert_equals_with_relative_tolerance(x, XRef, self.epsilonNonReg,
            XRef, self.epsilonDistance, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(y, YRef, self.epsilonNonReg,
            YRef, self.epsilonDistance, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(z, ZRef, self.epsilonNonReg,
            ZRef, self.epsilonDistance, "elevation deviation")

        # Rates
        self.validate.assert_equals_with_relative_tolerance(xd, XRateRef, self.epsilonNonReg,
            XRateRef, self.epsilonVelocity, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(yd, YRateRef, self.epsilonNonReg,
            YRateRef, self.epsilonVelocity, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(zd, ZRateRef, self.epsilonNonReg,
            ZRateRef, self.epsilonVelocity, "elevation deviation")


    def testTransformationPositionToCardanDegrade(self) :

        # Reference Inputs
        XRef = 100
        YRef = 50
        ZRef = 0

        # Reference Outputs
        XangleRef = -FastMath.PI / 2
        YangleRef = 1.1071487177940904
        rangeRef = 111.80339887498948

        # Non regression
        XangleNReg = -1.5707963267948966
        YangleNReg = 1.1071487177940906
        rangeNReg = 111.80339887498948

         #
         # TEST
         # 

        # North topocentric frame
        point = EllipsoidPoint(self.earthSpheric, self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(43.604482), MathLib.toRadians(1.443962), 0., "")
        topoNorth = TopocentricFrame(point, 0., self.northFrame)

        # Cartesian coordinates expressed in the North topocentric frame
        position = Vector3D(XRef, YRef, ZRef)

        # Conversion from Cartesian coordinates (position and velocity) to topocentric coordinates
        cardanCoordPV = topoNorth.transformFromPositionToCardan(position, topoNorth, self.date)

        # Computed results
        Xangle = cardanCoordPV.getXangle()
        Yangle = cardanCoordPV.getYangle()
        range = cardanCoordPV.getRange()

        # Values
        self.validate.assert_equals_with_relative_tolerance(Xangle, XangleNReg, self.epsilonNonReg,
            XangleRef, self.epsilonAngle, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(Yangle, YangleNReg, self.epsilonNonReg,
            YangleRef, self.epsilonAngle, "elevation deviation")
        self.validate.assert_equals_with_relative_tolerance(range, rangeNReg, self.epsilonNonReg,
            rangeRef, self.epsilonDistance, "elevation deviation")

    
    def testDelevation(self) :

        # Surface point at latitude 0°, longitude 0°
        groundPoint = EllipsoidPoint(self.earthSpheric,
            self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(0.), MathLib.toRadians(0.), 0., "")
        topoFrame = TopocentricFrame(groundPoint,
            "lon 0 lat 0")
        itrf = self.earthSpheric.getBodyFrame()

        # Determine the offset in [m]
        hElev = 1

        # Case #1: Target point express in the earthSpheric's frame (itrf)
        targetPoint = EllipsoidPoint(self.earthSpheric,
            self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(5.), MathLib.toRadians(5.), 800_000., "")
        extPoint = targetPoint.getPosition()

        # Build the offset target points
        extPointPlusHX = extPoint.add(Vector3D(+hElev, 0., 0.))
        extPointMinusHX = extPoint.add(Vector3D(-hElev, 0., 0.))

        extPointPlusHY = extPoint.add(Vector3D(0., +hElev, 0.))
        extPointMinusHY = extPoint.add(Vector3D(0., -hElev, 0.))

        extPointPlusHZ = extPoint.add(Vector3D(0., 0., +hElev))
        extPointMinusHZ = extPoint.add(Vector3D(0., 0., -hElev))

        # Compute the offset target points elevations
        elevPlusHX = topoFrame.getElevation(extPointPlusHX, itrf, self.date)
        elevMinusHX = topoFrame.getElevation(extPointMinusHX, itrf, self.date)

        elevPlusHY = topoFrame.getElevation(extPointPlusHY, itrf, self.date)
        elevMinusHY = topoFrame.getElevation(extPointMinusHY, itrf, self.date)

        elevPlusHZ = topoFrame.getElevation(extPointPlusHZ, itrf, self.date)
        elevMinusHZ = topoFrame.getElevation(extPointMinusHZ, itrf, self.date)

        # Compute the numerical values
        numValX = (elevPlusHX - elevMinusHX) / (2. * hElev)
        numValY = (elevPlusHY - elevMinusHY) / (2. * hElev)
        numValZ = (elevPlusHZ - elevMinusHZ) / (2. * hElev)

        # Compute the derivatives elevation vector
        dElev = topoFrame.getDElevation(extPoint, itrf, self.date)

        # Non regression evaluation
        validityThreshold = 1e-16

        assert math.isclose(6.61205847907187E-7, numValX, abs_tol=validityThreshold)
        assert math.isclose(-3.9393839385004625E-7, numValY, abs_tol=validityThreshold)
        assert math.isclose(-3.95443174650012E-7, numValZ, abs_tol=validityThreshold)

        assert math.isclose(6.6120584785882E-7, dElev.getX(), abs_tol=validityThreshold)
        assert math.isclose(-3.939383939701935E-7, dElev.getY(), abs_tol=validityThreshold)
        assert math.isclose(-3.9544317463724705E-7, dElev.getZ(), abs_tol=validityThreshold)

        # ---------------------------------------------------------------

        # Case #2: Target point express in the topocentric frame

        # Compute the offset target points elevations
        elevPlusHX = topoFrame.getElevation(extPointPlusHX, topoFrame, self.date)
        elevMinusHX = topoFrame.getElevation(extPointMinusHX, topoFrame, self.date)

        elevPlusHY = topoFrame.getElevation(extPointPlusHY, topoFrame, self.date)
        elevMinusHY = topoFrame.getElevation(extPointMinusHY, topoFrame, self.date)

        elevPlusHZ = topoFrame.getElevation(extPointPlusHZ, topoFrame, self.date)
        elevMinusHZ = topoFrame.getElevation(extPointMinusHZ, topoFrame, self.date)

        # Compute the numerical values
        numValX = (elevPlusHX - elevMinusHX) / (2. * hElev)
        numValY = (elevPlusHY - elevMinusHY) / (2. * hElev)
        numValZ = (elevPlusHZ - elevMinusHZ) / (2. * hElev)

        # Compute the derivatives elevation vector
        dElev = topoFrame.getDElevation(extPoint, topoFrame, self.date)

        # Non regression evaluation
        assert math.isclose(-1.209563085311771E-8, numValX, abs_tol=validityThreshold)
        assert math.isclose(-1.0582305778422006E-9, numValY, abs_tol=validityThreshold)
        assert math.isclose(1.387817999341497E-7, numValZ, abs_tol=validityThreshold)

        assert math.isclose(-1.2095630851083339E-8, dElev.getX(), abs_tol=validityThreshold)
        assert math.isclose(-1.0582305726147823E-9, dElev.getY(), abs_tol=validityThreshold)
        assert math.isclose(1.3878179993404016E-7, dElev.getZ(), abs_tol=validityThreshold)

    
    def testDazimuth(self) :

        # Surface point at latitude 0°, longitude 0°
        groundPoint = EllipsoidPoint(self.earthSpheric,
            self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(0.), MathLib.toRadians(0.), 0., "")
        topoFrame = TopocentricFrame(groundPoint,
            "lon 0 lat 0")
        itrf = self.earthSpheric.getBodyFrame()

        # Determine the offset in [m]
        hAzim = 1

        # Case #1: Target point express in the earthSpheric's frame (itrf)
        targetPoint = EllipsoidPoint(self.earthSpheric,
            self.earthSpheric.getLLHCoordinatesSystem(),
            MathLib.toRadians(5.), MathLib.toRadians(5.), 800_000., "")
        extPoint = targetPoint.getPosition()

        # Build the offset target points
        extPointPlusHX = extPoint.add(Vector3D(+hAzim, 0., 0.))
        extPointMinusHX = extPoint.add(Vector3D(-hAzim, 0., 0.))

        extPointPlusHY = extPoint.add(Vector3D(0., +hAzim, 0.))
        extPointMinusHY = extPoint.add(Vector3D(0., -hAzim, 0.))

        extPointPlusHZ = extPoint.add(Vector3D(0., 0., +hAzim))
        extPointMinusHZ = extPoint.add(Vector3D(0., 0., -hAzim))

        # Compute the offset target points azimuths
        azimPlusHX = topoFrame.getAzimuth(extPointPlusHX, itrf, self.date)
        azimMinusHX = topoFrame.getAzimuth(extPointMinusHX, itrf, self.date)

        azimPlusHY = topoFrame.getAzimuth(extPointPlusHY, itrf, self.date)
        azimMinusHY = topoFrame.getAzimuth(extPointMinusHY, itrf, self.date)

        azimPlusHZ = topoFrame.getAzimuth(extPointPlusHZ, itrf, self.date)
        azimMinusHZ = topoFrame.getAzimuth(extPointMinusHZ, itrf, self.date)

        # Compute the numerical values
        numValX = (azimPlusHX - azimMinusHX) / (2. * hAzim)
        numValY = (azimPlusHY - azimMinusHY) / (2. * hAzim)
        numValZ = (azimPlusHZ - azimMinusHZ) / (2. * hAzim)

        # Compute the derivatives azimuth vector
        dAzim = topoFrame.getDAzimuth(extPoint, itrf, self.date)

        # Non regression evaluation
        validityThreshold = 1e-16

        assert math.isclose(0.0, numValX, abs_tol=validityThreshold)
        assert math.isclose(8.022595644474606E-7, numValY, abs_tol=validityThreshold)
        assert math.isclose(-7.992067245776724E-7, numValZ, abs_tol=validityThreshold)

        assert math.isclose(0.0, dAzim.getX(), abs_tol=validityThreshold)
        assert math.isclose(8.022595644210772E-7, dAzim.getY(), abs_tol=validityThreshold)
        assert math.isclose(-7.9920672456967E-7, dAzim.getZ(), abs_tol=validityThreshold)

        # ---------------------------------------------------------------

        # Case #2: Target point express in the topocentric frame

        # Build the offset target points
        extPointPlusHX = extPoint.add(Vector3D(+hAzim, 0., 0.))
        extPointMinusHX = extPoint.add(Vector3D(-hAzim, 0., 0.))

        extPointPlusHY = extPoint.add(Vector3D(0., +hAzim, 0.))
        extPointMinusHY = extPoint.add(Vector3D(0., -hAzim, 0.))

        extPointPlusHZ = extPoint.add(Vector3D(0., 0., +hAzim))
        extPointMinusHZ = extPoint.add(Vector3D(0., 0., -hAzim))

        # Compute the offset target points azimuths
        azimPlusHX = topoFrame.getAzimuth(extPointPlusHX, topoFrame, self.date)
        azimMinusHX = topoFrame.getAzimuth(extPointMinusHX, topoFrame, self.date)

        azimPlusHY = topoFrame.getAzimuth(extPointPlusHY, topoFrame, self.date)
        azimMinusHY = topoFrame.getAzimuth(extPointMinusHY, topoFrame, self.date)

        azimPlusHZ = topoFrame.getAzimuth(extPointPlusHZ, topoFrame, self.date)
        azimMinusHZ = topoFrame.getAzimuth(extPointMinusHZ, topoFrame, self.date)

        # Compute the numerical values
        numValX = (azimPlusHX - azimMinusHX) / (2. * hAzim)
        numValY = (azimPlusHY - azimMinusHY) / (2. * hAzim)
        numValZ = (azimPlusHZ - azimMinusHZ) / (2. * hAzim)

        # Compute the derivatives azimuth vector
        dAzim = topoFrame.getDAzimuth(extPoint, topoFrame, self.date)

        # Non regression evaluation
        assert math.isclose(1.2188214032075394E-8, numValX, abs_tol=validityThreshold)
        assert math.isclose(-1.3931192386387147E-7, numValY, abs_tol=validityThreshold)
        assert math.isclose(0., numValZ, abs_tol=validityThreshold)

        assert math.isclose(1.2188213993624686E-8, dAzim.getX(), abs_tol=validityThreshold)
        assert math.isclose(-1.39311923885721E-7, dAzim.getY(), abs_tol=validityThreshold)
        assert math.isclose(0., dAzim.getZ(), abs_tol=validityThreshold)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTopocentricFrame)
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
