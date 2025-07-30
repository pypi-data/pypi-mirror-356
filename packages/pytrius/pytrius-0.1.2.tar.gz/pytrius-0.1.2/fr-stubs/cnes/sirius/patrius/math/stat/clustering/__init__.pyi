
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.io
import java.lang
import java.util
import jpype
import typing



_Cluster__T = typing.TypeVar('_Cluster__T', bound='Clusterable')  # <T>
class Cluster(java.io.Serializable, typing.Generic[_Cluster__T]):
    """
    public class Cluster<T extends :class:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable`<T>> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Cluster holding a set of :class:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable` points.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, t: _Cluster__T): ...
    def addPoint(self, t: _Cluster__T) -> None:
        """
            Add a point to this cluster.
        
            Parameters:
                point (:class:`~fr.cnes.sirius.patrius.math.stat.clustering.Cluster`): point to add
        
        
        """
        ...
    def getCenter(self) -> _Cluster__T:
        """
            Get the point chosen to be the center of this cluster.
        
            Returns:
                chosen cluster center
        
        
        """
        ...
    def getPoints(self) -> java.util.List[_Cluster__T]: ...

_Clusterable__T = typing.TypeVar('_Clusterable__T')  # <T>
class Clusterable(typing.Generic[_Clusterable__T]):
    """
    public interface Clusterable<T>
    
        Interface for points that can be clustered together.
    
        Since:
            2.0
    """
    def centroidOf(self, collection: typing.Union[java.util.Collection[_Clusterable__T], typing.Sequence[_Clusterable__T], typing.Set[_Clusterable__T]]) -> _Clusterable__T: ...
    def distanceFrom(self, t: _Clusterable__T) -> float:
        """
            Returns the distance from the given point.
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable`): the point to compute the distance from
        
            Returns:
                the distance from the given point
        
        
        """
        ...

_DBSCANClusterer__T = typing.TypeVar('_DBSCANClusterer__T', bound=Clusterable)  # <T>
class DBSCANClusterer(typing.Generic[_DBSCANClusterer__T]):
    """
    public class DBSCANClusterer<T extends :class:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable`<T>> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        DBSCAN (density-based spatial clustering of applications with noise) algorithm.
    
        The DBSCAN algorithm forms clusters based on the idea of density connectivity, i.e. a point p is density connected to
        another point q, if there exists a chain of points p :sub:`i` , with i = 1 .. n and p :sub:`1` = p and p :sub:`n` = q,
        such that each pair <p :sub:`i` , p :sub:`i+1` > is directly density-reachable. A point q is directly density-reachable
        from point p if it is in the ε-neighborhood of this point.
    
        Any point that is not density-reachable from a formed cluster is treated as noise, and will thus not be present in the
        result.
    
        The algorithm requires two parameters:
    
          - eps: the distance that defines the ε-neighborhood of a point
          - minPoints: the minimum number of density-connected points required to form a cluster
    
    
        **Note:** as DBSCAN is not a centroid-based clustering algorithm, the resulting
        :class:`~fr.cnes.sirius.patrius.math.stat.clustering.Cluster` objects will have no defined center, i.e.
        :meth:`~fr.cnes.sirius.patrius.math.stat.clustering.Cluster.getCenter` will return :code:`null`.
    
        Since:
            3.1
    
        Also see:
            `DBSCAN (wikipedia) <http://en.wikipedia.org/wiki/DBSCAN>`, ` A Density-Based Algorithm for Discovering Clusters in
            Large Spatial Databases with Noise <http://www.dbs.ifi.lmu.de/Publikationen/Papers/KDD-96.final.frame.pdf>`
    """
    def __init__(self, double: float, int: int): ...
    def cluster(self, collection: typing.Union[java.util.Collection[_DBSCANClusterer__T], typing.Sequence[_DBSCANClusterer__T], typing.Set[_DBSCANClusterer__T]]) -> java.util.List[Cluster[_DBSCANClusterer__T]]: ...
    def getEps(self) -> float:
        """
            Returns the maximum radius of the neighborhood to be considered.
        
            Returns:
                maximum radius of the neighborhood
        
        
        """
        ...
    def getMinPts(self) -> int:
        """
            Returns the minimum number of points needed for a cluster.
        
            Returns:
                minimum number of points needed for a cluster
        
        
        """
        ...

_KMeansPlusPlusClusterer__T = typing.TypeVar('_KMeansPlusPlusClusterer__T', bound=Clusterable)  # <T>
class KMeansPlusPlusClusterer(typing.Generic[_KMeansPlusPlusClusterer__T]):
    """
    public class KMeansPlusPlusClusterer<T extends :class:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable`<T>> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Clustering algorithm based on David Arthur and Sergei Vassilvitski k-means++ algorithm.
    
        Since:
            2.0
    
        Also see:
            `K-means++ (wikipedia) <http://en.wikipedia.org/wiki/K-means%2B%2B>`
    """
    @typing.overload
    def __init__(self, random: java.util.Random): ...
    @typing.overload
    def __init__(self, random: java.util.Random, emptyClusterStrategy: 'KMeansPlusPlusClusterer.EmptyClusterStrategy'): ...
    @typing.overload
    def cluster(self, collection: typing.Union[java.util.Collection[_KMeansPlusPlusClusterer__T], typing.Sequence[_KMeansPlusPlusClusterer__T], typing.Set[_KMeansPlusPlusClusterer__T]], int: int, int2: int) -> java.util.List[Cluster[_KMeansPlusPlusClusterer__T]]: ...
    @typing.overload
    def cluster(self, collection: typing.Union[java.util.Collection[_KMeansPlusPlusClusterer__T], typing.Sequence[_KMeansPlusPlusClusterer__T], typing.Set[_KMeansPlusPlusClusterer__T]], int: int, int2: int, int3: int) -> java.util.List[Cluster[_KMeansPlusPlusClusterer__T]]: ...
    class EmptyClusterStrategy(java.lang.Enum['KMeansPlusPlusClusterer.EmptyClusterStrategy']):
        LARGEST_VARIANCE: typing.ClassVar['KMeansPlusPlusClusterer.EmptyClusterStrategy'] = ...
        LARGEST_POINTS_NUMBER: typing.ClassVar['KMeansPlusPlusClusterer.EmptyClusterStrategy'] = ...
        FARTHEST_POINT: typing.ClassVar['KMeansPlusPlusClusterer.EmptyClusterStrategy'] = ...
        ERROR: typing.ClassVar['KMeansPlusPlusClusterer.EmptyClusterStrategy'] = ...
        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
        @typing.overload
        @staticmethod
        def valueOf(string: str) -> 'KMeansPlusPlusClusterer.EmptyClusterStrategy': ...
        @typing.overload
        @staticmethod
        def valueOf(class_: typing.Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
        @staticmethod
        def values() -> typing.MutableSequence['KMeansPlusPlusClusterer.EmptyClusterStrategy']: ...

class EuclideanDoublePoint(Clusterable['EuclideanDoublePoint'], java.io.Serializable):
    """
    public class EuclideanDoublePoint extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable`<:class:`~fr.cnes.sirius.patrius.math.stat.clustering.EuclideanDoublePoint`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        A simple implementation of :class:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable` for points with double
        coordinates.
    
        Since:
            3.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    def centroidOf(self, collection: typing.Union[java.util.Collection['EuclideanDoublePoint'], typing.Sequence['EuclideanDoublePoint'], typing.Set['EuclideanDoublePoint']]) -> 'EuclideanDoublePoint': ...
    def distanceFrom(self, euclideanDoublePoint: 'EuclideanDoublePoint') -> float:
        """
            Returns the distance from the given point.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable.distanceFrom` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.stat.clustering.EuclideanDoublePoint`): the point to compute the distance from
        
            Returns:
                the distance from the given point
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getPoint(self) -> typing.MutableSequence[float]:
        """
            Get the n-dimensional point in integer space.
        
            Returns:
                a reference (not a copy!) to the wrapped array
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...

