# setup.py

from setuptools import setup, find_packages

setup(
    name="shaksz",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[],
    author="Varun Verma",
    author_email="vermavarun@outlook.com",
    description="All coding and design solutions as package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vermavarun/shaksz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
