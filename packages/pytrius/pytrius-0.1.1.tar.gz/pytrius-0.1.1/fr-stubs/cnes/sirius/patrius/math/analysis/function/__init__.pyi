
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import fr.cnes.sirius.patrius.math.analysis
import fr.cnes.sirius.patrius.math.analysis.differentiation
import jpype
import typing



class Abs(fr.cnes.sirius.patrius.math.analysis.UnivariateFunction):
    """
    public class Abs extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
    
        Absolute value function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
        
        """
        ...

class Acos(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Acos extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Arc-cosine function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Acosh(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Acosh extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Hyperbolic arc-cosine function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Add(fr.cnes.sirius.patrius.math.analysis.BivariateFunction):
    """
    public class Add extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
    
        Add the two operands.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
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

class Asin(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Asin extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Arc-sine function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Asinh(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Asinh extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Hyperbolic arc-sine function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Atan(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Atan extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Arc-tangent function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Atan2(fr.cnes.sirius.patrius.math.analysis.BivariateFunction):
    """
    public class Atan2 extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
    
        Arc-tangent function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
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

class Atanh(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Atanh extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Hyperbolic arc-tangent function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Cbrt(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Cbrt extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Cube root function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Ceil(fr.cnes.sirius.patrius.math.analysis.UnivariateFunction):
    """
    public class Ceil extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
    
        :code:`ceil` function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
        
        """
        ...

class Constant(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Constant extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Constant function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Cos(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Cos extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Cosine function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Cosh(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Cosh extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Hyperbolic cosine function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class CosineFunction(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class CosineFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Cosine function of the form c.cos(f(x)) with f an univariate function that returns an angle in radians.
    
        Since:
            4.7
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, univariateDifferentiableFunction: fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction): ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Assumes t is has only one variable
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Divide(fr.cnes.sirius.patrius.math.analysis.BivariateFunction):
    """
    public class Divide extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
    
        Divide the first operand by the second.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
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

class Exp(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Exp extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Exponential function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Expm1(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Expm1 extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        :code:`e :sup:`x` -1` function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Floor(fr.cnes.sirius.patrius.math.analysis.UnivariateFunction):
    """
    public class Floor extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
    
        :code:`floor` function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
        
        """
        ...

class Gaussian(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Gaussian extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        ` Gaussian <http://en.wikipedia.org/wiki/Gaussian_function>` function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def __init__(self, double: float, double2: float, double3: float): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...
    class Parametric(fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction):
        def __init__(self): ...
        def gradient(self, double: float, *double2: float) -> typing.MutableSequence[float]: ...
        def value(self, double: float, *double2: float) -> float: ...

class HarmonicOscillator(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class HarmonicOscillator extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        ` simple harmonic oscillator <http://en.wikipedia.org/wiki/Harmonic_oscillator>` function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...
    class Parametric(fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction):
        def __init__(self): ...
        def gradient(self, double: float, *double2: float) -> typing.MutableSequence[float]: ...
        def value(self, double: float, *double2: float) -> float: ...

class Identity(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Identity extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Identity function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Inverse(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Inverse extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Inverse function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Log(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Log extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Natural logarithm function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Log10(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Log10 extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Base 10 logarithm function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Log1p(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Log1p extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        :code:`log(1 + p)` function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Logistic(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Logistic extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        ` Generalised logistic <http://en.wikipedia.org/wiki/Generalised_logistic_function>` function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, double2: float, double3: float, double4: float, double5: float, double6: float): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...
    class Parametric(fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction):
        def __init__(self): ...
        def gradient(self, double: float, *double2: float) -> typing.MutableSequence[float]: ...
        def value(self, double: float, *double2: float) -> float: ...

class Logit(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Logit extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        ` Logit <http://en.wikipedia.org/wiki/Logit>` function. It is the inverse of the
        :class:`~fr.cnes.sirius.patrius.math.analysis.function.Sigmoid` function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Raises:
                :class:`~fr.cnes.sirius.patrius.math.exception.OutOfRangeException`: if parameter is outside of function domain
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...
    class Parametric(fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction):
        def __init__(self): ...
        def gradient(self, double: float, *double2: float) -> typing.MutableSequence[float]: ...
        def value(self, double: float, *double2: float) -> float: ...

class Max(fr.cnes.sirius.patrius.math.analysis.BivariateFunction):
    """
    public class Max extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
    
        Maximum function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
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

class Min(fr.cnes.sirius.patrius.math.analysis.BivariateFunction):
    """
    public class Min extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
    
        Minimum function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
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

class Minus(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Minus extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Minus function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Multiply(fr.cnes.sirius.patrius.math.analysis.BivariateFunction):
    """
    public class Multiply extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
    
        Multiply the two operands.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
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

class Pow(fr.cnes.sirius.patrius.math.analysis.BivariateFunction):
    """
    public class Pow extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
    
        Power function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
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

class Power(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Power extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Power function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Rint(fr.cnes.sirius.patrius.math.analysis.UnivariateFunction):
    """
    public class Rint extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
    
        :code:`rint` function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
        
        """
        ...

class Sigmoid(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Sigmoid extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        ` Sigmoid <http://en.wikipedia.org/wiki/Sigmoid_function>` function. It is the inverse of the
        :class:`~fr.cnes.sirius.patrius.math.analysis.function.Logit` function. A more flexible version, the generalised
        logistic, is implemented by the :class:`~fr.cnes.sirius.patrius.math.analysis.function.Logistic` class.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, double: float, double2: float): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...
    class Parametric(fr.cnes.sirius.patrius.math.analysis.ParametricUnivariateFunction):
        def __init__(self): ...
        def gradient(self, double: float, *double2: float) -> typing.MutableSequence[float]: ...
        def value(self, double: float, *double2: float) -> float: ...

class Signum(fr.cnes.sirius.patrius.math.analysis.UnivariateFunction):
    """
    public class Signum extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
    
        :code:`signum` function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
        
        """
        ...

class Sin(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Sin extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Sine function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Sinc(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Sinc extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        `Sinc <http://en.wikipedia.org/wiki/Sinc_function>` function, defined by
    
        .. code-block: java
        
        
         
           sinc(x) = 1            if x = 0,
                     sin(x) / x   otherwise.
         
         
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, boolean: bool): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class SineFunction(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class SineFunction extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Sine function of the form c.sin(f(x)) with f an univariate function that returns an angle in radians.
    
        Since:
            4.7
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, double: float, univariateDifferentiableFunction: fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction): ...
    def toString(self) -> str:
        """
        
            Overrides:
                 in class 
        
        
        """
        ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Assumes t is has only one variable
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Sinh(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Sinh extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Hyperbolic sine function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Sqrt(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Sqrt extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Square-root function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class StepFunction(fr.cnes.sirius.patrius.math.analysis.UnivariateFunction):
    def __init__(self, doubleArray: typing.Union[typing.List[float], jpype.JArray], doubleArray2: typing.Union[typing.List[float], jpype.JArray]): ...
    def value(self, double: float) -> float: ...

class Subtract(fr.cnes.sirius.patrius.math.analysis.BivariateFunction):
    """
    public class Subtract extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.BivariateFunction`
    
        Subtract the second operand from the first.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
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

class Tan(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Tan extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Tangent function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Tanh(fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction):
    """
    public class Tanh extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
    
        Hyperbolic tangent function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    @typing.overload
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
            Simple mathematical function.
        
            :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction` classes compute both the
            value and the first derivative of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.UnivariateDifferentiableFunction`
        
            Parameters:
                t (:class:`~fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure`): function input value
        
            Returns:
                function result
        
            Since:
                3.1
        
        
        """
        ...
    @typing.overload
    def value(self, derivativeStructure: fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure) -> fr.cnes.sirius.patrius.math.analysis.differentiation.DerivativeStructure: ...

class Ulp(fr.cnes.sirius.patrius.math.analysis.UnivariateFunction):
    """
    public class Ulp extends `Object <http://docs.oracle.com/javase/8/docs/api/java/lang/Object.html?is-external=true>` implements :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
    
        :code:`ulp` function.
    
        Since:
            3.0
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self): ...
    def value(self, double: float) -> float:
        """
            Compute the value of the function.
        
            Specified by:
                :meth:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction.value` in
                interface :class:`~fr.cnes.sirius.patrius.math.analysis.UnivariateFunction`
        
            Parameters:
                x (double): Point at which the function value should be computed.
        
            Returns:
                the value of the function.
        
        
        """
        ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("fr.cnes.sirius.patrius.math.analysis.function")``.

    Abs: typing.Type[Abs]
    Acos: typing.Type[Acos]
    Acosh: typing.Type[Acosh]
    Add: typing.Type[Add]
    Asin: typing.Type[Asin]
    Asinh: typing.Type[Asinh]
    Atan: typing.Type[Atan]
    Atan2: typing.Type[Atan2]
    Atanh: typing.Type[Atanh]
    Cbrt: typing.Type[Cbrt]
    Ceil: typing.Type[Ceil]
    Constant: typing.Type[Constant]
    Cos: typing.Type[Cos]
    Cosh: typing.Type[Cosh]
    CosineFunction: typing.Type[CosineFunction]
    Divide: typing.Type[Divide]
    Exp: typing.Type[Exp]
    Expm1: typing.Type[Expm1]
    Floor: typing.Type[Floor]
    Gaussian: typing.Type[Gaussian]
    HarmonicOscillator: typing.Type[HarmonicOscillator]
    Identity: typing.Type[Identity]
    Inverse: typing.Type[Inverse]
    Log: typing.Type[Log]
    Log10: typing.Type[Log10]
    Log1p: typing.Type[Log1p]
    Logistic: typing.Type[Logistic]
    Logit: typing.Type[Logit]
    Max: typing.Type[Max]
    Min: typing.Type[Min]
    Minus: typing.Type[Minus]
    Multiply: typing.Type[Multiply]
    Pow: typing.Type[Pow]
    Power: typing.Type[Power]
    Rint: typing.Type[Rint]
    Sigmoid: typing.Type[Sigmoid]
    Signum: typing.Type[Signum]
    Sin: typing.Type[Sin]
    Sinc: typing.Type[Sinc]
    SineFunction: typing.Type[SineFunction]
    Sinh: typing.Type[Sinh]
    Sqrt: typing.Type[Sqrt]
    StepFunction: typing.Type[StepFunction]
    Subtract: typing.Type[Subtract]
    Tan: typing.Type[Tan]
    Tanh: typing.Type[Tanh]
    Ulp: typing.Type[Ulp]
