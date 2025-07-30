from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="digiPYn", # Confirmed, this is your chosen package name. Make sure it's unique on PyPI!
    version="0.1.0",
    description="A Python library to convert between (address) latitude/longitude and DIGIPINs.",
    author="Kawsshikh Sajjana Gandla",
    author_email="kawsshikhsajjan7@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    python_requires=">=3.7",

    license="Apache-2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
    ],

    long_description=long_description,
    long_description_content_type='text/markdown',

    url="https://github.com/kawsshikh/digiPyn",
)