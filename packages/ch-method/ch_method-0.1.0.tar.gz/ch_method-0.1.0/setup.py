# setup.py
from setuptools import setup, find_packages

setup(
    name="ch_method",
    version="0.1.0",
    description="The middle atmosphere temperature and density retrieval by using the Rayleigh lidar data",
    author="Aching Wu",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "nrlmsise00",
        "datetime",
    ],
    python_requires=">=3.7",
)
