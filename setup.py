from setuptools import setup, find_packages

setup(
    name = 'sudokuslayer',
    version = '1.0',
    packages = find_packages(exclude='tests'),
    long_description = open('README.md').read()
)