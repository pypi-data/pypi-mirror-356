"""

This script sets up the initialisation of the JVM 
to work with Java data types and arrays from within Python.

"""

import jpype
import jpype.imports  # This enables direct import of java classes
from typing import List, Union, Optional

import os

# Get the  path of the current file, used for finding the jars directory
dirpath = os.path.dirname(os.path.abspath(__file__))


print(dirpath)
def initVM(vmargs: Union[str, None] = None,
           additional_classpaths: Union[List, None] = None,
           jvmpath: Optional[Union[str, os.PathLike]] = None):
    """
    Initializes the Java Virtual Machine (JVM) for Patrius.

    Args:
        vmargs (Union[str, None], optional): Additional arguments to pass to the JVM. 
        Defaults to None.
             Example for debugging: 
             vmargs='-Xcheck:jni,-verbose:jni,-verbose:class,-XX:+UnlockDiagnosticVMOptions'
        additional_classpaths (Union[List, None], optional): Additional classpaths to 
        add to the JVM. 
        Defaults to None.
        jvmpath (Union[str, os.PathLike], optional): Path to the jvm library file,
            Typically one of (``libjvm.so``, ``jvm.dll``, ...)
            Defaults to None, in this case Jpype will look for a JDK on the system.

    Raises:
        FileNotFoundError: If any of the additional classpaths do not exist.

    """
    # Set the classpath
    if additional_classpaths is not None:
        for classpath in additional_classpaths:
            if not os.path.exists(classpath):
                raise FileNotFoundError(f"Classpath {os.path.abspath(classpath)} does not exist")
            jpype.addClassPath(os.path.abspath(classpath))

    # Add standard patrius jars to the classpath
    if not jpype.isJVMStarted():
        jpype.addClassPath(os.path.join(dirpath, 'jars', '*'))

        # Path to GitLab-CI JVM
        if dirpath == "/builds/patrius/internal/patrius_py/pytrius":  
            os.environ["JAVA_HOME"] = ("/builds/patrius/internal/patrius_py/jre/lib/amd64/server/")
            
        elif jvmpath != None :
            os.environ["JAVA_HOME"] = jvmpath

        else: 
            os.environ["JAVA_HOME"] = ("C:\\NoSave\\SIRIUS\\ATL-DEV-JAVA\\v4.3.2\\components\\"
                                   "java-1.8.0-oracle-1.8.0_144-b01.x86_64")

        # Start the JVM
        # '-Xcheck:jni','-verbose:jni','-verbose:class'
        if vmargs is not None:
            jpype.startJVM(*vmargs.split(","), convertStrings=True, jvmpath=jvmpath)
        else:
            jpype.startJVM(convertStrings=True, jvmpath=jvmpath)
    else:
        print("JVM already started, resuming on started JVM")

    # Perform modifications for Patrius
    import pytrius.patrius_converters


