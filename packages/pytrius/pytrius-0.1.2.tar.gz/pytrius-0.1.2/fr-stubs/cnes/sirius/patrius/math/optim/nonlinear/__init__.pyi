
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.optim.nonlinear.scalar
import fr.cnes.sirius.patrius.math.optim.nonlinear.vector
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.nonlinear")``.

    scalar: fr.cnes.sirius.patrius.math.optim.nonlinear.scalar.__module_protocol__
    vector: fr.cnes.sirius.patrius.math.optim.nonlinear.vector.__module_protocol__
