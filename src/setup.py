from setuptools import setup, find_packages

version_file = open('VERSION')
version = version_file.read().strip()

setup(name='crawler', version=version, packages=find_packages())