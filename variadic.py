#!/usr/bin/env python

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

"""
Define a variadic function:

    >>> @variadic(int)
    ... def f(*xs):
    ...   return xs

It can be called with a variable number of arguments,
and they are passed to decorated function as a single, iterable, parameter:

    >>> f()
    ()
    >>> f(1)
    (1,)
    >>> f(1, 2, 3, 4)
    (1, 2, 3, 4)

But it can also be called with lists (any iterable, in fact) of arguments:

    >>> f([])
    ()
    >>> f([1, 2, 3], [4, 5, 6])
    (1, 2, 3, 4, 5, 6)
    >>> f(xrange(1, 4))
    (1, 2, 3)

And you can even mix them:

    >>> f(1, [2, 3], 4, xrange(5, 8))
    (1, 2, 3, 4, 5, 6, 7)
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
# - add a doctest showing stack trace when decorated function raises
# - autodoc a decorated function


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
    Make a function very-variadic.
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
        spec = inspect.getargspec(wrapped)
        name = wrapped.__name__

        assert spec.varargs is not None

        # Example was generated with print ast.dump(ast.parse("def f(a, b, *args, **kwds): return call_wrapped((a, b), args, kwds)"), include_attributes=True)
        # http://code.activestate.com/recipes/578353-code-to-source-and-back/ helped a lot
        # http://stackoverflow.com/questions/10303248#29927459
        if sys.hexversion < 0x03000000:
            wrapper_ast_args = ast.arguments(
                    args=[ast.Name(id=a, ctx=ast.Param(), lineno=1, col_offset=0) for a in spec.args],
                    vararg=spec.varargs,
                    kwarg=spec.keywords,
                    defaults=[]
                )
        else:
            wrapper_ast_args = ast.arguments(
                args=[ast.arg(arg=a, annotation=None, lineno=1, col_offset=0) for a in spec.args],
                vararg=None if spec.varargs is None else ast.arg(arg=spec.varargs, annotation=None, lineno=1, col_offset=0),
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None if spec.keywords is None else ast.arg(arg=spec.keywords, annotation=None, lineno=1, col_offset=0),
                defaults=[]
            )
        wrapper_ast = ast.Module(body=[ast.FunctionDef(
            name=name,
            args=wrapper_ast_args,
            body=[ast.Return(value=ast.Call(
                func=ast.Name(id="wrapped", ctx=ast.Load(), lineno=1, col_offset=0),
                args=[ast.Name(id=a, ctx=ast.Load(), lineno=1, col_offset=0) for a in spec.args],
                keywords=[],
                starargs=ast.Call(
                    func=ast.Name(id="flatten", ctx=ast.Load(), lineno=1, col_offset=0),
                    args=[ast.Name(id=spec.varargs, ctx=ast.Load(), lineno=1, col_offset=0)],
                    keywords=[], starargs=None, kwargs=None, lineno=1, col_offset=0
                ),
                kwargs=None if spec.keywords is None else ast.Name(id=spec.keywords, ctx=ast.Load(), lineno=1, col_offset=0),
                lineno=1, col_offset=0
            ), lineno=1, col_offset=0)],
            decorator_list=[],
            lineno=1,
            col_offset=0
        )])
        wrapper_code = [c for c in compile(wrapper_ast, "<not_a_file>", "exec").co_consts if isinstance(c, types.CodeType)][0]
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


if __name__ == "__main__":
    unittest.main()
