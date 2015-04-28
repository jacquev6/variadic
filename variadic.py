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
# - make sure exceptions never show any internals like wrapped, wrapper, call_wrapper, etc.
# - handle default arguments (the last parameter should have [] as default argument)
# - add a parameter string to be prepended or appended to the docstring
# - support parameters before the variadic one
# - support default values
# - support **kwds
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
        assert spec.defaults is None
        assert spec.varargs is None
        assert spec.keywords is None

        new_spec = inspect.ArgSpec(
            args=spec.args[:-1],
            varargs=spec.args[-1],
            defaults=None,
            keywords=None,
        )

        def call_wrapped(posargs, varargs):
            args = list(posargs)
            args.append(flatten(varargs))
            return wrapped(*args)

        source = "def {name}({proto}): return {name}_(({call_1}), {call_2})".format(
            name=name,
            proto=", ".join(itertools.chain(new_spec.args, ["*{}".format(new_spec.varargs)])),
            call_1=", ".join(new_spec.args),
            call_2=new_spec.varargs,
        )
        exec_globals = {"{}_".format(name): call_wrapped}
        exec source in exec_globals
        wrapper = exec_globals[name]
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


if __name__ == "__main__":
    unittest.main()
