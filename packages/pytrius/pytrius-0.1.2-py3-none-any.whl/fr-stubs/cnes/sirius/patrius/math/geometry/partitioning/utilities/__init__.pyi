
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import typing



_AVLTree__T = typing.TypeVar('_AVLTree__T', bound=java.lang.Comparable)  # <T>
class AVLTree(typing.Generic[_AVLTree__T]):
    """
    public class AVLTree<T extends `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<T>> extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        This class implements AVL trees.
    
        The purpose of this class is to sort elements while allowing duplicate elements (i.e. such that :code:`a.equals(b)` is
        true). The :code:`SortedSet` interface does not allow this, so a specific class is needed. Null elements are not
        allowed.
    
        Since the :code:`equals` method is not sufficient to differentiate elements, the
        :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.delete` method is implemented using the
        equality operator.
    
        In order to clearly mark the methods provided here do not have the same semantics as the ones specified in the
        :code:`SortedSet` interface, different names are used (:code:`add` has been replaced by
        :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.insert` and :code:`remove` has been replaced
        by :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.delete`).
    
        This class is based on the C implementation Georg Kraml has put in the public domain. Unfortunately, his
        :class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.www.purists.org.georg.avltree.index` seems not to
        exist any more.
    
        Since:
            3.0
    """
    def __init__(self): ...
    def delete(self, t: _AVLTree__T) -> bool:
        """
            Delete an element from the tree.
        
            The element is deleted only if there is a node :code:`n` containing exactly the element instance specified, i.e. for
            which :code:`n.getElement() == element`. This is purposely *different* from the specification of the
            :code:`java.util.Set` :code:`remove` method (in fact, this is the reason why a specific class has been developed).
        
            Parameters:
                element (:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree`): element to delete (silently ignored if null)
        
            Returns:
                true if the element was deleted from the tree
        
        
        """
        ...
    def getLargest(self) -> 'AVLTree.Node':
        """
            Get the node whose element is the largest one in the tree.
        
            Returns:
                the tree node containing the largest element in the tree or null if the tree is empty
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getSmallest`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getNotSmaller`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getNotLarger`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.Node.getPrevious`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.Node.getNext`
        
        
        """
        ...
    def getNotLarger(self, t: _AVLTree__T) -> 'AVLTree.Node':
        """
            Get the node whose element is not larger than the reference object.
        
            Parameters:
                reference (:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree`): reference object (may not be in the tree)
        
            Returns:
                the tree node containing the largest element not larger than the reference object (in which case the node is guaranteed
                not to be empty) or null if either the tree is empty or all its elements are larger than the reference object
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getSmallest`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getLargest`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getNotSmaller`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.Node.getPrevious`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.Node.getNext`
        
        
        """
        ...
    def getNotSmaller(self, t: _AVLTree__T) -> 'AVLTree.Node':
        """
            Get the node whose element is not smaller than the reference object.
        
            Parameters:
                reference (:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree`): reference object (may not be in the tree)
        
            Returns:
                the tree node containing the smallest element not smaller than the reference object or null if either the tree is empty
                or all its elements are smaller than the reference object
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getSmallest`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getLargest`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getNotLarger`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.Node.getPrevious`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.Node.getNext`
        
        
        """
        ...
    def getSmallest(self) -> 'AVLTree.Node':
        """
            Get the node whose element is the smallest one in the tree.
        
            Returns:
                the tree node containing the smallest element in the tree or null if the tree is empty
        
            Also see:
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getLargest`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getNotSmaller`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.getNotLarger`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.Node.getPrevious`,
                :meth:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree.Node.getNext`
        
        
        """
        ...
    def insert(self, t: _AVLTree__T) -> None:
        """
            Insert an element in the tree.
        
            Parameters:
                element (:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.AVLTree`): element to insert (silently ignored if null)
        
        
        """
        ...
    def isEmpty(self) -> bool:
        """
            Check if the tree is empty.
        
            Returns:
                true if the tree is empty
        
        
        """
        ...
    def size(self) -> int:
        """
            Get the number of elements of the tree.
        
            Returns:
                number of elements contained in the tree
        
        
        """
        ...
    class Node:
        def delete(self) -> None: ...
        def getElement(self) -> _AVLTree__T: ...
        def getNext(self) -> 'AVLTree.Node': ...
        def getPrevious(self) -> 'AVLTree.Node': ...

class OrderedTuple(java.lang.Comparable['OrderedTuple']):
    """
    public class OrderedTuple extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements `Comparable <http://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html?is-external=true>`<:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.OrderedTuple`>
    
        This class implements an ordering operation for T-uples.
    
        Ordering is done by encoding all components of the T-uple into a single scalar value and using this value as the sorting
        key. Encoding is performed using the method invented by Georg Cantor in 1877 when he proved it was possible to establish
        a bijection between a line and a plane. The binary representations of the components of the T-uple are mixed together to
        form a single scalar. This means that the 2 :sup:`k` bit of component 0 is followed by the 2 :sup:`k` bit of component
        1, then by the 2 :sup:`k` bit of component 2 up to the 2 :sup:`k` bit of component :code:`t`, which is followed by the 2
        :sup:`k-1` bit of component 0, followed by the 2 :sup:`k-1` bit of component 1 ... The binary representations are
        extended as needed to handle numbers with different scales and a suitable 2 :sup:`p` offset is added to the components
        in order to avoid negative numbers (this offset is adjusted as needed during the comparison operations).
    
        The more interesting property of the encoding method for our purpose is that it allows to select all the points that are
        in a given range. This is depicted in dimension 2 by the following picture:
    
        T-uples with negative infinite or positive infinite components are sorted logically.
    
        Since the specification of the :code:`Comparator` interface allows only :code:`ClassCastException` errors, some
        arbitrary choices have been made to handle specific cases. The rationale for these choices is to keep *regular* and
        consistent T-uples together.
    
          - instances with different dimensions are sorted according to their dimension regardless of their components values
          - instances with :code:`Double.NaN` components are sorted after all other ones (even after instances with positive
            infinite components
          - instances with both positive and negative infinite components are considered as if they had :code:`Double.NaN`
            components
    
    
        Since:
            3.0
    """
    def __init__(self, *double: float): ...
    def compareTo(self, orderedTuple: 'OrderedTuple') -> int:
        """
            Compares this ordered T-uple with the specified object.
        
            The ordering method is detailed in the general description of the class. Its main property is to be consistent with
            distance: geometrically close T-uples stay close to each other when stored in a sorted collection using this comparison
            method.
        
            T-uples with negative infinite, positive infinite are sorted logically.
        
            Some arbitrary choices have been made to handle specific cases. The rationale for these choices is to keep *normal* and
            consistent T-uples together.
        
              - instances with different dimensions are sorted according to their dimension regardless of their components values
              - instances with :code:`Double.NaN` components are sorted after all other ones (evan after instances with positive
                infinite components
              - instances with both positive and negative infinite components are considered as if they had :code:`Double.NaN`
                components
        
        
            Specified by:
                 in interface 
        
            Parameters:
                ot (:class:`~fr.cnes.sirius.patrius.math.geometry.partitioning.utilities.OrderedTuple`): T-uple to compare instance with
        
            Returns:
                a negative integer if the instance is less than the object, zero if they are equal, or a positive integer if the
                instance is greater than the object
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    def getComponents(self) -> typing.MutableSequence[float]:
        """
            Get the components array.
        
            Returns:
                array containing the T-uple components
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.geometry.partitioning.utilities")``.

    AVLTree: typing.Type[AVLTree]
    OrderedTuple: typing.Type[OrderedTuple]
