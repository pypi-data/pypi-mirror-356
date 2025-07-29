
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.tools.cache
import fr.cnes.sirius.patrius.tools.parallel
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.tools")``.

    cache: fr.cnes.sirius.patrius.tools.cache.__module_protocol__
    parallel: fr.cnes.sirius.patrius.tools.parallel.__module_protocol__
