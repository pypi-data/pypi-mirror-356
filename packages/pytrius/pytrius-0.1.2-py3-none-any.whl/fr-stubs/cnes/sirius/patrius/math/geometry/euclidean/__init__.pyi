
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.geometry.euclidean.oned
import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import fr.cnes.sirius.patrius.math.geometry.euclidean.twod
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.geometry.euclidean")``.

    oned: fr.cnes.sirius.patrius.math.geometry.euclidean.oned.__module_protocol__
    threed: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.__module_protocol__
    twod: fr.cnes.sirius.patrius.math.geometry.euclidean.twod.__module_protocol__
