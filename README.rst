.. GENI: intro
.. GENERATED SECTION, MANUAL EDITS WILL BE LOST

*variadic* is a Python (2.7+ and 3.4+) `function decorator <https://docs.python.org/2/glossary.html#term-decorator>`_
to write variadic functions accepting a mix of arguments and iterables of those arguments.
Oh, and they keep their `argspec <https://docs.python.org/2/library/inspect.html#inspect.getargspec>`_,
so tools doing introspection (Sphinx doc, IDEs, etc.) will work well.
No ugly ``f(*args, **kwds)`` in your doc!

Note that `PEP 448 <https://www.python.org/dev/peps/pep-0448/>`_ makes *variadic* obsolete:
**if you're using Python 3.5+, you should keep plain variadic functions and call them with several argument unpackings.**

.. END OF GENERATED SECTION

.. GENI: info
.. GENERATED SECTION, MANUAL EDITS WILL BE LOST

It's licensed under the `MIT license <http://choosealicense.com/licenses/mit/>`_.
It's available on the `Python package index <http://pypi.python.org/pypi/variadic>`_.
Its `documentation <http://jacquev6.github.io/variadic>`_
and its `source code <https://github.com/jacquev6/variadic>`_ are on GitHub.

.. END OF GENERATED SECTION

.. GENI: badges
.. GENERATED SECTION, MANUAL EDITS WILL BE LOST

Questions? Remarks? Bugs? Want to contribute? `Open an issue <https://github.com/jacquev6/variadic/issues>`_!

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

.. image:: https://img.shields.io/github/forks/jacquev6/variadic.svg
    :target: https://github.com/jacquev6/variadic/network

.. image:: https://img.shields.io/github/stars/jacquev6/variadic.svg
    :target: https://github.com/jacquev6/variadic/stargazers

.. END OF GENERATED SECTION

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
