
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.analysis.differentiation
import fr.cnes.sirius.patrius.math.analysis.polynomials
import fr.cnes.sirius.patrius.math.random
import fr.cnes.sirius.patrius.math.utils
import java.io
import jpype
import typing



class AbstractLinearIntervalsFunction:
    """
    public abstract class AbstractLinearIntervalsFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>`
    
        Abstract class for linear interpolation. Allows 1, 2 or 3 dimensions. Owns an optimised indices search.
    
        Since:
            2.3
    """
    def __init__(self): ...
    def getxtab(self) -> typing.MutableSequence[float]:
        """
            Gets xtab
        
            Returns:
                the x values
        
        
        """
        ...

class BicubicSplineInterpolatingFunction(fr.cnes.sirius.patrius.math.analysis.BivariateFunction):
    """
    public class BicubicSplineInterpolatingFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
    
        Function that implements the ` bicubic spline interpolation <http://en.wikipedia.org/wiki/Bicubic_interpolation>`.
    
        Since:
            2.1
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray4: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray5: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray6: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    def partialDerivativeX(self, double: float, double2: float) -> float:
        """
        
            Parameters:
                x (double): x-coordinate.
                y (double): y-coordinate.
        
            Returns:
                the value at point (x, y) of the first partial derivative with respect to x.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`:             if :code:`x` (resp. :code:`y`) is outside the range defined by the boundary values of :code:`xval` (resp. :code:`yval`).
        
        
        """
        ...
    def partialDerivativeXX(self, double: float, double2: float) -> float:
        """
        
            Parameters:
                x (double): x-coordinate.
                y (double): y-coordinate.
        
            Returns:
                the value at point (x, y) of the second partial derivative with respect to x.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`:             if :code:`x` (resp. :code:`y`) is outside the range defined by the boundary values of :code:`xval` (resp. :code:`yval`).
        
        
        """
        ...
    def partialDerivativeXY(self, double: float, double2: float) -> float:
        """
        
            Parameters:
                x (double): x-coordinate.
                y (double): y-coordinate.
        
            Returns:
                the value at point (x, y) of the second partial cross-derivative.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`:             if :code:`x` (resp. :code:`y`) is outside the range defined by the boundary values of :code:`xval` (resp. :code:`yval`).
        
        
        """
        ...
    def partialDerivativeY(self, double: float, double2: float) -> float:
        """
        
            Parameters:
                x (double): x-coordinate.
                y (double): y-coordinate.
        
            Returns:
                the value at point (x, y) of the first partial derivative with respect to y.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`:             if :code:`x` (resp. :code:`y`) is outside the range defined by the boundary values of :code:`xval` (resp. :code:`yval`).
        
        
        """
        ...
    def partialDerivativeYY(self, double: float, double2: float) -> float:
        """
        
            Parameters:
                x (double): x-coordinate.
                y (double): y-coordinate.
        
            Returns:
                the value at point (x, y) of the second partial derivative with respect to y.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`:             if :code:`x` (resp. :code:`y`) is outside the range defined by the boundary values of :code:`xval` (resp. :code:`yval`).
        
        
        """
        ...
    def value(self, double: float, double2: float) -> float:
        """
            Compute the value for the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
        
            Parameters:
                x (double): Abscissa for which the function value should be computed.
                y (double): Ordinate for which the function value should be computed.
        
            Returns:
                the value.
        
        
        """
        ...

class BivariateGridInterpolator:
    """
    public interface BivariateGridInterpolator
    
        Interface representing a bivariate real interpolating function where the sample points must be specified on a regular
        grid.
    """
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> fr.cnes.sirius.patrius.math.analysis.BivariateFunction:
        """
            Compute an interpolating function for the dataset.
        
            Parameters:
                xval (double[]): All the x-coordinates of the interpolation points, sorted in increasing order.
                yval (double[]): All the y-coordinates of the interpolation points, sorted in increasing order.
                fval (double[][]): The values of the interpolation points on all the grid knots: :code:`fval[i][j] = f(xval[i], yval[j])` .
        
            Returns:
                a function which interpolates the dataset.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NoDataException`: if any of the arrays has zero length.
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array lengths are inconsistent.
        
        
        """
        ...

class HermiteInterpolator(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableVectorFunction, java.io.Serializable):
    """
    public class HermiteInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableVectorFunction`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Polynomial interpolator using both sample values and sample derivatives.
    
        WARNING: this class is *not* expected to remain in Orekit. It is provided by version 3.1 of Apache Commons Math.
        However, since as of writing (June 2012) this version is not released yet, Orekit depends on the latest official version
        3.0 which does not provides this class. So despite it is implemented as a public class in Orekit so it can be used in
        from any package, it does not belong to Orekit public API and should not be used at application level. Once version 3.1
        of Apache Commons Math is released, this class will be removed from Orekit.
    
        The interpolation polynomials match all sample points, including both values and provided derivatives. There is one
        polynomial for each component of the values vector. All polynomial have the same degree. The degree of the polynomials
        depends on the number of points and number of derivatives at each point. For example the interpolation polynomials for n
        sample points without any derivatives all have degree n-1. The interpolation polynomials for n sample points with the
        two extreme points having value and first derivative and the remaining points having value only all have degree n+1. The
        interpolation polynomial for n sample points with value, first and second derivative for all points all have degree
        3n-1.
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def addSamplePoint(self, double: float, *doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> None: ...
    def derivative(self, double: float) -> typing.MutableSequence[float]:
        """
            Interpolate first derivative at a specified abscissa.
        
            Calling this method is equivalent to call the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction.value` methods of the derivatives of all
            polynomials returned by :meth:`~fr.cnes.sirius.patrius.math.analysis.interpolation.HermiteInterpolator.getPolynomials`,
            except it builds neither the intermediate polynomials nor their derivatives, so this method is faster and numerically
            more stable.
        
            Parameters:
                x (double): interpolation abscissa
        
            Returns:
                interpolated derivative
        
            Raises:
                : if sample is empty
        
        
        """
        ...
    def getPolynomials(self) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction]:
        """
            Compute the interpolation polynomials.
        
            Returns:
                interpolation polynomials array
        
            Raises:
                : if sample is empty
        
        
        """
        ...
    def getSize(self) -> int:
        """
            Compute the size of the list of values of the function as created by the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction.value` method
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction.getSize` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction`
        
            Returns:
                the size of the values array
        
        
        """
        ...
    @typing.overload
    def value(self, double: float) -> typing.MutableSequence[float]:
        """
            Interpolate value at a specified abscissa.
        
            Calling this method is equivalent to call the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction.value` methods of all polynomials returned
            by :meth:`~fr.cnes.sirius.patrius.math.analysis.interpolation.HermiteInterpolator.getPolynomials`, except it does not
            build the intermediate polynomials, so this method is faster and numerically more stable.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateVectorFunction`
        
            Parameters:
                x (double): interpolation abscissa
        
            Returns:
                interpolated value
        
            Raises:
                : if sample is empty
        
            Interpolate value at a specified abscissa.
        
            Calling this method is equivalent to call the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction.value` methods of all polynomials returned
            by :meth:`~fr.cnes.sirius.patrius.math.analysis.interpolation.HermiteInterpolator.getPolynomials`, except it does not
            build the intermediate polynomials, so this method is faster and numerically more stable.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableVectorFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableVectorFunction`
        
            Parameters:
                x (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): interpolation abscissa
        
            Returns:
                interpolated value
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NoDataException`: if sample is empty
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> typing.MutableSequence[fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure]: ...
    def valueAndDerivative(self, double: float, boolean: bool) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Interpolate value, first and optionally second derivative at a specified abscissa.
        
            Calling this method is equivalent to call the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.interpolation.HermiteInterpolator.value` method with a structure
            representing 2 derivatives but is faster since it does not use the generic operations of the
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure` that are slower.
        
            Calling this method is equivalent to call the
            :meth:`~fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunction.value` method of the derivatives of all
            polynomials returned by :meth:`~fr.cnes.sirius.patrius.math.analysis.interpolation.HermiteInterpolator.getPolynomials`,
            except it builds neither the intermediate polynomials nor their derivatives, so this method is faster and numerically
            more stable.
        
            Parameters:
                x (double): interpolation abscissa
                computeDoubleDerivative (boolean): Indicates whether the second derivative should be computed
        
            Returns:
                interpolated value, derivative and optionally second derivative
        
            Raises:
                : if sample is empty
        
        
        """
        ...

class MicrosphereInterpolatingFunction(fr.cnes.sirius.patrius.math.analysis.MultivariateFunction):
    """
    public class MicrosphereInterpolatingFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction`
    
        Interpolating function that implements the `Microsphere Projection <http://www.dudziak.com/microsphere.php>`.
    """
    def __init__(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], int: int, int2: int, unitSphereRandomVectorGenerator: fr.cnes.sirius.patrius.math.random.UnitSphereRandomVectorGenerator): ...
    def value(self, doubleArray: typing.Union[typing.List[float], jpype.JArray]) -> float:
        """
            Description copied from interface: 
            Compute the value for the function at the given point.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.MultivariateFunction`
        
            Parameters:
                point (double[]): Interpolation point.
        
            Returns:
                the interpolated value.
        
        
        """
        ...

class MultivariateInterpolator:
    """
    public interface MultivariateInterpolator
    
        Interface representing a univariate real interpolating function.
    
        Since:
            2.1
    """
    def interpolate(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> fr.cnes.sirius.patrius.math.analysis.MultivariateFunction:
        """
            Computes an interpolating function for the data set.
        
            Parameters:
                xval (double[][]): the arguments for the interpolation points. :code:`xval[i][0]` is the first component of interpolation point :code:`i`,
                    :code:`xval[i][1]` is the second component, and so on until :code:`xval[i][d-1]`, the last component of that
                    interpolation point (where :code:`d` is thus the dimension of the space).
                yval (double[]): the values for the interpolation points
        
            Returns:
                a function which interpolates the data set
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the arguments violate assumptions made by the interpolation algorithm.
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: when the array dimensions are not consistent.
                :class:`~fr.cnes.sirius.patrius.math.exception.NoDataException`: if an array has zero-length.
                :class:`~fr.cnes.sirius.patrius.math.exception.NullArgumentException`: if the arguments are :code:`null`.
        
        
        """
        ...

class TricubicSplineInterpolatingFunction(fr.cnes.sirius.patrius.math.analysis.TrivariateFunction):
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray], doubleArray4: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray], doubleArray5: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray], doubleArray6: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray], doubleArray7: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray], doubleArray8: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray], doubleArray9: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray], doubleArray10: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray], doubleArray11: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray]): ...
    def value(self, double: float, double2: float, double3: float) -> float: ...

class TrivariateGridInterpolator:
    """
    public interface TrivariateGridInterpolator
    
        Interface representing a trivariate real interpolating function where the sample points must be specified on a regular
        grid.
    
        Since:
            2.2
    """
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray], doubleArray4: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray]) -> fr.cnes.sirius.patrius.math.analysis.TrivariateFunction:
        """
            Compute an interpolating function for the dataset.
        
            Parameters:
                xval (double[]): All the x-coordinates of the interpolation points, sorted in increasing order.
                yval (double[]): All the y-coordinates of the interpolation points, sorted in increasing order.
                zval (double[]): All the z-coordinates of the interpolation points, sorted in increasing order.
                fval (double[][][]): the values of the interpolation points on all the grid knots: :code:`fval[i][j][k] = f(xval[i], yval[j], zval[k])`.
        
            Returns:
                a function that interpolates the data set.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NoDataException`: if any of the arrays has zero length.
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array lengths are inconsistent.
        
        
        """
        ...

class UnivariateInterpolator:
    """
    public interface UnivariateInterpolator
    
        Interface representing a univariate real interpolating function.
    """
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction:
        """
            Compute an interpolating function for the dataset.
        
            Parameters:
                xval (double[]): Arguments for the interpolation points.
                yval (double[]): Values for the interpolation points.
        
            Returns:
                a function which interpolates the dataset.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.MathIllegalArgumentException`: if the arguments violate assumptions made by the interpolation algorithm.
        
        
        """
        ...

class BiLinearIntervalsFunction(AbstractLinearIntervalsFunction, fr.cnes.sirius.patrius.math.analysis.BivariateFunction):
    """
    public class BiLinearIntervalsFunction extends :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.AbstractLinearIntervalsFunction` implements :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
    
        Implements the representation of a linear function in dimension 2. If double[] are given to the constructor, they should
        be sorted by increasing order (duplicates are allowed). No test to ensure that will be made, therefore, if these tab are
        not correctly sorted, results can be totally wrong. No exception will be thrown.
    
        Since:
            2.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex, iSearchIndex2: fr.cnes.sirius.patrius.math.utils.ISearchIndex, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]): ...
    def getValues(self) -> typing.MutableSequence[typing.MutableSequence[float]]:
        """
            Gets ftab in dimension 2
        
            Returns:
                the function values
        
        
        """
        ...
    def getytab(self) -> typing.MutableSequence[float]:
        """
            Gets ytab
        
            Returns:
                the y values
        
        
        """
        ...
    def value(self, double: float, double2: float) -> float:
        """
            Computation of the interpolated/extrapolated value f(x,y).
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
        
            Parameters:
                x (double): : abscissa where to interpolate.
                y (double): : ordinate where to interpolate.
        
            Returns:
                fxy : the value of the function at (x,y).
        
        
        """
        ...

