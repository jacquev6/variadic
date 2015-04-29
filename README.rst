variadic is a Python (2.7+ and 3.4+) `function decorator <https://docs.python.org/2/glossary.html#term-decorator>`__
to write variadic functions accepting a mix of arguments and iterables of those arguments.
Oh, and they keep their `argspec <https://docs.python.org/2/library/inspect.html#inspect.getargspec>`__,
so tools doing introspection (Sphinx doc, IDEs, etc.) will work well.
No ugly ``f(*args, **kwds)`` in your doc!

It's licensed under the `MIT license <http://choosealicense.com/licenses/mit/>`__.
It's available on the `Python package index <http://pypi.python.org/pypi/variadic>`__,
its `documentation is hosted by Python <http://pythonhosted.org/variadic>`__
and its source code is on `GitHub <https://github.com/jacquev6/variadic>`__.

Questions? Remarks? Bugs? Want to contribute? `Open an issue <https://github.com/jacquev6/variadic/issues>`__!

.. image:: https://img.shields.io/travis/jacquev6/variadic/master.svg
    :target: https://travis-ci.org/jacquev6/variadic

.. image:: https://img.shields.io/coveralls/jacquev6/variadic/master.svg
    :target: https://coveralls.io/r/jacquev6/variadic

.. image:: https://img.shields.io/codeclimate/github/jacquev6/variadic.svg
    :target: https://codeclimate.com/github/jacquev6/variadic

.. image:: https://img.shields.io/pypi/dm/variadic.svg
    :target: https://pypi.python.org/pypi/variadic

.. image:: https://img.shields.io/pypi/l/variadic.svg
    :target: https://pypi.python.org/pypi/variadic

.. image:: https://img.shields.io/pypi/v/variadic.svg
    :target: https://pypi.python.org/pypi/variadic

.. image:: https://pypip.in/py_versions/variadic/badge.svg
    :target: https://pypi.python.org/pypi/variadic

.. image:: https://pypip.in/status/variadic/badge.svg
    :target: https://pypi.python.org/pypi/variadic

.. image:: https://img.shields.io/github/issues/jacquev6/variadic.svg
    :target: https://github.com/jacquev6/variadic/issues

.. image:: https://img.shields.io/github/forks/jacquev6/variadic.svg
    :target: https://github.com/jacquev6/variadic/network

.. image:: https://img.shields.io/github/stars/jacquev6/variadic.svg
    :target: https://github.com/jacquev6/variadic/stargazers

Quick start
===========

Install from PyPI::

    $ pip install variadic

.. Warning, these are NOT doctests because doctests aren't displayed on GitHub.

Import::

    >>> from variadic import variadic

Define a function::

    >>> @variadic(int)
    ... def f(*args):
    ...   return args
    >>> f(1, 2, [3, 4], xrange(5, 8))
    (1, 2, 3, 4, 5, 6, 7)
