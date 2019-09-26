#!/usr/bin/env python

from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = set()
with open( "requirements/pc2.txt" ) as f:
  for dep in f.read().split('\n'):
      if dep.strip() != '' and not dep.startswith('-e'):
          install_requires.add( dep )

setup(name='pc2-module',
      version='0.1',
      description='Base classes for integrating compute modules into the pc2 Framework',
      author='Thomas Maxwell',
      zip_safe=False,
      author_email='thomas.maxwell@nasa.gov',
      url='https://github.com/nasa-nccs-cds/pc2-module.git',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      install_requires=list(install_requires),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

