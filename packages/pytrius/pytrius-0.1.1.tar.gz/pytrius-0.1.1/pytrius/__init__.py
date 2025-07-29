"""

This script initializes the JVM and imports necessary JPype classes
to work with Java data types and arrays from within Python.

"""

# Imports the Java Virtual Machine (JVM) for interoperability
from .pytrius import initVM 

from jpype import JArray, JDouble

