"""Kiki setup script."""

from setuptools import setup
from setuptools import find_packages


with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()


setup(
    name='kiki',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements
)
