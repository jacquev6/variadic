#!/usr/bin/env python

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

"""
Define a function:

    >>> @variadic(int)
    ... def f(args):
    ...   return list(args)
    >>> f(1, 2, [3, 4], xrange(5, 8))
    [1, 2, 3, 4, 5, 6, 7]
"""

import functools
import itertools
import unittest

# Todo-list:
# - allow passing the flatten function instead of typ
# - allow an even simpler usage without any parameters
# - make sure exceptions never show any internals like wrapped, wrapper, call_wrapper, etc.
# - handle default arguments (the last parameter should have [] as default argument)


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
        def wrapper(*args):
            return wrapped(flatten(args))
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


if __name__ == "__main__":
    unittest.main()
