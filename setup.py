#!/usr/bin/env python
# Third Party Libraries
from setuptools import setup

version = "0.0.1"

setup(
    name="django-turbo-response",
    version=version,
    author="Dan Jacob",
    author_email="",
    url="",
    description="Hotwired/Turbo response helpers for Django",
    long_description=open("README.md").read() + "\n\n" + open("CHANGES.md").read(),
    license="AGPL license",
    requires=["django (>=3.1)"],
    packages=["turbo_response"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: AGPL License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
