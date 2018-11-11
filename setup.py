#!/usr/bin/env python
# coding: utf8

# Copyright 2015-2018 Vincent Jacques <vincent@vincent-jacques.net>

import setuptools

version = "0.1.4"

setuptools.setup(
    name="variadic",
    version=version,
    description="Decorator for very-variadic functions",
    long_description=open("README.rst").read(),
    author="Vincent Jacques",
    author_email="vincent@vincent-jacques.net",
    url="http://jacquev6.github.io/variadic",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development",
    ],
    py_modules=["variadic"],
    use_2to3=True,
    convert_2to3_doctests=["variadic.py", "README.rst"],
    test_suite="variadic",
    command_options={
        "build_sphinx": {
            "version": ("setup.py", version),
            "release": ("setup.py", version),
            "source_dir": ("setup.py", "doc"),
        },
    },
)