class BiLinearIntervalsInterpolator(BivariateGridInterpolator):
    """
    public final class BiLinearIntervalsInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.BivariateGridInterpolator`
    
        Class representing a BivariateGridInterpolator for linear interpolation in dimension 2.
    
        Since:
            2.3
    """
    def __init__(self): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> BiLinearIntervalsFunction:
        """
            Compute an interpolating function for the dataset.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.BivariateGridInterpolator`
        
            Parameters:
                xval (double[]): abscissas for the interpolation points.
                yval (double[]): ordinates for the interpolation points.
                fval (double[][]): function values for the interpolation points.
        
            Returns:
                a function which interpolates the dataset.
        
        
        """
        ...

class BicubicSplineInterpolator(BivariateGridInterpolator):
    """
    public class BicubicSplineInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.BivariateGridInterpolator`
    
        Generates a bicubic interpolating function.
    
        Since:
            2.2
    """
    def __init__(self): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> BicubicSplineInterpolatingFunction:
        """
            Compute an interpolating function for the dataset.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.BivariateGridInterpolator`
        
            Parameters:
                xval (double[]): All the x-coordinates of the interpolation points, sorted in increasing order.
                yval (double[]): All the y-coordinates of the interpolation points, sorted in increasing order.
                fval (double[][]): The values of the interpolation points on all the grid knots: :code:`fval[i][j] = f(xval[i], yval[j])` .
        
            Returns:
                a function which interpolates the dataset.
        
        
        """
        ...

