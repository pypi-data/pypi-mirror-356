#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


def read_requirements(filename):
    return [req.strip() for req in open(filename)]


setup(
    name="arkindex-client",
    version=open("VERSION").read().strip(),
    author="Teklia <contact@teklia.com>",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    package_data={"": ["*.rst", "LICENSE", "README"]},
    install_requires=read_requirements("requirements.txt"),
    python_requires=">=3.8",
    license="AGPL-v3",
    description="API client for the Arkindex project",
    long_description="""Documentation is available at https://api.arkindex.org""",
    keywords="api client arkindex",
    url="https://gitlab.teklia.com/arkindex/api-client",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Text Processing :: Linguistic",
    ],
)
