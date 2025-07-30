
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.files.general
import fr.cnes.sirius.patrius.files.sp3
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.files")``.

    general: fr.cnes.sirius.patrius.files.general.__module_protocol__
    sp3: fr.cnes.sirius.patrius.files.sp3.__module_protocol__
