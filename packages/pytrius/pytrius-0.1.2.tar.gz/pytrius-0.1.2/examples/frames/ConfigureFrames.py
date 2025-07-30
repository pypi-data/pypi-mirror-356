import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

from fr.cnes.sirius.patrius.frames import FramesFactory
from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory
from fr.cnes.sirius.patrius.frames.configuration import DiurnalRotation, FramesConfigurationBuilder, PolarMotion
from fr.cnes.sirius.patrius.frames.configuration.precessionnutation import PrecessionNutation
from fr.cnes.sirius.patrius.frames.configuration.eop import NoEOP2000History
from fr.cnes.sirius.patrius.frames.configuration.libration import LibrationCorrectionModelFactory
from fr.cnes.sirius.patrius.frames.configuration.precessionnutation import PrecessionNutationModelFactory
from fr.cnes.sirius.patrius.frames.configuration.sp import SPrimeModelFactory
from fr.cnes.sirius.patrius.frames.configuration.tides import TidalCorrectionModelFactory
from fr.cnes.sirius.patrius.math.geometry.euclidean.threed import RotationOrder



# Patrius Dataset initialization (needed for example to get the UTC time)
PatriusDataset.addResourcesFromPatriusDataset()

def print_transform_info(frame1, frame2, date):
    transform = frame1.getTransformTo(frame2, date)
    print("\nPsi: {}".format(transform.getRotation().getAngles(RotationOrder.ZYX)[0]))
    print("Teta: {}".format(transform.getRotation().getAngles(RotationOrder.ZYX)[1]))
    print("Phi: {}".format(transform.getRotation().getAngles(RotationOrder.ZYX)[2]))

def get_simplified_configuration(is_prec_nut):
    # Configurations builder
    builder = FramesConfigurationBuilder()

    # Tides and libration
    tides = TidalCorrectionModelFactory.NO_TIDE
    lib = LibrationCorrectionModelFactory.NO_LIBRATION

    # Polar Motion
    default_polar_motion = PolarMotion(False, tides, lib, SPrimeModelFactory.NO_SP)

    # Diurnal rotation
    default_diurnal_rotation = DiurnalRotation(tides, lib)

    # Precession Nutation
    if is_prec_nut:
        prec_nut = PrecessionNutation(False, PrecessionNutationModelFactory.PN_IERS2010_INTERPOLATED_NON_CONSTANT_OLD)
    else:
        prec_nut = PrecessionNutation(False, PrecessionNutationModelFactory.NO_PN)

    builder.setDiurnalRotation(default_diurnal_rotation)
    builder.setPolarMotion(default_polar_motion)
    builder.setCIRFPrecessionNutation(prec_nut)
    builder.setEOPHistory(NoEOP2000History())

    return builder.getConfiguration()

# Date of the orbit (given in UTC time scale)
TUC = TimeScalesFactory.getUTC()
date = AbsoluteDate("2010-01-01T12:00:00.000", TUC)

# Storing by default configuration
config_default = FramesFactory.getConfiguration()

# First configuration as simple as possible ...
config = get_simplified_configuration(False)
FramesFactory.setConfiguration(config)

# Corresponding GCRF frame
gcrf_no_pn = FramesFactory.getGCRF()
# Corresponding ICRF frame
icrf_no_pn = FramesFactory.getCIRF()

# Printing transform frame information
print_transform_info(gcrf_no_pn, icrf_no_pn, date)

# Second configuration with precession and nutation ...
config = get_simplified_configuration(True)
FramesFactory.setConfiguration(config)

# GCRF frame
gcrf_pn = FramesFactory.getGCRF()
# ICRF frame
icrf_pn = FramesFactory.getCIRF()

# Printing frame information
print_transform_info(gcrf_pn, icrf_pn, date)

# Setting by default configuration
FramesFactory.setConfiguration(config_default)

# GCRF frame
gcrf_def = FramesFactory.getGCRF()
# ICRF frame
icrf_def = FramesFactory.getCIRF()

# Printing frame information
print_transform_info(gcrf_def, icrf_def, date)