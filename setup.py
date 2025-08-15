from setuptools import setup, find_packages

setup(
    name="libDEA",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "ortools",
    ],
    python_requires=">=3.7",
    author="aav-antonov",
    description="A DEA library",
)