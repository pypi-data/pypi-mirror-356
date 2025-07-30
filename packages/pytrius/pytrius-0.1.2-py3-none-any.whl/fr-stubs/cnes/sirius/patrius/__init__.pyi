
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.assembly
import fr.cnes.sirius.patrius.attitudes
import fr.cnes.sirius.patrius.bodies
import fr.cnes.sirius.patrius.covariance
import fr.cnes.sirius.patrius.data
import fr.cnes.sirius.patrius.events
import fr.cnes.sirius.patrius.fieldsofview
import fr.cnes.sirius.patrius.files
import fr.cnes.sirius.patrius.forces
import fr.cnes.sirius.patrius.frames
import fr.cnes.sirius.patrius.groundstation
import fr.cnes.sirius.patrius.math
import fr.cnes.sirius.patrius.models
import fr.cnes.sirius.patrius.orbits
import fr.cnes.sirius.patrius.projections
import fr.cnes.sirius.patrius.propagation
import fr.cnes.sirius.patrius.signalpropagation
import fr.cnes.sirius.patrius.stela
import fr.cnes.sirius.patrius.time
import fr.cnes.sirius.patrius.tools
import fr.cnes.sirius.patrius.utils
import fr.cnes.sirius.patrius.wrenches
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius")``.

    assembly: fr.cnes.sirius.patrius.assembly.__module_protocol__
    attitudes: fr.cnes.sirius.patrius.attitudes.__module_protocol__
    bodies: fr.cnes.sirius.patrius.bodies.__module_protocol__
    covariance: fr.cnes.sirius.patrius.covariance.__module_protocol__
    data: fr.cnes.sirius.patrius.data.__module_protocol__
    events: fr.cnes.sirius.patrius.events.__module_protocol__
    fieldsofview: fr.cnes.sirius.patrius.fieldsofview.__module_protocol__
    files: fr.cnes.sirius.patrius.files.__module_protocol__
    forces: fr.cnes.sirius.patrius.forces.__module_protocol__
    frames: fr.cnes.sirius.patrius.frames.__module_protocol__
    groundstation: fr.cnes.sirius.patrius.groundstation.__module_protocol__
    math: fr.cnes.sirius.patrius.math.__module_protocol__
    models: fr.cnes.sirius.patrius.models.__module_protocol__
    orbits: fr.cnes.sirius.patrius.orbits.__module_protocol__
    projections: fr.cnes.sirius.patrius.projections.__module_protocol__
    propagation: fr.cnes.sirius.patrius.propagation.__module_protocol__
    signalpropagation: fr.cnes.sirius.patrius.signalpropagation.__module_protocol__
    stela: fr.cnes.sirius.patrius.stela.__module_protocol__
    time: fr.cnes.sirius.patrius.time.__module_protocol__
    tools: fr.cnes.sirius.patrius.tools.__module_protocol__
    utils: fr.cnes.sirius.patrius.utils.__module_protocol__
    wrenches: fr.cnes.sirius.patrius.wrenches.__module_protocol__
