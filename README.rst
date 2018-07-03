*variadic* is a Python (2.7+ and 3.4+) `function decorator <https://docs.python.org/2/glossary.html#term-decorator>`__
to write variadic functions accepting a mix of arguments and iterables of those arguments.
Oh, and they keep their `argspec <https://docs.python.org/2/library/inspect.html#inspect.getargspec>`__,
so tools doing introspection (Sphinx doc, IDEs, etc.) will work well.
No ugly ``f(*args, **kwds)`` in your doc!

Note that `PEP 448 <https://www.python.org/dev/peps/pep-0448/>`_ makes *variadic* obsolete:
**if you're using Python 3.5+, you should keep plain variadic functions and call them with several argument unpackings.**

It's licensed under the `MIT license <http://choosealicense.com/licenses/mit/>`__.
It's available on the `Python package index <http://pypi.python.org/pypi/variadic>`__,
its `documentation <http://jacquev6.github.io/variadic>`__
and its `source code <https://github.com/jacquev6/variadic>`__ are on GitHub.

Questions? Remarks? Bugs? Want to contribute? `Open an issue <https://github.com/jacquev6/variadic/issues>`__!

.. image:: https://img.shields.io/travis/jacquev6/variadic/master.svg
    :target: https://travis-ci.org/jacquev6/variadic

.. image:: https://img.shields.io/coveralls/jacquev6/variadic/master.svg
    :target: https://coveralls.io/r/jacquev6/variadic

.. image:: https://img.shields.io/codeclimate/github/jacquev6/variadic.svg
    :target: https://codeclimate.com/github/jacquev6/variadic

.. image:: https://img.shields.io/scrutinizer/g/jacquev6/variadic.svg
    :target: https://scrutinizer-ci.com/g/jacquev6/variadic

.. image:: https://img.shields.io/pypi/dm/variadic.svg
    :target: https://pypi.python.org/pypi/variadic

.. image:: https://img.shields.io/pypi/l/variadic.svg
    :target: https://pypi.python.org/pypi/variadic

.. image:: https://img.shields.io/pypi/v/variadic.svg
    :target: https://pypi.python.org/pypi/variadic

.. image:: https://img.shields.io/pypi/pyversions/variadic.svg
    :target: https://pypi.python.org/pypi/variadic

.. image:: https://img.shields.io/pypi/status/variadic.svg
    :target: https://pypi.python.org/pypi/variadic

.. image:: https://img.shields.io/github/issues/jacquev6/variadic.svg
    :target: https://github.com/jacquev6/variadic/issues

.. image:: https://badge.waffle.io/jacquev6/variadic.png?label=ready&title=ready
    :target: https://waffle.io/jacquev6/variadic

.. image:: https://img.shields.io/github/forks/jacquev6/variadic.svg
    :target: https://github.com/jacquev6/variadic/network

.. image:: https://img.shields.io/github/stars/jacquev6/variadic.svg
    :target: https://github.com/jacquev6/variadic/stargazers

Quick start
===========

Install from PyPI::

    $ pip install variadic

Import:

>>> from variadic import variadic

Define a function:

>>> @variadic(int)
... def f(*args):
...   return args
>>> f(1, 2, [3, 4], xrange(5, 8))
(1, 2, 3, 4, 5, 6, 7)
