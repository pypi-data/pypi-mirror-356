__author__ = "narmadha-raghu"
from setuptools import setup, find_packages

setup(
    name="narmadhar_calculator",
    version="0.1.0",
    author="Narmadha R",
    author_email="narmadharam26@gmail.com",
    description="A simple calculator package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
