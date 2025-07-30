import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytrius

pytrius.initVM()

from fr.cnes.sirius.patrius.assembly import AssemblyBuilder
from fr.cnes.sirius.patrius.assembly.models import MassModel
from fr.cnes.sirius.patrius.assembly.properties import MassProperty
from fr.cnes.sirius.patrius.frames.transformations import Transform

# Using an assembly builder
builder = AssemblyBuilder()

# Main part (for example dry mass)
dry_mass = 1000.0
builder.addMainPart("MAIN")
builder.addProperty(MassProperty(dry_mass), "MAIN")

# SPECIFIC
# Tank part (ergols mass); considering centered vs the main part
ergols_mass = 100.0
builder.addPart("TANK", "MAIN", Transform.IDENTITY)
builder.addProperty(MassProperty(ergols_mass), "TANK")
# SPECIFIC

# Getting the corresponding assembly
assembly = builder.returnAssembly()

# Getting the corresponding mass model (useful for propagation, maneuvres, ...)
mm = MassModel(assembly)

# Output part names and masses
for i, name in enumerate(mm.getAllPartsNames()):
    print(f"Part #{i}")
    print(f"  Name: {name}")
    print(f"  Mass: {mm.getMass(name)}")

print("\nTotal mass:", mm.getTotalMass())