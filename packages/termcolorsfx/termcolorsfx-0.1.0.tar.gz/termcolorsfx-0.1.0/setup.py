from setuptools import setup, find_packages

setup(
    name="termcolorsfx",
    version="0.1.0",
    author="Vignesh Selvaraj",
    description="Advanced terminal color formatting and logging",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
)
