from setuptools import find_packages
from setuptools import setup

setup(
    name='teleop_twist_keyboard',
    version='2.4.1',
    packages=find_packages(
        include=('teleop_twist_keyboard', 'teleop_twist_keyboard.*')),
)
