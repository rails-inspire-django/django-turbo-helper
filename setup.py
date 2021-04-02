#!/usr/bin/env python
# Third Party Libraries
from setuptools import setup

version = "0.0.40"

setup(
    name="django-turbo-response",
    version=version,
    author="Dan Jacob",
    author_email="danjac2018@gmail.com",
    url="https://github.com/hotwire-django/django-turbo-response",
    description="Hotwired/Turbo response helpers for Django",
    long_description=open("README.md").read() + "\n\n" + open("CHANGES.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.7",
    requires=["django (>=3.0)"],
    packages=["turbo_response"],
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