class DividedDifferenceInterpolator(UnivariateInterpolator, java.io.Serializable):
    """
    public class DividedDifferenceInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UnivariateInterpolator`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Implements the Divided Difference Algorithm for interpolation of real univariate functions. For reference, see
        **Introduction to Numerical Analysis**, ISBN 038795452X, chapter 2.
    
        The actual code of Neville's evaluation is in PolynomialFunctionLagrangeForm, this class provides an easy-to-use
        interface to it.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunctionNewtonForm:
        """
            Compute an interpolating function for the dataset.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UnivariateInterpolator`
        
            Parameters:
                x (double[]): Interpolating points array.
                y (double[]): Interpolating values array.
        
            Returns:
                a function which interpolates the dataset.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array lengths are different.
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the number of points is less than 2.
                :class:`~fr.cnes.sirius.patrius.math.exception.NonMonotonicSequenceException`: if :code:`x` is not sorted in strictly increasing order.
        
        
        """
        ...

class LinearInterpolator(UnivariateInterpolator):
    """
    public class LinearInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UnivariateInterpolator`
    
        Implements a linear function for interpolation of real univariate functions.
    """
    def __init__(self): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialSplineFunction:
        """
            Computes a linear interpolating function for the data set.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UnivariateInterpolator`
        
            Parameters:
                x (double[]): the arguments for the interpolation points
                y (double[]): the values for the interpolation points
        
            Returns:
                a function which interpolates the data set
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if :code:`x` and :code:`y` have different sizes.
                :class:`~fr.cnes.sirius.patrius.math.exception.NonMonotonicSequenceException`: if :code:`x` is not sorted in strict increasing order.
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the size of :code:`x` is smaller than 2.
        
        
        """
        ...

class LoessInterpolator(UnivariateInterpolator, java.io.Serializable):
    DEFAULT_BANDWIDTH: typing.ClassVar[float] = ...
    DEFAULT_ROBUSTNESS_ITERS: typing.ClassVar[int] = ...
    DEFAULT_ACCURACY: typing.ClassVar[float] = ...
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, int: int): ...
    @typing.overload
    def __init__(self, double: float, int: int, double2: float): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialSplineFunction: ...
    @typing.overload
    def smooth(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...
    @typing.overload
    def smooth(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray]) -> typing.MutableSequence[float]: ...

class MicrosphereInterpolator(MultivariateInterpolator):
    """
    public class MicrosphereInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.MultivariateInterpolator`
    
        Interpolator that implements the algorithm described in *William Dudziak*'s `MS thesis
        <http://www.dudziak.com/microsphere.pdf>`.
    
        Since:
            2.1
    """
    DEFAULT_MICROSPHERE_ELEMENTS: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_MICROSPHERE_ELEMENTS
    
        Default number of surface elements that composes the microsphere.
    
        Also see:
            :meth:`~constant`
    
    
    """
    DEFAULT_BRIGHTNESS_EXPONENT: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_BRIGHTNESS_EXPONENT
    
        Default exponent used the weights calculation.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> fr.cnes.sirius.patrius.math.analysis.MultivariateFunction:
        """
            Computes an interpolating function for the data set.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.MultivariateInterpolator`
        
            Parameters:
                xval (double[][]): the arguments for the interpolation points. :code:`xval[i][0]` is the first component of interpolation point :code:`i`,
                    :code:`xval[i][1]` is the second component, and so on until :code:`xval[i][d-1]`, the last component of that
                    interpolation point (where :code:`d` is thus the dimension of the space).
                yval (double[]): the values for the interpolation points
        
            Returns:
                a function which interpolates the data set
        
        
        """
        ...

