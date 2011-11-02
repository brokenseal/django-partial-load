#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name = "django-partial-load",
    version = "0.1.1.alfa",
    author = "Callegari Davide",
    author_email = "admin@brokenseal.it",
    description = "Partially load pages loading block list",
    long_description = open("README").read(),
    license = "All rights reserved",
    url = "https://bitbucket.org/brokenseal/django-partial-load",
    packages=find_packages(),
    #install_requires= [], # I wish I could use pip better
    classifiers = [
        "Development Status :: 1 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: All rights reserved",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)