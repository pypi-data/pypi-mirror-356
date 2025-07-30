from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name='operacionesmarlon',
    packages=find_packages(include=['operacionesmarlon']),
    version='0.1.0',    # arquitectura, clases, funciones
    description="libreria de operaciones básicas",
    long_description=description,
    long_description_content_type="text/markdown",
    author='Marlon García',
    license='UdeA',
    install_requires=[],
    python_requires=">=3.11.13"
)
