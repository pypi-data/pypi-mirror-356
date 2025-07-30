import unittest
import math
import sys
import os

from jpype import JImplements, JOverride

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.patrius.attitudes import Attitude, AttitudeLawLeg, BodyCenterPointing, ConstantSpinSlew, FixedRate, LofOffset, StrictAttitudeLegsSequence
from fr.cnes.sirius.patrius.frames import FramesFactory, LOFType
from fr.cnes.sirius.patrius.math.complex import Quaternion
from fr.cnes.sirius.patrius.math.geometry.euclidean.threed import Rotation, RotationOrder, Vector3D
from fr.cnes.sirius.patrius.math.util import MathLib, Precision
from fr.cnes.sirius.patrius.orbits import CircularOrbit, KeplerianOrbit, PositionAngle
from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.patrius.utils import Constants


class TestConstantSpinSlew(unittest.TestCase):

    # Epsilon comparison */
    EPS = Precision.DOUBLE_COMPARISON_EPSILON


    def test_SimpleCase(self) :

        # reference date
        refDate = AbsoluteDate(2012, 2, 10, TimeScalesFactory.getTAI())
        # reference frame
        refFrame = FramesFactory.getEME2000()

        # initial attitude
        qInitial = Quaternion(0, 1, 0, 0)
        attInitial = Attitude(refDate, refFrame,
            Rotation(False, qInitial), Vector3D.ZERO)
        iLaw = FixedRate(attInitial)

        # attitude
        qFinal = Quaternion(0, 0, 1, 0)
        attFinal = Attitude(refDate.shiftedBy(60.), refFrame, Rotation(False,
            qFinal), Vector3D.ZERO)
        fLaw = FixedRate(attFinal)
        
        # Satellite position
        mu = Constants.EGM96_EARTH_MU
        circOrbit = CircularOrbit(7178000.0, 0.5e-4, -0.5e-4, MathLib.toRadians(50.),
                MathLib.toRadians(270.), MathLib.toRadians(5.300), PositionAngle.MEAN, FramesFactory.getEME2000(),
                refDate, mu)

        # Slew
        slerp = ConstantSpinSlew(iLaw.getAttitude(circOrbit, refDate, refFrame), fLaw.getAttitude(circOrbit, refDate.shiftedBy(60), refFrame))

        # first intermediate rotation of 30°
        intermediateRot = slerp.getAttitude(refDate.shiftedBy(20.), refFrame).getRotation().getQuaternion()
        intermediateRefRot = Quaternion(0, MathLib.sqrt(3) / 2., -1 / 2., 0)
        isEqual = intermediateRefRot.equals(intermediateRot, self.EPS)

        self.assertTrue(isEqual)

        # second intermediate rotation of 30°
        intermediateRot = slerp.getAttitude(refDate.shiftedBy(40.), refFrame).getRotation().getQuaternion()
        intermediateRefRot = Quaternion(0, 1 / 2., -MathLib.sqrt(3) / 2., 0)
        isEqual = intermediateRefRot.equals(intermediateRot, self.EPS)

        self.assertTrue(isEqual)

        # third and last intermediate rotation of 30°
        intermediateRot = slerp.getAttitude(refDate.shiftedBy(60.), refFrame).getRotation().getQuaternion()
        intermediateRefRot = Quaternion(0, 0, 1, 0)
        isEqual = intermediateRefRot.equals(intermediateRot, self.EPS)

        self.assertTrue(isEqual)
    

    def testGeneralCase(self) :

        q0 = Quaternion(0.25, -MathLib.sqrt(3) / 4, 0, MathLib.sqrt(3) / 2)
        q1 = Quaternion(-MathLib.sqrt(3) / 8, (3 + 2 * MathLib.sqrt(3)) / 8, 0.125, (MathLib.sqrt(3) - 6) / 8)

        r0 = Rotation(False, q0)
        r1 = Rotation(False, q1)

        # reference date
        refDate = AbsoluteDate(2012, 2, 10, TimeScalesFactory.getTAI())
        # refernece frame
        refFrame = FramesFactory.getEME2000()

        # initial attitude
        attInitial = Attitude(refDate, refFrame,
            r0, Vector3D.ZERO)
        iLaw = FixedRate(attInitial)

        # attitude
        attFinal = Attitude(refDate.shiftedBy(120.), refFrame, r1, Vector3D.ZERO)
        fLaw = FixedRate(attFinal)

        # maneuver profile
        slerp = ConstantSpinSlew(attInitial, attFinal)

        r = r0.applyInverseTo(r1)

        # Satellite position
        mu = Constants.EGM96_EARTH_MU
        circOrbit = CircularOrbit(7178000.0, 0.5e-4, -0.5e-4, MathLib.toRadians(50.),
            MathLib.toRadians(270.), MathLib.toRadians(5.300), PositionAngle.MEAN, FramesFactory.getEME2000(),
            refDate, mu)

        #
         # first intermediate rotation of 30°
         #/
        # computed quaternion
        intermediateRot = slerp.getAttitude(circOrbit, refDate.shiftedBy(24.), refFrame).getRotation().getQuaternion()

        # reference quaternion
        t = .2
        intermediateRefRot = r0.applyTo(Rotation(r.getAxis(), r.getAngle() * t)).getQuaternion()
        isEqual = intermediateRefRot.equals(intermediateRot, self.EPS)

        # assertion
        self.assertTrue(isEqual)

        #
         # second intermediate rotation of 60°
         #/
        # computed quaternion
        intermediateRot = slerp.getAttitude(circOrbit, refDate.shiftedBy(48.), refFrame).getRotation().getQuaternion()

        # reference quaternion
        t = .4
        intermediateRefRot = r0.applyTo(Rotation(r.getAxis(), r.getAngle() * t)).getQuaternion()
        isEqual = intermediateRefRot.equals(intermediateRot, self.EPS)

        # assertion
        self.assertTrue(isEqual)

        #
         # third intermediate rotation of 90°
         #/
        # computed quaternion
        intermediateRot = slerp.getAttitude(circOrbit, refDate.shiftedBy(72.), refFrame).getRotation().getQuaternion()

        # reference quaternion
        t = .6
        intermediateRefRot = r0.applyTo(Rotation(r.getAxis(), r.getAngle() * t)).getQuaternion()
        isEqual = intermediateRefRot.equals(intermediateRot, self.EPS)

        # assertion
        self.assertTrue(isEqual)

        #
         # fourth intermediate rotation of 120°
         #/
        # computed quaternion
        intermediateRot = slerp.getAttitude(circOrbit, refDate.shiftedBy(96.), refFrame).getRotation().getQuaternion()

        # reference quaternion
        t = .8
        intermediateRefRot = r0.applyTo(Rotation(r.getAxis(), r.getAngle() * t)).getQuaternion()
        isEqual = intermediateRefRot.equals(intermediateRot, self.EPS)

        # assertion
        self.assertTrue(isEqual)

        #
         # fifth intermediate rotation of 145°
         #/
        # computed quaternion
        intermediateRot = slerp.getAttitude(circOrbit, refDate.shiftedBy(145 / 150. * 120), refFrame).getRotation().getQuaternion()

        # reference quaternion
        t = 145 / 150.
        intermediateRefRot = r0.applyTo(Rotation(r.getAxis(), r.getAngle() * t)).getQuaternion()
        isEqual = intermediateRefRot.equals(intermediateRot, self.EPS)

        # assertion
        self.assertTrue(isEqual)
    

    def testSmallAngleCase(self) :

        # reference date
        refDate = AbsoluteDate(2012, 2, 10, TimeScalesFactory.getTAI())
        # refernece frame
        refFrame = FramesFactory.getEME2000()

        # initial attitude
        qInitial = Quaternion(1 / 4., -MathLib.sqrt(3) / 4., 0., MathLib.sqrt(3) / 2.)
        attInitial = Attitude(refDate, refFrame,
            Rotation(False, qInitial), Vector3D.ZERO)
        iLaw = FixedRate(attInitial)

        # attitude
        qFinal = Quaternion(MathLib.sqrt(3) / 8., (-3. + 2 * MathLib.sqrt(3)) / 8., 1. / 8.,
            (MathLib.sqrt(3) + 6) / 8.)
        attFinal = Attitude(refDate.shiftedBy(300.), refFrame, Rotation(False,
            qFinal), Vector3D.ZERO)

        # maneuver profile
        slerp = ConstantSpinSlew(attInitial, attFinal)

        # orbit
        mu = Constants.EGM96_EARTH_MU

        # small angle : 0.1°
        theta = MathLib.toRadians(0.1)
        qRot = Quaternion(MathLib.cos(theta), 0, MathLib.sin(theta), 0)

        # intermediate rotation of 0.1°
        intermediateRot = slerp.getAttitude(refDate.shiftedBy(1.), refFrame).getRotation()
        intermediateRefRot = Rotation(False, Quaternion.multiply(qRot, qInitial))
        isEqual = Rotation.distance(intermediateRefRot, intermediateRot)

        assert math.isclose(0., isEqual, abs_tol=self.EPS)

        # intermediate rotation of 1°
        intermediateRot = slerp.getAttitude(refDate.shiftedBy(10.), refFrame).getRotation()
        intermediateRefQuat = intermediateRefRot.getQuaternion()
        for i in range(1, 10):
            intermediateRefQuat = Quaternion.multiply(qRot, intermediateRefQuat)

        intermediateRefRot = Rotation(False, intermediateRefQuat)
        isEqual = Rotation.distance(intermediateRefRot, intermediateRot)

        assert math.isclose(0., isEqual, abs_tol=self.EPS)


    def testLargeAngleCase(self) :

        # reference date
        refDate = AbsoluteDate(2012, 2, 10, TimeScalesFactory.getTAI())
        # reference frame
        refFrame = FramesFactory.getEME2000()

        # initial attitude
        qInitial = Quaternion(1 / 4., -MathLib.sqrt(3) / 4., 0., MathLib.sqrt(3) / 2.)
        r0 = Rotation(False, qInitial)
        attInitial = Attitude(refDate, refFrame, r0, Vector3D.ZERO)
        iLaw = FixedRate(attInitial)

        # large angle : 179° (near to PI)
        theta = MathLib.toRadians(179)
        qRot = Quaternion(MathLib.cos(theta), 0, MathLib.sin(theta), 0)

        # first intermediate rotation of 0.1°
        qFinal = Quaternion.multiply(qRot, qInitial)
        r1 = Rotation(False, qFinal)
        attFinal = Attitude(refDate.shiftedBy(44.75), refFrame, r1, Vector3D.ZERO)
        fLaw = FixedRate(attFinal)

        # maneuver profile
        slerp = ConstantSpinSlew(attInitial, attFinal)

        # orbit
        mu = Constants.EGM96_EARTH_MU
        circOrbit = CircularOrbit(7178000.0, 0.5e-4, -0.5e-4, MathLib.toRadians(50.),
            MathLib.toRadians(270.), MathLib.toRadians(5.300), PositionAngle.MEAN, FramesFactory.getEME2000(),
            refDate, mu)

        # intermediate rotation of 178°
        intermediateRot = slerp.getAttitude(refDate.shiftedBy(44.5), refFrame).getRotation().getQuaternion()

        # reference
        t = 178 / 179.
        r = r0.applyInverseTo(r1)
        intermediateRefRot = r0.applyTo(Rotation(r.getAxis(), r.getAngle() * t)).getQuaternion()

        isEqual = intermediateRefRot.equals(intermediateRot, self.EPS)

        self.assertTrue(isEqual)


     #
     # Like equals, but managing null.
     # 
    def eqNull(self, a,  b) :
        if (a == None and b == None):
            rez = True
        else :
            if (a == None or b == None):
                rez = False
            else:
                rez = (a == b)
        return rez

     #
     # Like equals, but managing null, for Rotation.
     # 
    def eqNullRot(self, a: Rotation, b: Rotation, threshold) :

        if (a == None and b == None) :
            rez = True
        else :
            if (a == None or b == None) :
                rez = False
            else :
                qa = a.getQuaternion()
                qb = b.getQuaternion()
                eq = qa.equals(qb, threshold)
                rez = eq
            
        return rez

     #
     # Compare instances. Needed because has no custom equals() method.
     # 
    def compareAttitudes(self, expected: Attitude, actual: Attitude, threshold) :

        eqDate = self.eqNull(expected.getDate(), actual.getDate())
        eqRefF = self.eqNull(expected.getReferenceFrame(), actual.getReferenceFrame())
        eqRot = self.eqNullRot(expected.getRotation(), actual.getRotation(), threshold)

        fullEq = eqDate and eqRefF and eqRot

        if not fullEq:
            raise AssertionError("instances differ.")


    def testSequence(self) :
        gcrf = FramesFactory.getGCRF()

        # attitude laws
        law1 = BodyCenterPointing(gcrf)
        law2 = LofOffset(gcrf, LOFType.LVLH, RotationOrder.ZXY, 0, MathLib.toRadians(20), 0)

        # orbit
        date = AbsoluteDate(2012, 3, 7, 12, 2, 0.0, TimeScalesFactory.getTT())
        mu = Constants.EGM96_EARTH_MU
        leo = KeplerianOrbit(7200000, 0.001, MathLib.toRadians(40), 0, 0, 0, PositionAngle.MEAN, gcrf,
            date, mu)

        # constant spin slew
        slerp = ConstantSpinSlew(law1.getAttitude(leo, date.shiftedBy(3 * 3600.), gcrf),
                law2.getAttitude(leo, date.shiftedBy(3 * 3600. + 300.), gcrf))

        # constant spin slew interval of validity (util to create the law legs of the sequence)
        slerpInterval = slerp.getTimeInterval()

        # first law leg
        lawLeg1 = AttitudeLawLeg(law1, date, slerpInterval.getLowerData())

        # second law leg
        lawLeg2 = AttitudeLawLeg(law2, slerpInterval.getUpperData(), slerpInterval.getUpperData()
            .shiftedBy(3600.))

        # attitude laws sequence
        sequence = StrictAttitudeLegsSequence()

        sequence.add(lawLeg1)
        sequence.add(slerp)
        sequence.add(lawLeg2)

        # attitude at the beginning of the constant spin slew
        att1 = law1.getAttitude(leo, slerp.getTimeInterval().getLowerData(), gcrf)
        # attitude at the end of the constant spin slew
        att2 = law2.getAttitude(leo, slerp.getTimeInterval().getUpperData(), gcrf)

        # the attitude at the beginning of the constant spin slew given by the constant spin slew and the first law are
        # equal with an allowed error of 1e-14 due to the computation errors
        self.compareAttitudes(att1, slerp.getAttitude(slerp.getTimeInterval().getLowerData(), gcrf), self.EPS)
        # the attitude at the end of the constant spin slew given by the constant spin slew and the second law are
        # equal with an allowed error of 1e-14 due to the computation errors
        self.compareAttitudes(att2, slerp.getAttitude(slerp.getTimeInterval().getUpperData(), gcrf), self.EPS)

        # the attitude at the beginning of the constant spin slew given by the constant spin slew and the sequence are
        # equal with an allowed error of 1e-14 due to the computation errors
        self.compareAttitudes(slerp.getAttitude(slerp.getTimeInterval().getLowerData(), gcrf),
            sequence.getAttitude(leo, slerp.getTimeInterval().getLowerData(), gcrf), self.EPS)
        # the attitude at the end of the constant spin slew given by the constant spin slew and the sequence are equal
        # with an allowed error of 1e-14 due to the computation errorss
        self.compareAttitudes(slerp.getAttitude(slerp.getTimeInterval().getUpperData(), gcrf),
            sequence.getAttitude(leo, slerp.getTimeInterval().getUpperData(), gcrf), self.EPS)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConstantSpinSlew)
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
