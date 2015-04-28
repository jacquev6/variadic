#!/usr/bin/env python
# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import setuptools

version = "0.0.0"


setuptools.setup(
    name="variadic",
    version=version,
    description="Decorator for very-variadic functions",
    author="Vincent Jacques",
    author_email="vincent@vincent-jacques.net",
    url="http://pythonhosted.org/variadic",
    py_modules=["variadic"],
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ],
    test_suite="variadic",
    use_2to3=True,
    command_options={
        "build_sphinx": {
            "version": ("setup.py", version),
            "release": ("setup.py", version),
            "source_dir": ("setup.py", "doc"),
        },
    }
)
