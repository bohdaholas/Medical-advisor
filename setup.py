from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name='Medical Advisor',
    version='1.0',
    packages=find_packages(),
    description="A package for analyzing health",
    long_description_content_type="text/markdown",
    long_description=long_description
)
