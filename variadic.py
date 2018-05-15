#!/usr/bin/env python

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

"""
Introduction
============

Define a variadic function:

    >>> @variadic(int)
    ... def f(*xs):
    ...   return xs

It can be called with a variable number of arguments:

    >>> f()
    ()
    >>> f(1, 2, 3, 4)
    (1, 2, 3, 4)

So far, no change, but it can also be called with lists (any iterable, in fact) of arguments:

    >>> f([])
    ()
    >>> f([1, 2, 3], (4, 5, 6))
    (1, 2, 3, 4, 5, 6)
    >>> f(xrange(1, 4))
    (1, 2, 3)

And you can even mix them:

    >>> f(1, [2, 3], (4, 5), xrange(6, 8))
    (1, 2, 3, 4, 5, 6, 7)

Positional arguments, default values and keyword arguments are OK as well:

    >>> @variadic(int)
    ... def f(a, b=None, *cs, **kwds):
    ...   return a, b, cs, kwds
    >>> f(1)
    (1, None, (), {})
    >>> f(1, d=4)
    (1, None, (), {'d': 4})
    >>> f(1, 2, (3, 4), 5, d=6)
    (1, 2, (3, 4, 5), {'d': 6})

Pearls
======

Documentation generated by Sphinx for decorated functions
---------------------------------------------------------

It looks like a regular variadic function:

.. autofunction:: demo

TypeError raised when calling with bad arguments
------------------------------------------------

Exactly as if it was not decorated:

    >>> @variadic(int)
    ... def f(*xs):
    ...   pass
    >>> f(a=1)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: f() got an unexpected keyword argument 'a'

Exception raised by the decorated function
------------------------------------------

``@variadic`` adds just one stack frame with the same name as the decorated function:

    >>> @variadic(int)
    ... def f(*xs):
    ...   raise Exception
    >>> f()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<ast_in_variadic_py>", line 1, in f
      File "<stdin>", line 3, in f
    Exception

"""

import ast
import functools
import inspect
import itertools
import sys
import types
import unittest

# Todo-list:
# - allow passing the flatten function instead of typ
# - allow an even simpler usage without any parameters
# - add a parameter string to be prepended or appended to the docstring
# - support decorating callables that are not functions?
# - support keyword-only parameter (on Python 3)


# >>> help(types.FunctionType)
# class function(object)
#  |  function(code, globals[, name[, argdefs[, closure]]])
#  |
#  |  Create a function object from a code object and a dictionary.
#  |  The optional name string overrides the name from the code object.
#  |  The optional argdefs tuple specifies the default argument values.
#  |  The optional closure tuple supplies the bindings for free variables.


def variadic(typ):
    """
    Decorator taking a variadic function and making a very-variadic function from it:
    a function that can be called with a variable number of iterables of arguments.

    :param typ: the type (or tuple of types) of arguments expected.
        Variadic arguments that are instances of this type will be passed to the decorated function as-is.
        Others will be iterated and their contents will be passed.
    """
    def flatten(args):
        flat = []
        for arg in args:
            if isinstance(arg, typ):
                flat.append((arg,))
            else:
                flat.append(arg)
        return itertools.chain.from_iterable(flat)

    def decorator(wrapped):
        if sys.hexversion < 0x03000000:
            spec = inspect.getargspec(wrapped)
            assert spec.varargs is not None
            varargs = spec.varargs
            keywords = spec.keywords
        else:
            spec = inspect.getfullargspec(wrapped)
            assert spec.varargs is not None
            assert spec.kwonlyargs == []
            assert spec.kwonlydefaults is None
            assert spec.annotations == {}
            varargs = spec.varargs
            keywords = spec.varkw

        name = wrapped.__name__

        # Example was generated with print ast.dump(ast.parse("def f(a, b, *args, **kwds):
        # return call_wrapped((a, b), *args, **kwds)"), include_attributes=True)
        # http://code.activestate.com/recipes/578353-code-to-source-and-back/ helped a lot
        # http://stackoverflow.com/questions/10303248#29927459

        if sys.hexversion < 0x03000000:
            wrapper_ast_args = ast.arguments(
                args=[ast.Name(id=a, ctx=ast.Param(), lineno=1, col_offset=0) for a in spec.args],
                vararg=varargs,
                kwarg=keywords,
                defaults=[]
            )
        else:
            wrapper_ast_args = ast.arguments(
                args=[ast.arg(arg=a, annotation=None, lineno=1, col_offset=0) for a in spec.args],
                vararg=(
                    None if varargs is None else
                    ast.arg(arg=varargs, annotation=None, lineno=1, col_offset=0)
                ),
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=(
                    None if keywords is None else
                    ast.arg(arg=keywords, annotation=None, lineno=1, col_offset=0)
                ),
                defaults=[]
            )

        wrapped_func = ast.Name(id="wrapped", ctx=ast.Load(), lineno=1, col_offset=0)
        wrapped_args = [ast.Name(id=a, ctx=ast.Load(), lineno=1, col_offset=0) for a in spec.args]
        flatten_func = ast.Name(id="flatten", ctx=ast.Load(), lineno=1, col_offset=0)
        flatten_args = [ast.Name(id=spec.varargs, ctx=ast.Load(), lineno=1, col_offset=0)]

        if sys.hexversion < 0x03050000:
            return_value = ast.Call(
                func=wrapped_func,
                args=wrapped_args,
                keywords=[],
                starargs=ast.Call(
                    func=flatten_func, args=flatten_args,
                    keywords=[], starargs=None, kwargs=None, lineno=1, col_offset=0
                ),
                kwargs=(
                    None if keywords is None else
                    ast.Name(id=keywords, ctx=ast.Load(), lineno=1, col_offset=0)
                ),
                lineno=1, col_offset=0
            )
        else:
            return_value = ast.Call(
                func=wrapped_func,
                args=wrapped_args + [
                    ast.Starred(
                        value=ast.Call(func=flatten_func, args=flatten_args, keywords=[], lineno=1, col_offset=0),
                        ctx=ast.Load(), lineno=1, col_offset=0
                    ),
                ],
                keywords=(
                    [] if keywords is None else
                    [ast.keyword(arg=None, value=ast.Name(id=keywords, ctx=ast.Load(), lineno=1, col_offset=0))]
                ),
                lineno=1, col_offset=0
            )

        wrapper_ast = ast.Module(body=[ast.FunctionDef(
            name=name,
            args=wrapper_ast_args,
            body=[ast.Return(value=return_value, lineno=1, col_offset=0)],
            decorator_list=[],
            lineno=1,
            col_offset=0
        )])
        wrapper_code = [
            c for c in compile(wrapper_ast, "<ast_in_variadic_py>", "exec").co_consts if isinstance(c, types.CodeType)
        ][0]
        wrapper = types.FunctionType(wrapper_code, {"wrapped": wrapped, "flatten": flatten}, argdefs=spec.defaults)

        functools.update_wrapper(wrapper, wrapped)
        return wrapper
    return decorator


