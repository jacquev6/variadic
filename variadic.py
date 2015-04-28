#!/usr/bin/env python

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

"""
Define a variadic function:

    >>> @variadic(int)
    ... def f(args):
    ...   return list(args)

It can be called with a variable number of arguments,
and they are passed to decorated function as a single, iterable, parameter:

    >>> f()
    []
    >>> f(1)
    [1]
    >>> f(1, 2, 3, 4)
    [1, 2, 3, 4]

But it can also be called with lists (any iterable, in fact) of arguments:

    >>> f([])
    []
    >>> f([1, 2, 3], [4, 5, 6])
    [1, 2, 3, 4, 5, 6]
    >>> f(xrange(1, 4))
    [1, 2, 3]

And you can even mix them:

    >>> f(1, [2, 3], 4, xrange(5, 8))
    [1, 2, 3, 4, 5, 6, 7]
"""

import functools
import inspect
import itertools
import unittest

# Todo-list:
# - allow passing the flatten function instead of typ
# - allow an even simpler usage without any parameters
# - add a parameter string to be prepended or appended to the docstring
# - support decorating callables that are not functions?
# - verify that closures are preserved


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

        assert len(spec.args) >= 1
        assert spec.defaults is None or spec.defaults[-1] == []
        assert spec.varargs is None

        new_spec = inspect.ArgSpec(
            args=spec.args[:-1],
            varargs=spec.args[-1],
            defaults=None if spec.defaults is None else spec.defaults[:-1],
            keywords=spec.keywords,
        )

        def call_wrapped(*args, **kwds):
            args = list(args)
            args[-1] = flatten(args[-1])
            return wrapped(*args, **kwds)

        prototype = list(new_spec.args)
        prototype.append("*{}".format(new_spec.varargs))
        if new_spec.keywords is not None:
            prototype.append("**{}".format(new_spec.keywords))

        call = list(new_spec.args)
        call.append(new_spec.varargs)
        if new_spec.keywords is not None:
            call.append("**{}".format(new_spec.keywords))

        source = "def {name}({proto}): return {name}_({call})".format(
            name=name,
            proto=", ".join(prototype),
            call=", ".join(call),
        )
        exec_globals = {"{}_".format(name): call_wrapped}
        exec source in exec_globals
        wrapper = exec_globals[name]
        wrapper.__defaults__ = new_spec.defaults
        functools.update_wrapper(wrapper, wrapped)
        return wrapper
    return decorator


class PurelyVariadicFunctionTestCase(unittest.TestCase):
    def setUp(self):
        @variadic(int)
        def f(xs):
            "f's doc"
            return list(xs)
        self.f = f

    def test_name_is_preserved(self):
        self.assertEqual(self.f.__name__, "f")

    def test_doc_is_preserved(self):
        self.assertEqual(self.f.__doc__, "f's doc")

    def test_argspec_keeps_param_name(self):
        self.assertEqual(inspect.getargspec(self.f).varargs, "xs")

    def test_call_without_arguments(self):
        self.assertEqual(self.f(), [])

    def test_call_with_one_argument(self):
        self.assertEqual(self.f(1), [1])

    def test_call_with_several_arguments(self):
        self.assertEqual(self.f(1, 2, 3), [1, 2, 3])

    def test_call_with_one_list(self):
        self.assertEqual(self.f([1, 2, 3]), [1, 2, 3])

    def test_call_with_several_lists(self):
        self.assertEqual(self.f([1, 2], [3], [4, 5]), [1, 2, 3, 4, 5])

    def test_call_with_lists_and_arguments(self):
        self.assertEqual(self.f([1, 2], 3, 4, [5, 6], 7), [1, 2, 3, 4, 5, 6, 7])

    def test_call_with_keywords(self):
        with self.assertRaises(TypeError) as catcher:
            self.f(a=1)
        self.assertEqual(catcher.exception.args, ("f() got an unexpected keyword argument 'a'",))


class NotOnlyVariadicFunctionTestCase(unittest.TestCase):
    def test_args_before_varargs(self):
        @variadic(int)
        def f(a, b, xs):
            return a, b, list(xs)
        self.assertEqual(f(1, 2, 3, [4, 5], 6), (1, 2, [3, 4, 5, 6]))

    @variadic(int)
    def f(self, a, b, xs):
        return self, a, b, list(xs)

    def test_method(self):
        self.assertEqual(self.f(1, 2, 3, [4, 5], 6), (self, 1, 2, [3, 4, 5, 6]))

    def test_kwds_after_varargs(self):
        @variadic(int)
        def f(a, b, xs, **kwds):
            return a, b, list(xs), kwds
        self.assertEqual(f(1, 2, 3, [4, 5], 6, c=7, d=8), (1, 2, [3, 4, 5, 6], {"c": 7, "d": 8}))

    def test_defaults_on_args_before_varargs(self):
        default = object()  # To avoid implementations wich would stringify the default values and feed them to exec.
        @variadic(int)
        def f(a=None, b=default, xs=[]):
            return a, b, list(xs)
        self.assertEqual(f(), (None, default, []))


if __name__ == "__main__":
    unittest.main()
