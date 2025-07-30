#!/usr/bin/env python3
# coding: utf-8
import os
import re

import setuptools
from setuptools import find_namespace_packages

# import joker; exit(1)
# DO NOT import your package from your setup.py

namespace = "m14"
package_name = "meta"
description = "experimental utilities for m14 projects"


def read(filename):
    with open(filename) as f:
        return f.read()


def version_find():
    if namespace:
        path = "{}/{}/__init__.py".format(namespace, package_name)
    else:
        path = "{}/__init__.py".format(package_name)
    root = os.path.dirname(__file__)
    path = os.path.join(root, path)
    regex = re.compile(r"""^__version__\s*=\s*('|"|'{3}|"{3})([.\w]+)\1\s*(#|$)""")
    # print('path', path)
    with open(path) as fin:
        for line in fin:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            mat = regex.match(line)
            if mat:
                return mat.groups()[1]
    raise ValueError("__version__ definition not found")


config = {
    "name": "m14",
    "version": version_find(),
    "description": "" + description,
    "keywords": "m14",
    "url": "",
    "author": "frozflame",
    "author_email": "frozflame@outlook.com",
    "license": "GNU General Public License (GPL)",
    "packages": find_namespace_packages(include=["m14.*"]),
    "namespace_packages": ["m14"],
    "zip_safe": False,
    "install_requires": read("requirements.txt"),
    "classifiers": [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    # ensure copy static file to runtime directory
    "include_package_data": True,
    "long_description": read("README.md"),
    "long_description_content_type": "text/markdown",
}

setuptools.setup(**config)
