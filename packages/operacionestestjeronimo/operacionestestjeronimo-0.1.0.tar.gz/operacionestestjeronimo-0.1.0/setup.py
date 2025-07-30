from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name='operacionestestjeronimo',
    packages=find_packages(include=['operacionestest']),
    version='0.1.0',
    description="libreria de operaciones básicas",
    long_description=description,
    long_description_content_type="text/markdown",
    author='Jerónimo Loaiza',
    license='MIT',
    install_requires=[],
    python_requires=">=3.12.4" #El python que tenga instalado yo
)