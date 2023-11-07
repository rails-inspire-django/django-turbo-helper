#!/usr/bin/env python
from setuptools import find_packages, setup

VERSION = "1.0.1"

setup(
    name="django-turbo-response",
    version=VERSION,
    author="Dan Jacob",
    author_email="danjac2018@gmail.com",
    url="https://github.com/hotwire-django/django-turbo-response",
    description="Hotwired/Turbo response helpers for Django",
    long_description=open("README.md").read() + "\n\n" + open("CHANGELOG.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.8",
    requires=["django (>=3.0)"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