class NevilleInterpolator(UnivariateInterpolator, java.io.Serializable):
    """
    public class NevilleInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UnivariateInterpolator`, `Serializable <http://docs.oracle.com/javase/8/docs/api/java/io/Serializable.html?is-external=true>`
    
        Implements the ` Neville's Algorithm <http://mathworld.wolfram.com/NevillesAlgorithm.html>` for interpolation of real
        univariate functions. For reference, see **Introduction to Numerical Analysis**, ISBN 038795452X, chapter 2.
    
        The actual code of Neville's algorithm is in PolynomialFunctionLagrangeForm, this class provides an easy-to-use
        interface to it.
    
        Since:
            1.2
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialFunctionLagrangeForm:
        """
            Computes an interpolating function for the data set.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UnivariateInterpolator`
        
            Parameters:
                x (double[]): Interpolating points.
                y (double[]): Interpolating values.
        
            Returns:
                a function which interpolates the data set
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.DimensionMismatchException`: if the array lengths are different.
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the number of points is less than 2.
                :class:`~fr.cnes.sirius.patrius.math.exception.NonMonotonicSequenceException`: if two abscissae have the same value.
        
        
        """
        ...

class SplineInterpolator(UnivariateInterpolator):
    def __init__(self): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> fr.cnes.sirius.patrius.math.analysis.polynomials.PolynomialSplineFunction: ...

class TriLinearIntervalsFunction(AbstractLinearIntervalsFunction, fr.cnes.sirius.patrius.math.analysis.TrivariateFunction):
    """
    public class TriLinearIntervalsFunction extends :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.AbstractLinearIntervalsFunction` implements :class:`~fr.cnes.sirius.patrius.math.analysis.TrivariateFunction`
    
        Implements the representation of a linear function in dimension 2. If double[] are given to the constructor, they should
        be sorted by increasing order. No test to ensure that will be made, therefore, if these tab are not correctly sorted,
        results can be totally wrong. No exception will be thrown.
    
        Since:
            2.3
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray], doubleArray4: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray]): ...
    @typing.overload
    def __init__(self, iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex, iSearchIndex2: fr.cnes.sirius.patrius.math.utils.ISearchIndex, iSearchIndex3: fr.cnes.sirius.patrius.math.utils.ISearchIndex, doubleArray: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray]): ...
    def getValues(self) -> typing.MutableSequence[typing.MutableSequence[typing.MutableSequence[float]]]:
        """
            Gets ftab in dimension 3
        
            Returns:
                the function values
        
        
        """
        ...
    def getytab(self) -> typing.MutableSequence[float]:
        """
            Gets ytab
        
            Returns:
                the y values
        
        
        """
        ...
    def getztab(self) -> typing.MutableSequence[float]:
        """
            Gets ztab
        
            Returns:
                the z values
        
        
        """
        ...
    def value(self, double: float, double2: float, double3: float) -> float:
        """
            Computation of the interpolated/extrapolated value f(x,y,z).
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.TrivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.TrivariateFunction`
        
            Parameters:
                x (double): : abscissa where to interpolate.
                y (double): : ordinate where to interpolate.
                z (double): : height where to interpolate.
        
            Returns:
                fxyz : the value of the function at (x,y,z).
        
        
        """
        ...

class TriLinearIntervalsInterpolator(TrivariateGridInterpolator):
    """
    public final class TriLinearIntervalsInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.TrivariateGridInterpolator`
    
        Class representing a TrivariateGridInterpolator for linear interpolation in dimension 3.
    
        Since:
            2.3
    """
    def __init__(self): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray], doubleArray4: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray]) -> TriLinearIntervalsFunction:
        """
            Compute an interpolating function for the dataset.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.TrivariateGridInterpolator`
        
            Parameters:
                xval (double[]): 1st component for the interpolation points.
                yval (double[]): 2nd component for the interpolation points.
                zval (double[]): 3rd component for the interpolation points.
                fval (double[][][]): function values for the interpolation points.
        
            Returns:
                a function which interpolates the dataset.
        
        
        """
        ...

class TricubicSplineInterpolator(TrivariateGridInterpolator):
    """
    public class TricubicSplineInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.TrivariateGridInterpolator`
    
        Generates a tricubic interpolating function.
    
        Since:
            2.2
    """
    def __init__(self): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[float], jpype.JArray], doubleArray4: typing.Union[typing.List[typing.MutableSequence[typing.MutableSequence[float]]], jpype.JArray]) -> TricubicSplineInterpolatingFunction:
        """
            Compute an interpolating function for the dataset.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.TrivariateGridInterpolator`
        
            Parameters:
                xval (double[]): All the x-coordinates of the interpolation points, sorted in increasing order.
                yval (double[]): All the y-coordinates of the interpolation points, sorted in increasing order.
                zval (double[]): All the z-coordinates of the interpolation points, sorted in increasing order.
                fval (double[][][]): the values of the interpolation points on all the grid knots: :code:`fval[i][j][k] = f(xval[i], yval[j], zval[k])`.
        
            Returns:
                a function that interpolates the data set.
        
        
        """
        ...

class UniLinearIntervalsFunction(AbstractLinearIntervalsFunction, fr.cnes.sirius.patrius.math.analysis.UnivariateFunction):
    @typing.overload
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    @typing.overload
    def __init__(self, iSearchIndex: fr.cnes.sirius.patrius.math.utils.ISearchIndex, doubleArray: typing.Union[typing.List[float], jpype.JArray]): ...
    def getValues(self) -> typing.MutableSequence[float]: ...
    def value(self, double: float) -> float: ...

class UniLinearIntervalsInterpolator(UnivariateInterpolator):
    """
    public final class UniLinearIntervalsInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UnivariateInterpolator`
    
        Class representing a univariate function for linear interpolation in dimension 1.
    
        Since:
            2.3
    """
    def __init__(self): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> UniLinearIntervalsFunction:
        """
            Compute an interpolating function for the dataset.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UnivariateInterpolator`
        
            Parameters:
                xval (double[]): Arguments for the interpolation points.
                fval (double[]): Values for the interpolation points.
        
            Returns:
                a function which interpolates the dataset.
        
        
        """
        ...

class UnivariatePeriodicInterpolator(UnivariateInterpolator):
    """
    public class UnivariatePeriodicInterpolator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UnivariateInterpolator`
    
        Adapter for classes implementing the :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UnivariateInterpolator`
        interface. The data to be interpolated is assumed to be periodic. Thus values that are outside of the range can be
        passed to the interpolation function: They will be wrapped into the initial range before being passed to the class that
        actually computes the interpolation.
    """
    DEFAULT_EXTEND: typing.ClassVar[int] = ...
    """
    public static final int DEFAULT_EXTEND
    
        Default number of extension points of the samples array.
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self, univariateInterpolator: typing.Union[UnivariateInterpolator, typing.Callable], double: float): ...
    @typing.overload
    def __init__(self, univariateInterpolator: typing.Union[UnivariateInterpolator, typing.Callable], double: float, int: int): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]) -> fr.cnes.sirius.patrius.math.analysis.UnivariateFunction:
        """
            Description copied from interface: 
            Compute an interpolating function for the dataset.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.UnivariateInterpolator`
        
            Parameters:
                xval (double[]): Arguments for the interpolation points.
                yval (double[]): Values for the interpolation points.
        
            Returns:
                a function which interpolates the dataset.
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.NumberIsTooSmallException`: if the number of extension points iss larger then the size of :code:`xval`.
        
        
        """
        ...

