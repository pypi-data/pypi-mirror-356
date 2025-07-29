
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.geometry.euclidean.threed
import java.io
import typing



class Facet(fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider, java.io.Serializable):
    """
    public final class Facet extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        This class is a cross section provider.
    
        Note that the use of this class implies a constant area which may not be suited for some application such as reentry.
    
        Since:
            1.1
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider`, :meth:`~serialized`
    """
    def __init__(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D, double: float): ...
    def getArea(self) -> float:
        """
        
            Returns:
                facet area
        
        
        """
        ...
    def getCrossSection(self, vector3D: fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D) -> float:
        """
            Computes the cross section from the direction defined by a Vector3D.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider.getCrossSection` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.CrossSectionProvider`
        
            Parameters:
                direction (:class:`~fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D`): the direction vector
        
            Returns:
                the cross section
        
        
        """
        ...
    def getNormal(self) -> fr.cnes.sirius.patrius.math.geometry.euclidean.threed.Vector3D:
        """
        
            Returns:
                unit normal vector
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.assembly.properties.features")``.

    Facet: typing.Type[Facet]
