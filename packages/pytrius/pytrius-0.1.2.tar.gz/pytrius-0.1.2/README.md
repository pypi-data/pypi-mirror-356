The Patrius python wrapper enables to use Patrius within a Python environment. This is done by creating a wrapper around the java library.
This version of the wrapper wraps **Patrius v4.16 in JAVA**.

# Installation

* Requirements:
  * JDK installed on your system (as pytrius is Java based)
  * Python >= 3.6
  * `pip`

To install from PyPI:
```bash
pip install pytrius
```

To install from source:
```bash
git clone git@gitlab.cnes.fr:patrius/internal/pytrius.git
or
git clone https://gitlab.cnes.fr/patrius/internal/pytrius.git
```

Followed by: 

```bash
mvn clean install
pip install -e .
```

# Usage

You will find examples of how to use pytrius in the `examples` and `test` folders. The examples given are heavily inspired from the already existing [Patrius Tutorial GitHub page](https://github.com/CNES/patrius-tutorials/tree/main) in java (but obviously translated to python in this case). 

```python
import pytrius
pytrius.initVM(jvmpath="path\\to\\jvm.dll")

from fr.cnes.sirius.addons.patriusdataset import PatriusDataset

from fr.cnes.sirius.patrius.frames import FramesFactory
from fr.cnes.sirius.patrius.time import AbsoluteDate, TimeScalesFactory

if __name__ == '__main__':
    # do stuff
```