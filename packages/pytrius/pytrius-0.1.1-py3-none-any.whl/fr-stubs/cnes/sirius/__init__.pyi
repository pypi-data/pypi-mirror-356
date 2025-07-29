
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.addons
import fr.cnes.sirius.patrius
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius")``.

    addons: fr.cnes.sirius.addons.__module_protocol__
    patrius: fr.cnes.sirius.patrius.__module_protocol__
