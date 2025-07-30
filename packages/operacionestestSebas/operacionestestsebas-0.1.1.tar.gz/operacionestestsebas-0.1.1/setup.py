from setuptools import find_packages, setup
with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name='operacionestestSebas',
    packages=find_packages(include=['operaciones']),
    version='0.1.1',
    description="libreria de operaciones básicas",
    long_description=description,
    long_description_content_type="text/markdown",
    author='Alexis Ruales',
    license='MIT',
    install_requires=[],
    python_requires=">=3.11.13"
)
