from setuptools import find_packages, setup




with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name='operacionestest',
    packages=find_packages(include=['operacionestest']),
    version='0.1.0',  # arquitectura de la libreria, clases o cambios grandes , funciones o cambios pequenos
    description="libreria de operaciones básicas",
    long_description=description,
    long_description_content_type="text/markdown",
    author='Alexis Ruales',
    license='MIT',
    install_requires=[],
    python_requires=">=3.12.4"
)
