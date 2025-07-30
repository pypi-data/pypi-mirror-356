import types
import typing


import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

import fr
import java


@typing.overload
def JPackage(__package_name: Literal['fr']) -> fr.__module_protocol__: ...


@typing.overload
def JPackage(__package_name: Literal['java']) -> java.__module_protocol__: ...


@typing.overload
def JPackage(__package_name: str) -> types.ModuleType: ...


def JPackage(__package_name) -> types.ModuleType: ...