class SmoothingPolynomialBicubicSplineInterpolator(BicubicSplineInterpolator):
    """
    public class SmoothingPolynomialBicubicSplineInterpolator extends :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.BicubicSplineInterpolator`
    
        Generates a bicubic interpolation function. Prior to generating the interpolating function, the input is smoothed using
        polynomial fitting.
    
        Since:
            2.2
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, int: int): ...
    @typing.overload
    def __init__(self, int: int, int2: int): ...
    def interpolate(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray], doubleArray3: typing.Union[typing.List[typing.MutableSequence[float]], jpype.JArray]) -> BicubicSplineInterpolatingFunction:
        """
            Compute an interpolating function for the dataset.
        
            Specified by:
                 in interface :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.BivariateGridInterpolator`
        
            Overrides:
                 in class :class:`~fr.cnes.sirius.patrius.math.analysis.interpolation.BicubicSplineInterpolator`
        
            Parameters:
                xval (double[]): All the x-coordinates of the interpolation points, sorted in increasing order.
                yval (double[]): All the y-coordinates of the interpolation points, sorted in increasing order.
                fval (double[][]): The values of the interpolation points on all the grid knots: :code:`fval[i][j] = f(xval[i], yval[j])` .
        
            Returns:
                a function which interpolates the dataset.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.analysis.interpolation")``.

    AbstractLinearIntervalsFunction: typing.Type[AbstractLinearIntervalsFunction]
    BiLinearIntervalsFunction: typing.Type[BiLinearIntervalsFunction]
    BiLinearIntervalsInterpolator: typing.Type[BiLinearIntervalsInterpolator]
    BicubicSplineInterpolatingFunction: typing.Type[BicubicSplineInterpolatingFunction]
    BicubicSplineInterpolator: typing.Type[BicubicSplineInterpolator]
    BivariateGridInterpolator: typing.Type[BivariateGridInterpolator]
    DividedDifferenceInterpolator: typing.Type[DividedDifferenceInterpolator]
    HermiteInterpolator: typing.Type[HermiteInterpolator]
    LinearInterpolator: typing.Type[LinearInterpolator]
    LoessInterpolator: typing.Type[LoessInterpolator]
    MicrosphereInterpolatingFunction: typing.Type[MicrosphereInterpolatingFunction]
    MicrosphereInterpolator: typing.Type[MicrosphereInterpolator]
    MultivariateInterpolator: typing.Type[MultivariateInterpolator]
    NevilleInterpolator: typing.Type[NevilleInterpolator]
    SmoothingPolynomialBicubicSplineInterpolator: typing.Type[SmoothingPolynomialBicubicSplineInterpolator]
    SplineInterpolator: typing.Type[SplineInterpolator]
    TriLinearIntervalsFunction: typing.Type[TriLinearIntervalsFunction]
    TriLinearIntervalsInterpolator: typing.Type[TriLinearIntervalsInterpolator]
    TricubicSplineInterpolatingFunction: typing.Type[TricubicSplineInterpolatingFunction]
    TricubicSplineInterpolator: typing.Type[TricubicSplineInterpolator]
    TrivariateGridInterpolator: typing.Type[TrivariateGridInterpolator]
    UniLinearIntervalsFunction: typing.Type[UniLinearIntervalsFunction]
    UniLinearIntervalsInterpolator: typing.Type[UniLinearIntervalsInterpolator]
    UnivariateInterpolator: typing.Type[UnivariateInterpolator]
    UnivariatePeriodicInterpolator: typing.Type[UnivariatePeriodicInterpolator]
