
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.optim.joptimizer.algebra
import fr.cnes.sirius.patrius.math.optim.joptimizer.functions
import fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers
import fr.cnes.sirius.patrius.math.optim.joptimizer.solvers
import fr.cnes.sirius.patrius.math.optim.joptimizer.util
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.optim.joptimizer")``.

    algebra: fr.cnes.sirius.patrius.math.optim.joptimizer.algebra.__module_protocol__
    functions: fr.cnes.sirius.patrius.math.optim.joptimizer.functions.__module_protocol__
    optimizers: fr.cnes.sirius.patrius.math.optim.joptimizer.optimizers.__module_protocol__
    solvers: fr.cnes.sirius.patrius.math.optim.joptimizer.solvers.__module_protocol__
    util: fr.cnes.sirius.patrius.math.optim.joptimizer.util.__module_protocol__