class EuclideanIntegerPoint(Clusterable['EuclideanIntegerPoint'], java.io.Serializable):
    """
    public class EuclideanIntegerPoint extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable`<:class:`~fr.cnes.sirius.patrius.math.stat.clustering.EuclideanIntegerPoint`>, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        A simple implementation of :class:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable` for points with integer
        coordinates.
    
        Since:
            2.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, intArray: typing.Union[typing.List[int], jpype.JArray]): ...
    def centroidOf(self, collection: typing.Union[java.util.Collection['EuclideanIntegerPoint'], typing.Sequence['EuclideanIntegerPoint'], typing.Set['EuclideanIntegerPoint']]) -> 'EuclideanIntegerPoint': ...
    def distanceFrom(self, euclideanIntegerPoint: 'EuclideanIntegerPoint') -> float:
        """
            Returns the distance from the given point.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable.distanceFrom` in
                interface :class:`~fr.cnes.sirius.patrius.math.stat.clustering.Clusterable`
        
            Parameters:
                p (:class:`~fr.cnes.sirius.patrius.math.stat.clustering.EuclideanIntegerPoint`): the point to compute the distance from
        
            Returns:
                the distance from the given point
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getPoint(self) -> typing.MutableSequence[int]:
        """
            Get the n-dimensional point in integer space.
        
            Returns:
                a reference (not a copy!) to the wrapped array
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
            Since:
                2.1
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.stat.clustering")``.

    Cluster: typing.Type[Cluster]
    Clusterable: typing.Type[Clusterable]
    DBSCANClusterer: typing.Type[DBSCANClusterer]
    EuclideanDoublePoint: typing.Type[EuclideanDoublePoint]
    EuclideanIntegerPoint: typing.Type[EuclideanIntegerPoint]
    KMeansPlusPlusClusterer: typing.Type[KMeansPlusPlusClusterer]
