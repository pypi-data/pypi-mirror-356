# setup.py
from setuptools import setup, find_packages

setup(
    packages=find_packages(where=".", exclude=("tests", "tests.*")),
    include_package_data=True,
)