import os 

from fr.cnes.sirius.patrius.frames.configuration import DiurnalRotation,  FramesConfigurationBuilder,  PolarMotion, FramesConfigurationFactory
from fr.cnes.sirius.patrius.frames.configuration.eop import NoEOP2000History, EOPHistoryFactory, EOPInterpolators
from fr.cnes.sirius.patrius.frames.configuration.libration import LibrationCorrectionModelFactory
from fr.cnes.sirius.patrius.frames.configuration.precessionnutation import PrecessionNutation, PrecessionNutationModelFactory
from fr.cnes.sirius.patrius.frames.configuration.sp import SPrimeModelFactory
from fr.cnes.sirius.patrius.frames.configuration.tides import TidalCorrectionModelFactory


class Utils ():

    # epsilon for tests
    epsilonTest = 1.e-12

    # epsilon for eccentricity
    epsilonE = 1.e+5 * epsilonTest

    # epsilon for circular eccentricity
    epsilonEcir = 1.e+8 * epsilonTest

    # epsilon for angles
    epsilonAngle = 1.e+5 * epsilonTest

    ae = 6378136.460
    mu = 3.986004415e+14
    
    def get_iers2003_configuration_woeop(ignore_tides: bool):
        # Configurations builder
        builder = FramesConfigurationBuilder()

        # Tides and libration
        tides = TidalCorrectionModelFactory.NO_TIDE if ignore_tides else TidalCorrectionModelFactory.TIDE_IERS2003_INTERPOLATED
        lib = LibrationCorrectionModelFactory.NO_LIBRATION

        # Polar Motion
        default_polar_motion = PolarMotion(False, tides, lib, SPrimeModelFactory.SP_IERS2003)

        # Diurnal rotation
        default_diurnal_rotation = DiurnalRotation(tides, lib)

        # Precession Nutation
        prec_nut = PrecessionNutation(False, PrecessionNutationModelFactory.PN_IERS2003_INTERPOLATED)

        # Setting the configurations in the builder
        builder.setDiurnalRotation(default_diurnal_rotation)
        builder.setPolarMotion(default_polar_motion)
        builder.setCIRFPrecessionNutation(prec_nut)
        builder.setEOPHistory(NoEOP2000History())

        return builder.getConfiguration()
    
    def get_IERS2003_configuration(ignore_tides):
        # Assume this method returns a FramesConfiguration object
        iers2003 = FramesConfigurationFactory.getIERS2003Configuration(ignore_tides)
        
        # Create a FramesConfigurationBuilder from the returned configuration
        fb = FramesConfigurationBuilder(iers2003)
        
        # Modify EOP history to use LAGRANGE 4 interpolation
        eop_history = EOPHistoryFactory.getEOP2000History(EOPInterpolators.LAGRANGE4)
        fb.setEOPHistory(eop_history)
        
        # Return the modified configuration
        return fb.getConfiguration()