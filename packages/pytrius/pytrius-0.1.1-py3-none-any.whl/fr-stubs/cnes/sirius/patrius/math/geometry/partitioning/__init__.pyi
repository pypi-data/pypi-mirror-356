
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.geometry
import fr.cnes.sirius.patrius.math.geometry.partitioning.utilities
import java.lang
import jpype
import typing



_BSPTree__LeafMerger__S = typing.TypeVar('_BSPTree__LeafMerger__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
_BSPTree__S = typing.TypeVar('_BSPTree__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
class BSPTree(typing.Generic[_BSPTree__S]):
    """
    public class BSPTree<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class represent a Binary Space Partition tree.
    
        BSP trees are an efficient way to represent space partitions and to associate attributes with each cell. Each node in a
        BSP tree represents a convex region which is partitioned in two convex sub-regions at each side of a cut hyperplane. The
        root tree contains the complete space.
    
        The main use of such partitions is to use a boolean attribute to define an inside/outside property, hence representing
        arbitrary polytopes (line segments in 1D, polygons in 2D and polyhedrons in 3D) and to operate on them.
    
        Another example would be to represent Voronoi tesselations, the attribute of each cell holding the defining point of the
        cell.
    
        The application-defined attributes are shared among copied instances and propagated to split parts. These attributes are
        not used by the BSP-tree algorithms themselves, so the application can use them for any purpose. Since the tree visiting
        method holds internal and leaf nodes differently, it is possible to use different classes for internal nodes attributes
        and leaf nodes attributes. This should be used with care, though, because if the tree is modified in any way after
        attributes have been set, some internal nodes may become leaf nodes and some leaf nodes may become internal nodes.
    
        One of the main sources for the development of this package was Bruce Naylor, John Amanatides and William Thibault paper
        `Merging BSP Trees Yields Polyhedral Set Operations <http://www.cs.yorku.ca/~amana/research/bsptSetOp.pdf>` Proc.
        Siggraph '90, Computer Graphics 24(4), August 1990, pp 115-124, published by the Association for Computing Machinery
        (ACM).
    
        Since:
            3.0
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, subHyperplane: 'SubHyperplane'[_BSPTree__S], bSPTree: 'BSPTree'[_BSPTree__S], bSPTree2: 'BSPTree'[_BSPTree__S], object: typing.Any): ...
    @typing.overload
    def __init__(self, object: typing.Any): ...
    def copySelf(self) -> 'BSPTree'[_BSPTree__S]: ...
    def getAttribute(self) -> typing.Any:
        """
            Get the attribute associated with the instance.
        
            Returns:
                attribute associated with the node or null if no attribute has been explicitly set using the
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree.setAttribute` method
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree.setAttribute`
        
        
        """
        ...
    def getCell(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[_BSPTree__S]) -> 'BSPTree'[_BSPTree__S]: ...
    def getCut(self) -> 'SubHyperplane'[_BSPTree__S]: ...
    def getMinus(self) -> 'BSPTree'[_BSPTree__S]: ...
    def getParent(self) -> 'BSPTree'[_BSPTree__S]: ...
    def getPlus(self) -> 'BSPTree'[_BSPTree__S]: ...
    def insertCut(self, hyperplane: 'Hyperplane'[_BSPTree__S]) -> bool: ...
    def insertInTree(self, bSPTree: 'BSPTree'[_BSPTree__S], boolean: bool) -> None: ...
    def merge(self, bSPTree: 'BSPTree'[_BSPTree__S], leafMerger: typing.Union['BSPTree.LeafMerger'[_BSPTree__S], typing.Callable[['BSPTree'[fr.cnes.sirius.patrius.math.geometry.Space], 'BSPTree'[fr.cnes.sirius.patrius.math.geometry.Space], 'BSPTree'[fr.cnes.sirius.patrius.math.geometry.Space], bool, bool], 'BSPTree'[fr.cnes.sirius.patrius.math.geometry.Space]]]) -> 'BSPTree'[_BSPTree__S]: ...
    def setAttribute(self, object: typing.Any) -> None:
        """
            Associate an attribute with the instance.
        
            Parameters:
                attributeIn (`Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`): attribute to associate with the node
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree.getAttribute`
        
        
        """
        ...
    def split(self, subHyperplane: 'SubHyperplane'[_BSPTree__S]) -> 'BSPTree'[_BSPTree__S]: ...
    def visit(self, bSPTreeVisitor: 'BSPTreeVisitor'[_BSPTree__S]) -> None: ...
    class LeafMerger(typing.Generic[_BSPTree__LeafMerger__S]):
        def merge(self, bSPTree: 'BSPTree'[_BSPTree__LeafMerger__S], bSPTree2: 'BSPTree'[_BSPTree__LeafMerger__S], bSPTree3: 'BSPTree'[_BSPTree__LeafMerger__S], boolean: bool, boolean2: bool) -> 'BSPTree'[_BSPTree__LeafMerger__S]: ...

_BSPTreeVisitor__S = typing.TypeVar('_BSPTreeVisitor__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
class BSPTreeVisitor(typing.Generic[_BSPTreeVisitor__S]):
    """
    public interface BSPTreeVisitor<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`>
    
        This interface is used to visit :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree` nodes.
    
        Navigation through :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree` can be done using two different
        point of views:
    
          - the first one is in a node-oriented way using the
            :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree.getPlus`,
            :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree.getMinus` and
            :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree.getParent` methods. Terminal nodes without associated
            :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane` can be visited this way, there is no
            constraint in the visit order, and it is possible to visit either all nodes or only a subset of the nodes
          - the second one is in a sub-hyperplane-oriented way using classes implementing this interface which obeys the visitor
            design pattern. The visit order is provided by the visitor as each node is first encountered. Each node is visited
            exactly once.
    
    
        Since:
            3.0
    
        Also see:
            :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree`,
            :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane`
    """
    def visitInternalNode(self, bSPTree: BSPTree[_BSPTreeVisitor__S]) -> None: ...
    def visitLeafNode(self, bSPTree: BSPTree[_BSPTreeVisitor__S]) -> None: ...
    def visitOrder(self, bSPTree: BSPTree[_BSPTreeVisitor__S]) -> 'BSPTreeVisitor.Order': ...
    class Order(java.lang.Enum['BSPTreeVisitor.Order']):
        PLUS_MINUS_SUB: typing.ClassVar['BSPTreeVisitor.Order'] = ...
        PLUS_SUB_MINUS: typing.ClassVar['BSPTreeVisitor.Order'] = ...
        MINUS_PLUS_SUB: typing.ClassVar['BSPTreeVisitor.Order'] = ...
        MINUS_SUB_PLUS: typing.ClassVar['BSPTreeVisitor.Order'] = ...
        SUB_PLUS_MINUS: typing.ClassVar['BSPTreeVisitor.Order'] = ...
        SUB_MINUS_PLUS: typing.ClassVar['BSPTreeVisitor.Order'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'BSPTreeVisitor.Order': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['BSPTreeVisitor.Order']: ...

_BoundaryAttribute__S = typing.TypeVar('_BoundaryAttribute__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
class BoundaryAttribute(typing.Generic[_BoundaryAttribute__S]):
    """
    public class BoundaryAttribute<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Class holding boundary attributes.
    
        This class is used for the attributes associated with the nodes of region boundary shell trees returned by the
        :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region.getTree`. It contains the parts of the node cut
        sub-hyperplane that belong to the boundary.
    
        This class is a simple placeholder, it does not provide any processing methods.
    
        Since:
            3.0
    
        Also see:
            :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region.getTree`
    """
    def __init__(self, subHyperplane: 'SubHyperplane'[_BoundaryAttribute__S], subHyperplane2: 'SubHyperplane'[_BoundaryAttribute__S]): ...
    def getPlusInside(self) -> 'SubHyperplane'[_BoundaryAttribute__S]: ...
    def getPlusOutside(self) -> 'SubHyperplane'[_BoundaryAttribute__S]: ...

_Embedding__S = typing.TypeVar('_Embedding__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
_Embedding__T = typing.TypeVar('_Embedding__T', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <T>
class Embedding(typing.Generic[_Embedding__S, _Embedding__T]):
    def toSpace(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[_Embedding__T]) -> fr.cnes.sirius.patrius.math.geometry.Vector[_Embedding__S]: ...
    def toSubSpace(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[_Embedding__S]) -> fr.cnes.sirius.patrius.math.geometry.Vector[_Embedding__T]: ...

_Hyperplane__S = typing.TypeVar('_Hyperplane__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
class Hyperplane(typing.Generic[_Hyperplane__S]):
    """
    public interface Hyperplane<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`>
    
        This interface represents an hyperplane of a space.
    
        The most prominent place where hyperplane appears in space partitioning is as cutters. Each partitioning node in a
        :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree` has a cut
        :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane` which is either an hyperplane or a part of an
        hyperplane. In an n-dimensions euclidean space, an hyperplane is an (n-1)-dimensions hyperplane (for example a
        traditional plane in the 3D euclidean space). They can be more exotic objects in specific fields, for example a circle
        on the surface of the unit sphere.
    
        Since:
            3.0
    """
    def copySelf(self) -> 'Hyperplane'[_Hyperplane__S]: ...
    def getOffset(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[_Hyperplane__S]) -> float: ...
    def sameOrientationAs(self, hyperplane: 'Hyperplane'[_Hyperplane__S]) -> bool: ...
    def wholeHyperplane(self) -> 'SubHyperplane'[_Hyperplane__S]: ...
    def wholeSpace(self) -> 'Region'[_Hyperplane__S]: ...

_Region__S = typing.TypeVar('_Region__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
class Region(typing.Generic[_Region__S]):
    """
    public interface Region<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`>
    
        This interface represents a region of a space as a partition.
    
        Region are subsets of a space, they can be infinite (whole space, half space, infinite stripe ...) or finite (polygons
        in 2D, polyhedrons in 3D ...). Their main characteristic is to separate points that are considered to be *inside* the
        region from points considered to be *outside* of it. In between, there may be points on the *boundary* of the region.
    
        This implementation is limited to regions for which the boundary is composed of several
        :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane`, including regions with no boundary at all:
        the whole space and the empty region. They are not necessarily finite and not necessarily path-connected. They can
        contain holes.
    
        Regions can be combined using the traditional sets operations : union, intersection, difference and symetric difference
        (exclusive or) for the binary operations, complement for the unary operation.
    
        Since:
            3.0
    """
    def buildNew(self, bSPTree: BSPTree[_Region__S]) -> 'Region'[_Region__S]: ...
    def checkPoint(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[_Region__S]) -> 'Region.Location': ...
    def contains(self, region: 'Region'[_Region__S]) -> bool: ...
    def copySelf(self) -> 'Region'[_Region__S]: ...
    def getBarycenter(self) -> fr.cnes.sirius.patrius.math.geometry.Vector[_Region__S]: ...
    def getBoundarySize(self) -> float:
        """
            Get the size of the boundary.
        
            Returns:
                the size of the boundary (this is 0 in 1D, a length in 2D, an area in 3D ...)
        
        
        """
        ...
    def getSize(self) -> float:
        """
            Get the size of the instance.
        
            Returns:
                the size of the instance (this is a length in 1D, an area in 2D, a volume in 3D ...)
        
        
        """
        ...
    def getTree(self, boolean: bool) -> BSPTree[_Region__S]: ...
    def intersection(self, subHyperplane: 'SubHyperplane'[_Region__S]) -> 'SubHyperplane'[_Region__S]: ...
    @typing.overload
    def isEmpty(self) -> bool:
        """
            Check if the instance is empty.
        
            Returns:
                true if the instance is empty
        
        boolean isEmpty(:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree`<:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region`> node)
        
            Check if the sub-tree starting at a given node is empty.
        
            Parameters:
                node (:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree`<:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region`> node): root node of the sub-tree (*must* have :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region` tree
                    semantics, i.e. the leaf nodes must have :code:`Boolean` attributes representing an inside/outside property)
        
            Returns:
                true if the sub-tree starting at the given node is empty
        
        
        """
        ...
    @typing.overload
    def isEmpty(self, bSPTree: BSPTree[_Region__S]) -> bool: ...
    def side(self, hyperplane: Hyperplane[_Region__S]) -> 'Side': ...
    class Location(java.lang.Enum['Region.Location']):
        INSIDE: typing.ClassVar['Region.Location'] = ...
        OUTSIDE: typing.ClassVar['Region.Location'] = ...
        BOUNDARY: typing.ClassVar['Region.Location'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'Region.Location': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['Region.Location']: ...

_RegionFactory__S = typing.TypeVar('_RegionFactory__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
class RegionFactory(typing.Generic[_RegionFactory__S]):
    """
    public class RegionFactory<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class is a factory for :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region`.
    
        Since:
            3.0
    """
    def __init__(self): ...
    def buildConvex(self, *hyperplane: Hyperplane[_RegionFactory__S]) -> Region[_RegionFactory__S]: ...
    def difference(self, region: Region[_RegionFactory__S], region2: Region[_RegionFactory__S]) -> Region[_RegionFactory__S]: ...
    def getComplement(self, region: Region[_RegionFactory__S]) -> Region[_RegionFactory__S]: ...
    def intersection(self, region: Region[_RegionFactory__S], region2: Region[_RegionFactory__S]) -> Region[_RegionFactory__S]: ...
    def union(self, region: Region[_RegionFactory__S], region2: Region[_RegionFactory__S]) -> Region[_RegionFactory__S]: ...
    def xor(self, region: Region[_RegionFactory__S], region2: Region[_RegionFactory__S]) -> Region[_RegionFactory__S]: ...

class Side(java.lang.Enum['Side']):
    """
    public enum Side extends `Enum <http://docs.oracle.com/javase/8/docs/api/java/lang/Enum.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Side`>
    
        Enumerate representing the location of an element with respect to an
        :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane` of a space.
    
        Since:
            3.0
    """
    PLUS: typing.ClassVar['Side'] = ...
    MINUS: typing.ClassVar['Side'] = ...
    BOTH: typing.ClassVar['Side'] = ...
    HYPER: typing.ClassVar['Side'] = ...
    _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'Side':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (`String <http://docs.oracle.com/javase/8/docs/api/java/lang/String.html?is-external=true>`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                : if this enum type has no constant with the specified name
                : if the argument is null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @staticmethod
    def values() -> typing.MutableSequence['Side']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            
            for (Side c : Side.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

_SubHyperplane__SplitSubHyperplane__U = typing.TypeVar('_SubHyperplane__SplitSubHyperplane__U', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <U>
_SubHyperplane__S = typing.TypeVar('_SubHyperplane__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
class SubHyperplane(typing.Generic[_SubHyperplane__S]):
    """
    public interface SubHyperplane<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`>
    
        This interface represents the remaining parts of an hyperplane after other parts have been chopped off.
    
        sub-hyperplanes are obtained when parts of an :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane` are
        chopped off by other hyperplanes that intersect it. The remaining part is a convex region. Such objects appear in
        :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree` as the intersection of a cut hyperplane with the
        convex region which it splits, the chopping hyperplanes are the cut hyperplanes closer to the tree root.
    
        Since:
            3.0
    """
    def copySelf(self) -> 'SubHyperplane'[_SubHyperplane__S]: ...
    def getHyperplane(self) -> Hyperplane[_SubHyperplane__S]: ...
    def getSize(self) -> float:
        """
            Get the size of the instance.
        
            Returns:
                the size of the instance (this is a length in 1D, an area in 2D, a volume in 3D ...)
        
        
        """
        ...
    def isEmpty(self) -> bool:
        """
            Check if the instance is empty.
        
            Returns:
                true if the instance is empty
        
        
        """
        ...
    def reunite(self, subHyperplane: 'SubHyperplane'[_SubHyperplane__S]) -> 'SubHyperplane'[_SubHyperplane__S]: ...
    def side(self, hyperplane: Hyperplane[_SubHyperplane__S]) -> Side: ...
    def split(self, hyperplane: Hyperplane[_SubHyperplane__S]) -> 'SubHyperplane.SplitSubHyperplane'[_SubHyperplane__S]: ...
    class SplitSubHyperplane(typing.Generic[_SubHyperplane__SplitSubHyperplane__U]):
        def __init__(self, subHyperplane: 'SubHyperplane'[_SubHyperplane__SplitSubHyperplane__U], subHyperplane2: 'SubHyperplane'[_SubHyperplane__SplitSubHyperplane__U]): ...
        def getMinus(self) -> 'SubHyperplane'[_SubHyperplane__SplitSubHyperplane__U]: ...
        def getPlus(self) -> 'SubHyperplane'[_SubHyperplane__SplitSubHyperplane__U]: ...

_Transform__S = typing.TypeVar('_Transform__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
_Transform__T = typing.TypeVar('_Transform__T', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <T>
class Transform(typing.Generic[_Transform__S, _Transform__T]):
    """
    public interface Transform<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`,T extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`>
    
        This interface represents an inversible affine transform in a space.
    
        Inversible affine transform include for example scalings, translations, rotations.
    
        Transforms are dimension-specific. The consistency rules between the three :code:`apply` methods are the following ones
        for a transformed defined for dimension D:
    
          - the transform can be applied to a point in the D-dimension space using its
            :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Transform.apply` method
          - the transform can be applied to a (D-1)-dimension hyperplane in the D-dimension space using its
            :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Transform.apply` method
          - the transform can be applied to a (D-2)-dimension sub-hyperplane in a (D-1)-dimension hyperplane using its
            :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Transform.apply` method
    
    
        Since:
            3.0
    """
    @typing.overload
    def apply(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[_Transform__S]) -> fr.cnes.sirius.patrius.math.geometry.Vector[_Transform__S]: ...
    @typing.overload
    def apply(self, hyperplane: Hyperplane[_Transform__S]) -> Hyperplane[_Transform__S]: ...
    @typing.overload
    def apply(self, subHyperplane: SubHyperplane[_Transform__T], hyperplane: Hyperplane[_Transform__S], hyperplane2: Hyperplane[_Transform__S]) -> SubHyperplane[_Transform__T]: ...

_AbstractRegion__S = typing.TypeVar('_AbstractRegion__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
_AbstractRegion__T = typing.TypeVar('_AbstractRegion__T', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <T>
class AbstractRegion(Region[_AbstractRegion__S], typing.Generic[_AbstractRegion__S, _AbstractRegion__T]):
    """
    public abstract class AbstractRegion<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`,T extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region`<S>
    
        Abstract class for all regions, independently of geometry type or dimension.
    
        Since:
            3.0
    """
    def __init__(self, hyperplaneArray: typing.Union[typing.List[Hyperplane[_AbstractRegion__S]], jpype.JArray]): ...
    def applyTransform(self, transform: Transform[_AbstractRegion__S, _AbstractRegion__T]) -> 'AbstractRegion'[_AbstractRegion__S, _AbstractRegion__T]: ...
    def buildNew(self, bSPTree: BSPTree[_AbstractRegion__S]) -> 'AbstractRegion'[_AbstractRegion__S, _AbstractRegion__T]: ...
    def checkPoint(self, vector: fr.cnes.sirius.patrius.math.geometry.Vector[_AbstractRegion__S]) -> Region.Location: ...
    def contains(self, region: Region[_AbstractRegion__S]) -> bool: ...
    def copySelf(self) -> 'AbstractRegion'[_AbstractRegion__S, _AbstractRegion__T]: ...
    def getBarycenter(self) -> fr.cnes.sirius.patrius.math.geometry.Vector[_AbstractRegion__S]: ...
    def getBoundarySize(self) -> float:
        """
            Get the size of the boundary.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region.getBoundarySize` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region`
        
            Returns:
                the size of the boundary (this is 0 in 1D, a length in 2D, an area in 3D ...)
        
        
        """
        ...
    def getSize(self) -> float:
        """
            Get the size of the instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region.getSize` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region`
        
            Returns:
                the size of the instance (this is a length in 1D, an area in 2D, a volume in 3D ...)
        
        
        """
        ...
    def getTree(self, boolean: bool) -> BSPTree[_AbstractRegion__S]: ...
    def intersection(self, subHyperplane: SubHyperplane[_AbstractRegion__S]) -> SubHyperplane[_AbstractRegion__S]: ...
    @typing.overload
    def isEmpty(self) -> bool:
        """
            Check if the instance is empty.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region.isEmpty` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region`
        
            Returns:
                true if the instance is empty
        
        public boolean isEmpty(:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree`<:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.AbstractRegion`> node)
        
            Check if the sub-tree starting at a given node is empty.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region.isEmpty` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region`
        
            Parameters:
                node (:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree`<:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.AbstractRegion`> node): root node of the sub-tree (*must* have :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Region` tree
                    semantics, i.e. the leaf nodes must have :code:`Boolean` attributes representing an inside/outside property)
        
            Returns:
                true if the sub-tree starting at the given node is empty
        
        
        """
        ...
    @typing.overload
    def isEmpty(self, bSPTree: BSPTree[_AbstractRegion__S]) -> bool: ...
    def side(self, hyperplane: Hyperplane[_AbstractRegion__S]) -> Side: ...

_AbstractSubHyperplane__S = typing.TypeVar('_AbstractSubHyperplane__S', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <S>
_AbstractSubHyperplane__T = typing.TypeVar('_AbstractSubHyperplane__T', bound=fr.cnes.sirius.patrius.math.geometry.Space)  # <T>
class AbstractSubHyperplane(SubHyperplane[_AbstractSubHyperplane__S], typing.Generic[_AbstractSubHyperplane__S, _AbstractSubHyperplane__T]):
    """
    public abstract class AbstractSubHyperplane<S extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`,T extends :class:`~fr.cnes.sirius.patrius.math.geometry.Space`> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane`<S>
    
        This class implements the dimension-independent parts of
        :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane`.
    
        sub-hyperplanes are obtained when parts of an :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.Hyperplane` are
        chopped off by other hyperplanes that intersect it. The remaining part is a convex region. Such objects appear in
        :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.BSPTree` as the intersection of a cut hyperplane with the
        convex region which it splits, the chopping hyperplanes are the cut hyperplanes closer to the tree root.
    
        Since:
            3.0
    """
    def applyTransform(self, transform: Transform[_AbstractSubHyperplane__S, _AbstractSubHyperplane__T]) -> 'AbstractSubHyperplane'[_AbstractSubHyperplane__S, _AbstractSubHyperplane__T]: ...
    def copySelf(self) -> 'AbstractSubHyperplane'[_AbstractSubHyperplane__S, _AbstractSubHyperplane__T]: ...
    def getHyperplane(self) -> Hyperplane[_AbstractSubHyperplane__S]: ...
    def getRemainingRegion(self) -> Region[_AbstractSubHyperplane__T]: ...
    def getSize(self) -> float:
        """
            Get the size of the instance.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane.getSize` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane`
        
            Returns:
                the size of the instance (this is a length in 1D, an area in 2D, a volume in 3D ...)
        
        
        """
        ...
    def isEmpty(self) -> bool:
        """
            Check if the instance is empty.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane.isEmpty` in
                interface :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.SubHyperplane`
        
            Returns:
                true if the instance is empty
        
        
        """
        ...
    def reunite(self, subHyperplane: SubHyperplane[_AbstractSubHyperplane__S]) -> 'AbstractSubHyperplane'[_AbstractSubHyperplane__S, _AbstractSubHyperplane__T]: ...
    def side(self, hyperplane: Hyperplane[_AbstractSubHyperplane__S]) -> Side: ...
    def split(self, hyperplane: Hyperplane[_AbstractSubHyperplane__S]) -> SubHyperplane.SplitSubHyperplane[_AbstractSubHyperplane__S]: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.geometry.partitioning")``.

    AbstractRegion: typing.Type[AbstractRegion]
    AbstractSubHyperplane: typing.Type[AbstractSubHyperplane]
    BSPTree: typing.Type[BSPTree]
    BSPTreeVisitor: typing.Type[BSPTreeVisitor]
    BoundaryAttribute: typing.Type[BoundaryAttribute]
    Embedding: typing.Type[Embedding]
    Hyperplane: typing.Type[Hyperplane]
    Region: typing.Type[Region]
    RegionFactory: typing.Type[RegionFactory]
    Side: typing.Type[Side]
    SubHyperplane: typing.Type[SubHyperplane]
    Transform: typing.Type[Transform]
    utilities: fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.__module_protocol__
