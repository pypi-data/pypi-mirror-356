import jpype

java_path = "C:\\NoSave\SIRIUS\\ATL-DEV-JAVA\\v4.3.2\\components\\jdk-11.0.20.1+1\\bin\\server\\jvm.dll"

classpath = [
    "pytrius/pytrius/jars/patrius-4.16.jar",
    "pytrius/pytrius/jars/patriusdataset-1.4.6.jar",
    # Add any other necessary JARs here
]

from pathlib import Path
import jpype
import stubgenj
import shutil
import sys
from subprocess import PIPE, run

jar_folder = Path("pytrius/jars") 
javadoc_jar_folder = Path("pytrius/jars") / "javadoc-jars"
stubs_folders = ["java-stubs", "fr-stubs", "jpype-stubs"]


if __name__ == '__main__':
    # First removing all old JARs to avoid multiple versions of the same JAR
    # if jar_folder.exists() and jar_folder.is_dir():
    #     shutil.rmtree(jar_folder)
    # if javadoc_jar_folder.exists() and javadoc_jar_folder.is_dir():
    #     shutil.rmtree(javadoc_jar_folder)

    # Calling maven to download the JARs. Maven must be installed on your system
    result = run(["mvn", "dependency:copy"], universal_newlines=True)

    jar_list = list(map(str, jar_folder.glob('**/*.jar')))
    javadoc_jar_list = list(map(str, javadoc_jar_folder.glob('**/*.jar')))

    if result.returncode == 0:
        print(f"""Successfully downloaded following JARs:
              - normal JARs: {jar_list}
              - javadoc JARs: {javadoc_jar_list}
************* Now generating stubs *************
              """)
    else:
        print(f"Maven called returned non-zero exit code {result.returncode}")
        sys.exit(result.returncode)

    # Removing old stubs folders
    for stub_folder in stubs_folders:
        stub_path = Path(stub_folder)
        if stub_path.exists() and stub_path.is_dir():
            shutil.rmtree(stub_path)

    # Generating stubs
    classpath = jar_list + javadoc_jar_list
    jpype.startJVM(classpath=classpath, convertStrings=True)

    import jpype.imports
    import fr.cnes.sirius.patrius
    import fr.cnes.sirius.addons.patriusdataset
    import java

    stubgenj.generateJavaStubs([java, fr.cnes.sirius.patrius, fr.cnes.addons.patriusdataset],
                                useStubsSuffix=True)


# python -m stubgenj --convert-strings --classpath "pytrius/jars/*.jar" fr.cnes.sirius.patrius fr.cnes.sirius.addons.patriusdataset java