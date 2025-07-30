
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis.integration.sphere.lebedev
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.analysis.integration.sphere")``.

    lebedev: fr.cnes.sirius.patrius.math.analysis.integration.sphere.lebedev.__module_protocol__
