#!/usr/bin/env python

from setuptools import setup
import imp

version = imp.load_source('thicc.version', 'version.py')

setup(
        name = 'thicc',
        version = version.version,
        description = "Very Basic C Compiler",
        author = "Geoffrey Ryan",
        packages = ['thicc'],
        scripts = ['scripts/thicc']
     )

