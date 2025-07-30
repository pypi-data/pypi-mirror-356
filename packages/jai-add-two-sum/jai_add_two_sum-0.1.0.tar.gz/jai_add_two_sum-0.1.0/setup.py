__author__ = "narmadha-raghu"
from setuptools import setup, find_packages

setup(
    name="jai_add_two_sum",
    version="0.1.0",
    author="Jai",
    author_email="jai@gmail.com",
    description="",
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