class PurelyVariadicFunctionTestCase(unittest.TestCase):
    def setUp(self):
        @variadic(int)
        def f(*xs):
            "f's doc"
            return xs

        self.f = f

        @variadic(int)
        def g(*ys):
            "g's doc"
            return ys

        self.g = g

    def test_name_is_preserved(self):
        self.assertEqual(self.f.__name__, "f")
        self.assertEqual(self.g.__name__, "g")

    def test_doc_is_preserved(self):
        self.assertEqual(self.f.__doc__, "f's doc")
        self.assertEqual(self.g.__doc__, "g's doc")

    def test_argspec_keeps_param_name(self):
        self.assertEqual(inspect.getargspec(self.f).varargs, "xs")
        self.assertEqual(inspect.getargspec(self.g).varargs, "ys")

    def test_call_without_arguments(self):
        self.assertEqual(self.f(), ())

    def test_call_with_one_argument(self):
        self.assertEqual(self.f(1), (1,))

    def test_call_with_several_arguments(self):
        self.assertEqual(self.f(1, 2, 3), (1, 2, 3))

    def test_call_with_one_list(self):
        self.assertEqual(self.f([1, 2, 3]), (1, 2, 3))

    def test_call_with_several_lists(self):
        self.assertEqual(self.f([1, 2], [3], [4, 5]), (1, 2, 3, 4, 5))

    def test_call_with_lists_and_arguments(self):
        self.assertEqual(self.f([1, 2], 3, 4, [5, 6], 7), (1, 2, 3, 4, 5, 6, 7))

    def test_call_with_keywords(self):
        with self.assertRaises(TypeError) as catcher:
            self.f(a=1)
        self.assertEqual(catcher.exception.args, ("f() got an unexpected keyword argument 'a'",))
        with self.assertRaises(TypeError) as catcher:
            self.g(a=1)
        self.assertEqual(catcher.exception.args, ("g() got an unexpected keyword argument 'a'",))


class NotOnlyVariadicFunctionTestCase(unittest.TestCase):
    def test_args_before_varargs(self):
        @variadic(int)
        def f(a, b, *xs):
            return a, b, xs

        self.assertEqual(f(1, 2, 3, [4, 5], 6), (1, 2, (3, 4, 5, 6)))

    @variadic(int)
    def f(self, a, b, *xs):
        return self, a, b, xs

    def test_method(self):
        self.assertEqual(self.f(1, 2, 3, [4, 5], 6), (self, 1, 2, (3, 4, 5, 6)))

    def test_kwds_after_varargs(self):
        @variadic(int)
        def f(a, b, *xs, **kwds):
            return a, b, xs, kwds

        self.assertEqual(f(1, 2, 3, [4, 5], 6, c=7, d=8), (1, 2, (3, 4, 5, 6), {"c": 7, "d": 8}))

    def test_defaults_on_args_before_varargs(self):
        default = object()  # To avoid implementations wich would stringify the default values and feed them to exec.

        @variadic(int)
        def f(a=None, b=default, *xs):
            return a, b, xs

        self.assertEqual(f(), (None, default, ()))

    def test_closures(self):
        a = 42

        @variadic(int)
        def f(*xs):
            return a, xs

        self.assertEqual(f(1, 2), (42, (1, 2)))
        a = 57
        self.assertEqual(f(1, 2), (57, (1, 2)))


@variadic(int)
def demo(a, b=None, *xs, **kwds):
    """
    Demo function.

    :param a: A
    :param b: B
    :param xs: Xs
    :param kwds: keywords
    """
    pass


if __name__ == "__main__":
    unittest.main()
