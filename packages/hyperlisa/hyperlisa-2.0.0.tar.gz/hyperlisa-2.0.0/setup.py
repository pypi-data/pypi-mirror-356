import os
import shutil
from setuptools import setup, find_packages

setup(
    name="hyperlisa",
    version="2.0.0",
    description="A package for combining source code files into one",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Omar Venturi",
    author_email="omar.venturi@hypertrue.com",
    url="https://github.com/moonClimber/hyperlisa",
    packages=find_packages(),
    package_data={
        "lisa": ["config.yaml.sample"],
    },
    include_package_data=True,
    install_requires=[
        "PyYAML>=5.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "combine-code=lisa._combine_code:main",
            "cmb=lisa._combine_code:main",
            "lisacmb=lisa._combine_code:main",
            "hyperlisacmb=lisa._combine_code:main",
            "hyperlisa-configure=lisa.configure:main",
            "hyperlisa-migrate=lisa.migrate:main",
        ],
    },
)
