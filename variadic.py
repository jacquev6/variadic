#!/usr/bin/env python

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import itertools
import unittest


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
        return wrapper
    return decorator


class PurelyVariadicFunctionTestCase(unittest.TestCase):
    def setUp(self):
        @variadic(int)
        def f(xs):
            return list(xs)
        self.f = f

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
